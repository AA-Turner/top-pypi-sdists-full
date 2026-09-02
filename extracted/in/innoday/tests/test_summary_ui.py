"""The browser surface for summaries: the profile page and the scrum panel.

Organised by failure mode, matching `tests/test_webui_pages.py`. The ones that
earn their place:

* **Route precedence.** ``/ui/{org_ref}`` matches a bare org alias, so the
  profile page is one registration-order mistake away from being read as an org
  called "profile". Both guards are asserted -- the literal route resolving, and
  the reserved segment refusing the alias.
* **The duplicate-handle message names the conflict, not the person.** Echoing
  the current owner would turn a claim form into a directory of who is on the
  board, readable by guessing display names.
* **The picklist is fed from `unmapped-assignees`.** It is the *primary* mapping
  path on Jira and Trello (neither reliably supplies an email), not a fallback,
  and it must agree with the count in the panel footer -- so both read the same
  capability.
* **Team by default; "Yours" only when there is one.** A toggle that leads to a
  blank box is worse than no toggle.
* **Both empty states say why and how.** An empty panel with no explanation is
  indistinguishable from a broken one.
* **The five-active cap holds in the rendered HTML**, and the trailing blocks do
  not consume a slot -- that is the whole shape of the agreed layout.
"""

import re
from datetime import datetime, timedelta, timezone
from urllib.parse import unquote
from uuid import uuid4

import pytest
from sqlmodel import Session, select

from src.adapters.board_assignee import BoardAssignee
from src.domain.board import BoardRegistration, BoardType
from src.domain.cli_token import CLIToken, generate_cli_token
from src.domain.organization import (
    Organization,
    OrganizationMembership,
    OrganizationRole,
)
from src.domain.project import Project, ProjectRepository
from src.domain.summary import Summary, SummaryItem, SummaryType
from src.domain.ticket import Ticket, TicketStatus
from src.domain.user import User
from src.domain.user_identity import IdentityPlatform, MatchSource, UserIdentity
from src.page_paths import (
    RESERVED_UI_SEGMENTS,
    UI_PREFIX,
    dashboard_path,
    profile_path,
)
from src.routers._brand_pages import FAVICON_SVG
from src.routers.webui.session import COOKIE_NAME, SESSION_TOKEN_NAME

UTC_NOW = datetime.now(timezone.utc)


# --------------------------------------------------------------------------- #
# Fixtures
# --------------------------------------------------------------------------- #


@pytest.fixture
def world(db_engine):
    """Factory for an org + project + signed-in member, and the raw cookie."""

    def _make(*, alias=None, with_board=BoardType.LINEAR, email=None):
        tag = uuid4().hex[:8]
        with Session(db_engine) as session:
            user = User(
                id=str(uuid4()),
                email=email or f"{tag}@example.com",
                full_name="Ada Lovelace",
            )
            session.add(user)
            raw = generate_cli_token(kind="oauth")
            from src.domain.cli_token import hash_cli_token

            session.add(
                CLIToken(
                    user_id=user.id,
                    token_hash=hash_cli_token(raw),
                    name=SESSION_TOKEN_NAME,
                    expires_at=UTC_NOW + timedelta(days=7),
                )
            )
            org = Organization(
                id=str(uuid4()), name=f"Org {tag}", alias=alias or f"org{tag}"
            )
            session.add(org)
            session.add(
                OrganizationMembership(
                    id=str(uuid4()),
                    user_id=user.id,
                    organization_id=org.id,
                    role=OrganizationRole.ADMIN,
                    is_active=True,
                )
            )
            project = Project(
                id=str(uuid4()),
                name=f"Project {tag}",
                alias=f"p{tag}",
                organization_id=org.id,
                description="ui fixture",
            )
            session.add(project)
            if with_board is not None:
                session.add(
                    BoardRegistration(
                        id=str(uuid4()),
                        organization_id=org.id,
                        project_id=project.id,
                        user_id=user.id,
                        board_type=with_board,
                        board_name=f"Board {tag}",
                        board_external_id=f"ext-{tag}",
                        board_url="https://linear.app/x",
                        is_active=True,
                    )
                )
            session.commit()
            session.refresh(user)
            session.refresh(org)
            session.refresh(project)
            return user, org, project, raw

    return _make


@pytest.fixture
def add_ticket(db_engine):
    def _make(project, org, **kw):
        with Session(db_engine) as session:
            ticket = Ticket(
                summary=kw.pop("summary", "A ticket"),
                organization_id=org.id,
                project_id=project.id,
                **kw,
            )
            session.add(ticket)
            session.commit()
            session.refresh(ticket)
            return ticket

    return _make


@pytest.fixture
def add_summary(db_engine):
    """A live summary with items. ``items`` are dicts of SummaryItem kwargs."""

    def _make(org, project, *, items=(), user_id=None, **kw):
        with Session(db_engine) as session:
            summary = Summary(
                organization_id=org.id,
                project_id=project.id,
                user_id=user_id,
                summary_type=kw.pop(
                    "summary_type",
                    SummaryType.PERSONAL if user_id else SummaryType.SCRUM,
                ),
                window_spec=kw.pop("window_spec", "3d"),
                body_markdown=kw.pop("body_markdown", "three quiet days"),
                motivational_quote="onward",
                **kw,
            )
            session.add(summary)
            session.flush()
            for rank, item in enumerate(items):
                session.add(SummaryItem(summary_id=summary.id, rank=rank, **dict(item)))
            session.commit()
            session.refresh(summary)
            return summary

    return _make


def _auth(client, raw_cookie):
    client.cookies.set(COOKIE_NAME, raw_cookie)
    return client


# --------------------------------------------------------------------------- #
# Route precedence
# --------------------------------------------------------------------------- #


def test_profile_resolves_and_is_never_read_as_an_org_alias(client, world):
    """Both guards at once, because either alone is a silent failure.

    The literal route must resolve under a real org (declaration order), and
    "profile" must be refused as an alias (`RESERVED_UI_SEGMENTS`) so nobody can
    create an org that shadows a page name.
    """
    user, org, _project, cookie = world(alias="acme")
    _auth(client, cookie)

    assert "profile" in RESERVED_UI_SEGMENTS
    page = client.get(profile_path(org.alias))
    assert page.status_code == 200
    assert "Board handles" in page.text

    # The bare segment is reserved, so it can never resolve to an org dashboard.
    assert client.get(f"{UI_PREFIX}/profile").status_code == 404


def test_profile_404s_for_a_non_member(client, world, db_engine):
    """404, not 403 -- same rule as the dashboard, same reason."""
    _user, _org, _project, cookie = world()
    with Session(db_engine) as session:
        other = Organization(id=str(uuid4()), name="Theirs", alias="theirs")
        session.add(other)
        session.commit()
    _auth(client, cookie)
    assert client.get(profile_path("theirs")).status_code == 404


def test_profile_requires_a_session(client, world):
    _user, org, _project, _cookie = world()
    r = client.get(profile_path(org.alias), follow_redirects=False)
    assert r.status_code == 303


# --------------------------------------------------------------------------- #
# Profile: GitHub handle
# --------------------------------------------------------------------------- #


def test_github_handle_writes_the_one_existing_column(client, world, db_engine):
    """The page must not introduce a second GitHub handle field.

    It writes `users.github_username` through `update_integration_status`, the
    same method `PUT /api/v1/users/{id}/integrations` uses -- so the CLI, the
    API and this page cannot disagree about what someone's GitHub login is.
    """
    user, org, _project, cookie = world()
    _auth(client, cookie)

    r = client.post(
        f"{profile_path(org.alias)}/github", data={"github_username": " @octocat "}
    )
    assert r.status_code == 200
    with Session(db_engine) as session:
        stored = session.get(User, user.id)
        assert stored.github_username == "octocat", "trimmed, and the @ stripped"
        assert stored.get_integration_status()["github"]["connected"] is True


# --------------------------------------------------------------------------- #
# Profile: board handles
# --------------------------------------------------------------------------- #


def test_picklist_offers_the_board_names_nobody_is_mapped_to(client, world, add_ticket):
    """The primary mapping path, fed from the `unmapped-assignees` capability.

    Auto-matching by email works on Linear and usually not on Jira; on Trello,
    never. So picking your own name off the board's own list is how this
    actually gets done, and the list has to be the *same* one the summary
    footer counts -- both read `SummaryService.unmapped_assignees`.
    """
    _user, org, project, cookie = world()
    add_ticket(project, org, summary="one", assignee="A. Lice")
    add_ticket(project, org, summary="two", assignee="A. Lice")
    add_ticket(project, org, summary="three", assignee="Bo B.")
    # Already attributed, so it is not a candidate.
    add_ticket(project, org, summary="four", assignee="Mapped", assigned_to=_user_id())

    _auth(client, cookie)
    page = client.get(profile_path(org.alias)).text

    assert 'value="A. Lice"' in page and 'value="Bo B."' in page
    assert "Unmapped on this board" in page
    # Ordered by how much work is behind the name, so the busiest is first.
    assert page.index('value="A. Lice"') < page.index('value="Bo B."')


def _user_id() -> str:
    """A user id that is not in the database -- enough to make `assigned_to`
    non-NULL, which is the only property `unmapped_assignees` reads."""
    return str(uuid4())


def test_claiming_a_handle_maps_it_to_the_signed_in_user(
    client, world, add_ticket, db_engine
):
    _user, org, project, cookie = world()
    add_ticket(project, org, assignee="A. Lice")
    _auth(client, cookie)

    r = client.post(
        f"{profile_path(org.alias)}/identities",
        data={"project_id": project.id, "platform": "linear", "handle": "A. Lice"},
    )
    assert r.status_code == 200
    with Session(db_engine) as session:
        row = session.exec(
            select(UserIdentity).where(UserIdentity.handle == "A. Lice")
        ).one()
        assert row.user_id == _user.id
        assert row.project_id == project.id
        assert row.match_source == MatchSource.MANUAL
    assert "A. Lice" in r.text


def test_a_handle_someone_else_holds_names_the_conflict_not_the_person(
    client, world, db_engine
):
    """The exact wording, and the absence of the other user's identity.

    "Already linked to another user" is all a claimant may learn. Naming them
    -- or their email -- would make this form an oracle for who is on the
    board, answerable by guessing display names.
    """
    _user, org, project, cookie = world()
    with Session(db_engine) as session:
        rival = User(
            id=str(uuid4()), email="rival@example.com", full_name="Grace Hopper"
        )
        session.add(rival)
        # In *this* org: the rule is an intra-organisation one, so the rival has
        # to be a member here for the claim to be a conflict at all.
        session.add(
            OrganizationMembership(
                id=str(uuid4()),
                user_id=rival.id,
                organization_id=org.id,
                role=OrganizationRole.MEMBER,
                is_active=True,
            )
        )
        session.add(
            UserIdentity(
                user_id=rival.id,
                project_id=None,
                platform=IdentityPlatform.LINEAR,
                handle="A. Lice",
                match_source=MatchSource.MANUAL,
            )
        )
        session.commit()

    _auth(client, cookie)
    r = client.post(
        f"{profile_path(org.alias)}/identities",
        data={"project_id": project.id, "platform": "linear", "handle": "A. Lice"},
    )

    assert r.status_code == 200
    assert "That handle is already linked to another user" in r.text
    assert "Grace Hopper" not in r.text and "rival@example.com" not in r.text
    with Session(db_engine) as session:
        mine = session.exec(
            select(UserIdentity).where(UserIdentity.user_id == _user.id)
        ).all()
        assert mine == [], "a refused claim must write nothing"


