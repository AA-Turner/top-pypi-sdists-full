import pytest

from mistralai.workflows.testing.constants import _current_version_is_older


@pytest.mark.parametrize(
    ("current", "minimum", "expected"),
    [
        # Unset API_VERSION runs all tests
        ("", "2026-1", False),
        # Version below the requirement is older
        ("2026-1", "2026-5", True),
        ("2025-12", "2026-1", True),
        # Version equal to the requirement is not older
        ("2026-5", "2026-5", False),
        # Version above the requirement is not older
        ("2026-5", "2026-1", False),
        ("2027-1", "2026-5", False),
        # Multi-digit months compare numerically, not lexicographically
        ("2026-10", "2026-5", False),
        ("2026-12", "2026-5", False),
        ("2026-5", "2026-10", True),
    ],
)
def test_current_version_is_older(
    current: str,
    minimum: str,
    expected: bool,
) -> None:
    assert _current_version_is_older(current, minimum) == expected
