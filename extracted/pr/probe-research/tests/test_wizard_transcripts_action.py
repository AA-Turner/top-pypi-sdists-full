"""Shared import selection and the retained direct transcript command paths."""

from __future__ import annotations

import pytest

from probe.cli import actions as actions_mod
from probe.cli.actions import ACTION_COPY, Action, grouped_actions


def _cli_main():
    """`probe.cli.main` is the entry-point FUNCTION on the package, not the
    module -- `from probe.cli import main` imports the wrong object."""
    import sys

    import probe.cli.main  # noqa: F401

    return sys.modules["probe.cli.main"]


def test_research_imports_share_one_menu_row_with_existing_imports_separate() -> None:
    groups = dict(grouped_actions())

    assert groups["Backfill"] == (Action.IMPORT_RESEARCH, Action.IMPORT_JOBS)
    assert ACTION_COPY[Action.IMPORT_RESEARCH][0] == "Import research work"
    assert ACTION_COPY[Action.IMPORT_JOBS][0] == "Existing imports"
    assert Action.BACKFILL not in ACTION_COPY and Action.TRANSCRIPTS not in ACTION_COPY


def test_menu_and_install_open_the_same_import_selector(monkeypatch) -> None:
    from probe.cli import setup, tui

    pages = []
    monkeypatch.setattr(tui, "ask", lambda question, **kwargs: pages.append(
        (question._probe_content, kwargs, tui.checkbox_control(question).selected_options),
    ) or [])
    setup.run_backfill_offer(("claude_code",))
    setup.run_backfill_offer(("claude_code",), onboarding=False)
    assert pages[0][0] == pages[1][0]
    assert pages[0][0]["title"] == ACTION_COPY[Action.IMPORT_RESEARCH][0]
    assert set(pages[0][2]) == set(pages[1][2]) == set(setup.BackfillChoice)
    assert pages[0][1]["progress"] and pages[1][1]["progress"] == []


def test_both_imports_skip_the_agent_picker() -> None:
    """Import lanes choose their own sources without asking which agents to
    configure. Existing imports observes the shared queue for this device."""
    assert actions_mod.IMPORT_ACTIONS == {
        Action.IMPORT_RESEARCH, Action.BACKFILL, Action.TRANSCRIPTS,
    }
    assert not (actions_mod.IMPORT_ACTIONS & actions_mod.DEVICE_ACTIONS)
    assert Action.IMPORT_JOBS in actions_mod.DEVICE_ACTIONS
    assert Action.IMPORT_JOBS not in actions_mod.IMPORT_ACTIONS


def _stub_lane(monkeypatch, seen: dict, lines=("imported 3 sessions",)):
    from probe.cli import backfill_transcripts as transcripts_mod

    cli_main = _cli_main()
    monkeypatch.setattr(cli_main, "_backfill_client", lambda: object())
    monkeypatch.setattr(
        transcripts_mod, "run_lane", lambda **kw: seen.update(kw) or list(lines)
    )
    return cli_main


@pytest.mark.parametrize("background", [True, False])
def test_the_action_runs_the_lane(monkeypatch, background) -> None:
    """The row reaches the lane, headless or not.

    It used to resolve a local coding agent to summarize with first, and the
    test worth having was that the lane was never handed `agent=None` with the
    gate already promising summaries. Both are gone: the digest lane retired
    server-side, so the row hands the lane nothing but `interactive`.
    """
    seen: dict = {}
    cli_main = _stub_lane(monkeypatch, seen)

    lines = cli_main._import_past_sessions(interactive=True, background=background)

    assert lines == ["imported 3 sessions"]
    assert seen["interactive"] is True
    assert seen["background"] is background


def test_the_menu_asks_no_agent_resolver_at_all(monkeypatch) -> None:
    """Guard against the resolvers coming back. `resolve_agent` refuses a
    pi-only machine outright, `resolve_digest_agent` runs `--help` against
    every agent binary on PATH and can open a picker -- and this lane needs
    neither now that it writes no summaries."""
    from probe.cli import backfill as backfill_impl

    seen: dict = {}
    cli_main = _stub_lane(monkeypatch, seen)
    for name in ("resolve_agent", "resolve_digest_agent"):
        monkeypatch.setattr(
            backfill_impl,
            name,
            lambda *a, _n=name, **k: pytest.fail(f"the transcripts lane must not call {_n}"),
            raising=False,  # `resolve_digest_agent` is gone; the guard outlives it
        )

    cli_main._import_past_sessions(interactive=False)

    assert seen["interactive"] is False
    assert "agent" not in seen and "digest_note" not in seen


