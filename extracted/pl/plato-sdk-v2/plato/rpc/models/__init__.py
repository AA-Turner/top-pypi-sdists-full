"""Pydantic wire models for the agent RPC protocol, one module per service.

Every operation gets its own Request/Response pair — no flat unions (the
git_ops stdio protocol's union-of-everything result model is the anti-pattern
this replaces). Evolution is additive-only within /v1: never rename or remove
fields; clients ignore unknown response fields.
"""

from plato.rpc.models.common import Ack, Limits
from plato.rpc.models.health import HandshakeResponse, HealthReport, PingResponse

__all__ = [
    "Ack",
    "HandshakeResponse",
    "HealthReport",
    "Limits",
    "PingResponse",
]
