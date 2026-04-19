"""CLI audit-writer construction helper (#925).

Centralises the chain-safe :class:`AuditWriter` construction pattern that
the REPL already uses (``cli/repl.py``), so every standalone CLI handler
that wants to record a governed action does so through a writer that:

1. Is keyed with the identity PEM, so the HMAC chain resumes from the
   prior on-disk segment via ``AuditWriter._load_last_hmac``.
2. Returns ``None`` cleanly when audit is disabled or the configured
   identity has no private key (cannot construct an HMAC chain).

Callers wire the returned writer into the underlying service call. When
``None`` is returned, services treat it as "audit disabled" and emit
nothing (per the lineage-emitter contract).

This helper is the **local-fallback** path. For the **server-reachable**
path (the routing-helper happy case), the server's
``app.state.audit_writer`` is the sole writer; the CLI never constructs
its own writer in that case.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ..services.audit import create_audit_writer

if TYPE_CHECKING:
    from ..config import AppConfig
    from ..services.audit import AuditWriter

logger = logging.getLogger(__name__)


def get_cli_audit_writer(config: AppConfig) -> AuditWriter | None:
    """Construct a chain-safe :class:`AuditWriter` for CLI local-fallback use.

    Returns ``None`` when:

    * ``audit.enabled`` is false on the merged config; or
    * the configured identity has no ``private_key`` (no PEM available
      to derive the HMAC key) — emitting unchained entries would corrupt
      tamper-evidence, so we decline.

    The returned writer must be passed into the lineage emitters that
    write the actual entries. Callers must not write entries directly
    against the writer constructed here without going through the
    lineage layer; the lineage layer performs the
    ``audit_writer is None`` short-circuit per emitter.
    """
    audit_cfg = getattr(config, "audit", None)
    if audit_cfg is None or not getattr(audit_cfg, "enabled", False):
        return None

    identity = getattr(config, "identity", None)
    private_key = getattr(identity, "private_key", "") if identity else ""
    if not private_key:
        logger.warning(
            "CLI audit writer requested but no identity private key is available; "
            "declining to construct an unchained writer."
        )
        return None

    return create_audit_writer(config, private_key_pem=private_key)
