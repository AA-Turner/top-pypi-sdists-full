"""A writer run that creates a project or experiment, or sets an experiment's
conclusion, owes that entity's summary (writer-owns-summary plan 3.5, bench
2026-10-16: one daemon-trial-2 replay set two conclusions and pushed no summary).
Plain code keeps the tally (`tools.note_summary_marks`) and the writer's output
validator sends the run back ONCE for what it did not push (`agent.SUMMARY_OWED`);
a team whose summaries are still the lane's owes nothing.
"""

from __future__ import annotations

import asyncio
import json

import pytest

from probe.daemon import tools

from test_daemon_same_response_end import SID, Probe, _deps, _retries, _state  # noqa: F401 -- fixture


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


class CheckoutProbe(Probe):
    """`Probe`, with `summary checkout` answering the JSON a real one prints."""

    def __init__(self, draft, *, eligible: bool = True) -> None:
        super().__init__()
        self.draft = draft
        self.eligible = eligible

    async def __call__(self, deps, argv, op_id, **kw):
        self.ran.append(list(argv))
        if argv[:2] == ["summary", "checkout"]:
            self.draft.write_text("")
            return tools.ProbeResult(0, json.dumps({"target": "experiment", "label": "wider", "path": str(self.draft),
                                                    "version": 0, "markdown": "",
                                                    "visuals": {"eligible": self.eligible, "count": 0}}))
        if argv[:2] == ["summary", "push"]:
            return tools.ProbeResult(0, json.dumps({"pushed": True, "merged": False, "version": 1}))
        if argv[:2] == ["visuals", "set"]:
            return tools.ProbeResult(0, json.dumps({"set": True, "version": 2}))
        if argv[:2] == ["visuals", "options"]:
            listing = self.draft.with_suffix(".visuals.json")
            listing.write_text("[]")
            return tools.ProbeResult(0, json.dumps({"path": str(listing), "eligible": True, "current": []}))
        return tools.ProbeResult(0, "{}")


def _ran(tmp_path, monkeypatch, *commands: str, outputs: dict[str, str] | None = None) -> tools.Deps:
    probe = CheckoutProbe(tmp_path / "draft.md")
    if outputs:
        async def answer(deps, argv, op_id, **kw):
            probe.ran.append(list(argv))
            head = " ".join(argv[:2])
            return tools.ProbeResult(0, outputs.get(head, "{}"))

        monkeypatch.setattr(tools, "run_probe_process", answer)
    else:
        monkeypatch.setattr(tools, "run_probe_process", probe)
    deps = _deps(tmp_path)
    for command in commands:
        asyncio.run(tools.shell(deps, command))
    return deps


@pytest.mark.parametrize("commands, owed", [
    (["probe experiment create wider --project p --question 'does it help?'"], ["experiment wider"]),
    (["probe project create digits --name Digits"], ["project digits"]),
    (["probe experiment set wider --conclusion 'keep 64 units'"], ["experiment wider"]),
    (["probe experiment set wider --conclusion 'keep 64 units'",
      "probe summary checkout --experiment wider --project p",
      "probe summary push --experiment wider --project p"], []),
    (["probe experiment set wider --name 'Wider layer'"], []),   # no conclusion: nothing owed
    (["probe run tag r1 done"], []),
], ids=["experiment-create", "project-create", "conclusion", "conclusion-then-push", "rename", "other-write"])
def test_what_a_run_owes(tmp_path, monkeypatch, commands, owed):
    deps = _ran(tmp_path, monkeypatch, *commands)
    assert tools.summaries_owed(deps) == owed


def test_a_lane_team_owes_nothing(tmp_path, monkeypatch):
    deps = _ran(tmp_path, monkeypatch,
                "probe experiment set wider --conclusion 'keep 64 units'",
                "probe summary checkout --experiment wider --project p",
                outputs={"summary checkout": json.dumps({"target": "experiment", "label": "wider",
                                                         "markdown": "", "version": 0, "mode": "lane"})})
    assert deps.summaries_off and tools.summaries_owed(deps) == []


