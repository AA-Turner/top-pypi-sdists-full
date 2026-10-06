"""A non-positive output-token cap means "no cap" — no provider accepts 0.

Live 2026-10-04: a chat turn carried ``max_output_tokens: 0`` from its config
and Gemini refused the whole request ("max_output_tokens must be positive").
"""

from __future__ import annotations

import pytest

from matrx_ai.config.llm_params import LLMParams, normalize_max_output_tokens
from matrx_ai.config.unified_config import UnifiedConfig


@pytest.mark.parametrize("value", [0, -1, 0.0, -3.5, "0", "-2"])
def test_non_positive_cap_normalizes_to_unset(value: object) -> None:
    assert normalize_max_output_tokens(value) is None


@pytest.mark.parametrize(("value", "expected"), [(1, 1), (4096, 4096), (2048.9, 2048), ("512", 512), (None, None)])
def test_positive_cap_survives(value: object, expected: object) -> None:
    assert normalize_max_output_tokens(value) == expected


def test_runtime_config_never_sends_a_zero_cap() -> None:
    config = UnifiedConfig.from_dict({"model": "gemini-2.5-flash", "messages": [], "max_output_tokens": 0})
    assert config.max_output_tokens is None
    assert "max_output_tokens" not in config.to_dict() or config.to_dict()["max_output_tokens"] is None


def test_request_override_never_sends_a_zero_cap() -> None:
    assert LLMParams(max_output_tokens=0).max_output_tokens is None
