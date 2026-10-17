"""Files (artifacts) and sweep groups no longer carry notes.

Notes live on projects, experiments, runs and the team note. What a file IS,
and where it lives, goes in its run's notes; what a sweep tested goes in its
experiment's. The old doors stay callable so a training script or an agent on
an older skill does not lose its upload: `notes=` is accepted, warned about
(a UserWarning that never raises) and never sent -- including by an outbox op an older
client queued with a `notes` field in it.
"""

from __future__ import annotations

import inspect
import json
import re
import warnings
from pathlib import Path

import pytest

from probe.sdk import journal as journal_mod
from probe.sdk.client import Anchor, Client
from probe.sdk.journal import drain
from tests.conftest import make_client, open_run

AGENT = Path(__file__).resolve().parents[1]
FILE_NOTES = "say what a file is in its run's notes"


def _sent(app, start: int = 0) -> list[dict]:
    """Every JSON body the client sent, PUTs of file bytes aside."""
    out = []
    for request in app.requests[start:]:
        if request.method == "PUT" or not request.content:
            continue
        try:
            out.append(json.loads(request.content))
        except ValueError:
            continue
    return out


def test_log_artifact_notes_are_warned_about_and_never_sent(client, app, tmp_path):
    run = open_run(client, experiment="e", name="r")
    src = tmp_path / "eval.csv"
    src.write_text("a,b\n1,2\n")
    big = tmp_path / "ckpt.pt"
    with open(big, "wb") as fh:
        fh.truncate(70 * 1024 * 1024)  # refused by the gate: the pointer row
    start = len(app.requests)

    with pytest.warns(UserWarning, match=FILE_NOTES):
        run.log_artifact("eval.csv", path=str(src), notes="held-out split")  # upload
    with pytest.warns(UserWarning, match=FILE_NOTES):
        run.log_artifact("w.pt", uri="s3://bucket/w.pt", notes="from sweep 2")  # reference
    with pytest.warns(UserWarning, match=FILE_NOTES):
        run.log_artifact("ckpt", path=str(big), notes="best so far")  # refused upload

    names = {a.get("name") for a in app.artifacts.get(run.id, [])}
    assert {"eval.csv", "w.pt", "ckpt.pt"} <= names, "every file still lands"
    bodies = _sent(app, start)
    assert bodies and not [b for b in bodies if "notes" in b]
    assert not {"held-out split", "from sweep 2", "best so far"} & set(json.dumps(bodies).split('"'))


def test_log_artifact_without_notes_says_nothing(client, app, tmp_path, recwarn):
    run = open_run(client, experiment="e", name="r")
    src = tmp_path / "eval.csv"
    src.write_text("a,b\n")
    run.log_artifact("eval.csv", path=str(src))
    assert not [w for w in recwarn if issubclass(w.category, UserWarning)
                and "notes" in str(w.message)]


def test_notes_never_fail_an_upload_under_warnings_as_errors(client, app, tmp_path):
    """`-W error` / `filterwarnings("error")` (several ML harnesses set it) must
    not turn the dropped-notes notice into an exception: the upload this door
    stays open for would fail instead."""
    run = open_run(client, experiment="e", name="r")
    src = tmp_path / "eval.csv"
    src.write_text("a,b\n1,2\n")
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        run.log_artifact("eval.csv", path=str(src), notes="held-out split")
    assert "eval.csv" in {a.get("name") for a in app.artifacts.get(run.id, [])}


def test_client_upload_doors_take_notes_and_send_none(client, app, tmp_path):
    project = client.create_project("p", kind="general")
    src = tmp_path / "f.csv"
    src.write_text("x\n")
    start = len(app.requests)

    with pytest.warns(UserWarning, match=FILE_NOTES):
        client.upload_file(Anchor.PROJECT, project["id"], "f.csv", str(src), notes="desc")
    with pytest.warns(UserWarning, match=FILE_NOTES):
        client.presign_upload(
            Anchor.PROJECT, project["id"], "g.csv", digest="0" * 64, size=2, notes="desc"
        )

    assert not [b for b in _sent(app, start) if "notes" in b]


def test_an_upload_an_older_client_queued_with_notes_still_delivers_without_them(app, tmp_path):
    """The outbox outlives the CLI that wrote it: an op queued by an older
    client carries `notes` in its upload block. The drain delivers the file and
    leaves the notes behind -- no crash, no dead letter, nothing sent."""
    client = make_client(app, tmp_spool=tmp_path / "spool", async_writes=True)
    run = open_run(client, experiment="e", name="r")
    src = tmp_path / "eval.csv"
    src.write_text("a,b\n1,2\n")
    journal = client.journal
    journal.append_upload(
        anchor="run", anchor_id=run.id, name="eval.csv", src_path=str(src),
        inline_hash=True, run_ref=run.id,
    )
    [(path, op)] = [(p, o) for p, o in journal.pending() if o["kind"] == "upload"]
    assert "notes" not in op["upload"], "a new client queues none"
    op["upload"]["notes"] = "what an older CLI queued"
    path.write_text(json.dumps(op, indent=2) + "\n")
    start = len(app.requests)

    report = drain(journal, client_factory=lambda ctx: client)

    assert report.clean and journal.pending() == [] and journal.failed() == []
    assert "eval.csv" in {a.get("name") for a in app.artifacts.get(run.id, [])}
    bodies = _sent(app, start)
    assert bodies and not [b for b in bodies if "notes" in b]
    client.close()


