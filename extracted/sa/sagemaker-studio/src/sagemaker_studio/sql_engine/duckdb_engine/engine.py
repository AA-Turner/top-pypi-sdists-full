"""The kernel's DuckDB engine: set up once, on first use, then run one statement at a time."""

import logging
import re
import threading
from typing import List

from sagemaker_studio import local_kernel
from sagemaker_studio.exceptions import (
    AccessDeniedError,
    CredentialsExpiredError,
    CredentialsUnavailableError,
)
from sagemaker_studio.sql_engine.duckdb_engine import _one_row, catalogs, extensions

logger = logging.getLogger(__name__)

_duckdb = None
#: Re-entrant lock over what the SDK does on the engine: set-up, the credential-chain secret, every
#: statement :func:`_run_local_duckdb` runs, and the catalog rounds (``duckdbutils``), so a statement
#: runs before or after a reset or round, never during one. Per statement, not per cell, and not
#: over a Python cell's own ``duckdb.sql()``. Taken before :class:`.catalogs.LocalCatalogs`' locks.
_lock = threading.RLock()


def _ensure_duckdb():
    """The kernel's DuckDB engine, set up once on the first call, on DuckDB's default session: the
    extension baseline when a bundle exists, the settings, the credential-chain secret
    (:func:`_sync_ambient_s3_secret`, which signs a connection-less cell's ``s3://`` reads) and the
    configuration lock. Every later call returns the engine and runs nothing; a cell and a catalog
    round each take it once. A signed-out local kernel still comes up; only its S3 reads are refused.
    """
    global _duckdb, _ambient_s3_secret, _ambient_s3_secret_unavailable, _default_aws_credentials_disabled
    with _lock:
        if _duckdb is not None:
            return _duckdb
        import duckdb

        # A new engine holds no secret yet, and its aws fallback is on, whatever an earlier one
        # did.
        _ambient_s3_secret = False
        _ambient_s3_secret_unavailable = False
        _default_aws_credentials_disabled = False

        # DuckDB's default session in both modes (shared with a cell's own duckdb.sql(), whose
        # tables and settings remain); the same baseline wherever a bundle exists.
        extension_directory = extensions._duckdb_bundle_directory(duckdb)
        logger.info(
            "Setting up the kernel's DuckDB engine (%s; extension bundle: %s)",
            "AWS Notebook local kernel" if local_kernel.is_local_kernel() else "remote compute",
            extension_directory or "none",
        )
        if extension_directory:
            extensions._apply_baseline(duckdb, extension_directory)
        # Refer to https://duckdb.org/duckdb-docs.pdf
        duckdb.sql("SET python_scan_all_frames = true;")
        try:
            _sync_ambient_s3_secret(duckdb)
        except Exception:
            # Signed out on a local kernel is a normal state, not a broken engine.
            if extension_directory and not local_kernel.is_local_kernel():
                raise
            # Without a bundle DuckDB downloads the aws extension here, which fails offline;
            # local queries still work.
            _log_ambient_s3_secret_failure()
        if extension_directory:
            extensions._lock_configuration(duckdb)
        # Cache only once set up: a failed setup must leave later calls retrying it, not running
        # on a half-set-up connection.
        _duckdb = duckdb
        return _duckdb


#: The ``aws`` extension's own fallback (DuckDB 2.0): for an ``s3://`` path no secret matches, it
#: resolves the default credential chain once and keeps that identity for the database's lifetime.
#: Off, so the SDK's secrets are the only credentials DuckDB signs with and a signed-out read gets
#: none rather than a cached identity. GLOBAL, so a cursor on the database sees it too.
_DISABLE_DEFAULT_AWS_CREDENTIALS_STATEMENT = "SET GLOBAL aws_default_credentials = false;"
#: Whether the fallback is off. The setting exists only once the ``aws`` extension is loaded (without
#: a bundle, possibly long after set-up), so the switch is tried after every chain-secret attempt
#: until it takes; once set it holds.
_default_aws_credentials_disabled = False


