"""Fuzzing-based sampler for adversarial prompt generation.

Implements a coverage-guided fuzzing approach inspired by AFL and GPTFuzzer.
Maintains a seed pool of successful templates and iteratively mutates them.

Reference: "GPTFUZZER: Red Teaming Large Language Models with Auto-Generated Jailbreak Prompts"
https://arxiv.org/abs/2309.10253
"""

import random
import typing as t
from dataclasses import dataclass

from loguru import logger

from dreadnode.core.transforms import Transform, TransformLike
from dreadnode.optimization.sampler import Sample, Sampler
from dreadnode.optimization.trial import Trial

CandidateT = t.TypeVar("CandidateT")


@dataclass
class SeedEntry(t.Generic[CandidateT]):
    """A seed in the fuzzing pool with success tracking.

    Attributes:
        candidate: The seed template.
        successes: Number of times this seed produced successful jailbreaks.
        attempts: Total number of times this seed was selected for mutation.
        children_added: Number of successful children added to pool from this seed.
        iteration_added: When this seed was added to the pool.
    """

    candidate: CandidateT
    successes: int = 0
    attempts: int = 0
    children_added: int = 0
    iteration_added: int = 0

    @property
    def success_rate(self) -> float:
        """Success rate of mutations from this seed."""
        return self.successes / self.attempts if self.attempts > 0 else 0.0


