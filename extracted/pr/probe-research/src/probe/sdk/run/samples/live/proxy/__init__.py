"""proxy: Probe's opt-in rollout proxy (rl-next W35): one local model URL per rollout, its calls forwarded untouched,
its progress and (while watched) turns recorded through its producer; `probe samples proxy` runs it as a sidecar.
DESIGN.md beside this file."""

from .observer import PROXY_ERROR_REASON
from .proxy import LOCALHOST, NOT_ROUTED, RolloutProxy
from .server import CANCELED_CODE
from .sidecar import DEFAULT_PRODUCER, ProxySidecar

__all__ = ["CANCELED_CODE", "DEFAULT_PRODUCER", "LOCALHOST", "NOT_ROUTED", "PROXY_ERROR_REASON", "ProxySidecar",
           "RolloutProxy"]
