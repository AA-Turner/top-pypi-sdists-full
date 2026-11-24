"""2026-11-18: rerank-v4.0-pro is catalogued with interaction "rerank"; both vocabularies must name it."""

from matrx_ai.providers.capability_vocabulary import INTERACTION_MODES, InteractionMode  # type: ignore[attr-defined]
from typing import get_args


def test_rerank_is_named() -> None:
    assert "rerank" in INTERACTION_MODES
    assert "rerank" in get_args(InteractionMode)


def test_unknown_mode_is_still_unknown() -> None:
    assert "rerankk" not in INTERACTION_MODES
