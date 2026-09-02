"""Which ticket a piece of code belongs to, and when nobody can tell.

The index and the branch-to-ticket matcher used to live in two different
modules -- one in `summary_service`, one inside the web UI router -- so the only
working join between a ticket and its pull requests sat where neither the
release path nor the summary path could reach it. Both rebuilt a worse version.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

import pytest
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from src.domain.organization import Organization
from src.domain.project import Project, ProjectRepository
from src.domain.repository import Repository
from src.domain.repository_pull_request import RepositoryPullRequest
from src.domain.ticket import Ticket
from src.services.ticket_matching import (
    TicketPullRequest,
    colliding_refs,
    merged_pull_requests_by_ticket,
    pull_requests_by_ticket,
    ref_prefixes,
    ticket_for_pull_request,
    tickets_by_ref,
)


class _Ticket:
    def __init__(
        self,
        id,
        external_ticket_id=None,
        project_ref_number=None,
        summary="",
        source_platform=None,
    ):
        self.id = id
        self.external_ticket_id = external_ticket_id
        self.project_ref_number = project_ref_number
        self.summary = summary
        self.source_platform = source_platform


class TestCollidingRefs:
    """The 22-in-221 problem, made visible instead of silently guessed at."""

    def test_the_same_string_naming_two_tickets_is_reported(self):
        """`BPAI-169` is one ticket in Linear and a different one here.

        `tickets_by_ref` resolves it in the board key's favour, which is the
        right guess and still a guess. A summary citing it is citing something
        the reader cannot resolve either, so it gets said out loud.
        """
        board = _Ticket(
            1, external_ticket_id="BPAI-169", summary="Generate Suggestions"
        )
        internal = _Ticket(2, project_ref_number=169, summary="Carbon Graph")
        clashes = colliding_refs("BPAI", [board, internal])
        assert [(ref, a.id, b.id) for ref, a, b in clashes] == [("BPAI-169", 1, 2)]

    def test_one_ticket_holding_both_names_is_not_a_collision(self):
        """Two names for the same ticket is the ordinary case, not a problem."""
        both = _Ticket(1, external_ticket_id="BPAI-7", project_ref_number=7)
        assert colliding_refs("BPAI", [both]) == []

    def test_a_board_key_on_another_prefix_cannot_collide(self):
        """A Linear `ZZ-9` on a project aliased BPAI shares no string with it."""
        board = _Ticket(1, external_ticket_id="ZZ-9")
        internal = _Ticket(2, project_ref_number=9)
        assert colliding_refs("BPAI", [board, internal]) == []

    def test_no_alias_reports_nothing(self):
        """Without an alias the internal namespace has no spelling at all."""
        assert colliding_refs("", [_Ticket(1, project_ref_number=1)]) == []

    def test_the_index_still_resolves_the_collision_to_the_board_key(self):
        """Pins the tie-break this detector exists to report, not to change.

        Removing the internal name instead would drop *correct* matches for
        tickets referenced by their InnoDay number, while changing no collision
        outcome -- the board key already won every one of them.
        """
        board = _Ticket(1, external_ticket_id="BPAI-169")
        internal = _Ticket(2, project_ref_number=169)
        assert tickets_by_ref("BPAI", [board, internal])["BPAI-169"].id == 1


class TestRefPrefixes:
    def test_it_finds_every_alias_the_index_answers_to(self):
        """A board key need not share the project's alias, and often does not."""
        index = tickets_by_ref(
            "BPAI",
            [_Ticket(1, external_ticket_id="ZZ-9"), _Ticket(2, project_ref_number=4)],
        )
        assert ref_prefixes(index) == ["BPAI", "ZZ"]


class TestTicketPullRequestCarriesWhatAReleaseNeeds:
    def test_merged_is_derived_from_a_confirmed_timestamp(self):
        """Not from `state`: an abandoned pull request is also closed."""
        assert TicketPullRequest("r", 1, None, None, state="closed").merged is False
        assert (
            TicketPullRequest(
                "r", 1, None, None, state="closed", merged_at="2026-08-10T00:00:00Z"
            ).merged
            is True
        )

    def test_the_author_is_carried(self):
        """Dropped by the original dataclass, which is why nothing could credit."""
        assert (
            TicketPullRequest("r", 1, None, None, author_login="havkarl").author_login
            == "havkarl"
        )


