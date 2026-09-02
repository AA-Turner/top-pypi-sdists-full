import json
from pathlib import Path

import pytest

from agentic_devtools.ai_providers.availability import (
    _CANONICAL_BODY_PREFIX,
    _PUBLICATION_LOCK_FILENAME,
    curate_availability_matrix,
)
from agentic_devtools.ai_providers.errors import ProviderError


def test_curate_availability_matrix_dry_run_does_not_write_files(tmp_path: Path) -> None:
    evidence_path = tmp_path / "evidence.json"
    doc_path = tmp_path / "adr.md"

    result = curate_availability_matrix(
        dry_run=True,
        evidence_path=evidence_path,
        doc_path=doc_path,
    )

    assert result["marker"] == _CANONICAL_BODY_PREFIX
    assert not evidence_path.exists()
    assert not doc_path.exists()


def test_curate_availability_matrix_writes_evidence_without_publish(tmp_path: Path) -> None:
    evidence_path = tmp_path / "nested" / "evidence.json"
    doc_path = tmp_path / "nested" / "availability.md"

    result = curate_availability_matrix(evidence_path=evidence_path, doc_path=doc_path)

    assert evidence_path.exists()
    assert not doc_path.exists()
    raw = json.loads(evidence_path.read_text(encoding="utf-8"))
    assert raw["body"].startswith(_CANONICAL_BODY_PREFIX)
    assert result["matrix"]["claude-opus-5"] == "available"


def test_curate_availability_matrix_publish_writes_evidence_and_adr(tmp_path: Path) -> None:
    evidence_path = tmp_path / "nested" / "evidence.json"
    doc_path = tmp_path / "nested" / "availability.md"

    result = curate_availability_matrix(publish=True, evidence_path=evidence_path, doc_path=doc_path)

    assert evidence_path.exists()
    assert doc_path.exists()
    raw = json.loads(evidence_path.read_text(encoding="utf-8"))
    assert raw["body"].startswith(_CANONICAL_BODY_PREFIX)
    assert result["matrix"]["claude-opus-5"] == "available"
    adr_content = doc_path.read_text(encoding="utf-8")
    assert "Agent Tasks model availability matrix" in adr_content
    assert str(evidence_path) in adr_content


def test_curate_availability_matrix_non_publish_uses_atomic_write(tmp_path: Path) -> None:
    from unittest.mock import patch

    evidence_path = tmp_path / "evidence.json"

    with patch("agentic_devtools.ai_providers.availability._write_files_atomically") as mock_atomic:
        curate_availability_matrix(evidence_path=evidence_path)

    mock_atomic.assert_called_once()
    written_paths = list(mock_atomic.call_args[0][0].keys())
    assert written_paths == [evidence_path]

    with pytest.raises(ProviderError, match="dry_run.*publish.*cannot"):
        curate_availability_matrix(
            dry_run=True,
            publish=True,
            evidence_path=tmp_path / "ignored.json",
            doc_path=tmp_path / "ignored.md",
        )


def test_curate_availability_matrix_rejects_same_evidence_and_doc_path(tmp_path: Path) -> None:
    same = tmp_path / "same.json"
    with pytest.raises(ProviderError, match="must not resolve to the same file"):
        curate_availability_matrix(publish=True, evidence_path=same, doc_path=same)


def test_curate_availability_matrix_rejects_paths_resolving_to_same_file(tmp_path: Path) -> None:
    evidence_path = tmp_path / "evidence.json"
    doc_path = tmp_path / "nested" / ".." / "evidence.json"
    with pytest.raises(ProviderError, match="must not resolve to the same file"):
        curate_availability_matrix(publish=True, evidence_path=evidence_path, doc_path=doc_path)