def test_the_writer_is_sent_back_once_for_an_owed_summary(tmp_path, monkeypatch, team_mode):
    pytest.importorskip("pydantic_ai")  # the `daemon` extra
    from pydantic_ai.messages import ModelResponse, ToolCallPart
    from pydantic_ai.models.function import FunctionModel

    from probe.daemon import agent as agent_mod

    monkeypatch.setattr(tools, "run_probe_process", Probe())
    first = ModelResponse(parts=[
        ToolCallPart("shell", {"command": "probe experiment set wider --conclusion 'keep 64 units'"}),
    ])
    end = ModelResponse(parts=[ToolCallPart("final_result", {"summary": "concluded wider"})])
    end_again = ModelResponse(parts=[ToolCallPart("final_result", {"summary": "the summary waits for the seeds"})])
    responses = [first, end, end_again]
    seen: list = []

    def model(messages, info):
        seen.append(messages)
        return responses[min(len(seen), len(responses)) - 1]

    agent = agent_mod.build_agent("instructions", model=FunctionModel(model))
    result = asyncio.run(agent.run("record the session", deps=_deps(tmp_path)))
    retries = _retries(result.all_messages())
    assert len(retries) == 1 and retries[0].startswith("Not ended: these summaries were not updated in this run: "
                                                       "experiment wider.")
    assert result.output.summary == "the summary waits for the seeds", "the second end stands"


def test_a_run_that_pushed_its_summary_ends_at_once(tmp_path, monkeypatch, team_mode):
    pytest.importorskip("pydantic_ai")  # the `daemon` extra
    from pydantic_ai.messages import ModelResponse, ToolCallPart
    from pydantic_ai.models.function import FunctionModel

    from probe.daemon import agent as agent_mod

    monkeypatch.setattr(tools, "run_probe_process", CheckoutProbe(tmp_path / "draft.md", eligible=False))
    first = ModelResponse(parts=[
        ToolCallPart("shell", {"command": "probe experiment set wider --conclusion 'keep 64 units'"}),
        ToolCallPart("shell", {"command": "probe summary checkout --experiment wider --project p"}),
        ToolCallPart("shell", {"command": "probe summary push --experiment wider --project p"}),
    ])
    end = ModelResponse(parts=[ToolCallPart("final_result", {"summary": "concluded and summarised wider"})])
    responses = [first, end]
    seen: list = []

    def model(messages, info):
        seen.append(messages)
        return responses[min(len(seen), len(responses)) - 1]

    agent = agent_mod.build_agent("instructions", model=FunctionModel(model))
    result = asyncio.run(agent.run("record the session", deps=_deps(tmp_path)))
    assert _retries(result.all_messages()) == [] and len(seen) == 2



def test_a_concluded_eligible_experiment_owes_its_tables(tmp_path, monkeypatch):
    deps = _ran(tmp_path, monkeypatch,
                "probe experiment set wider --conclusion 'keep 64 units'",
                "probe summary checkout --experiment wider --project p",
                "probe summary push --experiment wider --project p")
    assert tools.summaries_owed(deps) == [] and tools.visuals_owed(deps) == ["experiment wider"]


def test_tables_set_this_run_are_not_owed(tmp_path, monkeypatch):
    deps = _ran(tmp_path, monkeypatch,
                "probe experiment set wider --conclusion 'keep 64 units'",
                "probe summary checkout --experiment wider --project p",
                "probe visuals options --experiment wider --project p",
                "probe visuals set --experiment wider --project p --file " + str(tmp_path / "draft.visuals.json"))
    assert tools.visuals_owed(deps) == []


def test_a_new_experiment_without_a_conclusion_owes_no_tables(tmp_path, monkeypatch):
    deps = _ran(tmp_path, monkeypatch,
                "probe experiment create wider --project p --question 'does it help?'",
                "probe summary checkout --experiment wider --project p")
    assert tools.visuals_owed(deps) == []



