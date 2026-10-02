"""A refused CLI write fails; one Probe could not answer is queued and says so.

Lineage plan L14 (with L4's `edge add` specifics and L5's read verbs). Before
it, the CLI's client was fail-open for every write: any server answer was
queued, `null` printed, exit 0 -- a 404, a 422 or a duplicate read as success,
and the Probe daemon's logbook filed it as recorded. These drive the real CLI
(`probe.cli.main`) against the fake backend, with chosen answers on chosen
routes, and read the exit code, both output streams and the outbox.
"""

from __future__ import annotations

import errno
import importlib
import json
import re

import httpx
import pytest

from probe import cli
from probe.sdk.client import Client
from probe.sdk.config import Settings
from probe.sdk.journal import Journal
from probe.sdk.transport import Transport
from probe.sdk.write_outcome import NOT_QUEUED_PREFIX, QUEUED_PREFIX
from tests.conftest import FakeApp

cli_main = importlib.import_module("probe.cli.main")

RUN_A = "11111111-1111-4111-8111-111111111111"
RUN_B = "22222222-2222-4222-8222-222222222222"
EXISTING = "33333333-3333-4333-8333-333333333333"
VERSION = "44444444-4444-4444-8444-444444444444"


class Wired:
    """The fake backend, with `answers` taking precedence: (METHOD, path regex)
    -> (status, body), or an exception the transport raises (no answer)."""

    def __init__(self, tmp_path) -> None:
        self.app = FakeApp()
        self.answers: dict[tuple[str, str], object] = {}
        self.seen: list[tuple[str, str, object]] = []
        self.spool = tmp_path / "spool"

    def handler(self, request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content) if request.content else None
        self.seen.append((request.method, request.url.path, body))
        for (method, pattern), answer in self.answers.items():
            if method == request.method and re.fullmatch(pattern, request.url.path):
                if isinstance(answer, BaseException):
                    raise answer
                status, payload = answer
                return httpx.Response(status, json=payload)
        return self.app.handler(request)

    def client(self, **_kw) -> Client:
        settings = Settings(base_url="http://test", token="ros_pat_deadbeef", ingest_token="ros_ing_cafef00d",
                            hmac_secret="s3cr3t")
        # max_retries=0: a connect failure is answered at once, not after the
        # transport's own backoff (what is under test is what happens after).
        transport = Transport(settings, client=httpx.Client(base_url="http://test",
                                                            transport=httpx.MockTransport(self.handler)),
                              max_retries=0)
        journal = Journal(self.spool, context={"name": None, "base_url": settings.base_url})
        return Client(settings=settings, transport=transport, journal=journal, async_writes=False)

    def queued(self) -> list[dict]:
        return [op for _path, op in Journal(self.spool, context={"name": None, "base_url": "http://test"}).pending()]

    def sent(self, method: str, pattern: str) -> list[object]:
        return [body for m, p, body in self.seen if m == method and re.fullmatch(pattern, p)]


@pytest.fixture
def wired(tmp_path, monkeypatch) -> Wired:
    w = Wired(tmp_path)
    monkeypatch.setattr(cli, "Client", w.client)
    monkeypatch.delenv("PROBE_DAEMON_SESSION", raising=False)
    return w


def _edge(*extra: str) -> list[str]:
    return ["edge", "add", "--source", f"run:{RUN_B}", "--relation", "derived_from", "--target", f"run:{RUN_A}",
            *extra]


# ---------------------------------------------------------------------------
# A refusal fails, for `edge add` and for any other verb.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("status, detail", [
    (404, "target endpoint not found"),
    (422, "relation 'supersedes' is not accepted by this research-os backend"),
])
def test_a_refused_edge_exits_1_with_the_servers_reason_and_queues_nothing(wired, capsys, status, detail):
    wired.answers[("POST", "/v1/edges")] = (status, {"detail": detail})
    assert cli.main(_edge()) == 1
    out = capsys.readouterr()
    assert detail in out.err and out.err.startswith("error: ")
    assert out.out == "" and "null" not in out.out
    assert wired.queued() == []


