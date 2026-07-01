"""MAP-Elites sampler for quality-diversity optimization.

Implements the MAP-Elites algorithm for diverse adversarial prompt generation.
Used by Rainbow Teaming to maintain an archive of diverse high-quality attacks.

References:
- Rainbow Teaming: "Rainbow Teaming: Open-Ended Generation of Diverse Adversarial Prompts"
  https://arxiv.org/abs/2402.16822
- MAP-Elites: "Illuminating search spaces by mapping elites" (Mouret & Clune, 2015)
  https://arxiv.org/abs/1504.04909
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
class ArchiveCell(t.Generic[CandidateT]):
    """A cell in the MAP-Elites archive storing an elite candidate.

    Attributes:
        candidate: The elite candidate for this cell.
        fitness: The fitness score of this candidate.
        trial_id: The trial ID that produced this elite.
        iteration: When this elite was discovered.
    """

    candidate: CandidateT
    fitness: float
    trial_id: t.Any = None
    iteration: int = 0


@dataclass
class MutationTarget:
    """Target cell coordinates for mutation.

    Attributes:
        feature_indices: Tuple of indices for each feature dimension.
        feature_values: The actual feature values (for passing to mutator).
    """

    feature_indices: tuple[int, ...]
    feature_values: tuple[str, ...]


class MAPElitesSampler(Sampler[CandidateT]):
    """
    MAP-Elites sampler for quality-diversity optimization.

    Maintains a multidimensional archive where each cell stores the best
    candidate for that combination of feature values. Generates new candidates
    by mutating archive elites toward specific feature targets.

    The archive is organized by feature dimensions (e.g., risk_category * attack_style).
    Each cell can hold one elite. New candidates replace existing elites only if
    they have higher fitness.

    For Rainbow Teaming:
    - Feature 1: Risk category (10 categories)
    - Feature 2: Attack style (4 styles)
    - Total cells: 10 * 4 = 40

    Args:
        mutator: Transform that takes (parent_prompt, target_features) and generates
                a mutated candidate targeting those features.
        initial_candidates: Seed candidates to populate the archive initially.
        feature_dimensions: List of feature value lists. Each list defines the
                          possible values for one dimension.
        selection_strategy: How to select parents from archive.
                          "uniform" - random uniform selection
                          "sparse" - prioritize under-explored cells
    """

    def __init__(
        self,
        mutator: TransformLike[tuple[CandidateT, MutationTarget], CandidateT],
        initial_candidates: list[CandidateT],
        feature_dimensions: list[list[str]],
        *,
        selection_strategy: t.Literal["uniform", "sparse"] = "uniform",
        candidates_per_iteration: int = 1,
    ):
        self.mutator = Transform.fit(mutator)
        self.initial_candidates = initial_candidates
        self.feature_dimensions = feature_dimensions
        self.selection_strategy = selection_strategy
        self.candidates_per_iteration = candidates_per_iteration

        # Compute grid dimensions
        self.grid_shape = tuple(len(dim) for dim in feature_dimensions)
        self.total_cells = 1
        for dim_size in self.grid_shape:
            self.total_cells *= dim_size

        # Archive: maps feature index tuple to ArchiveCell
        self._archive: dict[tuple[int, ...], ArchiveCell[CandidateT]] = {}

        # Track pending evaluations: candidate -> target cell
        self._pending_targets: dict[int, MutationTarget] = {}

        # State tracking
        self._iteration = 0
        self._started = False
        self._initial_phase = True
        self._initial_index = 0

        logger.info(
            f"MAPElitesSampler initialized: "
            f"grid_shape={self.grid_shape}, "
            f"total_cells={self.total_cells}, "
            f"initial_candidates={len(initial_candidates)}, "
            f"selection_strategy={selection_strategy}"
        )

    async def sample(
        self,
        history: list[Trial[CandidateT]],  # noqa: ARG002
    ) -> list[Sample[CandidateT]]:
        """Generate new candidates by mutating archive elites."""
        self._started = True

        # Initial phase: return seed candidates one by one
        if self._initial_phase:
            if self._initial_index < len(self.initial_candidates):
                candidate = self.initial_candidates[self._initial_index]
                # Assign random target cell for initial candidates
                target = self._random_target()
                sample_id = id(candidate)
                self._pending_targets[sample_id] = target
                self._initial_index += 1
                return [Sample(candidate, metadata={"target": target, "sample_id": sample_id})]
            self._initial_phase = False

        # If archive is empty after initial phase, we're stuck
        if not self._archive:
            logger.warning("MAPElitesSampler: archive is empty, cannot generate candidates")
            return []

        # Generate candidates by mutating archive elites
        samples: list[Sample[CandidateT]] = []
        for _ in range(self.candidates_per_iteration):
            # Select parent from archive
            parent_cell = self._select_parent()
            if parent_cell is None:
                continue

            parent = parent_cell.candidate

            # Select target cell for mutation
            target = self._select_target()

            # Generate mutated candidate
            mutated = await self.mutator((parent, target))
            sample_id = id(mutated)
            self._pending_targets[sample_id] = target
            samples.append(
                Sample(
                    mutated,
                    metadata={
                        "target": target,
                        "parent_cell": parent_cell,
                        "sample_id": sample_id,
                    },
                )
            )

        self._iteration += 1
        logger.debug(
            f"MAPElitesSampler iteration {self._iteration}: "
            f"generated {len(samples)} candidates, "
            f"archive size {len(self._archive)}/{self.total_cells}"
        )
        return samples

    def tell(self, trials: list[Trial[CandidateT]]) -> None:
        """Process completed trials and update archive."""
        for trial in trials:
            if trial.status != "finished":
                continue

            # Get target cell for this trial
            trial_meta: dict[str, t.Any] | None = getattr(trial, "metadata", None)
            sample_id = trial_meta.get("sample_id") if trial_meta else None
            target: MutationTarget | None = None

            if sample_id and sample_id in self._pending_targets:
                target = self._pending_targets.pop(sample_id)
            elif trial_meta and "target" in trial_meta:
                target = trial_meta["target"]

            if target is None:
                # Fallback: assign to random cell
                target = self._random_target()

            cell_key = target.feature_indices
            fitness = trial.score

            # Update archive if this is better than existing elite
            if cell_key not in self._archive:
                self._archive[cell_key] = ArchiveCell(
                    candidate=trial.candidate,
                    fitness=fitness,
                    trial_id=trial.id,
                    iteration=self._iteration,
                )
                logger.debug(
                    f"MAPElitesSampler: new elite at {cell_key} with fitness {fitness:.3f}"
                )
            elif fitness > self._archive[cell_key].fitness:
                old_fitness = self._archive[cell_key].fitness
                self._archive[cell_key] = ArchiveCell(
                    candidate=trial.candidate,
                    fitness=fitness,
                    trial_id=trial.id,
                    iteration=self._iteration,
                )
                logger.debug(
                    f"MAPElitesSampler: replaced elite at {cell_key} "
                    f"({old_fitness:.3f} -> {fitness:.3f})"
                )

    def _select_parent(self) -> ArchiveCell[CandidateT] | None:
        """Select a parent from the archive for mutation."""
        if not self._archive:
            return None

        if self.selection_strategy == "uniform":
            # Uniform random selection
            return random.choice(list(self._archive.values()))
        if self.selection_strategy == "sparse":
            # Prioritize cells with lower fitness (room for improvement)
            cells = list(self._archive.values())
            # Inverse fitness weighting
            weights = [1.0 / (cell.fitness + 0.1) for cell in cells]
            total = sum(weights)
            weights = [w / total for w in weights]
            return random.choices(cells, weights=weights, k=1)[0]
        return random.choice(list(self._archive.values()))

    def _select_target(self) -> MutationTarget:
        """Select target cell coordinates for mutation."""
        if self.selection_strategy == "sparse":
            # Prioritize empty cells
            empty_cells = [
                self._indices_to_target(indices)
                for indices in self._all_cell_indices()
                if indices not in self._archive
            ]
            if empty_cells:
                return random.choice(empty_cells)

        # Random target
        return self._random_target()

    def _random_target(self) -> MutationTarget:
        """Generate random target cell coordinates."""
        indices = tuple(random.randrange(len(dim)) for dim in self.feature_dimensions)
        return self._indices_to_target(indices)

    def _indices_to_target(self, indices: tuple[int, ...]) -> MutationTarget:
        """Convert cell indices to MutationTarget with feature values."""
        values = tuple(self.feature_dimensions[i][idx] for i, idx in enumerate(indices))
        return MutationTarget(feature_indices=indices, feature_values=values)

    def _all_cell_indices(self) -> t.Iterator[tuple[int, ...]]:
        """Iterate over all possible cell indices."""
        import itertools

        ranges = [range(len(dim)) for dim in self.feature_dimensions]
        yield from itertools.product(*ranges)

    @property
    def archive(self) -> dict[tuple[int, ...], ArchiveCell[CandidateT]]:
        """Get the current archive."""
        return self._archive

    @property
    def coverage(self) -> float:
        """Fraction of archive cells that are filled."""
        return len(self._archive) / self.total_cells if self.total_cells > 0 else 0.0

    @property
    def exhausted(self) -> bool:
        """MAP-Elites never exhausts - always can generate more candidates."""
        return False

    def reset(self) -> None:
        """Reset sampler state."""
        self._archive = {}
        self._pending_targets = {}
        self._iteration = 0
        self._started = False
        self._initial_phase = True
        self._initial_index = 0


def mapelites_sampler(
    mutator: TransformLike[tuple[CandidateT, MutationTarget], CandidateT],
    initial_candidates: list[CandidateT],
    feature_dimensions: list[list[str]],
    *,
    selection_strategy: t.Literal["uniform", "sparse"] = "uniform",
    candidates_per_iteration: int = 1,
) -> MAPElitesSampler[CandidateT]:
    """
    Create a MAP-Elites sampler for quality-diversity optimization.

    MAP-Elites maintains a grid of "elites" - the best candidate found for each
    combination of behavioral features. This enables diverse exploration while
    still optimizing for quality.

    Args:
        mutator: Transform that takes (parent_candidate, target) and generates
                a mutated candidate targeting the specified feature values.
        initial_candidates: Seed candidates to start the archive.
        feature_dimensions: List of feature value lists defining the grid.
                          Example: [["risk1", "risk2"], ["style1", "style2"]]
                          creates a 2*2 grid.
        selection_strategy: Parent selection method.
                          "uniform" - random selection from archive
                          "sparse" - prioritize under-explored regions
        candidates_per_iteration: How many candidates to generate per iteration.

    Returns:
        A configured MAPElitesSampler instance.

    Example:
        ```python
        sampler = mapelites_sampler(
            mutator=my_mutation_transform,
            initial_candidates=["Start prompt"],
            feature_dimensions=[
                ["violence", "fraud", "hacking"],  # Risk categories
                ["roleplay", "authority", "emotion"],  # Attack styles
            ],
        )
        ```
    """
    return MAPElitesSampler(
        mutator=mutator,
        initial_candidates=initial_candidates,
        feature_dimensions=feature_dimensions,
        selection_strategy=selection_strategy,
        candidates_per_iteration=candidates_per_iteration,
    )