def _disable_default_aws_credentials(duck) -> None:
    """Switch the ``aws`` extension's default-chain fallback off unless it already is. A DuckDB
    without the setting (an older extension, or one not loaded yet) is left as it is, at DEBUG."""
    global _default_aws_credentials_disabled
    with _lock:
        if _default_aws_credentials_disabled:
            return
        try:
            duck.sql(_DISABLE_DEFAULT_AWS_CREDENTIALS_STATEMENT)
        except Exception:  # noqa: BLE001 - the setting does not exist on this DuckDB, or not yet
            logger.debug(
                "This DuckDB has no aws_default_credentials setting (yet); nothing switched off",
                exc_info=True,
            )
            return
        _default_aws_credentials_disabled = True
        logger.info("The aws extension's default-credential fallback is switched off")


def _log_ambient_s3_secret_failure() -> None:
    """Say the credential-chain secret could not be made: a warning, or on a local kernel, where
    being signed out is a normal state, a notice."""
    if local_kernel.is_local_kernel():
        logger.info(
            "No AWS credentials to resolve for DuckDB's S3 secret (signed out?); S3 reads need a sign-in",
            exc_info=True,
        )
    else:
        logger.warning(
            "Could not create the DuckDB S3 secret; S3 access from DuckDB is unavailable",
            exc_info=True,
        )


#: DuckDB's name for an unnamed ``s3`` secret, which is what the credential-chain secret is.
_AMBIENT_S3_SECRET_NAME = "__default_s3"
#: The credential-chain secret: the ``aws`` extension resolves the AWS credential chain and, with
#: ``REFRESH auto``, resolves it again when the credentials it holds stop working. Refer to
#: https://duckdb.org/docs/stable/core_extensions/aws#credential_chain-provider
_AMBIENT_S3_SECRET_STATEMENT = "CREATE SECRET (TYPE s3, PROVIDER credential_chain, REFRESH auto);"
#: Whether the engine currently holds the credential-chain secret.
_ambient_s3_secret = False
#: Whether creating it failed (offline without the aws extension; signed out on a local kernel):
#: not retried on every statement, only when a statement needs S3 or on a reset.
_ambient_s3_secret_unavailable = False


def _sync_ambient_s3_secret(duck) -> None:
    """
    Make sure the engine holds the credential-chain secret: at set-up, in every catalog round
    (:func:`_reset_ambient_s3_secret`) and for the first ``s3://`` read after a drop
    (:func:`_require_ambient_s3_secret`, :func:`_resume_ambient_s3_secret`). A failure to create it
    is raised once, then not retried until the next drop or :func:`_require_ambient_s3_secret`.
    """
    global _ambient_s3_secret, _ambient_s3_secret_unavailable
    with _lock:
        if _ambient_s3_secret or _ambient_s3_secret_unavailable:
            return
        try:
            duck.sql(_AMBIENT_S3_SECRET_STATEMENT)
        except Exception:
            _ambient_s3_secret_unavailable = True
            raise
        finally:
            # The attempt loaded the aws extension (if the baseline had not): its fallback can be
            # switched off now.
            _disable_default_aws_credentials(duck)
        _ambient_s3_secret = True


def _require_ambient_s3_secret(duck) -> None:
    """
    A local-kernel ``s3://`` read needs the credential-chain secret: try once more to create it
    when an earlier attempt failed (signed out then), and refuse the read before it runs when it
    still cannot be made.

    Raises:
        CredentialsUnavailableError: The chain resolves no credentials (signed out).
    """
    global _ambient_s3_secret_unavailable
    with _lock:
        if _ambient_s3_secret:
            return
        _ambient_s3_secret_unavailable = False
        try:
            _sync_ambient_s3_secret(duck)
        except Exception as e:  # noqa: BLE001 - DuckDB's reason, typed for the user
            raise CredentialsUnavailableError(
                "Reading S3 from DuckDB", str(e).splitlines()[0]
            ) from e


def _resume_ambient_s3_secret(duck) -> None:
    """An ``s3://`` read outside a local kernel after a drop: make the credential-chain secret
    again. When that fails it is logged, not retried until the next drop, and the read gets DuckDB's
    own error."""
    with _lock:
        try:
            _sync_ambient_s3_secret(duck)
        except Exception:  # noqa: BLE001 - logged; DuckDB says what the read lacks
            _log_ambient_s3_secret_failure()


