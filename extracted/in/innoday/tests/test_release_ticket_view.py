"""A release expressed as tickets, which is how a person reads one.

The payload used to be organised by repository, because that is how GitHub is
organised. Nobody outside the team thinks in repositories: one change routinely
spans three, and one repository routinely holds four unrelated changes. So a
release summary built from it could not lead with the ticket, could not say
whether a ticket had actually landed, and could not credit anybody.

It also could not see two whole categories of problem -- a ticket on the release
with no code, and code that shipped naming a ticket that is not on the release.
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest
from sqlmodel import Session

from src.domain.organization import Organization, OrganizationMembership
from src.domain.project import Project, ProjectRepository, RepositoryLayer
from src.domain.release import Release, ReleaseStatus
from src.domain.repository import Repository
from src.domain.summary import Summary, SummaryItem, SummaryType
from src.domain.ticket import Ticket, TicketStatus
from src.domain.user import User
from src.services.release_content import ReleaseContentService
from tests.db_helpers import build_test_engine

NOW = datetime(2026, 8, 21, tzinfo=timezone.utc)
SINCE = NOW - timedelta(days=30)
VERSION = "v1.11.0"


def _pr(number, title, *, branch, merged=True, author="kengsc", body=None):
    return {
        "body": body,
        "number": number,
        "title": title,
        "merged_at": "2026-08-10T00:00:00Z" if merged else None,
        "state": "closed" if merged else "open",
        "user": {"login": author},
        "head": {"ref": branch},
        "html_url": f"https://github.com/acme/r/pull/{number}",
    }


class _Api:
    def __init__(self, by_repo):
        self._by_repo = by_repo

    async def list_pull_requests(
        self, owner, name, state="all", since=None, max_pages=10
    ):
        prs = self._by_repo.get(name, [])
        if state == "open":
            return [p for p in prs if p["state"] == "open"], False
        if state == "closed":
            return [p for p in prs if p["state"] != "open"], False
        return list(prs), False

    async def count_commits(self, owner, name, since=None, until=None):
        return len(self._by_repo.get(name, []))


@pytest.fixture
def world():
    engine = build_test_engine()
    with Session(engine) as session:
        org = Organization(id=str(uuid4()), name="Acme", alias=f"a{str(uuid4())[:5]}")
        session.add(org)
        project = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias="BPAI",
            name="Bright Power",
            description="d",
        )
        session.add(project)
        session.commit()
        yield session, org, project


def _repo(session, org, project, name, layer=RepositoryLayer.API):
    repo = Repository(
        id=str(uuid4()),
        organization_id=org.id,
        name=name,
        full_name=f"acme/{name}",
        url=f"https://github.com/acme/{name}",
    )
    session.add(repo)
    session.add(
        ProjectRepository(
            id=str(uuid4()),
            project_id=project.id,
            repository_id=repo.id,
            layer=layer,
        )
    )
    session.commit()
    return repo


def _ticket(
    session,
    org,
    project,
    *,
    key,
    summary,
    status=TicketStatus.DONE,
    release=VERSION,
    number=None,
    assigned_to=None,
    assignee=None,
):
    t = Ticket(
        organization_id=org.id,
        project_id=project.id,
        summary=summary,
        status=status,
        release=release,
        external_ticket_id=key,
        project_ref_number=number,
        url=f"https://linear.app/bp/issue/{key}" if key else None,
        assigned_to=assigned_to,
        assignee=assignee,
    )
    session.add(t)
    session.commit()
    session.refresh(t)
    return t


def _assemble(session, org, project, by_repo, version=VERSION):
    svc = ReleaseContentService(session, client_factory=lambda _o: _Api(by_repo))
    return asyncio.run(
        svc.assemble(
            project=project,
            organization_id=org.id,
            since=SINCE,
            window_label="since v1.10.0",
            version=version,
        )
    )


class TestTheTicketIsTheUnit:
    def test_a_shipped_ticket_carries_its_pull_request(self, world):
        session, org, project = world
        _repo(session, org, project, "bps-api")
        _ticket(session, org, project, key="BPAI-402", summary="Jurisdiction first")

        content = _assemble(
            session,
            org,
            project,
            {"bps-api": [_pr(11, "fix it", branch="BPAI-402-jurisdiction")]},
        )
        item = content["items"][0]
        assert item["ref"] == "BPAI-402"
        assert item["state"] == "shipped"
        assert [p["number"] for p in item["prs"]] == [11]
        assert item["gaps"] == []

    def test_both_names_are_carried(self, world):
        """The board key leads and the InnoDay number travels with it.

        They format identically and name different tickets often enough that
        keeping only one loses the link between InnoDay's own surfaces and the
        board a customer reads.
        """
        session, org, project = world
        _repo(session, org, project, "bps-api")
        _ticket(session, org, project, key="BPAI-402", summary="x", number=7)

        item = _assemble(session, org, project, {"bps-api": []})["items"][0]
        assert item["ref"] == "BPAI-402"
        assert item["board_ref"] == "BPAI-402"
        assert item["innoday_ref"] == "BPAI-7"
        assert item["url"].endswith("/BPAI-402")


class TestGapsAreReportedNotHidden:
    def test_a_ticket_with_no_code_appears_at_all(self, world):
        """Previously invisible: the payload was built from pull requests."""
        session, org, project = world
        _repo(session, org, project, "bps-api")
        _ticket(session, org, project, key="BPAI-500", summary="nothing written")

        item = _assemble(session, org, project, {"bps-api": []})["items"][0]
        assert item["state"] == "no_code"
        assert [g["kind"] for g in item["gaps"]] == ["no_code", "unattributed"]
        assert all(g["remedy"] for g in item["gaps"])

    def test_an_open_pull_request_is_not_merged(self, world):
        session, org, project = world
        _repo(session, org, project, "bps-api")
        _ticket(
            session,
            org,
            project,
            key="BPAI-411",
            summary="in flight",
            status=TicketStatus.IN_PROGRESS,
        )

        content = _assemble(
            session,
            org,
            project,
            {"bps-api": [_pr(9, "wip", branch="BPAI-411-x", merged=False)]},
        )
        item = content["items"][0]
        assert item["state"] == "not_merged"
        assert "not_merged" in [g["kind"] for g in item["gaps"]]

    def test_merged_code_on_a_todo_ticket_is_a_gap(self, world):
        session, org, project = world
        _repo(session, org, project, "bps-api")
        _ticket(
            session,
            org,
            project,
            key="BPAI-333",
            summary="shipped but open",
            status=TicketStatus.TODO,
        )

        content = _assemble(
            session,
            org,
            project,
            {"bps-api": [_pr(3, "done", branch="BPAI-333-y")]},
        )
        assert "status_behind" in [g["kind"] for g in content["items"][0]["gaps"]]

    def test_in_review_counts_as_finished(self, world):
        """There is no TEST status -- Linear's "in test" normalises to IN_REVIEW."""
        session, org, project = world
        _repo(session, org, project, "bps-api")
        _ticket(
            session,
            org,
            project,
            key="BPAI-334",
            summary="in test",
            status=TicketStatus.IN_REVIEW,
        )

        content = _assemble(
            session,
            org,
            project,
            {"bps-api": [_pr(4, "done", branch="BPAI-334-z")]},
        )
        kinds = [g["kind"] for g in content["items"][0]["gaps"]]
        assert "status_behind" not in kinds