def test_the_writer_is_sent_back_once_more_for_owed_tables(tmp_path, monkeypatch, team_mode):
    pytest.importorskip("pydantic_ai")  # the `daemon` extra
    from pydantic_ai.messages import ModelResponse, ToolCallPart
    from pydantic_ai.models.function import FunctionModel

    from probe.daemon import agent as agent_mod

    monkeypatch.setattr(tools, "run_probe_process", CheckoutProbe(tmp_path / "draft.md"))
    first = ModelResponse(parts=[
        ToolCallPart("shell", {"command": "probe experiment set wider --conclusion 'keep 64 units'"}),
        ToolCallPart("shell", {"command": "probe summary checkout --experiment wider --project p"}),
        ToolCallPart("shell", {"command": "probe summary push --experiment wider --project p"}),
    ])
    end = ModelResponse(parts=[ToolCallPart("final_result", {"summary": "concluded wider"})])
    end_again = ModelResponse(parts=[ToolCallPart("final_result", {"summary": "tables wait for the last seed"})])
    responses = [first, end, end_again]
    seen: list = []

    def model(messages, info):
        seen.append(messages)
        return responses[min(len(seen), len(responses)) - 1]

    agent = agent_mod.build_agent("instructions", model=FunctionModel(model))
    result = asyncio.run(agent.run("record the session", deps=_deps(tmp_path)))
    retries = _retries(result.all_messages())
    assert len(retries) == 1 and retries[0].startswith("Not ended: these experiments have no tables or charts set: "
                                                       "experiment wider.")
    assert result.output.summary == "tables wait for the last seed"


def test_both_send_backs_leave_the_writer_its_own_output_retries(tmp_path, monkeypatch, team_mode):
    """The two send-backs spend pydantic-ai's OUTPUT retry budget, which a run
    never refills: with only the 2 every other tool gets, one malformed end after
    them failed the whole run ("Exceeded maximum output retries")."""
    pytest.importorskip("pydantic_ai")  # the `daemon` extra
    from pydantic_ai.messages import ModelResponse, ToolCallPart
    from pydantic_ai.models.function import FunctionModel

    from probe.daemon import agent as agent_mod

    monkeypatch.setattr(tools, "run_probe_process", CheckoutProbe(tmp_path / "draft.md"))
    first = ModelResponse(parts=[
        ToolCallPart("shell", {"command": "probe experiment set wider --conclusion 'keep 64 units'"}),
        ToolCallPart("shell", {"command": "probe summary checkout --experiment wider --project p"}),
    ])
    end = ModelResponse(parts=[ToolCallPart("final_result", {"summary": "concluded wider"})])
    malformed = ModelResponse(parts=[ToolCallPart("final_result", {"reply": "no summary field"})])
    responses = [first, end, malformed, end, end]
    seen: list = []

    def model(messages, info):
        seen.append(messages)
        return responses[min(len(seen), len(responses)) - 1]

    agent = agent_mod.build_agent("instructions", model=FunctionModel(model))
    result = asyncio.run(agent.run("record the session", deps=_deps(tmp_path)))
    retries = _retries(result.all_messages())
    assert len(retries) == 3, retries
    assert retries[0].startswith("Not ended: these summaries") and retries[2].startswith("Not ended: these experiments")
    assert result.output.summary == "concluded wider"


class Answers(CheckoutProbe):
    """`CheckoutProbe`, with some commands answering `(code, stdout)` as given."""

    def __init__(self, draft, answers: dict[str, tuple[int, str]]) -> None:
        super().__init__(draft)
        self.answers = answers

    async def __call__(self, deps, argv, op_id, **kw):
        head = " ".join(argv[:2])
        if head in self.answers:
            self.ran.append(list(argv))
            return tools.ProbeResult(*self.answers[head])
        return await super().__call__(deps, argv, op_id, **kw)


def _with(tmp_path, monkeypatch, answers, *commands):
    monkeypatch.setattr(tools, "run_probe_process", Answers(tmp_path / "draft.md", answers))
    deps = _deps(tmp_path)
    for command in commands:
        asyncio.run(tools.shell(deps, command))
    return deps


CONCLUDE = "probe experiment set wider --conclusion 'keep 64 units'"
CHECKOUT = "probe summary checkout --experiment wider --project p"
PUSH = "probe summary push --experiment wider --project p"


