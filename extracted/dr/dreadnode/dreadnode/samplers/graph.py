"""Graph-based samplers for LLM attack optimization."""

import typing as t
from uuid import UUID  # noqa: TC003

from loguru import logger

from dreadnode.core.transforms import Transform, TransformLike
from dreadnode.core.util import concurrent_gen
from dreadnode.optimization.collectors import lineage, local_neighborhood
from dreadnode.optimization.sampler import Sample, Sampler
from dreadnode.optimization.sampling import interleave_by_parent, top_k
from dreadnode.optimization.trial import Trial, TrialCollector, TrialSampler

CandidateT = t.TypeVar("CandidateT")


class GraphSampler(Sampler[CandidateT]):
    """
    Graph-based sampler using transforms to generate new candidates.

    Maintains a directed acyclic graph where nodes are trials and edges
    represent parent-child relationships. Uses an async transform to
    generate new candidates based on trial context.

    For each sampling step:
    1. Gather context trials for each leaf using context_collector
    2. Apply transform to generate branching_factor children per leaf
    3. Return all new candidates as samples

    After evaluation (via tell()), prunes to keep best candidates as leaves.
    """

    def __init__(
        self,
        transform: TransformLike[list[Trial[CandidateT]], CandidateT],
        initial_candidate: CandidateT,
        *,
        branching_factor: int = 3,
        context_collector: TrialCollector[CandidateT] = lineage,  # ty: ignore[invalid-parameter-default]
        pruning_sampler: TrialSampler[CandidateT] = top_k,  # ty: ignore[invalid-parameter-default]
    ):
        self.transform = Transform.fit(transform)
        self.initial_candidate = initial_candidate
        self.branching_factor = branching_factor
        self.context_collector = context_collector
        self.pruning_sampler = pruning_sampler

        # Internal state
        self._trials: list[Trial[CandidateT]] = []
        self._leaves: list[Trial[CandidateT]] = []
        self._trial_map: dict[UUID, Trial[CandidateT]] = {}
        self._started = False
        self._exhausted = False

        logger.info(
            f"GraphSampler initialized: "
            f"branching_factor={branching_factor}, "
            f"context_collector={context_collector}, "
            f"pruning_sampler={pruning_sampler}"
        )

    async def sample(self, history: list[Trial[CandidateT]]) -> list[Sample[CandidateT]]:
        """Generate new candidates from the current leaves."""
        # First call - return initial candidate
        if not self._started:
            self._started = True
            return [Sample(self.initial_candidate)]

        # If exhausted (no leaves after pruning), stop
        if self._exhausted or not self._leaves:
            return []

        # Update trial map with any new history
        for trial in history:
            if trial.id not in self._trial_map:
                self._trial_map[trial.id] = trial

        # Generate children from each leaf
        samples: list[Sample[CandidateT]] = []
        for leaf in self._leaves:
            # Collect context for this leaf
            context = [leaf, *self.context_collector(leaf, self._trials)]

            # Generate branching_factor children
            coroutines = [self.transform(context) for _ in range(self.branching_factor)]
            async with concurrent_gen(coroutines) as gen:
                samples.extend(
                    [
                        Sample(candidate=candidate, metadata={"parent_id": leaf.id})
                        async for candidate in gen
                    ]
                )

        logger.debug(
            f"GraphSampler generated {len(samples)} samples from {len(self._leaves)} leaves"
        )
        return samples

    def tell(self, trials: list[Trial[CandidateT]]) -> None:
        """Process completed trials and update leaves."""
        if not self._started:
            return

        # Handle initial trial
        if not self._trials and len(trials) == 1:
            initial = trials[0]
            self._trials.append(initial)
            self._trial_map[initial.id] = initial
            if initial.status == "finished":
                self._leaves = [initial]
            else:
                # Initial trial was pruned/failed - still use it as a leaf so the
                # search can generate alternative candidates from its context.
                # Score remains -inf so it will be ranked lowest during pruning.
                self._leaves = [initial]
                logger.warning(
                    f"GraphSampler: initial trial {initial.status}, "
                    f"continuing search with fallback leaf"
                )
            return

        # Collect finished trials
        finished = [t for t in trials if t.status == "finished"]

        # Update trial map
        for trial in finished:
            self._trial_map[trial.id] = trial

        # Add finished to our trial list
        self._trials.extend(finished)

        if not finished:
            # All trials failed - try with current leaves again or stop
            if not self._leaves:
                self._exhausted = True
            return

        # Interleave by parent for fair pruning
        interleaved = interleave_by_parent(finished)

        # Prune to get new leaves
        self._leaves = self.pruning_sampler(interleaved)

        if not self._leaves:
            self._exhausted = True

        logger.debug(
            f"GraphSampler updated: {len(self._trials)} total trials, {len(self._leaves)} leaves"
        )

    @property
    def exhausted(self) -> bool:
        return self._exhausted

    def reset(self) -> None:
        """Reset to initial state."""
        self._trials = []
        self._leaves = []
        self._trial_map = {}
        self._started = False
        self._exhausted = False