def test_the_dead_letter_pointer_for_an_old_op_carries_no_notes():
    op = {
        "upload": {
            "anchor": "run", "anchor_id": "r-1", "name": "f.csv", "src_path": "/data/f.csv",
            "meta": {}, "notes": "what an older CLI queued",
        },
        "last_error": "boom",
    }
    path, body = journal_mod._upload_fallback_request(op)
    assert path == "/v1/runs/r-1/artifacts"
    assert "notes" not in body


def test_backfill_delivery_never_sends_a_manifest_rows_notes(tmp_path):
    """An import's manifest "notes" is the project writer's input (it reads the
    manifests), never an upload field."""
    from probe.cli import backfill_delivery

    (tmp_path / "a.csv").write_text("x\n")
    row = {
        "path": "a.csv", "present": True, "approved_hash": "h", "observed_hash": "h",
        "observation_error": None, "exclusion": None, "project_id": "p1", "size": 2,
        "manifest": json.dumps({"path": "a.csv", "notes": "the importer's line"}),
    }

    class Coverage:
        source_id = "src"

        def rows_for(self, paths):
            return {"a.csv": row}

        def delivered_paths(self, paths):
            return set()

        def intend(self, row, *, reference, uri):
            return {"correlation": "c1", "artifact_name": "a.csv", "uri": uri}

        def enqueued(self, correlation):
            pass

        def failure(self, correlation, error):
            raise AssertionError(error)

    sent: dict = {}

    class Queue:
        def delivery_state(self, correlation):
            return {"state": "unknown"}

        def enqueue_artifact_upload(self, **kwargs):
            sent.update(kwargs)
            return {"state": "queued"}

    assert backfill_delivery.enqueue(Coverage(), Queue(), tmp_path, paths=["a.csv"]) == (1, [])
    assert "notes" not in sent and sent["name"] == "a.csv"
    # A **kwargs fake proves nothing about the real door: bind what was sent.
    inspect.signature(Client.enqueue_artifact_upload).bind(None, **sent)


_COPIES = (
    AGENT / "skills",
    AGENT / "plugins" / "probe-research" / "agent-skills",
    AGENT / "plugins" / "probe-research-pi" / "skills",
    AGENT / "plugins" / "probe-research-daemon" / "inline",
)


@pytest.mark.parametrize("root", _COPIES, ids=lambda p: str(p.relative_to(AGENT)))
def test_every_skill_copy_says_files_and_groups_carry_no_notes(root):
    reference = (root / "track-work" / "reference.md").read_text(encoding="utf-8")
    edit_notes = (root / "edit-notes" / "SKILL.md").read_text(encoding="utf-8")
    # Never a description on the file itself, nor in its name (0095). Only the
    # RETIRED forms are refused: a run's `--notes` is still a legitimate flag.
    retired = re.compile(
        r"probe (?:artifact (?:add|set)|group (?:create|set))\b[^\n`]*--notes"
        r"|probe notes [a-z]+\b[^\n`]*--(?:artifact|group)\b"
    )
    assert not retired.findall(reference)
    assert "Never put a\ndescription in a name" in reference
    assert "say what a file is, and where it\nlives, in its run's notes" in reference
    assert "Projects, experiments and runs, plus ONE team note" in reference
    assert "groups, artifacts" not in reference
    assert "Notes sit on a project, experiment or run, or are the one team note." in edit_notes
    assert "group or artifact" not in edit_notes


def test_a_correlated_upload_keeps_the_digest_older_clients_recorded(tmp_path, monkeypatch):
    """Before files stopped carrying notes, every correlated upload's request was
    digested with `"notes": null` in its fields. Re-enqueueing such a
    correlation (`enqueue_artifact_upload` replays the frozen request) must still
    match that digest, so the slot stays in the DIGESTED request -- while the
    queued upload itself carries no `notes`."""
    monkeypatch.setattr(journal_mod, "MIN_FREE_BYTES", 0)
    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config.json"))
    queue = journal_mod.Journal.for_receipts(
        tmp_path / "outbox", context={"name": None, "base_url": "http://test"}
    )
    digested = []
    real = journal_mod.Journal._request_digest
    monkeypatch.setattr(
        journal_mod.Journal, "_request_digest",
        staticmethod(lambda request: digested.append(request) or real(request)),
    )
    source = tmp_path / "source.py"
    source.write_bytes(b"original")
    queue.append_upload(
        correlation="scope:file:v1", anchor="project", anchor_id="p1",
        name="src/source.py", src_path=str(source),
    )
    assert digested and all(r["fields"].get("notes", "absent") is None for r in digested)
    ops = [json.loads(p.read_text()) for p in sorted(queue.ops_dir.glob("*.json"))]
    assert ops and all("notes" not in op.get("upload", {}) for op in ops)
