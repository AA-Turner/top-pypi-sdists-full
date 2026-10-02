"""Who the CLI and SDK say composed a name, and what actually leaves the process.

THE BUG THIS EXISTS FOR. `app/core/authorship.py` shipped `Authorship` and
`owns_field` on every project/experiment/run create and patch, and no client
ever sent the field. So every `--name` an agent typed arrived undeclared, the
server applied its historical inference ("a name arrived, a person sent it"),
and the row was stamped `name_customized = true` -- locked out of generation
forever, with no undo. Measured 2026-09-18: 15 projects and 66 experiments
rendering their slug because the prompt's answer to that was "never pass a
name".

WHAT IS ASSERTED HERE, AND WHAT IS NOT. These tests assert what the client puts
ON THE WIRE. They deliberately do NOT assert what the server does with it --
that lock, its monotonicity and its one-way-ness live in
`tests/unit/test_authorship.py` and `tests/integration/test_authorship_routes.py`
against the real routes. Re-asserting them here would only prove the fake
agrees with itself, which is the exact failure mode `_owns_field`'s truth table
below exists to catch.
"""

from __future__ import annotations

import json

import pytest

from probe import Authorship
from probe.sdk.agent_session import (
    AGENTS,
    AUTHORSHIP_AGENT,
    AUTHORSHIP_HUMAN,
    default_authorship,
)
from tests.conftest import _owns_field

#: Every variable that makes `detect_agent` say yes, flattened off AGENTS so a
#: new coding agent cannot be added without this file having an opinion.
_DETECT_VARS = [(spec.label, var) for spec in AGENTS for var in spec.detect_env]


@pytest.fixture
def no_agent(monkeypatch):
    """A bare terminal. THIS SUITE RUNS INSIDE A CODING AGENT, so without it the
    negative cases pass for the wrong reason -- or fail on someone else's box."""
    for _, var in _DETECT_VARS:
        monkeypatch.delenv(var, raising=False)
    return monkeypatch


class TestTheDefaultReadsTheEnvironmentAndNothingElse:
    @pytest.mark.parametrize(
        ("label", "var"), _DETECT_VARS, ids=[f"{label}:{var}" for label, var in _DETECT_VARS]
    )
    def test_every_detect_var_declares_agent(self, no_agent, label, var):
        no_agent.setenv(var, "1")
        assert default_authorship() == AUTHORSHIP_AGENT

    def test_an_uncaptured_agent_still_counts(self, no_agent):
        """Cursor is detectable and its transcripts are NOT captured, so
        `resolve_agent_session` rejects it. Authorship asks a different
        question: a program is composing the name either way."""
        no_agent.setenv("CURSOR_TRACE_ID", "abc")
        assert default_authorship() == AUTHORSHIP_AGENT

    def test_a_bare_terminal_declares_nothing(self, no_agent):
        """None, never "human". Declaring a person from a heuristic is the one
        move app/core/authorship.py exists to refuse."""
        assert default_authorship() is None

    def test_an_empty_variable_is_not_an_agent(self, no_agent):
        """`detect_agent` truth-tests the value, so `CLAUDECODE=` is absence.
        A stale empty export must not start claiming authorship."""
        no_agent.setenv("CLAUDECODE", "")
        assert default_authorship() is None

    def test_the_cli_choice_surface_matches_the_generated_enum(self):
        """`AuthoredBy` is a third spelling of the same vocabulary -- typer needs
        an Enum for the choice surface, and the generated model is pydantic. Its
        docstring claims this test pins it; without the assertion a third
        `Authorship` value would be missing from `--authored-by` with nothing
        failing."""
        from probe.cli.main import AuthoredBy

        assert {m.value for m in AuthoredBy} == {m.value for m in Authorship}

    def test_the_literals_match_the_generated_enum(self):
        """agent_session is stdlib-only and cannot import the pydantic enum, so
        it spells the two values. This is the pin that stops them drifting."""
        assert AUTHORSHIP_AGENT == Authorship.agent.value
        assert AUTHORSHIP_HUMAN == Authorship.human.value
        assert {AUTHORSHIP_AGENT, AUTHORSHIP_HUMAN} == {m.value for m in Authorship}


