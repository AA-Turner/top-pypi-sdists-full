"""A writer run that creates a project or experiment, or sets an experiment's
conclusion, owes that entity's summary (writer-owns-summary plan 3.5, bench
2026-10-16: one daemon-trial-2 replay set two conclusions and pushed no summary).
The CLI keeps what is owed (`probe.cli.owed`, notes parity N3), and the writer's
output validator sends the run back ONCE for what it did not push
(`agent.SUMMARY_OWED`); a team whose summaries are still the lane's owes
nothing.

Every command runs the REAL `probe` CLI in this process, as the daemon runs it
(`PROBE_DAEMON_SESSION`), against the repo's FakeApp with CONTRACT.md's summary
and visuals routes (`test_cli_summary.SummaryServer`): what it prints and what
it keeps in the ledger are the CLI's own.
"""

from __future__ import annotations

import asyncio
import io
import json
import os
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

import pytest

from probe import cli
from probe.daemon import tools
from tests.conftest import make_client, open_run
from tests.test_cli_summary import SummaryServer

from test_daemon_same_response_end import SID, _deps, _retries, _state  # noqa: F401 -- fixture

CONCLUDE = "probe experiment set wider --conclusion 'keep 64 units'"
CHECKOUT = "probe summary checkout --experiment wider --project p"
PUSH = "probe summary push --experiment wider --project p"


@pytest.fixture
def server(app, tmp_path, monkeypatch):
    """Project `p`, experiment `wider` and a run, made outside any session."""
    for name in ("PROBE_DAEMON_SESSION", "CLAUDE_CODE_SESSION_ID", "CODEX_THREAD_ID", "PI_SESSION_ID"):
        monkeypatch.delenv(name, raising=False)
    fake = SummaryServer(app)
    monkeypatch.setattr(cli, "Client", lambda **_kw: make_client(app, tmp_spool=tmp_path / "spool"))
    with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
        assert cli.main(["project", "create", "--kind", "general", "p"]) == 0
        assert cli.main(["experiment", "create", "wider", "--question", "does it help?", "--project", "p"]) == 0
    fake.run = open_run(make_client(app, tmp_spool=tmp_path / "s"), experiment="wider", name="r1")
    return fake


class RealCli:
    """`tools.run_probe_process` running the real CLI with what the daemon gives
    it. `edit`: after a `summary checkout`, the writer's edit of the draft it
    named (default: a line appended; None: no edit)."""

    def __init__(self, edit=lambda text: text + "\nThe answer: keep 64 units.\n") -> None:
        self.edit = edit
        self.ran: list[list[str]] = []
        self.after: dict[str, object] = {}

    async def __call__(self, deps, argv, op_id, **kw):
        self.ran.append(list(argv))
        out, err = io.StringIO(), io.StringIO()
        with mock.patch.dict(os.environ, {"PROBE_DAEMON_SESSION": deps.session_id}), \
                redirect_stdout(out), redirect_stderr(err):
            code = cli.main(list(argv))
        head = " ".join(argv[:2])
        if head == "summary checkout" and code == 0 and self.edit is not None:
            draft = Path(json.loads(out.getvalue())["path"])
            draft.write_text(self.edit(draft.read_text()))
        if callable(self.after.get(head)):
            self.after[head](out.getvalue())
        return tools.ProbeResult(code, out.getvalue(), err.getvalue())


@pytest.fixture
def real_cli(server, monkeypatch):
    probe = RealCli()
    monkeypatch.setattr(tools, "run_probe_process", probe)
    return probe


@pytest.fixture
def team_mode(monkeypatch):
    """What `probe_api.summaries_mode` answers (default: a recorder team), and
    how many times it was asked."""
    from probe.daemon import probe_api

    state = {"mode": "recorder", "asked": 0}

    async def answer(env, kind, ref):
        state["asked"] += 1
        return state["mode"]

    monkeypatch.setattr(probe_api, "summaries_mode", answer)
    return state


def _ran(tmp_path, *commands: str) -> tools.Deps:
    deps = _deps(tmp_path)
    for command in commands:
        asyncio.run(tools.shell(deps, command))
    return deps


@pytest.mark.parametrize("commands, owed", [
    (["probe experiment create wider2 --project p --question 'does it help?'"], ["experiment wider2"]),
    (["probe project create digits --kind general --name Digits"], ["project digits"]),
    ([CONCLUDE], ["experiment wider"]),
    ([CONCLUDE, CHECKOUT, PUSH], []),
    (["probe experiment set wider --name 'Wider layer'"], []),   # no conclusion: nothing owed
    (["probe run tag {run} done"], []),
], ids=["experiment-create", "project-create", "conclusion", "conclusion-then-push", "rename", "other-write"])
def test_what_a_run_owes(tmp_path, server, real_cli, commands, owed):
    deps = _ran(tmp_path, *(c.format(run=server.run.id) for c in commands))
    assert tools.summaries_owed(deps) == owed