def test_a_refused_claim_leaves_the_existing_mapping_intact(client, world, db_engine):
    """The conflict check runs before the delete, not after.

    Replacing a mapping means removing the old row; doing that first and *then*
    discovering the new handle is taken would leave the person unmapped as the
    price of a rejected attempt.
    """
    _user, org, project, cookie = world()
    with Session(db_engine) as session:
        session.add(
            UserIdentity(
                user_id=_user.id,
                project_id=project.id,
                platform=IdentityPlatform.LINEAR,
                handle="Mine",
                match_source=MatchSource.MANUAL,
            )
        )
        rival = User(id=str(uuid4()), email="r@example.com", full_name="R")
        session.add(rival)
        session.add(
            OrganizationMembership(
                id=str(uuid4()),
                user_id=rival.id,
                organization_id=org.id,
                role=OrganizationRole.MEMBER,
                is_active=True,
            )
        )
        session.add(
            UserIdentity(
                user_id=rival.id,
                project_id=None,
                platform=IdentityPlatform.LINEAR,
                handle="Theirs",
                match_source=MatchSource.MANUAL,
            )
        )
        session.commit()

    _auth(client, cookie)
    client.post(
        f"{profile_path(org.alias)}/identities",
        data={"project_id": project.id, "platform": "linear", "handle": "Theirs"},
    )

    with Session(db_engine) as session:
        still = session.exec(
            select(UserIdentity).where(UserIdentity.user_id == _user.id)
        ).one()
        assert still.handle == "Mine"


def test_overriding_replaces_this_project_s_handle(client, world, db_engine):
    _user, org, project, cookie = world()
    with Session(db_engine) as session:
        session.add(
            UserIdentity(
                user_id=_user.id,
                project_id=project.id,
                platform=IdentityPlatform.LINEAR,
                handle="Old Name",
                match_source=MatchSource.MANUAL,
            )
        )
        session.commit()

    _auth(client, cookie)
    client.post(
        f"{profile_path(org.alias)}/identities",
        data={"project_id": project.id, "platform": "linear", "handle": "New Name"},
    )

    with Session(db_engine) as session:
        rows = session.exec(
            select(UserIdentity).where(UserIdentity.user_id == _user.id)
        ).all()
        assert [r.handle for r in rows] == ["New Name"]


def test_an_email_match_is_labelled_as_one_and_stays_overridable(
    client, world, add_ticket
):
    """A handle nobody claimed, shown as what it is.

    Board sync resolves a Linear assignee by email without writing any
    `user_identity` row, so the mapping exists with nothing to point at. Saying
    "not mapped" beside work that is plainly attributed would be wrong; saying
    nothing about where it came from would leave a name the person may not
    recognise and no way to tell why it is theirs.
    """
    user, org, project, cookie = world()
    add_ticket(project, org, assignee="Ada L.", assigned_to=user.id)

    _auth(client, cookie)
    page = client.get(profile_path(org.alias)).text

    assert "matched by email" in page
    assert "Ada L." in page
    assert "Change" in page, "an auto-matched row must still be overridable"


def test_a_project_with_no_board_says_so_rather_than_offering_a_dead_form(
    client, world
):
    _user, org, _project, cookie = world(with_board=None)
    _auth(client, cookie)
    page = client.get(profile_path(org.alias)).text
    assert "No board connected" in page
    assert 'name="handle"' not in page


# --------------------------------------------------------------------------- #
# The scrum panel
# --------------------------------------------------------------------------- #


def test_no_summary_and_no_identity_each_say_why_and_how(
    client, world, add_ticket, db_engine
):
    """Two empty states, two different fixes, never a blank box.

    Unmapped wins when both apply: generating a summary you cannot be
    attributed in just produces another empty box.
    """
    user, org, project, cookie = world()
    _auth(client, cookie)

    unmapped = client.get(dashboard_path(org.alias)).text
    assert "We can&rsquo;t attribute your work yet" in unmapped
    assert profile_path(org.alias) in unmapped

    # Now the viewer is attributable, so the other reason is the live one.
    add_ticket(project, org, assignee="Ada L.", assigned_to=user.id)
    mapped = client.get(dashboard_path(org.alias)).text
    assert "We haven&rsquo;t generated your summary yet" in mapped
    assert "innoday summary --scrum" in mapped


def test_team_is_the_default_and_yours_appears_only_when_it_exists(
    client, world, add_summary
):
    """Populated for everyone the moment one person runs it.

    A personal-by-default panel would be empty for all but its author, which
    would make the panel worthless on a shared dashboard.
    """
    user, org, project, cookie = world()
    add_summary(org, project, body_markdown="the team shipped things")
    _auth(client, cookie)

    team_only = client.get(dashboard_path(org.alias)).text
    assert "the team shipped things" in team_only
    assert ">Yours<" not in team_only, "no personal summary, so no toggle"

    add_summary(org, project, user_id=user.id, body_markdown="you shipped things")
    with_both = client.get(dashboard_path(org.alias)).text
    assert ">Yours<" in with_both and ">Team<" in with_both
    assert "the team shipped things" in with_both, "still team by default"

    yours = client.get(f"{dashboard_path(org.alias)}?you={project.id}").text
    assert "you shipped things" in yours


def test_five_active_items_maximum_and_the_panel_never_says_five_of_eight(
    client, world, add_summary, add_ticket
):
    """The cap is on the *active* list only, and is never reported.

    The trailing blocks answer a different question ("what is not moving?"), so
    letting them compete for the five would hide the work that is.

    The cap itself stays unannounced. "5 of 8 active shown" described the
    renderer, in the position on the panel a reader looks for a conclusion.
    """
    user, org, project, cookie = world()
    tickets = [
        add_ticket(project, org, summary=f"active {i}", assignee="Ada L.")
        for i in range(8)
    ]
    idle = add_ticket(project, org, summary="stalled thing", assignee="Ada L.")
    orphan = add_ticket(project, org, summary="nobody owns this")

    items = [
        {
            "ticket_id": t.id,
            "assignee_display": "Ada L.",
            "assignee_user_id": user.id,
            "occurred_at": UTC_NOW - timedelta(hours=i),
            "repo": "innoday",
        }
        for i, t in enumerate(tickets)
    ]
    items.append(
        {"ticket_id": idle.id, "assignee_display": "Ada L.", "no_work_detected": True}
    )
    items.append({"ticket_id": orphan.id, "pr_url": "https://github.com/x/y/pull/1"})
    add_summary(org, project, items=items)

    _auth(client, cookie)
    page = client.get(dashboard_path(org.alias)).text

    assert "active shown" not in page, "the cap is not a fact worth a line"
    shown = [f"active {i}" for i in range(8) if f"active {i}" in page]
    assert len(shown) == 5, f"expected five active rows, rendered {shown}"
    # Most recent first: `active 0` is the newest of the eight.
    assert "active 0" in page and "active 7" not in page
    # The trailing blocks are present, and did not eat an active slot.
    assert "No activity in the last 3 days" in page and "stalled thing" in page
    assert "Unassigned — work happening" in page and "nobody owns this" in page


def test_the_unassigned_backlog_is_not_reported_on_the_panel_at_all(
    client, world, add_summary, add_ticket
):
    """The idle count is gone, not merely shortened.

    It was true and unusable: the size of a project's unassigned backlog (221
    tickets on this repo's own project) changes on a different clock from a
    stand-up, and answered no question a reader of one window was asking.
    """
    user, org, project, cookie = world()
    for i in range(4):
        add_ticket(project, org, summary=f"backlog {i}", status=TicketStatus.TODO)
    # A finished ticket is not idle work. Named distinctively on purpose: the
    # assertion below scans the whole document, so a one-word summary collides
    # with any page chrome that happens to contain it -- "closed" matched a CSS
    # comment once.
    add_ticket(project, org, summary="zzfinishedwork", status=TicketStatus.DONE)
    add_summary(org, project)

    _auth(client, cookie)
    page = client.get(dashboard_path(org.alias)).text

    assert "Unassigned — idle" not in page
    assert "4 tickets" not in page
    for i in range(4):
        assert f"backlog {i}" not in page
    assert "zzfinishedwork" not in page


def test_owner_labels_are_team_mode_only_and_mark_the_unmapped(
    client, world, add_summary, add_ticket
):
    """`@Name` in the team roll-up; nothing in a personal one.

    In a personal summary every line is already the viewer's, so prefixing
    their own name to all of them is noise. `(unmapped)` is the same wording
    the CLI and the engine use, so one row never reads two ways.
    """
    user, org, project, cookie = world()
    ticket = add_ticket(project, org, summary="shared work", assignee="Bo B.")
    mine = add_ticket(project, org, summary="my work", assignee="Ada L.")

    add_summary(
        org,
        project,
        items=[
            {
                "ticket_id": ticket.id,
                "assignee_display": "Bo B.",
                "occurred_at": UTC_NOW,
            }
        ],
    )
    add_summary(
        org,
        project,
        user_id=user.id,
        items=[
            {
                "ticket_id": mine.id,
                "assignee_display": "Ada L.",
                "assignee_user_id": user.id,
                "occurred_at": UTC_NOW,
            }
        ],
    )

    _auth(client, cookie)
    team = client.get(dashboard_path(org.alias)).text
    # A bubble of initials, not the handle itself: a column of addresses beside
    # ticket titles spent most of the row's width on something already known. The
    # handle survives in the `title`, so nothing is lost.
    assert "@Bo B. (unmapped)" not in team, "the handle is no longer the label"
    assert 'class="obub unmapped"' in team, "but unmapped is still marked"
    assert 'title="Bo B. &mdash; not mapped to an InnoDay user"' in team or (
        "not mapped to an InnoDay user" in team
    )
    assert ">BB<" in team, "initials from the display name"

    yours = client.get(f"{dashboard_path(org.alias)}?you={project.id}").text
    assert "@Ada L." not in yours, "no @owner in a personal summary"
    assert 'class="obub' not in yours, "and no bubble either -- every line is yours"
    assert "my work" in yours


def test_rows_link_to_the_ticket_and_the_pull_request(
    client, world, add_summary, add_ticket
):
    user, org, project, cookie = world()
    ticket = add_ticket(
        project,
        org,
        summary="linked work",
        assignee="Ada L.",
        external_ticket_id="PF-398",
        url="https://linear.app/hs/issue/PF-398",
    )
    add_summary(
        org,
        project,
        items=[
            {
                "ticket_id": ticket.id,
                "assignee_display": "Ada L.",
                "occurred_at": UTC_NOW,
                "pr_url": "https://github.com/havilandsoftware/innoday/pull/474",
                "pr_state": "open",
            }
        ],
    )

    _auth(client, cookie)
    page = client.get(dashboard_path(org.alias)).text
    assert "https://linear.app/hs/issue/PF-398" in page
    assert "PF-398" in page
    assert "https://github.com/havilandsoftware/innoday/pull/474" in page
    assert "pull request (open)" in page