def test_a_second_genealogy_parent_is_a_refusal_not_already_linked(wired, capsys):
    """This 409 carries `existing_id` too (the OTHER parent's edge): queued, the
    outbox read it as its own delivery landing, and nothing said the link was
    never made."""
    wired.answers[("POST", "/v1/edges")] = (409, {"detail": {
        "message": "this run already has a genealogy parent — a run descends from at most one predecessor",
        "existing_id": EXISTING}})
    assert cli.main(_edge()) == 1
    out = capsys.readouterr()
    assert "already has a genealogy parent" in out.err and "already_linked" not in out.out
    assert wired.queued() == []


def test_an_edge_that_already_exists_prints_its_id_and_exits_0(wired, capsys, monkeypatch):
    wired.answers[("POST", "/v1/edges")] = (409, {"detail": {"message": "lineage edge already exists",
                                                             "existing_id": EXISTING}})
    assert cli.main(_edge()) == 0
    out = capsys.readouterr()
    assert json.loads(out.out) == {"already_linked": True, "id": EXISTING} and out.err == ""
    assert wired.queued() == []
    # What the call carried beyond the edge is not applied to the edge that was there.
    monkeypatch.setenv("PROBE_DAEMON_SESSION", "daemon-session-1")
    assert cli.main(_edge("--reason", "B reads A's checkpoint", "--evidence", "main:4:0")) == 0
    out = capsys.readouterr()
    assert json.loads(out.out) == {"already_linked": True, "id": EXISTING, "applied": False}
    assert "--reason, --evidence were not applied" in out.err


def test_only_the_exact_edge_409_counts_as_already_linked(wired, capsys):
    """The outbox's rule (`journal.edge_already_exists`: the message STARTS so),
    not a substring anywhere in whatever the server said."""
    from probe.sdk.journal import edge_already_exists
    from probe.sdk.errors import ConflictError

    near = "this run already has a genealogy parent; lineage edge already exists elsewhere"
    wired.answers[("POST", "/v1/edges")] = (409, {"detail": {"message": near, "existing_id": EXISTING}})
    assert cli.main(_edge()) == 1
    assert "already_linked" not in capsys.readouterr().out
    assert edge_already_exists(ConflictError("x", detail={"message": "lineage edge already exists"}))
    assert not edge_already_exists(ConflictError("x", detail={"message": near}))


def test_a_refusal_fails_any_write_verb_not_only_edges(wired, capsys):
    wired.answers[("DELETE", "/v1/edges/.+")] = (404, {"detail": "edge not found"})
    assert cli.main(["edge", "remove", EXISTING]) == 1
    assert "edge not found" in capsys.readouterr().err
    assert wired.queued() == []


# ---------------------------------------------------------------------------
# A failure that could still succeed later is queued, and the CLI says so.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("answer", [httpx.ConnectError("connection refused"), (503, {"detail": "db down"})],
                         ids=["no-answer", "5xx"])
def test_a_write_probe_did_not_answer_is_queued_printed_as_queued_and_exits_0(wired, capsys, answer):
    wired.answers[("POST", "/v1/edges")] = answer
    assert cli.main(_edge("--reason", "B reads A's checkpoint")) == 0
    out = capsys.readouterr()
    queued_lines = [line for line in out.err.splitlines() if line.startswith(QUEUED_PREFIX)]
    assert len(queued_lines) == 1 and "POST /v1/edges" in queued_lines[0], out.err
    printed = json.loads(out.out)  # still ONE JSON value for a script, never `null`
    assert printed["queued"] is True and printed["count"] == 1 and printed["writes"][0]["path"] == "/v1/edges"
    ops = wired.queued()
    assert len(ops) == 1 and ops[0]["path"] == "/v1/edges"


def test_a_write_the_outbox_could_not_keep_fails(wired, capsys, monkeypatch):
    wired.answers[("POST", "/v1/edges")] = httpx.ConnectError("connection refused")

    def full(*_a, **_k):
        raise OSError(errno.ENOSPC, "No space left on device")

    monkeypatch.setattr(Journal, "append_http", full)
    assert cli.main(_edge()) == 1
    out = capsys.readouterr()
    assert any(line.startswith(NOT_QUEUED_PREFIX) for line in out.err.splitlines()), out.err
    assert json.loads(out.out)["queued"] is False