class FuzzingSampler(Sampler[CandidateT]):
    """
    Fuzzing-based sampler with mutation operators and seed pool management.

    Maintains a pool of seed templates and iteratively:
    1. Selects a seed using weighted selection (favoring successful seeds)
    2. Applies a random mutation operator to generate a new candidate
    3. Evaluates the candidate
    4. If successful (score > threshold), adds the mutated candidate to the pool

    This implements the core fuzzing loop from GPTFuzzer, using weighted random
    selection instead of full MCTS for simplicity.

    Args:
        mutators: List of mutation transforms. Each takes a seed and returns a mutated version.
        initial_seeds: Starting seed templates (human-written jailbreak prompts).
        crossover_mutator: Optional transform for crossover (takes two seeds, returns one).
        selection_strategy: How to select seeds for mutation.
                          "weighted" - weight by success rate (default)
                          "uniform" - random uniform selection
                          "ucb" - Upper Confidence Bound selection
        retention_threshold: Minimum score to retain a mutated candidate in the pool.
        max_pool_size: Maximum seeds to keep in pool (oldest removed if exceeded).
    """

    def __init__(
        self,
        mutators: list[TransformLike[CandidateT, CandidateT]],
        initial_seeds: list[CandidateT],
        *,
        crossover_mutator: TransformLike[tuple[CandidateT, CandidateT], CandidateT] | None = None,
        selection_strategy: t.Literal["weighted", "uniform", "ucb"] = "weighted",
        retention_threshold: float = 0.5,
        max_pool_size: int = 100,
        candidates_per_iteration: int = 1,
    ):
        if not initial_seeds:
            raise ValueError("At least one initial seed is required")
        if not mutators:
            raise ValueError("At least one mutator is required")

        self.mutators = [Transform.fit(m) for m in mutators]
        self.crossover_mutator = Transform.fit(crossover_mutator) if crossover_mutator else None
        self.selection_strategy = selection_strategy
        self.retention_threshold = retention_threshold
        self.max_pool_size = max_pool_size
        self.candidates_per_iteration = candidates_per_iteration

        # Store initial seeds for reset
        self._initial_seeds = list(initial_seeds)

        # Initialize seed pool with initial seeds (iteration -1 marks them as initial)
        self._pool: list[SeedEntry[CandidateT]] = [
            SeedEntry(candidate=seed, iteration_added=-1) for seed in initial_seeds
        ]

        # Track pending evaluations: sample_id -> (parent_index, mutator_index)
        self._pending: dict[int, tuple[int, int]] = {}

        # State tracking
        self._iteration = 0
        self._total_successes = 0
        self._started = False

        logger.info(
            f"FuzzingSampler initialized: "
            f"mutators={len(self.mutators)}, "
            f"initial_seeds={len(initial_seeds)}, "
            f"selection_strategy={selection_strategy}, "
            f"retention_threshold={retention_threshold}"
        )

    async def sample(
        self,
        history: list[Trial[CandidateT]],  # noqa: ARG002
    ) -> list[Sample[CandidateT]]:
        """Generate new candidates by mutating seeds from the pool."""
        self._started = True
        samples: list[Sample[CandidateT]] = []

        for _ in range(self.candidates_per_iteration):
            # Select parent seed
            parent_idx = self._select_seed()
            parent = self._pool[parent_idx]
            parent.attempts += 1

            # Decide mutation type
            use_crossover = (
                self.crossover_mutator is not None
                and len(self._pool) >= 2
                and random.random() < 0.2
            )

            if use_crossover:
                # Crossover: select second parent and combine
                assert self.crossover_mutator is not None
                other_idx = self._select_seed(exclude=parent_idx)
                other = self._pool[other_idx]
                mutated = await self.crossover_mutator((parent.candidate, other.candidate))
                mutator_idx = -1  # Special index for crossover
            else:
                # Regular mutation: select random mutator
                mutator_idx = random.randrange(len(self.mutators))
                mutator = self.mutators[mutator_idx]
                mutated = await mutator(parent.candidate)

            sample_id = id(mutated)
            self._pending[sample_id] = (parent_idx, mutator_idx)

            samples.append(
                Sample(
                    mutated,
                    metadata={
                        "parent_idx": parent_idx,
                        "mutator_idx": mutator_idx,
                        "sample_id": sample_id,
                    },
                )
            )

        self._iteration += 1
        logger.debug(
            f"FuzzingSampler iteration {self._iteration}: "
            f"generated {len(samples)} candidates, "
            f"pool size {len(self._pool)}"
        )
        return samples

    def tell(self, trials: list[Trial[CandidateT]]) -> None:
        """Process completed trials and update seed pool."""
        for trial in trials:
            if trial.status != "finished":
                continue

            # Get parent info
            trial_meta: dict[str, t.Any] | None = getattr(trial, "metadata", None)
            sample_id = trial_meta.get("sample_id") if trial_meta else None
            parent_idx = None

            if sample_id and sample_id in self._pending:
                parent_idx, _ = self._pending.pop(sample_id)
            elif trial_meta and "parent_idx" in trial_meta:
                parent_idx = trial_meta["parent_idx"]

            # Check if this is a successful jailbreak
            if trial.score >= self.retention_threshold:
                self._total_successes += 1

                # Update parent success count
                if parent_idx is not None and parent_idx < len(self._pool):
                    self._pool[parent_idx].successes += 1
                    self._pool[parent_idx].children_added += 1

                # Add successful mutation to pool
                new_entry = SeedEntry(
                    candidate=trial.candidate,
                    successes=1,  # Start with 1 since it was successful
                    attempts=0,
                    iteration_added=self._iteration,
                )
                self._pool.append(new_entry)

                logger.debug(
                    f"FuzzingSampler: added successful seed to pool "
                    f"(score={trial.score:.3f}, pool_size={len(self._pool)})"
                )

                # Prune if pool exceeds max size
                self._prune_pool()

    def _select_seed(self, exclude: int | None = None) -> int:
        """Select a seed index from the pool using the configured strategy."""
        if len(self._pool) == 1:
            return 0

        valid_indices = [i for i in range(len(self._pool)) if i != exclude]

        if self.selection_strategy == "uniform":
            return random.choice(valid_indices)

        if self.selection_strategy == "weighted":
            # Weight by success rate + baseline
            weights = []
            for i in valid_indices:
                seed = self._pool[i]
                # Add baseline weight so new seeds get selected too
                weight = seed.success_rate + 0.1
                weights.append(weight)
            total = sum(weights)
            weights = [w / total for w in weights]
            return random.choices(valid_indices, weights=weights, k=1)[0]

        if self.selection_strategy == "ucb":
            # Upper Confidence Bound selection
            import math

            total_attempts = sum(s.attempts for s in self._pool) + 1
            best_idx = valid_indices[0]
            best_score = -float("inf")

            for i in valid_indices:
                seed = self._pool[i]
                if seed.attempts == 0:
                    # Unexplored seeds get priority
                    return i
                exploitation = seed.success_rate
                exploration = math.sqrt(2 * math.log(total_attempts) / seed.attempts)
                ucb_score = exploitation + exploration
                if ucb_score > best_score:
                    best_score = ucb_score
                    best_idx = i

            return best_idx

        return random.choice(valid_indices)

    def _prune_pool(self) -> None:
        """Remove oldest/least successful seeds if pool exceeds max size."""
        if len(self._pool) <= self.max_pool_size:
            return

        # Sort by success rate (keep most successful)
        # But preserve initial seeds (they have iteration_added=-1)
        scored = []
        for i, seed in enumerate(self._pool):
            # Initial seeds get high priority
            priority = 1000 if seed.iteration_added == -1 else seed.success_rate
            scored.append((priority, i, seed))

        scored.sort(key=lambda x: x[0], reverse=True)

        # Keep top max_pool_size
        keep_indices = {x[1] for x in scored[: self.max_pool_size]}
        self._pool = [self._pool[i] for i in range(len(self._pool)) if i in keep_indices]

        logger.debug(f"FuzzingSampler: pruned pool to {len(self._pool)} seeds")

    @property
    def pool(self) -> list[SeedEntry[CandidateT]]:
        """Get the current seed pool."""
        return self._pool

    @property
    def pool_size(self) -> int:
        """Current number of seeds in the pool."""
        return len(self._pool)

    @property
    def total_successes(self) -> int:
        """Total number of successful jailbreaks found."""
        return self._total_successes

    @property
    def exhausted(self) -> bool:
        """Fuzzing sampler never exhausts - always can generate more candidates."""
        return False

    def reset(self) -> None:
        """Reset sampler state (keeps initial seeds only)."""
        self._pool = [SeedEntry(candidate=seed, iteration_added=-1) for seed in self._initial_seeds]
        self._pending = {}
        self._iteration = 0
        self._total_successes = 0
        self._started = False


