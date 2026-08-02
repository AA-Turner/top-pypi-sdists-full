# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Storage utilities for working with cloud object stores."""

import contextlib
import logging
import os
import threading
import time
from collections.abc import Iterator
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    import pyarrow.fs as pa_fs

_LOG = logging.getLogger(__name__)

_SLOW_LIST_INFO_MS_ENV = "GENEVA_SLOW_LIST_INFO_MS"
_SLOW_LIST_WARN_MS_ENV = "GENEVA_SLOW_LIST_WARN_MS"
_SLOW_LIST_INFO_MS_DEFAULT = 1000
_SLOW_LIST_WARN_MS_DEFAULT = 5000
_SLOW_LIST_WARN_RATE_LIMIT_SEC = 60.0

_slow_list_warn_last: dict[tuple[str, str], float] = {}
_slow_list_warn_lock = threading.Lock()


def _parse_threshold_ms(env: str, default: int) -> int:
    """Read an int threshold from ``env``; fall back to ``default`` if malformed.

    One of ``timed_list``'s callers swallows exceptions wholesale, so a bad
    env value (e.g. ``GENEVA_SLOW_LIST_INFO_MS=off``) must not raise out of
    the observability path — otherwise it silently disables the
    hierarchical/flat coexistence guard.
    """
    raw = os.environ.get(env)
    if raw is None:
        return default
    try:
        return int(raw)
    except (ValueError, TypeError):
        _LOG.warning("ignoring non-numeric %s=%r; using default %d", env, raw, default)
        return default


def _slow_list_thresholds_ms() -> tuple[int, int]:
    """Return (info_ms, warn_ms). A value of ``0`` disables that level."""
    return (
        _parse_threshold_ms(_SLOW_LIST_INFO_MS_ENV, _SLOW_LIST_INFO_MS_DEFAULT),
        _parse_threshold_ms(_SLOW_LIST_WARN_MS_ENV, _SLOW_LIST_WARN_MS_DEFAULT),
    )


def _should_warn(op: str, scope: str) -> bool:
    """Rate-limit WARN-level emissions per (op, scope[:64]) to once per window."""
    key = (op, scope[:64])
    now = time.monotonic()
    with _slow_list_warn_lock:
        last = _slow_list_warn_last.get(key, 0.0)
        if now - last < _SLOW_LIST_WARN_RATE_LIMIT_SEC:
            return False
        _slow_list_warn_last[key] = now
    return True


def timed_list(
    session: Any,
    scope: str | None,
    *,
    op: str,
    layout: str | None = None,
    root: str | None = None,
) -> list[str]:
    """``session.list(scope)`` with slow-list warning instrumentation.

    Drains the iterator and returns the full list so the timer measures the
    user-visible wall cost. Emits a single log line per call when elapsed
    crosses ``GENEVA_SLOW_LIST_INFO_MS`` (INFO) or
    ``GENEVA_SLOW_LIST_WARN_MS`` (WARNING). WARNING is rate-limited to once
    per 60 seconds per ``(op, scope)``.

    Parameters
    ----------
    session
        A ``LanceFileSession``-like object exposing ``.list(scope)``.
    scope
        Prefix passed to ``session.list``. May be ``None`` to list root.
    op
        Caller-supplied label (e.g. ``"list_keys"``, ``"deleted_markers"``).
        Used in the warning text and in WARN rate-limit bookkeeping.
    layout
        Optional layout tag (e.g. ``"flat"``, ``"hierarchical"``).
    root
        Optional root URI for the warning text. Pure context; not consulted
        for the LIST itself.
    """
    t0 = time.perf_counter()
    items = list(session.list(scope))
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    _emit_slow_list(op, layout, scope, len(items), elapsed_ms, root)
    return items


def timed_list_with_delimiter(
    session: Any,
    scope: str | None,
    *,
    op: str,
    layout: str | None = None,
    root: str | None = None,
) -> Any:
    """``session.list_with_delimiter(scope)`` with slow-list instrumentation.

    Non-recursive, path-delimited list: returns a ``lance.file.ListResult``
    whose ``common_prefixes`` are the immediate child "directories" and
    ``objects`` the immediate child files, both session-relative. Bounded by one
    level instead of the whole subtree, and blob-only on Azure (no
    hierarchical-namespace probe). Shares the slow-list warning thresholds with
    :func:`timed_list`.
    """
    t0 = time.perf_counter()
    result = session.list_with_delimiter(scope)
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    n_items = len(result.common_prefixes) + len(result.objects)
    _emit_slow_list(op, layout, scope, n_items, elapsed_ms, root)
    return result


def _emit_slow_list(
    op: str,
    layout: str | None,
    scope: str | None,
    n_items: int,
    elapsed_ms: float,
    root: str | None,
) -> None:
    """Log a single slow-list line when ``elapsed_ms`` crosses a threshold."""
    info_ms, warn_ms = _slow_list_thresholds_ms()
    scope_str = scope if scope is not None else ""

    if warn_ms and elapsed_ms >= warn_ms and _should_warn(op, scope_str):
        _LOG.warning(
            "slow list: op=%s layout=%s scope=%r items=%d elapsed=%.2fs store=%s",
            op,
            layout or "-",
            scope_str,
            n_items,
            elapsed_ms / 1000.0,
            root or "-",
        )
    elif info_ms and elapsed_ms >= info_ms:
        _LOG.info(
            "slow list: op=%s layout=%s scope=%r items=%d elapsed=%.2fs store=%s",
            op,
            layout or "-",
            scope_str,
            n_items,
            elapsed_ms / 1000.0,
            root or "-",
        )


