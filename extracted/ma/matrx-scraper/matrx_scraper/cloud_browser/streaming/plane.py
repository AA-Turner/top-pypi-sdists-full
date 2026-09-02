"""The streaming plane — the shared object holding every component the mint
service, gateway, and revocation coordinator operate on.

Keeping them in one injected container (rather than module globals) is what lets
the whole plane be constructed fresh per test and run standalone with the stub
mint endpoint and any headed Chromium (S4 §10).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .access import AccessResolver
from .config import StreamingConfig
from .control_lease import RunRegistry
from .ticket_store import InMemoryTicketStore, TicketStore
from .tickets import TicketSigner
from .worker_input import WorkerInputRegistry


@dataclass
class StreamPlane:
    config: StreamingConfig
    access: AccessResolver
    signer: TicketSigner
    runs: RunRegistry = field(default_factory=RunRegistry)
    tickets: TicketStore = field(default_factory=InMemoryTicketStore)
    workers: WorkerInputRegistry = field(default_factory=WorkerInputRegistry)

    @classmethod
    def build(cls, *, config: StreamingConfig, access: AccessResolver) -> "StreamPlane":
        signer = TicketSigner(private_key_pem=config.require_signing_key())
        return cls(config=config, access=access, signer=signer)

    def runs_by_handoff(self, handoff_id: str):
        """Resolve the live run currently carrying this handoff. Raises the same
        typed errors the registry raises (RUN_NOT_LIVE / HANDOFF_NOT_CLAIMABLE)."""
        from .errors import HANDOFF_NOT_CLAIMABLE, StreamError

        for run in self.runs.iter_live():
            if run.active_handoff_id == handoff_id:
                return run
        raise StreamError(HANDOFF_NOT_CLAIMABLE, "no live run carries this handoff")