def test_a_lane_team_owes_nothing(tmp_path, server, real_cli):
    server.mode = "lane"
    deps = _ran(tmp_path, CONCLUDE, CHECKOUT)
    assert deps.summaries_off and tools.summaries_owed(deps) == []


def _scripted(*responses):
    from pydantic_ai.models.function import FunctionModel

    seen: list = []

    def model(messages, info):
        seen.append(messages)
        return responses[min(len(seen), len(responses)) - 1]

    return FunctionModel(model), seen


def _shell(*commands: str):
    from pydantic_ai.messages import ModelResponse, ToolCallPart

    return ModelResponse(parts=[ToolCallPart("shell", {"command": c}) for c in commands])


def _end(summary: str):
    from pydantic_ai.messages import ModelResponse, ToolCallPart

    return ModelResponse(parts=[ToolCallPart("final_result", {"summary": summary})])


def test_the_writer_is_sent_back_once_for_an_owed_summary(tmp_path, real_cli, team_mode):
    pytest.importorskip("pydantic_ai")  # the `daemon` extra
    from probe.daemon import agent as agent_mod

    model, _ = _scripted(_shell(CONCLUDE), _end("concluded wider"), _end("the summary waits for the seeds"))
    result = asyncio.run(agent_mod.build_agent("instructions", model=model).run("record the session",
                                                                                 deps=_deps(tmp_path)))
    retries = _retries(result.all_messages())
    assert retries == [agent_mod.SUMMARY_OWED.format(entities="experiment wider")]
    assert retries[0].startswith("Not ended: these summaries were not updated in this run: experiment wider.")
    assert result.output.summary == "the summary waits for the seeds", "the second end stands"


def test_a_run_that_pushed_its_summary_ends_at_once(tmp_path, server, real_cli, team_mode):
    pytest.importorskip("pydantic_ai")  # the `daemon` extra
    from probe.daemon import agent as agent_mod

    server.eligible = False  # no tables or charts to owe
    model, seen = _scripted(_shell(CONCLUDE, CHECKOUT, PUSH), _end("concluded and summarised wider"))
    result = asyncio.run(agent_mod.build_agent("instructions", model=model).run("record the session",
                                                                                 deps=_deps(tmp_path)))
    assert _retries(result.all_messages()) == [] and len(seen) == 2


def test_a_concluded_eligible_experiment_owes_its_tables(tmp_path, real_cli):
    deps = _ran(tmp_path, CONCLUDE, CHECKOUT, PUSH)
    assert tools.summaries_owed(deps) == [] and tools.visuals_owed(deps) == ["experiment wider"]


def test_tables_set_this_run_are_not_owed(tmp_path, real_cli):
    drafts: dict[str, str] = {}

    def keep(stdout: str) -> None:
        drafts["path"] = json.loads(stdout)["path"]
        Path(drafts["path"]).write_text(json.dumps([{"kind": "table", "title": "Accuracy by width"}]))

    real_cli.after["visuals options"] = keep
    deps = _ran(tmp_path, CONCLUDE, CHECKOUT, "probe visuals options --experiment wider --project p")
    asyncio.run(tools.shell(deps, f"probe visuals set --experiment wider --project p --file {drafts['path']}"))
    assert real_cli.ran[-1][:2] == ["visuals", "set"]
    assert tools.visuals_owed(deps) == []


def test_a_new_experiment_without_a_conclusion_owes_no_tables(tmp_path, real_cli):
    deps = _ran(tmp_path, "probe experiment create wider2 --project p --question 'does it help?'",
                "probe summary checkout --experiment wider2 --project p")
    assert tools.visuals_owed(deps) == []


def test_the_writer_is_sent_back_once_more_for_owed_tables(tmp_path, real_cli, team_mode):
    pytest.importorskip("pydantic_ai")  # the `daemon` extra
    from probe.daemon import agent as agent_mod

    model, _ = _scripted(_shell(CONCLUDE, CHECKOUT, PUSH), _end("concluded wider"),
                         _end("tables wait for the last seed"))
    result = asyncio.run(agent_mod.build_agent("instructions", model=model).run("record the session",
                                                                                 deps=_deps(tmp_path)))
    retries = _retries(result.all_messages())
    assert len(retries) == 1 and retries[0].startswith("Not ended: these experiments have no tables or charts set: "
                                                       "experiment wider.")
    assert result.output.summary == "tables wait for the last seed"


