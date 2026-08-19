# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Vended-credential lifecycle: expiry detection, proactive and reactive re-vend.

The driver vends a short-lived storage token once at plan time and ships it into every
ScanTask, checkpoint store, table handle, and the fragment committer; any component that
outlives the token must refresh it or fail mid-job with 400/403 ExpiredToken.

Two refresh modes, shared by all call sites:

- **Proactive** — :func:`refresh_storage_options` re-vends once cached options
  enter the expiry safety window. Callers use it on their hot path (before an
  attempt) and then invalidate whatever they cached from the old options
  (object-store session, dataset handle, table handle).
- **Reactive** — :func:`force_revend_storage_options` re-vends unconditionally
  after :func:`is_credential_expiry_error` classifies a live failure. The error
  already proves the token is dead (early revocation / clock skew), so this
  bypasses the expiry window. Best-effort: failures warn and return ``None`` so
  the caller's retry surfaces the underlying error.
"""

from __future__ import annotations

import contextlib
import logging
import os
import time
from datetime import datetime
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable

    from lance_namespace import LanceNamespace

    from geneva.db import NamespaceConfig

_LOG = logging.getLogger(__name__)


VENDED_EXPIRY_KEY = "expires_at_millis"

# Re-vend this far ahead of the stated expiry so an in-flight request never
# signs with a token that lapses between the check and the S3 round-trip.
CREDENTIAL_REFRESH_SAFETY_MS = 5 * 60 * 1000
CREDENTIAL_REFRESH_SAFETY_MS_ENV = "GENEVA_CREDENTIAL_REFRESH_SAFETY_MS"


def credential_refresh_safety_ms() -> int:
    raw = os.environ.get(CREDENTIAL_REFRESH_SAFETY_MS_ENV)
    if raw is None:
        return CREDENTIAL_REFRESH_SAFETY_MS
    try:
        return int(raw)
    except ValueError:
        _LOG.warning(
            "invalid %s=%r; using default %d",
            CREDENTIAL_REFRESH_SAFETY_MS_ENV,
            raw,
            CREDENTIAL_REFRESH_SAFETY_MS,
        )
        return CREDENTIAL_REFRESH_SAFETY_MS


def is_credential_expiry_error(exception: BaseException) -> bool:
    """Detect a cloud object-store auth failure from expired vended credentials.

    Covers both clouds' vended-credential expiry:

    - **AWS** STS temp creds: usually ``403 ExpiredToken``, but a HEAD (no body)
      can surface as a bare ``400 Bad Request`` (``Generic S3 error``).
    - **Azure** user-delegation SAS: a ``403`` ``AuthenticationFailed`` with
      "Signature not valid in the specified time frame" / "Signed expiry time"
      (``Generic MicrosoftAzure error``).

    We gate on an object-store error marker AND an auth-ish signature so
    @retry_lance can re-vend and retry; a genuine non-credential error won't be
    fixed by re-vending and still gives up after the bounded attempts.
    """
    # TODO: need to better expose object store error reasons in namespace client
    msg = str(exception).lower()
    store_markers = ("s3 error", "object store error", "microsoftazure", "azure")
    if not any(m in msg for m in store_markers):
        return False
    auth_markers = (
        # Generic / AWS STS.
        "expired",
        "invalidtoken",
        "400 bad request",
        "403",
        "not authorized",
        "access denied",
        # Azure user-delegation SAS expiry.
        "authenticationfailed",
        "signature not valid",
        "signed expiry",
        "server failed to authenticate",
    )
    return any(m in msg for m in auth_markers)


def storage_options_need_refresh(
    storage_options: dict[str, str] | None,
    *,
    safety_ms: int | None = None,
    now_ms: int | None = None,
) -> bool:
    """Whether vended ``storage_options`` are within the safety window of expiry.

    ``safety_ms`` defaults to :func:`credential_refresh_safety_ms` (the
    env-tunable window). Returns ``False`` for static credentials (no
    ``expires_at_millis``) and for a missing/unparseable expiry, so non-vended
    tables never trigger re-vending.
    """
    if not storage_options:
        return False
    raw = storage_options.get(VENDED_EXPIRY_KEY)
    if raw is None:
        return False
    try:
        expires_ms = int(raw)
    except (TypeError, ValueError):
        return False
    if safety_ms is None:
        safety_ms = credential_refresh_safety_ms()
    if now_ms is None:
        now_ms = int(time.time() * 1000)
    return now_ms >= expires_ms - safety_ms


def table_handle_credentials_expiring(table: Any) -> bool:
    """True when a cached table handle's vended credentials are near expiry.

    Long-lived handles (the worker table cache, system-table managers) pin the
    storage options they were opened with; this scans both the handle's opening
    options and, when the inner lancedb table exposes it, the options currently
    live on the dataset. A no-op (``False``) for static credentials that carry
    no ``expires_at_millis``.
    """
    candidates = [getattr(table, "_storage_options", None)]
    ltbl = getattr(table, "_ltbl", None)
    latest = getattr(ltbl, "latest_storage_options", None)
    if callable(latest):
        # Best-effort; fall back to the static check on any error.
        with contextlib.suppress(Exception):
            candidates.append(latest())
    return any(storage_options_need_refresh(c) for c in candidates)


def log_vended_expiry(
    table_id: list[str] | None, storage_options: dict[str, str] | None
) -> None:
    expires_ms = (storage_options or {}).get(VENDED_EXPIRY_KEY)
    if expires_ms is None:
        return
    try:
        expires_local = datetime.fromtimestamp(int(expires_ms) / 1000).astimezone()
    except (TypeError, ValueError, OSError, OverflowError):
        return
    _LOG.debug(
        "vended credentials id=%s expires_at_millis=%s, local=%s",
        table_id,
        expires_ms,
        expires_local.isoformat(),
    )


def revend_storage_options(
    *,
    table_id: list[str] | None,
    namespace_client: LanceNamespace | None = None,
    namespace_config: NamespaceConfig | None = None,
    namespace_client_factory: Callable[[], LanceNamespace | None] | None = None,
    use_worker_props: bool = True,
) -> dict[str, str] | None:
    """Vend a fresh set of storage options for ``table_id`` from the namespace.

    The namespace client can be supplied directly, as a ``NamespaceConfig``, or
    as a zero-arg ``namespace_client_factory`` — the factory is only invoked
    here (i.e. when a re-vend actually happens), so hot-path callers can defer
    connecting until it's needed. Returns ``None`` when no namespace client /
    table is available (direct-URI or static-credential tables), so callers keep
    whatever they already have.
    """
    if table_id is None:
        return None
    ns_client = namespace_client
    if ns_client is None and namespace_client_factory is not None:
        ns_client = namespace_client_factory()
    if ns_client is None and namespace_config is not None:
        ns_client = namespace_config.connect_namespace_client(
            use_worker_props=use_worker_props
        )
    if ns_client is None:
        return None
    from lance_namespace import DescribeTableRequest

    response = ns_client.describe_table(
        DescribeTableRequest(id=table_id, vend_credentials=True)
    )
    fresh = response.storage_options or None
    log_vended_expiry(table_id, fresh)
    return fresh


def refresh_storage_options(
    storage_options: dict[str, str] | None,
    *,
    table_id: list[str] | None,
    namespace_client: LanceNamespace | None = None,
    namespace_config: NamespaceConfig | None = None,
    namespace_client_factory: Callable[[], LanceNamespace | None] | None = None,
    use_worker_props: bool = True,
    safety_ms: int | None = None,
) -> dict[str, str] | None:
    """PROACTIVE: return freshly vended options when the current ones are expiring.

    A no-op (returns the *same* object) when the options carry no expiry, are
    not yet within the safety window, or re-vending isn't possible. The guard
    runs before ``namespace_client_factory`` is called, so hot-path callers can
    pass a factory that only connects when a re-vend is actually due. Re-vend
    failures fall back to the existing options rather than aborting the read, so
    a transient namespace hiccup doesn't kill an otherwise-healthy job.

    Callers that cache anything built from the old options (sessions, handles)
    should compare the result by identity and invalidate on change.
    """
    if not storage_options_need_refresh(storage_options, safety_ms=safety_ms):
        return storage_options
    try:
        fresh = revend_storage_options(
            table_id=table_id,
            namespace_client=namespace_client,
            namespace_config=namespace_config,
            namespace_client_factory=namespace_client_factory,
            use_worker_props=use_worker_props,
        )
    except Exception:
        _LOG.warning(
            "Failed to re-vend storage options for table_id=%s; using existing "
            "(possibly expired) credentials",
            table_id,
            exc_info=True,
        )
        return storage_options
    if fresh is None:
        return storage_options
    _LOG.debug("Re-vended storage credentials for table_id=%s", table_id)
    return fresh


def force_revend_storage_options(
    *,
    table_id: list[str] | None,
    namespace_client: LanceNamespace | None = None,
    namespace_config: NamespaceConfig | None = None,
    namespace_client_factory: Callable[[], LanceNamespace | None] | None = None,
    use_worker_props: bool = True,
    label: str = "storage",
) -> dict[str, str] | None:
    """REACTIVE: unconditionally re-vend after an expired-credential error.

    Bypasses the expiry safety window — the caller has a live expired-token
    error in hand, which proves the credential is dead even when its stated
    expiry is still in the future (early revocation / clock skew). Best-effort:
    any failure (namespace-side or transport) warns and returns ``None`` so the
    caller keeps its existing options and the retry surfaces the underlying
    error. ``None`` with no warning means there was nothing to re-vend
    (direct-URI / static-credential table).

    ``label`` names the calling subsystem in log lines (e.g. ``"checkpoint"``,
    ``"commit"``).
    """
    try:
        fresh = revend_storage_options(
            table_id=table_id,
            namespace_client=namespace_client,
            namespace_config=namespace_config,
            namespace_client_factory=namespace_client_factory,
            use_worker_props=use_worker_props,
        )
    except Exception:  # noqa: BLE001 - best-effort; the retry surfaces the error
        _LOG.warning(
            "%s credential re-vend failed for table_id=%s; retrying with "
            "existing options",
            label,
            table_id,
            exc_info=True,
        )
        return None
    if fresh is not None:
        _LOG.debug("re-vended %s credentials for table_id=%s", label, table_id)
    return fresh
