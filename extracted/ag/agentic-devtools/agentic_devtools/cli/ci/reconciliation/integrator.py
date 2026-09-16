"""Single-writer integration for isolated specialist outputs."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from datetime import datetime

from agentic_devtools.cli.ci.reconciliation.models import PermitStatus, QueueState


@dataclass(frozen=True)
class SpecialistOutput:
    """An isolated worker result bound to its permit and starting PR head."""

    worker_id: str
    permit_id: str
    base_head_sha: str
    changed_files: tuple[str, ...] = ()
    changed_tests: tuple[str, ...] = ()
    payload: object = None

    @property
    def footprint(self) -> frozenset[str]:
        return frozenset((*self.changed_files, *self.changed_tests))


@dataclass(frozen=True)
class IntegrationResult:
    """Outcome of one serialized integration publication."""

    accepted: bool
    reason: str
    batches: tuple[tuple[SpecialistOutput, ...], ...] = ()
    published_head_sha: str | None = None


class StaleWriterError(ValueError):
    """Raised when isolated output no longer has authority to write."""


class SinglePRIntegrator:
    """Collect outputs, serialize overlaps, and publish through one writer."""

    def __init__(self, clock: Callable[[], datetime]) -> None:
        if not callable(clock):
            raise ValueError("clock is required")
        self._clock = clock

    def integrate(
        self,
        state: QueueState,
        outputs: Iterable[SpecialistOutput],
        *,
        current_head_sha: str,
        apply_batch: Callable[[tuple[SpecialistOutput, ...]], None],
        publish: Callable[[], str],
    ) -> IntegrationResult:
        """Reject stale output, then apply non-overlapping batches in one publication."""
        collected = tuple(outputs)
        for output in collected:
            permit = state.active_permits.get(output.permit_id)
            if permit is None or permit.status != PermitStatus.ACCEPTED:
                raise StaleWriterError("worker permit is no longer active")
            if permit.deadline_at <= self._clock() or output.base_head_sha != current_head_sha:
                raise StaleWriterError("worker output is stale")
        batches: list[tuple[SpecialistOutput, ...]] = []
        for output in collected:
            for index, batch in enumerate(batches):
                if all(output.footprint.isdisjoint(item.footprint) for item in batch):
                    batches[index] = (*batch, output)
                    break
            else:
                batches.append((output,))
        for batch in batches:
            apply_batch(batch)
        published = publish()
        return IntegrationResult(True, "published", tuple(batches), published)