def test_curate_availability_matrix_defaults_to_repo_root_paths(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    repo_root = tmp_path / "repo"
    nested = repo_root / "nested" / "cwd"
    nested.mkdir(parents=True)
    (repo_root / ".git").mkdir()
    monkeypatch.chdir(nested)

    curate_availability_matrix(publish=True)

    evidence_path = repo_root / "tests" / "fixtures" / "ai_providers" / "availability" / "evidence.json"
    doc_path = repo_root / "docs" / "architecture-decisions" / "agent-tasks-model-availability.md"
    assert evidence_path.exists()
    assert doc_path.exists()
    assert not (nested / "tests" / "fixtures" / "ai_providers" / "availability" / "evidence.json").exists()
    assert not (nested / "docs" / "architecture-decisions" / "agent-tasks-model-availability.md").exists()

    # The ADR must reference the stable, checkout-independent relative default
    # path rather than the resolved absolute path, so re-running `--publish`
    # from a different checkout does not churn the committed ADR content.
    adr_content = doc_path.read_text(encoding="utf-8")
    assert "tests/fixtures/ai_providers/availability/evidence.json" in adr_content
    assert str(evidence_path) not in adr_content


def test_curate_availability_matrix_requires_explicit_default_paths_without_repo_root(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    with pytest.raises(ProviderError, match="Cannot resolve default evidence path"):
        curate_availability_matrix()


def _expected_lock_path(target: Path) -> Path:
    """Return the expected lock path derived from a resolved output target."""
    resolved = target.resolve(strict=False)
    return resolved.parent / ".agdt-temp" / f"{resolved.name}{_PUBLICATION_LOCK_FILENAME}"


def test_curate_availability_matrix_lock_derives_from_evidence_target_outside_repo(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from unittest.mock import patch

    monkeypatch.chdir(tmp_path)
    evidence_path = tmp_path / "evidence.json"
    expected_lock_path = _expected_lock_path(evidence_path)

    with (
        patch("agentic_devtools.ai_providers.availability.locked_file") as mock_lock,
        patch("agentic_devtools.ai_providers.availability._write_files_atomically"),
    ):
        curate_availability_matrix(evidence_path=evidence_path)

    mock_lock.assert_called_once_with(expected_lock_path, mode="r+")


def test_curate_availability_matrix_serializes_publish_writes_with_file_lock(tmp_path: Path) -> None:
    from unittest.mock import patch

    evidence_path = tmp_path / "evidence.json"
    doc_path = tmp_path / "availability.md"

    with (
        patch("agentic_devtools.ai_providers.availability.locked_file") as mock_lock,
        patch("agentic_devtools.ai_providers.availability._write_files_atomically") as mock_atomic,
    ):
        curate_availability_matrix(publish=True, evidence_path=evidence_path, doc_path=doc_path)

    expected_lock_targets = sorted(
        (_expected_lock_path(evidence_path), _expected_lock_path(doc_path)),
        key=lambda p: p.as_posix(),
    )
    assert mock_lock.call_count == 2
    mock_lock.assert_any_call(expected_lock_targets[0], mode="r+")
    mock_lock.assert_any_call(expected_lock_targets[1], mode="r+")
    mock_atomic.assert_called_once()


def test_curate_availability_matrix_serializes_evidence_only_writes_with_file_lock(tmp_path: Path) -> None:
    from unittest.mock import patch

    evidence_path = tmp_path / "evidence.json"

    with (
        patch("agentic_devtools.ai_providers.availability.locked_file") as mock_lock,
        patch("agentic_devtools.ai_providers.availability._write_files_atomically") as mock_atomic,
    ):
        curate_availability_matrix(evidence_path=evidence_path)

    mock_lock.assert_called_once_with(_expected_lock_path(evidence_path), mode="r+")
    mock_atomic.assert_called_once()


def test_curate_availability_matrix_publish_uses_same_lock_regardless_of_cwd(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Two callers using the same explicit absolute paths must contend on the same locks

    even when their current working directories (and thus resolved repo roots) differ.
    """
    other_cwd = tmp_path / "other-checkout"
    other_cwd.mkdir()
    evidence_path = tmp_path / "evidence.json"
    doc_path = tmp_path / "availability.md"

    from unittest.mock import patch

    with patch("agentic_devtools.ai_providers.availability.locked_file") as mock_lock_first:
        monkeypatch.chdir(tmp_path)
        with patch("agentic_devtools.ai_providers.availability._write_files_atomically"):
            curate_availability_matrix(publish=True, evidence_path=evidence_path, doc_path=doc_path)
        first_lock_paths = {call.args[0] for call in mock_lock_first.call_args_list}

    with patch("agentic_devtools.ai_providers.availability.locked_file") as mock_lock_second:
        monkeypatch.chdir(other_cwd)
        with patch("agentic_devtools.ai_providers.availability._write_files_atomically"):
            curate_availability_matrix(publish=True, evidence_path=evidence_path, doc_path=doc_path)
        second_lock_paths = {call.args[0] for call in mock_lock_second.call_args_list}

    assert first_lock_paths == second_lock_paths