def test_there_is_no_generate_button(client, world, add_summary):
    """Generation is local, by design -- narration happens in the caller's
    Claude session and there is no server-side LLM call to fire. A button that
    could only say "run this in your terminal" is a worse version of printing
    the command."""
    _user, org, project, cookie = world()
    add_summary(org, project)
    _auth(client, cookie)
    page = client.get(dashboard_path(org.alias)).text
    assert "summaries/generate" not in page
    assert ">Generate<" not in page


# --------------------------------------------------------------------------- #
# Layout
# --------------------------------------------------------------------------- #


def test_the_launch_column_gets_two_thirds_and_stays_responsive(client, world):
    """One third / two thirds, and nothing can force sideways scroll.

    The right column carries the version, the scrum summary and the ticket counts
    -- prose and titles, which need width -- while the left is a list of
    repository names, the shortest text on the card. The split used to be even,
    which gave the most room to the column that needed it least.

    `minmax(0,...)` on both tracks is the other load-bearing half, unchanged:
    without it a long branch name in the summary panel widens the grid past the
    card and the whole page scrolls horizontally.
    """
    _user, org, _project, cookie = world()
    _auth(client, cookie)
    page = client.get(dashboard_path(org.alias)).text

    assert "grid-template-columns:minmax(0,1fr) minmax(0,2fr)" in page
    assert "minmax(0,1fr) minmax(0,1fr); }" not in page.split(".proj-body")[1][:200]
    # Still collapses, because a third of a phone is not a column.
    assert "@media (max-width:780px)" in page
    assert ".proj-body { grid-template-columns:1fr; }" in page


def test_the_owner_bubble_never_leaves_the_title_line(client, world):
    """A 22px circle alone on row two reads as a separate item, not as that row's
    owner. Unwrapped, the title shrinks and wraps inside its own box instead."""
    _user, org, _project, cookie = world()
    _auth(client, cookie)
    page = client.get(dashboard_path(org.alias)).text

    # The row the bubble sits in must not wrap...
    row = [ln for ln in page.splitlines() if ".sitem-top {" in ln]
    assert row, "the summary row rule is gone"
    assert "flex-wrap" not in row[0], f"the bubble can wrap onto its own line: {row[0]}"
    # ...and the bubble pins to the first line of a title that wrapped.
    assert "align-self:flex-start" in page


def test_the_narrative_is_rendered_and_escaped(client, world, add_summary):
    """The prose is the summary; the items are its evidence.

    Rendered as escaped paragraphs rather than parsed as markdown. Parsing
    would mean a dependency or a hand-rolled parser, and either turns text
    somebody typed into a way to inject markup into a page their whole team
    loads.
    """
    _user, org, project, cookie = world()
    add_summary(
        org,
        project,
        body_markdown="Shipped the parser.\n<img src=x onerror=alert(1)>",
    )
    _auth(client, cookie)
    page = client.get(dashboard_path(org.alias)).text

    assert "Shipped the parser." in page
    assert "<img src=x" not in page
    assert "&lt;img src=x" in page


def test_a_global_handle_is_found_and_labelled_as_global(client, world, db_engine):
    """`project_id IS NULL` rows must be matched with IS NULL, not `IN (..., NULL)`.

    In SQL `NULL IN (…)` evaluates to NULL, not true, so putting `None` in an
    IN list silently excludes every global row -- and a person whose only
    handle is the platform-wide one would be told they have none, on both this
    page and the panel's "we can't attribute your work" state.
    """
    user, org, project, cookie = world()
    with Session(db_engine) as session:
        session.add(
            UserIdentity(
                user_id=user.id,
                project_id=None,
                platform=IdentityPlatform.LINEAR,
                handle="Ada Everywhere",
                match_source=MatchSource.MANUAL,
            )
        )
        session.commit()

    _auth(client, cookie)
    profile = client.get(profile_path(org.alias)).text
    assert "Ada Everywhere" in profile
    assert "global" in profile

    dashboard = client.get(dashboard_path(org.alias)).text
    assert "We can&rsquo;t attribute your work yet" not in dashboard


# --------------------------------------------------------------------------- #
# Links: only http(s) reaches an href
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "hostile",
    [
        "javascript:alert('pr')",
        "JavaScript:alert(1)",
        "java\tscript:alert(1)",
        "data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==",
        "//evil.example/pull/1",
        "vbscript:msgbox(1)",
    ],
)
def test_a_hostile_pr_url_never_reaches_an_href(
    client, world, add_summary, add_ticket, hostile
):
    """`esc` escapes; it does not validate a scheme.

    `SummaryItemPayload.pr_url` is unvalidated and lands verbatim in `href`, and
    this app sends no Content-Security-Policy header, so a `javascript:` URL was
    one click away for every member of the org -- on a page they all load. The
    row still renders; it just stops being a link.
    """
    user, org, project, cookie = world()
    ticket = add_ticket(project, org, summary="a real ticket", assignee="Ada L.")
    add_summary(
        org,
        project,
        items=[
            {
                "ticket_id": ticket.id,
                "assignee_display": "Ada L.",
                "assignee_user_id": user.id,
                "pr_url": hostile,
                "occurred_at": UTC_NOW,
            }
        ],
    )

    _auth(client, cookie)
    page = client.get(dashboard_path(org.alias)).text

    assert "a real ticket" in page, "the row itself must still render"
    assert f'href="{hostile}"' not in page
    # Nothing that survived escaping may be sitting in an href either.
    for scheme in ("javascript:", "vbscript:", 'href="//'):
        assert f'href="{scheme}' not in page.lower()
    # `data:` gets the same treatment, minus the page's own tab icon -- a
    # compile-time constant in `_brand_pages.FAVICON_SVG`, not reachable from any
    # input. Stated as "the only one" rather than by deleting it and scanning the
    # rest, so a *second* `data:` href fails this too: the rule stays absolute,
    # with one audited exception rather than a widened scheme list.
    data_hrefs = re.findall(r'href="(data:[^"]*)"', page)
    assert len(data_hrefs) == 1, f"unexpected data: href on the page: {data_hrefs}"
    # Decoded and compared to the source SVG, rather than to what `favicon_link`
    # emits: comparing the page against the same function that wrote it cannot
    # fail, and that is precisely how a truncated URI shipped once -- an
    # unencoded `"` ended the attribute at the SVG's own `xmlns="`.
    prefix = "data:image/svg+xml,"
    assert data_hrefs[0].startswith(prefix)
    assert unquote(data_hrefs[0][len(prefix) :]) == FAVICON_SVG


def test_a_hostile_ticket_url_never_reaches_an_href(
    client, world, add_summary, add_ticket
):
    """Same hole, the other end: `Ticket.url` is whatever the board sent."""
    user, org, project, cookie = world()
    ticket = add_ticket(
        project,
        org,
        summary="synced from a board",
        assignee="Ada L.",
        external_ticket_id="EVIL-1",
        url="javascript:alert('ticket')",
    )
    add_summary(
        org,
        project,
        items=[
            {
                "ticket_id": ticket.id,
                "assignee_display": "Ada L.",
                "assignee_user_id": user.id,
                "occurred_at": UTC_NOW,
            }
        ],
    )

    _auth(client, cookie)
    page = client.get(dashboard_path(org.alias)).text

    assert "EVIL-1" in page, "the reference is still shown, just not linked"
    assert "javascript:" not in page.lower()


def test_an_ordinary_https_url_is_still_a_link(client, world, add_summary, add_ticket):
    """The allowlist must not cost the feature it is protecting."""
    user, org, project, cookie = world()
    ticket = add_ticket(
        project,
        org,
        summary="normal work",
        assignee="Ada L.",
        external_ticket_id="PF-1",
        url="https://linear.app/x/issue/PF-1",
    )
    add_summary(
        org,
        project,
        items=[
            {
                "ticket_id": ticket.id,
                "assignee_display": "Ada L.",
                "assignee_user_id": user.id,
                "pr_url": "https://github.com/havilandsoftware/innoday/pull/9",
                "occurred_at": UTC_NOW,
            }
        ],
    )

    _auth(client, cookie)
    page = client.get(dashboard_path(org.alias)).text

    assert 'href="https://linear.app/x/issue/PF-1"' in page
    assert 'href="https://github.com/havilandsoftware/innoday/pull/9"' in page

    # The reference carries an arrow saying the link leaves InnoDay. Asserted on
    # the rendered anchor, not on the icon constant: a test that only checks the
    # SVG exists would still pass if nothing ever rendered it.
    anchor = re.search(r'<a class="sref"[^>]*>(.*?)</a>', page, re.S)
    assert anchor is not None, "the ticket reference should be a link"
    assert "PF-1" in anchor.group(1)
    assert 'class="ext"' in anchor.group(1)


def test_a_reference_with_no_usable_url_renders_without_a_link_or_an_arrow(
    client, world, add_ticket, add_summary
):
    """An arrow promises a destination. A row whose ticket URL is absent -- or was
    rejected by ``safe_url`` -- has none, so it must render as plain text rather
    than as a link that goes nowhere."""
    user, org, project, cookie = world()
    ticket = add_ticket(project, org, assignee="Ada L.", assigned_to=user.id, url=None)
    add_summary(
        org,
        project,
        items=[
            {
                "ticket_id": ticket.id,
                "assignee_display": "Ada L.",
                "assignee_user_id": user.id,
                "occurred_at": UTC_NOW,
            }
        ],
    )

    _auth(client, cookie)
    page = client.get(dashboard_path(org.alias)).text

    plain = re.search(r'<span class="sref">(.*?)</span>', page, re.S)
    assert plain is not None, "an unlinkable reference should still be shown"
    assert 'class="ext"' not in plain.group(1)


# --------------------------------------------------------------------------- #
# The panel's window is the summary's window
# --------------------------------------------------------------------------- #


def test_a_weekly_summary_is_shown_and_labelled_with_its_own_window(
    client, world, add_summary, add_ticket
):
    """ "No summary generated yet" beside a summary that exists is the bug.

    The panel prefers `3d`, but a team that summarises weekly stores `1w` -- and
    an exact-match lookup answered the empty state, whose advice is to run the
    command they are already running.
    """
    user, org, project, cookie = world()
    ticket = add_ticket(project, org, summary="a week of work", assignee="Ada L.")
    add_summary(
        org,
        project,
        window_spec="1w",
        body_markdown="a productive week",
        items=[
            {
                "ticket_id": ticket.id,
                "assignee_display": "Ada L.",
                "assignee_user_id": user.id,
                "occurred_at": UTC_NOW,
            }
        ],
    )

    _auth(client, cookie)
    page = client.get(dashboard_path(org.alias)).text

    assert "No summary generated yet" not in page
    assert "a week of work" in page
    assert "last week" in page, "the heading must name the window actually shown"
    assert "last 3 days" not in page


def test_the_preferred_window_still_wins_when_both_exist(
    client, world, add_summary, add_ticket
):
    """The fallback is a fallback, not a replacement for the preference."""
    user, org, project, cookie = world()
    add_summary(org, project, window_spec="1w", body_markdown="the weekly one")
    add_summary(org, project, window_spec="3d", body_markdown="the three-day one")

    _auth(client, cookie)
    page = client.get(dashboard_path(org.alias)).text

    assert "the three-day one" in page
    assert "the weekly one" not in page
    assert "last 3 days" in page