@pytest.mark.parametrize("answer", [
    (0, json.dumps({"pushed": False, "merged": True, "version": 4, "detail": "merged; push again to send it"})),
    (0, json.dumps({"pushed": False, "merged": False, "version": 3, "detail": "no local edits"})),
    (2, json.dumps({"pushed": False, "conflicted": True, "detail": "conflict markers written"})),
    (1, json.dumps({"pushed": False, "detail": "summary text over 12,000 characters"})),
], ids=["merged-only", "no-edits", "conflict", "refused"])
def test_only_a_push_that_landed_settles_the_summary(tmp_path, monkeypatch, answer):
    """Both reviews: a merge that asks for another push, a conflict or a refusal
    published nothing, so the summary stays owed."""
    deps = _with(tmp_path, monkeypatch, {"summary push": answer}, CONCLUDE, CHECKOUT, PUSH)
    assert tools.summaries_owed(deps) == ["experiment wider"]


def test_a_conclusion_after_the_push_owes_it_again(tmp_path, monkeypatch):
    deps = _ran(tmp_path, monkeypatch, CHECKOUT, PUSH, CONCLUDE)
    assert tools.summaries_owed(deps) == ["experiment wider"]


def test_only_a_summary_command_can_say_lane(tmp_path, monkeypatch):
    """Prose the model or a person wrote can hold the lane's words: a project's
    description, a page read by a checkout in recorder mode."""
    lane_words = "this team: summary_writer_off (mode lane)"
    deps = _with(tmp_path, monkeypatch, {
        "experiment set": (0, json.dumps({"description": lane_words})),
        "summary checkout": (0, json.dumps({"target": "experiment", "label": "wider", "version": 1,
                                            "markdown": lane_words, "mode": "recorder"})),
    }, CONCLUDE, CHECKOUT)
    assert not deps.summaries_off and tools.summaries_owed(deps) == ["experiment wider"]
    refused = _with(tmp_path, monkeypatch, {
        "summary push": (1, json.dumps({"pushed": False, "detail": "the lane writes summaries (mode lane)"})),
    }, CONCLUDE, CHECKOUT, PUSH)
    assert refused.summaries_off and tools.summaries_owed(refused) == []


def _next_bite(deps: tools.Deps, bite_id: int) -> tools.Deps:
    """The Deps the worker builds for the next bite: same store, nothing in memory."""
    import dataclasses

    return dataclasses.replace(
        deps, bite_id=bite_id, summaries_owed=set(), summaries_pushed=set(), concluded=set(), visuals_state={},
        visuals_landed=set(), summaries_off=False, summaries_owed_asked=False, visuals_owed_asked=False,
        tally_loaded=False)


def test_what_a_run_owes_survives_a_pause_into_the_next_bite(tmp_path, monkeypatch):
    """Codex review: a run paused after ROUNDS_BEFORE_YIELD carries on in a new
    bite with new Deps; the debt and the tables state come from the store."""
    first = _ran(tmp_path, monkeypatch, CONCLUDE, CHECKOUT)
    later = _next_bite(first, 2)
    assert tools.summaries_owed(later) == ["experiment wider"]
    assert tools.visuals_owed(later) == ["experiment wider"]
    tools.tally_settled(later)
    assert tools.summaries_owed(_next_bite(first, 3)) == [], "an end that stood starts the next run clean"


def _ended(tmp_path, monkeypatch):
    """A run that concludes `wider` and ends at once: the retries it was sent."""
    from pydantic_ai.messages import ModelResponse, ToolCallPart
    from pydantic_ai.models.function import FunctionModel

    from probe.daemon import agent as agent_mod

    monkeypatch.setattr(tools, "run_probe_process", Probe())
    first = ModelResponse(parts=[ToolCallPart("shell", {"command": CONCLUDE})])
    end = ModelResponse(parts=[ToolCallPart("final_result", {"summary": "concluded wider"})])
    responses = [first, end, end]
    seen: list = []

    def model(messages, info):
        seen.append(messages)
        return responses[min(len(seen), len(responses)) - 1]

    deps = _deps(tmp_path)
    result = asyncio.run(agent_mod.build_agent("instructions", model=FunctionModel(model)).run("record", deps=deps))
    return _retries(result.all_messages()), deps


