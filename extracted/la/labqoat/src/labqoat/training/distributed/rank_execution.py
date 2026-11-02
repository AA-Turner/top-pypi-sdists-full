"""Fresh-process rank restoration and a fail-closed local fit-start barrier."""

from dataclasses import dataclass, replace
from multiprocessing.connection import Connection
from pathlib import Path

from labqoat.compute.checkpoint_group import CheckpointGroup
from labqoat.json_document import JsonDocument
from labqoat.training.distributed.checkpoint_archive import CheckpointArchive
from labqoat.training.distributed.rank_event import RankEvent
from labqoat.training.distributed.rank_factory import RankFactory
from labqoat.training.recovery.restore_snapshot import RestoreSnapshot


@dataclass(frozen=True)
class RankExecution:
    """Never reuse warm framework state and never let restoration acknowledgement start training."""

    rank: int
    factory: RankFactory
    group: CheckpointGroup
    snapshot: RestoreSnapshot
    rendezvous: Path

    def run(self, channel: Connection) -> None:
        """Report actual restored state, await the root's grant barrier and return a terminal rank outcome."""
        try:
            adapter = self.factory.create(self.rank, len(self.group.ranks), self.group.backend, self.rendezvous)
            if (adapter.adapter_id, adapter.adapter_version) != (self.factory.adapter_id, self.factory.adapter_version):
                raise ValueError("Rank factory changed the accepted adapter identity")
            path = self.snapshot.path.parent / f"rank-{self.rank}" / "checkpoint"
            CheckpointArchive.restore_rank(self.snapshot.path, self.group, self.rank, path)
            state = adapter.restore(replace(self.snapshot, path=path))
            state.evidence(self.snapshot.envelope)
            channel.send(RankEvent(self.rank, "restored", state=state))
            if channel.recv() != "fit":
                raise ValueError("Distributed fit start was not authorized")
            output = JsonDocument.expect_dict(adapter.fit())
            channel.send(RankEvent(self.rank, "completed", output=output))
        except Exception as error:
            channel.send(RankEvent(self.rank, "failed", reason=type(error).__name__))
            raise
        finally:
            channel.close()
