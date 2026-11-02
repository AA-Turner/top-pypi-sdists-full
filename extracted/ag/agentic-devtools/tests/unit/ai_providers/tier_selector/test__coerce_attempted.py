import pytest

from agentic_devtools.ai_providers.tier_selector import _coerce_attempted


def test_coerce_attempted_validates_and_filters_values() -> None:
    assert _coerce_attempted(None) == set()
    with pytest.raises(ValueError):
        _coerce_attempted("model-a")
    with pytest.raises(ValueError):
        _coerce_attempted(["model-a", 1])  # type: ignore[list-item]
    with pytest.raises(ValueError):
        _coerce_attempted([b"model-a"])  # type: ignore[list-item]
    with pytest.raises(ValueError):
        _coerce_attempted([""])
    assert _coerce_attempted(["model-a", "model-b"]) == {"model-a", "model-b"}