class TestTheFakeAgreesWithTheServersRule:
    """`conftest._owns_field` mirrors `app/core/authorship.py::owns_field`. The
    agent suite cannot import `app.`, so the mirror is hand-written -- and a
    mirror nobody checks is how a naming test passes against a fiction."""

    @pytest.mark.parametrize(
        ("value", "authored_by", "expected"),
        [
            ("Teacher Rollouts", None, True),  # historical inference
            ("Teacher Rollouts", "human", True),  # declared: locks
            ("Teacher Rollouts", "agent", False),  # declared: enhanceable
            (None, None, False),  # nothing supplied, nothing owned
            (None, "human", False),
            ("", "human", False),  # clearing hands it back
        ],
    )
    def test_the_truth_table(self, value, authored_by, expected):
        assert _owns_field(value, authored_by) is expected


def _bodies(app, method, needle):
    return [
        json.loads(r.content or b"{}")
        for r in app.requests
        if r.method == method and needle in r.url.path
    ]


class TestWhatLeavesTheProcessOnACreate:
    def test_under_an_agent_the_declaration_is_sent(self, client, app, no_agent):
        no_agent.setenv("CLAUDECODE", "1")
        client.create_project("declared-proj", "Declared Project", kind="general")
        body = _bodies(app, "POST", "/v1/projects")[-1]
        assert body["authored_by"] == AUTHORSHIP_AGENT

    def test_in_a_bare_terminal_the_key_is_ABSENT_not_null(self, client, app, no_agent):
        """Absence and null are different claims. Absent = "this client has not
        been taught to say", which is byte-identical to every release before
        this one. Null would be a new assertion about a person."""
        client.create_project("undeclared-proj", "Undeclared Project", kind="general")
        body = _bodies(app, "POST", "/v1/projects")[-1]
        assert "authored_by" not in body, f"sent {body.get('authored_by')!r}"

    def test_an_explicit_human_overrides_the_agent_default(self, client, app, no_agent):
        no_agent.setenv("CLAUDECODE", "1")
        client.create_project(
            "their-words", "Their Words", kind="general", authored_by=AUTHORSHIP_HUMAN
        )
        body = _bodies(app, "POST", "/v1/projects")[-1]
        assert body["authored_by"] == AUTHORSHIP_HUMAN

    def test_an_experiment_carries_it_too(self, client, app, no_agent):
        no_agent.setenv("CLAUDECODE", "1")
        project = client.create_project("exp-host", kind="general")
        client.create_experiment(
            "declared-exp", "Declared Exp", question="does it?", project_id=project["id"]
        )
        body = _bodies(app, "POST", "/v1/projects")[-1]
        assert body["authored_by"] == AUTHORSHIP_AGENT

    def test_the_slug_is_no_longer_sent_as_the_name(self, client, app, no_agent):
        """`name or slug` was a no-op server-side (`chosen_name` nulls it) and a
        LIE once authorship is on the wire: the slug plus a declaration claims
        somebody chose the identifier as the title."""
        client.create_project("no-name-please", kind="general")
        body = _bodies(app, "POST", "/v1/projects")[-1]
        assert "name" not in body, f"sent name={body.get('name')!r}"


class TestWhatLeavesTheProcessOnAPatch:
    def test_a_patch_carries_the_declaration(self, client, app, no_agent):
        no_agent.setenv("CLAUDECODE", "1")
        project = client.create_project("patch-me", kind="general")
        client.update_project(project["id"], name="Renamed By A Program")
        body = _bodies(app, "PATCH", f"/v1/projects/{project['id']}")[-1]
        assert body["authored_by"] == AUTHORSHIP_AGENT
        assert body["name"] == "Renamed By A Program"

    def test_authorship_alone_is_not_a_field_to_set(self, client, no_agent):
        """It declares who wrote the OTHER fields. On its own it declares
        authorship of nothing, and must not turn a no-op call into a PATCH."""
        no_agent.setenv("CLAUDECODE", "1")
        project = client.create_project("nothing-to-set", kind="general")
        with pytest.raises(ValueError, match="at least one field"):
            client.update_project(project["id"])


