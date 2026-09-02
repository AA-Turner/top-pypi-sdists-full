"""Tests for _compute_payload_digest."""

import os

import pytest

from agentic_devtools.cli.workflows.orchestrator_commands import _compute_payload_digest


def test_compute_payload_digest_is_stable_for_nested_directories(tmp_path) -> None:
    root = tmp_path / "scratch"
    (root / "nested" / "deeper").mkdir(parents=True)
    (root / "nested" / "file.txt").write_text("payload", encoding="utf-8")

    assert _compute_payload_digest(root) == _compute_payload_digest(root)


def test_compute_payload_digest_changes_when_executable_bit_changes(tmp_path) -> None:
    root = tmp_path / "scratch"
    root.mkdir()
    script = root / "run.sh"
    script.write_text("#!/bin/sh\necho hi\n", encoding="utf-8")
    script.chmod(0o644)
    non_executable_digest = _compute_payload_digest(root)

    script.chmod(0o755)

    assert _compute_payload_digest(root) != non_executable_digest


def test_compute_payload_digest_rejects_symlinks(tmp_path) -> None:
    root = tmp_path / "scratch"
    root.mkdir()
    target = tmp_path / "outside.txt"
    target.write_text("secret", encoding="utf-8")
    (root / "linked.txt").symlink_to(target)

    with pytest.raises(ValueError, match="contains symlink"):
        _compute_payload_digest(root)


def test_compute_payload_digest_rejects_unsupported_path_types(tmp_path) -> None:
    if not hasattr(os, "mkfifo"):
        pytest.skip("mkfifo not available on this platform")

    root = tmp_path / "scratch"
    root.mkdir()
    os.mkfifo(root / "named-pipe")

    with pytest.raises(ValueError, match="unsupported path type"):
        _compute_payload_digest(root)
