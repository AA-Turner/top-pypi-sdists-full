from __future__ import annotations

import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from probe.cli.backfill_coverage import Coverage, Scope
from probe.cli.backfill_ledger import Ledger, Unit
from probe.cli import backfill_legacy as legacy


PROJECT = {"id": "p1", "slug": "alpha", "customer_id": "tenant-a", "workspace_id": "w1"}
SCOPE = Scope("https://example.test", "tenant-a", "w1", "p1")


class Remote:
    def __init__(self, root):
        self.rows = []
        self.blobs = {}
        self.downloads = []
        self.tree_calls = []
        self.transport = SimpleNamespace(get=self.tree)
        for index, path in enumerate(sorted(root.iterdir())):
            data = path.read_bytes()
            ident = f"artifact-{index}"
            self.blobs[ident] = data
            self.rows.append({"id": ident, "name": path.name, "customer_id": "tenant-a",
                "project_id": "p1", "experiment_id": None, "run_id": None,
                "content_hash": hashlib.sha256(data).hexdigest(), "size_bytes": len(data),
                "is_reference": False, "uri": f"r2://test/{ident}", "status": "complete"})

    def resolve_project(self, slug, *, strict=False):
        assert strict
        return PROJECT

    def tree(self, path, *, params):
        assert path == "/v1/projects/p1/artifacts/tree"
        assert params["prefix"] == ""
        offset, limit = params["offset"], params["limit"]
        self.tree_calls.append(offset)
        more = offset + limit < len(self.rows)
        return {"files": self.rows[offset:offset + limit], "folders": [],
                "next_offset": offset + limit if more else None, "truncated": more}

    def download_artifact_to(self, ident, dest, *, max_bytes):
        data = self.blobs[ident]
        self.downloads.append(ident)
        assert max_bytes >= len(data)
        Path(dest).write_bytes(data)
        return {"sha256": hashlib.sha256(data).hexdigest(), "size_bytes": len(data)}


def setup(tmp_path, monkeypatch, count=1):
    root = tmp_path / "source"
    root.mkdir()
    for index in range(count):
        (root / f"file-{index:03}.md").write_text(f"source version {index}")
    monkeypatch.setenv("PROBE_BACKFILL_STATE_DIR", str(tmp_path / "state"))
    old = Ledger.for_folder(root)
    paths = tuple(path.name for path in sorted(root.iterdir()))
    old.record_plan([Unit("old-unit", "alpha", paths)], ["alpha"])
    old.record_approval()
    old.finish_unit("old-unit", ok=True, enqueued=count)
    scratch = old.path.parent / f"{old.path.stem}-manifests"
    scratch.mkdir()
    (scratch / "old-unit.jsonl").write_text("".join(json.dumps({"path": path}) + "\n" for path in paths))
    store = Coverage.for_folder(root, SCOPE)
    return root, paths, old, store, Remote(root)


def test_legacy_adoption_downloads_exact_bytes_and_preserves_old_state(tmp_path, monkeypatch):
    root, paths, old, store, remote = setup(tmp_path, monkeypatch, count=105)
    original = old.path.read_bytes()
    with store.writer() as coverage:
        coverage.observe(root, paths)
        assert legacy.reconcile(coverage, remote, root) == {}
        assert len(coverage.report()["delivered"]) == 105
        assert remote.tree_calls == [0, 100]
        assert len(remote.downloads) == 105
        legacy.reconcile(coverage, remote, root)
        assert len(remote.downloads) == 105, "durable receipts prevent repeated downloads"
    assert old.path.read_bytes() == original
    assert not (store.directory / "legacy-download.partial").exists()


def test_matching_metadata_with_corrupt_bytes_stays_unresolved(tmp_path, monkeypatch):
    root, paths, old, store, remote = setup(tmp_path, monkeypatch)
    remote.blobs["artifact-0"] = b"wrong"
    with store.writer() as coverage:
        coverage.observe(root, paths)
        unresolved = legacy.reconcile(coverage, remote, root)
        assert "bytes differ" in unresolved[paths[0]]["reason"]
        assert coverage.report()["delivered"] == []


@pytest.mark.parametrize("change", ["renamed", "duplicate", "wrong_tenant", "reference"])
def test_ambiguous_identity_or_wrong_transfer_mode_is_never_adopted(tmp_path, monkeypatch, change):
    root, paths, old, store, remote = setup(tmp_path, monkeypatch)
    if change == "renamed":
        remote.rows[0]["name"] = "different-name.md"
    elif change == "duplicate":
        remote.rows.append({**remote.rows[0], "id": "artifact-duplicate"})
    elif change == "wrong_tenant":
        remote.rows[0]["customer_id"] = "tenant-b"
    else:
        remote.rows[0]["is_reference"] = True
    with store.writer() as coverage:
        coverage.observe(root, paths)
        unresolved = legacy.reconcile(coverage, remote, root)
        assert paths[0] in unresolved
        assert remote.downloads == []
        assert coverage.report()["delivered"] == []
        if change == "renamed":
            assert unresolved[paths[0]]["candidates"] == [{"id": "artifact-0", "name": "different-name.md"}]


def test_failed_downloads_also_consume_verification_budget(tmp_path, monkeypatch):
    root, paths, old, store, remote = setup(tmp_path, monkeypatch, count=2)
    monkeypatch.setattr(legacy, "MAX_VERIFY_BYTES", remote.rows[0]["size_bytes"])
    remote.blobs["artifact-0"] = b"wrong"
    with store.writer() as coverage:
        coverage.observe(root, paths)
        unresolved = legacy.reconcile(coverage, remote, root)
        assert "budget reached" in unresolved[paths[1]]["reason"]
        assert remote.downloads == ["artifact-0"]


def test_legacy_counts_without_manifests_do_not_cover_or_upload(tmp_path, monkeypatch):
    root, paths, old, store, remote = setup(tmp_path, monkeypatch)
    (old.path.parent / f"{old.path.stem}-manifests" / "old-unit.jsonl").unlink()
    with store.writer() as coverage:
        coverage.observe(root, paths)
        assert paths[0] in legacy.reconcile(coverage, remote, root)
        assert coverage.report()["delivered"] == []
        assert remote.downloads == []