class TestWorkThatShippedWithoutBeingOnTheRelease:
    def test_it_is_reported_as_mis_tagged(self, world):
        """The category nothing could see before.

        A pull request merged in the window, naming a ticket that is on some
        other release. That is shipped work missing from the notes.
        """
        session, org, project = world
        _repo(session, org, project, "bps-api")
        _ticket(
            session,
            org,
            project,
            key="BPAI-900",
            summary="other release",
            release="v1.9.0",
        )

        content = _assemble(
            session,
            org,
            project,
            {"bps-api": [_pr(5, "shipped", branch="BPAI-900-a")]},
        )
        shipped_off = [
            r for r in content["off_release"] if r["state"] == "shipped_untagged"
        ]
        assert [r["ref"] for r in shipped_off] == ["BPAI-900"]
        assert "v1.11.0" in shipped_off[0]["remedy"]
        # **The id, not only the command that quotes it.** A caller that is not a
        # shell cannot act on `--ticket-id 1422` in a sentence, so a UI offering
        # to attach the ticket had nothing to send. `items` has always carried
        # this; these are the same tickets seen from the other side.
        assert shipped_off[0]["ticket_id"] is not None

    def test_a_pull_request_naming_nothing_is_unticketed(self, world):
        session, org, project = world
        _repo(session, org, project, "bps-api")
        content = _assemble(
            session, org, project, {"bps-api": [_pr(6, "tidy up", branch="patch-1")]}
        )
        assert [p["number"] for p in content["unticketed"]] == [6]


class TestDesignWorkIsSectioned:
    def test_a_design_repository_goes_to_its_own_bucket(self, world):
        session, org, project = world
        _repo(session, org, project, "bps-api")
        _repo(session, org, project, "bps-ui-demo", layer=RepositoryLayer.DESIGN)

        content = _assemble(
            session,
            org,
            project,
            {
                "bps-api": [_pr(1, "real", branch="patch-1")],
                "bps-ui-demo": [_pr(30, "layout", branch="patch-2")],
            },
        )
        assert [p["number"] for p in content["design"]["unticketed"]] == [30]
        assert [p["number"] for p in content["unticketed"]] == [1]

    def test_it_is_still_in_the_tag_set(self, world):
        """Sectioned in the story, not removed from the release."""
        session, org, project = world
        _repo(session, org, project, "bps-ui-demo", layer=RepositoryLayer.DESIGN)
        content = _assemble(session, org, project, {"bps-ui-demo": []})
        assert content["repos"] == ["bps-ui-demo"]

    def test_a_design_ticket_keeps_its_code(self, world):
        """The bug the live run found.

        Skipping design repositories in the join meant a ticket whose work is
        *entirely* design -- "Design Small UI Items" -- reported `no_code`, a
        gap to go and chase that was really seventeen merged pull requests one
        bucket away.
        """
        session, org, project = world
        _repo(session, org, project, "bps-ui-demo", layer=RepositoryLayer.DESIGN)
        _ticket(session, org, project, key="BPAI-379", summary="Design Small UI Items")

        content = _assemble(
            session,
            org,
            project,
            {"bps-ui-demo": [_pr(31, "layout", branch="BPAI-379-a")]},
        )
        assert content["items"] == []
        design_item = content["design"]["items"][0]
        assert design_item["ref"] == "BPAI-379"
        assert design_item["state"] == "shipped"
        assert "no_code" not in [g["kind"] for g in design_item["gaps"]]

    def test_a_ticket_with_no_code_is_not_design_work(self, world):
        """`is_design` needs pull requests to be true of.

        Otherwise every unstarted ticket would be filed as design and vanish
        from the part of the summary that chases gaps.
        """
        session, org, project = world
        _repo(session, org, project, "bps-ui-demo", layer=RepositoryLayer.DESIGN)
        _ticket(session, org, project, key="BPAI-500", summary="nothing yet")
        content = _assemble(session, org, project, {"bps-ui-demo": []})
        assert [i["ref"] for i in content["items"]] == ["BPAI-500"]
        assert content["design"]["items"] == []

    def test_a_ticket_spanning_both_is_not_design_work(self, world):
        """One real pull request makes it real work, narrated with the rest."""
        session, org, project = world
        _repo(session, org, project, "bps-api")
        _repo(session, org, project, "bps-ui-demo", layer=RepositoryLayer.DESIGN)
        _ticket(session, org, project, key="BPAI-411", summary="both")

        content = _assemble(
            session,
            org,
            project,
            {
                "bps-api": [_pr(1, "api", branch="BPAI-411-a")],
                "bps-ui-demo": [_pr(2, "mock", branch="BPAI-411-b")],
            },
        )
        assert [i["ref"] for i in content["items"]] == ["BPAI-411"]
        assert content["design"]["items"] == []


class TestPeopleNotHandles:
    def test_a_mapped_login_becomes_a_name(self, world):
        session, org, project = world
        user = User(
            id=str(uuid4()),
            email="ken@havilandsoftware.com",
            full_name="Ken Smith",
            github_username="kengsc",
        )
        session.add(user)
        session.add(
            OrganizationMembership(
                id=str(uuid4()), user_id=user.id, organization_id=org.id, is_active=True
            )
        )
        session.commit()
        _repo(session, org, project, "bps-api")
        _ticket(session, org, project, key="BPAI-402", summary="x")

        content = _assemble(
            session,
            org,
            project,
            {"bps-api": [_pr(11, "fix", branch="BPAI-402-a", author="kengsc")]},
        )
        assert content["items"][0]["people"] == ["Ken S."]

    def test_an_unmapped_login_is_still_credited(self, world):
        """Dropping the credit would hide that the mapping is missing."""
        session, org, project = world
        _repo(session, org, project, "bps-api")
        _ticket(session, org, project, key="BPAI-402", summary="x")

        content = _assemble(
            session,
            org,
            project,
            {"bps-api": [_pr(11, "fix", branch="BPAI-402-a", author="nobody")]},
        )
        assert content["items"][0]["people"] == ["nobody"]

    def test_nobody_at_all_is_a_gap(self, world):
        session, org, project = world
        _repo(session, org, project, "bps-api")
        _ticket(session, org, project, key="BPAI-402", summary="x")
        content = _assemble(session, org, project, {"bps-api": []})
        assert "unattributed" in [g["kind"] for g in content["items"][0]["gaps"]]


class TestTotals:
    def test_complete_counts_only_tickets_with_no_gaps(self, world):
        session, org, project = world
        _repo(session, org, project, "bps-api")
        user = User(
            id=str(uuid4()),
            email="k@x.com",
            full_name="Ken Smith",
            github_username="kengsc",
        )
        session.add(user)
        session.add(
            OrganizationMembership(
                id=str(uuid4()), user_id=user.id, organization_id=org.id, is_active=True
            )
        )
        session.commit()
        _ticket(session, org, project, key="BPAI-1", summary="good")
        _ticket(session, org, project, key="BPAI-2", summary="bad")

        content = _assemble(
            session,
            org,
            project,
            {"bps-api": [_pr(1, "fix", branch="BPAI-1-a", author="kengsc")]},
        )
        assert content["totals"]["tickets"] == 2
        assert content["totals"]["complete"] == 1
        assert content["totals"]["with_gaps"] == 1


