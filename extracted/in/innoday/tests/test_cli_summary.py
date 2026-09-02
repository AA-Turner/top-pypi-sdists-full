"""What `innoday summary` puts on the screen, pinned (PF-398).

The renderer is pure -- everything it needs is in the payload the engine
returns -- so every layout rule that matters is testable without a server:
which block a line lands in, who gets an `@`, how an unmapped assignee reads,
what the footer claims, and what happens when the caller themselves is the
thing that is unmapped.
"""

import argparse
from datetime import datetime, timezone

import pytest

from src.cli.commands.summary import (
    DEFAULT_WINDOW,
    SummaryCommands,
    SummaryWindow,
    _summary_params,
    no_identity_message,
    parse_window_arg,
    render_summary,
)
from src.utils.time_windows import normalize_window


def line(**kw):
    base = {
        "block": "active",
        "ticket_id": 1,
        "ticket_ref": "PF-118",
        "summary": "Tenant-scoped audit log retention",
        "status": "in review",
        "assignee_user_id": "u-karl",
        "assignee_display": "karl",
        "assignee_unmapped": False,
        "owner_label": "karl",
        "attribution": "board",
        "repo": "innoday",
        "branch": "PF-118-audit-retention",
        "pr_url": "https://github.com/havilandsoftware/innoday/pull/412",
        "pr_state": "open",
        "occurred_at": "2026-08-05T09:40:00+00:00",
        "commit_count": 3,
        "rank": 0,
    }
    base.update(kw)
    return base


def payload(**kw):
    base = {
        "outcome": "assembled",
        "summary_type": "personal",
        "window_spec": "3d",
        "active": [line()],
        "active_total": 1,
        "no_work_detected": [],
        "unassigned_work_happening": [],
        "unassigned_idle_count": 0,
        "up_next": [],
        "footer": "1 of 1 active shown",
        "unmapped_assignee_count": 0,
        "body_markdown": None,
    }
    base.update(kw)
    return base


def render(data, scrum=False):
    return render_summary(data, scrum=scrum, org_alias="hs", project_label="PF")


class TestActiveBlock:
    """One line shape, shared with a release note.

    These two used to pin the old stand-up-only layout: `PF-118 — <title>` glued
    together on the heading, a `repo · branch` context row, and the pull request
    on a third line as `→ PR #412 (open)`. A release note rendered the same data
    as prose over `ref · people · PRs · verdict`, and a team reading both could
    not tell it was one system.

    Every field below is still rendered -- these assert where, not whether.
    """

    def test_the_line_leads_with_what_it_says_and_carries_the_ref_below(self):
        out = render(payload())
        assert "Tenant-scoped audit log retention" in out
        assert "PF-118" in out
        # The ref has its own slot now, so gluing it to the title printed it twice.
        assert "PF-118 — Tenant-scoped audit log retention" not in out

    def test_the_status_and_the_moment_both_survive(self):
        out = render(payload())
        assert "🟢 In Review" in out
        assert "Aug 5, 09:40" in out

    def test_shows_the_pr_without_inventing_a_title_or_approvals(self):
        out = render(payload())
        assert "innoday#412 (open)" in out
        assert "approval" not in out

    def test_a_branch_with_no_pull_request_still_names_the_branch(self):
        """The one case where a branch name is all a reader has to go on."""
        out = render(payload(active=[line(pr_url=None, pr_state=None)]))
        assert "innoday:PF-118-audit-retention" in out

    def test_no_diff_stats_or_commit_counts(self):
        out = render(payload())
        assert "commit" not in out.lower()
        assert "+" not in out


class TestScrumOnlyAssignee:
    def test_personal_mode_omits_the_owner(self):
        assert "@karl" not in render(payload(), scrum=False)

    def test_scrum_mode_shows_the_owner(self):
        assert "@karl" in render(payload(), scrum=True)

    def test_code_attribution_says_where_the_name_came_from(self):
        data = payload(active=[line(attribution="code", assignee_display="havkarl")])
        assert "@havkarl (from commits)" in render(data, scrum=True)

    def test_unmapped_assignee_is_marked_not_dropped(self):
        data = payload(
            active=[
                line(
                    assignee_user_id=None,
                    assignee_display="A. Lice",
                    assignee_unmapped=True,
                    owner_label="@A. Lice (unmapped)",
                )
            ]
        )
        out = render(data, scrum=True)
        assert "@A. Lice (unmapped)" in out


