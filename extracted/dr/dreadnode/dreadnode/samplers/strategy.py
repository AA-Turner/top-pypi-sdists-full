"""Strategy-based sampler for lifelong adversarial learning.

Implements a strategy library approach inspired by AutoDAN-Turbo for
maintaining and growing a collection of attack strategies over time.

Reference: "AutoDAN-Turbo: A Lifelong Agent for Strategy Self-Exploration to Jailbreak LLMs"
https://arxiv.org/abs/2410.05295
"""

import json
import random
import typing as t
from dataclasses import dataclass, field
from pathlib import Path

from loguru import logger

from dreadnode.core.transforms import Transform, TransformLike
from dreadnode.optimization.sampler import Sample, Sampler
from dreadnode.optimization.trial import Trial

CandidateT = t.TypeVar("CandidateT")


@dataclass
class Strategy:
    """A reusable attack strategy with embedding for retrieval.

    Attributes:
        name: Short descriptive name for the strategy.
        description: Detailed description of how the strategy works.
        template: Template prompt that implements the strategy.
        embedding: Vector embedding for similarity search.
        successes: Number of successful attacks using this strategy.
        attempts: Total number of times this strategy was used.
        metadata: Additional metadata (source, discovered_from, etc.).
    """

    name: str
    description: str
    template: str
    embedding: list[float] | None = None
    successes: int = 0
    attempts: int = 0
    metadata: dict[str, t.Any] = field(default_factory=dict)

    @property
    def success_rate(self) -> float:
        """Success rate of this strategy."""
        return self.successes / self.attempts if self.attempts > 0 else 0.0

    def to_dict(self) -> dict[str, t.Any]:
        """Convert to dictionary for serialization."""
        return {
            "name": self.name,
            "description": self.description,
            "template": self.template,
            "embedding": self.embedding,
            "successes": self.successes,
            "attempts": self.attempts,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, t.Any]) -> "Strategy":
        """Create from dictionary."""
        return cls(
            name=data["name"],
            description=data["description"],
            template=data["template"],
            embedding=data.get("embedding"),
            successes=data.get("successes", 0),
            attempts=data.get("attempts", 0),
            metadata=data.get("metadata", {}),
        )