def beam_search_sampler(
    transform: TransformLike[list[Trial[CandidateT]], CandidateT],
    initial_candidate: CandidateT,
    *,
    beam_width: int = 3,
    branching_factor: int = 3,
    parent_depth: int = 10,
) -> GraphSampler[CandidateT]:
    """
    Create a graph sampler configured for classic beam search.

    Maintains parallel reasoning paths by keeping a "beam" of the top k
    best trials from the previous step.

    Args:
        transform: Function that takes trial context and generates new candidates.
        initial_candidate: The starting point for the search.
        beam_width: Number of top candidates to keep at each step (the 'k').
        branching_factor: How many new candidates to generate from each beam trial.
        parent_depth: Number of ancestors to include in context for refinement.

    Returns:
        A configured GraphSampler instance.
    """
    return GraphSampler(
        transform=transform,
        initial_candidate=initial_candidate,
        branching_factor=branching_factor,
        context_collector=lineage.configure(depth=parent_depth),
        pruning_sampler=top_k.configure(k=beam_width),
    )


def graph_neighborhood_sampler(
    transform: TransformLike[list[Trial[CandidateT]], CandidateT],
    initial_candidate: CandidateT,
    *,
    neighborhood_depth: int = 2,
    frontier_size: int = 5,
    branching_factor: int = 3,
) -> GraphSampler[CandidateT]:
    """
    Create a graph sampler with local neighborhood context.

    The trial context includes trials in the local neighborhood up to
    2h-1 distance away, where h is the neighborhood depth.

    See: "Graph of Attacks" - https://arxiv.org/pdf/2504.19019v1

    Args:
        transform: Function that takes neighborhood context and generates candidates.
        initial_candidate: The starting point for the search.
        neighborhood_depth: Depth 'h' for calculating neighborhood size.
        frontier_size: Number of top candidates to form the next frontier.
        branching_factor: How many candidates to generate from each leaf.

    Returns:
        A configured GraphSampler instance.
    """
    return GraphSampler(
        transform=transform,
        initial_candidate=initial_candidate,
        branching_factor=branching_factor,
        context_collector=local_neighborhood.configure(depth=neighborhood_depth),
        pruning_sampler=top_k.configure(k=frontier_size),
    )


def iterative_sampler(
    transform: TransformLike[list[Trial[CandidateT]], CandidateT],
    initial_candidate: CandidateT,
    *,
    branching_factor: int = 1,
    parent_depth: int = 10,
) -> GraphSampler[CandidateT]:
    """
    Create a graph sampler for simple iterative refinement.

    A single-path sampler that keeps only the best candidate at each step
    (k=1 pruning). Useful for greedy hill-climbing style optimization.

    Args:
        transform: Function that takes trial context and generates new candidates.
        initial_candidate: The starting point for the search.
        branching_factor: How many candidates to generate each iteration.
        parent_depth: Number of ancestors to include in context for refinement.

    Returns:
        A configured GraphSampler instance with k=1 pruning.
    """
    return GraphSampler(
        transform=transform,
        initial_candidate=initial_candidate,
        branching_factor=branching_factor,
        context_collector=lineage.configure(depth=parent_depth),
        pruning_sampler=top_k.configure(k=1),
    )