def fuzzing_sampler(
    mutators: list[TransformLike[CandidateT, CandidateT]],
    initial_seeds: list[CandidateT],
    *,
    crossover_mutator: TransformLike[tuple[CandidateT, CandidateT], CandidateT] | None = None,
    selection_strategy: t.Literal["weighted", "uniform", "ucb"] = "weighted",
    retention_threshold: float = 0.5,
    max_pool_size: int = 100,
    candidates_per_iteration: int = 1,
) -> FuzzingSampler[CandidateT]:
    """
    Create a fuzzing sampler for adversarial prompt generation.

    Implements coverage-guided fuzzing where successful mutations are retained
    in a growing seed pool. Seeds that produce more successful offspring are
    selected more frequently.

    Args:
        mutators: List of mutation transforms (expand, shorten, rephrase, generate).
        initial_seeds: Starting seed templates.
        crossover_mutator: Optional transform for combining two seeds.
        selection_strategy: Seed selection method.
                          "weighted" - favor seeds with higher success rates
                          "uniform" - random selection
                          "ucb" - Upper Confidence Bound (explore-exploit balance)
        retention_threshold: Minimum score to add mutation to pool.
        max_pool_size: Maximum seeds to keep (prunes least successful).
        candidates_per_iteration: How many candidates to generate per iteration.

    Returns:
        A configured FuzzingSampler instance.

    Example:
        ```python
        sampler = fuzzing_sampler(
            mutators=[expand_mutator, shorten_mutator, rephrase_mutator],
            initial_seeds=["You are a helpful assistant...", "Ignore previous..."],
            retention_threshold=0.5,
        )
        ```
    """
    return FuzzingSampler(
        mutators=mutators,
        initial_seeds=initial_seeds,
        crossover_mutator=crossover_mutator,
        selection_strategy=selection_strategy,
        retention_threshold=retention_threshold,
        max_pool_size=max_pool_size,
        candidates_per_iteration=candidates_per_iteration,
    )
