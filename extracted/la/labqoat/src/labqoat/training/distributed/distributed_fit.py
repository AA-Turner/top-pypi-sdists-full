"""Explicit fixed-topology recovery with one root-owned cumulative fit allowance."""

import time
from contextlib import ExitStack
from datetime import UTC, datetime

from labqoat.compute.checkpoint_group import CheckpointGroup
from labqoat.json_document import JsonDocument
from labqoat.run_context import RunContext
from labqoat.training.distributed.group_restoration import GroupRestoration
from labqoat.training.distributed.rank_execution import RankExecution
from labqoat.training.distributed.rank_factory import RankFactory
from labqoat.training.distributed.rank_failure_error import RankFailureError
from labqoat.training.distributed.rank_processes import RankProcesses
from labqoat.training.recovery.restore_state import RestoreState


class DistributedFit:
    """Restore every required rank before granting any of them permission to update training state."""

    def __init__(self, context: RunContext, group: CheckpointGroup, factory: RankFactory) -> None:
        """Bind one invocation, complete coordinated inventory and retained workload adapter factory."""
        self.context, self.group, self.factory = context, group, factory
        self._used = False

    def run(self) -> tuple[JsonDocument, ...]:
        """Resume exactly once, reap all ranks before disarming and charge group wall time only once."""
        recovery = self.context.recovery
        if recovery is None or recovery.envelope.document["mode"] != "resume" or self._used:
            raise ValueError("Distributed fit requires an unused resume plan")
        self._used = True
        snapshot = recovery.stage(self.factory.adapter_id, self.factory.adapter_version)
        protocol = GroupRestoration(recovery.api, snapshot, self.group)
        protocol.validate()
        peers = RankProcesses()
        try:
            with ExitStack() as lifetime:
                lifetime.callback(peers.close)
                rendezvous = snapshot.path.parent / "rendezvous"
                peers.start(RankExecution(0, self.factory, self.group, snapshot, rendezvous))
                state = self._restore(peers, protocol)
                recovery.acknowledge(state)
                return self._fit(peers)
        except RankFailureError as error:
            protocol.fail(error.rank, "collective", str(error))
            raise

    def _restore(self, peers: RankProcesses, protocol: GroupRestoration) -> RestoreState:
        """Preserve the first-claim deadline while persisting each rank's actual restored evidence."""
        remaining = (protocol.snapshot.envelope.deadline_at - datetime.now(UTC)).total_seconds()
        deadline = time.monotonic() + max(0.0, remaining)
        pending = set(range(len(self.group.ranks)))
        states: list[RestoreState] = []
        while pending:
            event = peers.receive(pending, deadline)
            if event.phase != "restored" or event.state is None:
                raise RankFailureError(event.rank, "Rank trained before restoration was authorized")
            protocol.acknowledge(event.rank, event.state)
            states.append(event.state)
            pending.remove(event.rank)
        return states[0]

    def _fit(self, peers: RankProcesses) -> tuple[JsonDocument, ...]:
        """Enter one supervised interval, then terminate every rank before releasing its reservation."""
        with self.context.fit_budget.maintained():
            try:
                peers.permit()
                return self._results(peers)
            finally:
                peers.close()

    def _results(self, peers: RankProcesses) -> tuple[JsonDocument, ...]:
        """Retain rank ordering while observing results and failures through event-driven channels."""
        pending = set(range(len(self.group.ranks)))
        results: dict[int, JsonDocument] = {}
        while pending:
            event = peers.receive(pending, None)
            if event.phase != "completed" or event.output is None:
                raise RankFailureError(event.rank, "Unexpected rank event during fit")
            results[event.rank] = event.output
            pending.remove(event.rank)
        return tuple(results[rank] for rank in range(len(self.group.ranks)))