def test_a_sync_log_that_was_queued_does_not_say_delivered(wired, capsys):
    assert cli.main(["project", "create", "--kind", "general", "p"]) == 0
    assert cli.main(["experiment", "create", "e", "--question", "q", "--project", "p"]) == 0
    capsys.readouterr()
    assert cli.main(["run", "start", "--experiment", "e", "--name", "r1"]) == 0
    run = capsys.readouterr().out.strip().splitlines()[-1]
    wired.answers[("POST", r"/v1/runs/[^/]+/metrics")] = (503, {"detail": "busy"})
    assert cli.main(["--sync", "log", run, "loss=0.5", "--step", "1"]) == 0
    out = capsys.readouterr()
    assert out.out.strip().endswith("(queued)"), out.out
    assert QUEUED_PREFIX in out.err
    del wired.answers[("POST", r"/v1/runs/[^/]+/metrics")]
    assert cli.main(["--sync", "log", run, "loss=0.4", "--step", "2"]) == 0
    assert capsys.readouterr().out.strip().endswith("(delivered)")


def test_the_sdk_default_is_still_fail_open_and_records_nothing(tmp_path):
    """Only the CLI raises refusals: a training loop must never see one, and
    without the CLI's hook nothing is kept per failed write (a long loop's
    record would grow without end)."""
    w = Wired(tmp_path)
    w.answers[("POST", "/v1/edges")] = (404, {"detail": "target endpoint not found"})
    client = w.client()
    assert client.raise_permanent is False and client.on_undelivered is None
    assert client.add_edge(source_type="run", source_id=RUN_B, relation="derived_from", target_type="run",
                           target_id=RUN_A) is None
    assert list(client.undelivered_writes) == [] and client.undelivered_count == 0
    assert len(w.queued()) == 1


def test_a_hooked_clients_record_is_bounded(tmp_path):
    w = Wired(tmp_path)
    w.answers[("POST", "/v1/edges")] = (503, {"detail": "down"})
    client = w.client()
    seen: list[dict] = []
    client.on_undelivered = seen.append
    for _ in range(client.UNDELIVERED_KEPT + 8):
        client.add_edge(source_type="run", source_id=RUN_B, relation="derived_from", target_type="run",
                        target_id=RUN_A)
    assert len(seen) == client.undelivered_count == client.UNDELIVERED_KEPT + 8
    assert len(client.undelivered_writes) == client.UNDELIVERED_KEPT


def test_many_undelivered_writes_print_a_few_lines_not_one_each(capsys, monkeypatch):
    """The first of each kind at once, then at most one per REPEAT_SECONDS with the
    running count (the SDK delivery notices' rule), and the result keeps the last few."""
    clock = [1000.0]
    monkeypatch.setattr(cli_main.time, "monotonic", lambda: clock[0])
    cli_main._UNDELIVERED.reset()
    entry = {"method": "POST", "path": "/v1/runs/r/metrics", "error": "ServerError: busy", "queued": True}
    for _ in range(100):
        cli_main._report_undelivered(entry)
    clock[0] += cli_main._Undelivered.REPEAT_SECONDS
    cli_main._report_undelivered(entry)
    cli_main._report_undelivered(dict(entry, queued=False))
    lines = capsys.readouterr().err.splitlines()
    assert len(lines) == 3, lines
    assert lines[0].startswith(QUEUED_PREFIX) and lines[1].endswith("(101 writes so far)")
    assert lines[2].startswith(NOT_QUEUED_PREFIX)
    result = cli_main._UNDELIVERED.result()
    assert result["count"] == 102 and result["queued"] is False
    assert len(result["writes"]) == cli_main._Undelivered.KEPT
    cli_main._UNDELIVERED.reset()


def test_probe_exec_reports_nothing_per_write(monkeypatch):
    """`probe exec` carries a job's run through the SDK: no hook, so neither a
    stderr line per failed write nor an exit code it would change."""
    made: list = []

    class Stub:
        def __init__(self, **_kw):
            self.on_undelivered = None
            made.append(self)

    monkeypatch.setattr(cli_main, "Client", Stub)
    cli_main._client(raise_permanent=False)
    cli_main._client()
    assert made[0].on_undelivered is None and made[0].raise_permanent is False
    assert made[1].on_undelivered is cli_main._report_undelivered and made[1].raise_permanent is True


