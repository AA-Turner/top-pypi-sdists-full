from __future__ import annotations

from typing import Any

from matrx_graph.checkpoint.protocol import Checkpoint, NodeOutcome, latest_settled_keys


class MemoryCheckpointer:
    """Process-local Checkpointer for tests and single-server dev use.

    Not durable across restarts. For production, use PostgresCheckpointer from
    matrx_graph[postgres].
    """

    def __init__(self, *, keep_history: bool = True) -> None:
        #: False: only each run's LATEST checkpoint is kept (a store whose history nothing reads back — an
        #: inline child's, which never resumes — would otherwise hold a deep copy of every super-step).
        self._keep_history = keep_history
        self._checkpoints: dict[str, Checkpoint] = {}
        self._run_checkpoints: dict[str, list[str]] = {}
        # Full correlation key (ENGINE_SPEC §4.2):
        # (run_id, step, node_id, dispatch_id, item_index, attempt).
        self._outcomes: dict[tuple[str, int, str, str, int, int], NodeOutcome] = {}

    async def save_checkpoint(self, checkpoint: Checkpoint) -> None:
        # The scheduler hands over a checkpoint whose payloads are SHARED with
        # its live state (no per-save deep copy — MKT-111). A store that keeps
        # the object, rather than serializing it like Postgres does, snapshots
        # it here so history stays immutable.
        checkpoint = checkpoint.model_copy(deep=True)
        if not self._keep_history:
            for earlier in self._run_checkpoints.pop(checkpoint.run_id, []):
                self._checkpoints.pop(earlier, None)
        self._checkpoints[checkpoint.checkpoint_id] = checkpoint
        self._run_checkpoints.setdefault(checkpoint.run_id, []).append(checkpoint.checkpoint_id)

    async def save_checkpoint_with_outcomes(
        self, checkpoint: Checkpoint, outcomes: list[NodeOutcome]
    ) -> None:
        """The outcomes and the checkpoint, together (Postgres: one transaction)."""
        for outcome in outcomes:
            await self.record_outcome(outcome)
        await self.save_checkpoint(checkpoint)

    async def save_checkpoint_chain(self, items: list[tuple[Checkpoint, list[NodeOutcome]]]) -> None:
        """A chain of pure steps' checkpoints with their outcomes, in step order (Postgres: one
        transaction for the chain)."""
        for checkpoint, outcomes in items:
            await self.save_checkpoint_with_outcomes(checkpoint, outcomes)

    async def load_checkpoint(self, checkpoint_id: str) -> Checkpoint | None:
        return self._checkpoints.get(checkpoint_id)

    async def latest_checkpoint(self, run_id: str) -> Checkpoint | None:
        ids = self._run_checkpoints.get(run_id)
        if not ids:
            return None
        return self._checkpoints[ids[-1]]

    async def list_checkpoints(self, run_id: str) -> list[Checkpoint]:
        ids = self._run_checkpoints.get(run_id, [])
        return [self._checkpoints[cid] for cid in ids]

    async def record_outcome(self, outcome: NodeOutcome) -> None:
        self._outcomes[
            (
                outcome.run_id,
                outcome.step,
                outcome.node_id,
                outcome.dispatch_id,
                outcome.item_index,
                outcome.attempt,
            )
        ] = outcome

    async def step_history(self, run_id: str) -> tuple[set[str], dict[str, dict[str, str]]]:
        """Succeeded and failed steps of ``run_id`` across every leg (``step_history_from_outcomes``)."""
        from matrx_graph.checkpoint.protocol import step_history_from_outcomes

        return step_history_from_outcomes(
            [(o.node_id, o.error) for key, o in self._outcomes.items() if key[0] == run_id]
        )

    async def settled_outputs(
        self, run_id: str, node_ids: set[str], up_to_step: int | None = None
    ) -> dict[str, Any]:
        """``{step id: output}`` of each of ``node_ids``' latest successful outcome in ``run_id`` at or
        before ``up_to_step``, across every leg (``latest_settled_keys``); a step that never succeeded
        is absent."""
        keys = latest_settled_keys(
            [
                (o.node_id, (o.step, o.dispatch_id, o.item_index, o.attempt), o.error)
                for key, o in self._outcomes.items()
                if key[0] == run_id
            ],
            node_ids,
            up_to_step,
        )
        out: dict[str, Any] = {}
        for node_id, (step, dispatch_id, item_index, attempt) in keys.items():
            outcome = self._outcomes.get((run_id, step, node_id, dispatch_id, item_index, attempt))
            if outcome is not None and outcome.output is not None:
                out[node_id] = outcome.output
        return out

    async def item_outcomes(
        self, run_id: str, node_id: str, dispatch_id: str, *, step: int | None = None
    ) -> dict[int, str]:
        """``{item_index: outcome}`` of ``node_id``'s items in ``dispatch_id`` — at ``step`` only when
        given (one pass of a dispatch a cycle runs again, ``item_outcomes_from_rows``)."""
        from matrx_graph.checkpoint.protocol import item_outcomes_from_rows

        return item_outcomes_from_rows([
            (o.item_index, o.error, o.source)
            for key, o in self._outcomes.items()
            if key[0] == run_id and o.node_id == node_id and o.dispatch_id == dispatch_id
            and (step is None or o.step == step)
        ])

    async def outcome_keys(self, run_id: str, dispatch_prefix: str) -> list[tuple[int, str, str, int, int]]:
        """``(step, node_id, dispatch_id, item_index, attempt)`` of ``run_id``'s outcomes whose dispatch id
        starts with ``dispatch_prefix`` (an inline child's recorded steps, ``nodes/subgraph/inline.py``)."""
        return [
            (o.step, o.node_id, o.dispatch_id, o.item_index, o.attempt)
            for key, o in self._outcomes.items()
            if key[0] == run_id and o.dispatch_id.startswith(dispatch_prefix)
        ]

    async def get_outcome(
        self,
        run_id: str,
        step: int,
        node_id: str,
        attempt: int,
        dispatch_id: str = "",
        item_index: int = 0,
    ) -> NodeOutcome | None:
        return self._outcomes.get((run_id, step, node_id, dispatch_id, item_index, attempt))
