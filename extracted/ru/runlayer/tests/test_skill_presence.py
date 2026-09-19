"""Tests for durable host skill-presence reconciliation state."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from runlayer_cli.scan import skill_presence
from runlayer_cli.scan.skill_presence import (
    SkillPresenceParams,
    build_state,
    compute_removals,
    load_state,
    path_hash,
    save_state,
)


def _state(
    *,
    project: tuple[str, ...] = (),
    global_: tuple[str, ...] = (),
    depth: int = 7,
    home: str | None = "/home/alice",
):
    return build_state(
        SkillPresenceParams(project_depth=depth, home=home),
        project_paths=project,
        global_paths=global_,
    )


def test_state_persists_only_sorted_deduplicated_path_hashes(tmp_path: Path) -> None:
    state_path = tmp_path / "skill-presence.json"
    raw_paths = (
        "/home/alice/repo/.agents/skills/release",
        "/home/alice/.claude/skills/review",
    )
    state = _state(
        project=(raw_paths[0], raw_paths[0]),
        global_=(raw_paths[1],),
    )

    assert (
        path_hash(raw_paths[0])
        == hashlib.md5(raw_paths[0].encode("utf-8"), usedforsecurity=False).hexdigest()
    )
    assert save_state(state, state_path)

    payload = json.loads(state_path.read_text(encoding="utf-8"))
    serialized = state_path.read_text(encoding="utf-8")
    assert payload == {
        "version": 1,
        "params": {"project_depth": 7, "home": "/home/alice"},
        "phases": {
            "project": [path_hash(raw_paths[0])],
            "global": [path_hash(raw_paths[1])],
        },
    }
    assert all(raw_path not in serialized for raw_path in raw_paths)
    assert load_state(state_path) == state


def test_path_hash_is_total_over_surrogateescape_paths() -> None:
    # A crawled filename with a non-UTF-8 byte decodes to a lone surrogate;
    # a strict encode raised UnicodeEncodeError and aborted presence-state build.
    raw = b"/home/alice/repo/.agents/skills/rel\xffease"
    escaped = raw.decode("utf-8", "surrogateescape")

    digest = path_hash(escaped)

    assert digest == hashlib.md5(raw, usedforsecurity=False).hexdigest()
    assert skill_presence._sorted_hashes((escaped, escaped)) == (digest,)


def test_compute_removals_uses_union_of_phases() -> None:
    previous = _state(
        project=("/project/removed", "/shared"),
        global_=("/global/removed", "/shared"),
    )
    current = _state(project=("/shared",), global_=("/global/current",))

    assert compute_removals(previous, current, crawl_complete=True) == sorted(
        [path_hash("/project/removed"), path_hash("/global/removed")]
    )


def test_compute_removals_without_prior_state_is_baseline() -> None:
    assert (
        compute_removals(None, _state(project=("/current",)), crawl_complete=True) == []
    )


def test_compute_removals_suppressed_for_incomplete_crawl() -> None:
    previous = _state(project=("/removed",))
    current = _state()

    assert compute_removals(previous, current, crawl_complete=False) == []


def test_compute_removals_suppressed_when_params_change() -> None:
    previous = _state(project=("/removed",), depth=7)

    assert compute_removals(previous, _state(depth=8), crawl_complete=True) == []
    assert (
        compute_removals(previous, _state(home="/home/bob"), crawl_complete=True) == []
    )


def test_compute_removals_survive_project_set_changes() -> None:
    """Discovered projects are crawl output, not a comparability input.

    Deleting a repository removes its skills in the same scan that changes the
    project set; that must still yield removals.
    """
    previous = _state(
        project=(
            "/home/alice/repo/.agents/skills/release",
            "/home/alice/other/.agents/skills/kept",
        )
    )
    current = _state(project=("/home/alice/other/.agents/skills/kept",))

    assert compute_removals(previous, current, crawl_complete=True) == [
        path_hash("/home/alice/repo/.agents/skills/release")
    ]


def test_legacy_roots_params_load_as_no_prior_state(tmp_path: Path) -> None:
    state_path = tmp_path / "skill-presence.json"
    state_path.write_text(
        json.dumps(
            {
                "version": 1,
                "params": {"project_depth": 7, "roots": ["/home/alice"]},
                "phases": {"project": [path_hash("/removed")], "global": []},
            }
        ),
        encoding="utf-8",
    )

    assert load_state(state_path) is None


def test_save_atomically_replaces_from_same_directory(
    tmp_path: Path, monkeypatch
) -> None:
    state_path = tmp_path / "skill-presence.json"
    state_path.write_text('{"old":true}', encoding="utf-8")
    replacement = _state(project=("/replacement",))
    real_replace = os.replace
    replace_calls: list[tuple[Path, Path]] = []

    def observe_replace(source: str, destination: str | Path) -> None:
        source_path = Path(source)
        destination_path = Path(destination)
        assert source_path.parent == state_path.parent
        assert source_path.exists()
        replace_calls.append((source_path, destination_path))
        real_replace(source, destination)

    monkeypatch.setattr(skill_presence.os, "replace", observe_replace)

    assert save_state(replacement, state_path)
    assert replace_calls and replace_calls[0][1] == state_path
    assert load_state(state_path) == replacement


def test_corrupt_file_loads_as_no_prior_state(tmp_path: Path) -> None:
    state_path = tmp_path / "skill-presence.json"
    state_path.write_text(
        json.dumps(
            {
                "version": 1,
                "params": {"project_depth": 7, "home": "/home/alice"},
                "phases": {"project": ["/raw/path"], "global": []},
            }
        ),
        encoding="utf-8",
    )

    assert load_state(state_path) is None
    assert (
        compute_removals(
            load_state(state_path),
            _state(project=("/current",)),
            crawl_complete=True,
        )
        == []
    )


def test_missing_or_wrong_version_loads_as_no_prior_state(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing.json"
    wrong_version_path = tmp_path / "wrong-version.json"
    payload = _state(project=("/current",)).to_dict()
    payload["version"] = True
    wrong_version_path.write_text(json.dumps(payload), encoding="utf-8")

    assert load_state(missing_path) is None
    assert load_state(wrong_version_path) is None


def test_write_failure_is_best_effort_and_preserves_old_state(
    tmp_path: Path, monkeypatch
) -> None:
    state_path = tmp_path / "skill-presence.json"
    previous = _state(project=("/previous",))
    assert save_state(previous, state_path)

    def fail_replace(_source: str, _destination: str | Path) -> None:
        raise OSError("read-only filesystem")

    monkeypatch.setattr(skill_presence.os, "replace", fail_replace)

    assert save_state(_state(project=("/current",)), state_path) is False
    assert load_state(state_path) == previous
    assert list(tmp_path.glob("*.tmp")) == []