# ---------------------------------------------------------------------------
# L4: --evidence, stored with the session it came from.
# ---------------------------------------------------------------------------


def test_evidence_is_stored_as_session_and_event_pairs(wired, capsys, monkeypatch):
    monkeypatch.setenv("PROBE_DAEMON_SESSION", "daemon-session-1")
    assert cli.main(_edge("--evidence", "main:1200:0", "--evidence", "agent-7:88:2")) == 0
    [body] = wired.sent("POST", "/v1/edges")
    assert body["meta"] == {"evidence": [{"session": "daemon-session-1", "event": "main:1200:0"},
                                         {"session": "daemon-session-1", "event": "agent-7:88:2"}]}
    assert "via" not in body["meta"] and "by" not in body["meta"]  # the server stamps those (L1)
    capsys.readouterr()


def test_evidence_takes_the_agent_session_outside_the_daemon(wired, capsys, monkeypatch):
    monkeypatch.setattr(cli_main.agent_session, "session_id_from_env", lambda *a, **k: "agent-session-9")
    assert cli.main(_edge("--evidence", "main:5:1")) == 0
    [body] = wired.sent("POST", "/v1/edges")
    assert body["meta"]["evidence"] == [{"session": "agent-session-9", "event": "main:5:1"}]
    capsys.readouterr()


def test_evidence_with_no_session_to_open_it_in_is_a_usage_error(wired, capsys, monkeypatch):
    """An event id alone names nothing the audit can open (R7)."""
    monkeypatch.setattr(cli_main.agent_session, "session_id_from_env", lambda *a, **k: None)
    assert cli.main(_edge("--evidence", "main:6:0")) == 2
    err = capsys.readouterr().err
    assert "--evidence" in err and "PROBE_DAEMON_SESSION" in err
    assert wired.sent("POST", "/v1/edges") == []


def test_evidence_that_is_not_an_event_id_is_a_usage_error(wired, capsys, monkeypatch):
    monkeypatch.setenv("PROBE_DAEMON_SESSION", "daemon-session-1")
    assert cli.main(_edge("--evidence", "the run config")) == 2
    assert "--evidence" in capsys.readouterr().err
    assert wired.sent("POST", "/v1/edges") == []


def test_no_evidence_sends_no_meta_of_its_own(wired, capsys):
    assert cli.main(_edge()) == 0
    [body] = wired.sent("POST", "/v1/edges")
    assert not body.get("meta")
    capsys.readouterr()


# ---------------------------------------------------------------------------
# L12: experiments and projects as ends, named the way `run move --to` takes them.
# ---------------------------------------------------------------------------


def _line_of_work(wired: Wired) -> tuple[dict, dict]:
    """A project and an experiment under it, seeded through the SDK."""
    c = wired.client()
    parent = c.create_project("tokenizer-work", kind="training")
    child = c.create_experiment("bpe-ablation", question="Does BPE help?", project_id=parent["id"])
    return parent, child


@pytest.mark.parametrize("source, target, want", [
    # slug -> slug: an experiment building on its project's earlier line of work
    ("experiment:bpe-ablation", "project:tokenizer-work", ("child", "parent")),
    # `id:` works on either word; an experiment's id under `project:` too (one row)
    ("project:id:{child}", "experiment:id:{child}", ("child", "child")),
    # across levels: a run built on an experiment's conclusion
    (f"run:{RUN_B}", "experiment:bpe-ablation", (RUN_B, "child")),
])
def test_experiment_and_project_ends_are_resolved_and_sent_as_project(wired, capsys, source, target, want):
    parent, child = _line_of_work(wired)
    ids = {"parent": parent["id"], "child": child["id"]}
    argv = ["edge", "add", "--source", source.format(**ids), "--relation", "derived_from",
            "--target", target.format(**ids), "--reason", "the session says it builds on it"]
    assert cli.main(argv) == 0, capsys.readouterr().err
    [body] = wired.sent("POST", "/v1/edges")
    expected = [(("run", RUN_B) if end == RUN_B else ("project", ids[end])) for end in want]
    assert [(body["source_type"], body["source_id"]), (body["target_type"], body["target_id"])] == expected
    capsys.readouterr()