class TestBlocksAndTheCap:
    def test_idle_items_sit_in_their_own_block(self):
        data = payload(
            no_work_detected=[
                line(
                    block="no_work_detected",
                    ticket_ref="PF-121",
                    summary="Rotate ingest shared secrets",
                    status="todo",
                    repo=None,
                    branch=None,
                    pr_url=None,
                    pr_state=None,
                    occurred_at=None,
                )
            ]
        )
        out = render(data)
        assert "── No work detected ──" in out
        assert "PF-121" in out

    def test_idle_items_do_not_consume_an_active_slot(self):
        """The footer counts active work only; idle rows are extra, not part of it."""
        data = payload(
            active=[line()],
            active_total=1,
            footer="1 of 1 active shown",
            no_work_detected=[line(block="no_work_detected", ticket_ref="PF-121")],
        )
        out = render(data)
        assert "1 of 1 active shown" in out
        assert "2 of" not in out

    def test_the_cap_is_reported_not_hidden(self):
        data = payload(
            active=[line(ticket_ref=f"PF-{n}") for n in range(5)],
            active_total=12,
            footer="5 of 12 active shown",
        )
        assert "5 of 12 active shown" in render(data)

    def test_unassigned_work_happening_block(self):
        data = payload(
            unassigned_work_happening=[
                line(
                    block="unassigned_work_happening",
                    ticket_ref="PF-140",
                    summary="Add tenant usage export",
                    attribution="code",
                    assignee_display="karl",
                )
            ]
        )
        out = render(data, scrum=True)
        assert "── Unassigned — work happening ──" in out
        assert "PF-140" in out
        assert "@karl (from commits)" in out

    def test_up_next_is_personal_mode_only(self):
        data = payload(up_next=[line(block="up_next", ticket_ref="PF-121")])
        assert "── Up next ──" in render(data, scrum=False)
        assert "── Up next ──" not in render(data, scrum=True)

    def test_cached_prose_is_rendered_when_there_is_some(self):
        data = payload(outcome="cached", body_markdown="Audit retention landed.")
        out = render(data)
        assert "Audit retention landed." in out
        assert "cached" in out


class TestFooter:
    def test_unmapped_count_points_at_the_profile_page(self):
        data = payload(unmapped_assignee_count=2)
        out = render(data)
        assert "2 assignees unmapped — map at /ui/hs/profile" in out

    def test_singular_unmapped_reads_naturally(self):
        assert "1 assignee unmapped" in render(payload(unmapped_assignee_count=1))

    def test_idle_backlog_is_counted_not_listed(self):
        out = render(payload(unassigned_idle_count=7))
        assert "7 unassigned idle" in out

    def test_a_quiet_window_says_so(self):
        data = payload(active=[], active_total=0, footer="0 of 0 active shown")
        assert "Nothing moved in this window." in render(data)


class TestNoIdentityMessage:
    def test_names_the_fix_not_the_emptiness(self):
        message = no_identity_message(
            project_label="PF", org_alias="hs", candidate_count=0
        )
        assert "No board identity for you on PF" in message
        # The runnable fix comes first. The browser form is still named, but a
        # message whose *only* remedy is a web page is not a fix a terminal --
        # or an agent driving one -- can act on.
        assert "innoday auth identity --set" in message
        assert "/ui/hs/profile" in message

    def test_says_how_many_candidates_were_actually_seen(self):
        message = no_identity_message(
            project_label="PF", org_alias="hs", candidate_count=3
        )
        assert "3 unmapped names seen" in message

    def test_one_candidate_reads_singular(self):
        message = no_identity_message(
            project_label="PF", org_alias="hs", candidate_count=1
        )
        assert "1 unmapped name seen" in message


