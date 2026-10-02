"""Regression cases found at the folder/SDK/CLI integration boundaries."""

import importlib
import json
from types import SimpleNamespace

import pytest
import typer

from probe.cli.backfill_coverage import Coverage, Scope
from probe.cli.backfill_delivery import enqueue
from probe.sdk.client import Client
from probe.sdk.config import Settings
from probe.sdk.errors import ValidationError
from probe.sdk.journal import Journal, drain


@pytest.mark.parametrize("queued_before_move", [False, True])
def test_reference_remount_preserves_intent_before_and_after_enqueue(
    tmp_path, monkeypatch, queued_before_move,
):
    from probe.sdk import journal as jm

    monkeypatch.setattr(jm, "MIN_FREE_BYTES", 0)
    source = tmp_path / "original"
    source.mkdir()
    (source / "weights.pt").write_bytes(b"weights")
    scope = Scope("http://test", "tenant", "workspace", "project")
    project = {"id": "project", "slug": "project", "customer_id": "tenant", "workspace_id": "workspace"}
    store = Coverage.for_folder(source, scope, directory=tmp_path / "coverage")
    with Client(settings=Settings(base_url="http://test", token="test-token"),
                spool_dir=tmp_path / "outbox", auto_drain=False,
                async_writes=False, attribution="backfill") as client:
        with store.writer() as state:
            state.observe(source, ["weights.pt"])
            state.approve({"weights.pt": project})
            state.remember_manifest("weights.pt", {"path": "weights.pt", "reference": True})
            original = state.intend(state.rows()[0], reference=True,
                                    uri=(source / "weights.pt").as_uri())
            if queued_before_move:
                assert enqueue(state, client, source) == (1, [])
        moved = source.rename(tmp_path / "moved")
        resumed = Coverage.for_folder(moved, scope, directory=tmp_path / "coverage", source_id=store.source_id)
        with resumed.writer() as state:
            state.observe(moved, ["weights.pt"])
            assert enqueue(state, client, moved) == (1, [])
            assert state.rows()[0]["correlation"] == original["correlation"]
            assert state.conn.execute("SELECT COUNT(*) FROM versions").fetchone()[0] == 1
        # The client's own receipt namespace: a token passed in code queues in
        # its credential's folder (#2035), not the shared root's.
        operations = client._delivery_journal().pending()
        assert len(operations) == 1
        assert original["uri"] in json.dumps(operations[0][1])
        assert (moved / "weights.pt").as_uri() not in json.dumps(operations[0][1])


@pytest.mark.parametrize("failed", [False, True])
def test_outbox_status_includes_receipt_namespace(tmp_path, monkeypatch, capsys, failed):
    module = importlib.import_module("probe.cli.main")
    root = Journal(tmp_path / "outbox")
    child = Journal.for_receipts(root.dir)
    child.append_http("POST", "/v1/projects/p/artifacts", {
        "name": "weights.pt", "uri": "file:///original/weights.pt", "is_reference": True,
    }, correlation="review:reference")
    if failed:
        def reject(*args, **kwargs):
            raise ValidationError("test rejection", status=422)
        remote = SimpleNamespace(transport=SimpleNamespace(request=reject))
        assert drain(child, client_factory=lambda _: remote).dead_lettered == 1
    monkeypatch.setattr(module, "_journal", lambda: root)
    with pytest.raises(typer.Exit) as result:
        module.outbox_status(verbose=True, run=None)
    assert result.value.exit_code == 2
    status = json.loads(capsys.readouterr().out)
    assert status["failed" if failed else "pending"] == 1
    assert len(status["ops"]) == 1
    module.outbox_status(verbose=True, run="unrelated-run")
    assert json.loads(capsys.readouterr().out)["ops"] == []