@pytest.mark.parametrize("ref, says", [
    ("project:{parent}", "id:"),  # a bare ref is a slug: a UUID gets the exact edit
    ("experiment:no-such-experiment", "no experiment with slug"),
])
def test_an_unresolvable_experiment_or_project_end_is_a_usage_error(wired, capsys, ref, says):
    parent, _ = _line_of_work(wired)
    argv = ["edge", "add", "--source", f"run:{RUN_B}", "--relation", "derived_from",
            "--target", ref.format(parent=parent["id"])]
    assert cli.main(argv) == 2
    assert says in capsys.readouterr().err
    assert wired.sent("POST", "/v1/edges") == []


def test_an_end_with_no_ref_names_the_type_ref_shape(wired, capsys):
    assert cli.main(["edge", "add", "--source", "experiment", "--relation", "derived_from",
                     "--target", f"run:{RUN_A}"]) == 2
    assert "type:ref" in capsys.readouterr().err
    assert wired.sent("POST", "/v1/edges") == []


def test_edge_add_help_names_every_end_type_and_relation():
    import typer

    add = typer.main.get_command(cli_main.app).commands["edge"].commands["add"]
    helps = {p.name: p.help or "" for p in add.params}
    ends = ["run", "artifact", "artifact_version", "paper", "experiment", "project"]
    assert helps["source"] == helps["target"] == "type: " + " | ".join(ends)
    relations = set(helps["relation"].split(" | "))
    assert {"derived_from", "evaluates_on", "retried_from", "branched_from", "supersedes",
            "informed_by", "discovered_via"} <= relations
    assert "experiment" in add.help and "slug" in add.help


# ---------------------------------------------------------------------------
# L5: the read facts, and their correction.
# ---------------------------------------------------------------------------


def test_run_inputs_and_upstream_print_the_servers_facts(wired, capsys):
    wired.answers[("GET", f"/v1/runs/{RUN_A}")] = (200, {"id": RUN_A, "slug": "a"})
    facts = {"run_id": RUN_A, "coverage": {"recorder": "sdk", "truncated": False}, "inputs": [
        {"path": "data/train.csv", "stable": True, "first_seen_at": "2026-09-27T00:00:00Z",
         "match_dismissed": False, "match_version_id": None,
         "matches": [{"target_type": "artifact_version", "target_id": VERSION, "writer_run_id": RUN_B}]}]}
    wired.answers[("GET", f"/v1/runs/{RUN_A}/inputs")] = (200, facts)
    assert cli.main(["run", "inputs", RUN_A]) == 0
    assert json.loads(capsys.readouterr().out) == facts
    walk = {"run_id": RUN_A, "depth": 3, "runs": [{"id": RUN_A, "depth": 0}], "edges": [], "truncated": False}
    wired.answers[("GET", f"/v1/runs/{RUN_A}/upstream")] = (200, walk)
    assert cli.main(["run", "upstream", RUN_A, "--depth", "3"]) == 0
    assert json.loads(capsys.readouterr().out) == walk
    assert [p for m, p, _ in wired.seen if p.endswith("/upstream")] == [f"/v1/runs/{RUN_A}/upstream"]
    assert cli.main(["run", "upstream", RUN_A, "--depth", "9"]) == 2  # the server's cap, said locally


@pytest.mark.parametrize("argv, sent", [
    (["dismiss", RUN_A, "data/train.csv"], {"path": "data/train.csv", "dismissed": True}),
    (["pin", RUN_A, "data/train.csv", "--version", VERSION], {"path": "data/train.csv", "version_id": VERSION}),
    (["pin", RUN_A, "data/train.csv", "--writer", RUN_B, "--hash", "a" * 64],
     {"path": "data/train.csv", "writer_run_id": RUN_B, "content_hash": "a" * 64}),
    (["reset", RUN_A, "data/train.csv", "--hash", "sha256:" + "a" * 64],
     {"path": "data/train.csv", "dismissed": False, "content_hash": "sha256:" + "a" * 64}),
])
def test_a_read_is_corrected_with_one_patch(wired, capsys, argv, sent):
    wired.answers[("GET", f"/v1/runs/{RUN_A}")] = (200, {"id": RUN_A, "slug": "a"})
    wired.answers[("GET", f"/v1/runs/{RUN_B}")] = (200, {"id": RUN_B, "slug": "b"})
    wired.answers[("PATCH", f"/v1/runs/{RUN_A}/inputs")] = (204, None)
    assert cli.main(["run", "input", *argv]) == 0
    assert wired.sent("PATCH", f"/v1/runs/{RUN_A}/inputs") == [sent]
    printed = json.loads(capsys.readouterr().out)
    assert printed["run_id"] == RUN_A and printed["path"] == "data/train.csv"


