import pytest

from agentic_devtools.ai_providers import copilot as copilot_module


def test_validate_segment_accepts_safe_segment() -> None:
    assert copilot_module._validate_segment("owner", "octo-demo_1") == "octo-demo_1"


@pytest.mark.parametrize("value", ["", ".", "..", "a/b", "a b", None, 123])
def test_validate_segment_rejects_unsafe_values(value: object) -> None:
    with pytest.raises(ValueError, match="safe non-empty path segment"):
        copilot_module._validate_segment("owner", value)