# -- the other door: `probe backfill --transcripts-only` ----------------------


def _run_transcripts_only(monkeypatch, seen: dict, **kwargs):
    """Drive the `--transcripts-only` branch of the `backfill` command.

    Everything before the branch is bootstrap and telemetry; both reach the
    network and neither is what this is about.
    """
    from probe.cli import bootstrap
    from probe.cli import setup as wizard_mod
    from probe.cli import telemetry as telemetry_mod

    cli_main = _stub_lane(monkeypatch, seen)
    monkeypatch.setattr(
        bootstrap, "ensure_persistent_install", lambda *a, **k: type("B", (), {"message": ""})()
    )
    monkeypatch.setattr(
        telemetry_mod.TelemetryContext, "start", classmethod(
            lambda cls, **kw: telemetry_mod.null_context()
        )
    )
    monkeypatch.setattr(wizard_mod, "interactive", lambda: False)
    call = dict(
        folder=None, agent=None, project=None, transcripts=None,
        transcripts_only=True, transcripts_budget_mb=None,
    )
    call.update(kwargs)
    cli_main.backfill(**call)


def test_transcripts_only_uploads_without_resolving_an_agent(monkeypatch) -> None:
    """The sibling door to the menu row. It used to resolve a digest agent
    here, which is how a pi-only machine ended up refusing the whole lane
    rather than uploading its pi sessions; there is nothing left to resolve."""
    from probe.cli import backfill as backfill_impl

    seen: dict = {}
    for name in ("resolve_agent", "resolve_digest_agent"):
        monkeypatch.setattr(
            backfill_impl,
            name,
            lambda *a, _n=name, **k: pytest.fail(f"--transcripts-only must not call {_n}"),
            raising=False,
        )
    _run_transcripts_only(monkeypatch, seen)

    assert seen["interactive"] is False and seen["budget_bytes"] is None
    assert "agent" not in seen and "digest_note" not in seen


def test_transcripts_only_still_carries_the_byte_budget(monkeypatch) -> None:
    """`--transcripts-budget-mb` is the one flag this branch still forwards."""
    seen: dict = {}
    _run_transcripts_only(monkeypatch, seen, transcripts_budget_mb=2)

    assert seen["budget_bytes"] == 2 * 1024 * 1024


def test_the_agent_flag_no_longer_offers_pi_for_summaries() -> None:
    """`--agent pi` was advertised because the transcripts lane would take it
    to write summaries. That lane is gone and the folder importer refuses pi,
    so no lane accepts it and the help must not offer it."""
    import inspect

    cli_main = _cli_main()
    help_text = inspect.signature(cli_main.backfill).parameters["agent"].default.help

    assert "pi" not in help_text
    assert "summaries" not in help_text


@pytest.mark.parametrize("interactive", [True, False])
def test_the_menu_action_dispatches_to_the_lane(monkeypatch, interactive) -> None:
    """The row is wired to the helper, not to the folder importer next to it."""
    from probe.cli import setup as wizard_mod

    cli_main = _cli_main()

    # `wizard` inside `_run_wizard_action` is a LOCAL `from probe.cli import
    # setup as wizard` -- the module-level name is the typer command that
    # shadows it -- so the module is what has to be patched.
    monkeypatch.setattr(wizard_mod, "interactive", lambda: interactive)
    seen: dict = {}
    monkeypatch.setattr(
        cli_main, "_import_past_sessions", lambda **kw: seen.update(kw) or ["ok"]
    )

    lines = cli_main._run_wizard_action(
        Action.TRANSCRIPTS,
        caps=None,
        base_now="https://example.test",
        yes=False,
        tracking=None,
        capture=None,
        auto_update=None,
        agent_rules=None,
        uninstall=False,
        configured=True,
        folder=None,
    )

    assert lines == ["ok"]
    assert seen == {"interactive": interactive, "background": interactive}
