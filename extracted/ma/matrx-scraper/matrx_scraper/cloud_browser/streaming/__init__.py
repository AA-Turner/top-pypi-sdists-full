"""Cloud Browser streaming and takeover plane (WS-4).

Narrowed by DECISIONS D-8: the stream exists ONLY while a person is actively
driving. Nothing streams by default; there is exactly ONE controller, ONE stream,
minted on takeover and revoked on return; the encoder is asleep otherwise.

Public surface — the pieces a host (the Browser Manager, WS-5) wires up:

    StreamingConfig      host-injected VALUES (signing key, origins, TURN)
    FixtureAccessResolver / AccessResolver   the iam.has_access_for seam
    StreamPlane          the shared component container
    MintService          mint authority + control-lease ops
    StreamGateway        claim/renew + the session lifecycle
    RevocationCoordinator  the one place the revocation ORDER lives
    build_standalone_app  the WS-4 standalone FastAPI harness (S4 §10)

Authority: contracts/S4-stream-tickets.md, PLAN.md §WebRTC streaming.
"""

from __future__ import annotations

from .access import AccessAnswer, AccessResolver, FixtureAccessResolver
from .config import (
    CONTROL_MEDIA_POLICY,
    StreamingConfig,
    StreamTicketNotConfigured,
)
from .control_plane import MintService
from .errors import StreamError
from .gateway import RevocationCoordinator, SessionRegistry, StreamGateway
from .plane import StreamPlane
from .selkies_worker import SelkiesWorkerConfig
from .tickets import TicketClaims, TicketSigner
from .turn_credentials import TurnCredential, mint_turn_credential

__all__ = [
    "AccessAnswer",
    "AccessResolver",
    "FixtureAccessResolver",
    "StreamingConfig",
    "StreamTicketNotConfigured",
    "CONTROL_MEDIA_POLICY",
    "MintService",
    "StreamError",
    "StreamGateway",
    "SessionRegistry",
    "RevocationCoordinator",
    "StreamPlane",
    "SelkiesWorkerConfig",
    "TicketClaims",
    "TicketSigner",
    "TurnCredential",
    "mint_turn_credential",
]