class TestAHandMadeAttachmentWins:
    """The confirmation half of the proposal loop.

    Ten of thirty-four merged pull requests on a real release named their ticket
    in no branch, title or description. `fix/roi-multiplier-null` is plainly
    "Stop showing a 0.0x return when a scenario loses money" and says so
    nowhere. Nothing infers that; a person confirms it, and the confirmation is
    what this reads.
    """

    def _attach(self, session, repo_id, number, ticket_id):
        from src.domain.repository_pull_request import RepositoryPullRequest

        session.add(
            RepositoryPullRequest(
                repository_id=repo_id,
                number=number,
                title="",
                url=f"https://github.com/acme/r/pull/{number}",
                state="closed",
                ticket_id=ticket_id,
            )
        )
        session.commit()

    def test_an_attached_pull_request_lands_on_its_ticket(self, world):
        session, org, project = world
        repo = _repo(session, org, project, "bps-api")
        ticket = _ticket(session, org, project, key="BPAI-417", summary="0.0x return")
        self._attach(session, repo.id, 600, ticket.id)

        content = _assemble(
            session,
            org,
            project,
            {
                "bps-api": [
                    _pr(600, "fix(v2): baseline ROI multiplier", branch="fix/roi")
                ]
            },
        )
        item = content["items"][0]
        assert [p["number"] for p in item["prs"]] == [600]
        assert item["prs"][0]["matched_by"] == "manual"
        assert content["unticketed"] == []

    def test_it_overrules_what_the_branch_says(self, world):
        """A person who attached a pull request has said something the branch did not.

        No amount of pattern matching should be able to overrule that -- it is
        the only signal in the system that somebody actually looked.
        """
        session, org, project = world
        repo = _repo(session, org, project, "bps-api")
        _ticket(session, org, project, key="BPAI-100", summary="what the branch says")
        meant = _ticket(
            session, org, project, key="BPAI-200", summary="what a person said"
        )
        self._attach(session, repo.id, 7, meant.id)

        content = _assemble(
            session,
            org,
            project,
            {"bps-api": [_pr(7, "x", branch="BPAI-100-work")]},
        )
        landed = {i["ref"]: [p["number"] for p in i["prs"]] for i in content["items"]}
        assert landed["BPAI-200"] == [7]
        assert landed["BPAI-100"] == []


class TestHowAMatchWasFoundIsRecorded:
    """The three sources are not equally trustworthy, so the payload says which.

    A branch reference is a deliberate act. A reference found in a description
    may be a passing mention that happened to be the only one. A summary should
    be able to hedge accordingly rather than asserting every match alike.
    """

    def test_a_branch_match_says_branch(self, world):
        session, org, project = world
        _repo(session, org, project, "bps-api")
        _ticket(session, org, project, key="BPAI-402", summary="x")
        content = _assemble(
            session,
            org,
            project,
            {"bps-api": [_pr(1, "anything", branch="BPAI-402-work")]},
        )
        assert content["items"][0]["prs"][0]["matched_by"] == "branch"

    def test_a_body_match_says_body(self, world):
        session, org, project = world
        _repo(session, org, project, "bps-api")
        _ticket(session, org, project, key="BPAI-414", summary="x")
        content = _assemble(
            session,
            org,
            project,
            {
                "bps-api": [
                    _pr(
                        2,
                        "Label updates",
                        branch="labels",
                        body="Implements BPAI-414 label changes",
                    )
                ]
            },
        )
        assert content["items"][0]["prs"][0]["matched_by"] == "body"


class TestCandidateTickets:
    """The other direction of the loop.

    "Implement Small UI Items v1.11.0" sat In Test, on no release, while four of
    its checklist items merged inside the window -- and a payload built from
    pull requests could never mention it, because it only sees tickets that pull
    requests point at.
    """

    def test_started_work_on_no_release_is_offered(self, world):
        session, org, project = world
        _repo(session, org, project, "bps-api")
        _ticket(
            session,
            org,
            project,
            key="BPAI-407",
            summary="Implement Small UI Items",
            status=TicketStatus.IN_REVIEW,
            release=None,
        )
        content = _assemble(session, org, project, {"bps-api": []})
        assert [c["ref"] for c in content["off_release"]] == ["BPAI-407"]
        assert content["off_release"][0]["state"] == "started_untagged"
        assert "v1.11.0" in content["off_release"][0]["remedy"]
        # Both kinds of off-release row are actionable, not just the loud one.
        assert content["off_release"][0]["ticket_id"] is not None

    def test_a_ticket_already_on_the_release_is_not_a_candidate(self, world):
        session, org, project = world
        _repo(session, org, project, "bps-api")
        _ticket(
            session,
            org,
            project,
            key="BPAI-402",
            summary="x",
            status=TicketStatus.IN_REVIEW,
        )
        assert _assemble(session, org, project, {"bps-api": []})["off_release"] == []

    def test_the_backlog_is_not_a_list_of_candidates(self, world):
        """Two hundred planned tickets is noise, not a suggestion."""
        session, org, project = world
        _repo(session, org, project, "bps-api")
        _ticket(
            session,
            org,
            project,
            key="BPAI-900",
            summary="someday",
            status=TicketStatus.TODO,
            release=None,
        )
        assert _assemble(session, org, project, {"bps-api": []})["off_release"] == []