def get_azure_storage_account() -> str:
    """Get Azure storage account name from environment.

    Prefers AZURE_STORAGE_ACCOUNT_NAME over AZURE_STORAGE_ACCOUNT.
    """
    account = os.environ.get("AZURE_STORAGE_ACCOUNT_NAME") or os.environ.get(
        "AZURE_STORAGE_ACCOUNT"
    )
    if not account:
        raise ValueError(
            "AZURE_STORAGE_ACCOUNT_NAME must be set for az:// URIs. "
            "This is required for Azure Blob Storage access."
        )
    return account


_ENV_LOCK = threading.Lock()

# Maps an Azure service principal supplied via ``storage_options`` onto the
# ``AZURE_*`` env vars that pyarrow's ``AzureFileSystem`` reads (its internal
# ``DefaultAzureCredential`` resolves an ``EnvironmentCredential`` from these).
# Both the bare and ``azure_``-prefixed option spellings are accepted.
_AZURE_CREDENTIAL_ENV: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("AZURE_TENANT_ID", ("tenant_id", "azure_tenant_id")),
    ("AZURE_CLIENT_ID", ("client_id", "azure_client_id")),
    ("AZURE_CLIENT_SECRET", ("client_secret", "azure_client_secret")),
    (
        "AZURE_FEDERATED_TOKEN_FILE",
        ("federated_token_file", "azure_federated_token_file"),
    ),
)


def azure_credential_env(storage_options: dict[str, Any] | None) -> dict[str, str]:
    """Map an Azure service principal from ``storage_options`` to ``AZURE_*`` env.

    pyarrow's ``AzureFileSystem`` exposes no service-principal constructor
    params on the ``pyarrow>=16`` floor, so the portable way to pass an SP is
    through the environment, which its ``DefaultAzureCredential`` /
    ``EnvironmentCredential`` chain reads.
    """
    opts = storage_options or {}
    env: dict[str, str] = {}
    for env_key, option_keys in _AZURE_CREDENTIAL_ENV:
        for option_key in option_keys:
            value = opts.get(option_key)
            if value is not None:
                env[env_key] = str(value)
                break
    return env


@contextlib.contextmanager
def temporary_env(updates: dict[str, str]) -> Iterator[None]:
    """Set ``os.environ`` entries for the duration of the block, then restore.

    Serialized by a lock because ``os.environ`` is process-global and worker
    threads construct filesystems concurrently; interleaved updates would let
    one thread observe another's credentials.
    """
    if not updates:
        yield
        return
    with _ENV_LOCK:
        previous = {key: os.environ.get(key) for key in updates}
        try:
            os.environ.update(updates)
            yield
        finally:
            for key, old in previous.items():
                if old is None:
                    os.environ.pop(key, None)
                else:
                    os.environ[key] = old


def filesystem_from_uri(
    uri: str,
    *,
    storage_options: dict[str, str] | None,
) -> tuple["pa_fs.FileSystem", str]:
    """Create a PyArrow FileSystem from a URI, with Azure support.

    PyArrow's FileSystem.from_uri() doesn't auto-detect az:// URIs,
    so this function handles Azure URIs by creating an AzureFileSystem explicitly.

    For Azure, the storage account name is read from ``storage_options``
    (``account_name`` or ``azure_storage_account_name``) and falls back to the
    ``AZURE_STORAGE_ACCOUNT_NAME`` environment variable. Authentication uses
    DefaultAzureCredential (workload identity, managed identity, Azure CLI, etc.)
    unless ``account_key`` is supplied in ``storage_options``.

    Parameters
    ----------
        uri
            Storage URI (e.g., "s3://bucket/path", "gs://bucket/path", "az://container/path")
        storage_options
            Optional cloud storage options (forwarded for Azure).

    Returns
    -------
        Tuple of (FileSystem, path) where path is the path within the filesystem

    Raises
    ------
        ValueError
            If Azure URI is used but no account_name is available in
            ``storage_options`` or the ``AZURE_STORAGE_ACCOUNT_NAME`` env var.
    """
    import pyarrow.fs as fs

    if uri.startswith("az://"):
        opts = storage_options or {}
        account_name = (
            opts.get("account_name")
            or opts.get("azure_storage_account_name")
            or get_azure_storage_account()
        )
        path = uri.removeprefix("az://")
        # Build kwargs from non-None values only. `sas_token` landed in
        # pyarrow 20.0.0 (apache/arrow#45705); workers running an older
        # pyarrow that still satisfies geneva's `pyarrow>=16` floor have
        # AzureFileSystem but no `sas_token` param, so passing
        # `sas_token=None` raises `TypeError: __init__() got an unexpected
        # keyword argument 'sas_token'`. Notebook (uv-locked at pyarrow 20)
        # and worker (pyarrow from the Ray base image — pip won't upgrade
        # an already-satisfied dep) can disagree.
        azure_kwargs: dict = {"account_name": account_name}
        account_key = opts.get("account_key") or opts.get("azure_storage_account_key")
        if account_key:
            azure_kwargs["account_key"] = account_key
        sas_token = opts.get("sas_token") or opts.get("azure_storage_sas_token")
        if sas_token:
            azure_kwargs["sas_token"] = sas_token
        with temporary_env(azure_credential_env(opts)):
            azure_fs = fs.AzureFileSystem(**azure_kwargs)  # type: ignore[arg-type]
        return azure_fs, path

    return fs.FileSystem.from_uri(uri)
