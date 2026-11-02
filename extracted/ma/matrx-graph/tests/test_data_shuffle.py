"""``data.shuffle`` — the same seed gives the same order on every machine, Python version and run.

The pinned permutations below were computed once from the SHA-256 Fisher–Yates stream. If one of
them changes, every saved blind-judging order and pilot draw stops being reproducible: that is the
break these tests exist to catch (e.g. a switch to ``random.Random(seed)``, whose string seeding is
an implementation detail).
"""

from __future__ import annotations

import asyncio
import hashlib

import pytest

from matrx_graph.nodes import register_builtin_nodes
from matrx_graph.nodes.data.shuffle import (
    ShuffleConfig,
    ShuffleExecutor,
    ShuffleInput,
    seed_text,
    seeded_permutation,
)
from matrx_graph.types.primitives import ActionTier
from matrx_graph.types.result import Failure, Success

PANELISTS = [
    {"name": "Dr. Jane Doe", "field": "cardiology"},
    {"name": "John Doe", "field": "law"},
    {"name": "Alex Example", "field": "tax"},
    {"name": "Sam Sample", "field": "nutrition"},
    {"name": "Riley Placeholder", "field": "real estate"},
    {"name": "Morgan Test", "field": "cybersecurity"},
    {"name": "Casey Demo", "field": "pediatrics"},
    {"name": "Jordan Mock", "field": "insurance"},
    {"name": "Taylor Fixture", "field": "logistics"},
    {"name": "Quinn Stub", "field": "accounting"},
]


def _run(items, *, seed=None, config_seed=None, limit=None):
    return asyncio.run(
        ShuffleExecutor().execute(
            None, ShuffleInput(items=items, seed=seed), ShuffleConfig(seed=config_seed, limit=limit)
        )
    )


def test_a_seed_gives_the_pinned_order_on_every_machine() -> None:
    assert seeded_permutation(10, "podcast-cast-2026-10") == [4, 3, 0, 9, 5, 6, 7, 1, 2, 8]
    assert seeded_permutation(5, "tripwire") == [2, 0, 3, 4, 1]
    result = _run(PANELISTS, config_seed="podcast-cast-2026-10")
    assert isinstance(result, Success)
    out = result.result
    assert out.permutation == [4, 3, 0, 9, 5, 6, 7, 1, 2, 8]
    assert out.items == [PANELISTS[i] for i in out.permutation]
    assert out.seed == "podcast-cast-2026-10"


def test_the_order_comes_from_sha256_not_pythons_random() -> None:
    """The first swap partner for the last slot is the first 8 bytes of sha256(seed || 0), mod 10."""
    first = int.from_bytes(hashlib.sha256(b"podcast-cast-2026-10" + (0).to_bytes(8, "big")).digest()[:8], "big")
    assert first < (1 << 64) - ((1 << 64) % 10)  # not a rejected draw for this seed
    order = list(range(10))
    j = first % 10
    order[9], order[j] = order[j], order[9]
    assert seeded_permutation(10, "podcast-cast-2026-10")[9] == order[9]


def test_the_same_seed_twice_is_the_same_order_and_a_different_seed_is_not() -> None:
    a = _run(PANELISTS, config_seed="blind-judging-round-3").result
    b = _run(PANELISTS, config_seed="blind-judging-round-3").result
    c = _run(PANELISTS, config_seed="blind-judging-round-4").result
    assert a.permutation == b.permutation
    assert a.permutation != c.permutation
    assert sorted(a.permutation) == list(range(len(PANELISTS)))


def test_a_number_seed_and_the_same_number_as_text_agree() -> None:
    assert seed_text(42) == seed_text("42") == seed_text(42.0) == "42"
    assert _run(PANELISTS, seed=42).result.permutation == [9, 7, 6, 4, 5, 8, 0, 1, 2, 3]
    assert _run(PANELISTS, seed="42").result.permutation == [9, 7, 6, 4, 5, 8, 0, 1, 2, 3]


def test_the_run_seed_wins_over_the_steps_seed() -> None:
    out = _run(PANELISTS, seed="42", config_seed="ignored").result
    assert out.seed == "42"


def test_limit_keeps_the_first_n_of_the_shuffled_order() -> None:
    out = _run(PANELISTS, config_seed="podcast-cast-2026-10", limit=3).result
    assert out.permutation == [4, 3, 0]
    assert out.items == [PANELISTS[4], PANELISTS[3], PANELISTS[0]]


def test_no_seed_is_refused_with_a_sentence() -> None:
    result = _run(PANELISTS)
    assert isinstance(result, Failure)
    assert result.error.code == "missing_seed"
    assert "needs a seed" in result.error.message


@pytest.mark.parametrize("items", [[], ["only"]])
def test_empty_and_single_lists_pass_through(items) -> None:
    out = _run(items, config_seed="x").result
    assert out.items == items and out.permutation == list(range(len(items)))


def test_shuffle_is_registered_as_a_pure_data_step() -> None:
    from matrx_graph.nodes import BUILTIN_VALUES_ARE
    from matrx_graph.executor.registry import NodeRegistry

    registry = NodeRegistry()
    register_builtin_nodes(registry)
    spec = registry.get("data.shuffle").spec
    assert spec.determinism == ActionTier.PURE
    assert spec.display_name == "Shuffle"
    assert BUILTIN_VALUES_ARE["data.shuffle"] == "deterministic"