def _drop_ambient_s3_secret() -> None:
    """Drop the credential-chain secret (sign-out, kernel reset); the next round or ``s3://`` read
    re-creates it from the chain of then."""
    global _ambient_s3_secret, _ambient_s3_secret_unavailable
    with _lock:
        if _ambient_s3_secret and _duckdb is not None:
            try:
                _duckdb.sql(f"DROP SECRET IF EXISTS {_AMBIENT_S3_SECRET_NAME};")
            except Exception:  # noqa: BLE001 - best effort
                logger.warning(
                    "Could not drop DuckDB secret %s; it stays until the next drop",
                    _AMBIENT_S3_SECRET_NAME,
                    exc_info=True,
                )
        _ambient_s3_secret = False
        _ambient_s3_secret_unavailable = False


def _reset_ambient_s3_secret(duck) -> None:
    """Drop the credential-chain secret and create it again, so it holds what the chain resolves
    now (every catalog round: sign-in, profile switch). When it cannot be created (signed out), S3
    reads say so when they run."""
    with _lock:
        _drop_ambient_s3_secret()
        try:
            _sync_ambient_s3_secret(duck)
        except Exception:
            _log_ambient_s3_secret_failure()


local_kernel.add_reset_listener(_drop_ambient_s3_secret)


def _run_local_duckdb(duck, statement: str):
    """
    Run one statement of a cell with no connection on ``duck``, the cell's engine (a cell with a
    connection runs on the connection's own engine, never here). A statement reading ``s3://``
    first makes sure of the credential-chain secret: on a local kernel it is refused before it runs
    when there is none (:func:`_require_ambient_s3_secret`) and a refusal AWS answers is typed
    (:func:`_classify_duckdb_error`); elsewhere DuckDB says what the read lacks. Under the engine's
    lock from that check to the end of the read.
    """
    with _lock:
        reads_s3 = bool(_s3_uris(statement))
        if not local_kernel.is_local_kernel():
            if reads_s3:
                _resume_ambient_s3_secret(duck)
            relation = duck.sql(statement)
            return relation.df() if relation else None
        if reads_s3:
            _require_ambient_s3_secret(duck)
        try:
            # DuckDB reads lazily: the S3 request, and so a refusal, can surface at ``.df()``
            # rather than at ``.sql()``, so both run under the classifier.
            relation = duck.sql(statement)
            return relation.df() if relation else None
        except Exception as e:  # noqa: BLE001 - classify, then re-raise what is not ours
            raise _classify_duckdb_error(e, statement, _current_search_path(duck)) from e


def _current_search_path(duck) -> str:
    """DuckDB's ``search_path`` now (a cell's catalog is first on it while the cell runs); ``""`` when it cannot be read."""
    try:
        row = _one_row(duck, "SELECT current_setting('search_path')")
    except Exception:  # noqa: BLE001 - for an error message only
        return ""
    return str(row[0]) if row and row[0] is not None else ""


_S3_URI_PATTERN = re.compile(r"s3://[^\s'\"`()\[\]{}<>]+", re.IGNORECASE)


def _s3_uris(statement: str) -> List[str]:
    """The ``s3://`` locations ``statement`` names."""
    return _S3_URI_PATTERN.findall(statement)


_EXPIRED_CREDENTIALS_MARKERS = ("ExpiredToken", "InvalidAccessKeyId", "SignatureDoesNotMatch")
_REFUSED_CREDENTIALS_MARKERS = _EXPIRED_CREDENTIALS_MARKERS + (
    "HTTP 403",
    "403 (Forbidden)",
    "AccessDenied",
)


def _looks_like_refused_credentials(error: Exception) -> bool:
    message = str(error)
    return any(marker in message for marker in _REFUSED_CREDENTIALS_MARKERS)