# --------------------------------------------------------------------------- #
# Rows with nothing in them
# --------------------------------------------------------------------------- #


def test_an_item_with_nothing_to_say_renders_no_row(
    client, world, add_summary, add_ticket
):
    """An unassigned item with no ticket, title or owner used to emit an empty
    ``<div>`` -- which on a shared dashboard reads as a rendering fault."""
    user, org, project, cookie = world()
    real = add_ticket(project, org, summary="something real")

    add_summary(
        org,
        project,
        items=[
            # Unassigned, has activity, and a ticket to name: a real thin row.
            {"ticket_id": real.id, "repo": "innoday", "occurred_at": UTC_NOW},
            # Unassigned, has activity, and nothing at all to render.
            {"repo": "innoday", "occurred_at": UTC_NOW},
        ],
    )

    _auth(client, cookie)
    page = client.get(dashboard_path(org.alias)).text

    assert "something real" in page
    assert '<div class="sthin"></div>' not in page


def test_a_block_of_only_empty_rows_is_not_drawn_at_all(client, world, add_summary):
    """A heading over nothing is worse than no heading."""
    user, org, project, cookie = world()
    add_summary(
        org,
        project,
        items=[{"repo": "innoday", "occurred_at": UTC_NOW}],
    )

    _auth(client, cookie)
    page = client.get(dashboard_path(org.alias)).text

    assert "Unassigned — work happening" not in page


# --------------------------------------------------------------------------- #
# The panel's own furniture: headings and owners
# --------------------------------------------------------------------------- #


def _panel(page: str) -> str:
    """The scrum panel's markup, with nothing above it -- the stylesheet least.

    **This is the guard, not a convenience.** Every CSS rule in `render.py` is
    inlined into the `<head>` of every response, so `assert "foo" in page` can be
    satisfied by a declaration or a selector rather than by anything rendered --
    which has already produced three false-passing tests in this repo. Slicing
    from the panel's own opening tag, which is below the `</style>`, means nothing
    in the returned string can be stylesheet; the assertion below proves it rather
    than assuming it.
    """
    at = page.index('<div class="scrum">')
    region = page[at:]
    assert "</style>" not in region, "the slice must not contain the inlined CSS"
    return region


def test_the_active_rows_carry_a_heading_like_the_blocks_below_them(
    client, world, add_summary, add_ticket
):
    """The active rows were the one unlabelled run on the panel.

    The narrative above them says what it is and both trailing blocks name
    themselves, so a reader met the tickets with nothing saying these are the ones
    that moved. Same `.sblock` device as those trailing blocks -- they are peer
    sections of one panel.

    Ordering is asserted, not just presence: a heading is only a heading if it is
    above the thing it names.
    """
    user, org, project, cookie = world()
    moving = add_ticket(project, org, summary="actually moving", assignee="Ada L.")
    stalled = add_ticket(project, org, summary="stalled", assignee="Bo B.")
    add_summary(
        org,
        project,
        items=[
            {
                "ticket_id": moving.id,
                "assignee_display": "Ada L.",
                "assignee_user_id": user.id,
                "occurred_at": UTC_NOW,
            },
            {
                "ticket_id": stalled.id,
                "assignee_display": "Bo B.",
                "no_work_detected": True,
            },
        ],
    )

    _auth(client, cookie)
    panel = _panel(client.get(dashboard_path(org.alias)).text)

    assert '<div class="sblock">Active Tickets</div>' in panel
    assert panel.index(">Active Tickets<") < panel.index('class="sitem"'), (
        "the heading must be above the rows it names"
    )
    assert panel.index(">Active Tickets<") < panel.index("No activity in the"), (
        "and above the trailing block, which is a different section"
    )


def test_no_active_rows_means_no_heading_over_nothing(
    client, world, add_summary, add_ticket
):
    """The rule `_summary_thin_block` already follows, applied to this heading too.

    A summary whose only line is idle has an empty active section, and a label
    over an empty section reads as a rendering fault rather than as the absence it
    is.
    """
    user, org, project, cookie = world()
    stalled = add_ticket(project, org, summary="stalled", assignee="Bo B.")
    add_summary(
        org,
        project,
        items=[
            {
                "ticket_id": stalled.id,
                "assignee_display": "Bo B.",
                "no_work_detected": True,
            }
        ],
    )

    _auth(client, cookie)
    panel = _panel(client.get(dashboard_path(org.alias)).text)

    assert "stalled" in panel, "the idle row is still drawn"
    assert 'class="sitem"' not in panel, "there is no active section"
    assert "Active Tickets" not in panel


def test_a_trailing_block_shows_its_owner_as_a_bubble_not_a_handle(
    client, world, add_summary, add_ticket
):
    """One device for one thing, across the whole panel.

    These rows used to print `owner_label` verbatim, so the same person was
    initials in the active rows and `george@havilandsoftware.com` two blocks
    below -- under a class (``sowner``) that had no stylesheet rule at all. The
    full handle survives in the bubble's `title`, exactly as it does above, so the
    assertion is about what is *displayed*, not about the handle being dropped.
    """
    user, org, project, cookie = world()
    stalled = add_ticket(
        project, org, summary="stalled work", assignee="george@havilandsoftware.com"
    )
    add_summary(
        org,
        project,
        items=[
            {
                "ticket_id": stalled.id,
                "assignee_display": "george@havilandsoftware.com",
                "no_work_detected": True,
            }
        ],
    )

    _auth(client, cookie)
    panel = _panel(client.get(dashboard_path(org.alias)).text)

    row = re.search(r'<div class="sthin">(.*?)</div>', panel, re.S)
    assert row, "the idle row is drawn"
    row = row.group(1)

    assert 'class="obub' in row, "the owner is the same bubble the active rows use"
    assert ">GE<" in row, "initials, taken from the handle's local part"
    assert "not mapped to an InnoDay user" in row, (
        "unmapped is still said, in the title"
    )
    # The handle is no longer the row's text. It is still in the `title`, so this
    # has to be about the displayed string rather than about the substring.
    assert ">george@havilandsoftware.com" not in row
    assert "(unmapped)" not in row, "a ring on the bubble, not a suffix on a name"
    assert 'class="sowner"' not in panel, "the ruleless class is gone from the page"


# --------------------------------------------------------------------------- #
# Block recovery, through the real write path
# --------------------------------------------------------------------------- #


def test_idle_rows_posted_by_the_assembler_do_not_eat_the_five_active_slots(
    client, world, add_ticket
):
    """The end-to-end version of the block round trip, and the property it protects.

    Every other panel test builds `SummaryItem` rows directly and sets
    `no_work_detected` by hand, so all of them passed while a summary posted the
    way the CLI posts one stored eight idle lines as active. Nine items, eight of
    them idle: the footer must read "1 of 1", not "5 of 9".
    """
    from src.services.summary_service import Block, SummaryLine

    user, org, project, cookie = world()
    idle = [
        add_ticket(project, org, summary=f"stalled {i}", assignee="Ada L.")
        for i in range(8)
    ]
    moving = add_ticket(project, org, summary="actually moving", assignee="Ada L.")

    items = [
        SummaryLine(
            block=Block.NO_WORK,
            ticket_id=t.id,
            ticket_summary=t.summary,
            assignee_display="Ada L.",
            assignee_user_id=user.id,
        ).to_dict()
        for t in idle
    ]
    items.append(
        SummaryLine(
            block=Block.ACTIVE,
            ticket_id=moving.id,
            ticket_summary=moving.summary,
            assignee_display="Ada L.",
            assignee_user_id=user.id,
            occurred_at=UTC_NOW,
        ).to_dict()
    )

    posted = client.post(
        f"/api/v1/organizations/{org.id}/projects/{project.id}/summaries",
        json={
            "summary_type": "scrum",
            "window_spec": "3d",
            "body_markdown": "one thing moved",
            "items": items,
        },
        headers={"Authorization": f"Bearer {cookie}"},
    )
    assert posted.status_code == 201, posted.text

    _auth(client, cookie)
    page = client.get(dashboard_path(org.alias)).text

    # `.sitem` is the active row; `.sthin` is a trailing-block line. Counting the
    # former is what the removed footer count used to make observable.
    assert page.count('class="sitem"') == 1, "idle rows must not compete for a slot"
    assert "No activity in the last 3 days" in page
    assert "actually moving" in page
    for i in range(8):
        assert f"stalled {i}" in page, "an idle row is still shown, just not as active"


# --------------------------------------------------------------------------- #
# Unmapped assignees: grouped in SQL, and batched across projects
# --------------------------------------------------------------------------- #


def test_unmapped_assignees_group_in_sql_and_batch_across_projects(
    db_engine, world, add_ticket
):
    """One query for every project, and no `Ticket` built to compute a count.

    This used to `select(Ticket)` -- full ORM objects -- once per project, in
    both the panel and the profile page. The answer is a `GROUP BY`; nothing
    here ever needed a `Ticket`.
    """
    from src.services.summary_service import SummaryService

    user, org, project, _cookie = world()
    with Session(db_engine) as session:
        second = Project(
            id=str(uuid4()),
            name="Second",
            alias=f"s{uuid4().hex[:6]}",
            organization_id=org.id,
            description="another",
        )
        session.add(second)
        session.commit()
        session.refresh(second)

    for _ in range(3):
        add_ticket(project, org, assignee="Ada L.")
    add_ticket(project, org, assignee="  Ada L.  ")  # padded: the same person
    add_ticket(project, org, assignee="Bo B.")
    add_ticket(project, org, assignee="   ")  # whitespace is nobody
    add_ticket(second, org, assignee="Cy C.")

    with Session(db_engine) as session:
        grouped = SummaryService(session).unmapped_assignees_by_project(
            [project.id, second.id]
        )

    assert [row["assignee"] for row in grouped[project.id]] == ["Ada L.", "Bo B."]
    assert grouped[project.id][0]["ticket_count"] == 4
    assert grouped[project.id][1]["ticket_count"] == 1
    assert [row["assignee"] for row in grouped[second.id]] == ["Cy C."]


def test_a_project_with_nobody_unmapped_answers_an_empty_list_not_a_gap(
    db_engine, world
):
    """ "None unmapped" and "not looked at" are different facts."""
    from src.services.summary_service import SummaryService

    _user, org, project, _cookie = world()
    with Session(db_engine) as session:
        grouped = SummaryService(session).unmapped_assignees_by_project([project.id])
    assert grouped == {project.id: []}


# --------------------------------------------------------------------------- #
# Issue #501: the dashboard's panel reads must not scale with project count
# --------------------------------------------------------------------------- #


def _count_summary_selects(db_engine):
    """Count SELECTs against `summaries` while the block runs.

    Counting the *query*, not the wall clock: a timing assertion on a suite this
    small measures the machine, and would pass on a fast one no matter how many
    queries ran.

    The list is cleared on entry. A cumulative counter makes the second
    measurement include the first, which reads exactly like a regression — the
    instrument has to be reset or it reports its own history.
    """
    import contextlib

    from sqlalchemy import event

    @contextlib.contextmanager
    def _watch():
        seen = []

        def _before(conn, cursor, statement, params, context, many):
            if "FROM summaries" in statement:
                seen.append(statement)

        event.listen(db_engine, "before_cursor_execute", _before)
        try:
            yield seen
        finally:
            event.remove(db_engine, "before_cursor_execute", _before)

    return _watch