class TestEveryOffReleaseTicketGetsAVerdictToo:
    """ "In Test, on no release, with code merged to main" is a state.

    It was being reported as a flat entry in a list of fifteen, next to tickets
    where nothing had happened at all — so the single loudest thing a release
    report can say, *this shipped and is not in your release*, read exactly like
    *this might belong here one day*.

    BPAI-407 is the real one: title says v1.11.0, release field says Not
    planned, status In Test, and its checklist matches merged work in the
    window.
    """

    def test_merged_work_on_an_untagged_ticket_is_shipped_untagged(self, world):
        session, org, project = world
        _repo(session, org, project, "bps-api")
        _ticket(
            session,
            org,
            project,
            key="BPAI-407",
            summary="Small UI Items",
            status=TicketStatus.IN_REVIEW,
            release=None,
        )

        content = _assemble(
            session,
            org,
            project,
            {"bps-api": [_pr(1, "work", branch="BPAI-407-a")]},
        )
        row = content["off_release"][0]
        assert row["ref"] == "BPAI-407"
        assert row["state"] == "shipped_untagged"
        assert content["totals"]["shipped_untagged"] == 1

    def test_a_started_ticket_with_nothing_merged_is_only_a_candidate(self, world):
        session, org, project = world
        _repo(session, org, project, "bps-api")
        _ticket(
            session,
            org,
            project,
            key="BPAI-407",
            summary="Small UI Items",
            status=TicketStatus.IN_REVIEW,
            release=None,
        )

        content = _assemble(session, org, project, {"bps-api": []})
        assert content["off_release"][0]["state"] == "started_untagged"
        assert content["totals"]["shipped_untagged"] == 0

    def test_shipped_untagged_is_listed_first(self, world):
        """Order is the whole point.

        A summary that buries "this shipped and is not in your release" beneath
        fourteen quiet candidates has technically reported it.
        """
        session, org, project = world
        _repo(session, org, project, "bps-api")
        _ticket(
            session,
            org,
            project,
            key="BPAI-100",
            summary="quiet",
            status=TicketStatus.IN_PROGRESS,
            release=None,
        )
        _ticket(
            session,
            org,
            project,
            key="BPAI-900",
            summary="shipped",
            status=TicketStatus.IN_REVIEW,
            release=None,
        )

        content = _assemble(
            session,
            org,
            project,
            {"bps-api": [_pr(1, "work", branch="BPAI-900-a")]},
        )
        assert [r["state"] for r in content["off_release"]] == [
            "shipped_untagged",
            "started_untagged",
        ]

    def test_the_verdict_carries_who_did_it(self, world):
        session, org, project = world
        _repo(session, org, project, "bps-api")
        _ticket(
            session,
            org,
            project,
            key="BPAI-900",
            summary="shipped",
            status=TicketStatus.IN_REVIEW,
            release=None,
        )
        content = _assemble(
            session,
            org,
            project,
            {"bps-api": [_pr(1, "work", branch="BPAI-900-a", author="nobody")]},
        )
        assert content["off_release"][0]["people"] == ["nobody"]

    def test_each_row_says_how_to_fix_it(self, world):
        session, org, project = world
        _repo(session, org, project, "bps-api")
        _ticket(
            session,
            org,
            project,
            key="BPAI-407",
            summary="x",
            status=TicketStatus.IN_REVIEW,
            release=None,
        )
        content = _assemble(session, org, project, {"bps-api": []})
        assert "--release v1.11.0" in content["off_release"][0]["remedy"]


class TestTheSummaryCanActuallyBeSaved:
    """A release summary has to be storable, and it nearly was not.

    `save_project_summary` ties each line of prose to a ticket and a person
    through `ticket_id` and `assignee_user_id`, and files the whole thing under
    `window_spec`. The release payload carried none of the three, so a narrator
    had either to skip saving or to invent them — and a line saved without them
    is stored as work on no ticket, owned by nobody.
    """

    def test_each_item_carries_the_ids_the_save_path_needs(self, world):
        session, org, project = world
        _repo(session, org, project, "bps-api")
        ticket = _ticket(session, org, project, key="BPAI-402", summary="x")

        content = _assemble(
            session,
            org,
            project,
            {"bps-api": [_pr(1, "fix", branch="BPAI-402-a")]},
        )
        item = content["items"][0]
        assert item["ticket_id"] == ticket.id
        assert "assignee_user_id" in item

    def test_the_window_spec_is_the_key_a_summary_is_filed_under(self, world):
        """Emitted, not left to the narrator to build from two other fields.

        A re-spelling is a permanent cache miss, so the shape belongs here.
        """
        session, org, project = world
        _repo(session, org, project, "bps-api")
        assert _assemble(session, org, project, {"bps-api": []})["window_spec"] == (
            "release:v1.11.0"
        )

    def test_no_version_means_no_window_spec(self, world):
        """A hotfix targets a commit, not a release, and files under nothing."""
        session, org, project = world
        _repo(session, org, project, "bps-api")
        content = _assemble(session, org, project, {"bps-api": []}, version=None)
        assert content["window_spec"] is None

    def test_the_assignee_id_is_the_resolved_user_not_a_display_name(self, world):
        """`assignee_user_id` is a foreign key; `people` is for reading."""
        from src.domain.user import User

        session, org, project = world
        user = User(id=str(uuid4()), email="k@x.com", full_name="Ken Smith")
        session.add(user)
        session.commit()
        _repo(session, org, project, "bps-api")
        _ticket(session, org, project, key="BPAI-402", summary="x", assigned_to=user.id)

        item = _assemble(session, org, project, {"bps-api": []})["items"][0]
        assert item["assignee_user_id"] == user.id
        assert item["people"] == ["Ken S."]


class TestTheLooseEndsAreGatheredTogether:
    """Three views of one problem, in one place.

    A ticket on the release with no code, a merged pull request with no ticket,
    and a started ticket carrying no release are the same gap seen from
    different sides. Reported as three separate sections, the reader is left to
    notice that the pull request in one is plainly the missing code in another —
    which is the most useful thing anybody could have told them.
    """

    def test_a_ticket_with_no_code_is_listed(self, world):
        session, org, project = world
        _repo(session, org, project, "bps-api")
        _ticket(session, org, project, key="BPAI-379", summary="Design small UI items")
        content = _assemble(session, org, project, {"bps-api": []})
        assert [t["ref"] for t in content["unresolved"]["tickets_without_code"]] == [
            "BPAI-379"
        ]

    def test_a_pull_request_with_no_ticket_is_listed_with_its_commits(self, world):
        """The commits are the evidence a proposal is argued from."""
        session, org, project = world
        _repo(session, org, project, "bps-api")
        content = _assemble(
            session,
            org,
            project,
            {
                "bps-api": [
                    _pr(
                        600,
                        "stop reporting a baseline ROI multiplier",
                        branch="fix/roi",
                    )
                ]
            },
        )
        loose = content["unresolved"]["pull_requests_without_tickets"]
        assert [p["number"] for p in loose] == [600]
        assert "commits" in loose[0]

    def test_a_started_ticket_with_no_release_is_listed(self, world):
        session, org, project = world
        _repo(session, org, project, "bps-api")
        _ticket(
            session,
            org,
            project,
            key="BPAI-421",
            summary="next release work",
            status=TicketStatus.IN_PROGRESS,
            release=None,
        )
        content = _assemble(session, org, project, {"bps-api": []})
        assert [t["ref"] for t in content["unresolved"]["tickets_without_release"]] == [
            "BPAI-421"
        ]

    def test_a_resolved_release_has_nothing_loose(self, world):
        session, org, project = world
        _repo(session, org, project, "bps-api")
        _ticket(session, org, project, key="BPAI-402", summary="done work")
        content = _assemble(
            session,
            org,
            project,
            {"bps-api": [_pr(1, "work", branch="BPAI-402-a")]},
        )
        assert content["unresolved"]["tickets_without_code"] == []
        assert content["unresolved"]["pull_requests_without_tickets"] == []
        assert content["totals"]["unresolved"] == 0

    def test_the_count_spans_both_sides_of_the_gap(self, world):
        """One number for "how much of this release nobody can account for"."""
        session, org, project = world
        _repo(session, org, project, "bps-api")
        _ticket(session, org, project, key="BPAI-379", summary="no code here")
        content = _assemble(
            session,
            org,
            project,
            {"bps-api": [_pr(9, "orphan", branch="patch-1")]},
        )
        assert content["totals"]["unresolved"] == 2

    def test_nothing_is_paired_for_you(self, world):
        """Pairing is a judgement about what two pieces of English mean.

        A link the platform guessed and stored would be indistinguishable, a
        week later, from one somebody meant — so the sets are handed over
        unpaired and the narrator proposes.
        """
        session, org, project = world
        _repo(session, org, project, "bps-api")
        _ticket(
            session, org, project, key="BPAI-417", summary="Stop showing a 0.0x return"
        )
        content = _assemble(
            session,
            org,
            project,
            {
                "bps-api": [
                    _pr(
                        600,
                        "stop reporting a baseline ROI multiplier",
                        branch="fix/roi",
                    )
                ]
            },
        )
        loose = content["unresolved"]
        assert len(loose["tickets_without_code"]) == 1
        assert len(loose["pull_requests_without_tickets"]) == 1
        # Obvious to a reader, and deliberately not asserted by the service.
        assert all("ticket" not in pr for pr in loose["pull_requests_without_tickets"])