def _classify_duckdb_error(error: Exception, statement: str, search_path: str = "") -> Exception:
    """
    The error to raise for ``error`` from a local-kernel DuckDB statement. AWS naming the token
    (expired, unknown key, bad signature) is :class:`CredentialsExpiredError`. Any other refusal
    (``403``, ``AccessDenied``) is :class:`AccessDeniedError`, naming who was refused: the signed-in
    identity (the SDK knows no account for it), or, when the statement reads no ``s3://`` path of
    its own and every attached catalog it ran against (``search_path``'s first entry and the names
    it qualifies) signs as one access role, that role and its connection. Anything else is
    returned unchanged.
    """
    message = str(error)
    if any(marker in message for marker in _EXPIRED_CREDENTIALS_MARKERS):
        return CredentialsExpiredError(message)
    if not _looks_like_refused_credentials(error):
        return error
    uris = _s3_uris(statement)
    signer = None if uris else catalogs._state.role_signing(statement, search_path)
    if signer is None:
        return AccessDeniedError(uris[0] if uris else "", detail=message)
    return AccessDeniedError(
        ", ".join(f"catalog {alias!r}" for alias in signer.aliases),
        detail=message,
        role=signer.role_arn,
        connections=signer.connections,
    )


def _resolve_pending_for_duckdb(duck, statement: str) -> None:
    """Resolve any ``PendingDataFrame`` proxies a DuckDB statement references, BEFORE the
    statement runs, asking ``duck`` (the cell's engine, see :func:`_run_local_duckdb`) which
    names it references.

    DuckDB (``python_scan_all_frames=true``) resolves a namespace name via its replacement
    scan, which validates the object **by type in the C++ engine** -- it bypasses the
    proxy's ``__getattr__``, so the proxy's access-triggered blocking never fires and
    DuckDB would reject the proxy with ``InvalidInputException`` instead of waiting.

    To give DuckDB only real frames, ask DuckDB itself which names the statement references
    (``con.get_table_names`` -- a structured ``set[str]``, no execution, no replacement scan
    on the proxy), and for each referenced name that is a ``PendingDataFrame`` in the
    namespace, block on ``_resolve()`` (which rebinds it to the real DataFrame). This is
    referenced-only: a pending df the statement does not touch is never resolved. Any name
    that is not a pending proxy (a real table, a CTE name) is simply skipped.

    Non-fatal DISCOVERY, propagating RESOLUTION: if ``get_table_names`` is unavailable or
    raises (parse edge case), we swallow it and let DuckDB run as it does today -- the
    discovery step is a best-effort optimization. But once a referenced pending proxy is
    found, ``_resolve()`` deliberately PROPAGATES an upstream materialization failure or
    ``TimeoutError`` to the caller (surfacing a clear "upstream df failed/timed out" instead
    of a confusing DuckDB catalog error). So this is not a no-new-failure-surface guarantee
    on the resolution itself -- an upstream failure the statement genuinely depends on is
    meant to surface here.
    """
    try:
        from IPython import get_ipython
    except Exception:
        return
    ip = get_ipython()
    if ip is None:
        return

    from sagemaker_studio.utils.pending_dataframe import PendingDataFrame

    # Snapshot the namespace before scanning: background materialize threads bind new names
    # (df_0, df_1, ...) into ip.user_ns concurrently, so iterating the live view can raise
    # "dictionary changed size during iteration" (#8). A list() snapshot is a point-in-time
    # copy of references -- but list() ITSELF iterates the dict view, so a bind landing
    # DURING the list() call raises the same RuntimeError. Retry a few times: binds are
    # brief, so a re-snapshot almost always lands in a quiet window. This is best-effort
    # pre-resolution; if every attempt races (pathological), fall through without the
    # snapshot and let DuckDB handle any still-pending proxy as it would today.
    ns_items = None
    for _attempt in range(5):
        try:
            ns_items = list(ip.user_ns.items())
            break
        except RuntimeError:
            continue
    if ns_items is None:
        return

    # Fast path: nothing pending in the namespace -> skip the get_table_names call entirely.
    if not any(isinstance(v, PendingDataFrame) for _k, v in ns_items):
        return

    ns_snapshot = dict(ns_items)
    try:
        referenced = duck.get_table_names(statement)
    except Exception:
        # get_table_names unavailable / parse edge case: fall through to today's behavior.
        logger.debug("duckdb get_table_names failed; skipping pending pre-resolve", exc_info=True)
        return

    for name in referenced:
        obj = ns_snapshot.get(name)
        if isinstance(obj, PendingDataFrame):
            # Blocks until the referenced df materializes (or raises its terminal error /
            # times out). Rebinds the namespace name to the real frame as a side effect of
            # the background thread's commit; _resolve() also caches it on the proxy.
            obj._resolve()
