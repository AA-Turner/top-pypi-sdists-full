"""Tests for filtering colliding skills while preserving managed entries."""

from pathlib import Path

import pytest

from agentic_devtools.skill_injector_prepare_skills import _filter_colliding_skills


def test_no_collisions_return_original_mappings(tmp_path: Path) -> None:
    origins = {"my-skill/SKILL.md": tmp_path / "SKILL.md"}
    cache: dict[Path, dict[str, object]] = {}

    filtered_origins, filtered_cache, selected_count, shared_collision = _filter_colliding_skills(
        tmp_path, origins, cache, set(), set()
    )

    assert filtered_origins is origins
    assert filtered_cache is cache
    assert selected_count == 1
    assert shared_collision is False


def test_shared_collision_is_reported_without_filtering(tmp_path: Path) -> None:
    origins = {
        "fingerprint.py": tmp_path / "fingerprint.py",
        "my-skill/SKILL.md": tmp_path / "SKILL.md",
    }

    with pytest.warns(RuntimeWarning, match="refusing to inject bundled skills"):
        filtered_origins, _cache, selected_count, shared_collision = _filter_colliding_skills(
            tmp_path,
            origins,
            {},
            set(),
            {"fingerprint.py"},
        )

    assert filtered_origins is origins
    assert selected_count == 1
    assert shared_collision is True