class TestSummarisingAReleaseThatHasAlreadyShipped:
    """Both ends of the window follow the version named, end to end.

    Every other test in this file supplies `since`, so the derived path -- the
    one every real caller takes, because `innoday releases content` no longer
    asks for a date -- was exercised nowhere against real release rows. That is
    where the defect lived: an hour after BPAI v1.11.0 shipped, asking for its
    content returned ten tickets and zero pull requests.
    """

    def _shipped_releases(self, session, org, project):
        for version, released_at in (
            ("v1.10.0", datetime(2026, 7, 1, tzinfo=timezone.utc)),
            ("v1.11.0", datetime(2026, 8, 15, tzinfo=timezone.utc)),
        ):
            session.add(
                Release(
                    organization_id=org.id,
                    project_id=project.id,
                    version=version,
                    status=ReleaseStatus.RELEASED,
                    released_at=released_at,
                )
            )
        session.commit()

    def _derive(self, session, org, project, by_repo, version):
        svc = ReleaseContentService(session, client_factory=lambda _o: _Api(by_repo))
        return asyncio.run(
            svc.assemble(
                project=project,
                organization_id=org.id,
                version=version,
            )
        )

    def test_work_from_the_named_release_is_in_it(self, world):
        session, org, project = world
        self._shipped_releases(session, org, project)
        _repo(session, org, project, "bps-api")
        _ticket(session, org, project, key="BPAI-402", summary="Cite the right law")
        during = _pr(589, "Cite the right law", branch="bpai-402-law")
        during["merged_at"] = "2026-08-10T00:00:00Z"

        payload = self._derive(session, org, project, {"bps-api": [during]}, "v1.11.0")

        assert payload["window"]["previous_version"] == "v1.10.0"
        [item] = payload["items"]
        assert [pr["number"] for pr in item["prs"]] == [589]
        assert item["state"] == "shipped"

    def test_work_merged_after_it_shipped_is_not(self, world):
        """The release that followed must not be reported as part of this one.

        Fixing only the opening boundary leaves this: a window running from
        v1.10.0 to *now*, which is the ninety-three-pull-request report in a
        different costume.
        """
        session, org, project = world
        self._shipped_releases(session, org, project)
        _repo(session, org, project, "bps-api")
        _ticket(session, org, project, key="BPAI-402", summary="Cite the right law")
        during = _pr(589, "Cite the right law", branch="bpai-402-law")
        during["merged_at"] = "2026-08-10T00:00:00Z"
        after = _pr(640, "Cite the right law again", branch="bpai-402-later")
        after["merged_at"] = "2026-08-24T00:00:00Z"

        payload = self._derive(
            session, org, project, {"bps-api": [during, after]}, "v1.11.0"
        )

        [item] = payload["items"]
        assert [pr["number"] for pr in item["prs"]] == [589]
        assert payload["window"]["until"].startswith("2026-08-15")

    def test_the_release_in_flight_is_still_open_ended(self, world):
        """The common call keeps taking everything up to now."""
        session, org, project = world
        self._shipped_releases(session, org, project)
        session.add(
            Release(
                organization_id=org.id,
                project_id=project.id,
                version="v1.12.0",
                status=ReleaseStatus.IN_PROGRESS,
            )
        )
        session.commit()
        _repo(session, org, project, "bps-api")
        _ticket(
            session,
            org,
            project,
            key="BPAI-500",
            summary="Something new",
            release="v1.12.0",
        )
        recent = _pr(700, "Something new", branch="bpai-500-new")
        recent["merged_at"] = "2026-08-24T00:00:00Z"

        payload = self._derive(session, org, project, {"bps-api": [recent]}, "v1.12.0")

        assert payload["window"]["until"] is None
        assert payload["window"]["previous_version"] == "v1.11.0"
        [item] = payload["items"]
        assert [pr["number"] for pr in item["prs"]] == [700]


class TestTheNarratorsSentenceIsJoinedBack:
    """`narrative` is the one field on an item with no other source.

    Who worked on a ticket, which pull requests carried it and whether they
    merged are all derived here. The sentence saying what the change meant to
    somebody *using the product* is written by a Claude session and stored on
    `summary_items` -- nothing can recompute it, and without this join the
    rendered release summary could only ever show ticket titles, which say what
    the work was and never what it did for anyone.
    """

    def _saved_summary(self, session, org, project, ticket, prose, *, version=VERSION):
        summary = Summary(
            organization_id=org.id,
            project_id=project.id,
            summary_type=SummaryType.SCRUM,
            window_spec=f"release:{version}",
            body_markdown="the whole release",
            motivational_quote="",
        )
        session.add(summary)
        session.commit()
        session.add(
            SummaryItem(summary_id=summary.id, ticket_id=ticket.id, body_markdown=prose)
        )
        session.commit()
        return summary

    def test_the_saved_prose_lands_on_the_ticket_it_was_written_about(self, world):
        session, org, project = world
        _repo(session, org, project, "bps-api")
        ticket = _ticket(session, org, project, key="BPAI-402", summary="Fix Lumen")
        self._saved_summary(session, org, project, ticket, "Lumen cites the right law.")

        payload = _assemble(
            session,
            org,
            project,
            {"bps-api": [_pr(589, "Fix Lumen", branch="bpai-402-law")]},
        )

        [item] = payload["items"]
        assert item["narrative"] == "Lumen cites the right law."

    def test_a_release_nobody_has_narrated_carries_no_prose(self, world):
        """Absent, not empty-stringed -- the renderer's fallback to the ticket
        title keys on it, and so does the count it reports."""
        session, org, project = world
        _repo(session, org, project, "bps-api")
        _ticket(session, org, project, key="BPAI-402", summary="Fix Lumen")

        payload = _assemble(
            session,
            org,
            project,
            {"bps-api": [_pr(589, "Fix Lumen", branch="bpai-402-law")]},
        )

        assert payload["items"][0]["narrative"] is None

    def test_another_releases_prose_does_not_leak_in(self, world):
        """`window_spec` is the key. A summary written for v1.10.0 describes
        v1.10.0's version of the work, and printing it against v1.11.0 would be
        a wrong sentence rather than a missing one."""
        session, org, project = world
        _repo(session, org, project, "bps-api")
        ticket = _ticket(session, org, project, key="BPAI-402", summary="Fix Lumen")
        self._saved_summary(
            session, org, project, ticket, "The old story.", version="v1.10.0"
        )

        payload = _assemble(
            session,
            org,
            project,
            {"bps-api": [_pr(589, "Fix Lumen", branch="bpai-402-law")]},
        )

        assert payload["items"][0]["narrative"] is None