class TestParser:
    @pytest.fixture
    def parser(self):
        parser = argparse.ArgumentParser()
        SummaryCommands.setup_parser(parser)
        return parser

    def test_the_common_case_takes_no_flags(self, parser):
        args = parser.parse_args([])
        assert args.scrum is False
        assert args.window == DEFAULT_WINDOW

    @pytest.mark.parametrize("window", [w.value for w in SummaryWindow])
    def test_every_named_window_is_accepted(self, parser, window):
        """The named ones still work; the aliases arrive canonicalised.

        `release` is the exception -- it has no duration until the server
        answers, so it passes through as itself.
        """
        parsed = parser.parse_args(["--window", window]).window
        expected = window if window == "release" else normalize_window(window)
        assert parsed == expected

    @pytest.mark.parametrize("window", ["12h", "2w", "1h", "10d"])
    def test_any_duration_the_engine_accepts_is_accepted_here(self, parser, window):
        """These four were rejected by the old `choices` list, while the engine
        took them happily -- the divergence this replaced."""
        assert parser.parse_args(["--window", window]).window == window

    def test_there_is_deliberately_no_choices_list(self, parser):
        """A `choices` list could only ever be a subset of the grammar, which is
        how `--window 2w` came to be rejected. Validation moved to `type=`."""
        action = next(a for a in parser._actions if a.dest == "window")
        assert action.choices is None
        assert action.type is parse_window_arg

    def test_the_default_survives_argparse_untouched(self, parser):
        """`default=` bypasses `type=`, so the default is the one value that is
        never normalised -- it has to be canonical as written."""
        action = next(a for a in parser._actions if a.dest == "window")
        assert normalize_window(action.default) == action.default

    def test_rejects_an_unknown_window(self, parser):
        with pytest.raises(SystemExit):
            parser.parse_args(["--window", "fortnight"])

    def test_project_override_does_not_shadow_the_global_flag(self, parser):
        """A local --project reusing dest='project_id' would clobber the global one."""
        action = next(a for a in parser._actions if "--project" in a.option_strings)
        assert action.dest == "summary_project"


class TestReleaseScope:
    """`--window release` is a **scope**, not a day count (#563, defect 3).

    These three tests used to pin the opposite: the command fetched the
    project's releases, took `max(released_at)`, and returned "N days" -- the
    release's identity was discarded before the engine ever saw it, so nothing
    downstream could filter by it. They also stubbed the client with `"PF"`,
    which is why none of them could see that the ref was being sent as
    `?project_id=` where the endpoint matched `Release.project_id` exactly: an
    alias matched zero rows and the command silently summarised the last week
    instead.

    Resolving `current` is now the server's job -- there are already two
    resolvers for it, and computing a third one here is what produced the bug.
    """

    def test_fixed_windows_are_a_window_and_no_release(self):
        assert SummaryCommands.window_to_scope("week") == ("1w", None, None)

    def test_a_release_scope_names_the_release_instead_of_a_duration(self):
        window_spec, release, note = SummaryCommands.window_to_scope("release")
        assert window_spec is None
        assert release == "current"
        assert "release" in note

    def test_no_day_count_is_computed_client_side(self):
        """The whole defect: a duration cannot express "these tickets"."""
        _, release, _ = SummaryCommands.window_to_scope("release")
        assert release is not None and not release.endswith("d")


class TestReleaseScopeRendering:
    """What a release-scoped summary must say about its own boundary."""

    def _release_payload(self, **kw):
        base = dict(
            window_spec="release:v1.9.0",
            release="v1.9.0",
            release_ticket_count=4,
            tickets_without_release_count=337,
        )
        base.update(kw)
        return payload(**base)

    def test_the_header_names_the_release_not_a_duration(self):
        out = render(self._release_payload())
        assert "release v1.9.0" in out
        assert "last release:v1.9.0" not in out

    def test_the_boundary_is_stated_once_with_what_it_left_out(self):
        """Most tickets carry no release, so a release summary is a slice.

        Reporting a subset without saying so is the hazard -- the reader has no
        way to tell a quiet release from a quiet project.
        """
        out = render(self._release_payload())
        assert "4" in out and "337" in out
        assert out.count("on no release") == 1

    def test_absence_is_labelled_as_the_releases_absence(self):
        """`no_work_detected` under a release scope means "nothing on v1.9.0".

        Unlabelled, a quiet release reads as a silent project.
        """
        out = render(
            self._release_payload(
                active=[],
                active_total=0,
                no_work_detected=[line(block="no_work_detected")],
                unassigned_idle_count=3,
            )
        )
        assert "No work detected on v1.9.0" in out
        assert "3 unassigned idle on v1.9.0" in out

    def test_a_quiet_release_does_not_claim_a_quiet_project(self):
        out = render(
            self._release_payload(
                active=[], active_total=0, footer="0 of 0 active shown"
            )
        )
        assert "v1.9.0" in out
        assert "Nothing moved in this window." not in out

    def test_an_unscoped_summary_is_unchanged(self):
        out = render(payload())
        assert "last 3d" in out
        assert "on no release" not in out


