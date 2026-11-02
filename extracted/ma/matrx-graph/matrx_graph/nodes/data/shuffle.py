"""``data.shuffle`` — put a list in a random-looking order that the SEED decides.

The same items and the same seed give the same order on every machine, every Python version and
every run: the order comes from a SHA-256 byte stream (``sha256(seed_text || counter)``) driving a
Fisher–Yates shuffle with rejection sampling, never from ``random`` (whose string seeding and
algorithms are an implementation detail). A number seed and the same number written as text
give the same order (``42`` and ``"42"``), so a seed typed on a form and one computed upstream
agree.

A shuffle with no seed is refused: an order nobody can reproduce cannot be audited, re-run or
compared, which is the whole point of drawing it here (a blind judging order, a pilot draw).
"""

from __future__ import annotations

import hashlib
import json
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.content_ir.model import KindModel
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success

Seed = str | int | float


class ShuffleInput(KindModel, kind="shuffle_request"):
    items: list[JsonValue] = Field(description="The list to shuffle.")
    seed: Seed | None = Field(
        default=None,
        description="The seed for this run (e.g. a run input). Wins over the step's own seed.",
    )


class ShuffleConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
    seed: Seed | None = Field(
        default=None,
        description="Same seed, same order — every time, on every machine.",
    )
    limit: int | None = Field(
        default=None,
        ge=0,
        le=100_000,
        description="Keep only this many items after shuffling. Empty keeps them all.",
    )


class ShuffleOutput(KindModel, kind="shuffled_list_result"):
    items: list[JsonValue] = Field(description="The items in their shuffled order.")
    permutation: list[int] = Field(
        description="For each output item, its position (from 0) in the original list."
    )
    seed: str = Field(description="The seed that decided the order, as text.")


def seed_text(seed: Seed) -> str:
    """The canonical text of a seed: strings as written; numbers so 42, 42.0 and "42" agree."""
    if isinstance(seed, bool):
        raise ValueError("a seed is text or a number, not true/false")
    if isinstance(seed, str):
        return seed
    if isinstance(seed, float) and seed.is_integer():
        return str(int(seed))
    return json.dumps(seed)


class _ByteStream:
    """An endless, machine-independent byte stream: sha256(seed || 8-byte big-endian counter)."""

    __slots__ = ("_seed", "_counter", "_buffer")

    def __init__(self, seed: str) -> None:
        self._seed = seed.encode("utf-8")
        self._counter = 0
        self._buffer = b""

    def take(self, n: int) -> bytes:
        while len(self._buffer) < n:
            self._buffer += hashlib.sha256(self._seed + self._counter.to_bytes(8, "big")).digest()
            self._counter += 1
        out, self._buffer = self._buffer[:n], self._buffer[n:]
        return out

    def below(self, bound: int) -> int:
        """A uniform integer in [0, bound), by rejection sampling over 8-byte draws."""
        span = 1 << 64
        ceiling = span - (span % bound)
        while True:
            value = int.from_bytes(self.take(8), "big")
            if value < ceiling:
                return value % bound


def seeded_permutation(count: int, seed: str) -> list[int]:
    """The original positions in shuffled order (Fisher–Yates, high index down)."""
    order = list(range(count))
    stream = _ByteStream(seed)
    for i in range(count - 1, 0, -1):
        j = stream.below(i + 1)
        order[i], order[j] = order[j], order[i]
    return order


class ShuffleExecutor:
    """Seeded, reproducible shuffle with an optional limit."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="data.shuffle",
        category=NodeCategory.DATA,
        display_name="Shuffle",
        description="Mix up a list's order. The same seed always gives the same order.",
        input_schema=ShuffleInput,
        input_kind="shuffle_request",
        output_schema=ShuffleOutput,
        output_kind="shuffled_list_result",
        config_schema=ShuffleConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.PURE,
        icon="shuffle",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: ShuffleInput,
        config: ShuffleConfig,
    ) -> NodeResult[ShuffleOutput]:
        _ = ctx
        raw = inputs.seed if inputs.seed is not None else config.seed
        if raw is None or (isinstance(raw, str) and not raw.strip()):
            return failure(
                "missing_seed",
                "data.shuffle needs a seed — set one on the step or feed one in (e.g. a run input). "
                "Without it nobody could reproduce the order."
            )
        try:
            seed = seed_text(raw)
        except ValueError as exc:
            return failure("invalid_seed", f"data.shuffle: {exc}")
        permutation = seeded_permutation(len(inputs.items), seed)
        if config.limit is not None:
            permutation = permutation[: config.limit]
        return success(
            ShuffleOutput(
                items=[inputs.items[i] for i in permutation],
                permutation=permutation,
                seed=seed,
            )
        )


__all__ = [
    "ShuffleConfig",
    "ShuffleExecutor",
    "ShuffleInput",
    "ShuffleOutput",
    "seed_text",
    "seeded_permutation",
]