# --------------------------------------------------------------------------- #
# The join itself, against a real database.
#
# Everything above tests pure functions. Nothing tested that the row actually
# reaches the object -- so dropping `author_login` from the mapping changed no
# test, which is precisely the gap that let a release have nobody to credit.
# --------------------------------------------------------------------------- #

MERGED_AT = datetime(2026, 8, 10, tzinfo=timezone.utc)


@pytest.fixture
def world_session():
    """A project with one repository, one ticket, and no pull requests yet."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        org = Organization(id=str(uuid.uuid4()), name="Org", alias="org")
        project = Project(
            id=str(uuid.uuid4()),
            name="Proj",
            alias="BPAI",
            description="",
            organization_id=org.id,
        )
        repo = Repository(
            id="gh-1",
            name="bps-api",
            full_name="an-org/bps-api",
            url="https://github.com/an-org/bps-api",
            organization_id=org.id,
        )
        session.add_all([org, project, repo])
        session.add(ProjectRepository(project_id=project.id, repository_id=repo.id))
        ticket = Ticket(
            organization_id=org.id,
            project_id=project.id,
            summary="Jurisdiction first",
            external_ticket_id="BPAI-402",
        )
        session.add(ticket)
        session.commit()
        session.refresh(ticket)
        yield session, project, ticket


def _add_pr(session, **kwargs):
    kwargs.setdefault(
        "url", f"https://github.com/an-org/bps-api/pull/{kwargs['number']}"
    )
    session.add(RepositoryPullRequest(repository_id="gh-1", **kwargs))
    session.commit()


class TestTheRowReachesTheObject:
    def test_a_merged_pull_request_carries_its_author_and_timestamp(
        self, world_session
    ):
        """The three fields a release needs, read off the row it came from."""
        session, project, ticket = world_session
        _add_pr(
            session,
            number=11,
            title="Fix jurisdiction",
            head_ref="BPAI-402-jurisdiction",
            state="closed",
            merged_at=MERGED_AT,
            author_login="havkarl",
        )
        found = merged_pull_requests_by_ticket(session, project.id)
        pr = found[ticket.id][0]
        assert pr.author_login == "havkarl"
        assert pr.state == "closed"
        assert pr.merged is True

    def test_an_open_pull_request_is_not_merged(self, world_session):
        session, project, ticket = world_session
        _add_pr(
            session,
            number=12,
            title="Work in progress",
            head_ref="BPAI-402-more",
            state="open",
            author_login="someone",
        )
        pr = pull_requests_by_ticket(session, project.id)[ticket.id][0]
        assert pr.merged is False
        assert pr.author_login == "someone"

    def test_a_title_names_the_ticket_when_the_branch_does_not(self, world_session):
        """Branch first, then title -- a badly named branch is not a lost link."""
        session, project, ticket = world_session
        _add_pr(
            session,
            number=13,
            title="BPAI-402: fix it",
            head_ref="patch-1",
            state="closed",
            merged_at=MERGED_AT,
            author_login="havkarl",
        )
        assert ticket.id in merged_pull_requests_by_ticket(session, project.id)

    def test_a_pull_request_naming_nothing_links_to_nothing(self, world_session):
        session, project, ticket = world_session
        _add_pr(
            session,
            number=14,
            title="tidy up",
            head_ref="patch-2",
            state="closed",
            merged_at=MERGED_AT,
        )
        assert merged_pull_requests_by_ticket(session, project.id) == {}


class TestAnAmbiguousTitleNamesNothing:
    """A title mentioning two tickets is prose, not an attribution.

    `docs(rules): add fix-as-you-touch rule for BPAI-355 & BPAI-380` is a
    documentation change *about* two tickets. Taking the first reference
    credited its work to BPAI-355, which then appeared in a release report as
    "shipped outside a release" -- a finding that was not true, dressed in the
    same confident formatting as the true ones.

    A branch is different: it belongs to one piece of work, so the first
    reference in it is the answer.
    """

    def _index(self):
        return tickets_by_ref(
            "BPAI",
            [
                _Ticket(1, external_ticket_id="BPAI-355", summary="consolidate types"),
                _Ticket(2, external_ticket_id="BPAI-380", summary="something else"),
            ],
        )

    def _pattern(self):
        from src.services.code_activity import ticket_ref_pattern

        return ticket_ref_pattern("BPAI")

    def test_two_references_in_a_title_match_nothing(self):
        assert (
            ticket_for_pull_request(
                "patch-1",
                "docs(rules): add fix-as-you-touch rule for BPAI-355 & BPAI-380",
                self._index(),
                self._pattern(),
            )
            is None
        )

    def test_one_reference_in_a_title_still_matches(self):
        """The rule must not cost the ordinary case."""
        found = ticket_for_pull_request(
            "patch-1", "BPAI-355: consolidate types", self._index(), self._pattern()
        )
        assert found is not None and found.id == 1

    def test_the_same_reference_twice_is_not_ambiguous(self):
        """Repetition is emphasis, not a second subject."""
        found = ticket_for_pull_request(
            "patch-1",
            "BPAI-355: consolidate types (closes BPAI-355)",
            self._index(),
            self._pattern(),
        )
        assert found is not None and found.id == 1

    def test_a_branch_wins_over_an_ambiguous_title(self):
        """The branch is unambiguous by construction, so it still decides."""
        found = ticket_for_pull_request(
            "BPAI-380-work",
            "docs: rule for BPAI-355 & BPAI-380",
            self._index(),
            self._pattern(),
        )
        assert found is not None and found.id == 2


class TestTheThreePlacesAPullRequestNamesItsTicket:
    """Seven of thirty-four merged pull requests matched. The rest were real.

    A review of one BPAI release found tickets sitting on it reporting "no pull
    request names this ticket" while a merged pull request named them plainly --
    in a branch our regex could not read, in a branch prefixed with the tool
    instead of the project, or in a description we never looked at.
    """

    def _world(self):
        tickets = [
            _Ticket(
                1,
                external_ticket_id="BPAI-413",
                project_ref_number=206,
                source_platform="linear",
            ),
            _Ticket(
                2,
                external_ticket_id="BPAI-414",
                project_ref_number=205,
                source_platform="linear",
            ),
            _Ticket(3, external_ticket_id="BPAI-409", source_platform="linear"),
        ]
        index = tickets_by_ref("BPAI", tickets)
        from src.services.code_activity import ticket_ref_pattern

        return index, ticket_ref_pattern(*ref_prefixes(index), "BPAI")

    def test_an_underscored_branch_matches(self):
        """`bpai_409_small_ui_items` -- the boundary bug, in the wild.

        `\\b` after the digits fails against a trailing underscore, so the
        hyphenated form matched and the underscored form did not. Nothing
        indicated the reference was sitting right there in the branch name.
        """
        index, pattern = self._world()
        found = ticket_for_pull_request(
            "bpai_409_small_ui_items", "feat(ui): collapsible nav", index, pattern
        )
        assert found is not None and found.id == 3

    def test_a_branch_named_after_the_tool_matches(self):
        """`linear_413_...` -- people name branches after Linear, not the project."""
        index, pattern = self._world()
        found = ticket_for_pull_request(
            "linear_413_manage_org_small_fixes",
            "Manage org icon and label change",
            index,
            pattern,
        )
        assert found is not None and found.id == 1

    def test_the_body_is_read_when_the_branch_and_title_say_nothing(self):
        """A pull request titled "Label updates" on `financial_summary_labels`.

        Its description says BPAI-414. The ticket reported no code; the code was
        naming it the whole time.
        """
        index, pattern = self._world()
        found = ticket_for_pull_request(
            "financial_summary_labels",
            "Label updates",
            index,
            pattern,
            body="Implements BPAI-414 label changes",
        )
        assert found is not None and found.id == 2

    def test_a_closing_keyword_wins_over_other_mentions(self):
        """A description that closes one ticket and mentions three is explicit.

        Without this, the "exactly one reference" rule would reject a thorough
        description for being thorough.
        """
        index, pattern = self._world()
        found = ticket_for_pull_request(
            "patch-1",
            "some work",
            index,
            pattern,
            body="Related to BPAI-409 and BPAI-413.\n\nCloses BPAI-414.",
        )
        assert found is not None and found.id == 2

    def test_an_ambiguous_body_with_no_closing_keyword_matches_nothing(self):
        index, pattern = self._world()
        assert (
            ticket_for_pull_request(
                "patch-1",
                "some work",
                index,
                pattern,
                body="Touches BPAI-409 and BPAI-413 in passing.",
            )
            is None
        )

    def test_nothing_anywhere_still_matches_nothing(self):
        """The honest remainder. 23 of the 34 are this, and no rule fixes them.

        `fix/roi-multiplier-null` / "stop reporting a baseline ROI multiplier" is
        obviously the ticket "Stop showing a 0.0x return when a scenario loses
        money" -- and says so nowhere. Guessing from wording is how a summary
        starts inventing.
        """
        index, pattern = self._world()
        assert (
            ticket_for_pull_request(
                "fix/roi-multiplier-null",
                "fix(v2): stop reporting a baseline ROI multiplier",
                index,
                pattern,
                body="Removes the baseline multiplier.",
            )
            is None
        )

    def test_the_branch_still_beats_the_body(self):
        """Precedence: the branch is the strongest signal, the body the weakest."""
        index, pattern = self._world()
        found = ticket_for_pull_request(
            "BPAI-413-work", "x", index, pattern, body="Closes BPAI-414"
        )
        assert found is not None and found.id == 1

    def test_a_tool_prefix_cannot_shadow_a_real_key(self):
        """Tool aliases are added last, so a genuine `LINEAR-9` key still wins."""
        real = _Ticket(9, external_ticket_id="LINEAR-9")
        other = _Ticket(10, external_ticket_id="BPAI-9", source_platform="linear")
        index = tickets_by_ref("BPAI", [real, other])
        assert index["LINEAR-9"].id == 9


class TestPrecisionCostsOfMatchingHarder:
    """Widening the net caught things it should not.

    Reading branches more loosely and reading descriptions at all recovered real
    work — and on the same release produced three attributions that were simply
    wrong. Each is a distinct way a number can appear next to a project alias
    without anybody claiming the work.
    """

    def _world(self):
        tickets = [
            _Ticket(1, external_ticket_id="BPAI-355", source_platform="linear"),
            _Ticket(2, external_ticket_id="BPAI-380", source_platform="linear"),
            _Ticket(3, external_ticket_id="BPAI-343", source_platform="linear"),
            _Ticket(4, external_ticket_id="BPAI-414", source_platform="linear"),
        ]
        index = tickets_by_ref("BPAI", tickets)
        from src.services.code_activity import ticket_ref_pattern

        return index, ticket_ref_pattern(*ref_prefixes(index), "BPAI")

    def test_a_branch_listing_two_numbers_matches_nothing(self):
        """`linear_355_380_claude_rule` — a rule written while touching both.

        Only the first number carries a prefix, so counting references finds one
        and the branch reads as unambiguous. Numbers stacked after a reference
        are a list, and a list is not an attribution.
        """
        index, pattern = self._world()
        assert (
            ticket_for_pull_request(
                "linear_355_380_claude_rule",
                "docs(rules): add fix-as-you-touch rule for BPAI-355 & BPAI-380",
                index,
                pattern,
            )
            is None
        )

    def test_a_reference_inside_a_filename_is_not_a_claim(self):
        """`docs/BPAI-343-phase1-summary.md` in a README refresh.

        The pull request is about documentation and mentions the file by name.
        Reading that as "this delivered BPAI-343" put an unrelated ticket into a
        release report as shipped.
        """
        index, pattern = self._world()
        assert (
            ticket_for_pull_request(
                "docs/readme-refresh",
                "docs: correct README deploy, env, and endpoint reference",
                index,
                pattern,
                body="- `docs/BPAI-343-phase1-summary.md` links the design spec",
            )
            is None
        )

    def test_a_description_that_still_names_one_ticket_survives(self):
        """The guard must not undo the recovery it was added alongside."""
        index, pattern = self._world()
        found = ticket_for_pull_request(
            "financial_summary_labels",
            "Label updates",
            index,
            pattern,
            body="Implements BPAI-414 label changes",
        )
        assert found is not None and found.id == 4

    def test_a_description_naming_a_ticket_and_a_file_still_matches(self):
        """Stripping paths must not strip the sentence around them."""
        index, pattern = self._world()
        found = ticket_for_pull_request(
            "patch-1",
            "x",
            index,
            pattern,
            body="Closes BPAI-414. See docs/BPAI-343-phase1-summary.md for context.",
        )
        assert found is not None and found.id == 4

    def test_a_branch_with_a_description_after_the_number_still_matches(self):
        """`bpai_409_small_ui_items` — words after a reference are a description."""
        index, pattern = self._world()
        tickets = [_Ticket(9, external_ticket_id="BPAI-409", source_platform="linear")]
        idx = tickets_by_ref("BPAI", tickets)
        from src.services.code_activity import ticket_ref_pattern

        pat = ticket_ref_pattern(*ref_prefixes(idx), "BPAI")
        found = ticket_for_pull_request("bpai_409_small_ui_items", "x", idx, pat)
        assert found is not None and found.id == 9