class TestTheNESTEDCreatesInheritIt:
    def test_an_experiment_auto_created_by_run_declares_the_same_author(
        self, client, app, no_agent
    ):
        """`run()` reaches `ensure_experiment`, which used to pass no
        declaration -- so a run was enhanceable while the experiment born
        alongside it was locked, by the same caller, in the same breath."""
        no_agent.setenv("CLAUDECODE", "1")
        project = client.create_project("nested-host", kind="general")
        client.run(
            experiment="born-with-the-run",
            question="does the parent inherit?",
            project=project["slug"],
            heartbeat=False,
        )
        body = _bodies(app, "POST", "/v1/projects")[-1]
        assert body["authored_by"] == AUTHORSHIP_AGENT

    def test_the_auto_created_experiment_is_not_named_after_its_slug(self, client, app, no_agent):
        no_agent.setenv("CLAUDECODE", "1")
        project = client.create_project("nested-host-2", kind="general")
        client.run(
            experiment="unnamed-parent",
            question="is it named?",
            project=project["slug"],
            heartbeat=False,
        )
        body = _bodies(app, "POST", "/v1/projects")[-1]
        assert "name" not in body, f"sent name={body.get('name')!r}"


class TestAFabricatedNameAlwaysDeclaresItself:
    def test_a_fork_with_no_name_declares_agent_even_in_a_bare_terminal(
        self, client, app, no_agent
    ):
        """`fork_run` composes `<source>-fork` when the caller gives no name.
        The SDK wrote that string, so the SDK says so -- otherwise it is the
        `run child --name` defect again: a machine string locked forever."""
        from tests.conftest import open_run

        parent = open_run(client, experiment="e1", slug="fork-source", heartbeat=False)
        client.fork_run(parent.id, step=0, heartbeat=False)
        body = _bodies(app, "POST", "/runs")[-1]
        assert body["authored_by"] == AUTHORSHIP_AGENT
        assert body["name"].endswith("-fork")


class TestAFabricatedNameNeverOverridesAnExplicitOne:
    """0170 follow-up. `fork_run` and the supersede path both compose a string
    and declare it -- but only when the caller has said nothing. Overwriting an
    explicit `--authored-by human` made the flag silently inert on the very path
    it is most used on: a fork with no `--name`."""

    def test_an_explicit_human_survives_a_fork_that_names_itself(
        self, client, app, no_agent
    ):
        from tests.conftest import open_run

        parent = open_run(client, experiment="e1", slug="fork-src-human", heartbeat=False)
        client.fork_run(parent.id, step=0, heartbeat=False, authored_by=AUTHORSHIP_HUMAN)
        body = _bodies(app, "POST", "/runs")[-1]
        assert body["authored_by"] == AUTHORSHIP_HUMAN, (
            "a fabricated NAME must not relabel words the researcher dictated"
        )

    def test_an_undeclared_fork_still_declares_itself(self, client, app, no_agent):
        from tests.conftest import open_run

        parent = open_run(client, experiment="e1", slug="fork-src-plain", heartbeat=False)
        client.fork_run(parent.id, step=0, heartbeat=False)
        body = _bodies(app, "POST", "/runs")[-1]
        assert body["authored_by"] == AUTHORSHIP_AGENT


class TestAnEmptyNameIsNotAName:
    def test_an_empty_string_is_omitted_rather_than_sent(self, client, app, no_agent):
        """`ProjectCreate.name` is `min_length=1`. `name or slug` used to swallow
        `""`; `name is not None` forwarded it and turned a working call into a
        422 -- reachable from `probe project create SLUG --name ""` and from a
        folder backfill whose basename is empty at a filesystem root."""
        client.create_project("empty-name-proj", "", kind="general")
        body = _bodies(app, "POST", "/v1/projects")[-1]
        assert "name" not in body