class TestTheReleaseRecordTravelsWithTheContent:
    """Whether the release has gone out is not derivable from its tickets.

    A reader who has to run `releases list` beside a release summary to find out
    if it shipped is being handed half an answer.
    """

    def test_it_reports_status_date_and_how_many_tickets_are_still_open(self, world):
        session, org, project = world
        session.add(
            Release(
                organization_id=org.id,
                project_id=project.id,
                version=VERSION,
                status=ReleaseStatus.RELEASED,
                released_at=datetime(2026, 8, 25, tzinfo=timezone.utc),
            )
        )
        session.commit()
        _repo(session, org, project, "bps-api")
        _ticket(session, org, project, key="BPAI-402", summary="Done one")
        _ticket(
            session,
            org,
            project,
            key="BPAI-407",
            summary="Still going",
            status=TicketStatus.IN_PROGRESS,
        )

        record = _assemble(session, org, project, {"bps-api": []})["release_record"]

        assert record["status"] == "released"
        assert record["released_at"].startswith("2026-08-25")
        assert (record["tickets"], record["open"]) == (2, 1)


def _release(session, org, project, version, status, released_at=None):
    row = Release(
        organization_id=org.id,
        project_id=project.id,
        version=version,
        status=status,
        released_at=released_at,
    )
    session.add(row)
    session.commit()
    return row


class TestTheTwoOpenSlotsAnswerDifferently:
    """The release being cut and the one being filled are not the same report.

    Both are unreleased, so both sit inside the same stretch of time: the
    predecessor is the newest released row for each, and neither has a ship date
    to close at. Every window-derived half of the payload was therefore
    identical, and BPAI's v1.12.0 and v1.13.0 differed only in which tickets
    carried the string -- three commits, the same thirty-three pull requests and
    the same eight untagged tickets reported against both.
    """

    def _two_slots(self, session, org, project):
        _release(session, org, project, "v1.11.0", ReleaseStatus.RELEASED, NOW)
        _release(session, org, project, "v1.12.0", ReleaseStatus.IN_PROGRESS)
        _release(session, org, project, "v1.13.0", ReleaseStatus.PLANNED)
        _repo(session, org, project, "bps-api")

    def test_the_planned_release_is_not_the_release_being_cut(self, world):
        session, org, project = world
        self._two_slots(session, org, project)
        _ticket(
            session,
            org,
            project,
            key="BPAI-500",
            summary="started, on no release",
            status=TicketStatus.IN_PROGRESS,
            release=None,
        )
        prs = {"bps-api": [_pr(9, "feat: a thing", branch="feat/thing")]}

        cutting = _assemble(session, org, project, prs, version="v1.12.0")
        planned = _assemble(session, org, project, prs, version="v1.13.0")

        # Compared on the window-derived halves, not on the whole payload: the
        # two dicts have always differed by `release` and `window_spec`, which
        # are the version string echoed back, so `cutting != planned` was true
        # even while every substantive field matched. That is the assertion this
        # test exists to make, and the loose form of it proves nothing.
        derived = (
            "window",
            "window_label",
            "commit_count",
            "included",
            "unticketed",
            "off_release",
        )
        same = [k for k in derived if cutting[k] == planned[k]]
        assert same == [], (
            "the release being cut and the one being planned still answer "
            f"identically on: {same}"
        )

    def test_the_planned_release_borrows_no_window(self, world):
        session, org, project = world
        self._two_slots(session, org, project)
        planned = _assemble(
            session,
            org,
            project,
            {"bps-api": [_pr(9, "feat: a thing", branch="feat/thing")]},
            version="v1.13.0",
        )

        assert planned["window"] is None
        assert planned["included"] == []
        assert planned["commit_count"] == 0
        assert planned["unticketed"] == []

    def test_only_the_release_being_cut_is_offered_candidates(self, world):
        session, org, project = world
        self._two_slots(session, org, project)
        _ticket(
            session,
            org,
            project,
            key="BPAI-500",
            summary="started, on no release",
            status=TicketStatus.IN_PROGRESS,
            release=None,
        )

        def candidates(version):
            content = _assemble(session, org, project, {}, version=version)
            return [
                r["ref"]
                for r in content["off_release"]
                if r["state"] == "started_untagged"
            ]

        assert candidates("v1.12.0") == ["BPAI-500"]
        # Shipped three days ago: it cannot absorb anything.
        assert candidates("v1.11.0") == []
        # The slot behind the one being cut is not the slot being filled.
        assert candidates("v1.13.0") == []


class TestACandidateCarriesNoReleaseAtAll:
    """`release != version` swept in every ticket tagged for the next release."""

    def test_a_ticket_on_another_open_release_is_not_a_candidate(self, world):
        session, org, project = world
        _release(session, org, project, "v1.11.0", ReleaseStatus.RELEASED, NOW)
        _release(session, org, project, "v1.12.0", ReleaseStatus.IN_PROGRESS)
        _release(session, org, project, "v1.13.0", ReleaseStatus.PLANNED)
        _repo(session, org, project, "bps-api")
        _ticket(
            session,
            org,
            project,
            key="BPAI-410",
            summary="correctly placed on the next release",
            status=TicketStatus.IN_REVIEW,
            release="v1.13.0",
        )

        content = _assemble(session, org, project, {}, version="v1.12.0")

        assert [r["ref"] for r in content["off_release"]] == []
        assert content["unresolved"]["tickets_without_release"] == []


class TestStrandedOnAReleaseThatShipped:
    """Shipping touches no ticket, so nothing said one had been left behind."""

    def test_an_unfinished_ticket_on_a_shipped_release_is_a_conflict(self, world):
        session, org, project = world
        _release(session, org, project, "v1.11.0", ReleaseStatus.RELEASED, NOW)
        _release(session, org, project, "v1.12.0", ReleaseStatus.IN_PROGRESS)
        _repo(session, org, project, "bps-api")
        _ticket(
            session,
            org,
            project,
            key="BPAI-407",
            summary="Implement Small UI Items v1.11.0",
            status=TicketStatus.IN_REVIEW,
            release="v1.11.0",
        )

        content = _assemble(session, org, project, {}, version="v1.12.0")

        assert [c["ref"] for c in content["conflicts"]] == ["BPAI-407"]
        assert content["conflicts"][0]["state"] == "on_shipped_release"
        # Not also offered as a candidate: it has a release, and proposing one
        # would overwrite it.
        assert [r["ref"] for r in content["off_release"]] == []

    def test_a_finished_ticket_on_a_shipped_release_is_not_a_conflict(self, world):
        session, org, project = world
        _release(session, org, project, "v1.11.0", ReleaseStatus.RELEASED, NOW)
        _release(session, org, project, "v1.12.0", ReleaseStatus.IN_PROGRESS)
        _repo(session, org, project, "bps-api")
        _ticket(
            session,
            org,
            project,
            key="BPAI-402",
            summary="done and shipped",
            status=TicketStatus.DONE,
            release="v1.11.0",
        )

        content = _assemble(session, org, project, {}, version="v1.12.0")

        assert content["conflicts"] == []