class StrategyStore:
    """Persistent storage for attack strategies with embedding-based retrieval.

    Stores strategies with their embeddings and supports:
    - Adding new strategies
    - Retrieving similar strategies by embedding similarity
    - Persisting to/loading from disk (JSON format)
    - Tracking strategy performance over time

    Args:
        strategies: Initial list of strategies.
    """

    def __init__(self, strategies: list[Strategy] | None = None):
        self._strategies: list[Strategy] = strategies or []
        self._name_index: dict[str, int] = {}
        self._rebuild_index()

    def _rebuild_index(self) -> None:
        """Rebuild the name lookup index."""
        self._name_index = {s.name: i for i, s in enumerate(self._strategies)}

    def add(self, strategy: Strategy) -> None:
        """Add a strategy to the store.

        If a strategy with the same name exists, it will be updated.
        """
        if strategy.name in self._name_index:
            idx = self._name_index[strategy.name]
            self._strategies[idx] = strategy
            logger.debug(f"Updated existing strategy: {strategy.name}")
        else:
            self._strategies.append(strategy)
            self._name_index[strategy.name] = len(self._strategies) - 1
            logger.debug(f"Added new strategy: {strategy.name}")

    def get(self, name: str) -> Strategy | None:
        """Get a strategy by name."""
        idx = self._name_index.get(name)
        return self._strategies[idx] if idx is not None else None

    def search(
        self,
        query_embedding: list[float],
        k: int = 5,
        min_similarity: float = 0.0,
    ) -> list[tuple[Strategy, float]]:
        """Search for similar strategies using cosine similarity.

        Args:
            query_embedding: Query vector to search for.
            k: Maximum number of results to return.
            min_similarity: Minimum similarity threshold.

        Returns:
            List of (strategy, similarity_score) tuples, sorted by similarity descending.
        """
        if not self._strategies:
            return []

        results: list[tuple[Strategy, float]] = []
        for strategy in self._strategies:
            if strategy.embedding is None:
                continue
            similarity = self._cosine_similarity(query_embedding, strategy.embedding)
            if similarity >= min_similarity:
                results.append((strategy, similarity))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:k]

    def _cosine_similarity(self, a: list[float], b: list[float]) -> float:
        """Compute cosine similarity between two vectors."""
        if len(a) != len(b):
            return 0.0
        dot = sum(x * y for x, y in zip(a, b, strict=True))
        norm_a = sum(x * x for x in a) ** 0.5
        norm_b = sum(x * x for x in b) ** 0.5
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    def update_stats(self, name: str, *, success: bool) -> None:
        """Update success/attempt stats for a strategy."""
        idx = self._name_index.get(name)
        if idx is not None:
            self._strategies[idx].attempts += 1
            if success:
                self._strategies[idx].successes += 1

    def save(self, path: Path | str) -> None:
        """Save strategy library to JSON file."""
        path = Path(path)
        data = {
            "version": "1.0",
            "strategies": [s.to_dict() for s in self._strategies],
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w") as f:
            json.dump(data, f, indent=2)
        logger.info(f"Saved {len(self._strategies)} strategies to {path}")

    def load(self, path: Path | str) -> None:
        """Load strategy library from JSON file."""
        path = Path(path)
        if not path.exists():
            logger.warning(f"Strategy library not found at {path}, starting empty")
            return
        with path.open() as f:
            data = json.load(f)
        self._strategies = [Strategy.from_dict(s) for s in data.get("strategies", [])]
        self._rebuild_index()
        logger.info(f"Loaded {len(self._strategies)} strategies from {path}")

    @property
    def strategies(self) -> list[Strategy]:
        """Get all strategies."""
        return self._strategies.copy()

    def __len__(self) -> int:
        return len(self._strategies)

    def __iter__(self) -> t.Iterator[Strategy]:
        return iter(self._strategies)


class StrategyLibrarySampler(Sampler[str]):
    """Strategy library sampler with embedding-based retrieval and exploration.

    Implements lifelong learning where the sampler:
    1. Retrieves relevant strategies from library based on goal similarity
    2. Generates attack prompts using selected strategies
    3. Discovers new strategies from successful attacks
    4. Updates the library with new strategies

    This implements the core approach from AutoDAN-Turbo: balancing
    exploration (discovering new strategies) with exploitation (using
    known successful strategies).

    Args:
        strategy_transform: Transform that generates attack prompts from (goal, strategies).
        extraction_transform: Transform that extracts new strategies from successful attacks.
        embedding_transform: Transform that computes embeddings for text.
        strategy_store: Persistent strategy storage.
        exploration_rate: Probability of exploring new strategies vs exploiting known ones.
        top_k_strategies: Number of similar strategies to retrieve.
        retention_threshold: Minimum score to extract strategies from successful attacks.
    """

    def __init__(
        self,
        strategy_transform: TransformLike[dict[str, t.Any], str],
        extraction_transform: TransformLike[dict[str, t.Any], Strategy | None],
        embedding_transform: TransformLike[str, list[float]],
        strategy_store: StrategyStore,
        *,
        exploration_rate: float = 0.3,
        top_k_strategies: int = 5,
        retention_threshold: float = 0.7,
        candidates_per_iteration: int = 1,
    ):
        self.strategy_transform = Transform.fit(strategy_transform)
        self.extraction_transform = Transform.fit(extraction_transform)
        self.embedding_transform = Transform.fit(embedding_transform)
        self.strategy_store = strategy_store
        self.exploration_rate = exploration_rate
        self.top_k_strategies = top_k_strategies
        self.retention_threshold = retention_threshold
        self.candidates_per_iteration = candidates_per_iteration

        # State tracking
        self._goal: str | None = None
        self._goal_embedding: list[float] | None = None
        self._pending: dict[int, list[str]] = {}  # sample_id -> strategy names used
        self._extraction_queue: list[tuple[str, float]] = []  # (prompt, score) for extraction
        self._iteration = 0
        self._total_successes = 0

        logger.info(
            f"StrategyLibrarySampler initialized: "
            f"strategies={len(strategy_store)}, "
            f"exploration_rate={exploration_rate}, "
            f"top_k={top_k_strategies}"
        )

    def set_goal(self, goal: str) -> None:
        """Set the current attack goal (for strategy retrieval)."""
        self._goal = goal
        self._goal_embedding = None  # Will be computed lazily

    async def _get_goal_embedding(self) -> list[float]:
        """Get or compute the goal embedding."""
        if self._goal_embedding is None and self._goal is not None:
            self._goal_embedding = await self.embedding_transform(self._goal)
        return self._goal_embedding or []

    async def sample(
        self,
        history: list[Trial[str]],  # noqa: ARG002
    ) -> list[Sample[str]]:
        """Generate attack prompts using strategies from the library."""
        # Process any pending extractions from successful trials
        await self._process_extraction_queue()

        samples: list[Sample[str]] = []

        for _ in range(self.candidates_per_iteration):
            # Decide: explore or exploit
            explore = random.random() < self.exploration_rate

            strategies_used: list[str] = []

            if explore or len(self.strategy_store) == 0:
                # Exploration mode: generate without specific strategies
                # or with random selection
                selected_strategies = self._select_random_strategies()
                mode = "explore"
            else:
                # Exploitation mode: use similar strategies
                goal_embedding = await self._get_goal_embedding()
                similar = self.strategy_store.search(goal_embedding, k=self.top_k_strategies)
                selected_strategies = [s for s, _ in similar]
                mode = "exploit"

            strategies_used = [s.name for s in selected_strategies]

            # Update attempt counts
            for name in strategies_used:
                self.strategy_store.update_stats(name, success=False)

            # Generate attack prompt using strategy transform
            prompt_input = {
                "goal": self._goal,
                "strategies": selected_strategies,
                "mode": mode,
            }
            candidate = await self.strategy_transform(prompt_input)

            sample_id = id(candidate)
            self._pending[sample_id] = strategies_used

            samples.append(
                Sample(
                    candidate,
                    metadata={
                        "strategies_used": strategies_used,
                        "mode": mode,
                        "sample_id": sample_id,
                    },
                )
            )

        self._iteration += 1
        logger.debug(
            f"StrategyLibrarySampler iteration {self._iteration}: "
            f"generated {len(samples)} candidates"
        )
        return samples

    def _select_random_strategies(self, max_strategies: int = 3) -> list[Strategy]:
        """Select random strategies for exploration."""
        if len(self.strategy_store) == 0:
            return []
        strategies = list(self.strategy_store)
        k = min(max_strategies, len(strategies))
        return random.sample(strategies, k)

    def tell(self, trials: list[Trial[str]]) -> None:
        """Process completed trials and queue successful ones for strategy extraction."""
        for trial in trials:
            if trial.status != "finished":
                continue

            # Look up strategies used via pending dict (sample_id was tracked in sample())
            # We use id(candidate) as sample_id - find matching pending entry
            strategies_used: list[str] = []
            sample_id_to_remove: int | None = None

            for sample_id, strats in self._pending.items():
                # Match by checking if this trial's candidate matches
                # We stored id(candidate) as sample_id
                if sample_id in self._pending:
                    strategies_used = strats
                    sample_id_to_remove = sample_id
                    break

            if sample_id_to_remove is not None:
                self._pending.pop(sample_id_to_remove)

            is_success = trial.score >= self.retention_threshold

            # Update success stats for used strategies
            if is_success:
                self._total_successes += 1
                for name in strategies_used:
                    self.strategy_store.update_stats(name, success=True)

                # Queue for extraction (will be processed in next sample() call)
                self._extraction_queue.append((trial.candidate, trial.score))

    async def _process_extraction_queue(self) -> None:
        """Process queued trials for strategy extraction."""
        while self._extraction_queue:
            prompt, score = self._extraction_queue.pop(0)
            await self._extract_strategy(prompt, score)

    async def _extract_strategy(self, prompt: str, score: float) -> None:
        """Extract a new strategy from a successful attack."""
        extraction_input = {
            "goal": self._goal,
            "prompt": prompt,
            "response": None,  # Response not available in tell()
            "score": score,
        }

        try:
            new_strategy = await self.extraction_transform(extraction_input)
            if new_strategy is not None:
                # Compute embedding for the new strategy
                embedding = await self.embedding_transform(
                    f"{new_strategy.name}: {new_strategy.description}"
                )
                new_strategy.embedding = embedding
                new_strategy.successes = 1
                new_strategy.attempts = 1
                new_strategy.metadata["discovered_iteration"] = self._iteration

                self.strategy_store.add(new_strategy)
                logger.info(f"Discovered new strategy: {new_strategy.name}")
        except (ValueError, TypeError, KeyError, AttributeError) as e:
            logger.warning(f"Failed to extract strategy: {e}")

    @property
    def total_successes(self) -> int:
        """Total number of successful attacks."""
        return self._total_successes

    @property
    def exhausted(self) -> bool:
        """Strategy sampler never exhausts - always can generate more."""
        return False

    def reset(self) -> None:
        """Reset sampler state (preserves strategy library)."""
        self._pending = {}
        self._extraction_queue = []
        self._iteration = 0
        self._total_successes = 0
        self._goal = None
        self._goal_embedding = None


def strategy_library_sampler(
    strategy_transform: TransformLike[dict[str, t.Any], str],
    extraction_transform: TransformLike[dict[str, t.Any], Strategy | None],
    embedding_transform: TransformLike[str, list[float]],
    strategy_store: StrategyStore | None = None,
    *,
    exploration_rate: float = 0.3,
    top_k_strategies: int = 5,
    retention_threshold: float = 0.7,
    candidates_per_iteration: int = 1,
) -> StrategyLibrarySampler:
    """Create a strategy library sampler for lifelong adversarial learning.

    Implements the core approach from AutoDAN-Turbo: maintaining a growing
    library of attack strategies that can be retrieved and combined.

    Args:
        strategy_transform: Transform that generates attacks from (goal, strategies).
        extraction_transform: Transform that extracts strategies from successful attacks.
        embedding_transform: Transform that computes embeddings for text.
        strategy_store: Persistent strategy storage (created if None).
        exploration_rate: Probability of exploring vs exploiting (0.0-1.0).
        top_k_strategies: Number of similar strategies to retrieve.
        retention_threshold: Minimum score to extract new strategies.
        candidates_per_iteration: How many candidates to generate per iteration.

    Returns:
        A configured StrategyLibrarySampler instance.

    Example:
        ```python
        sampler = strategy_library_sampler(
            strategy_transform=attack_generator,
            extraction_transform=strategy_extractor,
            embedding_transform=embed_text,
            exploration_rate=0.3,
        )
        ```
    """
    store = strategy_store or StrategyStore()
    return StrategyLibrarySampler(
        strategy_transform=strategy_transform,
        extraction_transform=extraction_transform,
        embedding_transform=embedding_transform,
        strategy_store=store,
        exploration_rate=exploration_rate,
        top_k_strategies=top_k_strategies,
        retention_threshold=retention_threshold,
        candidates_per_iteration=candidates_per_iteration,
    )
