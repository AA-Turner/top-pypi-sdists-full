"""An agent's successful exit cannot certify omitted or misfiled source files."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from probe.cli import backfill, backfill_ledger, backfill_run
from probe.cli.backfill_manifest import validate_manifest


@pytest.mark.parametrize("bad", [
    {"path": "outside.py"},
    {"path": "../a.py"},
    {"path": "a.py", "reference": "false"},
    {"path": "a.py", "notes": []},
    {"path": "a.py", "project": "another-project"},
    {"path": "a.py", "name": "renamed.py"},
])
def test_invalid_rows_never_cover_assigned_files(tmp_path, bad):
    manifest = tmp_path / "manifest.jsonl"
    manifest.write_text(json.dumps(bad) + '\n{"path":"b.py"}\n')
    checked = validate_manifest(manifest, ("a.py", "b.py"), root=tmp_path)
    assert not checked.complete
    assert checked.missing == ("a.py",)
    assert checked.rows == ({"path": "b.py"},)


def test_conflicting_duplicate_is_not_resolved_by_row_order(tmp_path):
    manifest = tmp_path / "manifest.jsonl"
    manifest.write_text('{"path":"a.py","reference":false}\n'
                        '{"path":"a.py","reference":true}\n')
    checked = validate_manifest(manifest, ("a.py",), root=tmp_path)
    assert checked.rows == ()
    assert checked.missing == ("a.py",)
    assert "duplicate" in checked.describe()


def test_unit_success_requires_every_assigned_path(tmp_path, monkeypatch):
    folder = tmp_path / "folder"
    folder.mkdir()
    work = tmp_path / "work"
    work.mkdir()
    unit = backfill_ledger.Unit("unit", "project", ("a.py", "b.py"))
    ledger = backfill_ledger.Ledger.for_folder(folder, directory=work)
    ledger.record_plan([unit], ["project"])

    def launch(*args, **kwargs):
        (work / "unit.jsonl").write_text('{"path":"a.py"}\n')
        return True, "Imported both files"

    monkeypatch.setattr(backfill, "launch_agent", launch)
    outcome = backfill_run.run_unit(folder, unit, agent=backfill.Agent.CODEX,
                                   ledger=ledger, work_dir=work)
    assert not outcome.ok
    assert outcome.rows == 1
    assert "b.py" in outcome.detail
    assert ledger.read().outstanding()[0].unit == unit


def test_external_symlink_cannot_be_manifested(tmp_path):
    folder = tmp_path / "folder"
    folder.mkdir()
    (folder / "a.py").symlink_to(tmp_path / "outside.py")
    manifest = tmp_path / "manifest.jsonl"
    manifest.write_text('{"path":"a.py"}\n')
    checked = validate_manifest(manifest, ("a.py",), root=folder)
    assert not checked.complete
    assert not checked.rows


def test_enqueue_revalidates_legacy_manifests_and_uploads_only_valid_rows(tmp_path, monkeypatch):
    manifest = tmp_path / "unit.jsonl"
    manifest.write_text('{"path":"a.py"}\n{"path":"outside.py"}\n')
    unit = backfill_ledger.Unit("unit", "project", ("a.py", "b.py"))
    received = []

    def run(argv, **kwargs):
        selected = Path(argv[argv.index("--from-manifest") + 1])
        received.extend(json.loads(line) for line in selected.read_text().splitlines())
        return SimpleNamespace(stdout='{"enqueued":1,"failed":0}', stderr="", returncode=0)

    monkeypatch.setattr("subprocess.run", run)
    count, problems = backfill_run.enqueue_manifests(
        tmp_path, [backfill_run.UnitOutcome(unit, True, manifest, 2)], project_of={"unit": "project"}
    )
    assert count == 1
    assert received == [{"path": "a.py"}]
    assert problems and "b.py" in problems[0]
    assert "outside.py" in manifest.read_text(), "keep rejected agent output for diagnosis"


def test_dotfiles_and_extensionless_names_stay_exact(tmp_path):
    manifest = tmp_path / "manifest.jsonl"
    paths = (".flake8", "Dockerfile", "nested/λ.txt")
    manifest.write_text("".join(json.dumps({"path": p}) + "\n" for p in paths))
    checked = validate_manifest(manifest, paths, root=tmp_path)
    assert checked.complete
    assert tuple(row["path"] for row in checked.rows) == paths