class TestAnOpenPullRequestAgainstAnUntaggedTicket:
    """The evidence "somebody is working on this" had nowhere to land."""

    def test_it_is_attached_rather_than_discarded(self, world):
        session, org, project = world
        _release(session, org, project, "v1.12.0", ReleaseStatus.IN_PROGRESS)
        _repo(session, org, project, "bps-api")
        _ticket(
            session,
            org,
            project,
            key="BPAI-219",
            summary="LL97 pathway designation",
            status=TicketStatus.IN_PROGRESS,
            release=None,
        )

        content = _assemble(
            session,
            org,
            project,
            {
                "bps-api": [
                    _pr(
                        571,
                        "BPAI-219 pathway",
                        branch="feature/BPAI-219-LL97",
                        merged=False,
                    )
                ]
            },
            version="v1.12.0",
        )

        row = next(r for r in content["off_release"] if r["ref"] == "BPAI-219")
        # `release_candidate`, not `started_untagged`: the open pull request is
        # the difference between work in flight and a ticket nobody has touched,
        # and it decides whether this can make the release being cut.
        assert row["state"] == "release_candidate"
        assert [p["number"] for p in row["prs"]] == [571]
        assert row["recommendation"] == "attach_ticket_to_release"


class TestAResolvedReferenceIsNotAlwaysTheRightTicket:
    """bps-ui-v2 #241 -- the entire content of BPAI's v1.11.1 hotfix."""

    def test_a_mismatched_owner_and_subject_are_flagged(self, world):
        session, org, project = world
        _release(session, org, project, "v1.12.0", ReleaseStatus.IN_PROGRESS)
        _repo(session, org, project, "bps-ui-v2")
        _ticket(
            session,
            org,
            project,
            key="BPAI-409",
            summary="Incorporate ESC-Utility-Rates",
            status=TicketStatus.DONE,
            release=None,
            assignee="george",
        )

        content = _assemble(
            session,
            org,
            project,
            {
                "bps-ui-v2": [
                    _pr(
                        241,
                        "Bpai 409 small UI items",
                        branch="bpai_409_small_ui_items",
                        author="jasminder",
                    )
                ]
            },
            version="v1.12.0",
        )

        row = next(r for r in content["off_release"] if r["ref"] == "BPAI-409")
        pr = row["prs"][0]
        contested = pr["contested"]
        # The subject disagrees, and that is evidence on its own.
        assert any("no significant word in common" in reason for reason in contested)
        # **Ownership is not evidence here, and must not be claimed as it.**
        # Neither side of this fixture resolves to a real user, so
        # `name_for_ticket` returns the board's string and `name_for` returns the
        # raw login. Two unresolved names disagreeing says nothing about who owns
        # the work -- it is the commonest configuration there is, and treating it
        # as a mismatch contested every correct match on such a project.
        assert not any("belongs to" in reason for reason in contested)
        assert pr["state"] == "contested"

    def test_an_unresolved_identity_alone_never_contests(self, world):
        """The regression this guards: a matching subject plus two unresolved
        names used to contest purely on the name difference."""
        session, org, project = world
        _release(session, org, project, "v1.12.0", ReleaseStatus.IN_PROGRESS)
        _repo(session, org, project, "bps-api")
        _ticket(
            session,
            org,
            project,
            key="BPAI-500",
            summary="Add the jurisdiction filter",
            status=TicketStatus.IN_PROGRESS,
            release=None,
            assignee="Jasminder Singh",
        )

        content = _assemble(
            session,
            org,
            project,
            {
                "bps-api": [
                    _pr(
                        90,
                        "feat: jurisdiction filter on the property list",
                        branch="feature/BPAI-500/jurisdiction",
                        author="jasminder",
                    )
                ]
            },
            version="v1.12.0",
        )

        row = next(r for r in content["off_release"] if r["ref"] == "BPAI-500")
        assert "contested" not in row["prs"][0]

    def test_a_title_that_is_only_a_reference_never_contests(self, world):
        """`BPAI-500` shares no word with any ticket title, and is the least
        ambiguous match there is."""
        session, org, project = world
        _release(session, org, project, "v1.12.0", ReleaseStatus.IN_PROGRESS)
        _repo(session, org, project, "bps-api")
        _ticket(
            session,
            org,
            project,
            key="BPAI-500",
            summary="Add the jurisdiction filter",
            status=TicketStatus.IN_PROGRESS,
            release=None,
        )

        content = _assemble(
            session,
            org,
            project,
            {"bps-api": [_pr(91, "BPAI-500", branch="feature/BPAI-500")]},
            version="v1.12.0",
        )

        row = next(r for r in content["off_release"] if r["ref"] == "BPAI-500")
        assert "contested" not in row["prs"][0]

    def test_a_matching_ticket_is_not_flagged(self, world):
        session, org, project = world
        _release(session, org, project, "v1.12.0", ReleaseStatus.IN_PROGRESS)
        _repo(session, org, project, "bps-ui-v2")
        _ticket(
            session,
            org,
            project,
            key="BPAI-421",
            summary="Implement Small UI Items v1.12.0",
            status=TicketStatus.IN_PROGRESS,
            release=None,
            assignee="jasminder",
        )

        content = _assemble(
            session,
            org,
            project,
            {
                "bps-ui-v2": [
                    _pr(
                        242,
                        "Bpai 421 small UI items",
                        branch="bpai_421_small_ui_items",
                        author="jasminder",
                    )
                ]
            },
            version="v1.12.0",
        )

        row = next(r for r in content["off_release"] if r["ref"] == "BPAI-421")
        assert "contested" not in row["prs"][0]


class TestTheDefaultReportIsNeverBlanked:
    """The worst regression the short-circuit could cause, and did.

    `current_release_version` prefers IN_PROGRESS but falls back to the lowest
    PLANNED above the high-water mark, and `releases create` defaults to PLANNED.
    So on a project whose next release has not been started, the *unversioned*
    call resolved to a planned version and short-circuited -- every merged pull
    request, candidate and unticketed pull request gone from the default report,
    with no warning. Asking for "the release in flight" must answer about the
    window even when the slot is only planned.
    """

    def _project_with_only_a_planned_slot(self, session, org, project):
        _release(session, org, project, "v1.11.0", ReleaseStatus.RELEASED, NOW)
        _release(session, org, project, "v1.12.0", ReleaseStatus.PLANNED)
        _repo(session, org, project, "bps-api")

    def test_asking_for_the_current_release_still_reads_the_window(self, world):
        session, org, project = world
        self._project_with_only_a_planned_slot(session, org, project)

        content = _assemble(
            session,
            org,
            project,
            {"bps-api": [_pr(9, "feat: a thing", branch="feat/thing")]},
            version=None,
        )

        assert content["window"] is not None
        assert content["commit_count"] > 0
        assert [p["number"] for r in content["included"] for p in r["prs"]] == [9]
        assert len(content["unticketed"]) == 1

    def test_naming_that_same_version_does_short_circuit(self, world):
        """The distinction is who chose the version, not what its status is."""
        session, org, project = world
        self._project_with_only_a_planned_slot(session, org, project)

        content = _assemble(
            session,
            org,
            project,
            {"bps-api": [_pr(9, "feat: a thing", branch="feat/thing")]},
            version="v1.12.0",
        )

        assert content["window"] is None
        assert content["planned"] is True