@pytest.mark.parametrize("mode", ["lane", None], ids=["lane", "unknown"])
def test_no_send_back_unless_the_team_is_in_recorder_mode(tmp_path, monkeypatch, team_mode, mode):
    """In lane mode the push is refused, so asking costs rounds for nothing
    (the CLI ships before the flip); an unknown mode is no reason either."""
    pytest.importorskip("pydantic_ai")  # the `daemon` extra
    team_mode["mode"] = mode
    retries, deps = _ended(tmp_path, monkeypatch)
    assert retries == [] and team_mode["asked"] == 1
    assert tools.summaries_owed(_next_bite(deps, 2)) == [], "the end stood: nothing carries over"


def test_a_mode_seen_lately_is_not_asked_again(tmp_path, monkeypatch, team_mode):
    pytest.importorskip("pydantic_ai")  # the `daemon` extra
    deps = _deps(tmp_path)
    tools._note_mode(deps, "lane")
    retries, _ = _ended(tmp_path, monkeypatch)
    assert retries == [] and team_mode["asked"] == 0


def test_a_chart_title_in_a_409_never_says_lane(tmp_path, monkeypatch):
    """Codex re-review: a refused `visuals set` prints the current list, whose
    titles anyone wrote; only the CLI's own error line can say lane."""
    titled = json.dumps({"set": False, "current": [{"id": "x", "kind": "table", "title": "summary_writer_off (mode lane)"}]})
    probe = Answers(tmp_path / "draft.md", {"visuals set": (2, titled)})
    monkeypatch.setattr(tools, "run_probe_process", probe)
    deps = _deps(tmp_path)
    for command in (CONCLUDE, CHECKOUT, "probe visuals options --experiment wider --project p",
                    "probe visuals set --experiment wider --project p"):
        asyncio.run(tools.shell(deps, command))
    assert probe.ran[-1][:2] == ["visuals", "set"], "the set ran (its 409 printed the list)"
    assert not deps.summaries_off


def test_a_refused_key_in_the_mode_read_hands_recording_back(tmp_path, monkeypatch):
    from probe.daemon import probe_api

    async def refused(env, kind, ref):
        raise probe_api.KeyRefused("401")

    monkeypatch.setattr(probe_api, "summaries_mode", refused)
    deps = _deps(tmp_path)
    assert asyncio.run(tools.summaries_mode(deps, "experiment wider")) is None
    assert deps.key_refused and deps.stopped


def test_once_lane_is_seen_the_summary_commands_are_not_run(tmp_path, monkeypatch):
    """Bench, lane mode (the CLI before the flip): the writer kept checking out,
    pushing and setting visuals the server refuses, +27% on writer-filing-b."""
    probe = Answers(tmp_path / "draft.md", {
        "summary checkout": (0, json.dumps({"target": "experiment", "label": "wider", "version": 0,
                                            "markdown": "", "mode": "lane"})),
    })
    monkeypatch.setattr(tools, "run_probe_process", probe)
    deps = _deps(tmp_path)
    asyncio.run(tools.shell(deps, CHECKOUT))
    ran = len(probe.ran)
    for command in (CHECKOUT, PUSH, "probe visuals options --experiment wider --project p"):
        out = asyncio.run(tools.shell(deps, command))
        assert "mode lane" in out and "Record everything else" in out, out
    assert len(probe.ran) == ran, "nothing reached the CLI"
    asyncio.run(tools.shell(deps, CONCLUDE))
    assert len(probe.ran) == ran + 1, "other writes run as usual"
    deps.store.set_fact(tools.SUMMARIES_MODE, {"mode": "lane", "at": 0})
    asyncio.run(tools.shell(deps, CHECKOUT))
    assert len(probe.ran) == ran + 2, "a stale lane is asked again"