def test_dashboard_summary_queries_do_not_grow_with_project_count(
    client, world, add_summary, db_engine, make_org, signed_in
):
    """Two reads for the whole dashboard, not two per card.

    `project_cards` and `unmapped_counts_for` were both deliberately batched;
    `summary_panel` was the one call in `_render_dashboard` that still issued its
    own pair per project (#501). The assertion is that adding projects does not
    add queries — an absolute number would pin an implementation detail, while
    "flat as N grows" is the property that actually matters.
    """
    from uuid import uuid4

    from src.domain.project import Project

    user, org, project, cookie = world()
    watch = _count_summary_selects(db_engine)
    _auth(client, cookie)

    with watch() as first_seen:
        client.get(dashboard_path(org.alias))
    with_one = len(first_seen)

    with Session(db_engine) as session:
        for i in range(4):
            session.add(
                Project(
                    id=str(uuid4()),
                    organization_id=org.id,
                    alias=f"X{i}",
                    name=f"Extra {i}",
                    description="d",
                )
            )
        session.commit()

    with watch() as second_seen:
        client.get(dashboard_path(org.alias))
    with_five = len(second_seen)

    assert with_five == with_one, (
        f"summary queries grew from {with_one} to {with_five} when the org went "
        "from 1 project to 5 — the panel reads are not batched"
    )
    # The shape matters as much as the count: one statement covering five
    # projects, not five statements that happen to have been counted once.
    assert any("IN (?, ?, ?, ?, ?)" in st for st in second_seen), (
        "expected a single batched IN over all five projects"
    )


# --------------------------------------------------------------------------- #
# The narrated write path: a summary posted without the identifying ids
#
# `get_scrum_summary` hands a narrator `ticket_id`, `ticket_ref` and
# `assignee_user_id` on every line. A model asked to narrate echoes the prose and
# routinely drops all three -- which is how every live summary on this
# deployment came to store lines about no ticket, owned by nobody, and to render
# them as "Untitled" and "(unmapped)". The server fills them back in.
# --------------------------------------------------------------------------- #


def _post_narrated(client, org, project, cookie, items, **kw):
    """Post a summary the way a narrating session actually posts one."""
    body = {
        "summary_type": "scrum",
        "window_spec": "3d",
        "body_markdown": "a couple of things moved",
        "items": items,
    }
    body.update(kw)
    response = client.post(
        f"/api/v1/organizations/{org.id}/projects/{project.id}/summaries",
        json=body,
        headers={"Authorization": f"Bearer {cookie}"},
    )
    assert response.status_code == 201, response.text
    return response


def _stored_items(db_engine, project):
    with Session(db_engine) as session:
        summary = session.exec(
            select(Summary)
            .where(
                Summary.project_id == project.id,
                Summary.superseded_by_id.is_(None),
            )
            .order_by(Summary.created_at.desc())
        ).first()
        assert summary is not None, "no live summary was stored"
        return list(
            session.exec(
                select(SummaryItem)
                .where(SummaryItem.summary_id == summary.id)
                .order_by(SummaryItem.rank)
            ).all()
        )


@pytest.mark.parametrize("ref_field", ["external", "internal"])
def test_a_narrated_line_recovers_its_ticket_from_either_name(
    client, world, add_ticket, db_engine, ref_field
):
    """`ticket_ref` alone is enough, under either name a ticket answers to.

    The board's own key and the internal `{alias}-{number}` are both real names
    for one ticket, and a narrator echoes whichever the assembler gave it.
    """
    user, org, project, cookie = world()
    ticket = add_ticket(
        project,
        org,
        summary="the real title",
        external_ticket_id="ZZ-9",
        project_ref_number=41,
    )
    ref = "ZZ-9" if ref_field == "external" else f"{project.alias}-41"

    _post_narrated(
        client,
        org,
        project,
        cookie,
        [{"ticket_ref": ref, "body_markdown": "still open, no movement"}],
    )

    stored = _stored_items(db_engine, project)
    assert [i.ticket_id for i in stored] == [ticket.id]


def test_a_narrated_line_takes_the_owner_the_ticket_already_resolved(
    client, world, add_ticket, db_engine
):
    """`Ticket.assigned_to` first, because board sync resolved it with more.

    A Linear or Jira ticket carries an *email* that never reaches
    `Ticket.assignee` -- which stores the display name -- so the row is better
    resolved than any later attempt on the string could be.
    """
    user, org, project, cookie = world()
    ticket = add_ticket(
        project,
        org,
        summary="assigned work",
        external_ticket_id="ZZ-1",
        assignee="A Board Name Nobody Registered",
        assigned_to=user.id,
    )

    _post_narrated(
        client,
        org,
        project,
        cookie,
        [
            {
                "ticket_ref": "ZZ-1",
                "assignee_display": "A Board Name Nobody Registered",
                "body_markdown": "moved along",
            }
        ],
    )

    stored = _stored_items(db_engine, project)
    assert [i.ticket_id for i in stored] == [ticket.id]
    assert [i.assignee_user_id for i in stored] == [user.id]


def test_an_address_in_the_assignee_slot_resolves_to_that_person(
    client, world, db_engine
):
    """A narrator often writes an address where the board wrote a name.

    No ticket, no handle registered anywhere -- just `user.email`, which is what
    the resolver's own first branch matches on. This is the case every live
    summary on the deployment hit: the narrator wrote the address and the row
    stored nobody.
    """
    user, org, project, cookie = world()

    _post_narrated(
        client,
        org,
        project,
        cookie,
        [{"assignee_display": user.email, "body_markdown": "reviewing a PR"}],
    )

    stored = _stored_items(db_engine, project)
    assert [i.assignee_user_id for i in stored] == [user.id]


def test_an_id_the_caller_supplied_is_never_replaced(
    client, world, add_ticket, db_engine
):
    """The caller's own claim about its assembly wins.

    Re-deriving it would make one request mean two different things depending on
    our matching -- and the id is tenancy-checked either way.
    """
    user, org, project, cookie = world()
    named = add_ticket(
        project, org, summary="named directly", external_ticket_id="ZZ-2"
    )
    other = add_ticket(
        project, org, summary="pointed at by ref", external_ticket_id="ZZ-3"
    )

    _post_narrated(
        client,
        org,
        project,
        cookie,
        [
            {
                # The ref and the id disagree. The id is what was asserted.
                "ticket_id": named.id,
                "ticket_ref": "ZZ-3",
                "body_markdown": "one line",
            }
        ],
    )

    stored = _stored_items(db_engine, project)
    assert [i.ticket_id for i in stored] == [named.id]
    assert other.id not in [i.ticket_id for i in stored]


def test_a_person_who_resolves_to_nobody_is_still_stored_as_unmapped(
    client, world, db_engine
):
    """Unmatched stays a valid answer -- the marker has to remain reachable.

    A resolver that guessed would attribute one person's work to another, which
    is worse than the "(unmapped)" this is the source of.
    """
    user, org, project, cookie = world()

    _post_narrated(
        client,
        org,
        project,
        cookie,
        [{"assignee_display": "Someone Outside The Org", "body_markdown": "a line"}],
    )

    stored = _stored_items(db_engine, project)
    assert [i.assignee_user_id for i in stored] == [None]
    assert [i.assignee_display for i in stored] == ["Someone Outside The Org"]


def test_a_resolved_narrated_summary_renders_with_a_title_and_no_unmapped(
    client, world, add_ticket, db_engine
):
    """The end-to-end property, stated as the page a person actually reads.

    This is the bug as reported: a narrated summary rendered every line
    "Untitled" and every owner "(unmapped)".
    """
    user, org, project, cookie = world()
    add_ticket(
        project,
        org,
        summary="a ticket with a real name",
        external_ticket_id="ZZ-7",
        assignee=user.email,
        assigned_to=user.id,
    )

    _post_narrated(
        client,
        org,
        project,
        cookie,
        [
            {
                "ticket_ref": "ZZ-7",
                "assignee_display": user.email,
                "body_markdown": "picked this up today",
                "occurred_at": UTC_NOW.isoformat(),
            }
        ],
    )

    _auth(client, cookie)
    page = client.get(dashboard_path(org.alias)).text

    assert "a ticket with a real name" in page
    assert "Untitled" not in page
    assert "(unmapped)" not in page


def test_a_line_with_no_ticket_is_never_labelled_untitled(client, world, add_summary):
    """ "Untitled" named nothing and read as a rendering fault.

    Some lines legitimately have no ticket -- code activity on a branch nobody
    opened one for -- so this has to hold even after the resolution above.
    """
    user, org, project, cookie = world()
    add_summary(
        org,
        project,
        items=[
            {
                "assignee_display": "Ada L.",
                "body_markdown": "a branch with no ticket behind it",
                "repo": "innoday",
                "occurred_at": UTC_NOW,
            }
        ],
    )

    _auth(client, cookie)
    page = client.get(dashboard_path(org.alias)).text

    assert "Untitled" not in page
    assert "a branch with no ticket behind it" in page


def test_a_trailing_block_line_shows_its_prose_when_it_has_no_ticket(
    client, world, add_summary
):
    """The block is shorter because it matters less, not because it says less.

    It used to render ref, title and owner only -- so a line whose ticket was
    never identified showed as a bare name under a heading, and the sentence
    about it, the only thing on the row that said anything, was dropped.
    """
    user, org, project, cookie = world()
    add_summary(
        org,
        project,
        items=[
            {
                "assignee_display": "Ada L.",
                "body_markdown": "in review since Tuesday, nothing since",
                "no_work_detected": True,
            }
        ],
    )

    _auth(client, cookie)
    page = client.get(dashboard_path(org.alias)).text

    assert "No activity in the last 3 days" in page
    assert "in review since Tuesday, nothing since" in page


def test_the_dashboard_empty_state_only_asks_people_who_can_act_on_it(
    client, world, db_engine
):
    """Same rule as the project page, at the other place it is said.

    The dashboard panel renders `_summary_empty` where the project page collapses
    the whole band, so both had to learn the distinction: no handle anywhere is a
    prompt, a handle on another project is an explanation.
    """
    from src.domain.user_identity import IdentityPlatform, MatchSource, UserIdentity

    user, org, project, cookie = world()

    _auth(client, cookie)
    before = client.get(dashboard_path(org.alias)).text
    assert "Map your board handle" in before

    # Scoped to a *different* project, deliberately. A **global** handle
    # (`project_id IS NULL`) would make the viewer attributable here too --
    # `viewer_has_identity` matches it on purpose -- so it would land on the
    # "no summary generated yet" state instead, and prove nothing about this rule.
    with Session(db_engine) as session:
        elsewhere = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias="EL",
            name="Elsewhere",
            description="d",
        )
        session.add(elsewhere)
        session.commit()
        session.add(
            UserIdentity(
                user_id=user.id,
                project_id=elsewhere.id,
                platform=IdentityPlatform.GITHUB,
                handle="ada",
                match_source=MatchSource.MANUAL,
            )
        )
        session.commit()

    after = client.get(dashboard_path(org.alias)).text
    assert "Map your board handle" not in after
    assert "None of your handles are on this board" in after