class TestNoteHeadingAndEmptiness:
    """The note's date, and the diagnostic it must not suppress."""

    def test_the_heading_matches_the_dashboard_order(self):
        """`9 Aug`, not `Aug 9`.

        Both surfaces render the same field beside the same prose; two orders
        read as two different pieces of data rather than one formatted twice.
        """
        from src.cli.commands.summary import _note_heading

        now = datetime.now(timezone.utc)
        assert _note_heading(now.isoformat()) == f"── Note ({now.day} {now:%b}) ──"

    def test_an_older_year_is_qualified(self):
        """Indefinite inheritance is exactly when a bare day/month misleads."""
        from src.cli.commands.summary import _note_heading

        old = datetime.now(timezone.utc).replace(year=datetime.now().year - 1)
        assert str(old.year) in _note_heading(old.isoformat())

    def test_junk_and_absence_degrade_to_a_plain_heading(self):
        from src.cli.commands.summary import _note_heading

        assert _note_heading(None) == "── Note ──"
        assert _note_heading("garbage") == "── Note ──"

    def test_a_note_is_content_for_rendering(self):
        from src.cli.commands.summary import _is_empty

        assert _is_empty({"active": [], "notes_markdown": None}) is True
        assert _is_empty({"active": [], "notes_markdown": "something"}) is False

    def test_a_note_is_not_work_for_the_identity_diagnostic(self):
        """An inherited note must not hide "your handle is unmapped".

        The note persists across every regeneration, so folding it into one
        emptiness check permanently suppressed the only message that tells an
        unmapped person why their tickets never appear.
        """
        from src.cli.commands.summary import _has_no_work

        assert _has_no_work({"active": [], "notes_markdown": "a month-old note"})
        assert not _has_no_work({"active": [{"ticket_ref": "PF-1"}]})


class TestSummaryRequestParams:
    """What the command actually asks the engine for.

    This is the path that produced the bad summary: the skill shells out to
    `innoday summary --json`, so a release scope that never reaches these
    params never reaches the engine, whatever the MCP tool does.
    """

    def test_a_release_scope_sends_the_release_and_no_window(self):
        """`window_spec` and `release` are two different scopes; sending both
        would leave which one won up to the server to guess."""
        params = _summary_params(window_spec=None, release="current", scrum=True)
        assert params == {"summary_type": "scrum", "release": "current"}

    def test_a_window_scope_sends_the_window_and_no_release(self):
        params = _summary_params(window_spec="3d", release=None, scrum=True)
        assert params == {"summary_type": "scrum", "window_spec": "3d"}

    def test_personal_scope_lets_the_token_say_who_me_is(self):
        params = _summary_params(window_spec="3d", release=None, scrum=False)
        assert params["summary_type"] == "personal"
        assert params["user_id"] == "me"


class TestBoundaryLinePluralisation:
    def test_a_single_in_scope_ticket_reads_as_one(self):
        out = render(
            payload(
                window_spec="release:v1.9.0",
                release="v1.9.0",
                release_ticket_count=1,
                tickets_without_release_count=0,
            )
        )
        assert "the 1 ticket on v1.9.0" in out


class TestSummaryReadsTheContextDirectory:
    """`--dir` is the automation path — the MCP server and scheduled skills run
    from one place and point the CLI at another project's workspace."""

    def test_the_context_directory_reaches_the_label_lookup(self, monkeypatch):
        """`config` honours `--dir`, so `project_ref` is the pointed-at
        project's. Reading the *name* from the cwd meant the two never matched
        under `--dir`, and the header fell back to printing a UUID."""
        import argparse
        import asyncio
        from pathlib import Path

        import src.cli.commands.summary as sm

        seen = {}

        def fake_load(start=None):
            seen["start"] = start
            return {"project_id": "proj-bpai", "project_alias": "BPAI"}

        class Resp:
            status_code = 200
            text = "{}"

            def json(self):
                return {}

        class Client:
            async def __aenter__(self):
                return self

            async def __aexit__(self, *a):
                return False

            async def get(self, path, params=None):
                return Resp()

        class C:
            def get_current_organization(self):
                return "bp"

            def get_organization_id(self, alias):
                return "org-1"

            def get_current_project_id(self):
                return "proj-bpai"

        monkeypatch.setattr(sm, "load_project_context", fake_load)
        monkeypatch.setattr(sm, "InnoDayAPIClient", lambda config: Client())

        args = argparse.Namespace(
            summary_project=None,
            scrum=False,
            summary_json=True,
            format="json",
            window="week",
            dir="/somewhere/bpai",
        )
        rc = asyncio.run(sm.SummaryCommands.execute(args, C()))
        assert rc == 0
        assert seen["start"] == Path("/somewhere/bpai")
