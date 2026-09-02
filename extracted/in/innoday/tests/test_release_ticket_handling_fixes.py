"""
Regressions for the release/ticket handling faults found while planning BPAI
v1.11.0. Each test here corresponds to something that shipped broken and was
observed against a live board, not to a hypothetical.
"""

from datetime import date
from unittest.mock import patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from src.adapters.linear_adapter import LinearBoardAdapter
from src.api.app import app
from src.cli.utils.formatters import OutputFormatter
from src.database import get_session
from src.domain.organization import Organization
from src.domain.project import Project
from src.domain.release import Release, ReleaseStatus
from src.domain.ticket import Ticket, TicketStatus
from src.domain.user import User, UserRole
from src.mcp.server import _note_unapplied_status
from tests.auth_helpers import bearer_for
from tests.db_helpers import build_test_engine


@pytest.fixture
def db_engine():
    return build_test_engine()


@pytest.fixture
def db_session(db_engine):
    with Session(db_engine) as session:
        yield session


@pytest.fixture
def client(db_engine):
    def override_get_session():
        with Session(db_engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    with patch("src.api.app._assert_schema_at_head"):
        with TestClient(app) as c:
            yield c
    app.dependency_overrides.clear()


@pytest.fixture
def org(db_session):
    o = Organization(id=str(uuid4()), name="Test Org")
    db_session.add(o)
    db_session.commit()
    db_session.refresh(o)
    return o


@pytest.fixture
def project(db_session, org):
    p = Project(
        id=str(uuid4()),
        organization_id=org.id,
        alias=f"T{str(uuid4())[:6]}".upper(),
        name="Test Project",
        description="Test project",
    )
    db_session.add(p)
    db_session.commit()
    db_session.refresh(p)
    return p


@pytest.fixture
def auth_headers(db_session, org):
    u = User(
        id=str(uuid4()),
        email=f"{uuid4()}@example.com",
        full_name="Test User",
        role=UserRole.MEMBER,
        is_platform_member=True,
    )
    db_session.add(u)
    db_session.commit()
    return bearer_for(db_session, u.id)


# ---------------------------------------------------------------------------
# The status vocabulary clients were already using
# ---------------------------------------------------------------------------


class TestStatusIsAcceptedInEitherSpelling:
    @pytest.mark.parametrize(
        "sent,expected",
        [
            ("DONE", TicketStatus.DONE),
            ("IN_REVIEW", TicketStatus.IN_REVIEW),
            ("IN_PROGRESS", TicketStatus.IN_PROGRESS),
            ("in-progress", TicketStatus.IN_PROGRESS),
            ("In Progress", TicketStatus.IN_PROGRESS),
            ("  todo  ", TicketStatus.TODO),
            ("in review", TicketStatus.IN_REVIEW),
        ],
    )
    def test_the_member_name_resolves_as_well_as_the_value(self, sent, expected):
        """The MCP server documented the NAMES and posted them raw, so every
        documented value 422'd; the CLI worked only because its HTTP client
        lowercased behind the scenes."""
        assert TicketStatus(sent) is expected

    def test_an_unknown_status_still_fails(self):
        """Leniency about spelling must not become leniency about meaning."""
        with pytest.raises(ValueError):
            TicketStatus("shipped-ish")


# ---------------------------------------------------------------------------
# Outbound board state matching
# ---------------------------------------------------------------------------


def _adapter_with_states(*names):
    a = LinearBoardAdapter.__new__(LinearBoardAdapter)
    a.state_name_to_id = {n: f"id-{n}" for n in names}
    return a


class TestBoardStateNamesThatDoNotMatchLiterally:
    # Bright Power's real Linear workflow.
    BRIGHT_POWER = (
        "In Test",
        "In Progress",
        "Duplicate",
        "Backlog",
        "Internal Review",
        "Todo",
        "Canceled",
        "Done",
    )

    def test_in_review_reaches_a_state_named_internal_review(self):
        """The failure that started this: the transition silently did not happen,
        so a ticket created as IN_REVIEW sat in the board's default Backlog while
        the API answered 200."""
        a = _adapter_with_states(*self.BRIGHT_POWER)
        assert a._state_id_for("in review") == "id-Internal Review"

    def test_a_review_request_prefers_the_review_state_over_in_test(self):
        """Both classify as IN_REVIEW inbound. A board with both means them as
        different steps, so the choice must be stable and must be the review
        one -- not whichever the dict happened to yield first."""
        a = _adapter_with_states(*self.BRIGHT_POWER)
        assert a._state_id_for("in review") == "id-Internal Review"

    def test_done_never_resolves_to_a_cancelled_state(self):
        """Marking somebody's finished ticket Canceled is a wrong fact written to
        a client's board; CANCELLED exists to say that deliberately."""
        a = _adapter_with_states(*self.BRIGHT_POWER)
        assert a._state_id_for("done") == "id-Done"

    def test_done_fails_loudly_rather_than_settling_for_canceled(self):
        a = _adapter_with_states("Backlog", "Todo", "Canceled")
        assert a._state_id_for("done") is None

    def test_cancelled_still_reaches_a_state_spelled_with_one_l(self):
        """Guarding DONE must not strand CANCELLED, whose own spelling differs
        from the board's by a single letter."""
        a = _adapter_with_states(*self.BRIGHT_POWER)
        assert a._state_id_for("cancelled") == "id-Canceled"

    def test_a_board_with_no_matching_state_returns_none(self):
        a = _adapter_with_states("Backlog", "Todo", "Done")
        assert a._state_id_for("in review") is None


# ---------------------------------------------------------------------------
# A status that did not stick is reported
# ---------------------------------------------------------------------------


class TestUnappliedStatusIsSurfaced:
    def test_a_status_the_board_refused_is_reported_to_the_caller(self):
        out = _note_unapplied_status({"id": 1, "status": "backlog"}, "in review")
        assert "warning" in out
        assert "in review" in out["warning"]
        assert "backlog" in out["warning"]

    def test_a_status_that_applied_adds_no_noise(self):
        out = _note_unapplied_status({"id": 1, "status": "in review"}, "IN_REVIEW")
        assert "warning" not in out

    def test_an_error_response_is_passed_through_untouched(self):
        payload = {"error": "API error 422"}
        assert _note_unapplied_status(payload, "done") == payload


# ---------------------------------------------------------------------------
# Release ordering and counts
# ---------------------------------------------------------------------------


class TestReleaseListing:
    def _make(self, db_session, org, project, versions):
        for v in versions:
            db_session.add(
                Release(
                    id=str(uuid4()),
                    organization_id=org.id,
                    project_id=project.id,
                    version=v,
                    status=ReleaseStatus.PLANNED,
                )
            )
        db_session.commit()

    def test_versions_are_ordered_numerically_not_as_strings(
        self, client, db_session, org, project, auth_headers
    ):
        """`ORDER BY version DESC` put v1.9.0 above v1.12.0/v1.11.0/v1.10.0,
        which -- with a default limit of 10 -- hid the version being cut."""
        self._make(
            db_session,
            org,
            project,
            ["v1.9.0", "v1.12.0", "v1.10.0", "v1.11.0", "v1.2.0"],
        )
        resp = client.get(
            f"/api/v1/organizations/{org.id}/releases",
            params={"project_id": project.id},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        assert [r["version"] for r in resp.json()] == [
            "v1.12.0",
            "v1.11.0",
            "v1.10.0",
            "v1.9.0",
            "v1.2.0",
        ]

    def test_a_non_semver_version_is_kept_but_sorts_last(
        self, client, db_session, org, project, auth_headers
    ):
        """BPAI carries a literal 'rancher-FINAL'. It is a real record and must
        not vanish, and must not outrank a real version either."""
        self._make(db_session, org, project, ["v1.1.0", "rancher-FINAL", "v1.2.0"])
        resp = client.get(
            f"/api/v1/organizations/{org.id}/releases",
            params={"project_id": project.id},
            headers=auth_headers,
        )
        versions = [r["version"] for r in resp.json()]
        assert versions == ["v1.2.0", "v1.1.0", "rancher-FINAL"]

    def test_ticket_counts_survive_the_switch_to_one_grouped_query(
        self, client, db_session, org, project, auth_headers
    ):
        """The per-release COUNTs were replaced by a single grouped query because
        88 releases meant ~176 round trips -- and `tickets update --release`
        validates against this list, so one field took ~28s to set."""
        self._make(db_session, org, project, ["v2.0.0", "v2.1.0"])
        for status in (TicketStatus.DONE, TicketStatus.DONE, TicketStatus.TODO):
            db_session.add(
                Ticket(
                    organization_id=org.id,
                    project_id=project.id,
                    release="v2.0.0",
                    summary="t",
                    status=status,
                )
            )
        db_session.commit()

        resp = client.get(
            f"/api/v1/organizations/{org.id}/releases",
            params={"project_id": project.id},
            headers=auth_headers,
        )
        rows = {r["version"]: r for r in resp.json()}
        assert (
            rows["v2.0.0"]["ticket_count"],
            rows["v2.0.0"]["open_ticket_count"],
        ) == (
            3,
            1,
        )
        # A version nothing carries is absent from the grouped result; that must
        # read as zero, not as a missing key.
        assert (
            rows["v2.1.0"]["ticket_count"],
            rows["v2.1.0"]["open_ticket_count"],
        ) == (
            0,
            0,
        )

    def test_counts_do_not_leak_across_projects_sharing_a_version(
        self, client, db_session, org, auth_headers
    ):
        """A version string is unique per project, so the grouped query has to be
        keyed on both. Two projects can each have a v1.9.0."""
        others = []
        for name in ("A", "B"):
            p = Project(
                id=str(uuid4()),
                organization_id=org.id,
                alias=f"{name}{str(uuid4())[:5]}".upper(),
                name=name,
                description="d",
            )
            db_session.add(p)
            others.append(p)
        db_session.commit()
        for p, n in zip(others, (2, 1)):
            db_session.add(
                Release(
                    id=str(uuid4()),
                    organization_id=org.id,
                    project_id=p.id,
                    version="v1.9.0",
                    status=ReleaseStatus.PLANNED,
                )
            )
            for _ in range(n):
                db_session.add(
                    Ticket(
                        organization_id=org.id,
                        project_id=p.id,
                        release="v1.9.0",
                        summary="t",
                        status=TicketStatus.TODO,
                    )
                )
        db_session.commit()

        counts = {}
        for p in others:
            resp = client.get(
                f"/api/v1/organizations/{org.id}/releases",
                params={"project_id": p.id},
                headers=auth_headers,
            )
            counts[p.name] = resp.json()[0]["ticket_count"]
        assert counts == {"A": 2, "B": 1}


# ---------------------------------------------------------------------------
# target_date
# ---------------------------------------------------------------------------


class TestTargetDateOnCreate:
    def test_a_target_date_given_at_create_is_persisted(
        self, client, db_session, org, project, auth_headers
    ):
        """`ReleaseCreate` accepted the field and the constructor never read it,
        so a create answered 201 with the date silently dropped."""
        resp = client.post(
            f"/api/v1/organizations/{org.id}/releases",
            json={
                "version": "v3.0.0",
                "project_id": project.id,
                "target_date": "2026-08-21",
            },
            headers=auth_headers,
        )
        assert resp.status_code == 201, resp.text
        assert resp.json()["target_date"] == "2026-08-21"

        stored = db_session.get(Release, resp.json()["id"])
        db_session.refresh(stored)
        assert stored.target_date == date(2026, 8, 21)


# ---------------------------------------------------------------------------
# Release config without a release_configs block
# ---------------------------------------------------------------------------


class TestTheReleaseTargetComesFromInnoDay:
    """Reading the GitHub org and topics out of `project.yml` is superseded.

    That fallback was right about the important thing -- **everything blastoff
    needs is already recorded against the org and the project**, so refusing to
    release over a missing `release_configs` section was refusing over a
    formatting detail while the values sat two lines away.

    It read them from the *generated copy*. They are now read from the source:
    `/onboarding/resolve`, the same answer `innoday init` uses to write that
    copy in the first place. One place to be wrong instead of two, and a
    workspace whose file predates a change stops mattering.
    """

    def test_the_file_reader_is_gone(self):
        import src.cli.commands.release_proxy as proxy

        assert not hasattr(proxy, "_load_release_config")
        assert hasattr(proxy, "_resolve_release_target")


class TestTicketPanelRendering:
    def _render(self, ticket):
        formatter = OutputFormatter()
        with formatter.console.capture() as cap:
            formatter.format_ticket(ticket)
        return cap.get()

    def test_the_panel_renders_fields_and_not_a_python_repr(self):
        """The f-string called str() on a Rich Table, so every `tickets show`
        and `tickets create` printed '<rich.table.Table object at 0x...>' where
        the ticket's fields belonged."""
        out = self._render(
            {"id": 1428, "status": "done", "summary": "A ticket", "release": "v1.11.0"}
        )
        assert "rich.table.Table object" not in out
        assert "1428" in out

    def test_the_panel_shows_the_release_and_the_board_key(self):
        """Both were absent: you could set --release and had no way to read it
        back, and the board key you had in hand was never the id on screen."""
        out = self._render(
            {
                "id": 1428,
                "external_ticket_id": "BPAI-417",
                "status": "done",
                "summary": "A ticket",
                "release": "v1.11.0",
            }
        )
        assert "BPAI-417" in out
        assert "v1.11.0" in out

    def test_an_unplanned_ticket_says_so_rather_than_showing_nothing(self):
        out = self._render({"id": 9, "status": "todo", "summary": "Bare"})
        assert "Not planned" in out


class TestTopicProbingIsNoLongerNeeded:
    """The probe asked GitHub which *one* topic to release by. Nothing has to
    choose any more, because every topic is passed and any of them matches.

    **The finding that motivated the probe is real and still worth recording.**
    A project's topics are not ranked: BPAI lists `bpai,bp-ai,brightpower` and
    *nothing* carries `bpai` while 9 repos carry `bp-ai`; PF lists `pf,pixelfuel`
    where `pixelfuel` has 9 and `pf` has 1. Picking positionally resolved a
    valid-looking release against an empty repo set and reported "0 repos" --
    a wrong answer dressed as a normal one.

    Passing the whole list removes the question rather than answering it. An
    empty topic contributes nothing, so `bpai` is harmless; and a repo carrying
    only `pf` now joins PF's release, which is what InnoDay already considers it
    part of. That is a deliberate widening -- see the PR.
    """

    def test_the_probe_is_gone(self):
        import src.cli.commands.release_proxy as proxy

        assert not hasattr(proxy, "_topic_with_repos"), (
            "the probe is back. If a single topic has to be chosen again, the "
            "list is not reaching the engine."
        )

    def test_an_empty_topic_costs_nothing(self):
        """`bpai` matches no repo. In a union that is simply not a contribution,
        which is why nothing needs to detect and drop it."""
        from blastoff.api.github_api import GithubOrgApi

        api = GithubOrgApi.__new__(GithubOrgApi)
        api.list_repos = lambda: [
            {
                "name": "one",
                "description": "",
                "language": "Python",
                "size": 1,
                "topics": ["bp-ai"],
                "archived": False,
                "disabled": False,
                "visibility": "private",
                "created_at": "",
                "updated_at": "",
                "url": "",
                "ssh_url": "",
            }
        ]
        found = api.list_repos_for_topic(["bpai", "bp-ai", "brightpower"], quiet=True)
        assert [r.name for r in found] == ["one"]


class TestStatusVocabularyIsDerived:
    def test_the_mcp_create_default_is_a_status_the_api_accepts(self):
        """A tool whose default argument is rejected by its own API fails on the
        simplest call it has. A `default=` is never validated client-side, which
        is how an invalid "TODO" survived there."""
        import inspect

        from src.mcp.server import create_ticket

        fn = getattr(create_ticket, "fn", create_ticket)
        default = inspect.signature(fn).parameters["status"].default.default
        assert TicketStatus(default) is TicketStatus.TODO
        # Specifically the enum's own value, so it is valid without relying on
        # the leniency added elsewhere.
        assert default == TicketStatus.TODO.value

    def test_the_cli_offers_every_member_and_nothing_stale(self):
        from src.cli.commands.tickets import STATUS_CHOICES

        for status in TicketStatus:
            assert status.name in STATUS_CHOICES
            assert status.value in STATUS_CHOICES
        # Nothing in the list that the enum does not recognise.
        for choice in STATUS_CHOICES:
            TicketStatus(choice)

    def test_the_mcp_description_lists_every_member(self):
        from src.mcp.server import _STATUS_NAMES

        for status in TicketStatus:
            assert status.name in _STATUS_NAMES

    def test_no_module_restates_the_vocabulary_by_hand(self):
        """The drift guard. Written-out lists are what #630 was; a member added to
        the enum must not be able to leave a description behind."""
        import pathlib

        # `src/domain/ticket.py` is where the enum lives, and its `_missing_`
        # docstring quotes the member names to explain the bug. Naming them there
        # is the point; restating them as a *declaration* anywhere else is the
        # fault. Everything else in src/ is fair game for this guard.
        allowed = {pathlib.Path("src/domain/ticket.py")}

        offenders = []
        for path in pathlib.Path("src").rglob("*.py"):
            if path in allowed:
                continue
            for i, line in enumerate(path.read_text().splitlines(), 1):
                if "DRAFT, BACKLOG, TODO, IN_PROGRESS" in line:
                    offenders.append(f"{path}:{i}")
        assert offenders == [], f"hand-written status vocabulary at {offenders}"


# ---------------------------------------------------------------------------
# A board key works wherever the numeric id does
# ---------------------------------------------------------------------------


class TestTicketRefResolution:
    def _ticket(self, db_session, org, project, key, **kw):
        t = Ticket(
            organization_id=org.id,
            project_id=project.id,
            summary="t",
            status=TicketStatus.TODO,
            external_ticket_id=key,
            **kw,
        )
        db_session.add(t)
        db_session.commit()
        db_session.refresh(t)
        return t

    def test_a_numeric_ref_is_an_id_and_needs_no_lookup(self, db_session, org):
        from src.middleware.rbac import resolve_ticket_ref

        assert resolve_ticket_ref("1380", org.id, db_session) == 1380

    def test_a_board_key_resolves_to_the_ticket_id(self, db_session, org, project):
        """The id a person has in hand is the board's, never InnoDay's."""
        from src.middleware.rbac import resolve_ticket_ref

        t = self._ticket(db_session, org, project, "BPAI-402")
        assert resolve_ticket_ref("BPAI-402", org.id, db_session) == t.id

    def test_a_board_key_is_matched_case_insensitively(self, db_session, org, project):
        """The same issue is BPAI-402 in Linear and bpai-402 in a branch name."""
        from src.middleware.rbac import resolve_ticket_ref

        t = self._ticket(db_session, org, project, "BPAI-402")
        assert resolve_ticket_ref("bpai-402", org.id, db_session) == t.id

    def test_an_unknown_key_is_a_404(self, db_session, org):
        from fastapi import HTTPException

        from src.middleware.rbac import resolve_ticket_ref

        with pytest.raises(HTTPException) as e:
            resolve_ticket_ref("NOPE-1", org.id, db_session)
        assert e.value.status_code == 404

    def test_a_soft_deleted_ticket_does_not_answer_for_its_key(
        self, db_session, org, project
    ):
        """A cancelled row must not be acted on in place of a live one."""
        from datetime import datetime

        from fastapi import HTTPException

        from src.middleware.rbac import resolve_ticket_ref

        self._ticket(
            db_session, org, project, "BPAI-999", deleted_at=datetime(2026, 1, 1)
        )
        with pytest.raises(HTTPException) as e:
            resolve_ticket_ref("BPAI-999", org.id, db_session)
        assert e.value.status_code == 404

    def test_an_ambiguous_key_is_refused_rather_than_guessed(
        self, db_session, org, project
    ):
        """A board key is unique per board, not per org: two boards in one org can
        both carry an ABC-1. Acting on whichever row came back first would be a
        write to the wrong ticket."""
        from fastapi import HTTPException

        from src.middleware.rbac import resolve_ticket_ref

        self._ticket(db_session, org, project, "ABC-1")
        self._ticket(db_session, org, project, "ABC-1")
        with pytest.raises(HTTPException) as e:
            resolve_ticket_ref("ABC-1", org.id, db_session)
        assert e.value.status_code == 409

    def test_a_route_accepts_the_board_key_end_to_end(
        self, client, db_session, org, project, auth_headers
    ):
        """Normalised in the guard, so handlers keep `ticket_id: int` unchanged --
        this is the test that pins the ordering that makes that work."""
        t = self._ticket(db_session, org, project, "BPAI-402")
        resp = client.get(
            f"/api/v1/organizations/{org.id}/tickets/BPAI-402", headers=auth_headers
        )
        assert resp.status_code == 200, resp.text
        assert resp.json()["id"] == t.id

    def test_a_route_still_accepts_the_numeric_id(
        self, client, db_session, org, project, auth_headers
    ):
        t = self._ticket(db_session, org, project, "BPAI-403")
        resp = client.get(
            f"/api/v1/organizations/{org.id}/tickets/{t.id}", headers=auth_headers
        )
        assert resp.status_code == 200, resp.text
        assert resp.json()["external_ticket_id"] == "BPAI-403"


# ---------------------------------------------------------------------------
# The CLI takes the ticket positionally
# ---------------------------------------------------------------------------


class TestTicketIdArgumentShape:
    def _parse(self, argv):
        import argparse

        from src.cli.commands.tickets import TicketCommands

        p = argparse.ArgumentParser()
        # setup_parser adds the subparsers itself; adding our own first raises
        # "cannot have multiple subparser arguments".
        TicketCommands.setup_parser(p)
        return p.parse_args(argv)

    def test_the_ticket_is_positional(self):
        """`innoday tickets show 1416` used to exit with a usage error, because
        the id was a required flag on six subcommands while cancel/delete took it
        positionally."""
        assert self._parse(["show", "1416"]).ticket == "1416"

    def test_a_board_key_is_accepted_positionally(self):
        assert self._parse(["show", "BPAI-402"]).ticket == "BPAI-402"

    def test_the_deprecated_flag_still_works(self):
        """Scripts and skills in other repos already pass it."""
        ns = self._parse(["show", "--ticket-id", "1416"])
        assert ns.ticket is None and ns.ticket_id_flag == "1416"

    def test_a_second_positional_still_binds_correctly(self):
        """`assign` and `comment` already had a positional; an optional one in
        front of a required one is the ambiguous case worth pinning."""
        ns = self._parse(["assign", "BPAI-402", "alice"])
        assert (ns.ticket, ns.assignee) == ("BPAI-402", "alice")

    def test_the_flag_form_of_assign_is_unchanged(self):
        ns = self._parse(["assign", "alice", "--ticket-id", "1380"])
        assert (ns.ticket, ns.assignee, ns.ticket_id_flag) == (None, "alice", "1380")


class TestTargetDateCanBeClearedAndPreserved:
    """`--target-date ""` is documented as clearing the date. That relies on the
    CLI sending an explicit null and on `exclude_unset` keeping it -- worth
    pinning, because "omitted" and "explicitly null" are one keystroke apart and
    must not behave the same."""

    def _release(self, client, org, project, auth_headers, target):
        return client.post(
            f"/api/v1/organizations/{org.id}/releases",
            json={"version": "v7.0.0", "project_id": project.id, "target_date": target},
            headers=auth_headers,
        )

    def test_an_explicit_null_clears_the_date(self, client, org, project, auth_headers):
        created = self._release(client, org, project, auth_headers, "2026-08-21")
        assert created.json()["target_date"] == "2026-08-21"

        resp = client.patch(
            f"/api/v1/organizations/{org.id}/releases/{created.json()['id']}",
            json={"target_date": None},
            headers=auth_headers,
        )
        assert resp.status_code == 200, resp.text
        assert resp.json()["target_date"] is None

    def test_omitting_the_field_leaves_the_date_alone(
        self, client, org, project, auth_headers
    ):
        created = self._release(client, org, project, auth_headers, "2026-08-21")
        resp = client.patch(
            f"/api/v1/organizations/{org.id}/releases/{created.json()['id']}",
            json={"notes": "unrelated edit"},
            headers=auth_headers,
        )
        assert resp.status_code == 200, resp.text
        assert resp.json()["target_date"] == "2026-08-21"

    def test_the_cli_sends_null_for_an_empty_string(self):
        """The CLI half of the same contract: `--target-date ""` must reach the
        API as a set-but-null field, not be dropped by truthiness."""
        import argparse

        from src.cli.commands.releases import ReleasesCommands

        args = argparse.Namespace(target_date="")
        assert ReleasesCommands._build_release_body(args) == {"target_date": None}

    def test_the_cli_omits_the_field_when_the_flag_is_absent(self):
        import argparse

        from src.cli.commands.releases import ReleasesCommands

        assert "target_date" not in ReleasesCommands._build_release_body(
            argparse.Namespace()
        )


class TestReleaseHonoursTheContextDirectory:
    """`--dir` is the automation path: the MCP server, cron jobs and skills like
    `innoday:morning-sync` run from one place and point the CLI at another
    project's workspace. A human would `cd` and never see this; an agent hits it
    every time."""

    def _resolve(self, monkeypatch, context_dir):
        import argparse
        import asyncio

        import src.cli.commands.release_proxy as proxy

        seen = {}

        def fake_load(start=None):
            seen["start"] = start
            return {"org_alias": "bp", "project_alias": "BPAI"}

        async def fake_target(config, org_ref, project_ref):
            seen["org_ref"] = org_ref
            seen["project_ref"] = project_ref
            return ("BPAI", "havilandsoftware", ["bpai", "bp-ai"])

        monkeypatch.setattr(proxy, "load_project_context", fake_load)
        monkeypatch.setattr(proxy, "_resolve_release_target", fake_target)
        monkeypatch.setattr(proxy, "_resolve_org_id", lambda config: "org-uuid")

        class Config:
            def get_current_project_id(self):
                return "project-uuid"

            def get_current_organization(self):
                return "hs"

        args = argparse.Namespace(dir=context_dir, github_org=None, topics=None)
        result = asyncio.run(
            proxy.ReleaseProxyCommands._resolve_context(args, Config())
        )
        return result, seen

    def test_the_context_directory_reaches_the_project_lookup(self, monkeypatch):
        """org_id/project_id came from `config`, which honours --dir, while the
        aliases driving topic and repo discovery were read from the cwd. That
        split one release across two projects: `innoday --dir <bpai> release`
        reported PF's topics and PF's nine repos carrying BPAI's version and
        BPAI's ticket picture."""
        from pathlib import Path

        result, seen = self._resolve(monkeypatch, "/somewhere/bpai")
        assert seen["start"] == Path("/somewhere/bpai")
        assert result is not None
        assert result[3] == ["bpai", "bp-ai"]

    def test_no_context_directory_still_means_the_cwd(self, monkeypatch):
        """Passing None keeps `load_project_context`'s own default, so the
        ordinary `cd`-into-the-workspace path is untouched."""
        _, seen = self._resolve(monkeypatch, None)
        assert seen["start"] is None