def test_both_send_backs_leave_the_writer_its_own_output_retries(tmp_path, real_cli, team_mode):
    """The two send-backs spend pydantic-ai's OUTPUT retry budget, which a run
    never refills: with only the 2 every other tool gets, one malformed end after
    them failed the whole run ("Exceeded maximum output retries")."""
    pytest.importorskip("pydantic_ai")  # the `daemon` extra
    from pydantic_ai.messages import ModelResponse, ToolCallPart

    from probe.daemon import agent as agent_mod

    malformed = ModelResponse(parts=[ToolCallPart("final_result", {"reply": "no summary field"})])
    end = _end("concluded wider")
    model, _ = _scripted(_shell(CONCLUDE, CHECKOUT), end, malformed, end, end)
    result = asyncio.run(agent_mod.build_agent("instructions", model=model).run("record the session",
                                                                                 deps=_deps(tmp_path)))
    retries = _retries(result.all_messages())
    assert len(retries) == 3, retries
    assert retries[0].startswith("Not ended: these summaries") and retries[2].startswith("Not ended: these experiments")
    assert result.output.summary == "concluded wider"


BASE = "# Wider\n\nThe question: does a wider layer help?\n\nNothing run yet.\n"


def _page(tmp_path, deps, server, real_cli, text: str) -> None:
    """Give the experiment's page `text` (a first checkout makes its anchor)."""
    edit, real_cli.edit = real_cli.edit, None
    asyncio.run(tools.shell(deps, CHECKOUT))
    real_cli.edit = edit
    server.write(server.anchor_of(""), text)


def _another_writer(server, change):
    """After our checkout, someone else pushes `change(page)` first."""
    def push(stdout: str) -> None:
        anchor = server.anchor_of("")
        server.write(anchor, change(server.page(anchor)["markdown"]))

    return push


@pytest.mark.parametrize("case", ["merged-only", "no-edits", "conflict", "refused"])
def test_only_a_push_that_landed_settles_the_summary(tmp_path, server, real_cli, case):
    """Both reviews: a merge that asks for another push, a conflict or a refusal
    published nothing, so the summary stays owed."""
    deps = _ran(tmp_path, CONCLUDE)
    _page(tmp_path, deps, server, real_cli, BASE)
    if case == "merged-only":
        real_cli.after["summary checkout"] = _another_writer(server, lambda page: page.replace("# Wider", "# Wide"))
    elif case == "no-edits":
        real_cli.edit = None
    elif case == "conflict":
        real_cli.edit = lambda text: text.replace("Nothing run yet.", "Seed 1 ran.")
        real_cli.after["summary checkout"] = _another_writer(server, lambda page: page.replace("Nothing run yet.",
                                                                                               "Seed 2 ran."))
    else:
        real_cli.edit = lambda text: text + "x" * 12_001  # past what the server keeps: 422
    asyncio.run(tools.shell(deps, CHECKOUT))
    out = asyncio.run(tools.shell(deps, PUSH))
    said = {"merged-only": '"merged":true', "no-edits": "nolocaledits", "conflict": '"conflicted":true',
            "refused": "12,000"}[case]
    assert '"pushed":false' in out.replace(" ", "") and said in out.replace(" ", ""), out
    assert tools.summaries_owed(deps) == ["experiment wider"]


def test_a_conclusion_after_the_push_owes_it_again(tmp_path, real_cli):
    deps = _ran(tmp_path, CHECKOUT, PUSH, CONCLUDE)
    assert tools.summaries_owed(deps) == ["experiment wider"]


def test_only_a_summary_command_can_say_lane(tmp_path, server, real_cli):
    """Prose the model or a person wrote can hold the lane's words: a project's
    description, a page read by a checkout in recorder mode."""
    lane_words = "this team: summary_writer_off (mode lane)"
    deps = _ran(tmp_path, f"probe experiment set wider --description '{lane_words}'", CONCLUDE)
    _page(tmp_path, deps, server, real_cli, lane_words + "\n")
    asyncio.run(tools.shell(deps, CHECKOUT))
    assert not deps.summaries_off and tools.summaries_owed(deps) == ["experiment wider"]
    server.mode = "lane"  # the push meets the closed door
    asyncio.run(tools.shell(deps, PUSH))
    assert deps.summaries_off and tools.summaries_owed(deps) == []


def _next_bite(deps: tools.Deps, bite_id: int) -> tools.Deps:
    """The Deps the worker builds for the next bite: same store, nothing in memory."""
    import dataclasses

    return dataclasses.replace(
        deps, bite_id=bite_id, ledger_from=0, concluded=set(), visuals_state={}, visuals_landed=set(),
        summaries_off=False, summaries_owed_asked=False, notes_owed_asked=False, visuals_owed_asked=False,
        tally_loaded=False)


