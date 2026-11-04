"""Capability flag gating from ``PLATO_AGENT_RPC_CAPS``.

RPC is **ON by default**: an unset env var enables every group. The var is the
kill switch — ``none`` disables everything (full SSH fallback), and a comma
list (``health,env,exec,files,pool,git,job``) enables just a subset for a
targeted rollback. Effective enablement of a capability = the flag group is on
AND the daemon's handshake advertises it, so baked-SDK skew degrades silently
to SSH regardless of the default.

The intended production off-path: a Chronos-side feature flag (PostHog)
injects ``PLATO_AGENT_RPC_CAPS=none`` into the world runner's environment.
That wiring lives in the platform repo, not here.
"""

from __future__ import annotations

import os

from plato.rpc.protocol import FLAG_GROUPS, FLAGS_ENV_VAR


def _enabled_groups(raw: str | None) -> set[str]:
    if raw is None:
        return set(FLAG_GROUPS)  # unset -> everything on (default)
    tokens = {t.strip().lower() for t in raw.split(",") if t.strip()}
    if "all" in tokens:
        return set(FLAG_GROUPS)
    if "none" in tokens:
        return set()
    return {t for t in tokens if t in FLAG_GROUPS}


def flag_enables(capability: str, *, env: str | None = None) -> bool:
    """Whether the flag config permits attempting ``capability`` over RPC.

    Independent of what any daemon advertises — this is only the operator's
    kill-switch half of the AND (``None`` means "var unset": enabled).
    """
    raw = env if env is not None else os.environ.get(FLAGS_ENV_VAR)
    groups = _enabled_groups(raw)
    for group in groups:
        for prefix in FLAG_GROUPS[group]:
            if capability == prefix or capability.startswith(prefix):
                return True
    return False