class TestAVersionThisProjectDoesNotHave:
    def test_nothing_is_proposed_onto_a_phantom_version(self, world):
        """`--version v9.9.9` used to return the in-flight window branded with
        the typo, plus a copy-pasteable command tagging real tickets onto it."""
        session, org, project = world
        _release(session, org, project, "v1.11.0", ReleaseStatus.RELEASED, NOW)
        _release(session, org, project, "v1.12.0", ReleaseStatus.IN_PROGRESS)
        _repo(session, org, project, "bps-api")
        _ticket(
            session,
            org,
            project,
            key="BPAI-500",
            summary="started, on no release",
            status=TicketStatus.IN_PROGRESS,
            release=None,
        )

        content = _assemble(session, org, project, {}, version="v9.9.9")

        assert content["unknown_version"] == "v9.9.9"
        assert content["off_release"] == []

    def test_a_project_with_no_release_records_still_gets_candidates(self, world):
        """The legitimate half of the same shape: nothing to check against."""
        session, org, project = world
        _repo(session, org, project, "bps-api")
        _ticket(
            session,
            org,
            project,
            key="BPAI-500",
            summary="started, on no release",
            status=TicketStatus.IN_PROGRESS,
            release=None,
        )

        content = _assemble(session, org, project, {}, version=VERSION)

        assert content["unknown_version"] is None
        assert [r["ref"] for r in content["off_release"]] == ["BPAI-500"]


class TestVersionsAreComparedAsVersions:
    def test_a_differently_spelled_release_is_the_same_release(self, world):
        """A row spelled `1.13.0` against a ticket tagged `v1.13.0` made the
        ticket look untagged, so the report offered to overwrite a version
        somebody had set on purpose -- the exact bug the filter exists to stop."""
        session, org, project = world
        _release(session, org, project, "v1.11.0", ReleaseStatus.RELEASED, NOW)
        _release(session, org, project, "v1.12.0", ReleaseStatus.IN_PROGRESS)
        _release(session, org, project, "1.13.0", ReleaseStatus.PLANNED)
        _repo(session, org, project, "bps-api")
        _ticket(
            session,
            org,
            project,
            key="BPAI-410",
            summary="correctly placed on the next release",
            status=TicketStatus.IN_REVIEW,
            release="v1.13.0",
        )

        content = _assemble(
            session,
            org,
            project,
            {"bps-api": [_pr(9, "BPAI-410 thing", branch="feature/BPAI-410")]},
            version="v1.12.0",
        )

        assert content["off_release"] == []


class TestAShippedReleaseDoesNotConflictWithItself:
    def test_its_own_unfinished_ticket_is_a_member_not_a_conflict(self, world):
        """One ticket became two rows across two counters, with a detail reading
        "v1.11.0 shipped without this finished" about the release being read."""
        session, org, project = world
        _release(session, org, project, "v1.11.0", ReleaseStatus.RELEASED, NOW)
        _release(session, org, project, "v1.12.0", ReleaseStatus.IN_PROGRESS)
        _repo(session, org, project, "bps-api")
        _ticket(
            session,
            org,
            project,
            key="BPAI-407",
            summary="Implement Small UI Items",
            status=TicketStatus.IN_REVIEW,
            release="v1.11.0",
        )

        own = _assemble(session, org, project, {}, version="v1.11.0")
        assert [i["ref"] for i in own["items"]] == ["BPAI-407"]
        assert own["conflicts"] == []

        # Still a conflict when asked about any *other* release.
        other = _assemble(session, org, project, {}, version="v1.12.0")
        assert [c["ref"] for c in other["conflicts"]] == ["BPAI-407"]


class TestThePlannedPayloadAddsUp:
    def test_totals_are_counted_from_the_items(self, world):
        """They were literals, so a planned release with gaps on every ticket
        reported `with_gaps: 0` -- on the field the MCP tool tells callers to
        drive to zero before cutting. Every planned release read as ready."""
        session, org, project = world
        _release(session, org, project, "v1.11.0", ReleaseStatus.RELEASED, NOW)
        _release(session, org, project, "v1.12.0", ReleaseStatus.PLANNED)
        _repo(session, org, project, "bps-api")
        for key in ("BPAI-600", "BPAI-601"):
            _ticket(
                session,
                org,
                project,
                key=key,
                summary=f"planned work {key}",
                status=TicketStatus.BACKLOG,
                release="v1.12.0",
            )

        content = _assemble(session, org, project, {}, version="v1.12.0")
        totals = content["totals"]

        assert totals["tickets"] == 2
        assert totals["tickets"] == totals["complete"] + totals["with_gaps"]
        assert totals["with_gaps"] == 2
        assert totals["unresolved"] == 2
        assert len(content["unresolved"]["tickets_without_code"]) == 2

    def test_a_supplied_boundary_is_not_silently_dropped(self, world):
        session, org, project = world
        _release(session, org, project, "v1.11.0", ReleaseStatus.RELEASED, NOW)
        _release(session, org, project, "v1.12.0", ReleaseStatus.PLANNED)
        _repo(session, org, project, "bps-api")

        svc = ReleaseContentService(session, client_factory=lambda _o: _Api({}))
        content = asyncio.run(
            svc.assemble(
                project=project,
                organization_id=org.id,
                since=SINCE,
                window_label="since v1.10.0",
                version="v1.12.0",
            )
        )

        assert any("no window" in w for w in content["warnings"])

    def test_it_keeps_the_shape_a_full_assembly_has(self, world):
        """`_planned_only`'s docstring promises "same keys as a full assembly so
        no caller has to branch on shape". Nothing asserted it, so the next key
        added to `assemble` would diverge silently -- the `KeyError` the
        docstring says it is avoiding."""
        session, org, project = world
        _release(session, org, project, "v1.11.0", ReleaseStatus.RELEASED, NOW)
        _release(session, org, project, "v1.12.0", ReleaseStatus.IN_PROGRESS)
        _release(session, org, project, "v1.13.0", ReleaseStatus.PLANNED)
        _repo(session, org, project, "bps-api")

        prs = {"bps-api": [_pr(9, "feat: a thing", branch="feat/thing")]}
        cutting = _assemble(session, org, project, prs, version="v1.12.0")
        planned = _assemble(session, org, project, prs, version="v1.13.0")

        # `warnings` is conditional on both paths -- `assemble` emits it only when
        # the window or the coverage has something to say -- so it is excluded
        # rather than asserted. `planned` is the one key that exists to mark which
        # kind of payload this is.
        optional = {"warnings", "truncated_repos"}
        assert set(cutting) - set(planned) - optional == set()
        assert set(planned) - set(cutting) - optional == {"planned"}