def test_a_summary_row_shows_connection_icons_not_a_branch_name(
    client, world, add_summary, add_ticket
):
    """`bps-api · refactor/BPAI-367-v1-types` was the longest string on the row
    and the least readable thing on it. Two icons carry it in less room and link
    to the same places -- green connected, grey not.
    """
    user, org, project, cookie = world()
    wired = add_ticket(
        project,
        org,
        summary="has code and a board issue",
        external_ticket_id="ZZ-1",
        url="https://linear.app/x/issue/ZZ-1",
    )
    bare = add_ticket(project, org, summary="has neither")
    add_summary(
        org,
        project,
        items=[
            {
                "ticket_id": wired.id,
                "assignee_display": "Ada Lovelace",
                "assignee_user_id": user.id,
                "repo": "bps-api",
                "branch": "refactor/ZZ-1-v1-types",
                "pr_url": "https://github.com/hs/bps-api/pull/595",
                "pr_state": "open",
                "occurred_at": UTC_NOW,
            },
            {
                "ticket_id": bare.id,
                "assignee_display": "Ada Lovelace",
                "assignee_user_id": user.id,
                "occurred_at": UTC_NOW,
            },
        ],
    )

    _auth(client, cookie)
    page = client.get(dashboard_path(org.alias)).text

    # The branch name is gone; the PR is reachable through the icon instead.
    assert "refactor/ZZ-1-v1-types" not in page
    assert "bps-api &middot;" not in page and "bps-api ·" not in page
    assert "https://github.com/hs/bps-api/pull/595" in page

    # One connected row and one unconnected one, so both states are asserted from
    # the same page rather than inferred from one.
    assert page.count('class="cx on"') == 2, "the wired row: board + code, both green"
    assert page.count('class="cx"') == 2, "the bare row: board + code, both grey"
    assert "No pull request on this ticket" in page
    assert "Not linked to a board issue" in page
    # The divider between code and board.
    assert 'class="cxsep"' in page


def test_the_owner_is_a_bubble_and_the_handle_only_a_tooltip(
    client, world, add_summary, add_ticket
):
    """Board handles are addresses or logins, and a column of those beside ticket
    titles spends most of the row on something the reader already knows."""
    user, org, project, cookie = world()
    ticket = add_ticket(project, org, summary="somebody's work")
    add_summary(
        org,
        project,
        items=[
            {
                "ticket_id": ticket.id,
                "assignee_display": "george@havilandsoftware.com",
                "assignee_user_id": user.id,
                "occurred_at": UTC_NOW,
            }
        ],
    )

    _auth(client, cookie)
    page = client.get(dashboard_path(org.alias)).text

    # Not shown as the label...
    assert ">george@havilandsoftware.com<" not in page
    # ...but not lost either: the handle is the bubble's title.
    assert 'title="george@havilandsoftware.com"' in page
    # An address has no surname, so the local part supplies the initials.
    assert ">GE<" in page


# --------------------------------------------------------------------------- #
# Handle mapping over the API (#569)
# --------------------------------------------------------------------------- #


def _identities(client, org, cookie, **params):
    q = "&".join(f"{k}={v}" for k, v in params.items())
    return client.get(
        f"/api/v1/organizations/{org.id}/identities" + (f"?{q}" if q else ""),
        headers={"Authorization": f"Bearer {cookie}"},
    )


def test_mapping_a_github_login_over_the_api_makes_it_resolve(
    client, world, add_ticket, db_engine
):
    """The end-to-end property: a mapping that changes what summaries attribute.

    Before #569 there was no API path at all — the Team page was the only way, so
    this could not be scripted, could not happen during onboarding, and had to be
    done by hand in the database when `dgillen27` resolved to nobody.
    """
    from src.services.identity_resolution import IdentityResolutionService

    user, org, project, cookie = world()

    posted = client.post(
        f"/api/v1/organizations/{org.id}/identities",
        json={"user": user.email, "platform": "github", "handle": "dgillen27"},
        headers={"Authorization": f"Bearer {cookie}"},
    )
    assert posted.status_code == 201, posted.text
    body = posted.json()
    # Which store it landed in is surfaced, because it decides what an unmap has
    # to touch and a caller should not infer it from the platform.
    assert body["stored_as"] == "github_username"
    assert body["user_email"] == user.email

    # The assertion that matters: resolution now answers.
    with Session(db_engine) as session:
        match = IdentityResolutionService.resolve(
            session,
            organization_id=org.id,
            project_id=project.id,
            platform=IdentityPlatform.GITHUB,
            assignee=BoardAssignee(display_name="dgillen27"),
        )
        assert match is not None and match.user.id == user.id

    listed = _identities(client, org, cookie).json()
    assert any(r["handle"] == "dgillen27" for r in listed)

    # And it is reversible, because a wrong mapping reattributes somebody's work
    # in every summary that follows.
    dropped = client.delete(
        f"/api/v1/organizations/{org.id}/identities?platform=github&handle=dgillen27",
        headers={"Authorization": f"Bearer {cookie}"},
    )
    assert dropped.status_code == 204
    with Session(db_engine) as session:
        assert (
            IdentityResolutionService.resolve(
                session,
                organization_id=org.id,
                project_id=project.id,
                platform=IdentityPlatform.GITHUB,
                assignee=BoardAssignee(display_name="dgillen27"),
            )
            is None
        )


def test_a_board_handle_is_stored_as_a_user_identity_row(client, world):
    """Two stores, one question. A board handle is not a GitHub login."""
    user, org, project, cookie = world()
    posted = client.post(
        f"/api/v1/organizations/{org.id}/identities",
        json={"user": user.email, "platform": "linear", "handle": "Ada L."},
        headers={"Authorization": f"Bearer {cookie}"},
    )
    assert posted.status_code == 201, posted.text
    assert posted.json()["stored_as"] == "user_identity"
    assert posted.json()["id"] is not None, "a row has an id; a column does not"


def test_a_handle_already_held_by_someone_else_is_a_409_that_names_no_names(
    client, world, db_engine
):
    """The message names the handle and **not** its current owner.

    Echoing the owner would turn a mapping call into a way to enumerate who is on
    the board by guessing display names — the same reasoning the profile page's
    duplicate-handle message follows.
    """
    user, org, project, cookie = world()
    with Session(db_engine) as session:
        other = User(
            id=str(uuid4()),
            email="someone.else@example.com",
            full_name="Someone Else",
        )
        session.add(other)
        session.commit()
        session.add(
            OrganizationMembership(
                id=str(uuid4()),
                user_id=other.id,
                organization_id=org.id,
                role=OrganizationRole.MEMBER,
                is_active=True,
            )
        )
        session.add(
            UserIdentity(
                user_id=other.id,
                platform=IdentityPlatform.LINEAR,
                handle="Contested Name",
                match_source=MatchSource.MANUAL,
            )
        )
        session.commit()

    posted = client.post(
        f"/api/v1/organizations/{org.id}/identities",
        json={"user": user.email, "platform": "linear", "handle": "Contested Name"},
        headers={"Authorization": f"Bearer {cookie}"},
    )
    assert posted.status_code == 409
    detail = posted.json()["detail"]
    assert "Contested Name" in detail
    assert "someone.else@example.com" not in detail, "the owner is not disclosed"


def test_mapping_someone_outside_the_organization_is_refused(client, world, db_engine):
    """404, and the message says why it would not have worked anyway.

    Resolution refuses to match a non-member on every path, so a mapping to one
    would be a row that looks right and never fires.
    """
    user, org, project, cookie = world()
    with Session(db_engine) as session:
        session.add(
            User(
                id=str(uuid4()),
                email="outsider@elsewhere.example",
                full_name="An Outsider",
            )
        )
        session.commit()

    posted = client.post(
        f"/api/v1/organizations/{org.id}/identities",
        json={
            "user": "outsider@elsewhere.example",
            "platform": "github",
            "handle": "outsider",
        },
        headers={"Authorization": f"Bearer {cookie}"},
    )
    assert posted.status_code == 404
    assert "not an active member" in posted.json()["detail"]


def test_unmapping_something_that_is_not_mapped_is_not_an_error(client, world):
    """The caller's intent is already satisfied, and there is nothing they could
    do about a 404."""
    user, org, project, cookie = world()
    resp = client.delete(
        f"/api/v1/organizations/{org.id}/identities?platform=github&handle=nobody",
        headers={"Authorization": f"Bearer {cookie}"},
    )
    assert resp.status_code == 204


def _join_org(db_engine, org, *, role=OrganizationRole.MEMBER, user=None):
    """Add someone to an org — a new member with their own token by default."""
    from src.domain.cli_token import hash_cli_token

    raw = generate_cli_token(kind="oauth")
    created = user is None
    with Session(db_engine) as session:
        if created:
            user = User(
                id=str(uuid4()),
                email=f"{uuid4().hex[:8]}@example.com",
                full_name="A Plain Member",
            )
            session.add(user)
        session.add(
            CLIToken(
                user_id=user.id,
                token_hash=hash_cli_token(raw),
                name=SESSION_TOKEN_NAME,
                expires_at=UTC_NOW + timedelta(days=7),
            )
        )
        session.add(
            OrganizationMembership(
                id=str(uuid4()),
                user_id=user.id,
                organization_id=org.id,
                role=role,
                is_active=True,
            )
        )
        session.commit()
        if created:
            # Only the row this session owns: refreshing an instance that came
            # from another session raises rather than reloading it, and a commit
            # expires the ones it does own.
            session.refresh(user)
        return user, raw


def test_a_plain_member_may_read_the_mappings_but_not_change_them(
    client, world, db_engine
):
    """#569's "a non-admin gets 403", which nothing could previously observe.

    Both write routes ask for ADMIN, and dropping that argument from either
    decorator left the whole suite green: `world()` mints its user as an ADMIN,
    so every other test here runs as one and none can tell a guarded route from
    an unguarded one. Reading stays open on purpose — knowing who a handle
    belongs to is not a privilege, reassigning somebody's work is.
    """
    _admin, org, _project, _cookie = world()
    _member, token = _join_org(db_engine, org, role=OrganizationRole.MEMBER)
    headers = {"Authorization": f"Bearer {token}"}

    assert (
        client.get(
            f"/api/v1/organizations/{org.id}/identities", headers=headers
        ).status_code
        == 200
    )

    posted = client.post(
        f"/api/v1/organizations/{org.id}/identities",
        json={"user": _member.email, "platform": "github", "handle": "sneaky"},
        headers=headers,
    )
    assert posted.status_code == 403
    assert "ADMIN" in posted.json()["detail"]

    deleted = client.delete(
        f"/api/v1/organizations/{org.id}/identities?platform=github&handle=sneaky",
        headers=headers,
    )
    assert deleted.status_code == 403
    assert "ADMIN" in deleted.json()["detail"]