def test_what_a_run_owes_survives_a_pause_into_the_next_bite(tmp_path, real_cli):
    """Codex review: a run paused after ROUNDS_BEFORE_YIELD carries on in a new
    bite with new Deps; the debt and the tables state come from the store."""
    real_cli.edit = None
    first = _ran(tmp_path, CONCLUDE, CHECKOUT)
    later = _next_bite(first, 2)
    assert tools.summaries_owed(later) == ["experiment wider"]
    assert tools.visuals_owed(later) == ["experiment wider"]
    tools.tally_settled(later)
    assert tools.summaries_owed(_next_bite(first, 3)) == [], "an end that stood starts the next run clean"


def _ended(tmp_path):
    """A run that concludes `wider` and ends at once: the retries it was sent."""
    from probe.daemon import agent as agent_mod

    end = _end("concluded wider")
    model, _ = _scripted(_shell(CONCLUDE), end, end)
    deps = _deps(tmp_path)
    result = asyncio.run(agent_mod.build_agent("instructions", model=model).run("record", deps=deps))
    return _retries(result.all_messages()), deps


@pytest.mark.parametrize("mode", ["lane", None], ids=["lane", "unknown"])
def test_no_send_back_unless_the_team_is_in_recorder_mode(tmp_path, real_cli, team_mode, mode):
    """In lane mode the push is refused, so asking costs rounds for nothing
    (the CLI ships before the flip); an unknown mode is no reason either."""
    pytest.importorskip("pydantic_ai")  # the `daemon` extra
    team_mode["mode"] = mode
    retries, deps = _ended(tmp_path)
    assert retries == [] and team_mode["asked"] == 1
    assert tools.summaries_owed(_next_bite(deps, 2)) == [], "the end stood: nothing carries over"


def test_a_mode_seen_lately_is_not_asked_again(tmp_path, real_cli, team_mode):
    pytest.importorskip("pydantic_ai")  # the `daemon` extra
    deps = _deps(tmp_path)
    tools._note_mode(deps, "lane")
    retries, _ = _ended(tmp_path)
    assert retries == [] and team_mode["asked"] == 0


def test_a_chart_title_in_a_409_never_says_lane(tmp_path, server, real_cli):
    """Codex re-review: a refused `visuals set` prints the current list, whose
    titles anyone wrote; only the CLI's own error line can say lane."""
    drafts: dict[str, str] = {}

    def moved(stdout: str) -> None:
        drafts["path"] = json.loads(stdout)["path"]
        Path(drafts["path"]).write_text(json.dumps([{"kind": "table"}]))
        page = server.page(server.anchor_of(""))
        page["visuals"] = [{"id": "x", "kind": "table", "title": "summary_writer_off (mode lane)"}]
        page["version"] += 1  # someone set theirs first: our set meets a 409 naming it

    real_cli.after["visuals options"] = moved
    deps = _ran(tmp_path, CONCLUDE, CHECKOUT, "probe visuals options --experiment wider --project p")
    asyncio.run(tools.shell(deps, f"probe visuals set --experiment wider --project p --file {drafts['path']}"))
    assert real_cli.ran[-1][:2] == ["visuals", "set"], "the set ran (its 409 printed the list)"
    assert not deps.summaries_off


def test_a_refused_key_in_the_mode_read_hands_recording_back(tmp_path, monkeypatch):
    from probe.daemon import probe_api

    async def refused(env, kind, ref):
        raise probe_api.KeyRefused("401")

    monkeypatch.setattr(probe_api, "summaries_mode", refused)
    deps = _deps(tmp_path)
    assert asyncio.run(tools.summaries_mode(deps, "experiment wider")) is None
    assert deps.key_refused and deps.stopped


def test_once_lane_is_seen_the_summary_commands_are_not_run(tmp_path, server, real_cli):
    """Bench, lane mode (the CLI before the flip): the writer kept checking out,
    pushing and setting visuals the server refuses, +27% on writer-filing-b."""
    server.mode = "lane"
    deps = _ran(tmp_path, CHECKOUT)
    ran = len(real_cli.ran)
    for command in (CHECKOUT, PUSH, "probe visuals options --experiment wider --project p"):
        out = asyncio.run(tools.shell(deps, command))
        assert "mode lane" in out and "Record everything else" in out, out
    assert len(real_cli.ran) == ran, "nothing reached the CLI"
    asyncio.run(tools.shell(deps, CONCLUDE))
    assert len(real_cli.ran) == ran + 1, "other writes run as usual"
    deps.store.set_fact(tools.SUMMARIES_MODE, {"mode": "lane", "at": 0})
    asyncio.run(tools.shell(deps, CHECKOUT))
    assert len(real_cli.ran) == ran + 2, "a stale lane is asked again"