def test_a_pin_names_a_writer_by_slug(wired, capsys):
    """`--writer` takes any run ref; the server pins the id it resolves to."""
    wired.answers[("GET", f"/v1/runs/{RUN_A}")] = (200, {"id": RUN_A, "slug": "a"})
    wired.answers[("GET", "/v1/runs/tokenizer-run")] = (200, {"id": RUN_B, "slug": "tokenizer-run"})
    wired.answers[("PATCH", f"/v1/runs/{RUN_A}/inputs")] = (204, None)
    assert cli.main(["run", "input", "pin", RUN_A, "vocab.json", "--writer", "tokenizer-run"]) == 0
    assert wired.sent("PATCH", f"/v1/runs/{RUN_A}/inputs") == [{"path": "vocab.json", "writer_run_id": RUN_B}]
    assert json.loads(capsys.readouterr().out)["writer_run_id"] == RUN_B


@pytest.mark.parametrize("flags", [[], ["--version", VERSION, "--writer", RUN_B]])
def test_a_pin_names_exactly_one_thing(wired, capsys, flags):
    assert cli.main(["run", "input", "pin", RUN_A, "data/train.csv", *flags]) == 2
    assert "--version or --writer" in capsys.readouterr().err
    assert not [s for s in wired.seen if s[0] == "PATCH"]


@pytest.mark.parametrize(("status", "detail"), [
    (422, "writer_run_id not found"), (410, "run is in the trash"), (404, "no read at that path"),
])
def test_a_refused_writer_pin_exits_non_zero(wired, capsys, status, detail):
    wired.answers[("GET", f"/v1/runs/{RUN_A}")] = (200, {"id": RUN_A, "slug": "a"})
    wired.answers[("GET", f"/v1/runs/{RUN_B}")] = (200, {"id": RUN_B, "slug": "b"})
    wired.answers[("PATCH", "/v1/runs/[^/]+/inputs")] = (status, {"detail": detail})
    assert cli.main(["run", "input", "pin", RUN_A, "data/train.csv", "--writer", RUN_B]) == 1
    assert detail in capsys.readouterr().err
    assert wired.queued() == []


def test_a_refused_correction_fails(wired, capsys):
    wired.answers[("GET", f"/v1/runs/{RUN_A}")] = (200, {"id": RUN_A, "slug": "a"})
    wired.answers[("PATCH", "/v1/runs/[^/]+/inputs")] = (422, {"detail": "send dismissed or version_id"})
    assert cli.main(["run", "input", "dismiss", RUN_A, "data/train.csv"]) == 1
    assert "send dismissed or version_id" in capsys.readouterr().err
    assert wired.queued() == []


def test_a_correction_that_was_not_delivered_prints_what_happened_to_it(wired, capsys, monkeypatch):
    """Queued: exit 0 and the queued object. Lost with the outbox: exit 1 and the
    same object -- never the correction as if it were made."""
    wired.answers[("GET", f"/v1/runs/{RUN_A}")] = (200, {"id": RUN_A, "slug": "a"})
    wired.answers[("PATCH", f"/v1/runs/{RUN_A}/inputs")] = httpx.ConnectError("connection refused")
    assert cli.main(["run", "input", "dismiss", RUN_A, "data/train.csv"]) == 0
    printed = json.loads(capsys.readouterr().out)
    assert printed["queued"] is True and "run_id" not in printed

    def full(*_a, **_k):
        raise OSError(errno.ENOSPC, "No space left on device")

    monkeypatch.setattr(Journal, "append_http", full)
    assert cli.main(["run", "input", "dismiss", RUN_A, "data/train.csv"]) == 1
    printed = json.loads(capsys.readouterr().out)
    assert printed["queued"] is False and "run_id" not in printed