def test_another_organizations_mapping_is_neither_listed_nor_deletable(
    client, world, db_engine
):
    """The tenancy boundary, on the read side and the destroy side.

    `UserIdentity` carries no `organization_id`, so filtering on "is this row's
    owner a member of *my* org" is not a scope: one person in two orgs — a
    contractor, or any platform member, for whom membership is synthesised
    everywhere — was enough for an admin of org A to list org B's project-scoped
    row (leaking its handle and project id) and then silently delete it, so org
    B's tickets stopped resolving. Org is the tenancy boundary; the row reaches
    its org through `Project.organization_id`.
    """
    admin, org_a, _project_a, cookie_a = world()
    _other_admin, org_b, project_b, cookie_b = world()
    # The one person in both — which is all it took.
    _join_org(db_engine, org_b, role=OrganizationRole.MEMBER, user=admin)
    with Session(db_engine) as session:
        session.add(
            UserIdentity(
                user_id=admin.id,
                project_id=project_b.id,
                platform=IdentityPlatform.LINEAR,
                handle="Sam Patel",
                match_source=MatchSource.MANUAL,
            )
        )
        session.commit()

    def rows_for(org, cookie):
        listed = _identities(client, org, cookie).json()
        return [r["handle"] for r in listed]

    assert "Sam Patel" not in rows_for(org_a, cookie_a), "org B's row is not org A's"
    assert "Sam Patel" in rows_for(org_b, cookie_b), "and it is still org B's own"

    dropped = client.delete(
        f"/api/v1/organizations/{org_a.id}/identities"
        "?platform=linear&handle=Sam%20Patel",
        headers={"Authorization": f"Bearer {cookie_a}"},
    )
    # 204 either way: from org A's side there is nothing there to unmap, which
    # is the same answer as unmapping something that was never mapped.
    assert dropped.status_code == 204
    with Session(db_engine) as session:
        surviving = session.exec(
            select(UserIdentity).where(UserIdentity.handle == "Sam Patel")
        ).all()
        assert len(surviving) == 1, "org A must not have deleted org B's mapping"
        assert surviving[0].project_id == project_b.id


# --------------------------------------------------------------------------- #
# Listing what is *not* mapped (#598)
# --------------------------------------------------------------------------- #


def _add_pull_request(db_engine, org, project, *, login, number=1):
    """A repository on this project with one open PR by `login`."""
    from src.domain.repository import Repository
    from src.domain.repository_pull_request import RepositoryPullRequest

    with Session(db_engine) as session:
        name = f"repo-{uuid4().hex[:6]}"
        repo = Repository(
            id=str(uuid4()),
            name=name,
            full_name=f"hs/{name}",
            url=f"https://github.com/hs/{name}",
            organization_id=org.id,
        )
        session.add(repo)
        session.commit()
        session.add(
            ProjectRepository(
                id=str(uuid4()),
                project_id=project.id,
                repository_id=repo.id,
                is_active=True,
            )
        )
        session.add(
            RepositoryPullRequest(
                repository_id=repo.id,
                number=number,
                title="A pull request",
                url=f"https://github.com/hs/{name}/pull/{number}",
                author_login=login,
            )
        )
        session.commit()


def test_unmapped_lists_the_handles_that_resolve_to_nobody(
    client, world, add_ticket, db_engine
):
    """The half of #569 that was never built.

    Without it the only way to discover *which* handles need mapping was to read
    the Team page -- the browser dependency the API and CLI existed to remove.
    Both kinds appear, because "who is this?" is one question whether the name
    came off a board or off a commit.
    """
    _user, org, project, cookie = world()
    add_ticket(project, org, summary="one", assignee="A. Lice")
    add_ticket(project, org, summary="two", assignee="A. Lice")
    # Already attributed, so nobody needs to map it.
    add_ticket(project, org, summary="three", assignee="Mapped", assigned_to=_user_id())
    _add_pull_request(db_engine, org, project, login="dgillen27")

    rows = _identities(client, org, cookie, unmapped="true").json()
    by_handle = {r["handle"]: r for r in rows}

    assert "A. Lice" in by_handle, "a board assignee nothing could attribute"
    assert by_handle["A. Lice"]["kind"] == "board"
    assert "2 tickets" in by_handle["A. Lice"]["detail"]
    assert "dgillen27" in by_handle, "a PR author matching no member's login"
    assert by_handle["dgillen27"]["kind"] == "commit"
    assert "Mapped" not in by_handle, "an attributed assignee is not unmapped"

    # And the default listing is still the mappings, not this.
    assert all("kind" not in r for r in _identities(client, org, cookie).json())


def test_another_organizations_unmapped_handles_are_not_listed(
    client, world, add_ticket, db_engine
):
    """The #593 hole, on the route that answers the opposite question.

    A member of two orgs is ordinary, and `verify_org_membership` synthesises
    ADMIN for any platform member — so "the caller belongs here" scopes nothing.
    The scope is the project filter: `unmapped_handles` derives board handles
    through `Ticket.project_id` and commit logins through `ProjectRepository`,
    so a listing built from every project rather than this org's would hand one
    tenant's board names and PR authors to the other.
    """
    admin, org_a, _project_a, cookie_a = world()
    _other_admin, org_b, project_b, cookie_b = world()
    # The one person in both — which is all it took last time.
    _join_org(db_engine, org_b, role=OrganizationRole.MEMBER, user=admin)
    add_ticket(project_b, org_b, summary="theirs", assignee="Sam Patel")
    _add_pull_request(db_engine, org_b, project_b, login="theirlogin")

    def unmapped_handles_for(org, cookie):
        listed = _identities(client, org, cookie, unmapped="true").json()
        return {r["handle"] for r in listed}

    assert unmapped_handles_for(org_b, cookie_b) >= {"Sam Patel", "theirlogin"}, (
        "org B still sees its own"
    )
    leaked = unmapped_handles_for(org_a, cookie_a)
    assert "Sam Patel" not in leaked, "org B's board assignee is not org A's to read"
    assert "theirlogin" not in leaked, "nor is org B's pull-request author"


def test_unmapped_cannot_be_narrowed_by_platform(client, world):
    """Refused, not silently ignored.

    An unmapped board handle is a `Ticket.assignee` string grouped across
    whatever boards a project has; the grouping carries no `source_platform`, so
    `?platform=linear` could only be honoured by inventing one. Dropping the
    filter quietly would answer a different question while looking like it had.
    """
    _user, org, _project, cookie = world()

    refused = _identities(client, org, cookie, unmapped="true", platform="linear")
    assert refused.status_code == 422
    assert "kind" in refused.json()["detail"]


