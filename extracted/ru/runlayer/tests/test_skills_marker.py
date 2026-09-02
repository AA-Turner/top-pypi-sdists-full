from pathlib import Path

import pytest

from runlayer_cli.skills.marker import managed_marker, managed_marker_skill_id


@pytest.mark.parametrize(
    ("content", "expected_marker", "expected_skill_id"),
    [
        (
            "managed:550e8400-e29b-41d4-a716-446655440000:abc123\n",
            "managed:550e8400-e29b-41d4-a716-446655440000:abc123",
            "550e8400-e29b-41d4-a716-446655440000",
        ),
        ("", None, None),
        ("user:abc123", None, None),
        ("managed:", None, None),
    ],
)
def test_managed_marker_content(
    tmp_path: Path,
    content: str,
    expected_marker: str | None,
    expected_skill_id: str | None,
) -> None:
    (tmp_path / ".installed").write_text(content, encoding="utf-8")

    assert managed_marker(tmp_path) == expected_marker
    assert managed_marker_skill_id(tmp_path) == expected_skill_id


def test_managed_marker_missing(tmp_path: Path) -> None:
    assert managed_marker(tmp_path) is None
    assert managed_marker_skill_id(tmp_path) is None
