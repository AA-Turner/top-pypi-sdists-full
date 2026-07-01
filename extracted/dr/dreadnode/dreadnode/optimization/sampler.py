"""
Sampler interface for optimization studies.

Samplers propose candidates and learn from results.
Study controls the execution loop - samplers are passive.
"""

import typing as t
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from uuid import UUID

import typing_extensions as te

if t.TYPE_CHECKING:
    from dreadnode.optimization.trial import Trial

CandidateT = te.TypeVar("CandidateT", default=t.Any)


@dataclass
class Sample(t.Generic[CandidateT]):
    """A candidate proposed by a sampler.

    Attributes:
        candidate: The candidate value to evaluate.
        metadata: Optional metadata (e.g., parent_id for graph-based search).
    """

    candidate: CandidateT
    metadata: dict[str, t.Any] = field(default_factory=dict)

    @property
    def parent_id(self) -> UUID | None:
        """Convenience accessor for parent_id in metadata."""
        return self.metadata.get("parent_id")


class Sampler(ABC, t.Generic[CandidateT]):
    """
    Base class for optimization samplers.

    Samplers propose candidates and learn from evaluation results.
    Study controls the execution loop - samplers are passive.

    The sample/tell interface:
        - sample(history) -> list[Sample]: Propose candidates to evaluate
        - tell(trials): Receive evaluation results

    Example:
        class GridSampler(Sampler[dict]):
            def __init__(self, grid: dict[str, list]):
                self.combinations = list(itertools.product(*grid.values()))
                self.keys = list(grid.keys())
                self.index = 0

            def sample(self, history: list[Trial]) -> list[Sample]:
                if self.exhausted:
                    return []
                candidate = dict(zip(self.keys, self.combinations[self.index]))
                self.index += 1
                return [Sample(candidate)]

            @property
            def exhausted(self) -> bool:
                return self.index >= len(self.combinations)
    """

    @abstractmethod
    def sample(
        self, history: list["Trial[CandidateT]"]
    ) -> list[Sample[CandidateT]] | t.Awaitable[list[Sample[CandidateT]]]:
        """
        Propose candidates to evaluate.

        Can be sync or async. If async (returns awaitable), Study will await it.
        This allows samplers that use async operations (like LLM calls) to
        generate candidates.

        Args:
            history: All trials evaluated so far (completed, failed, or pruned).

        Returns:
            List of samples to evaluate together as a batch.
            Return empty list to signal the sampler is exhausted.
            Can also return an awaitable that resolves to the list.
        """
        ...

    def tell(self, trials: list["Trial[CandidateT]"]) -> None:
        """
        Receive evaluation results.

        Called after each batch from sample() completes evaluation.
        Override to update internal state based on results.

        Args:
            trials: Completed trials from the last sample() batch.
                   Each trial has status, scores, and other result data.
        """

    @property
    def exhausted(self) -> bool:
        """
        Check if sampler has no more candidates to propose.

        Override for finite samplers (grid search, explicit candidate list).
        Default: never exhausted (infinite sampling).

        Returns:
            True if sampler cannot propose more candidates.
        """
        return False

    def reset(self) -> None:
        """
        Reset sampler state for reuse.

        Override if sampler maintains state that should be cleared
        between study runs.
        """