def test_a_plain_member_may_read_what_is_unmapped(client, world, db_engine):
    """Same rule as the mapping listing: reading is not a privilege.

    Knowing which names still need somebody is what an operator starts from, and
    gating it to ADMIN would leave the person who can see the problem unable to
    see it.
    """
    _admin, org, project, _cookie = world()
    _member, token = _join_org(db_engine, org, role=OrganizationRole.MEMBER)
    with Session(db_engine) as session:
        session.add(
            Ticket(
                summary="unowned",
                organization_id=org.id,
                project_id=project.id,
                assignee="A. Lice",
            )
        )
        session.commit()

    listed = client.get(
        f"/api/v1/organizations/{org.id}/identities?unmapped=true",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert listed.status_code == 200
    assert [r["handle"] for r in listed.json()] == ["A. Lice"]


def test_a_github_login_mapped_by_a_user_identity_row_is_not_unmapped(
    client, world, db_engine
):
    """One endpoint must not answer both ways in the same breath.

    Since #593 an explicit `user_identity` row *beats* `users.github_username`
    in `resolve`. The commit half of `unmapped_handles` tested the column alone,
    so a login mapped by a row with the column left NULL resolved to a real
    person, was listed by `GET .../identities` as mapped, and was listed by
    `?unmapped=true` as unmapped -- same route, same request cycle. Following
    the CLI's own printed next step then answered **409 "already mapped to
    another member"** without naming them: a handle the tool says is unmapped,
    refuses to map, and will not identify, on the exact `dgillen27` case #569
    exists to remove.

    Not an exotic state. `POST /ui/{org_ref}/profile/identities` and the auth
    claim route both accept `github`, so any user can create the row from the
    profile page with no admin involved -- and unlike the board half there is no
    later sync to reconcile it, so the divergence is permanent.

    Both scopes a row can have are covered: project-scoped, and global
    (`project_id IS NULL`), which `resolve` honours for a member of the org.
    """
    from src.services.identity_resolution import IdentityResolutionService

    user, org, project, cookie = world()
    with Session(db_engine) as session:
        for handle, pid in (("dgillen27", project.id), ("globaldev", None)):
            session.add(
                UserIdentity(
                    user_id=user.id,
                    project_id=pid,
                    platform=IdentityPlatform.GITHUB,
                    handle=handle,
                    match_source=MatchSource.MANUAL,
                )
            )
        # The column is NULL -- the row is the whole mapping, which is the case.
        assert session.get(User, user.id).github_username is None
        session.commit()
    _add_pull_request(db_engine, org, project, login="dgillen27")
    _add_pull_request(db_engine, org, project, login="globaldev", number=2)

    with Session(db_engine) as session:
        for handle in ("dgillen27", "globaldev"):
            match = IdentityResolutionService.resolve(
                session,
                organization_id=org.id,
                project_id=project.id,
                platform=IdentityPlatform.GITHUB,
                assignee=BoardAssignee(display_name=handle),
            )
            assert match is not None and match.user.id == user.id, handle

    mapped = {r["handle"] for r in _identities(client, org, cookie).json()}
    assert {"dgillen27", "globaldev"} <= mapped, "the default listing calls them mapped"

    unmapped = {
        r["handle"] for r in _identities(client, org, cookie, unmapped="true").json()
    }
    assert "dgillen27" not in unmapped, "and the same route must not disagree"
    assert "globaldev" not in unmapped, "a global row resolves here too"


def test_another_organizations_mapping_does_not_hide_this_org_s_unmapped_login(
    client, world, db_engine
):
    """The `known` set is the org's, not the platform's.

    `select(User.github_username)` carried no org or membership filter, so *any*
    tenant's mapping suppressed a row here while `resolve`, which requires
    active membership, answered `None` for the same login. It hides rather than
    leaks -- but another tenant's data still decided what this one was shown,
    and a contractor shared across orgs is exactly the population this listing
    is for.

    Both halves of the set are pinned, and by two *different* people, because
    they are scoped by different means and one of those means is not enough on
    its own:

    * `ghostlogin` sits on a user who is not in org A at all -- the column is
      scoped by membership in *this* org.
    * `ghostrow` sits on a **contractor who is an active member of both**, in a
      `user_identity` row scoped to org B's project. Membership therefore says
      "yes" and the row is still not org A's, so the scope has to come from
      `project_id -> Project.organization_id`. That is #593's finding exactly:
      `UserIdentity` carries no `organization_id`, and membership alone is not a
      tenancy boundary -- `verify_org_membership` synthesises ADMIN for any
      platform member. `resolve` agrees, because a row scoped to another
      project is neither an override for this one nor global.
    """
    from src.services.identity_resolution import IdentityResolutionService

    _admin, org_a, project_a, cookie_a = world()
    outsider, org_b, project_b, _cookie_b = world()
    contractor, _token = _join_org(db_engine, org_a, role=OrganizationRole.MEMBER)
    _join_org(db_engine, org_b, role=OrganizationRole.MEMBER, user=contractor)
    with Session(db_engine) as session:
        them = session.get(User, outsider.id)
        them.github_username = "ghostlogin"
        session.add(them)
        session.add(
            UserIdentity(
                user_id=contractor.id,
                project_id=project_b.id,
                platform=IdentityPlatform.GITHUB,
                handle="ghostrow",
                match_source=MatchSource.MANUAL,
            )
        )
        session.commit()
    _add_pull_request(db_engine, org_a, project_a, login="ghostlogin")
    _add_pull_request(db_engine, org_a, project_a, login="ghostrow", number=2)

    # Nobody in org A is either person, and resolution says so.
    with Session(db_engine) as session:
        for handle in ("ghostlogin", "ghostrow"):
            assert (
                IdentityResolutionService.resolve(
                    session,
                    organization_id=org_a.id,
                    project_id=project_a.id,
                    platform=IdentityPlatform.GITHUB,
                    assignee=BoardAssignee(display_name=handle),
                )
                is None
            ), handle

    listed = {
        r["handle"]
        for r in _identities(client, org_a, cookie_a, unmapped="true").json()
    }
    assert "ghostlogin" in listed, "another org's github_username is not a mapping here"
    assert "ghostrow" in listed, "nor is another org's project-scoped identity row"


def test_a_github_login_already_held_by_a_user_identity_row_is_a_409(
    client, world, db_engine
):
    """Both stores are consulted for a clash, or the mapping steals one.

    The GitHub path checked only `users.github_username`, so mapping a login
    that somebody already held as a `user_identity` row answered 201 and — with
    the row now beating the column — left the older, deliberate mapping unable
    to resolve. Every commit of theirs would be reattributed, which is the exact
    harm this route exists to prevent.
    """
    from src.services.identity_resolution import IdentityResolutionService

    claimant, org, project, cookie = world()
    holder, _token = _join_org(db_engine, org, role=OrganizationRole.MEMBER)
    with Session(db_engine) as session:
        session.add(
            UserIdentity(
                user_id=holder.id,
                project_id=project.id,
                platform=IdentityPlatform.GITHUB,
                handle="octo",
                match_source=MatchSource.MANUAL,
            )
        )
        session.commit()

    posted = client.post(
        f"/api/v1/organizations/{org.id}/identities",
        json={"user": claimant.email, "platform": "github", "handle": "octo"},
        headers={"Authorization": f"Bearer {cookie}"},
    )
    assert posted.status_code == 409, posted.text
    detail = posted.json()["detail"]
    assert "octo" in detail
    assert holder.email not in detail, "the owner is not disclosed"

    # And the mapping that was already there still answers.
    with Session(db_engine) as session:
        match = IdentityResolutionService.resolve(
            session,
            organization_id=org.id,
            project_id=project.id,
            platform=IdentityPlatform.GITHUB,
            assignee=BoardAssignee(display_name="octo"),
        )
        assert match is not None and match.user.id == holder.id


def test_mapping_a_board_handle_reattributes_the_tickets_already_synced(
    client, world, add_ticket, db_engine
):
    """ "One write is enough" is only true if the board's history moves too.

    A GitHub login is re-resolved on every summary run; `board_sync_service`
    resolves once and *persists* `ticket.assigned_to`. So without this a Linear
    mapping fixed future syncs and left every ticket already in the table
    unattributed, with nothing in the response to say so.
    """
    user, org, project, cookie = world()
    mine = add_ticket(
        project, org, summary="Mine", assignee="Ada L.", source_platform="linear"
    )
    theirs = add_ticket(
        project,
        org,
        summary="Someone else's",
        assignee="Someone Else",
        source_platform="linear",
    )
    other_board = add_ticket(
        project, org, summary="Jira", assignee="Ada L.", source_platform="jira"
    )

    posted = client.post(
        f"/api/v1/organizations/{org.id}/identities",
        json={"user": user.email, "platform": "linear", "handle": "Ada L."},
        headers={"Authorization": f"Bearer {cookie}"},
    )
    assert posted.status_code == 201, posted.text
    assert posted.json()["tickets_reattributed"] == 1

    with Session(db_engine) as session:
        assert session.get(Ticket, mine.id).assigned_to == user.id
        assert session.get(Ticket, theirs.id).assigned_to is None
        # A Jira ticket is not a Linear mapping's business, however the board
        # spells the name.
        assert session.get(Ticket, other_board.id).assigned_to is None

    # Unmapping releases them again, or the undo would leave the wrong person
    # credited on everything already synced.
    dropped = client.delete(
        f"/api/v1/organizations/{org.id}/identities?platform=linear&handle=Ada%20L.",
        headers={"Authorization": f"Bearer {cookie}"},
    )
    assert dropped.status_code == 204
    with Session(db_engine) as session:
        assert session.get(Ticket, mine.id).assigned_to is None


def test_unmapping_a_github_login_does_not_leave_it_connected_without_one(
    client, world, db_engine
):
    """`github_connected` means "we know their login", so it goes with it.

    The profile page writes the pair as `connected=bool(handle)`. Blanking the
    login alone left the profile page and `GET /users/{id}/integrations`
    reporting a connected account with no username.
    """
    user, org, _project, cookie = world()
    assert (
        client.post(
            f"/api/v1/organizations/{org.id}/identities",
            json={"user": user.email, "platform": "github", "handle": "octocat"},
            headers={"Authorization": f"Bearer {cookie}"},
        ).status_code
        == 201
    )
    with Session(db_engine) as session:
        assert session.get(User, user.id).github_connected is True, (
            "mapping a login is the API saying we know it"
        )

    client.delete(
        f"/api/v1/organizations/{org.id}/identities?platform=github&handle=octocat",
        headers={"Authorization": f"Bearer {cookie}"},
    )

    with Session(db_engine) as session:
        stored = session.get(User, user.id)
        assert stored.github_username is None
        assert stored.get_integration_status()["github"]["connected"] is False


def test_a_ticket_with_work_in_two_repos_gets_an_icon_for_each(
    client, world, add_summary, add_ticket, db_engine
):
    """The point of #579, and what a ticket actually looks like.

    A `SummaryItem` stores one `pr_url`, so before the branch was stored a ticket
    with code in three repositories rendered as a ticket with code in one. The
    branch is the only thing on a pull request that names a ticket, and nothing
    stored it.
    """
    from src.domain.repository import Repository
    from src.domain.repository_pull_request import RepositoryPullRequest

    user, org, project, cookie = world()
    ticket = add_ticket(
        project, org, summary="spans two repos", external_ticket_id="ZZ-9"
    )
    with Session(db_engine) as session:
        for name, number, branch, draft in (
            ("bps-api", 595, "refactor/ZZ-9-types", False),
            ("bps-ui", 12, "zz-9-the-ui-half", True),
            # A branch naming no ticket must link to nothing rather than guess.
            ("bps-api", 999, "chore/bump-deps", False),
        ):
            repo = session.exec(
                select(Repository).where(Repository.name == name)
            ).first()
            if repo is None:
                repo = Repository(
                    id=str(uuid4()),
                    name=name,
                    full_name=f"hs/{name}",
                    url=f"https://github.com/hs/{name}",
                    organization_id=org.id,
                )
                session.add(repo)
                session.commit()
                session.add(
                    ProjectRepository(
                        id=str(uuid4()),
                        project_id=project.id,
                        repository_id=repo.id,
                        is_active=True,
                    )
                )
                session.commit()
            session.add(
                RepositoryPullRequest(
                    repository_id=repo.id,
                    number=number,
                    title=f"PR {number}",
                    url=f"https://github.com/hs/{name}/pull/{number}",
                    head_ref=branch,
                    is_draft=draft,
                )
            )
        session.commit()

    add_summary(
        org,
        project,
        items=[
            {
                "ticket_id": ticket.id,
                "assignee_display": "Ada Lovelace",
                "assignee_user_id": user.id,
                "occurred_at": UTC_NOW,
            }
        ],
    )

    _auth(client, cookie)
    page = client.get(dashboard_path(org.alias)).text

    # One icon per repository that has a PR naming this ticket -- and only those.
    assert "https://github.com/hs/bps-api/pull/595" in page
    assert "https://github.com/hs/bps-ui/pull/12" in page
    assert "pull/999" not in page, "a branch naming no ticket links to nothing"
    # The draft reads as pending rather than as done.
    assert "cx on draft" in page
    assert "bps-ui &mdash; #12 (draft)" in page or "#12 (draft)" in page


def test_the_stored_single_pr_still_shows_when_no_branch_matches(
    client, world, add_summary, add_ticket
):
    """A summary written before `head_ref` existed keeps the one link it had.

    Falling back matters because the join only sees pull requests synced *since*
    the column was added -- without this, every historical summary would lose its
    PR link the moment the join shipped.
    """
    user, org, project, cookie = world()
    ticket = add_ticket(project, org, summary="older summary row")
    add_summary(
        org,
        project,
        items=[
            {
                "ticket_id": ticket.id,
                "assignee_display": "Ada Lovelace",
                "assignee_user_id": user.id,
                "repo": "innoday",
                "pr_url": "https://github.com/hs/innoday/pull/1",
                "pr_state": "open",
                "occurred_at": UTC_NOW,
            }
        ],
    )

    _auth(client, cookie)
    page = client.get(dashboard_path(org.alias)).text
    assert "https://github.com/hs/innoday/pull/1" in page


def test_a_pull_request_naming_its_ticket_in_the_title_is_linked(
    client, db_engine, world, add_ticket, add_summary
):
    """The branch is not the only place a ticket reference lives.

    `BPAI-334: property report endpoint` says which ticket it belongs to as
    plainly as any branch name does, and the release and summary views could not
    see it: they read `head_ref` alone, through a hand-rolled parser, while
    `code_activity` had been consulting branch *and* title through the shared
    pattern all along. Two matchers answering one question, and these readers
    had the weaker one.
    """
    from uuid import uuid4

    from sqlmodel import Session

    from src.domain.repository import Repository
    from src.domain.repository_pull_request import RepositoryPullRequest

    user, org, project, cookie = world()
    ticket = add_ticket(
        project, org, summary="titled, not branched", external_ticket_id="ZZ-42"
    )
    with Session(db_engine) as session:
        repo = Repository(
            id=str(uuid4()),
            name="titled-repo",
            full_name="hs/titled-repo",
            url="https://github.com/hs/titled-repo",
            organization_id=org.id,
        )
        session.add(repo)
        session.commit()
        session.add(
            ProjectRepository(
                id=str(uuid4()),
                project_id=project.id,
                repository_id=repo.id,
                is_active=True,
            )
        )
        session.add(
            RepositoryPullRequest(
                id=str(uuid4()),
                repository_id=repo.id,
                number=777,
                title="ZZ-42: the thing, named in the title",
                url="https://github.com/hs/titled-repo/pull/777",
                # **No branch at all.** The query used to require one, so a
                # reference in the title could never be reached however plainly
                # it was written.
                head_ref=None,
                state="open",
            )
        )
        session.commit()

    # The ticket has to be on the summary to be rendered at all -- without this
    # the assertion below passes or fails on whether anything else happened to
    # put it on the page, which is not what is under test.
    add_summary(
        org,
        project,
        items=[
            {
                "ticket_id": ticket.id,
                "assignee_display": "Ada Lovelace",
                "assignee_user_id": user.id,
                "occurred_at": UTC_NOW,
            }
        ],
    )

    _auth(client, cookie)
    page = client.get(dashboard_path(org.alias)).text
    assert "https://github.com/hs/titled-repo/pull/777" in page
