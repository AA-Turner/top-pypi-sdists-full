"""A folder import whose approved file is redacted on upload still finishes.

Uploads replace credential-shaped spans before they are hashed, so such a file
lands under its REDACTED digest. CLIs 0.175.0-0.281.0 stored that receipt with
nothing tying it to the approved file, and the import's receipt check failed it
on every run ("Delivery receipt does not match the approved file, bytes and
destination", 2026-10-20, a 157-file folder stuck at 144). The journal now
stamps the source digest it verified (`source_content_hash`); these pin every
way a version reaches, or must not reach, delivered.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from probe.cli import backfill_record
from probe.cli.backfill_coverage import Coverage, Scope
from probe.cli.backfill_delivery import enqueue
from probe.sdk import errors
from probe.sdk import journal as jm
from probe.sdk import secret_gate
from probe.sdk.client import Client
from probe.sdk.config import Settings
from probe.sdk.journal import DELIVERY_SCHEMA, drain
from probe.sdk.redaction import scrub_text

TOKEN = "ghp_KKF0RDt0Xaetn6QMfStFUWSus4jowQUux6hu"
SECRET = f'GITHUB_TOKEN = "{TOKEN}"\n'.encode()
PROJECT = {"id": "project", "slug": "project", "customer_id": "tenant", "workspace_id": "workspace"}
MISMATCH = "Receipt reconciliation failed: Delivery receipt does not match the approved file, bytes and destination."


@pytest.fixture(autouse=True)
def isolated(monkeypatch, tmp_path):
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config.json"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.delenv("PROBE_ATTRIBUTION", raising=False)
    monkeypatch.setattr(jm, "MIN_FREE_BYTES", 0)


class Server:
    def __init__(self):
        self.live = {}

    def upload_fingerprinted(self, anchor, anchor_id, name, path, *, digest, size, **kwargs):
        data = Path(path).read_bytes()
        assert hashlib.sha256(data).hexdigest() == digest and TOKEN.encode() not in data
        return self.live.setdefault((anchor_id, name, digest), {
            "id": f"artifact-{len(self.live)}", "name": name, "status": "complete",
            "uri": f"r2://artifacts/{digest}", "content_hash": digest,
            "size_bytes": size, "is_reference": False,
        })


def _setup(tmp_path, content=SECRET, path="a.py"):
    folder = tmp_path / "repo"
    (folder / path).parent.mkdir(parents=True, exist_ok=True)
    (folder / path).write_bytes(content)
    store = Coverage.for_folder(folder, Scope("http://test", "tenant", "workspace", "project"),
                                directory=tmp_path / "coverage")
    client = Client(settings=Settings(base_url="http://test", token="test-token"),
                    spool_dir=tmp_path / "outbox", auto_drain=False, async_writes=False,
                    attribution="backfill")
    with store.writer() as state:
        state.observe(folder, [path])
        state.approve({path: PROJECT})
        state.remember_manifest(path, {"path": path})
    return folder, store, client


def _old_cli(monkeypatch):
    """Stage ops the way CLIs before the stamp did: no `source_content_hash`."""
    original = jm.Journal._publish_receipt_op

    def unstamped(self, correlation, request, op, publish=None):
        (op.get("upload") or {}).pop("source_content_hash", None)
        return original(self, correlation, request, op, publish)

    monkeypatch.setattr(jm.Journal, "_publish_receipt_op", unstamped)


def _error(state):
    return state.conn.execute(
        "SELECT v.error FROM files f JOIN versions v USING(correlation)").fetchone()[0]


def test_an_old_cli_redacted_receipt_is_delivered_on_resume_without_uploading_again(
        tmp_path, monkeypatch):
    folder, store, client = _setup(tmp_path)
    server = Server()
    with client, store.writer() as state:
        with monkeypatch.context() as m:
            _old_cli(m)
            assert enqueue(state, client, folder) == (1, [])
        assert drain(client._delivery_journal(), client_factory=lambda _: server).delivered == 1
        correlation = state.rows()[0]["correlation"]
        assert "source_content_hash" not in client.delivery_receipt(correlation)
        state.failure(correlation, MISMATCH)  # what CLI 0.281.0 recorded
        assert state.report()["unresolved"] == ["a.py"]
        state.reconcile(client)
        assert state.report()["delivered"] == ["a.py"]
        assert _error(state) is None and len(server.live) == 1


def test_a_new_cli_redacted_file_lands_delivered_with_its_stamp(tmp_path):
    folder, store, client = _setup(tmp_path)
    with client, store.writer() as state:
        assert enqueue(state, client, folder) == (1, [])
        correlation = state.rows()[0]["correlation"]
        state.failure(correlation, "Receipt reconciliation failed: transient")
        assert drain(client._delivery_journal(), client_factory=lambda _: Server()).delivered == 1
        receipt = client.delivery_receipt(correlation)
        assert receipt["source_content_hash"] == state.rows()[0]["approved_hash"] != receipt["content_hash"]
        state.reconcile(client)
        assert state.report()["delivered"] == ["a.py"] and _error(state) is None


def test_an_upload_queued_by_the_old_cli_lands_after_the_upgrade(tmp_path, monkeypatch):
    folder, store, client = _setup(tmp_path)
    with client, store.writer() as state:
        with monkeypatch.context() as m:
            _old_cli(m)
            assert enqueue(state, client, folder) == (1, [])
        assert state.report()["queued"] == ["a.py"]
        drain(client._delivery_journal(), client_factory=lambda _: Server())
        state.reconcile(client)
        assert state.report()["delivered"] == ["a.py"]


def _receipt(intent, **fields):
    return {"correlation": intent["correlation"], "state": "delivered", "status": "complete",
            "artifact_id": "x", "anchor": "project", "anchor_id": "project", "name": "a.py",
            "content_hash": "f" * 64, "size_bytes": 9, "is_reference": intent["mode"] == "reference",
            "readable": intent["mode"] == "upload", "uri": intent["uri"],
            "schema": DELIVERY_SCHEMA, "request_digest": "d" * 64, **fields}


@pytest.mark.parametrize("reference,fields", [
    (False, {"source_content_hash": "e" * 64}),  # stamped for other bytes
    (True, {}),  # a pointer never accepts other bytes, stamped or not
])
def test_reconcile_refuses_a_receipt_for_other_bytes(tmp_path, reference, fields):
    _folder, store, _client = _setup(tmp_path)
    with store.writer() as state:
        intent = state.intend(state.rows()[0], reference=reference,
                              uri="file:///repo/a.py" if reference else None)
        state.reconcile(SimpleNamespace(delivery_state=lambda _c: _receipt(intent, **fields)))
        assert state.report()["unresolved"] == ["a.py"]
        assert "does not match" in _error(state)


def test_a_dead_redacted_file_is_delivered_on_resume(tmp_path, monkeypatch):
    folder, store, client = _setup(tmp_path)
    with client, store.writer() as state:
        with monkeypatch.context() as m:
            _old_cli(m)
            enqueue(state, client, folder)
        drain(client._delivery_journal(), client_factory=lambda _: Server())
        state.failure(state.rows()[0]["correlation"], MISMATCH)
        state.mark_dead(["a.py"], "u1: died")
        assert state.report()["dead"] == ["a.py"]
        state.reconcile(client)
        assert state.report()["delivered"] == ["a.py"] and state.dead_reasons() == {}


def test_retrying_a_dead_file_reuses_its_redacted_receipt(tmp_path, monkeypatch):
    folder, store, client = _setup(tmp_path)
    server = Server()
    with client, store.writer() as state:
        with monkeypatch.context() as m:
            _old_cli(m)
            enqueue(state, client, folder)
        drain(client._delivery_journal(), client_factory=lambda _: server)
        correlation = state.rows()[0]["correlation"]
        state.failure(correlation, MISMATCH)
        state.mark_dead(["a.py"], "u1: died")
        assert state.clear_dead(["a.py"]) == 1
        state.approve({"a.py": PROJECT})
        state.remember_manifest("a.py", {"path": "a.py"})
        assert enqueue(state, client, folder) == (0, [])
        assert state.rows()[0]["correlation"] == correlation
        assert state.report()["delivered"] == ["a.py"] and len(server.live) == 1


def test_a_changed_file_is_not_covered_by_its_old_redacted_receipt(tmp_path, monkeypatch):
    folder, store, client = _setup(tmp_path)
    with client, store.writer() as state:
        with monkeypatch.context() as m:
            _old_cli(m)
            enqueue(state, client, folder)
        drain(client._delivery_journal(), client_factory=lambda _: Server())
        old = state.rows()[0]["correlation"]
        state.failure(old, MISMATCH)
        (folder / "a.py").write_bytes(SECRET + b"# edited\n")
        state.observe(folder, ["a.py"])
        state.approve({"a.py": PROJECT}, changed=True)
        state.reconcile(client)
        assert state.conn.execute("SELECT receipt FROM versions WHERE correlation=?", (old,)).fetchone()[0]
        assert state.report()["delivered"] == []


def test_a_cut_name_redacted_file_is_reissued_and_lands(tmp_path, monkeypatch):
    path = "apps/web/pages/Admin/Users/Edit.tsx"
    folder, store, client = _setup(tmp_path, path=path)
    server = Server()
    with client, store.writer() as state:
        with monkeypatch.context() as legacy:
            legacy.setattr(jm, "scrub_string", scrub_text)  # CLI 0.260.0's cut names
            _old_cli(legacy)
            assert enqueue(state, client, folder) == (1, [])
        drain(client._delivery_journal(), client_factory=lambda _: server)
        state.reconcile(client)
        assert state.report()["delivered"] == []
        assert enqueue(state, client, folder) == (1, [])
        drain(client._delivery_journal(), client_factory=lambda _: server)
        state.reconcile(client)
        assert state.report()["delivered"] == [path]
        stale = state.conn.execute(
            "SELECT receipt FROM versions WHERE intent NOT LIKE '%reissue_of%'").fetchone()
        assert stale[0] is None


def test_a_pending_redacted_intent_keeps_its_stamp(tmp_path):
    folder, store, client = _setup(tmp_path)
    with client, store.writer() as state:
        enqueue(state, client, folder)
        outbox = client._delivery_journal()
        for op in outbox.ops_dir.iterdir():
            op.unlink()  # the intent committed, its op file did not
        correlation = state.rows()[0]["correlation"]
        assert client.delivery_state(correlation)["state"] == "pending"
        enqueue(state, client, folder)
        assert drain(outbox, client_factory=lambda _: Server()).delivered == 1
        state.reconcile(client)
        assert client.delivery_receipt(correlation)["source_content_hash"]
        assert state.report()["delivered"] == ["a.py"]


def test_a_dead_lettered_redacted_op_keeps_its_stamp(tmp_path):
    folder, store, client = _setup(tmp_path)

    class Down:
        def upload_fingerprinted(self, *args, **kwargs):
            raise errors.ValidationError("refused")

    with client, store.writer() as state:
        enqueue(state, client, folder)
        outbox = client._delivery_journal()
        assert drain(outbox, client_factory=lambda _: Down()).dead_lettered == 1
        correlation = state.rows()[0]["correlation"]
        client.resume_delivery(correlation)
        assert drain(outbox, client_factory=lambda _: Server()).delivered == 1
        state.reconcile(client)
        assert client.delivery_receipt(correlation)["source_content_hash"]
        assert state.report()["delivered"] == ["a.py"]


def test_a_file_reverted_after_its_snapshot_is_never_stamped_as_approved(tmp_path, monkeypatch):
    """Approved as A, staged as B, back to A before any later read: the stamp
    must describe the bytes the snapshot read, never A. CLIs that re-read the
    source after the stat window stamped A."""
    folder, store, client = _setup(tmp_path)
    source = folder / "a.py"
    source.write_bytes(SECRET + b'print("not approved")\n')
    real, reads = secret_gate._read_source, []

    def read(path, **kwargs):  # the snapshot, and any read of the source after it
        if Path(path) == source:
            if reads:
                source.write_bytes(SECRET)
            reads.append(path)
        return real(path, **kwargs)

    monkeypatch.setattr(secret_gate, "_read_source", read)
    server = Server()
    with client, store.writer() as state:
        enqueue(state, client, folder)
        drain(client._delivery_journal(), client_factory=lambda _: server)
        state.reconcile(client)
        assert reads and state.report()["delivered"] == [] and server.live == {}


def test_reconcile_records_an_exact_reference_receipt(tmp_path):
    _folder, store, _client = _setup(tmp_path)
    with store.writer() as state:
        intent = state.intend(state.rows()[0], reference=True, uri="file:///repo/a.py")
        exact = _receipt(intent, content_hash=intent["content_hash"], size_bytes=intent["size_bytes"])
        state.failure(intent["correlation"], MISMATCH)
        state.reconcile(SimpleNamespace(delivery_state=lambda _c: exact))
        assert state.report()["references"] == ["a.py"] and _error(state) is None


def test_reconcile_refuses_an_unstamped_receipt_the_journal_did_not_write(tmp_path):
    _folder, store, _client = _setup(tmp_path)
    with store.writer() as state:
        intent = state.intend(state.rows()[0], reference=False)
        receipt = {k: v for k, v in _receipt(intent).items() if k not in ("schema", "request_digest")}
        state.reconcile(SimpleNamespace(delivery_state=lambda _c: receipt))
        assert state.report()["unresolved"] == ["a.py"] and "does not match" in _error(state)


def test_the_record_pass_reads_a_redacted_receipt_and_samples_redacted_bytes(tmp_path):
    folder, store, client = _setup(tmp_path)
    with client, store.writer() as state:
        enqueue(state, client, folder)
        drain(client._delivery_journal(), client_factory=lambda _: Server())
        state.reconcile(client)
        row = state.rows()[0]
        assert backfill_record._receipt(state, row)["artifact_id"]
        sample, limitation = backfill_record._read_sample(folder, row)
        assert limitation is None and "GITHUB_TOKEN" in sample and TOKEN not in sample
        stored = json.loads(state.conn.execute("SELECT receipt FROM versions").fetchone()[0])
        assert stored["content_hash"] != row["approved_hash"]
        # The record pass's excerpts are the redacted bytes, and carry no hash:
        # the original's beside its redaction would let a short secret be guessed.
        items, _gaps = backfill_record.excerpts(state, folder, row["project_id"])
        assert [item["path"] for item in items] == ["a.py"]
        assert TOKEN not in json.dumps(items) and row["approved_hash"] not in json.dumps(items)


def test_a_redacted_excerpt_is_the_stored_snapshot(tmp_path):
    """The excerpt the model reads is the redaction the outbox stored, byte
    for byte: the two must use the same check."""
    folder = tmp_path / "src"
    folder.mkdir()
    (folder / "a.py").write_bytes(SECRET + b'print("hi")\n')
    snapshot = tmp_path / "snapshot"
    digest = secret_gate.safe_snapshot_file(folder / "a.py", snapshot)
    sample, limitation = backfill_record._read_sample(folder, {"path": "a.py", "approved_hash": digest})
    assert limitation is None and sample.encode() == snapshot.read_bytes() != (folder / "a.py").read_bytes()


@pytest.mark.parametrize("receipt_change,intent_change", [
    ({"source_content_hash": "e" * 64}, {}),  # stamped for other bytes
    ({"source_content_hash": None, "schema": "probe.outbox.delivery/0"}, {}),  # unstamped, not the journal's
    ({}, {"content_hash": "e" * 64}),  # the intent names another version
])
def test_the_record_pass_refuses_a_receipt_for_other_bytes(tmp_path, receipt_change, intent_change):
    folder, store, client = _setup(tmp_path)
    with client, store.writer() as state:
        enqueue(state, client, folder)
        drain(client._delivery_journal(), client_factory=lambda _: Server())
        state.reconcile(client)
        row = state.rows()[0]
        receipt, intent = map(json.loads, state.conn.execute("SELECT receipt, intent FROM versions").fetchone())
        receipt = {k: v for k, v in {**receipt, **receipt_change}.items() if v is not None}
        state.conn.execute("UPDATE versions SET receipt=?, intent=?",
                           (json.dumps(receipt), json.dumps({**intent, **intent_change})))
        with pytest.raises(ValueError, match="unverified receipt"):
            backfill_record._receipt(state, row)
