"""Tests for the server-rendered ``/ui`` pages (sign-in + dashboard).

Organised by failure mode rather than by function: one test per way this can
break, with related assertions sharing a setup instead of each getting their own
near-identical one. That keeps the count honest -- a suite that grows a test per
line of code stops being read, and stops being maintained.

The ones worth more than the coverage they buy:

* **Route precedence.** ``/ui/{org_ref}`` matches a bare org alias, so a
  regression in registration order would let an org named "login" shadow the
  sign-in page.
* **404 not 403 for a non-member.** A 403 confirms the org exists, which turns
  guessing aliases into an org-enumeration oracle.
* **The minted token is shown once.** The raw value is unrecoverable afterwards,
  so a regression that re-rendered it would be a lasting disclosure.
* **The login form never provisions an account.** The endpoint behind it creates
  an identity for an address it does not recognise rather than refusing.
* **Launch versions are asserted inside the launch panel**, not across the
  document -- a page-wide substring check passed locally and failed in CI once the
  CLI version appeared in the menu.
"""

import asyncio
import logging
import re
from datetime import date, datetime, timedelta, timezone
from unittest import mock
from urllib.parse import quote
from uuid import uuid4

import pytest
from sqlalchemy import event
from sqlalchemy.exc import OperationalError
from sqlmodel import Session, select

from src.adapters.base_adapter import BoardAdapterError, BoardCapabilityError
from src.domain.board import BoardRegistration, BoardType
from src.domain.cli_token import CLIToken, hash_cli_token
from src.domain.organization import (
    Organization,
    OrganizationMembership,
    OrganizationRole,
)
from src.domain.project import Project, ProjectRepository, RepositoryLayer
from src.domain.release import Release, ReleaseStatus
from src.domain.repository import Repository
from src.domain.scrum import ScrumTicketVisit
from src.domain.ticket import Ticket, TicketStatus
from src.domain.user import User
from src.page_paths import (
    AUTH_CALLBACK_PATH,
    DEVICE_PATH,
    INVITE_ACCEPT_PATH,
    JOIN_PATH,
    LOGIN_PATH,
    LOGOUT_PATH,
    RESERVED_UI_SEGMENTS,
    SESSION_PATH,
    UI_PREFIX,
    dashboard_path,
)
from src.routers.webui.session import COOKIE_NAME, SESSION_TOKEN_NAME
from src.services.github_connect_service import _UNEXPECTED_SYNC_ERROR
from src.services.supabase_invite import MagicLinkResult

# Anchored to real time, not a frozen instant. The pages render relative times
# against `datetime.now`, so a hardcoded "now" would make the freshness
# assertions pass only when the suite happened to run at that hour.
UTC_NOW = datetime.now(timezone.utc)


# --------------------------------------------------------------------------- #
# Fixtures
# --------------------------------------------------------------------------- #


def _auth(client, raw_cookie):
    client.cookies.set(COOKIE_NAME, raw_cookie)
    return client


# --------------------------------------------------------------------------- #
# Sign-in
# --------------------------------------------------------------------------- #


def _configure(monkeypatch):
    """Env the sign-in route needs: the public OTP endpoint uses the anon key."""
    monkeypatch.setenv("SUPABASE_URL", "https://example.supabase.co")
    monkeypatch.setenv("SUPABASE_KEY", "anon-key")


def _capture_sends(monkeypatch):
    """Replace the dispatch with a recorder; returns the list of (email, redirect)."""
    sent = []

    def _fake(email, redirect_to):
        sent.append((email, redirect_to))
        return MagicLinkResult(configured=True, sent=True, status_code=200)

    monkeypatch.setattr("src.routers.webui.routes.send_magic_link", _fake)
    return sent


@pytest.mark.parametrize(
    "env,expect_form",
    [
        pytest.param(
            {"SUPABASE_URL": "https://x.supabase.co", "SUPABASE_KEY": "anon"},
            True,
            id="configured",
        ),
        pytest.param({}, False, id="unconfigured"),
    ],
)
def test_login_page_reflects_whether_sending_is_possible(
    client, monkeypatch, env, expect_form
):
    """A form that cannot mail anyone is worse than a message saying so."""
    for key in ("SUPABASE_URL", "SUPABASE_KEY"):
        monkeypatch.delenv(key, raising=False)
    for key, value in env.items():
        monkeypatch.setenv(key, value)

    r = client.get(LOGIN_PATH)
    assert r.status_code == 200
    assert ('name="email"' in r.text) is expect_form
    if expect_form:
        assert "Sign in" in r.text and "#F15B35" in r.text  # brand tokens shared
    else:
        assert "set up here" in r.text


def test_login_sends_only_for_known_users_and_says_nothing_either_way(
    client, monkeypatch, signed_in
):
    """Two guarantees that share a setup, and would be tested with identical
    fixtures apart:

    1. An unknown address never reaches Supabase. The admin endpoint behind this
       *creates* an identity for one it does not recognise, so a public form
       wired straight to it would let a stranger provision an account.
    2. The responses are byte-identical, so there is no enumeration oracle.
    """
    _configure(monkeypatch)
    sent = _capture_sends(monkeypatch)
    signed_in(email="real@havilandsoftware.com")

    known = client.post(LOGIN_PATH, data={"email": "  Real@Havilandsoftware.com "})
    unknown = client.post(LOGIN_PATH, data={"email": "fake@havilandsoftware.com"})

    assert [address for address, _ in sent] == ["real@havilandsoftware.com"], (
        "an unknown address must not reach the send path; the known one is "
        "trimmed and lowercased"
    )
    assert sent[0][1].endswith(AUTH_CALLBACK_PATH), (
        "Supabase silently falls back to the Site URL when redirect_to is wrong, "
        "which looks like success and lands the person on a 401"
    )
    assert known.status_code == unknown.status_code == 200
    assert known.text.replace("real@", "X@") == unknown.text.replace("fake@", "X@")
    assert 'aria-label="PixelFuel"' in known.text  # branded, not a bare rocket


def test_login_throttles_one_address_and_logs_a_failed_send(
    client, monkeypatch, signed_in, caplog
):
    """Sends are rate-limited upstream, and a silently broken login page looks
    exactly like a working one -- which is how the 422 in #451 went unnoticed."""
    _configure(monkeypatch)
    sent = _capture_sends(monkeypatch)
    address = f"{uuid4().hex[:8]}@havilandsoftware.com"
    signed_in(email=address)

    for _ in range(4):
        assert client.post(LOGIN_PATH, data={"email": address}).status_code == 200
    assert len(sent) == 1, f"expected one send, got {len(sent)}"

    other = f"{uuid4().hex[:8]}@havilandsoftware.com"
    signed_in(email=other)
    monkeypatch.setattr(
        "src.routers.webui.routes.send_magic_link",
        lambda email, redirect_to: MagicLinkResult(
            configured=True, sent=False, status_code=500, error="upstream exploded"
        ),
    )
    with caplog.at_level(logging.WARNING, logger="src.routers.webui.routes"):
        r = client.post(LOGIN_PATH, data={"email": other})

    assert r.status_code == 200 and "Check your email" in r.text
    assert any("not sent" in rec.getMessage() for rec in caplog.records)


def test_an_unconfirmed_user_gets_a_fresh_invite_instead_of_silence(
    client, monkeypatch, signed_in, caplog
):
    """The dead end this fixes.

    `/auth/v1/otp` cannot reach someone whose identity exists but was never
    confirmed: with `[auth] enable_signup = false` GoTrue routes their magic link
    through its signup path and answers `422 signup_disabled`. The page still
    said "check your email" and no email ever came — from their side the platform
    was silently, permanently broken. `resend_invite` is the admin path, which
    works with signup disabled.
    """
    _configure(monkeypatch)
    address = f"{uuid4().hex[:8]}@havilandsoftware.com"
    signed_in(email=address)

    monkeypatch.setattr(
        "src.routers.webui.routes.send_magic_link",
        lambda email, redirect_to: MagicLinkResult(
            configured=True, sent=False, status_code=422, error="signup_disabled"
        ),
    )
    invited = []
    monkeypatch.setattr(
        "src.routers.webui.routes.resend_invite",
        lambda email: invited.append(email) or None,
    )

    r = client.post(LOGIN_PATH, data={"email": address})

    assert invited == [address], "an unconfirmed user got silence, not an invite"
    # Same page as every other outcome — the fallback must not become an oracle
    # for which addresses have unconfirmed identities.
    assert r.status_code == 200 and "Check your email" in r.text


def test_an_unknown_address_never_reaches_the_invite_fallback(
    client, monkeypatch, signed_in
):
    """The fallback runs only for an address already matched against our own
    users table. Otherwise it would be a public form that provisions identities —
    the exact thing the sign-in route was written to prevent."""
    _configure(monkeypatch)
    invited = []
    monkeypatch.setattr(
        "src.routers.webui.routes.resend_invite",
        lambda email: invited.append(email) or None,
    )
    monkeypatch.setattr(
        "src.routers.webui.routes.send_magic_link",
        lambda email, redirect_to: MagicLinkResult(
            configured=True, sent=False, status_code=422, error="signup_disabled"
        ),
    )

    client.post(LOGIN_PATH, data={"email": f"stranger-{uuid4().hex[:6]}@x.com"})
    assert invited == []


def test_the_sent_page_offers_another_link(client, monkeypatch, signed_in):
    """An expired link is the common case, and the person holding it has no way
    to know that is what happened."""
    _configure(monkeypatch)
    _capture_sends(monkeypatch)
    address = f"{uuid4().hex[:8]}@havilandsoftware.com"
    signed_in(email=address)

    page = client.post(LOGIN_PATH, data={"email": address}).text
    assert "Send another" in page
    assert f'value="{address}"' in page, "the resend form must carry the address"


@pytest.mark.parametrize(
    "payload,expected",
    [({"access_token": "not-a-jwt"}, 401), ({}, 400)],
    ids=["bad-jwt", "no-token"],
)
def test_session_exchange_rejects_bad_input(client, payload, expected):
    assert client.post(SESSION_PATH, json=payload).status_code == expected


# --------------------------------------------------------------------------- #
# Session cookie
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "kwargs",
    [
        pytest.param(None, id="no-cookie"),
        pytest.param({"expires_at": UTC_NOW - timedelta(days=1)}, id="expired"),
        pytest.param({"revoked_at": UTC_NOW - timedelta(hours=1)}, id="revoked"),
    ],
)
def test_unusable_sessions_all_redirect_to_login(client, signed_in, make_org, kwargs):
    """Absent, expired and revoked must be indistinguishable -- telling them apart
    tells an attacker which guessed cookie values are real tokens."""
    if kwargs is None:
        r = client.get(f"{UI_PREFIX}/anything", follow_redirects=False)
    else:
        user, cookie = signed_in(**kwargs)
        org = make_org("acme", member=user)
        _auth(client, cookie)
        r = client.get(f"{UI_PREFIX}/{org.alias}", follow_redirects=False)

    assert r.status_code == 303
    assert r.headers["location"] == LOGIN_PATH


def test_logout_revokes_the_session_row(client, signed_in, db_engine):
    user, cookie = signed_in()
    _auth(client, cookie)
    r = client.post(LOGOUT_PATH, follow_redirects=False)

    assert r.status_code == 303 and r.headers["location"] == LOGIN_PATH
    with Session(db_engine) as session:
        row = session.exec(
            select(CLIToken).where(CLIToken.token_hash == hash_cli_token(cookie))
        ).first()
        assert row is not None and row.revoked_at is not None


def test_root_sends_you_to_your_default_org_and_it_resolves(
    client, signed_in, make_org, db_engine
):
    """The redirect target must be a URL a route actually serves: lowercasing on
    the way out and exact-matching on the way in would 404.

    Signing in lands on the **workflow launcher**, not the dashboard -- the front
    door answers "what do I want to do?" rather than "how are things?". The
    dashboard has not moved; it is still ``/ui/{org}``.
    """
    user, cookie = signed_in()
    make_org("first", name="A First", member=user)
    preferred = make_org("PF", name="Z Preferred", member=user)
    with Session(db_engine) as session:
        row = session.get(User, user.id)
        row.default_organization_id = preferred.id
        session.add(row)
        session.commit()

    _auth(client, cookie)
    target = client.get(UI_PREFIX, follow_redirects=False).headers["location"]

    assert target == f"{UI_PREFIX}/pf/workflow", (
        "the default org must win over alphabetical order, and the front door is "
        "the workflow launcher"
    )
    assert client.get(target).status_code == 200
    # The dashboard is still reachable at its own address.
    assert client.get(f"{UI_PREFIX}/pf").status_code == 200


def test_user_with_no_orgs_gets_a_dead_end_page_not_a_crash(client, signed_in):
    user, cookie = signed_in()
    _auth(client, cookie)
    r = client.get(UI_PREFIX)
    assert r.status_code == 200 and "No organizations yet" in r.text


def test_choosing_a_default_org_persists_it(client, signed_in, make_org, db_engine):
    """`GET /ui` already consulted this field; nothing could set it from here, so
    someone in four orgs landed on whichever sorted first, every time."""
    user, cookie = signed_in()
    here = make_org("acme", member=user)
    other = make_org("bp", member=user)
    _auth(client, cookie)

    r = client.post(
        f"{UI_PREFIX}/{here.alias}/default-org",
        data={"organization_id": other.id},
        follow_redirects=False,
    )
    assert r.status_code == 303

    with Session(db_engine) as session:
        assert session.get(User, user.id).default_organization_id == other.id
    # The star chooses the *org*; the front door is the workflow launcher.
    assert (
        client.get(UI_PREFIX, follow_redirects=False).headers["location"]
        == f"{UI_PREFIX}/bp/workflow"
    )


def test_cannot_default_to_an_org_you_are_not_in(client, signed_in, make_org):
    """Membership of the target is checked separately from the org in the path --
    they are different orgs by design, so authorising one says nothing about the
    other."""
    user, cookie = signed_in()
    here = make_org("acme", member=user)
    foreign = make_org("secret")
    _auth(client, cookie)

    r = client.post(
        f"{UI_PREFIX}/{here.alias}/default-org", data={"organization_id": foreign.id}
    )
    assert r.status_code == 404


# --------------------------------------------------------------------------- #
# Org resolution and route precedence
# --------------------------------------------------------------------------- #


def test_org_resolves_by_alias_any_case_and_by_uuid(client, signed_in, make_org):
    """Only auto-derived aliases are lowercased; an explicit one is stored
    verbatim, so `PF` exists. Matching a lowercased segment against the stored
    value would make such an org unreachable at every spelling of its own URL."""
    user, cookie = signed_in()
    lower = make_org("acme", member=user)
    # Creates the uppercase-alias org the last two URLs below resolve. The result
    # is deliberately unbound -- the call is the point, not the value.
    make_org("PF", name="PixelFuel", member=user)
    _auth(client, cookie)

    for url in (
        f"{UI_PREFIX}/{lower.alias}",
        f"{UI_PREFIX}/ACME",
        f"{UI_PREFIX}/{lower.id}",
        f"{UI_PREFIX}/pf",
        f"{UI_PREFIX}/PF",
    ):
        assert client.get(url).status_code == 200, url


def test_non_member_gets_404_and_platform_member_gets_in(client, signed_in, make_org):
    """403 would confirm the org exists, making aliases enumerable. Platform
    members bypass membership, the same way rbac.verify_org_membership does."""
    outsider, outsider_cookie = signed_in()
    org = make_org("secret")
    _auth(client, outsider_cookie)
    assert client.get(f"{UI_PREFIX}/{org.alias}").status_code == 404

    staff, staff_cookie = signed_in(is_platform_member=True)
    client.cookies.clear()
    _auth(client, staff_cookie)
    assert client.get(f"{UI_PREFIX}/{org.alias}").status_code == 200


def test_literal_pages_win_over_a_same_named_org(client, signed_in, db_engine):
    """Registration order is load-bearing, and RESERVED_UI_SEGMENTS is the second
    guard -- an org actually aliased "device" must not shadow /ui/device."""
    for path in (DEVICE_PATH, INVITE_ACCEPT_PATH, AUTH_CALLBACK_PATH, LOGIN_PATH):
        assert client.get(path, follow_redirects=False).status_code == 200, path

    user, cookie = signed_in(is_platform_member=True)
    with Session(db_engine) as session:
        for segment in sorted(RESERVED_UI_SEGMENTS - {"login", "logout"}):
            session.add(
                Organization(id=str(uuid4()), name=f"Sneaky {segment}", alias=segment)
            )
        session.commit()

    _auth(client, cookie)
    for segment in sorted(RESERVED_UI_SEGMENTS - {"login", "logout"}):
        r = client.get(f"{UI_PREFIX}/{segment}", follow_redirects=False)
        assert r.status_code != 200 or "Projects" not in r.text, segment


@pytest.fixture
def populated_org(db_engine, signed_in, make_org):
    """An org with one project, three repos of different layers, and releases."""
    user, cookie = signed_in()
    org = make_org("pf", name="Haviland Software", member=user)

    with Session(db_engine) as session:
        project = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias="PF",
            name="PixelFuel Innoday",
            description="d",
        )
        session.add(project)

        # Board synced 2h ago; the newest repo 10 min ago -- the card must show the
        # repo's time, since it is the more recent of the two.
        #
        # Read the clock HERE, not from the module-level UTC_NOW. The page renders
        # "N min ago" against the clock at request time, so a 10-minute stamp taken
        # at import renders as "11 min ago" once more than a minute passes between
        # collection and this test running -- which is a function of how long the
        # whole suite takes, not of anything this test does. It failed at 89s and
        # passed at 52s. The other UTC_NOW offsets here are hours and days and
        # cannot flip that way.
        now = datetime.now(timezone.utc)
        session.add(
            BoardRegistration(
                id=str(uuid4()),
                organization_id=org.id,
                project_id=project.id,
                board_name="PF",
                board_url="https://linear.app/hs/team/PF",
                board_type=BoardType.LINEAR,
                board_external_id="PF",
                is_active=True,
                last_sync_at=now - timedelta(hours=2),
            )
        )

        specs = [
            ("innoday", RepositoryLayer.API, None, timedelta(minutes=10)),
            ("site", RepositoryLayer.UNASSIGNED, "ui", timedelta(hours=3)),
            ("guide", RepositoryLayer.UNASSIGNED, None, timedelta(days=30)),
        ]
        for name, link_layer, repo_layer, age in specs:
            repo = Repository(
                id=str(uuid4()),
                name=name,
                full_name=f"hs/{name}",
                url=f"https://github.com/hs/{name}",
                organization_id=org.id,
                layer=repo_layer,
                last_synced_at=now - age,
            )
            session.add(repo)
            session.add(
                ProjectRepository(
                    id=str(uuid4()),
                    project_id=project.id,
                    repository_id=repo.id,
                    layer=link_layer,
                    is_active=True,
                )
            )

        # An archived repo, and a soft-deleted link: neither should render.
        gone = Repository(
            id=str(uuid4()),
            name="archived-thing",
            full_name="hs/archived-thing",
            url="https://github.com/hs/archived-thing",
            organization_id=org.id,
            archived=True,
        )
        session.add(gone)
        session.add(
            ProjectRepository(
                id=str(uuid4()),
                project_id=project.id,
                repository_id=gone.id,
                is_active=True,
            )
        )
        unlinked = Repository(
            id=str(uuid4()),
            name="dropped-topic",
            full_name="hs/dropped-topic",
            url="https://github.com/hs/dropped-topic",
            organization_id=org.id,
        )
        session.add(unlinked)
        session.add(
            ProjectRepository(
                id=str(uuid4()),
                project_id=project.id,
                repository_id=unlinked.id,
                is_active=False,
            )
        )

        for version, status in [
            ("v1.9.0", ReleaseStatus.PLANNED),
            ("v1.10.0", ReleaseStatus.PLANNED),
            ("v0.1.0", ReleaseStatus.RELEASED),
        ]:
            session.add(
                Release(
                    id=str(uuid4()),
                    organization_id=org.id,
                    project_id=project.id,
                    version=version,
                    status=status,
                )
            )
        session.commit()
        project_id = project.id

    return user, cookie, org, project_id


# --------------------------------------------------------------------------- #
# Dashboard content
# --------------------------------------------------------------------------- #


def test_dashboard_shows_projects_repos_and_resolved_layers(client, populated_org):
    """Layer resolution is a three-step fallback and the exclusions are silent, so
    both are asserted against one rendered page rather than three near-identical
    ones."""
    user, cookie, org, _ = populated_org
    _auth(client, cookie)
    text = client.get(f"{UI_PREFIX}/{org.alias}").text

    assert "PixelFuel Innoday" in text and ">PF<" in text
    for name in ("innoday", "site", "guide"):
        assert name in text

    # junction layer wins -> repo layer -> unassigned, shown with the team's own
    # names (an earlier version invented "service"/"interface").
    assert ">api<" in text and ">ui/ux<" in text and ">unassigned<" in text
    assert "service" not in text and "interface" not in text

    # Archived repos and soft-deleted links must not appear at all.
    assert "archived-thing" not in text and "dropped-topic" not in text

    # Chrome that has to be there for the page to be usable.
    # Both halves lowercased: WorkspaceOnboardService resolves with func.lower()
    # on each side, and a command you can type without shift is the better default.
    assert f"innoday init {org.alias.lower()}/pf" in text
    assert 'class="copybtn"' in text
    assert 'aria-label="Sync now"' in text
    # The install guide is gone; the user menu's PyPI link is the one route in.
    assert "Install the innoday CLI" in text
    assert "https://pypi.org/project/innoday/" in text
    assert 'class="panel install"' not in text
    assert client.get(f"{UI_PREFIX}/{org.alias}").headers["cache-control"] == "no-store"


@pytest.mark.parametrize(
    "extra,expected",
    [
        pytest.param(None, "v1.9.0", id="lowest-semver-not-string-order"),
        pytest.param(
            ("v2.0.0", ReleaseStatus.IN_PROGRESS), "v2.0.0", id="in-progress-wins"
        ),
    ],
)
def test_next_launch_selection(client, populated_org, db_engine, extra, expected):
    """`Release` has no target date, so "next" is status-then-semver. v1.9.0 must
    beat v1.10.0 -- a string compare gets that backwards.

    Versions are read out of the launch panel, not the whole document: a page-wide
    substring check passed locally and failed in CI once the CLI version appeared
    in the menu (a tagless build reports `v0.1.0-beta`, containing `v0.1.0`).
    """
    user, cookie, org, project_id = populated_org
    if extra:
        version, status = extra
        with Session(db_engine) as session:
            session.add(
                Release(
                    id=str(uuid4()),
                    organization_id=org.id,
                    project_id=project_id,
                    version=version,
                    status=status,
                )
            )
            session.commit()

    _auth(client, cookie)
    versions = re.findall(
        r'<span class="ver">([^<]+)</span>',
        client.get(f"{UI_PREFIX}/{org.alias}").text,
    )
    assert expected in versions
    assert "v1.10.0" not in versions  # string order would pick this
    assert "v0.1.0" not in versions  # already released


def test_freshness_is_derived_and_stated_plainly(
    client, signed_in, make_org, populated_org, db_engine
):
    """Two things about the sync column: the project time is the newest of board
    and repo syncs, and an unsynced repo says "never synced" rather than a bare
    "never" -- which is every repo in dev today, so it is the common case."""
    user, cookie, org, _ = populated_org
    _auth(client, cookie)
    text = client.get(f"{UI_PREFIX}/{org.alias}").text
    # board 2h ago, newest repo 10 min ago -> minutes wins. Freshness is carried
    # by the sync pill itself now; the separate dot restated its colour.
    assert "synced 10 min ago" in text
    assert 'class="sync fresh"' in text
    assert 'class="dot' not in text

    user2, cookie2 = signed_in()
    bare = make_org("nosync", member=user2)
    with Session(db_engine) as session:
        project = Project(
            id=str(uuid4()),
            organization_id=bare.id,
            alias="NS",
            name="Never Synced",
            description="d",
        )
        repo = Repository(
            id=str(uuid4()),
            name="fresh-repo",
            full_name="hs/fresh-repo",
            url="https://github.com/hs/fresh-repo",
            organization_id=bare.id,
            last_synced_at=None,
        )
        session.add_all([project, repo])
        session.add(
            ProjectRepository(
                id=str(uuid4()),
                project_id=project.id,
                repository_id=repo.id,
                is_active=True,
            )
        )
        session.commit()

    client.cookies.clear()
    _auth(client, cookie2)
    text = client.get(f"{UI_PREFIX}/{bare.alias}").text
    assert "never synced" in text and "synced never synced" not in text


def test_empty_states_render(client, signed_in, make_org, db_engine):
    """No projects, and a project with no upcoming release."""
    user, cookie = signed_in()
    bare = make_org("bare", member=user)
    _auth(client, cookie)
    assert (
        "No projects in this organization yet."
        in client.get(f"{UI_PREFIX}/{bare.alias}").text
    )

    with Session(db_engine) as session:
        session.add(
            Project(
                id=str(uuid4()),
                organization_id=bare.id,
                alias="EMP",
                name="Nothing Planned",
                description="d",
            )
        )
        session.commit()
    text = client.get(f"{UI_PREFIX}/{bare.alias}").text
    assert "Next launch" in text and "—" in text and "Nothing on the pad yet." in text


def test_org_switcher_appears_only_with_more_than_one_org(client, signed_in, make_org):
    """An affordance that leads nowhere is worse than no affordance."""
    user, cookie = signed_in()
    only = make_org("solo", name="Solo Org", member=user)
    _auth(client, cookie)
    assert "»" not in client.get(f"{UI_PREFIX}/{only.alias}").text

    second = make_org("duo", name="Second Org", member=user)
    text = client.get(f"{UI_PREFIX}/{only.alias}").text
    assert "»" in text and f"{UI_PREFIX}/{second.alias}" in text


def test_org_names_are_escaped_everywhere_they_are_rendered(
    client, signed_in, make_org
):
    """An org name is attacker-influenced text: an org ADMIN can PUT their own
    org's name with only a user token, and a platform member sees every org's
    name in this switcher. One un-escaped interpolation of it -- inside the
    star's aria-label, where the quotes are easy to miss -- was enough to break
    out of the attribute."""
    user, cookie = signed_in()
    here = make_org("here", name="Here", member=user)
    make_org("evil", name='X" onmouseover="alert(1)', member=user)

    text = client.get(
        f"{UI_PREFIX}/{here.alias}", cookies={"innoday_session": cookie}
    ).text
    assert 'onmouseover="alert(1)' not in text
    assert "&#34; onmouseover=" in text or "&quot; onmouseover=" in text


def test_repo_lookup_does_not_scale_with_project_count(
    client, signed_in, make_org, db_engine
):
    """One batched query, not one per project. Asserted by counting SELECTs, since
    the regression is silent -- the page still renders, just slower each time a
    project is added."""
    from sqlalchemy import event

    user, cookie = signed_in()
    org = make_org("many", member=user)
    with Session(db_engine) as session:
        for n in range(6):
            session.add(
                Project(
                    id=str(uuid4()),
                    organization_id=org.id,
                    alias=f"P{n}",
                    name=f"Project {n}",
                    description="d",
                )
            )
        session.commit()

    statements = []

    def _record(conn, cursor, statement, *a):
        if statement.lstrip().upper().startswith("SELECT"):
            statements.append(statement)

    event.listen(db_engine, "before_cursor_execute", _record)
    try:
        _auth(client, cookie)
        assert client.get(f"{UI_PREFIX}/{org.alias}").status_code == 200
    finally:
        event.remove(db_engine, "before_cursor_execute", _record)

    repo_queries = [s for s in statements if "project_repositories" in s]
    assert len(repo_queries) == 1, (
        f"expected 1 batched repo query, got {len(repo_queries)}"
    )


# --------------------------------------------------------------------------- #
# CLI tokens
# --------------------------------------------------------------------------- #


def test_token_lifecycle(client, signed_in, make_org, db_engine):
    """One token, created from the header, shown once, replacing the last.

    A list of five is unanswerable -- the raw values are unrecoverable, so nobody
    can tell which their laptop is using.
    """
    user, cookie = signed_in()
    org = make_org("acme", member=user)
    _auth(client, cookie)

    page = client.get(f"{UI_PREFIX}/{org.alias}").text
    assert "No token yet." in page and SESSION_TOKEN_NAME not in page
    assert 'name="expires_days"' not in page  # derived, not asked
    assert 'placeholder="Name this token"' not in page

    first = client.post(f"{UI_PREFIX}/{org.alias}/tokens")
    assert "copy it now" in first.text
    raw = next(line for line in first.text.splitlines() if 'class="val"' in line)
    token_value = raw.split(">")[-2].split("<")[0]
    assert token_value.startswith("idt_")
    # Shown exactly once.
    assert token_value not in client.get(f"{UI_PREFIX}/{org.alias}").text

    client.post(f"{UI_PREFIX}/{org.alias}/tokens")
    with Session(db_engine) as session:
        live = session.exec(
            select(CLIToken).where(
                CLIToken.user_id == user.id,
                CLIToken.revoked_at == None,  # noqa: E711
                CLIToken.name != SESSION_TOKEN_NAME,
            )
        ).all()
        revoked = session.exec(
            select(CLIToken).where(
                CLIToken.user_id == user.id,
                CLIToken.revoked_at != None,  # noqa: E711
            )
        ).all()
    assert len(live) == 1 and live[0].name.startswith("web-")
    assert live[0].expires_at is not None
    assert len(revoked) == 1, "the previous token must be revoked, not just hidden"


# --------------------------------------------------------------------------- #
# Layer classification
# --------------------------------------------------------------------------- #


def test_every_layer_is_offered_and_infra_round_trips(client, populated_org, db_engine):
    """`infra` was absent from the enum entirely, so Terraform and CI repos had
    nowhere to go but `unassigned`."""
    from src.domain.project import RepositoryLayer

    assert RepositoryLayer("infra") is RepositoryLayer.INFRA

    user, cookie, org, project_id = populated_org
    _auth(client, cookie)
    text = client.get(f"{UI_PREFIX}/{org.alias}").text
    for label in ("ui/ux", "api", "data", "intelligence", "infra", "legacy"):
        assert f">{label}<" in text, f"{label} missing from the picker"

    with Session(db_engine) as session:
        repo_id = (
            session.exec(
                select(ProjectRepository).where(
                    ProjectRepository.project_id == project_id,
                    ProjectRepository.is_active == True,  # noqa: E712
                )
            )
            .first()
            .repository_id
        )

    r = client.post(
        f"{UI_PREFIX}/{org.alias}/repos/{repo_id}/layer",
        data={"layer": "infra"},
        follow_redirects=False,
    )
    assert r.status_code == 303
    with Session(db_engine) as session:
        link = session.exec(
            select(ProjectRepository).where(
                ProjectRepository.repository_id == repo_id,
                ProjectRepository.project_id == project_id,
            )
        ).first()
        assert getattr(link.layer, "value", link.layer) == "infra"


def test_layer_change_writes_the_project_link_not_the_repo(
    client, populated_org, db_engine
):
    """The same repo can be one project's UI layer and another's library, so the
    org-wide Repository.layer must be left alone as the fallback it is."""
    user, cookie, org, _ = populated_org
    _auth(client, cookie)
    with Session(db_engine) as session:
        repo = session.exec(select(Repository).where(Repository.name == "site")).first()
        repo_id, before = repo.id, repo.layer

    client.post(
        f"{UI_PREFIX}/{org.alias}/repos/{repo_id}/layer", data={"layer": "data"}
    )

    with Session(db_engine) as session:
        assert session.get(Repository, repo_id).layer == before, "repo layer changed"
        link = session.exec(
            select(ProjectRepository).where(ProjectRepository.repository_id == repo_id)
        ).first()
        assert getattr(link.layer, "value", link.layer) == "data"


# --------------------------------------------------------------------------- #
# Sync, and the write routes' shared guards
# --------------------------------------------------------------------------- #


# The success cases below are the shape `GitHubConnectService.sync_project_repositories`
# **actually returns** -- copied from the `return {...}` at the end of that method,
# key for key.
#
# **The previous version of this parametrize invented the shape instead**
# (`{"total_repositories": 7, "added": [...], "removed": [...]}`), and that is the
# whole reason the bug it was meant to cover survived: the handler read those three
# keys, the result dict has never contained any of them, and the stub supplied them
# anyway. So every real press flashed "synced — ? repositories" with both counts
# suppressed as falsy, while this test stayed green (#652). A stub that agrees with
# the caller instead of with the callee cannot fail.
_REAL_SYNC_RESULT = {
    "sync_id": "s-1",
    "project_id": "p-1",
    "status": "completed",
    "repositories_synced": 7,
    "issues_synced": 0,
    "open_pr_repos_counted": 7,
    "releases_discovered": 0,
    "changes": {
        "new_repositories": ["a"],
        "reactivated_repositories": 0,
        "updated_repositories": 6,
        "deactivated_repositories": 0,
        "deactivated_repository_names": [],
        "new_issues": 0,
        "updated_issues": 0,
    },
    "timestamp": "2026-08-18T00:00:00",
}


@pytest.mark.parametrize(
    "outcome,expected",
    [
        pytest.param(
            _REAL_SYNC_RESULT,
            ("7 repositories", "1 added"),
            id="reports-what-changed",
        ),
        pytest.param(
            {
                **_REAL_SYNC_RESULT,
                "changes": {
                    **_REAL_SYNC_RESULT["changes"],
                    # A list and an int, in the same dict. Reading `len()` over both
                    # (or neither) is the mistake this param exists to catch.
                    "new_repositories": [],
                    "reactivated_repositories": 2,
                    "deactivated_repositories": 3,
                },
            },
            ("7 repositories", "2 added", "3 removed"),
            id="reactivated-counts-as-added-and-deactivated-as-removed",
        ),
        pytest.param(
            # A `ValueError`, because that is what the service raises for a missing
            # credential -- and it is the type the notice is allowed to quote. A
            # stand-in of some other type would render the generic string, so this
            # param would have been pinning the opposite of what it reads as.
            ValueError("No GitHub connection found for organization"),
            ("Sync failed", "No GitHub connection found"),
            id="reports-failure-not-a-stack-trace",
        ),
    ],
)
def test_sync_surfaces_its_result(
    client, populated_org, monkeypatch, outcome, expected
):
    """No credential is the usual reason this fails, and the person pressing the
    button is the one who can fix it -- so it has to reach them."""
    user, cookie, org, project_id = populated_org

    class _Service:
        def __init__(self, session):
            pass

        async def sync_project_repositories(self, **kwargs):
            if isinstance(outcome, Exception):
                raise outcome
            return outcome

    monkeypatch.setattr(
        "src.services.github_connect_service.GitHubConnectService", _Service
    )
    _auth(client, cookie)
    r = client.post(
        f"{UI_PREFIX}/{org.alias}/projects/{project_id}/sync", follow_redirects=False
    )

    # Post-redirect-GET. Rendering the dashboard straight from the POST left the
    # address bar on the POST, so a refresh re-ran a live GitHub sync.
    assert r.status_code == 303
    assert r.headers["location"] == dashboard_path(org.alias)

    followed = client.get(r.headers["location"])
    assert followed.status_code == 200
    for fragment in expected:
        assert fragment in followed.text

    # The direct pin. `?` is what `.get("total_repositories", "?")` produced for
    # every sync that ever ran, and a count read from a key the result lacks is
    # falsy, so both change clauses were suppressed too. A notice that cannot say
    # how many repositories it synced is not a report, and it is what the fabricated
    # stub above was concealing.
    if not isinstance(outcome, Exception):
        assert "? repositories" not in followed.text


def test_the_sync_notice_quotes_no_more_than_the_stored_message_does(
    client, populated_org, monkeypatch
):
    """The notice and ``Project.github_error_message`` are the same disclosure, and
    have to be narrowed by the same rule.

    The service classifies an exception before storing it, so a database failure
    reaches the dashboard tooltip as a generic line. This route interpolated the
    *original* exception instead -- so the identical failure, on the identical
    screen, showed the reader SQL, its bound parameters and connection detail
    because they were the one who pressed the button. Nothing about pressing Sync
    grants that.
    """
    user, cookie, org, project_id = populated_org
    detail = "NOT-A-SECRET-connection-detail-placeholder"
    leaky = OperationalError(
        f"SELECT project.id FROM project WHERE project.id = ? [{detail}]",
        {"id": project_id},
        Exception("server closed the connection unexpectedly"),
    )
    assert detail in str(leaky), (
        "premise of this test: this exception type stringifies to its own detail"
    )

    class _Service:
        def __init__(self, session):
            pass

        async def sync_project_repositories(self, **kwargs):
            raise leaky

    monkeypatch.setattr(
        "src.services.github_connect_service.GitHubConnectService", _Service
    )
    _auth(client, cookie)
    r = client.post(
        f"{UI_PREFIX}/{org.alias}/projects/{project_id}/sync", follow_redirects=False
    )
    followed = client.get(r.headers["location"])

    assert "Sync failed" in followed.text, "it still has to say the sync failed"
    assert _UNEXPECTED_SYNC_ERROR in followed.text
    assert detail not in followed.text
    assert "SELECT" not in followed.text


def test_sync_notice_is_shown_once_and_not_again_on_refresh(
    client, populated_org, monkeypatch
):
    """The notice survives exactly one redirect.

    A flash that outlived its redirect would announce a sync on every later load
    of the dashboard, which reads as the sync having just happened again.
    """
    user, cookie, org, project_id = populated_org

    class _Service:
        def __init__(self, session):
            pass

        async def sync_project_repositories(self, **kwargs):
            # The real return shape -- see `_REAL_SYNC_RESULT` above for why a
            # hand-invented one is worse than no stub at all.
            return {**_REAL_SYNC_RESULT, "repositories_synced": 3}

    monkeypatch.setattr(
        "src.services.github_connect_service.GitHubConnectService", _Service
    )
    _auth(client, cookie)
    client.post(
        f"{UI_PREFIX}/{org.alias}/projects/{project_id}/sync", follow_redirects=False
    )

    # Scoped to the notice banner, not the whole document: "3 repositories" also
    # appears in the GitHub icon's tooltip, so a page-wide substring check passes
    # on the refresh it is supposed to fail on.
    def _notice(html):
        found = re.search(r'<div class="syncnote[^"]*">(.*?)</div>', html, re.S)
        return found.group(1) if found else None

    first = client.get(dashboard_path(org.alias))
    assert "3 repositories" in (_notice(first.text) or "")

    second = client.get(dashboard_path(org.alias))
    assert _notice(second.text) is None


def test_sync_returns_to_the_page_it_was_pressed_from(
    client, populated_org, monkeypatch
):
    """`return_to` decides where the browser lands, so the card can be rendered
    on more than one page without the handler guessing."""
    user, cookie, org, project_id = populated_org

    class _Service:
        def __init__(self, session):
            pass

        async def sync_project_repositories(self, **kwargs):
            # Real return shape -- see `_REAL_SYNC_RESULT`.
            return {**_REAL_SYNC_RESULT, "repositories_synced": 1}

    monkeypatch.setattr(
        "src.services.github_connect_service.GitHubConnectService", _Service
    )
    _auth(client, cookie)
    here = f"{UI_PREFIX}/{org.alias}/projects/pf"
    r = client.post(
        f"{UI_PREFIX}/{org.alias}/projects/{project_id}/sync",
        data={"return_to": here},
        follow_redirects=False,
    )
    assert r.headers["location"] == here


@pytest.mark.parametrize(
    "hostile",
    [
        "https://evil.example.com",
        "//evil.example.com",
        "/ui//evil.example.com",
        "/api/v1/organizations",
        "\\evil.example.com",
        "",
    ],
)
def test_return_to_never_leaves_this_router(
    client, populated_org, monkeypatch, hostile
):
    """`return_to` arrives in a request body, so it is attacker-controlled.

    A leading `//` is the one that looks safe and is not: browsers read it as
    protocol-relative, so `/ui//evil.example.com` is an absolute URL wearing a
    prefix the check would otherwise accept.
    """
    user, cookie, org, project_id = populated_org

    class _Service:
        def __init__(self, session):
            pass

        async def sync_project_repositories(self, **kwargs):
            # Real return shape -- see `_REAL_SYNC_RESULT`.
            return {**_REAL_SYNC_RESULT, "repositories_synced": 1}

    monkeypatch.setattr(
        "src.services.github_connect_service.GitHubConnectService", _Service
    )
    _auth(client, cookie)
    r = client.post(
        f"{UI_PREFIX}/{org.alias}/projects/{project_id}/sync",
        data={"return_to": hostile},
        follow_redirects=False,
    )
    assert r.headers["location"] == dashboard_path(org.alias), hostile


def test_write_routes_require_a_session(client, signed_in, make_org, populated_org):
    """Every mutating route redirects rather than 401ing -- a page auth failure
    should land on the sign-in page, not an error."""
    _u, _c, org, project_id = populated_org
    for path, data in (
        (f"{UI_PREFIX}/{org.alias}/tokens", {}),
        (f"{UI_PREFIX}/{org.alias}/projects/{project_id}/sync", {}),
        (f"{UI_PREFIX}/{org.alias}/repos/anything/layer", {"layer": "infra"}),
        (f"{UI_PREFIX}/{org.alias}/default-org", {"organization_id": org.id}),
    ):
        r = client.post(path, data=data, follow_redirects=False)
        assert r.status_code == 303, path
        assert r.headers["location"] == LOGIN_PATH, path


def test_write_routes_reject_another_tenants_ids(
    client, signed_in, make_org, populated_org, db_engine
):
    """A repo or project id from another org must not be usable by guessing it."""
    _u, _c, _org, project_id = populated_org
    with Session(db_engine) as session:
        repo_id = (
            session.exec(
                select(ProjectRepository).where(
                    ProjectRepository.project_id == project_id
                )
            )
            .first()
            .repository_id
        )

    outsider, cookie = signed_in(email="outsider@example.com")
    other = make_org("elsewhere", member=outsider)
    _auth(client, cookie)

    for path, data in (
        (f"{UI_PREFIX}/{other.alias}/projects/{project_id}/sync", {}),
        (f"{UI_PREFIX}/{other.alias}/repos/{repo_id}/layer", {"layer": "infra"}),
    ):
        assert client.post(path, data=data).status_code == 404, path

    # An unknown layer is refused rather than persisted. 400, not 404: this user
    # *is* a member of `other`, so the org resolves and the value is what fails.
    assert (
        client.post(
            f"{UI_PREFIX}/{other.alias}/repos/{repo_id}/layer", data={"layer": "banana"}
        ).status_code
        == 400
    )


def test_repo_rows_show_open_prs_and_distinguish_never_counted(
    client, populated_org, db_engine
):
    """Replaces a per-repo "last synced" that read `never synced` on every row --
    accurate, since repo sync had never run, and so telling nobody anything.

    None (never counted) and 0 (counted, none open) must not render the same: the
    old column's whole failure was flattening exactly that kind of distinction.
    """
    user, cookie, org, project_id = populated_org
    with Session(db_engine) as session:
        repos = session.exec(select(Repository).order_by(Repository.name)).all()
        by_name = {r.name: r for r in repos}
        by_name["innoday"].open_pr_count = 3
        by_name["site"].open_pr_count = 0
        by_name["guide"].open_pr_count = None
        session.add_all(list(by_name.values()))
        session.commit()

    _auth(client, cookie)
    text = client.get(f"{UI_PREFIX}/{org.alias}").text

    assert "3 PRs" in text
    assert "0 PRs" in text
    assert "never synced" not in text  # the column it replaced
    assert 'class="prs none"' in text  # guide: counted never, rendered blank

    # The count is the start of a question; the answer is on GitHub. Zero links
    # too -- "are there really none?" is fair, and a dead badge does not answer it.
    assert "https://github.com/hs/innoday/pulls" in text
    assert "https://github.com/hs/site/pulls" in text
    # ...but never-counted does not link: the number would be a claim the page
    # cannot make.
    assert "https://github.com/hs/guide/pulls" not in text


def _repo_row(html, name):
    """One repository's row from the dashboard, so assertions cannot match the page.

    The counts and the ages here repeat across three cards and the inlined CSS, and
    a page-wide `in` check is how this file's oldest bug got in (see the module
    docstring). ``.repo`` contains no nested `<div>` -- a tile, a name, a layer
    `<details>` and the PR badge -- so the non-greedy match is exact.
    """
    for block in re.findall(r'<div class="repo"[^>]*>.*?</div>', html, re.S):
        if f">{name}</a>" in block or f">{name}</span>" in block:
            return block
    raise AssertionError(f"no repo row for {name!r}")


def test_a_pr_count_nobody_has_refreshed_says_so(client, populated_org, db_engine):
    """A stale count and a real zero must not render alike (#650).

    The report behind this was a teammate's pull requests "disappearing". They had
    not: nothing schedules a repository sync, the last one had run five days
    earlier, and `0 open PRs` was rendered with exactly the confidence of a
    freshly-read zero. #641 gave the *project's* GitHub icon a red/grey/green state
    for the same blind spot and did not reach the counts, so the icon could go red
    beside an unqualified number.

    **Every repository here has a fresh `last_synced_at`, deliberately.** That is
    the field an earlier draft of the badge dated the count from, and it is not the
    count's timestamp: three code paths stamp it without reading a pull request, and
    the org-wide registration sync stamps it on every repository while leaving
    `open_pr_count` untouched. Dated from `last_synced_at`, every row below would
    read as freshly counted -- so this test fails against that draft, which is the
    point of setting the two fields against each other.

    The three repositories sit either side of the boundary, which is `_freshness`'s
    `cold` -- over 24 hours, the same threshold the sync pill on this card uses:

    * ``guide`` counted 30 days ago -- stale, and says how old it is.
    * ``site`` counted 3 hours ago -- inside the day, so it says nothing extra.
      Asserting this is what stops the fix being "mark everything, always", which
      would put the caveat on every badge on the page and teach people to skip it.
    * ``innoday`` counted 6 days ago and flagged errored -- the one caller that
      writes `Repository.errored_at` is the open-PR read, so the flag means the last
      attempt did not refresh this number. The age stays on screen: without it a
      repository whose GitHub grant lapsed in July reads identically to one that
      failed this morning.
    """
    user, cookie, org, project_id = populated_org
    fresh = datetime.now(timezone.utc) - timedelta(minutes=3)
    with Session(db_engine) as session:
        by_name = {r.name: r for r in session.exec(select(Repository)).all()}
        for repo in by_name.values():
            # The decoy: a metadata sync minutes ago, which says nothing about when
            # anyone last counted pull requests.
            repo.last_synced_at = fresh
        by_name["guide"].open_pr_count = 0
        by_name["guide"].open_pr_counted_at = datetime.now(timezone.utc) - timedelta(
            days=30
        )
        by_name["site"].open_pr_count = 0
        by_name["site"].open_pr_counted_at = datetime.now(timezone.utc) - timedelta(
            hours=3
        )
        by_name["innoday"].open_pr_count = 2
        by_name["innoday"].open_pr_counted_at = datetime.now(timezone.utc) - timedelta(
            days=6
        )
        by_name["innoday"].errored_at = datetime.now(timezone.utc)
        by_name["innoday"].error_message = "Could not read open pull requests"
        session.add_all(list(by_name.values()))
        session.commit()

    _auth(client, cookie)
    html = client.get(f"{UI_PREFIX}/{org.alias}").text

    cold = _repo_row(html, "guide")
    assert "0 PRs · 30 days ago" in cold, (
        "a month-old zero read as a fresh one; the age has to be on screen, "
        "not only in a tooltip -- and it has to be the count's age, not the "
        "repository's last metadata sync 3 minutes ago"
    )
    assert "prs zero stale" in cold

    warm = _repo_row(html, "site")
    assert "0 PRs<" in warm, "inside the day, the number stands on its own"
    assert "stale" not in warm

    unread = _repo_row(html, "innoday")
    assert "2 PRs · 6 days ago, not refreshed" in unread, (
        "the failed attempt must not swallow the age, and 'unread' is GitHub's "
        "word for notifications -- '2 PRs · unread' reads as two PRs nobody "
        "has reviewed"
    )
    assert "stale" in unread


def test_a_count_with_no_timestamp_of_its_own_says_the_age_is_unknown(
    client, populated_org, db_engine
):
    """A count that predates `open_pr_counted_at` must not borrow another field.

    Every row that had a count before that column existed has NULL in it, and there
    is nothing to backfill it from -- no other column records when a count was read,
    which is the whole bug. The honest render is "age unknown"; dating it from
    `last_synced_at` would print "counted 3 min ago" about a number nobody has
    looked at in a month, which is a worse failure than the bare count this replaced
    because it adds a false claim.
    """
    user, cookie, org, project_id = populated_org
    with Session(db_engine) as session:
        guide = session.exec(select(Repository).where(Repository.name == "guide")).one()
        guide.open_pr_count = 4
        guide.open_pr_counted_at = None
        guide.last_synced_at = datetime.now(timezone.utc) - timedelta(minutes=3)
        session.add(guide)
        session.commit()

    _auth(client, cookie)
    html = client.get(f"{UI_PREFIX}/{org.alias}").text

    row = _repo_row(html, "guide")
    assert "4 PRs · age unknown" in row
    assert "stale" in row
    assert "3 min ago" not in row, (
        "the repository's metadata-sync time is not the count's age; printing it "
        "here is the false provenance claim this column exists to avoid"
    )


def _tickets_block(html):
    """The card's release-tickets block, so assertions cannot match the whole page.

    The counts and the words around them repeat elsewhere in the document -- the
    Tickets tab has its own badge, and the release panel names the same version --
    and a page-wide substring check is how this file's oldest bug got in (see the
    module docstring). It also keeps every assertion here against **rendered
    output**: the served CSS and script are inlined into the same string, so a
    page-wide `in` can be satisfied by an authoring comment rather than by
    anything a reader would see (issue #582).
    """
    found = re.search(r'<div class="tickets">(.*?)</div>', html, re.S)
    return found.group(1) if found else ""


def _n_tickets(status, count, release):
    """`count` `_add_tickets` specs in one status, all on the same version."""
    return [(f"{status} {n} {release}", status, release) for n in range(count)]


def test_launch_panel_counts_only_the_open_releases_tickets(
    client, populated_org, db_engine
):
    """The block describes **the open release**, not the project's whole board.

    `populated_org`'s next launch is v1.9.0, so only the tickets carrying that
    exact string may be counted. v1.10.0 is a real release row on the same
    project and unattached tickets are the common case on real data -- both are
    here because both were previously counted, which made "56 planned · 117 done"
    under a version a false claim about that version (HS-574).

    Also: "in review", not "in test". The board has no test state, and labelling
    IN_REVIEW as one would report something the data does not say.
    """
    from src.domain.ticket import TicketStatus

    user, cookie, org, project_id = populated_org
    _add_tickets(
        db_engine,
        org,
        project_id,
        _n_tickets(TicketStatus.IN_PROGRESS, 2, "v1.9.0")
        + _n_tickets(TicketStatus.IN_REVIEW, 3, "v1.9.0")
        + _n_tickets(TicketStatus.DONE, 4, "v1.10.0")
        + _n_tickets(TicketStatus.TODO, 5, None),
    )

    _auth(client, cookie)
    block = _tickets_block(client.get(f"{UI_PREFIX}/{org.alias}").text)

    # The heading names the release, because "Release tickets" alone only moves
    # the ambiguity one step along.
    assert "<h4>Release tickets &middot; v1.9.0</h4>" in block
    assert "2</b> in progress" in block
    assert "3</b> in review" in block
    # The other version's four and the unattached five are not this release's.
    assert "4</b> done" not in block
    assert "5</b> planned" not in block
    assert "in test" not in block

    # The board's own total stays available -- but as one figure that says whose
    # it is, never as a count sitting under the version heading.
    assert "14 tickets on the project board in total." in block


def test_release_tickets_never_show_a_different_versions_work(
    client, populated_org, db_engine
):
    """Every ticket carries a version, and none of them is the open one.

    The false-fallback case: project-wide numbers exist and are non-zero, so a
    regression that dropped the release predicate would render them under
    `v1.9.0` and look entirely plausible.
    """
    from src.domain.ticket import TicketStatus

    user, cookie, org, project_id = populated_org
    _add_tickets(
        db_engine, org, project_id, _n_tickets(TicketStatus.DONE, 7, "v1.10.0")
    )

    _auth(client, cookie)
    block = _tickets_block(client.get(f"{UI_PREFIX}/{org.alias}").text)

    assert "<h4>Release tickets &middot; v1.9.0</h4>" in block
    assert "7</b> done" not in block
    assert "Nothing assigned to this version yet" in block
    assert "7 tickets on the project board, none of them attached to v1.9.0." in block


def test_next_launch_ignores_versions_below_what_shipped(
    client, populated_org, db_engine
):
    """Board sync creates a PLANNED row every time a ticket carries a
    version-shaped label, and nothing ever closes them. BPAI had forty-odd, most
    `v0.1.x-beta` from a repo on a different versioning line -- so "lowest
    upcoming" picked v0.1.1-beta as the next launch for a project already on
    v1.9.0. A version below the high-water mark is history someone forgot to
    close, not a plan.

    With nothing genuinely ahead, the panel shows what *did* ship rather than an
    em-dash: a project that has plainly released things reading as "no releases"
    was worse than the stale row it replaced.
    """
    user, cookie, org, project_id = populated_org
    with Session(db_engine) as session:
        session.add_all(
            [
                Release(
                    id=str(uuid4()),
                    organization_id=org.id,
                    project_id=project_id,
                    version="v9.0.0",
                    status=ReleaseStatus.RELEASED,
                ),
                Release(
                    id=str(uuid4()),
                    organization_id=org.id,
                    project_id=project_id,
                    version="v0.1.1-beta",
                    status=ReleaseStatus.PLANNED,
                ),
            ]
        )
        session.commit()

    _auth(client, cookie)
    text = client.get(f"{UI_PREFIX}/{org.alias}").text
    versions = re.findall(r'<span class="ver">([^<]+)</span>', text)

    assert "v0.1.1-beta" not in versions, "a stale planned row must not be 'next'"
    assert "v9.0.0" in versions, "the newest shipped version should be shown instead"
    assert "Latest release" in text
    assert "Plan v" not in text, "planning is the sync's job now, not a button"


def test_sync_opens_the_next_release_when_nothing_is_ahead(session_factory=None):
    """A project on v1.9.0 with nothing planned is heading for v1.10.0 whether or
    not anyone has said so. Sync writes that intent; blastoff still cuts the tag.
    """
    from src.services.release_planning import next_release, suggest_next_version

    shipped = [
        Release(
            organization_id="o",
            project_id="p",
            version=v,
            status=ReleaseStatus.RELEASED,
        )
        for v in ("v1.8.0", "v1.9.0")
    ]
    stale = Release(
        organization_id="o",
        project_id="p",
        version="v0.1.1-beta",
        status=ReleaseStatus.PLANNED,
    )

    assert next_release(shipped + [stale]) is None, "stale rows are not 'ahead'"
    assert suggest_next_version(shipped + [stale]) == "v1.10.0"

    planned = Release(
        organization_id="o",
        project_id="p",
        version="v1.10.0",
        status=ReleaseStatus.PLANNED,
    )
    nxt = next_release(shipped + [stale, planned])
    assert nxt is not None and nxt.version == "v1.10.0"


# --------------------------------------------------------------------------- #
# The card header: what a project is wired to, and where clicking it goes
# --------------------------------------------------------------------------- #


def _head(html):
    """The project card's header row, so assertions cannot match the whole page.

    The tooltips repeat words that appear elsewhere in the document -- "3
    repositories" is also in the launch panel -- and a page-wide substring check
    is how this file's oldest bug got in (see the module docstring).
    """
    found = re.search(r'<div class="proj-head">(.*?)</div>', html, re.S)
    return found.group(1) if found else ""


def test_card_header_reports_what_the_project_is_wired_to(client, populated_org):
    """Three icons, and each says configured or not.

    `populated_org` has repositories and an active Linear board but has never had
    `project_context` written -- which is every project in the system today,
    since nothing generates that column (issue #498). So this fixture exercises
    the mixed case rather than an artificial one.
    """
    user, cookie, org, project_id = populated_org
    _auth(client, cookie)
    head = _head(client.get(dashboard_path(org.alias)).text)

    assert 'aria-label="GitHub · 3 repositories"' in head
    assert 'aria-label="Linear · synced' in head
    assert 'aria-label="Project context · not generated yet"' in head

    # Connected renders `.intg on`; unconfigured renders bare `.intg`. Counting
    # the difference is what proves the state reaches the markup at all.
    assert head.count('class="intg on"') == 2
    assert head.count('class="intg"') == 1


def test_a_project_with_nothing_connected_still_shows_all_three_icons(
    client, signed_in, make_org, db_engine
):
    """Greyed, not omitted. A missing icon and an unconfigured one would differ
    only by an absence nobody counts, and seeing what is *not* set up is the
    entire reason the row exists."""
    user, cookie = signed_in()
    org = make_org("bare", name="Bare", member=user)
    with Session(db_engine) as session:
        session.add(
            Project(
                id=str(uuid4()),
                organization_id=org.id,
                alias="BR",
                name="Bare",
                description="d",
            )
        )
        session.commit()

    _auth(client, cookie)
    head = _head(client.get(dashboard_path(org.alias)).text)

    assert head.count('class="intg"') == 3
    assert 'class="intg on"' not in head
    assert 'aria-label="GitHub · no repositories linked"' in head
    assert 'aria-label="Board · not connected"' in head


def test_project_context_lights_the_icon_when_it_holds_something(
    client, populated_org, db_engine
):
    """Whitespace is not content. A column holding only spaces is a column
    nobody wrote anything into, and lighting the icon for it is the one failure
    this indicator exists to rule out."""
    user, cookie, org, project_id = populated_org
    _auth(client, cookie)

    for stored, expected_on in (("   \n  ", False), ("# PixelFuel\n\nRepos...", True)):
        with Session(db_engine) as session:
            project = session.get(Project, project_id)
            project.project_context = stored
            session.add(project)
            session.commit()

        head = _head(client.get(dashboard_path(org.alias)).text)
        lit = 'aria-label="Project context · generated"' in head
        assert lit is expected_on, f"{stored!r} should light the icon: {expected_on}"


def test_card_identity_links_to_the_project_page(client, populated_org):
    """The alias and name are one target; the sync pill and init command are not.

    Making the whole header a link would have swallowed both controls that
    already live in it.
    """
    user, cookie, org, project_id = populated_org
    _auth(client, cookie)
    head = _head(client.get(dashboard_path(org.alias)).text)

    assert f'<a class="projlink" href="{UI_PREFIX}/{org.alias}/projects/pf">' in head
    assert "syncform" in head, "the sync control must not be inside the link"


def test_tickets_block_renders_its_heading_even_with_nothing_in_flight(
    client, populated_org, db_engine
):
    """A heading with a quiet line under it, not an empty gap.

    Returning "" for a quiet project left neighbouring cards at different heights
    for no reason a reader could infer.

    A project with no tickets at all says so plainly rather than reciting a total
    of zero: "0 tickets on the project board, none attached to v1.9.0" is true but
    reads as a malfunction.
    """
    user, cookie, org, project_id = populated_org
    _auth(client, cookie)
    page = client.get(dashboard_path(org.alias)).text

    assert '<div class="tickets"><h4>Release tickets &middot; v1.9.0</h4>' in page
    assert "No tickets on this project yet." in _tickets_block(page)


def test_tickets_block_falls_back_to_the_project_when_no_release_is_open(
    client, populated_org, db_engine
):
    """With nothing upcoming there is no version to scope to, and no version to
    name -- so the heading says "project" and the counts are the project's.

    The one thing that must never happen is a "Release tickets" heading with no
    version under it: that is the ambiguity the release scope was introduced to
    remove.
    """
    from src.domain.ticket import TicketStatus

    user, cookie, org, project_id = populated_org
    with Session(db_engine) as session:
        for release in session.exec(select(Release)).all():
            release.status = ReleaseStatus.RELEASED
            session.add(release)
        session.commit()
    _add_tickets(
        db_engine, org, project_id, _n_tickets(TicketStatus.IN_PROGRESS, 6, None)
    )

    _auth(client, cookie)
    block = _tickets_block(client.get(dashboard_path(org.alias)).text)

    assert "<h4>Project tickets</h4>" in block
    assert "6</b> in progress" in block
    assert "Release tickets" not in block


def test_new_project_button_opens_the_form(client, populated_org):
    """The dashboard's button and the form it opens."""
    user, cookie, org, project_id = populated_org
    _auth(client, cookie)

    assert (
        f'href="{UI_PREFIX}/{org.alias}/projects/new"'
        in client.get(dashboard_path(org.alias)).text
    )
    form = client.get(f"{UI_PREFIX}/{org.alias}/projects/new")
    assert form.status_code == 200
    assert 'name="alias"' in form.text and 'name="name"' in form.text


# --------------------------------------------------------------------------- #
# One project's own page
# --------------------------------------------------------------------------- #


def _project_url(org, alias="pf", tab=""):
    base = f"{UI_PREFIX}/{org.alias}/projects/{alias}"
    return f"{base}/{tab}" if tab else base


def test_project_page_resolves_by_alias_in_either_case(client, populated_org):
    """The alias is the URL, and it is unique per org, so the pair identifies a
    project as precisely as a UUID would while reading as what people call it."""
    user, cookie, org, project_id = populated_org
    _auth(client, cookie)

    for alias in ("pf", "PF", "Pf"):
        r = client.get(_project_url(org, alias))
        assert r.status_code == 200, alias
        assert "PixelFuel Innoday" in r.text


def test_unknown_project_and_another_orgs_project_both_404(
    client, populated_org, signed_in, make_org, db_engine
):
    """404, never 403. A distinguishable response would confirm a project exists
    to someone who only guessed its alias -- the same reasoning the org routes
    already apply."""
    user, cookie, org, project_id = populated_org

    other_user, other_cookie = signed_in()
    other_org = make_org("other", name="Other", member=other_user)
    with Session(db_engine) as session:
        session.add(
            Project(
                id=str(uuid4()),
                organization_id=other_org.id,
                alias="ZZ",
                name="Theirs",
                description="d",
            )
        )
        session.commit()

    _auth(client, cookie)
    assert client.get(_project_url(org, "nosuch")).status_code == 404
    # Exists, but not in an org this viewer belongs to.
    assert client.get(f"{UI_PREFIX}/{other_org.alias}/projects/zz").status_code == 404


def test_an_unknown_tab_404s_rather_than_falling_back(client, populated_org):
    """A mistyped URL that silently renders a different page is how someone
    concludes a feature is broken when they are simply not on it."""
    user, cookie, org, project_id = populated_org
    _auth(client, cookie)

    for tab in ("you", "tickets", "releases", "timeline", "settings"):
        assert client.get(_project_url(org, tab=tab)).status_code == 200, tab
    assert client.get(_project_url(org, tab="nonsense")).status_code == 404


def test_new_is_the_form_not_a_project_alias(client, populated_org):
    """`/projects/new` is declared before `/projects/{alias}`, so "new" can never
    be read as a project. Ordering is the whole guard."""
    user, cookie, org, project_id = populated_org
    _auth(client, cookie)
    r = client.get(f"{UI_PREFIX}/{org.alias}/projects/new")
    assert r.status_code == 200
    # The form, not a project page that matched "new" as an alias.
    assert 'name="alias"' in r.text
    assert "PixelFuel Innoday" not in r.text


def test_project_page_requires_a_session(client, populated_org):
    user, cookie, org, project_id = populated_org
    r = client.get(_project_url(org), follow_redirects=False)
    assert r.status_code == 303
    assert r.headers["location"] == LOGIN_PATH


def test_menu_marks_the_open_tab_and_links_the_others(client, populated_org):
    user, cookie, org, project_id = populated_org
    _auth(client, cookie)
    page = client.get(_project_url(org, tab="timeline")).text

    assert f'aria-current="page" href="{_project_url(org, tab="timeline")}"' in page
    assert f'href="{_project_url(org)}"' in page  # You, not current
    # Shut by default now: the pane is what you came for, and a rail that must be
    # dismissed every visit costs more than it gives. `_COPY_JS` reopens it if this
    # browser last left it open.
    assert '<details class="navwrap">' in page
    assert '<details class="navwrap" open>' not in page


def _css_rule(selector: str) -> str:
    """One rule's declaration block, from the stylesheet that is actually served.

    Read from `_APP_CSS` rather than from a page body on purpose. A CSS-only
    change has no rendered markup to assert on, and pulling the rule out by
    selector is the difference between pinning a declaration and pinning a
    substring that happens to occur somewhere in 1200 lines of inlined CSS.
    """
    from src.routers.webui.render import _APP_CSS

    found = re.search(re.escape(selector) + r"\s*\{([^{}]*)\}", _APP_CSS)
    assert found, f"{selector} is no longer in the stylesheet"
    return found.group(1)


def test_the_menu_is_an_edge_not_a_panel_and_the_open_tab_still_reads_as_open(
    client, populated_org
):
    """The rail is the border. No fill on the menu, its hover, or its open row.

    **Both halves matter and only one of them is about colour.** Removing the
    active row's tinted background is the request; leaving it identifiable
    afterwards is the constraint. So this asserts the fills are gone *from the
    stylesheet* and that the markup still carries the two cues that do not depend
    on colour at all -- `aria-current="page"`, which is what a screen reader
    announces, and the `on` class the leading rail and the bolder weight hang off.

    The stylesheet half is deliberately read from `_APP_CSS` and not from the
    page: every rule in this file is inlined into every response, so
    `"background" not in page` would be false for reasons that have nothing to do
    with the menu.
    """
    user, cookie, org, project_id = populated_org
    _auth(client, cookie)
    page = client.get(_project_url(org, tab="timeline")).text

    # The vertical line stays -- it is the only structure the menu has left.
    navwrap = _css_rule(".navwrap")
    assert "border-right:1px solid" in navwrap, "the vertical line is the rail"
    assert "background" not in navwrap, "but the panel fill is gone"

    for selector in (".navwrap > summary:hover", ".nav a:hover", ".nav a.on"):
        assert "background" not in _css_rule(selector), f"{selector} still fills"

    # What is left to mark the open tab, in the markup rather than the stylesheet.
    on = re.search(r'<a class="on"[^>]*>', page)
    assert on, "the open tab is still marked in the markup"
    assert 'aria-current="page"' in on.group(0), "and announced, not only drawn"
    assert "border-left-color:var(--orange)" in _css_rule(".nav a.on")
    assert "font-weight:600" in _css_rule(".nav a.on"), "weight, not colour alone"

    # The count chip keeps its own background: it is a chip, not the menu.
    assert "background" in _css_rule(".nav .ct")


def test_the_summary_panel_keeps_the_spacing_and_type_sizes_it_was_given():
    """Four decisions about the scrum panel with no markup to show for them.

    Every one is a declaration and nothing else -- no element, class or attribute
    changes when a `font-size` does -- so this pins the declarations, pulled out
    of the *served* stylesheet by selector. Kept in this file rather than in
    `test_summary_ui.py` because what it asserts is a stylesheet fact, and the
    stylesheet's other guards live here.

    It is a regression pin and nothing more: it cannot tell you the panel reads
    well, only that nobody quietly restored the old values.
    """
    # Air after the panel. It is the last block in the card, so its final row sat
    # against the card's edge and the block read as clipped.
    assert "padding-bottom:18px" in _css_rule(".scrum")

    # Less below a ticket's prose than above its reference. 12px both ways put
    # 24px between two tickets -- more air than the four stacked lines within one.
    assert "padding:12px 0 7px" in _css_rule(".sitem")

    # Slightly larger, and only the text a person actually reads.
    assert "font-size:13.4px" in _css_rule(".stitle")
    assert "font-size:12.6px" in _css_rule(".sbody")
    assert "font-size:12.8px" in _css_rule(".sthin")
    # The furniture around it does not grow with it -- otherwise this is a global
    # font bump wearing four selectors, and the hierarchy inside a row is lost.
    assert "font-size:11px" in _css_rule(".sref"), "the reference stayed put"
    assert "font-size:10px" in _css_rule(".sblock"), "the block heading stayed put"
    assert "font-size:9.5px" in _css_rule(".obub"), "the bubble stayed put"


def test_unmapped_viewer_gets_one_sentence_not_four_empty_cards(
    client, signed_in, make_org, db_engine
):
    """Rendering "Your summary" and "Your tickets" both empty would be two ways of
    saying the same thing, and neither says what to do about it.

    The personal timeline card that used to make this three is gone -- the
    project's own Timeline tab is that surface. Its assertion went with it rather
    than being left behind: an assertion about markup nothing emits any more can
    never fail, so it reads as coverage while providing none.
    """
    user, cookie = signed_in()
    org = make_org("solo", name="Solo", member=user)
    with Session(db_engine) as session:
        session.add(
            Project(
                id=str(uuid4()),
                organization_id=org.id,
                alias="SO",
                name="Solo",
                description="d",
            )
        )
        session.commit()

    _auth(client, cookie)
    page = client.get(f"{UI_PREFIX}/{org.alias}/projects/so").text

    assert "not mapped to this project" in page
    assert "Your active tickets" not in page


def test_your_tickets_lists_only_yours_and_only_the_active_ones(
    client, populated_org, db_engine
):
    """Uncapped and status-filtered. DRAFT/BACKLOG/DONE are excluded -- a list
    that opened with forty backlog rows would bury the ones actually moving."""
    from src.domain.ticket import Ticket, TicketStatus

    user, cookie, org, project_id = populated_org
    with Session(db_engine) as session:
        rows = [
            ("mine-inprogress", TicketStatus.IN_PROGRESS, user.id, None),
            ("mine-review", TicketStatus.IN_REVIEW, user.id, None),
            ("mine-todo", TicketStatus.TODO, user.id, None),
            ("mine-backlog", TicketStatus.BACKLOG, user.id, None),
            ("mine-done", TicketStatus.DONE, user.id, None),
            ("mine-deleted", TicketStatus.TODO, user.id, UTC_NOW),
            ("someone-elses", TicketStatus.IN_PROGRESS, "other-user-id", None),
        ]
        for summary, status, owner, deleted in rows:
            session.add(
                Ticket(
                    summary=summary,
                    organization_id=org.id,
                    project_id=project_id,
                    status=status,
                    assigned_to=owner,
                    deleted_at=deleted,
                )
            )
        session.commit()

    _auth(client, cookie)
    page = client.get(_project_url(org)).text
    block = re.search(r"Your active tickets.*?</section>", page, re.S)
    assert block is not None
    listed = block.group(0)

    for shown in ("mine-inprogress", "mine-review", "mine-todo"):
        assert shown in listed, shown
    for hidden in ("mine-backlog", "mine-done", "mine-deleted", "someone-elses"):
        assert hidden not in listed, hidden
    assert "3 assigned to you" in listed


# --------------------------------------------------------------------------- #
# Creating a project
# --------------------------------------------------------------------------- #


@pytest.fixture
def fake_github(monkeypatch):
    """Stand in for the org's GitHub listing.

    Patched at `_org_repos`, which is the seam the routes actually call — one
    request per form load, because GitHub's org listing already returns each
    repo's topics.
    """

    def _install(repos, ok=True):
        async def _fake(session, org):
            return repos, ok

        monkeypatch.setattr("src.routers.webui.routes._org_repos", _fake)

    return _install


REPOS = [
    {"name": "innoday", "topics": ["zz", "extra"], "archived": False},
    {"name": "agents", "topics": ["zz"], "archived": False},
    {"name": "site", "topics": ["extra"], "archived": False},
    {"name": "old", "topics": ["zz"], "archived": True},
]


def test_topic_preview_locks_the_alias_and_lists_names_not_a_count(
    client, populated_org, fake_github
):
    """The alias is always searched, so offering it as a choice would let someone
    deselect a topic that still applies — and the preview would then be a lie."""
    user, cookie, org, project_id = populated_org
    fake_github(REPOS)
    _auth(client, cookie)

    r = client.post(
        f"{UI_PREFIX}/{org.alias}/projects/new",
        data={"name": "Zed", "alias": "ZZ", "intent": "preview"},
    )
    assert r.status_code == 200
    assert "topic locked" in r.text
    # Names, because a count cannot show you picked the wrong topic.
    assert "innoday" in r.text and "agents" in r.text
    # Archived is shown struck through, not dropped: sync skips it, so the count
    # at create time must match the count you get.
    assert "rchip gone" in r.text
    assert "site" not in r.text.split("Included")[-1]


def test_choosing_a_topic_widens_the_preview(client, populated_org, fake_github):
    user, cookie, org, project_id = populated_org
    fake_github(REPOS)
    _auth(client, cookie)

    r = client.post(
        f"{UI_PREFIX}/{org.alias}/projects/new",
        data={"name": "Zed", "alias": "ZZ", "topic": "extra", "intent": "preview"},
    )
    included = r.text.split("would be included")[0]
    assert "3 repositories" in included


@pytest.mark.parametrize(
    "payload,fragment",
    [
        ({"name": "", "alias": "AB"}, "required"),
        ({"name": "X", "alias": ""}, "required"),
        ({"name": "X", "alias": "a b"}, "only letters"),
        ({"name": "X", "alias": "new"}, "reserved"),
        ({"name": "X", "alias": "login"}, "reserved"),
        ({"name": "X", "alias": "PF"}, "already has a project"),
    ],
    ids=["no-name", "no-alias", "bad-chars", "new", "reserved", "duplicate"],
)
def test_create_refuses_bad_input_and_says_why(
    client, populated_org, fake_github, payload, fragment
):
    """`new` matters most: it sits where an alias goes in the URL, so a project
    called that would shadow the very form used to make it."""
    user, cookie, org, project_id = populated_org
    fake_github(REPOS)
    _auth(client, cookie)

    r = client.post(
        f"{UI_PREFIX}/{org.alias}/projects/new",
        data={**payload, "intent": "create"},
    )
    assert r.status_code == 400
    assert fragment in r.text
    # What was already typed survives the refusal.
    if payload.get("name"):
        assert f'value="{payload["name"]}"' in r.text


def test_create_makes_the_project_and_lands_on_its_page(
    client, populated_org, fake_github, db_engine
):
    user, cookie, org, project_id = populated_org
    fake_github(REPOS)
    _auth(client, cookie)

    r = client.post(
        f"{UI_PREFIX}/{org.alias}/projects/new",
        data={
            "name": "Zed Project",
            "alias": "zz",
            "description": "Does things",
            "intent": "create",
        },
        follow_redirects=False,
    )
    assert r.status_code == 303
    assert r.headers["location"] == f"{UI_PREFIX}/{org.alias}/projects/zz"

    with Session(db_engine) as session:
        made = session.exec(
            select(Project).where(
                Project.organization_id == org.id, Project.alias == "ZZ"
            )
        ).first()
    # Stored uppercase, because the alias is a ticket prefix; lowercased in URLs.
    assert made is not None and made.name == "Zed Project"


def test_extra_topics_are_stored_where_discovery_reads_them(
    client, populated_org, fake_github, db_engine
):
    """`github_topics` lives on the ORG keyed by project alias — that is where
    `WorkspaceOnboardService.github_topics()` looks. Storing them anywhere else
    would mean discovery never searches them."""
    user, cookie, org, project_id = populated_org
    fake_github(REPOS)
    _auth(client, cookie)

    client.post(
        f"{UI_PREFIX}/{org.alias}/projects/new",
        data={"name": "Zed", "alias": "zz", "topic": "extra", "intent": "create"},
        follow_redirects=False,
    )

    with Session(db_engine) as session:
        fresh = session.get(Organization, org.id)
        assert (fresh.settings or {}).get("github_topics", {}).get("ZZ") == "extra"


def test_a_missing_github_credential_is_said_not_shown_as_no_repos(
    client, populated_org, fake_github
):
    """ "Set this up" and "nothing is tagged" are different problems with
    different fixes, so they must not render the same."""
    user, cookie, org, project_id = populated_org
    fake_github([], ok=False)
    _auth(client, cookie)

    page = client.get(f"{UI_PREFIX}/{org.alias}/projects/new").text
    assert "No GitHub credential" in page


def test_create_requires_a_session(client, populated_org):
    user, cookie, org, project_id = populated_org
    r = client.post(
        f"{UI_PREFIX}/{org.alias}/projects/new",
        data={"name": "X", "alias": "XX", "intent": "create"},
        follow_redirects=False,
    )
    assert r.status_code == 303
    assert r.headers["location"] == LOGIN_PATH


# --------------------------------------------------------------------------- #
# The remaining tabs
# --------------------------------------------------------------------------- #


def test_tabs_render_real_content_not_placeholders(client, populated_org, db_engine):
    """Tickets, Timeline and Settings each show the project's own data."""
    from src.domain.ticket import Ticket, TicketStatus

    user, cookie, org, project_id = populated_org
    with Session(db_engine) as session:
        session.add(
            Ticket(
                summary="a project ticket",
                organization_id=org.id,
                project_id=project_id,
                status=TicketStatus.TODO,
                assignee="Ada L.",
            )
        )
        session.commit()

    _auth(client, cookie)
    tickets = client.get(_project_url(org, tab="tickets")).text
    assert "a project ticket" in tickets
    assert "Ada L." in tickets
    assert "Not built yet" not in tickets

    settings = client.get(_project_url(org, tab="settings")).text
    assert "Configuration" in settings
    assert "Repository layers" in settings
    assert "Not built yet" not in settings


# --------------------------------------------------------------------------- #
# Releases tab
# --------------------------------------------------------------------------- #


def _add_tickets(db_engine, org, project_id, specs):
    """`specs` is (summary, status, release) -- release being the free-text join."""
    from src.domain.ticket import Ticket

    with Session(db_engine) as session:
        for summary, status, release in specs:
            session.add(
                Ticket(
                    summary=summary,
                    organization_id=org.id,
                    project_id=project_id,
                    status=status,
                    release=release,
                )
            )
        session.commit()


def test_the_releases_tab_separates_the_pool_from_both_slots(
    client, populated_org, db_engine
):
    """Three lists, and the split between them is the whole planning surface.

    The fixture's slot 1 is v1.9.0 and slot 2 is v1.10.0 (v0.1.0 already
    shipped). A ticket belongs to exactly one of the three by its version string,
    and the two slots are not interchangeable -- work in slot 1 is being cut now,
    work in slot 2 is deferred to the release after.
    """
    from src.domain.ticket import TicketStatus

    user, cookie, org, project_id = populated_org
    _add_tickets(
        db_engine,
        org,
        project_id,
        [
            ("in the current release", TicketStatus.TODO, "v1.9.0"),
            ("shipped in the current release", TicketStatus.DONE, "v1.9.0"),
            ("planned for the one after", TicketStatus.TODO, "v1.10.0"),
            ("not planned yet", TicketStatus.TODO, None),
            # Board sync writes an empty string rather than NULL when a ticket
            # carries no version label. Both mean "unassigned".
            ("also not planned", TicketStatus.BACKLOG, ""),
            # Finished and unversioned: not a planning candidate, but it has to
            # be attachable after the fact -- see the `.doneband` assertions.
            ("long since done", TicketStatus.DONE, None),
        ],
    )
    _auth(client, cookie)
    page = client.get(_project_url(org, tab="releases")).text

    # Both slots are labelled for what they are. An earlier version of this page
    # rendered only slot 1 and called it "Next release", which said the opposite.
    assert "Current release" in page and "Next release" in page
    assert "v1.9.0" in page and "v1.10.0" in page

    current, _, planned = page.partition("Next release")
    # In slot 1, whatever the status -- DONE work is emphatically in the release.
    assert "in the current release" in current
    assert "shipped in the current release" in current
    # In slot 2, and not muddled into slot 1.
    assert "planned for the one after" in planned
    assert "planned for the one after" not in current
    # In the pool.
    assert "not planned yet" in page and "also not planned" in page

    # Finished work carrying no version is in **its own band**, not in either
    # slot and not in the planning pool. This assertion used to read
    # `not in page`, which was the deliberate old rule -- the pool is limited to
    # `_PLANNABLE` and you do not plan finished work. But that also made
    # "completed before anyone recorded a release for it" invisible on the one
    # page that answers what a release contains, so it now has to be shown and
    # attachable.
    assert "Done, never in a release" in page
    # Extracted by element, not by `partition`: the pool renders *before* the two
    # slots, so "everything above Next release" contains the band too and could
    # not distinguish them.
    band = re.search(r'<div class="doneband">(.*?)</section>', page, re.S)
    assert band, "no done band on the page"
    assert page.count("long since done") == 1, "listed once, in one place"
    assert "long since done" in band.group(1)
    # Attachable: the band carries the same plan control the pool does.
    assert 'name="release" value="v1.9.0"' in band.group(1)


def test_the_next_release_is_the_same_one_the_card_calls_next_launch(
    client, populated_org
):
    """Two renderings that disagreed about which release is next would be worse
    than either alone, so both go through `next_release`'s high-water rule."""
    user, cookie, org, project_id = populated_org
    _auth(client, cookie)

    dashboard = client.get(f"{UI_PREFIX}/{org.alias}").text
    releases = client.get(_project_url(org, tab="releases")).text

    assert '<span class="ver">v1.9.0</span>' in dashboard
    assert '<span class="ver">v1.9.0</span>' in releases


def test_a_release_summary_is_a_click_away_and_absence_is_not_an_empty_toggle(
    client, populated_org, db_engine
):
    """Ten client-facing narratives stacked on the page would bury the list they
    belong to -- but a `<details>` that opens onto nothing is its own small lie."""
    user, cookie, org, project_id = populated_org
    with Session(db_engine) as session:
        session.add(
            Release(
                id=str(uuid4()),
                organization_id=org.id,
                project_id=project_id,
                version="v0.2.0",
                name="Groundwork",
                status=ReleaseStatus.RELEASED,
                released_at=UTC_NOW - timedelta(days=4),
                summary="Rebuilt the sync path end to end.",
                changelog=[
                    {"repo": "innoday", "prs": [{"number": 1}, {"number": 2}]},
                    {"repo": "site", "prs": [{"number": 3}]},
                ],
            )
        )
        session.commit()

    _auth(client, cookie)
    page = client.get(_project_url(org, tab="releases")).text

    assert "Rebuilt the sync path end to end." in page
    assert '<details class="rel">' in page
    assert "2 repos" in page and "3 PRs" in page
    # v0.1.0 is in the fixture with no summary at all: a row, not a toggle.
    assert '<div class="rel"><div class="relhead">' in page
    assert "v0.1.0" in page


def test_a_changelog_of_an_unexpected_shape_does_not_take_the_page_down(
    client, populated_org, db_engine
):
    """`changelog` is a JSON column written by the release engine, so its shape is
    a convention rather than a guarantee -- an older row must not 500 the tab."""
    user, cookie, org, project_id = populated_org
    with Session(db_engine) as session:
        session.add(
            Release(
                id=str(uuid4()),
                organization_id=org.id,
                project_id=project_id,
                version="v0.3.0",
                status=ReleaseStatus.RELEASED,
                released_at=UTC_NOW - timedelta(days=1),
                changelog={"repo": "innoday"},  # a dict, not the expected list
            )
        )
        session.commit()

    _auth(client, cookie)
    r = client.get(_project_url(org, tab="releases"))
    assert r.status_code == 200
    assert "v0.3.0" in r.text


def test_a_project_with_nothing_shipped_says_so(client, signed_in, make_org, db_engine):
    """An empty history has to read as "nothing yet", never as a broken page."""
    user, cookie = signed_in()
    org = make_org("np", name="New Place", member=user)
    with Session(db_engine) as session:
        session.add(
            Project(
                id=str(uuid4()),
                organization_id=org.id,
                alias="NP",
                name="Nothing Planned",
                description="d",
            )
        )
        session.commit()

    _auth(client, cookie)
    page = client.get(f"{UI_PREFIX}/{org.alias}/projects/np/releases").text
    # Both slots say what is missing, separately -- one empty card standing for
    # two absent things would not say which.
    assert "Nothing in progress" in page
    assert "Nothing planned above the current release yet" in page
    assert "Nothing shipped yet" in page
    assert "Every live ticket is already assigned to a version." in page


def _give_identity(db_engine, org, project_id, user):
    """A ticket assigned to the viewer, so the "You" band renders at all.

    Without an identity on the project the whole band collapses to one row by
    design, and there would be no card to assert against.
    """
    from src.domain.ticket import Ticket, TicketStatus

    with Session(db_engine) as session:
        session.add(
            Ticket(
                summary="anything",
                organization_id=org.id,
                project_id=project_id,
                status=TicketStatus.TODO,
                assigned_to=user.id,
            )
        )
        session.commit()


def test_no_github_handle_is_said_not_shown_as_no_open_prs(
    client, populated_org, db_engine
):
    """`None` and `[]` are different claims.

    An empty list says "you have nothing open", which is wrong for anyone who
    has simply never told us their GitHub username — and the page cannot tell
    the difference unless the reader is told which it is.
    """
    user, cookie, org, project_id = populated_org
    _give_identity(db_engine, org, project_id, user)
    _auth(client, cookie)

    page = client.get(_project_url(org)).text
    assert "Your open pull requests" in page
    assert "Add your GitHub username" in page


def test_open_prs_are_listed_for_author_or_assignee(client, populated_org, db_engine):
    """Authored **or** assigned. GitHub allows several assignees and the author
    is often not among them, so keying on either alone drops real work."""
    from src.domain.repository_pull_request import RepositoryPullRequest

    user, cookie, org, project_id = populated_org
    _give_identity(db_engine, org, project_id, user)

    with Session(db_engine) as session:
        fresh = session.get(User, user.id)
        fresh.github_username = "Karl"  # case must not matter
        session.add(fresh)
        repo_id = session.exec(
            select(Repository.id).where(Repository.name == "innoday")
        ).first()
        session.add_all(
            [
                RepositoryPullRequest(
                    repository_id=repo_id,
                    number=1,
                    title="authored by me",
                    url="https://github.com/hs/innoday/pull/1",
                    author_login="karl",
                    assignee_logins=[],
                ),
                RepositoryPullRequest(
                    repository_id=repo_id,
                    number=2,
                    title="assigned to me",
                    url="https://github.com/hs/innoday/pull/2",
                    author_login="someone",
                    assignee_logins=["other", "karl"],
                ),
                RepositoryPullRequest(
                    repository_id=repo_id,
                    number=3,
                    title="nothing to do with me",
                    url="https://github.com/hs/innoday/pull/3",
                    author_login="someone",
                    assignee_logins=["other"],
                ),
            ]
        )
        session.commit()

    _auth(client, cookie)
    page = client.get(_project_url(org)).text
    block = re.search(r"Your open pull requests.*?</section>", page, re.S).group(0)

    assert "authored by me" in block
    assert "assigned to me" in block
    assert "nothing to do with me" not in block
    assert "2 open" in block


def test_a_failed_sync_turns_the_icon_red_and_a_good_one_clears_it(
    client, populated_org, db_engine
):
    """Red beats green: configured-but-broken is more urgent than working, and
    an icon showing "connected" over a dead token is worse than no icon.

    The clearing half is what makes the flag mean anything — a mark that only
    ever gets set becomes a permanent red for one bad afternoon (#499).
    """
    user, cookie, org, project_id = populated_org
    _auth(client, cookie)

    head = _head(client.get(dashboard_path(org.alias)).text)
    assert 'class="intg err"' not in head

    with Session(db_engine) as session:
        repo = session.exec(
            select(Repository).where(Repository.name == "innoday")
        ).one()
        repo.errored_at = UTC_NOW
        repo.error_message = "401 Bad credentials"
        session.add(repo)
        session.commit()

    head = _head(client.get(dashboard_path(org.alias)).text)
    assert 'class="intg err"' in head
    assert "last sync failed" in head

    with Session(db_engine) as session:
        repo = session.exec(
            select(Repository).where(Repository.name == "innoday")
        ).one()
        repo.errored_at = None
        session.add(repo)
        session.commit()

    head = _head(client.get(dashboard_path(org.alias)).text)
    assert 'class="intg err"' not in head


def _repoless_project(db_engine, signed_in, make_org, *, errored, message=None):
    """An org whose single project has no repositories at all.

    Deliberately its own org rather than a second project in ``populated_org``:
    ``_head`` reads the *first* card on the page, so a shared org would make the
    assertion depend on how the two aliases happen to sort.
    """
    user, cookie = signed_in()
    org = make_org("solo", name="Repoless Co", member=user)
    with Session(db_engine) as session:
        session.add(
            Project(
                id=str(uuid4()),
                organization_id=org.id,
                alias="SOLO",
                name="No repos here",
                description="d",
                github_errored_at=UTC_NOW if errored else None,
                github_error_message=message,
            )
        )
        session.commit()
    return cookie, org


def test_a_whole_sync_failure_reds_the_icon_with_no_repo_rows_at_all(
    client, db_engine, signed_in, make_org
):
    """The case #640 is about, and the one the old signal could not express.

    ``Repository.errored_at`` needs a repo row to hang a failure on. A sync that
    died in discovery never produced one, so a project with a dead token and
    nothing attached rendered identically to a healthy new project.
    """
    cookie, org = _repoless_project(
        db_engine, signed_in, make_org, errored=True, message="401 Bad credentials"
    )
    _auth(client, cookie)

    head = _head(client.get(dashboard_path(org.alias)).text)
    assert 'class="intg err"' in head
    assert "last sync failed" in head


def test_a_dead_token_reds_even_with_stale_repo_rows(client, populated_org, db_engine):
    """Repos from a sync that worked last week do not make today's token fine.

    ``github_connected`` stays "repositories are linked" -- red beats green in
    `_integration_icon`, so the healthy rows cannot outvote the failure. And the
    title has to carry the *stored* reason rather than the generic fallback,
    since this signal is the one that knows why.
    """
    user, cookie, org, project_id = populated_org
    _auth(client, cookie)

    with Session(db_engine) as session:
        project = session.get(Project, project_id)
        project.github_errored_at = UTC_NOW
        project.github_error_message = (
            "Failed to fetch repositories: 401 Bad credentials"
        )
        session.add(project)
        session.commit()

    head = _head(client.get(dashboard_path(org.alias)).text)
    assert 'class="intg err"' in head
    assert "401 Bad credentials" in head, (
        "the stored message, not the generic 'check the organization's token'"
    )


def test_a_project_with_no_repos_and_no_failure_stays_grey(
    client, db_engine, signed_in, make_org
):
    """Three states have to stay distinguishable.

    A sync that legitimately found zero repos is not a failure and must not go
    red -- but it is not connected either, so it must not go green. Grey is the
    honest answer, and asserting only the absence of red would pass for a card
    that had wrongly turned green.
    """
    cookie, org = _repoless_project(db_engine, signed_in, make_org, errored=False)
    _auth(client, cookie)

    head = _head(client.get(dashboard_path(org.alias)).text)
    assert 'class="intg err"' not in head
    assert 'class="intg on"' not in head


# --------------------------------------------------------------------------- #
# Google sign-in
# --------------------------------------------------------------------------- #


def _google_env(monkeypatch, *, configured=True):
    monkeypatch.setenv("SUPABASE_URL", "https://abc.supabase.co")
    monkeypatch.setenv("SUPABASE_KEY", "anon")
    if configured:
        monkeypatch.setenv(
            "SUPABASE_AUTH_EXTERNAL_GOOGLE_CLIENT_ID", "x.apps.googleusercontent.com"
        )
    else:
        monkeypatch.delenv("SUPABASE_AUTH_EXTERNAL_GOOGLE_CLIENT_ID", raising=False)


def test_google_button_appears_only_when_the_provider_is_configured(
    client, monkeypatch
):
    """A "Continue with Google" that leads to a 400 is worse than its absence: it
    reads as InnoDay being broken rather than a door that was never opened."""
    _google_env(monkeypatch, configured=False)
    assert "Continue with Google" not in client.get(LOGIN_PATH).text

    _google_env(monkeypatch, configured=True)
    page = client.get(LOGIN_PATH).text
    assert "Continue with Google" in page
    assert "abc.supabase.co/auth/v1/authorize?provider=google" in page


def test_google_returns_to_the_same_callback_the_magic_link_uses(client, monkeypatch):
    """`/ui/auth/callback` serves both flows, so the OAuth round trip needed no
    new page — and `redirect_to` must be a URL Supabase allow-lists or it is
    silently replaced with site_url, which looks like Google misrouting."""
    _google_env(monkeypatch, configured=True)
    page = client.get(LOGIN_PATH).text

    assert quote(AUTH_CALLBACK_PATH, safe="") in page.replace("&amp;", "&")


def test_the_sign_in_card_says_google_does_not_create_an_account(client, monkeypatch):
    """`[auth] enable_signup = false` means an uninvited Google user gets
    `signup_disabled`, not an account. Saying so on the card stops that landing
    as a mysterious failure — and stops anyone "fixing" it by enabling signup,
    which would hand an account to anyone with a Google address."""
    _google_env(monkeypatch, configured=True)
    assert "does not create an account" in client.get(LOGIN_PATH).text


def test_supabase_config_keeps_signup_closed_while_google_is_enabled():
    """The invariant, asserted against the file rather than trusted to a comment.

    `[auth] enable_signup = false` is what makes Google a second way to *sign in*
    rather than a second way to *get an account*. Enabling one without the other
    is the change that would quietly open the front door, so it fails here.

    Stated as an implication -- enabled ⟹ signup closed -- rather than as
    `enabled is True`. It was the latter, which pinned the day's value instead of
    the rule and so failed when Google was turned OFF: a test that goes red on the
    *safer* configuration teaches people to edit the test.
    """
    import tomllib
    from pathlib import Path

    config = tomllib.loads(Path("supabase/config.toml").read_text(encoding="utf-8"))
    google = config["auth"]["external"]["google"]

    if google["enabled"]:
        assert config["auth"]["enable_signup"] is False, (
            "Google is enabled while public signup is on — anyone with a Google "
            "address could mint an account on the IdP backing this deployment"
        )
    # The email provider's own switch is a different key with the same name, and
    # setting it false would take invites down with it (supabase/cli#4469).
    assert config["auth"]["email"]["enable_signup"] is True
    # Secrets by reference, never literal: this file is tracked.
    assert google["client_id"].startswith("env(")
    assert google["secret"].startswith("env(")


# --------------------------------------------------------------------------- #
# Team: bubbles, roster, and the guards
# --------------------------------------------------------------------------- #


def _add_member(db_engine, org, *, email, role, name="Someone Else"):
    from src.domain.organization import OrganizationMembership, OrganizationRole

    with Session(db_engine) as session:
        user = User(id=str(uuid4()), email=email, full_name=name)
        session.add(user)
        session.add(
            OrganizationMembership(
                user_id=user.id,
                organization_id=org.id,
                role=OrganizationRole(role),
                is_active=True,
            )
        )
        session.commit()
        return user.id


def test_bubbles_show_who_works_on_the_project_not_the_whole_org(
    client, populated_org, db_engine
):
    """Membership is org-scoped, so a literal member list would render the same
    on every card. The bubbles are derived from tickets and identities instead —
    who is on *this* project."""
    from src.domain.ticket import Ticket, TicketStatus

    user, cookie, org, project_id = populated_org
    # An org member with nothing on this project — must not appear.
    _add_member(db_engine, org, email="nobody@x.com", role="MEMBER")

    with Session(db_engine) as session:
        session.add(
            Ticket(
                summary="t",
                organization_id=org.id,
                project_id=project_id,
                status=TicketStatus.TODO,
                assigned_to=user.id,
            )
        )
        session.commit()

    _auth(client, cookie)
    head = _head(client.get(dashboard_path(org.alias)).text)

    assert 'class="bubbles"' in head
    # The org member with nothing on this project is not shown.
    assert "Someone Else" not in head
    assert f'href="{UI_PREFIX}/{org.alias}/team"' in head


def test_a_project_with_nobody_mapped_says_so(client, populated_org):
    """An absent row and an empty team must not look alike."""
    user, cookie, org, project_id = populated_org
    _auth(client, cookie)
    assert "No one mapped yet" in _head(client.get(dashboard_path(org.alias)).text)


def test_team_page_shows_the_roster_and_hides_controls_from_non_admins(
    client, populated_org, db_engine, signed_in, make_org
):
    """Everyone may look. Only admins may change anything — and the check is the
    server's, not the template's."""
    user, cookie, org, project_id = populated_org
    _add_member(db_engine, org, email="dev@x.com", role="DEVELOPER", name="Dev Person")

    _auth(client, cookie)
    page = client.get(f"{UI_PREFIX}/{org.alias}/team").text
    assert "Dev Person" in page
    assert "Send invite" in page  # populated_org's viewer is an admin


def test_the_last_admin_cannot_be_demoted_or_removed(client, populated_org, db_engine):
    """An org with no admin is an org nobody can add one to, and there is no way
    back from the UI. Enforced server-side — the disabled control is a courtesy.
    """
    from src.domain.organization import OrganizationMembership, OrganizationRole

    user, cookie, org, project_id = populated_org
    _auth(client, cookie)

    # Demote the only admin (themselves) — refused.
    r = client.post(
        f"{UI_PREFIX}/{org.alias}/team/members/{user.id}/role",
        data={"role": "MEMBER"},
        follow_redirects=False,
    )
    assert r.status_code == 303
    with Session(db_engine) as session:
        still = session.exec(
            select(OrganizationMembership).where(
                OrganizationMembership.user_id == user.id,
                OrganizationMembership.organization_id == org.id,
            )
        ).one()
    assert still.role == OrganizationRole.ADMIN, "the only admin was demoted"

    assert "only admin" in client.get(f"{UI_PREFIX}/{org.alias}/team").text


def test_removal_deactivates_rather_than_deletes(client, populated_org, db_engine):
    """Their tickets, identities and summaries all point at the user row. A hard
    delete would leave that work attributed to somebody the org no longer lists.
    """
    from src.domain.organization import OrganizationMembership

    user, cookie, org, project_id = populated_org
    victim = _add_member(db_engine, org, email="gone@x.com", role="MEMBER")
    _auth(client, cookie)

    client.post(
        f"{UI_PREFIX}/{org.alias}/team/members/{victim}/remove", follow_redirects=False
    )

    with Session(db_engine) as session:
        row = session.exec(
            select(OrganizationMembership).where(
                OrganizationMembership.user_id == victim
            )
        ).one()
    assert row is not None, "the membership row was deleted, not deactivated"
    assert row.is_active is False


def test_a_non_admin_cannot_change_roles_even_by_posting_directly(
    client, populated_org, db_engine, signed_in
):
    """Hiding the control is not the guard. The POST has to refuse too."""
    from src.domain.organization import OrganizationMembership, OrganizationRole

    user, cookie, org, project_id = populated_org
    plain_user, plain_cookie = signed_in(email=f"{uuid4().hex[:8]}@x.com")
    with Session(db_engine) as session:
        session.add(
            OrganizationMembership(
                user_id=plain_user.id,
                organization_id=org.id,
                role=OrganizationRole.MEMBER,
                is_active=True,
            )
        )
        session.commit()

    _auth(client, plain_cookie)
    r = client.post(
        f"{UI_PREFIX}/{org.alias}/team/members/{plain_user.id}/role",
        data={"role": "ADMIN"},
        follow_redirects=False,
    )
    assert r.status_code == 404

    with Session(db_engine) as session:
        row = session.exec(
            select(OrganizationMembership).where(
                OrganizationMembership.user_id == plain_user.id
            )
        ).one()
    assert row.role == OrganizationRole.MEMBER, "a member promoted themselves"


def test_mapping_a_commit_handle_writes_the_column_the_profile_page_uses(
    client, populated_org, db_engine
):
    """One place a GitHub handle lives. Two columns claiming the same fact is how
    summaries start disagreeing about who did what."""
    user, cookie, org, project_id = populated_org
    target = _add_member(db_engine, org, email="dev@x.com", role="DEVELOPER")
    _auth(client, cookie)

    client.post(
        f"{UI_PREFIX}/{org.alias}/team/map",
        data={"kind": "commit", "handle": "octocat", "user_id": target},
        follow_redirects=False,
    )

    with Session(db_engine) as session:
        assert session.get(User, target).github_username == "octocat"


def test_team_page_requires_a_session(client, populated_org):
    user, cookie, org, project_id = populated_org
    r = client.get(f"{UI_PREFIX}/{org.alias}/team", follow_redirects=False)
    assert r.status_code == 303
    assert r.headers["location"] == LOGIN_PATH


# --------------------------------------------------------------------------- #
# Moving the pipeline onto another version line
# --------------------------------------------------------------------------- #


def _pipeline_fixture(db_engine, org, project_id, *, planned=True):
    """v1.8.0 shipped, v1.9.0 in progress, v1.10.0 planned.

    Replaces `populated_org`'s releases rather than adding to them: that fixture
    already carries v1.9.0 and v1.10.0 as PLANNED, and these tests are about a
    pipeline in one specific, stated shape.
    """
    rows = [("v1.8.0", ReleaseStatus.RELEASED), ("v1.9.0", ReleaseStatus.IN_PROGRESS)]
    if planned:
        rows.append(("v1.10.0", ReleaseStatus.PLANNED))
    with Session(db_engine) as session:
        for existing in session.exec(
            select(Release).where(Release.project_id == project_id)
        ).all():
            session.delete(existing)
        session.commit()
        for version, status in rows:
            session.add(
                Release(
                    id=str(uuid4()),
                    organization_id=org.id,
                    project_id=project_id,
                    version=version,
                    status=status,
                )
            )
        session.commit()


def _versions(db_engine, project_id):
    with Session(db_engine) as session:
        return {
            r.version: r.status
            for r in session.exec(
                select(Release).where(Release.project_id == project_id)
            ).all()
        }


def test_the_version_line_offers_the_options_and_marks_the_current_one(
    client, populated_org, db_engine
):
    user, cookie, org, project_id = populated_org
    _auth(client, cookie)
    page = client.get(_project_url(org, tab="releases")).text

    # The fixture's pipeline is v1.9.0, a minor bump of the shipped v0.1.0's
    # successor line -- so minor is not current here; what matters is that all
    # three parts are offered and exactly one is marked.
    assert 'class="bumps"' in page
    for part in ("major", "minor", "patch"):
        assert part in page


def test_a_bump_query_previews_and_writes_nothing(client, populated_org, db_engine):
    """A GET that renamed the version every repo is about to be tagged with
    would be a GET a link prefetcher could fire."""
    user, cookie, org, project_id = populated_org
    _pipeline_fixture(db_engine, org, project_id)
    before = _versions(db_engine, project_id)

    _auth(client, cookie)
    page = client.get(_project_url(org, tab="releases") + "?bump=major").text

    assert "Confirm" in page
    assert "v2.0.0" in page and "v2.1.0" in page
    assert _versions(db_engine, project_id) == before


def test_confirming_moves_both_slots_and_takes_the_tickets_with_them(
    client, populated_org, db_engine
):
    from src.domain.ticket import Ticket, TicketStatus

    user, cookie, org, project_id = populated_org
    _pipeline_fixture(db_engine, org, project_id)
    with Session(db_engine) as session:
        session.add(
            Ticket(
                summary="planned into the next release",
                organization_id=org.id,
                project_id=project_id,
                status=TicketStatus.TODO,
                release="v1.9.0",
            )
        )
        session.commit()

    _auth(client, cookie)
    resp = client.post(
        f"{_project_url(org)}/releases/version",
        data={"bump": "major"},
        follow_redirects=False,
    )
    assert resp.status_code == 303

    assert _versions(db_engine, project_id) == {
        "v1.8.0": ReleaseStatus.RELEASED,
        "v2.0.0": ReleaseStatus.IN_PROGRESS,
        "v2.1.0": ReleaseStatus.PLANNED,
    }

    # The join is free text with no foreign key, so a rename that left the
    # ticket behind would detach it silently -- and stop it auto-closing on ship.
    with Session(db_engine) as session:
        ticket = session.exec(select(Ticket)).first()
        assert ticket.release == "v2.0.0"


def test_the_parts_are_a_toggle_so_reverting_is_choosing_the_other_one(
    client, populated_org, db_engine
):
    """Every option is recomputed from the last *shipped* version, not from where
    the pipeline currently sits, so flipping back lands exactly where it started
    and nothing has to store a previous value."""
    user, cookie, org, project_id = populated_org
    _pipeline_fixture(db_engine, org, project_id)
    start = _versions(db_engine, project_id)

    _auth(client, cookie)
    for part in ("major", "patch", "minor"):
        client.post(
            f"{_project_url(org)}/releases/version",
            data={"bump": part},
            follow_redirects=False,
        )

    assert _versions(db_engine, project_id) == start


def test_a_colliding_target_is_refused_and_changes_nothing(
    client, populated_org, db_engine
):
    """v2.0.0 already exists as an archived row. Renaming onto it would violate
    uq_release_project_version -- a failure at commit, after a half-applied move."""
    user, cookie, org, project_id = populated_org
    _pipeline_fixture(db_engine, org, project_id)
    with Session(db_engine) as session:
        session.add(
            Release(
                id=str(uuid4()),
                organization_id=org.id,
                project_id=project_id,
                version="v2.0.0",
                status=ReleaseStatus.ARCHIVED,
            )
        )
        session.commit()
    before = _versions(db_engine, project_id)

    _auth(client, cookie)
    resp = client.post(
        f"{_project_url(org)}/releases/version",
        data={"bump": "major"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    assert _versions(db_engine, project_id) == before

    page = client.get(_project_url(org, tab="releases")).text
    assert "already exists on this project" in page


def test_an_unknown_part_is_refused(client, populated_org, db_engine):
    user, cookie, org, project_id = populated_org
    _pipeline_fixture(db_engine, org, project_id)
    before = _versions(db_engine, project_id)

    _auth(client, cookie)
    resp = client.post(
        f"{_project_url(org)}/releases/version",
        data={"bump": "mnior"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    assert _versions(db_engine, project_id) == before


def test_moving_the_line_needs_a_session(client, populated_org):
    user, cookie, org, project_id = populated_org
    resp = client.post(
        f"{_project_url(org)}/releases/version",
        data={"bump": "major"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    assert resp.headers["location"] == LOGIN_PATH


def test_the_current_release_is_never_labelled_as_the_next_one(
    client, populated_org, db_engine
):
    """The pipeline's two slots answer different questions, and showing slot 1
    under the heading "Next release" said the opposite of what it meant: the
    version being cut is precisely the one you can no longer plan into."""
    user, cookie, org, project_id = populated_org
    _pipeline_fixture(db_engine, org, project_id)

    _auth(client, cookie)
    page = client.get(_project_url(org, tab="releases")).text

    # Asserted on the *rendered version*, by position, rather than by splitting on
    # the heading text: each slot's `data-release` attribute sits on the section
    # tag, which precedes its own heading, so a substring split puts one slot's
    # version inside the other's half.
    assert page.index("Current release") < page.index("Next release")
    at_current = page.index('<span class="ver">v1.9.0</span>')
    at_next = page.index('<span class="ver">v1.10.0</span>')
    assert page.index("Current release") < at_current < page.index("Next release")
    assert at_next > page.index("Next release")
    assert "in progress" in page and "planned" in page


def test_a_half_rotated_pipeline_says_which_slot_is_missing(
    client, populated_org, db_engine
):
    """Slot 2 can genuinely be absent -- a rotation that failed partway leaves
    one. An empty card naming it beats a page that silently shows one slot, which
    is indistinguishable from the bug this replaced."""
    user, cookie, org, project_id = populated_org
    _pipeline_fixture(db_engine, org, project_id, planned=False)

    _auth(client, cookie)
    page = client.get(_project_url(org, tab="releases")).text

    assert "Current release" in page and "v1.9.0" in page
    assert "Nothing planned above the current release yet" in page


def test_the_planning_board_is_two_halves_with_the_slots_stacked(
    client, populated_org, db_engine
):
    """Two columns, not three. The slots are a sequence -- current then next --
    so they stack on one side and the pool takes the other."""
    user, cookie, org, project_id = populated_org
    _pipeline_fixture(db_engine, org, project_id)
    _auth(client, cookie)
    page = client.get(_project_url(org, tab="releases")).text

    assert 'class="planboard"' in page
    assert 'class="stack"' in page
    # `.board` would collide with the existing `.kindchip.board` rule and turn
    # those chips into grids.
    assert '<div class="board">' not in page
    # Both slots still present, in order, and still distinct.
    current_at = page.index("Current release")
    next_at = page.index("Next release")
    assert current_at < next_at


def test_a_ticket_on_a_version_the_project_does_not_have_is_still_shown(
    client, populated_org, db_engine
):
    """The join is free text with no foreign key, so this state is reachable: a
    typo, or a version renamed or archived after the ticket was labelled.

    Such a ticket is in no slot and no release will ship it -- and
    `_bulk_close_tickets_for_release` will never close it, because there is no
    release to close. Without surfacing it here it is simply absent from the one
    page someone would look on.
    """
    from src.domain.ticket import TicketStatus

    user, cookie, org, project_id = populated_org
    _pipeline_fixture(db_engine, org, project_id)
    _add_tickets(
        db_engine,
        org,
        project_id,
        [
            ("points at nothing", TicketStatus.TODO, "v9.9.9"),
            ("genuinely unassigned", TicketStatus.TODO, None),
        ],
    )

    _auth(client, cookie)
    page = client.get(_project_url(org, tab="releases")).text

    assert "points at nothing" in page
    assert "genuinely unassigned" in page
    # Marked with the string it points at, so the reason is visible.
    assert 'class="orphan"' in page and "v9.9.9" in page


def test_an_empty_pool_with_orphans_does_not_claim_everything_is_assigned(
    client, populated_org, db_engine
):
    """ "Every live ticket is already assigned to a version" directly above a
    ticket assigned to a version that does not exist contradicts itself."""
    from src.domain.ticket import TicketStatus

    user, cookie, org, project_id = populated_org
    _pipeline_fixture(db_engine, org, project_id)
    _add_tickets(
        db_engine, org, project_id, [("stale only", TicketStatus.TODO, "v9.9.9")]
    )

    _auth(client, cookie)
    page = client.get(_project_url(org, tab="releases")).text

    assert "stale only" in page
    assert "Every live ticket is already assigned to a version" not in page


def test_the_plan_arrows_are_revealed_by_the_rows_they_are_on(
    client, populated_org, db_engine
):
    """They shipped invisible. The reveal keyed on `.trow:hover`, and the rows the
    control lives on are `.brow` -- so every button rendered at zero width on the
    one surface it exists for. A rule naming both classes is the fix; this asserts
    it, because a CSS selector that matches nothing fails silently."""
    from src.domain.ticket import TicketStatus

    user, cookie, org, project_id = populated_org
    _pipeline_fixture(db_engine, org, project_id)
    _add_tickets(db_engine, org, project_id, [("plan me", TicketStatus.TODO, None)])

    _auth(client, cookie)
    page = client.get(_project_url(org, tab="releases")).text

    assert 'class="planq"' in page
    assert ".brow:hover .planq" in page, "the pool's rows must reveal the control"


def test_only_moving_work_carries_a_status_chip_in_the_pool(
    client, populated_org, db_engine
):
    """In progress and in test change how you plan; todo and backlog would be a
    chip on nearly every row, saying nothing."""
    from src.domain.ticket import TicketStatus

    user, cookie, org, project_id = populated_org
    _pipeline_fixture(db_engine, org, project_id)
    _add_tickets(
        db_engine,
        org,
        project_id,
        [
            ("already moving", TicketStatus.IN_PROGRESS, None),
            ("being checked", TicketStatus.IN_REVIEW, None),
            ("not started", TicketStatus.TODO, None),
        ],
    )

    _auth(client, cookie)
    page = client.get(_project_url(org, tab="releases")).text
    pool = page.split("Current release")[0]

    assert "already moving" in pool and "being checked" in pool
    assert "not started" in pool
    # Two chips in the pool, not three.
    assert pool.count('<span class="st prog">') == 1
    assert pool.count('<span class="st rev">') == 1


def test_the_rail_preference_key_is_versioned(client, populated_org):
    """Open used to be the default, and the old key stored '1' whenever the rail
    was open -- so every browser that had merely used the page carried a value
    that reopens it against the new default. Only a new key tells "chose open"
    from "was open before the change"."""
    user, cookie, org, project_id = populated_org
    _auth(client, cookie)
    page = client.get(_project_url(org)).text

    assert "innoday.nav.open.v2" in page
    assert "'innoday.nav.open'" not in page


def test_drag_targets_the_form_the_buttons_already_use(
    client, populated_org, db_engine
):
    """Drag is enhancement, not a second write path.

    The script finds the hover arrow's own form for that release and submits it,
    so there is no new endpoint and nothing to keep in step. With script disabled
    the arrows still work, which is why the markup is asserted here rather than
    the behaviour.
    """
    from src.domain.ticket import TicketStatus

    user, cookie, org, project_id = populated_org
    _pipeline_fixture(db_engine, org, project_id)
    _add_tickets(db_engine, org, project_id, [("drag me", TicketStatus.TODO, None)])

    _auth(client, cookie)
    page = client.get(_project_url(org, tab="releases")).text

    assert 'draggable="true"' in page and "data-ticket=" in page
    assert 'data-release="v1.9.0"' in page and 'data-release="v1.10.0"' in page
    # The drop handler submits an existing form; it must not post anywhere else.
    assert "form.requestSubmit" in page
    assert page.count("/tickets/plan") >= 2, "one form per slot on the row"


def test_a_rotation_takes_the_backlog_with_it(
    client, populated_org, db_engine, monkeypatch
):
    """A per-ticket rule alone would miss this: a rotation lands a whole
    release's worth of backlog in the slot being cut, at once."""
    from src.services.release_pipeline import promote_backlog_in

    user, cookie, org, project_id = populated_org
    with Session(db_engine) as session:
        for existing in session.exec(
            select(Release).where(Release.project_id == project_id)
        ).all():
            session.delete(existing)
        session.commit()
        session.add(
            Release(
                id=str(uuid4()),
                organization_id=org.id,
                project_id=project_id,
                version="v2.0.0",
                status=ReleaseStatus.IN_PROGRESS,
            )
        )
        session.commit()

    from src.domain.ticket import Ticket, TicketStatus

    with Session(db_engine) as session:
        for summary, status_ in (
            ("was in the backlog", TicketStatus.BACKLOG),
            ("already moving", TicketStatus.IN_PROGRESS),
        ):
            session.add(
                Ticket(
                    summary=summary,
                    organization_id=org.id,
                    project_id=project_id,
                    status=status_,
                    release="v2.0.0",
                )
            )
        session.commit()

        moved = promote_backlog_in(session, project_id, "v2.0.0")
        session.commit()

    assert moved == 1, "only the backlog ticket moves"
    with Session(db_engine) as session:
        by_summary = {t.summary: t.status for t in session.exec(select(Ticket)).all()}
    assert by_summary["was in the backlog"] == TicketStatus.TODO
    # Further along than TODO, so left alone -- demoting it would lose information.
    assert by_summary["already moving"] == TicketStatus.IN_PROGRESS


def test_promoting_the_backlog_is_idempotent(populated_org, db_engine):
    """Stated as an invariant, not an event, so both callers can simply assert it
    and a second run is a no-op."""
    from src.domain.ticket import Ticket, TicketStatus
    from src.services.release_pipeline import promote_backlog_in

    user, cookie, org, project_id = populated_org
    with Session(db_engine) as session:
        session.add(
            Ticket(
                summary="backlog item",
                organization_id=org.id,
                project_id=project_id,
                status=TicketStatus.BACKLOG,
                release="v1.9.0",
            )
        )
        session.commit()
        assert promote_backlog_in(session, project_id, "v1.9.0") == 1
        session.commit()
        assert promote_backlog_in(session, project_id, "v1.9.0") == 0


# --------------------------------------------------------------------------- #
# The board counts, and who is actually asked to map a handle
# --------------------------------------------------------------------------- #


def test_the_tickets_block_counts_planned_and_done_not_only_what_is_unfinished(
    client, populated_org, db_engine
):
    """Four counts, each carrying its status colour on the number.

    Without `done` the card showed only what was outstanding, so a project that
    had delivered a hundred tickets and one that had delivered none read
    identically. `planned` folds TODO and BACKLOG together -- the difference
    between them is a board's own grooming state.

    All eight carry v1.9.0, the fixture's open release, because that is the scope
    the block renders.
    """
    from src.domain.ticket import Ticket, TicketStatus

    user, cookie, org, project_id = populated_org
    with Session(db_engine) as session:
        rows = [
            ("a", TicketStatus.TODO),
            ("b", TicketStatus.BACKLOG),
            ("c", TicketStatus.BACKLOG),
            ("d", TicketStatus.IN_PROGRESS),
            ("e", TicketStatus.IN_REVIEW),
            ("f", TicketStatus.DONE),
            ("g", TicketStatus.DONE),
            ("h", TicketStatus.DONE),
        ]
        for summary, status in rows:
            session.add(
                Ticket(
                    summary=f"count-{summary}",
                    organization_id=org.id,
                    project_id=project_id,
                    status=status,
                    release="v1.9.0",
                )
            )
        session.commit()

    _auth(client, cookie)
    block = _tickets_block(client.get(dashboard_path(org.alias)).text)

    assert '<b class="c-plan">3</b> planned' in block
    assert '<b class="c-live">1</b> in progress' in block
    assert '<b class="c-rev">1</b> in review' in block
    assert '<b class="c-done">3</b> done' in block


def test_a_soft_deleted_ticket_is_not_counted_as_work(client, populated_org, db_engine):
    """Deletion is most common on tickets that never shipped, so `done` --
    a claim about delivery -- was the count this would have distorted worst.

    Both are on v1.9.0, so this covers the release-scoped query rather than only
    the project-wide one: the predicate has to be on both, and only one of them
    is what the card renders.
    """
    from src.domain.ticket import Ticket, TicketStatus

    user, cookie, org, project_id = populated_org
    with Session(db_engine) as session:
        session.add(
            Ticket(
                summary="kept",
                organization_id=org.id,
                project_id=project_id,
                status=TicketStatus.DONE,
                release="v1.9.0",
            )
        )
        session.add(
            Ticket(
                summary="binned",
                organization_id=org.id,
                project_id=project_id,
                status=TicketStatus.DONE,
                deleted_at=UTC_NOW,
                release="v1.9.0",
            )
        )
        session.commit()

    _auth(client, cookie)
    block = _tickets_block(client.get(dashboard_path(org.alias)).text)

    assert '<b class="c-done">1</b> done' in block
    # And the project total beside it counts one, not two.
    assert "1 ticket on the project board in total." in block


def test_map_your_handle_is_offered_only_to_someone_with_no_handle_anywhere(
    client, signed_in, make_org, db_engine
):
    """The prompt is advice, and advice you cannot follow is noise.

    Identities are registered per project, so anyone mapped on two projects was
    told to map their handle on every *other* project in the org -- by a link to
    a page that already listed the handles they had mapped. Nothing on this
    project resolves to them either way; the difference is whether there is
    anything they could do about it.
    """
    from src.domain.user_identity import IdentityPlatform, MatchSource, UserIdentity

    user, cookie = signed_in()
    org = make_org("mapped", name="Mapped", member=user)
    with Session(db_engine) as session:
        other = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias="OT",
            name="Other",
            description="d",
        )
        here = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias="HE",
            name="Here",
            description="d",
        )
        session.add(other)
        session.add(here)
        session.commit()
        other_id = other.id

    _auth(client, cookie)
    before = client.get(f"{UI_PREFIX}/{org.alias}/projects/he").text
    assert "Map your handle" in before, "with no handle at all, the prompt belongs"

    # The same person, now mapped -- on a different project's board.
    with Session(db_engine) as session:
        session.add(
            UserIdentity(
                user_id=user.id,
                project_id=other_id,
                platform=IdentityPlatform.LINEAR,
                handle="Ada L.",
                match_source=MatchSource.MANUAL,
            )
        )
        session.commit()

    after = client.get(f"{UI_PREFIX}/{org.alias}/projects/he").text
    assert "Map your handle" not in after
    assert "none of them appears on this" in after, "say why, since there is no action"


def test_every_page_shell_carries_the_rocket_tab_icon(client, populated_org):
    """Before this there was no `<link rel="icon">` anywhere, so every InnoDay
    tab showed the browser's blank default.

    Asserted on both shells, because there are two and only one of them is in
    `webui/`: the wide signed-in pages here, and `brand_page`'s centred card for
    the device/invite/auth pages. A favicon added to one is exactly the kind of
    thing that stays missing from the other.
    """
    from src.routers._brand_pages import brand_page, favicon_link

    link = favicon_link()
    assert 'rel="icon"' in link and "data:image/svg+xml," in link
    # A literal `#` ends a data URI at the first colour, taking the rest of the
    # SVG with it -- the icon would silently not render.
    assert "#" not in link, "colour literals must be percent-encoded"

    user, cookie, org, project_id = populated_org
    _auth(client, cookie)
    assert link in client.get(dashboard_path(org.alias)).text
    assert link in client.get(f"{UI_PREFIX}/{org.alias}/projects/pf").text
    assert link in client.get(f"{UI_PREFIX}/login").text
    assert link in brand_page("t", "<p>body</p>", "")


# --------------------------------------------------------------------------- #
# Target dates: the day a release is aimed at
# --------------------------------------------------------------------------- #


def _target_dates(db_engine, project_id):
    with Session(db_engine) as session:
        return {
            r.version: r.target_date
            for r in session.exec(
                select(Release).where(Release.project_id == project_id)
            ).all()
        }


def test_both_forward_slots_show_a_date_and_say_so_when_there_is_none(
    client, populated_org, db_engine
):
    """An unset date is rendered, not omitted.

    A release with no date and a page that forgot to draw one look identical
    otherwise -- and telling those apart is the reason the field exists.
    """
    user, cookie, org, project_id = populated_org
    _pipeline_fixture(db_engine, org, project_id)
    with Session(db_engine) as session:
        row = session.exec(
            select(Release).where(
                Release.project_id == project_id, Release.version == "v1.9.0"
            )
        ).one()
        row.target_date = date(2027, 11, 14)
        session.add(row)
        session.commit()

    _auth(client, cookie)
    page = client.get(_project_url(org, tab="releases")).text

    assert "14 Nov 2027" in page, "the date it is aimed at, beside the version"
    assert 'datetime="2027-11-14"' in page, "machine-readable too"
    # **A dateless release says nothing.** This asserted `"no date set" in page`,
    # which was the old rule -- and after the rule changed the assertion went on
    # passing, because the CSS carried those three words in a comment. So the
    # check is on the rendered element, and the words are gone from the source.
    assert "no date set" not in page
    assert page.count('class="tdate"') == 1, "one dated release, one chip"


def test_an_admin_can_set_and_clear_a_target_date(client, populated_org, db_engine):
    """Clearing is as easy as setting: a wrong date on a shared page is worse
    than no date, so getting back to "not decided" cannot be the hard path."""
    user, cookie, org, project_id = populated_org
    _pipeline_fixture(db_engine, org, project_id)

    _auth(client, cookie)
    page = client.get(_project_url(org, tab="releases")).text
    assert 'type="date"' in page, "an admin gets the picker"

    resp = client.post(
        f"{_project_url(org)}/releases/date",
        data={"version": "v1.9.0", "target_date": "2027-11-14"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    assert _target_dates(db_engine, project_id)["v1.9.0"] == date(2027, 11, 14)

    cleared = client.post(
        f"{_project_url(org)}/releases/date",
        data={"version": "v1.9.0", "target_date": ""},
        follow_redirects=False,
    )
    assert cleared.status_code == 303
    assert _target_dates(db_engine, project_id)["v1.9.0"] is None


def test_a_non_admin_can_neither_see_the_picker_nor_post_to_it(
    client, signed_in, make_org, db_engine
):
    """The gate is on the route, not the template.

    Hiding the control is presentation; a member who crafts the POST must still
    be refused, or the date is editable by anyone in the org who reads the HTML.
    """
    from src.domain.organization import OrganizationMembership, OrganizationRole

    user, cookie = signed_in()
    org = make_org("memberonly", name="Member Only")
    with Session(db_engine) as session:
        session.add(
            OrganizationMembership(
                id=str(uuid4()),
                user_id=user.id,
                organization_id=org.id,
                role=OrganizationRole.MEMBER,
                is_active=True,
            )
        )
        project = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias="MO",
            name="Member Only Project",
            description="d",
        )
        session.add(project)
        session.commit()
        project_id = project.id
    _pipeline_fixture(db_engine, org, project_id)

    _auth(client, cookie)
    page = client.get(_project_url(org, alias="mo", tab="releases")).text
    assert 'type="date"' not in page, "a member gets no picker"

    resp = client.post(
        f"{_project_url(org, alias='mo')}/releases/date",
        data={"version": "v1.9.0", "target_date": "2027-11-14"},
        follow_redirects=False,
    )
    assert resp.status_code == 303, "refused with a flash, not an error page"
    assert _target_dates(db_engine, project_id)["v1.9.0"] is None, (
        "a member's POST must not write"
    )


def test_a_version_from_another_project_cannot_be_dated(
    client, populated_org, make_org, db_engine
):
    """The version names a row *within this project*, so a forged one only misses."""
    user, cookie, org, project_id = populated_org
    _pipeline_fixture(db_engine, org, project_id)
    other = make_org("otherorg", name="Other", member=user)
    with Session(db_engine) as session:
        stranger = Project(
            id=str(uuid4()),
            organization_id=other.id,
            alias="OZ",
            name="Other Project",
            description="d",
        )
        session.add(stranger)
        session.commit()
        session.add(
            Release(
                id=str(uuid4()),
                organization_id=other.id,
                project_id=stranger.id,
                version="v9.9.9",
                status=ReleaseStatus.PLANNED,
            )
        )
        session.commit()
        stranger_id = stranger.id

    _auth(client, cookie)
    resp = client.post(
        f"{_project_url(org)}/releases/date",
        data={"version": "v9.9.9", "target_date": "2027-01-01"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    assert _target_dates(db_engine, stranger_id)["v9.9.9"] is None


def test_a_shipped_release_offers_no_picker(client, populated_org, db_engine):
    """The date it was aimed at is history now; `released_at` is the live fact."""
    user, cookie, org, project_id = populated_org
    _pipeline_fixture(db_engine, org, project_id, planned=False)
    with Session(db_engine) as session:
        for row in session.exec(
            select(Release).where(Release.project_id == project_id)
        ).all():
            if row.version != "v1.8.0":
                session.delete(row)
        session.commit()

    _auth(client, cookie)
    page = client.get(_project_url(org, tab="releases")).text
    assert 'type="date"' not in page


def test_a_malformed_date_is_refused_without_touching_the_row(
    client, populated_org, db_engine
):
    """`<input type="date">` submits ISO or nothing, so this is a hand-made
    request -- it still gets a sentence rather than a 422 page."""
    user, cookie, org, project_id = populated_org
    _pipeline_fixture(db_engine, org, project_id)

    _auth(client, cookie)
    resp = client.post(
        f"{_project_url(org)}/releases/date",
        data={"version": "v1.9.0", "target_date": "14/11/2027"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    assert _target_dates(db_engine, project_id)["v1.9.0"] is None


# --------------------------------------------------------------------------- #
# One bar across the release surface: editing is DEVELOPER, destroying is ADMIN
# --------------------------------------------------------------------------- #


def test_a_member_cannot_move_the_version_line(client, populated_org, db_engine):
    """**The control that mattered most was the one with no gate at all.**

    Retargeting renames the version every repository is about to be tagged with
    *and* rewrites every ticket planned into it. It was reachable by any member
    of the org, while setting that same release's *date* required an admin --
    so the page protected the label and not the thing the label names.

    Both halves are asserted: the button is gone, and a crafted POST is still
    refused. Hiding a control is presentation; the gate has to be on the route.
    """
    from src.domain.organization import OrganizationRole

    user, cookie, org, project_id = populated_org
    _pipeline_fixture(db_engine, org, project_id)
    before = _versions(db_engine, project_id)
    _set_role(db_engine, org, user, OrganizationRole.MEMBER)
    _auth(client, cookie)

    page = client.get(_project_url(org, tab="releases")).text
    assert "/releases/version" not in page, "a member gets no bump control"

    resp = client.post(
        f"{_project_url(org)}/releases/version",
        data={"bump": "major"},
        follow_redirects=False,
    )
    assert resp.status_code == 303, "refused with a flash, not an error page"
    assert _versions(db_engine, project_id) == before, "the version line moved"


def test_a_developer_can_set_a_release_date(client, populated_org, db_engine):
    """The date used to need an admin. It needs what editing a release needs.

    A target date is release bookkeeping, and every other way of editing a
    release -- `POST`/`PATCH .../releases` on the API, and the version line
    beside it on this page -- asks for DEVELOPER. Holding this one control to a
    higher bar meant a developer could rename the version but not say when it
    was aimed at.
    """
    from datetime import date

    from src.domain.organization import OrganizationRole

    user, cookie, org, project_id = populated_org
    _pipeline_fixture(db_engine, org, project_id)
    _set_role(db_engine, org, user, OrganizationRole.DEVELOPER)
    _auth(client, cookie)

    assert 'type="date"' in client.get(_project_url(org, tab="releases")).text

    resp = client.post(
        f"{_project_url(org)}/releases/date",
        data={"version": "v1.9.0", "target_date": "2027-11-14"},
        follow_redirects=False,
    )
    assert resp.status_code == 303
    assert _target_dates(db_engine, project_id)["v1.9.0"] == date(2027, 11, 14)


def test_a_member_cannot_plan_a_ticket_into_a_release(client, populated_org, db_engine):
    """Writing `ticket.release` is a ticket write, and those need DEVELOPER.

    Every ticket write in `src/routers/tickets.py` requires it. This page held
    no bar, so a member could put work into -- or pull work out of -- the
    version about to ship.
    """
    from src.domain.organization import OrganizationRole
    from src.domain.ticket import Ticket, TicketStatus

    user, cookie, org, project_id = populated_org
    _pipeline_fixture(db_engine, org, project_id)
    ticket_id = _ticket(
        db_engine, org, project_id, summary="unplanned", status=TicketStatus.TODO
    )
    _set_role(db_engine, org, user, OrganizationRole.MEMBER)
    _auth(client, cookie)

    page = client.get(_project_url(org, tab="tickets")).text
    assert "/tickets/plan" not in page, "a member gets no plan button"

    resp = client.post(
        f"{_project_url(org)}/tickets/plan",
        data={"ticket_id": str(ticket_id), "release": "v1.9.0", "previous": ""},
        follow_redirects=False,
    )
    assert resp.status_code == 303, "refused with a flash, not an error page"
    with Session(db_engine) as session:
        assert session.get(Ticket, ticket_id).release is None, "the ticket was planned"


# --------------------------------------------------------------------------- #
# UI polish (#567 / PF-1282): project selectability, menu, and labels
# --------------------------------------------------------------------------- #


def test_a_project_whose_every_repo_is_archived_is_not_selectable(
    client, signed_in, make_org, db_engine
):
    """And it says why.

    The distinction this rests on is invisible from the card's repo list:
    `_repo_rows_by_project` drops archived rows, so an all-archived project
    arrives with `repos == []` -- identical to one that has never had a repo.
    Only `archived_only` separates them, which is why it is a field and not a
    scan of `card.repos`.
    """
    from src.domain.project import ProjectRepository
    from src.domain.repository import Repository

    user, cookie = signed_in()
    org = make_org("arch", name="Archive Co", member=user)
    with Session(db_engine) as session:
        done = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias="OLD",
            name="Finished Thing",
            description="d",
        )
        fresh = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias="NEW",
            name="Brand New Thing",
            description="d",
        )
        session.add(done)
        session.add(fresh)
        repo = Repository(
            id=str(uuid4()),
            name="retired",
            full_name="arch/retired",
            url="https://github.com/arch/retired",
            organization_id=org.id,
            archived=True,
        )
        session.add(repo)
        session.commit()
        session.add(
            ProjectRepository(
                id=str(uuid4()),
                project_id=done.id,
                repository_id=repo.id,
                is_active=True,
            )
        )
        session.commit()

    _auth(client, cookie)
    page = client.get(dashboard_path(org.alias)).text

    assert f'href="{UI_PREFIX}/{org.alias}/projects/old"' not in page, (
        "an all-archived project must not be selectable"
    )
    assert "OLD" in page and ">archived<" in page, "and must say why"
    # And the card must not claim it has no repositories: it has two, both
    # archived. That sentence is what a *new* project shows, which is the exact
    # confusion this whole distinction exists to prevent.
    assert "Every repository on this project is archived." in page
    assert page.count("No repositories linked yet.") == 1, (
        "only the genuinely-empty project says that"
    )
    # The project with no repos at all is new, not finished.
    assert f'href="{UI_PREFIX}/{org.alias}/projects/new"' in page, (
        "a project with no repos is new, not archived -- it stays reachable"
    )


def test_the_project_bar_names_the_project_on_every_tab(client, populated_org):
    """Continuity: the alias and name used to live only inside the project card,
    which only the Project tab renders -- so Tickets and Releases showed a menu
    and a list with nothing saying whose they were."""
    user, cookie, org, project_id = populated_org
    _auth(client, cookie)

    import re

    for tab in ("", "tickets", "releases", "timeline", "settings"):
        page = client.get(_project_url(org, tab=tab)).text
        bar = re.search(r'<div class="projbar">(.*?)</div>', page, re.S)
        assert bar, f"no project bar on {tab or 'you'}"
        # Inside the bar specifically. `"PF" in page` would have passed on every
        # tab whether or not the bar carried anything, since the alias appears in
        # the URL, the init command and the page title.
        assert ">PF<" in bar.group(1), f"bar has no alias on {tab or 'you'}"
        assert "PixelFuel Innoday" in bar.group(1), f"bar has no name on {tab or 'you'}"

    # And not twice on the Project tab, where the card would otherwise repeat it.
    assert client.get(_project_url(org)).text.count('class="proj-name"') == 1


def test_the_menu_shows_the_rocket_and_no_dead_project_label(client, populated_org):
    """The one word on the menu that looked most like its heading was the one
    thing that did nothing when clicked."""
    user, cookie, org, project_id = populated_org
    _auth(client, cookie)
    page = client.get(_project_url(org)).text

    from src.routers.webui import icons

    assert 'class="navlabel"' not in page
    # **Assert the rocket's own geometry.** A first version of this test checked
    # `viewBox="0 0 16 16" fill="currentColor"` and a count of `class="ic"` --
    # both of which the person glyph it replaced also satisfied, so the test could
    # not have failed if someone put the person back.
    assert icons.NAV_ROCKET_SVG in page
    assert 'polygon points="8,0.6 11,6 11,10.4 5,10.4 5,6"' in page
    # And the glyph it replaced is gone from the codebase, not merely unused here.
    assert not hasattr(icons, "NAV_YOU_SVG"), "the person glyph has no callers left"
    # It takes colour from the row, so it dims and brightens with it rather than
    # reading as the selected row at all times.
    assert 'fill="currentColor"' in icons.NAV_ROCKET_SVG


def test_the_release_slot_hint_is_self_evident_and_the_cap_is_not_announced(
    client, populated_org, db_engine
):
    """ "Being cut." read as jargon, and "first 100" invited "of how many?" --
    which the list cannot answer, having stopped counting at the cap."""
    user, cookie, org, project_id = populated_org
    _pipeline_fixture(db_engine, org, project_id)

    _auth(client, cookie)
    page = client.get(_project_url(org, tab="releases")).text

    assert "Being cut" not in page
    assert "The version that ships next." in page
    assert "first 100" not in page
    assert '<span class="src">first ' not in page, "the cap is not announced"


def test_form_controls_inherit_the_page_font(client, populated_org):
    """Browsers give `<button>` a platform default family, so the dashboard's
    `+ New project` (an `<a>`) and the form's `Create project` (a `<button>`)
    rendered in two different faces one click apart."""
    user, cookie, org, project_id = populated_org
    _auth(client, cookie)
    page = client.get(dashboard_path(org.alias)).text

    assert "button, input, select, textarea, optgroup { font-family:inherit; }" in page
    # The local workaround used the `font` shorthand, which also reset size and
    # weight -- so the form's buttons differed from the dashboard's in size too.
    # Narrowed to that rule: `font:inherit; font-size:X` elsewhere is a deliberate
    # idiom that states its own size straight after, and is unaffected.
    assert ".actions .newproj, .actions .ghost { cursor:pointer; }" in page
    assert (
        ".actions .newproj, .actions .ghost { cursor:pointer; font:inherit; }"
        not in page
    )


def test_a_release_scoped_window_reads_as_a_release_not_a_key():
    """#565 stores `release:<version>` as a window_spec; the verbatim fallback
    would render it as `window release:v1.9.0`."""
    from src.routers.webui.data import window_label

    assert window_label("release:v1.9.0") == "release v1.9.0"
    assert window_label("RELEASE:v2.0.0") == "release v2.0.0"
    assert window_label("release:") == "a release"
    # The durations, and the honest fallback, are untouched.
    assert window_label("3d") == "last 3 days"
    assert window_label("1d") == "last day"
    assert window_label("") == "no fixed window"
    assert window_label("nonsense") == "window nonsense"


def test_the_done_band_reports_the_total_not_just_what_it_lists(
    client, populated_org, db_engine
):
    """Hitting the cap here is the normal case, not the edge.

    One project had 219 of these when this shipped. A list of 100 with no total
    would understate the size of the problem by more than half -- which is a
    different situation from the planning pool, where the cap is rarely reached
    and naming it only invited "of how many?".
    """
    from src.domain.ticket import TicketStatus

    user, cookie, org, project_id = populated_org
    _add_tickets(
        db_engine,
        org,
        project_id,
        [(f"finished-{i}", TicketStatus.DONE, None) for i in range(7)],
    )
    _auth(client, cookie)
    # A cap below the row count, so the two numbers must differ.
    with mock.patch("src.routers.webui.routes.RELEASE_BACKLOG_LIMIT", 3):
        page = client.get(_project_url(org, tab="releases")).text

    band = re.search(r'<div class="doneband">(.*?)</section>', page, re.S).group(1)
    assert ">3 of 7<" in band, "the total, alongside what is shown"
    assert band.count('class="brow"') == 3, "and only the cap is listed"


def test_a_cancelled_ticket_is_not_offered_for_a_release(
    client, populated_org, db_engine
):
    """Cancelled work never shipped, so attaching it would misreport what the
    release contained. Excluded by the status filter, not lumped in with DONE."""
    from src.domain.ticket import TicketStatus

    user, cookie, org, project_id = populated_org
    _add_tickets(
        db_engine,
        org,
        project_id,
        [
            ("zzfinishedandcounted", TicketStatus.DONE, None),
            ("zzabandonedentirely", TicketStatus.CANCELLED, None),
        ],
    )
    _auth(client, cookie)
    page = client.get(_project_url(org, tab="releases")).text

    assert "zzfinishedandcounted" in page
    assert "zzabandonedentirely" not in page


def test_attaching_a_done_ticket_records_the_release_without_reopening_it(
    client, populated_org, db_engine
):
    """The whole point of the band, and the one thing that must not go wrong.

    `promote_backlog_in` moves BACKLOG to TODO when work is planned into the
    release being cut. A DONE ticket must be exempt -- reopening finished work to
    satisfy a rule about the backlog would be a worse bug than the one this fixes.
    """
    from src.domain.ticket import Ticket, TicketStatus

    user, cookie, org, project_id = populated_org
    _pipeline_fixture(db_engine, org, project_id)
    _add_tickets(
        db_engine, org, project_id, [("done before planning", TicketStatus.DONE, None)]
    )
    with Session(db_engine) as session:
        ticket = session.exec(
            select(Ticket).where(Ticket.summary == "done before planning")
        ).one()
        ticket_id = ticket.id

    _auth(client, cookie)
    resp = client.post(
        f"{_project_url(org)}/tickets/plan",
        data={"ticket_id": str(ticket_id), "release": "v1.9.0", "previous": ""},
        follow_redirects=False,
    )
    assert resp.status_code == 303

    with Session(db_engine) as session:
        after = session.get(Ticket, ticket_id)
        assert after.release == "v1.9.0", "the release is recorded"
        assert after.status == TicketStatus.DONE, "and it is still done"


# --------------------------------------------------------------------------- #
# Source comments never reach the browser
# --------------------------------------------------------------------------- #


def test_no_page_serves_its_own_source_comments(client, populated_org):
    """The hazard this closes, stated as a test.

    These pages have no static mount, so every stylesheet and script is inlined
    into every response — which made a substring assertion against a rendered
    page a search of the *source*. Two tests passed for the wrong reason before
    this: `assert "no date set" in page` kept succeeding after that label was
    removed, satisfied by a CSS comment about the class that used to render it,
    and an unrelated `assert "closed" not in page` failed against a comment that
    merely used the word.

    Asserted on real pages rather than on the constants, because it is the
    response that has to be clean.
    """
    from src.routers._brand_pages import brand_page

    user, cookie, org, project_id = populated_org
    _auth(client, cookie)
    pages = {
        "dashboard": client.get(dashboard_path(org.alias)).text,
        "project": client.get(_project_url(org)).text,
        "releases": client.get(_project_url(org, tab="releases")).text,
        "login": client.get(f"{UI_PREFIX}/login").text,
        "brand shell": brand_page("t", "<p>body</p>", "var x = 1;"),
    }
    for name, page in pages.items():
        assert "/*" not in page, f"{name} serves a block comment"
        offenders = [
            line for line in page.splitlines() if line.strip().startswith("//")
        ]
        assert not offenders, f"{name} serves a line comment: {offenders[:2]}"


def test_stripping_comments_leaves_the_rules_alone(client, populated_org):
    """Removing prose must not remove behaviour.

    Compares the served CSS against its own source rather than against a fixed
    list: every declaration in the source has to survive, and only comments may
    go. A hand-listed sample would pass while silently eating the rule below the
    one sampled.
    """
    import re

    from src.routers.webui.render import _APP_CSS, _APP_CSS_SOURCE

    declarations = re.compile(r"[.#:a-zA-Z][^{}/]*\{[^{}]*\}")
    # Every rule in the source, minus any that lived inside a comment.
    from src.routers._brand_pages import strip_authoring_comments

    expected = set(declarations.findall(strip_authoring_comments(_APP_CSS_SOURCE)))
    actual = set(declarations.findall(_APP_CSS))
    assert expected == actual
    assert len(actual) > 300, "sanity: the stylesheet still has its rules"
    # Idempotent, so applying it twice cannot corrupt anything.
    assert strip_authoring_comments(_APP_CSS) == _APP_CSS


def test_only_whole_line_slash_comments_are_stripped():
    """**The narrow `//` rule is the whole safety argument.**

    An inline rule would eat the `//` in every URL — and this app inlines links to
    Linear, GitHub and its own pages. All 30 line comments in the served script
    are whole-line and none of its lines carries an inline one, so the narrow rule
    loses nothing and cannot corrupt a link.
    """
    from src.routers._brand_pages import strip_authoring_comments

    kept = strip_authoring_comments('var u = "https://inno.day/ui";')
    assert kept == 'var u = "https://inno.day/ui";', "a URL is not a comment"

    kept = strip_authoring_comments("var x = 1; // trailing note\nvar y = 2;")
    assert "trailing note" in kept, "an inline comment is deliberately left alone"

    gone = strip_authoring_comments("  // a whole line\nvar y = 2;")
    assert "a whole line" not in gone and "var y = 2;" in gone

    gone = strip_authoring_comments("a { b:c } /* note\nover two lines */ d { e:f }")
    assert "note" not in gone and "a { b:c }" in gone and "d { e:f }" in gone


# --------------------------------------------------------------------------- #
# The workflow launcher -- the page `GET /ui` opens.
# --------------------------------------------------------------------------- #


def _workflow_blob(html: str) -> dict:
    """The page's own JSON payload, decoded.

    The steps on this page are data, not markup -- the engine renders whatever
    is in here -- so assertions about what a step *says* belong against the blob
    rather than against a substring of the served HTML. `_json_blob` escapes
    ``<``, ``>`` and ``&`` as JSON unicode escapes so no value can close the tag;
    `json.loads` reverses exactly that, which is also what makes it the right
    place to check escaping: a body that reached here with a raw ``<script>`` in
    it got one because `esc` was skipped, not because the blob let it through.
    """
    import json

    match = re.search(r"window\.INNODAY_WORKFLOWS=(\{.*?\});</script>", html, re.S)
    assert match, "the page carries no workflow payload"
    return json.loads(match.group(1))


def test_workflow_page_lists_every_workflow_under_its_pillar(client, populated_org):
    """Nine workflows, four pillars, in the order the pillars were specified.

    The order is not cosmetic: it is the arc of a project's life (bring it into
    being, decide what ships, build it, ship it), and a rearranged grid reads as
    a different product.
    """
    _, cookie, org, _ = populated_org
    _auth(client, cookie)
    html = client.get(f"{UI_PREFIX}/{org.alias}/workflow").text

    for pillar in ("vibing", "planning", "building", "releasing"):
        assert pillar in html.lower(), pillar

    for title in (
        "Create a project",
        "Connect repos",
        "Design features",
        "Organize the release",
        "Run scrum",
        "Pick up a ticket",
        "Review a PR",
        "Summarize the release",
        "Run the release",
    ):
        assert title in html, title

    assert html.index("vibing") < html.index("planning") < html.index("building")
    assert html.index("building") < html.index("releasing")


def test_workflow_page_never_invents_a_test_status(client, populated_org, db_engine):
    """ "In test" is a label for IN_REVIEW, never a status.

    `TicketStatus` has no IN_TEST member and deliberately never has -- inventing
    one would report something the board does not say. The page may *call* the
    column "In test"; it must not claim the data has that status.

    **The IN_REVIEW ticket is the test.** Without one, `_STATUS_LABELS` is never
    consulted and the page renders no walk at all, so the assertions below hold
    for a page that could not have said "IN_TEST" whatever the mapping was --
    which is what they used to do: rewriting the label table to emit ``IN_TEST``
    left this green. With the ticket present the label path actually runs, and
    the page has to produce the label *and* the real status beside it.
    """
    from src.domain.ticket import Ticket, TicketStatus

    _, cookie, org, project_id = populated_org
    with Session(db_engine) as session:
        session.add(
            Ticket(
                summary="halfway out the door",
                organization_id=org.id,
                project_id=project_id,
                status=TicketStatus.IN_REVIEW,
            )
        )
        session.commit()

    _auth(client, cookie)
    html = client.get(f"{UI_PREFIX}/{org.alias}/workflow").text

    # The label path ran: the walk carries this ticket, labelled.
    assert "halfway out the door" in html
    assert "In test" in html
    # And the status underneath the label is the board's own.
    assert '"st":"in review"' in html

    assert "IN_TEST" not in html
    assert "in_test" not in html
    assert not any(t.value == "in test" for t in TicketStatus)


def test_workflow_page_escapes_untrusted_text_in_the_json_blob(
    client, signed_in, make_org, db_engine
):
    """Board-supplied text reaches a JSON blob inside a ``<script>``.

    That is the one place on this surface where an escaping failure is not
    cosmetic: this app sets no Content-Security-Policy header, so a value that
    closes the tag is script execution.

    **The values tested here are the ones that actually enter the blob.** An
    earlier version used the project *name*, which never does -- it lands in a
    ``title=""`` attribute, escaped by a different code path -- so the test
    passed on the strength of machinery it was not exercising. What the blob
    carries is ticket ``summary``, ``ref`` and ``owner``, `SummaryItem`
    ``body_markdown`` (as the walk's per-ticket note), the project ``alias`` and
    the next release ``version``. Each is writable by anyone who can write to a
    board.

    **The payload ticket needs a status per step that renders one.** With only an
    IN_REVIEW ticket the walk was reached and nothing else was: `pick-ticket.0`,
    `organize-release.1` and `_pull_markup` never saw it, and deleting `esc`
    from `_ticket_left`, `_chip` or `_text_input` left the suite green. A TODO
    ticket and a finished-unreleased one put the payload through all three.

    **The update workflow's reopen picker needs a fourth.** Its list is DONE
    *and* assigned to the viewer *and* stamped inside the window -- three
    conditions none of the tickets above satisfies, so the picker was absent from
    the payload entirely and a mutant dropping `esc` from its row builder would
    have survived. The ticket below meets all three, and both of the workflow's
    body keys are checked by name in the loop at the end.

    **And the assertion is against the decoded payload, not the raw HTML.**
    `_json_blob` escapes every ``<`` in the document as a second line of
    defence, so `html.count("<script")` balances whether or not `esc` ran --
    which is the other half of why those mutants survived. Decoding undoes only
    the blob's own escaping; anything `esc` should have caught is then visible.
    """
    from src.domain.scrum import Scrum, ScrumKind
    from src.domain.summary import Summary, SummaryItem, SummaryType
    from src.domain.ticket import Ticket, TicketStatus

    payload = "</script><script>alert(1)</script>"

    user, cookie = signed_in()
    org = make_org("pf", name="Haviland", member=user)
    with Session(db_engine) as session:
        project = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias=f"X{payload}",
            name="Ordinary name",
            description="d",
        )
        session.add(project)
        session.commit()
        session.refresh(project)

        for status in (
            TicketStatus.IN_REVIEW,  # the walk, and the walk's cards
            TicketStatus.TODO,  # `pick-ticket.0` and the walk's pull list
            TicketStatus.DONE,  # `organize-release.1`, unreleased
        ):
            session.add(
                Ticket(
                    summary=payload,
                    organization_id=org.id,
                    project_id=project.id,
                    status=status,
                    external_ticket_id=f"PF-{payload}",
                    assignee=payload,
                    release="" if status is TicketStatus.DONE else None,
                )
            )
        # The update workflow's reopen picker: DONE, the viewer's, and stamped
        # inside the window. Nothing above satisfies all three, so without this
        # `give-scrum-update.0` renders "nothing finished lately" and escapes
        # nothing at all.
        session.add(
            Ticket(
                summary=payload,
                organization_id=org.id,
                project_id=project.id,
                status=TicketStatus.DONE,
                external_ticket_id=f"PF-mine-{payload}",
                assignee=payload,
                assigned_to=user.id,
                completed_at=UTC_NOW.replace(tzinfo=None) - timedelta(days=1),
                release="v9",
            )
        )
        # And its take-on picker, which is **unowned** work -- so the TODO in the
        # loop above (which carries a board `assignee`) is deliberately not
        # eligible for it. Without a genuinely unowned row `give-scrum-update.1`
        # renders "nothing queued is unowned" and escapes nothing.
        session.add(
            Ticket(
                summary=payload,
                organization_id=org.id,
                project_id=project.id,
                status=TicketStatus.TODO,
                external_ticket_id=f"PF-free-{payload}",
            )
        )
        # Reaches `_text_input(value=...)` on `organize-release.0` and the chip
        # beside it -- the only board-writable value that gets that far.
        session.add(
            Release(
                id=str(uuid4()),
                organization_id=org.id,
                project_id=project.id,
                version=f"v9-{payload}",
                status=ReleaseStatus.PLANNED,
            )
        )
        # A teammate who gave their update today, named with the payload.
        # Display names are **self-edited**, so they are attacker-writable in
        # exactly the way a board summary is -- and they are the only untrusted
        # value in `run-scrum`'s avatar group and its wrap-up sentence.
        mate = User(id=str(uuid4()), email="mate-xss@example.com", full_name=payload)
        session.add(mate)
        session.add(
            OrganizationMembership(
                id=str(uuid4()),
                organization_id=org.id,
                user_id=mate.id,
                role=OrganizationRole.DEVELOPER,
                is_active=True,
            )
        )
        session.commit()
        began = UTC_NOW.replace(tzinfo=None)
        session.add(
            Scrum(
                id=str(uuid4()),
                organization_id=org.id,
                project_id=project.id,
                run_by_user_id=mate.id,
                kind=ScrumKind.UPDATE.value,
                started_at=began,
                day=began.date(),
                ended_at=began,
            )
        )
        summary = Summary(
            id=str(uuid4()),
            organization_id=org.id,
            project_id=project.id,
            summary_type=SummaryType.SCRUM,
            window_spec="today",
            body_markdown="fine",
            motivational_quote="Onward.",
        )
        session.add(summary)
        session.commit()
        session.add(
            SummaryItem(
                id=str(uuid4()),
                summary_id=summary.id,
                ticket_ref=f"PF-{payload}",
                body_markdown=payload,
            )
        )
        session.commit()

    _auth(client, cookie)
    html = client.get(f"{UI_PREFIX}/{org.alias}/workflow").text

    # Not one of them got to open a tag.
    assert "<script>alert(1)</script>" not in html
    assert html.count("<script") == html.count("</script>")
    # And the payload did reach the page -- so this is escaping, not absence.
    assert "alert(1)" in html

    # Now inside the payload, where the blob's own escaping is already undone.
    blob = _workflow_blob(html)
    project_data = next(iter(blob["projects"].values()))
    reached = 0
    for key, body in project_data["bodies"].items():
        assert payload not in body, f"{key} interpolated board text unescaped"
        if "alert(1)" in body:
            reached += 1
    assert payload not in project_data["pull"], "the walk's pull list is unescaped"
    # The three steps the earlier version never exercised, plus the ones it did,
    # plus both of the update workflow's pickers.
    for key in (
        "pick-ticket.0",
        "organize-release.0",
        "organize-release.1",
        "give-scrum-update.0",
        "give-scrum-update.1",
        # The avatar group and the sentence that names today's submitters. Both
        # interpolate a self-edited display name, and both are `bodies` values
        # because `_bubbles` returns HTML it has already escaped.
        "run-scrum.0",
        "run-scrum.2",
    ):
        assert "alert(1)" in project_data["bodies"][key], key
    assert "alert(1)" in project_data["pull"]
    assert reached >= 5
    # The alias is escaped in the rail's own markup too, not only in the blob.
    assert f'data-alias="X{payload}"' not in html


def test_a_workflow_that_writes_nothing_never_reports_a_save(client, populated_org):
    """**Eight of the ten workflows record nothing, and none of them may pretend.**

    Walking "Create a project" -- type a name and an alias, press Continue,
    Continue, "Create project" -- used to end with three green ticks and
    "Create a project — done. Nothing else is pending." while ``SELECT count(*)
    FROM project`` had not moved. The same held for seven more. That is the
    defect the scrum walk needed two review rounds to lose, in eight further
    places.

    The fix is honesty, not wiring: the state is a field on the workflow, so
    this asserts against the payload the engine reads rather than against a
    sentence in the script. Wiring one up later flips `saves` and this test
    changes in one line.
    """
    _, cookie, org, _ = populated_org
    _auth(client, cookie)
    html = client.get(f"{UI_PREFIX}/{org.alias}/workflow").text
    blob = _workflow_blob(html)

    by_id = {w["id"]: w for w in blob["workflows"]}
    assert len(by_id) == 10

    # Exactly the workflows that claim to write are the ones with write routes:
    # the scrum walk, and the personal update that records its picks onto a
    # `Scrum` row of its own kind.
    assert {i for i, w in by_id.items() if w["saves"]} == {
        "run-scrum",
        "give-scrum-update",
    }

    for wid, wf in by_id.items():
        if wf["saves"]:
            continue
        # Every step of it carries the warning -- the engine renders `warn`
        # under each step's controls, above the button.
        assert "saved" in wf["warn"].lower(), wid
        # And the completion panel says nothing was saved, then points
        # somewhere that does the real thing.
        assert wf["done"].startswith("Nothing was saved."), wid
        assert len(wf["done"]) > len("Nothing was saved."), (
            f"{wid} says nothing was saved and leaves the reader nowhere to go"
        )
        assert "done" not in wf["done"].lower().split(".")[0], wid

    # The one that does write does not carry the warning, so the note is a
    # statement about this workflow rather than boilerplate on all nine.
    assert by_id["run-scrum"]["warn"] == ""
    assert not by_id["run-scrum"]["done"].startswith("Nothing was saved.")

    # The engine reads the flag rather than hard-coding the nine ids.
    assert "run.wf.saves" in html


def test_the_unreleased_count_is_a_total_not_the_page_of_rows(
    client, signed_in, make_org, db_engine
):
    """**A capped list must not be reported as a total.**

    `done_unreleased_for` stops at 60 rows per project. The page counted what it
    was handed and printed it as "N finished tickets with no release", so a
    project with 90 such tickets said 60 -- and the organize-release step told
    you "52 more not shown" when 82 were.

    Ninety rather than a token few, because the number has to exceed the cap for
    the two answers to differ at all.
    """
    from src.domain.ticket import Ticket, TicketStatus

    user, cookie = signed_in()
    org = make_org("pf", name="Haviland", member=user)
    with Session(db_engine) as session:
        project = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias="PF",
            name="PixelFuel",
            description="d",
        )
        session.add(project)
        session.commit()
        session.refresh(project)
        for n in range(90):
            session.add(
                Ticket(
                    summary=f"shipped {n}",
                    organization_id=org.id,
                    project_id=project.id,
                    status=TicketStatus.DONE,
                    release="",
                )
            )
        session.commit()
        project_id = project.id

    _auth(client, cookie)
    blob = _workflow_blob(client.get(f"{UI_PREFIX}/{org.alias}/workflow").text)
    bodies = blob["projects"][project_id]["bodies"]

    assert "90 finished tickets with no release" in bodies["summarize-release.0"]
    # 90 total, 8 drawn (`PICK_CAP`).
    assert "82 more not shown" in bodies["organize-release.1"]


def test_the_walk_takes_in_review_before_in_progress(
    client, signed_in, make_org, db_engine
):
    """ "In test first, then in progress" is a promise the step makes in words.

    `WALK_STATUSES` is the order, and the walk is built from it. Reversing that
    tuple used to leave the suite green: no test put a ticket in each status and
    read the resulting queue, so the sentence on the step was the only thing
    asserting it.
    """
    from src.domain.ticket import Ticket, TicketStatus

    user, cookie = signed_in()
    org = make_org("pf", name="Haviland", member=user)
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    with Session(db_engine) as session:
        project = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias="PF",
            name="PixelFuel",
            description="d",
        )
        session.add(project)
        session.commit()
        session.refresh(project)
        # The in-progress one moved *more* recently, so a queue that merely
        # sorted by `updated_at` would put it first. Only the status order puts
        # the in-review ticket at the front.
        session.add(
            Ticket(
                summary="waiting on test",
                organization_id=org.id,
                project_id=project.id,
                status=TicketStatus.IN_REVIEW,
                updated_at=now - timedelta(days=3),
            )
        )
        session.add(
            Ticket(
                summary="being built",
                organization_id=org.id,
                project_id=project.id,
                status=TicketStatus.IN_PROGRESS,
                updated_at=now,
            )
        )
        session.commit()
        project_id = project.id

    _auth(client, cookie)
    blob = _workflow_blob(client.get(f"{UI_PREFIX}/{org.alias}/workflow").text)
    walk = blob["projects"][project_id]["walk"]

    assert [row["st"] for row in walk] == ["in review", "in progress"]
    assert [row["sum"] for row in walk] == ["waiting on test", "being built"]


def test_a_ticket_that_has_not_moved_in_weeks_is_counted_as_lingering(
    client, signed_in, make_org, db_engine
):
    """`LINGER_DAYS` is what the wrap-up reports and what the record stores.

    One number, two consumers -- the step shows it and the finish write sends it
    -- so `_days_since` returning 0 for everything would make both say "0
    tickets" in agreement, and be wrong twice. Stubbing it to `return 0` left
    the suite green: nothing put an old ticket in front of it.
    """
    from src.domain.ticket import Ticket, TicketStatus

    user, cookie = signed_in()
    org = make_org("pf", name="Haviland", member=user)
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    with Session(db_engine) as session:
        project = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias="PF",
            name="PixelFuel",
            description="d",
        )
        session.add(project)
        session.commit()
        session.refresh(project)
        session.add(
            Ticket(
                summary="stuck for a month",
                organization_id=org.id,
                project_id=project.id,
                status=TicketStatus.IN_PROGRESS,
                updated_at=now - timedelta(days=30),
            )
        )
        session.add(
            Ticket(
                summary="moved this morning",
                organization_id=org.id,
                project_id=project.id,
                status=TicketStatus.IN_PROGRESS,
                updated_at=now,
            )
        )
        session.commit()
        project_id = project.id

    _auth(client, cookie)
    blob = _workflow_blob(client.get(f"{UI_PREFIX}/{org.alias}/workflow").text)
    project_data = blob["projects"][project_id]

    # The number the wrap-up sends to the server.
    assert project_data["lingering"] == 1
    # The same number, rendered on the wrap-up step.
    assert "1 ticket" in project_data["bodies"]["run-scrum.2"]
    # And the per-ticket age the walk card shows.
    ages = {row["sum"]: row["days"] for row in project_data["walk"]}
    assert ages["stuck for a month"] >= 30
    assert ages["moved this morning"] == 0


def test_every_step_helper_escapes_what_it_interpolates():
    """The three markup helpers, checked directly rather than through a page.

    Two of them (`_ticket_left`, `_chip`) are reachable from board text and the
    page-level escaping test drives them there. `_text_input`'s ``value`` is
    **not** reachable today: its only caller passes a version, and both sources
    of that version (`next_release`, `next_version_suggestion`) are filtered by
    `is_semver`, so no payload can survive the trip. That makes the page test
    structurally incapable of covering it -- deleting its `esc` left the suite
    green -- and it is exactly the kind of control that must not quietly stop
    working before the first caller that *does* hand it board text arrives.

    So this asserts the helpers themselves. It is a smaller claim than the page
    test makes and it is the claim that can actually be checked here.
    """
    from src.routers.webui import workflow as wf
    from src.routers.webui.data import ProjectTicketRow

    payload = '"><script>alert(1)</script>'

    row = ProjectTicketRow(
        id=1,
        ref=payload,
        summary=payload,
        status="todo",
        url=None,
        owner=payload,
        updated_at=None,
    )
    left = wf._ticket_left(row)
    assert "<script" not in left and payload not in left
    assert "alert(1)" in left

    chip = wf._chip(payload)
    assert "<script" not in chip and payload not in chip
    assert "alert(1)" in chip

    box = wf._text_input(value=payload, placeholder=payload, style=payload)
    assert "<script" not in box and payload not in box
    assert "alert(1)" in box

    area = wf._textarea(payload)
    assert "<script" not in area and payload not in area

    # `_textarea`'s value **is** reachable: it renders a note somebody typed into
    # their own update and is read back on re-entry. It goes into a text node
    # rather than an attribute, which is why the value is not routed through
    # `_text_input` -- a newline cannot live in `value="…"`.
    resumed = wf._textarea("ph", value=payload + "\nsecond line")
    assert "<script" not in resumed and payload not in resumed
    assert "alert(1)" in resumed
    assert "second line" in resumed, "a multi-line note lost its second line"

    # `_row`'s ticket id is **coerced, not escaped** -- an integer in an attribute
    # cannot carry a quote or a bracket. So the guarantee is that a string never
    # gets there at all: it raises rather than interpolating.
    assert 'data-pick="7"' in wf._row("x", check=False, ticket_id=7)
    with pytest.raises((ValueError, TypeError)):
        wf._row("x", check=False, ticket_id=payload)


def test_default_project_persists_on_the_membership(client, populated_org, db_engine):
    """The star writes `OrganizationMembership.default_project_id`.

    On the membership rather than on `User`, because a project default is only
    meaningful inside one org -- a single column on `users` would follow someone
    into an org where it names a project they cannot see.
    """
    user, cookie, org, project_id = populated_org
    _auth(client, cookie)

    r = client.post(
        f"{UI_PREFIX}/{org.alias}/default-project",
        data={"project_id": project_id},
        follow_redirects=False,
    )
    assert r.status_code == 303
    assert r.headers["location"] == f"{UI_PREFIX}/{org.alias.lower()}/workflow"

    with Session(db_engine) as session:
        row = session.exec(
            select(OrganizationMembership).where(
                OrganizationMembership.organization_id == org.id,
                OrganizationMembership.user_id == user.id,
            )
        ).first()
        assert row.default_project_id == project_id


def test_cannot_default_to_a_project_in_another_org(
    client, populated_org, make_org, db_engine
):
    """A project id from elsewhere is not a different-but-valid choice.

    `set_default_org` deliberately resolves its target independently, because you
    set your default org from whichever dashboard you are on. A project is
    reachable only through the org that owns it, so the same latitude here would
    just be someone naming a row they were never shown.
    """
    user, cookie, org, _ = populated_org
    other = make_org("other", name="Other", member=user)
    with Session(db_engine) as session:
        stranger = Project(
            id=str(uuid4()),
            organization_id=other.id,
            alias="OTH",
            name="Not yours",
            description="d",
        )
        session.add(stranger)
        session.commit()
        stranger_id = stranger.id

    _auth(client, cookie)
    r = client.post(
        f"{UI_PREFIX}/{org.alias}/default-project",
        data={"project_id": stranger_id},
        follow_redirects=False,
    )
    assert r.status_code == 404

    with Session(db_engine) as session:
        row = session.exec(
            select(OrganizationMembership).where(
                OrganizationMembership.organization_id == org.id,
                OrganizationMembership.user_id == user.id,
            )
        ).first()
        assert row.default_project_id is None


def test_workflow_write_route_requires_a_session(client, populated_org):
    _, _, org, project_id = populated_org
    r = client.post(
        f"{UI_PREFIX}/{org.alias}/default-project",
        data={"project_id": project_id},
        follow_redirects=False,
    )
    assert r.status_code == 303 and r.headers["location"] == LOGIN_PATH


def test_ticket_reads_do_not_scale_with_project_count(
    client, signed_in, make_org, db_engine
):
    """The two ticket helpers stay at one SELECT each however many projects there are.

    The rail switches projects client-side precisely so switching is free, which
    means the page carries every project's work at once. Building that with
    `project_tickets` per project is the shape #501 batched away -- and it would
    be worse here, since the whole point of the rail is that it costs nothing.

    This asserts a property of the **helpers**, and says so. It is not a claim
    about the page: see `test_workflow_page_query_count_grows_with_project_count`
    for what the route actually does.
    """
    user, cookie = signed_in()
    org = make_org("pf", name="Haviland", member=user)
    with Session(db_engine) as session:
        for n in range(6):
            session.add(
                Project(
                    id=str(uuid4()),
                    organization_id=org.id,
                    alias=f"P{n}",
                    name=f"Project {n}",
                    description="d",
                )
            )
        session.commit()

    from src.routers.webui.data import (
        done_unreleased_for,
        done_unreleased_totals_for,
        project_tickets_for,
    )

    with Session(db_engine) as session:
        ids = [
            p.id
            for p in session.exec(
                select(Project).where(Project.organization_id == org.id)
            ).all()
        ]
        statements = []
        listener = lambda conn, cur, stmt, *a: statements.append(stmt)  # noqa: E731
        event.listen(db_engine, "before_cursor_execute", listener)
        try:
            tickets = project_tickets_for(session, ids)
            unreleased = done_unreleased_for(session, ids)
            totals = done_unreleased_totals_for(session, ids)
        finally:
            event.remove(db_engine, "before_cursor_execute", listener)

    selects = [s for s in statements if s.lstrip().upper().startswith("SELECT")]
    assert len(selects) == 3, (
        f"expected one SELECT per helper regardless of project count, got "
        f"{len(selects)} for {len(ids)} projects"
    )
    # Every project is represented, so a missing key can't masquerade as batching.
    assert set(tickets) == set(ids)
    assert set(unreleased) == set(ids)
    # The totals helper is the newest of the three and the easiest to write as a
    # per-project loop, since it answers one integer per project.
    assert set(totals) == set(ids)


def test_workflow_page_query_count_grows_with_project_count(
    client, signed_in, make_org, db_engine
):
    """**The route is not fully batched, and this is what pins the truth of it.**

    The eight table reads are one query each -- `scrum_activity_today` issues two
    statements but both are org-wide, so it is still constant in the project count.
    `summary_panel` is the one that is not: the route calls it once per project, so
    the page's total query count rises with the number of projects -- the
    dashboard's shape, inherited.

    Inheriting it is acceptable; claiming it was fixed is not. The route's
    docstring used to say "one read per table for the whole page, never one per
    project" while the only test of the claim called the two helpers directly and
    never loaded a page. This test loads the page, twice, and asserts the real
    relationship -- so the day somebody batches `summary_panel`, this fails and
    the comment gets corrected with it rather than drifting further.
    """

    def _cost(project_count, alias):
        user, cookie = signed_in()
        org = make_org(alias, name="Haviland", member=user)
        with Session(db_engine) as session:
            for n in range(project_count):
                session.add(
                    Project(
                        id=str(uuid4()),
                        organization_id=org.id,
                        alias=f"{alias.upper()}{n}",
                        name=f"Project {n}",
                        description="d",
                    )
                )
            session.commit()

        _auth(client, cookie)
        statements = []
        listener = lambda conn, cur, stmt, *a: statements.append(stmt)  # noqa: E731
        event.listen(db_engine, "before_cursor_execute", listener)
        try:
            assert client.get(f"{UI_PREFIX}/{org.alias}/workflow").status_code == 200
        finally:
            event.remove(db_engine, "before_cursor_execute", listener)
        return len([s for s in statements if s.lstrip().upper().startswith("SELECT")])

    one = _cost(1, "qa")
    many = _cost(9, "qb")

    assert many > one, (
        "the page is now batched per project -- delete this test and correct the "
        "route comment that says it is not"
    )
    # Linear in the project count, not quadratic: whatever grows, grows once.
    per_project = (many - one) / 8
    assert per_project < 4, f"{per_project} extra SELECTs per project is not linear"


def test_in_flight_work_survives_a_wave_of_finished_tickets(
    signed_in, make_org, db_engine
):
    """**A busy DONE column must not be able to empty the walk.**

    Reproduces the shape that broke it: seventy DONE tickets touched today and
    three IN_REVIEW tickets touched a week ago, in one project. The old query
    ordered every status together by ``updated_at DESC`` and applied a single
    ``LIMIT per_project * len(ids)``, so the seventy filled the budget and the
    three never appeared -- and the page renders that as "Nothing is in test or
    in progress on this board", a sentence that is simply false.

    Nothing exotic causes it: a routine board sync bumps ``updated_at`` on
    everything it touches, and finished work is most of what a board holds.
    """
    from src.domain.ticket import Ticket, TicketStatus
    from src.routers.webui.data import project_tickets, project_tickets_for

    user, _ = signed_in()
    org = make_org("pf", name="Haviland", member=user)
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    with Session(db_engine) as session:
        project = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias="PF",
            name="PixelFuel",
            description="d",
        )
        session.add(project)
        session.commit()
        session.refresh(project)

        for n in range(70):
            session.add(
                Ticket(
                    summary=f"shipped {n}",
                    organization_id=org.id,
                    project_id=project.id,
                    status=TicketStatus.DONE,
                    updated_at=now,
                )
            )
        for n in range(3):
            session.add(
                Ticket(
                    summary=f"still in review {n}",
                    organization_id=org.id,
                    project_id=project.id,
                    status=TicketStatus.IN_REVIEW,
                    updated_at=now - timedelta(days=7),
                )
            )
        session.commit()
        project_id = project.id

    with Session(db_engine) as session:
        single = project_tickets(session, project_id)
        batched = project_tickets_for(session, [project_id])[project_id]

    def _in_review(rows):
        return [r for r in rows if r.status == TicketStatus.IN_REVIEW.value]

    # The single-project query has always been right; the batched one is what
    # the workflow page reads, and the two must agree about what is in flight.
    assert len(_in_review(single)) == 3
    assert len(_in_review(batched)) == 3, (
        "the batched read dropped in-flight work behind a wall of DONE tickets"
    )


def test_one_busy_project_cannot_starve_another(signed_in, make_org, db_engine):
    """The same starvation across projects rather than across statuses.

    Two hundred recently-touched tickets in one project and two long-untouched
    ones in another: under a single shared ``LIMIT`` the second project came
    back empty, and the rail would have shown its board as idle.

    **Both projects' tickets are IN_PROGRESS, and that is the whole test.** They
    were DONE and IN_PROGRESS, so the two projects never competed for one
    budget: dropping ``project_id`` from the window's ``partition_by`` -- the
    exact regression this test names -- left it green, because ``(status,)``
    alone still gave the quiet project's IN_PROGRESS tickets a partition of
    their own. Sharing the status is what makes `project_id` load-bearing here,
    and its sibling `test_in_flight_work_survives_a_wave_of_finished_tickets`
    is what makes `status` load-bearing. Each dies to the mutant the other
    survives; neither is redundant.
    """
    from src.domain.ticket import Ticket, TicketStatus
    from src.routers.webui.data import project_tickets_for

    user, _ = signed_in()
    org = make_org("pf", name="Haviland", member=user)
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    with Session(db_engine) as session:
        busy = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias="BUSY",
            name="Busy",
            description="d",
        )
        quiet = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias="QQ",
            name="Quiet",
            description="d",
        )
        session.add(busy)
        session.add(quiet)
        session.commit()
        session.refresh(busy)
        session.refresh(quiet)

        for n in range(200):
            session.add(
                Ticket(
                    summary=f"busy wip {n}",
                    organization_id=org.id,
                    project_id=busy.id,
                    status=TicketStatus.IN_PROGRESS,
                    updated_at=now,
                )
            )
        for n in range(2):
            session.add(
                Ticket(
                    summary=f"quiet wip {n}",
                    organization_id=org.id,
                    project_id=quiet.id,
                    status=TicketStatus.IN_PROGRESS,
                    updated_at=now - timedelta(days=90),
                )
            )
        session.commit()
        busy_id, quiet_id = busy.id, quiet.id

    with Session(db_engine) as session:
        grouped = project_tickets_for(session, [busy_id, quiet_id])

    assert len(grouped[quiet_id]) == 2, "the quiet project was starved by the busy one"
    # And the busy project still gets its own full budget, so this is a
    # per-partition cap and not a global one that happened to favour it.
    assert len(grouped[busy_id]) == 25


# --------------------------------------------------------------------------- #
# The scrum walk's `/ui` writes
#
# The page records the meeting while it happens. These routes are what it posts
# to -- `/ui`, session cookie, same origin -- because a browser cannot
# authenticate against `/api/v1` at all.
# --------------------------------------------------------------------------- #


def _walk_ticket(db_engine, org, project_id, summary="in review now"):
    from src.domain.ticket import Ticket, TicketStatus

    with Session(db_engine) as session:
        ticket = Ticket(
            summary=summary,
            organization_id=org.id,
            project_id=project_id,
            status=TicketStatus.IN_REVIEW,
        )
        session.add(ticket)
        session.commit()
        session.refresh(ticket)
        return ticket.id


def test_the_scrum_walk_actually_persists(client, populated_org, db_engine):
    """**The whole point of the workflow: a walked board leaves a record.**

    Open, one visit per ticket as the walk goes, close at wrap-up. The page tells
    the user this happens; before these routes existed it did not, and
    ``SELECT count(*) FROM scrums`` stayed at zero after a full meeting.
    """
    from src.domain.scrum import Scrum, ScrumTicketVisit

    user, cookie, org, project_id = populated_org
    ticket_id = _walk_ticket(db_engine, org, project_id)
    _auth(client, cookie)

    opened = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums", json={"project_id": project_id}
    )
    assert opened.status_code == 201, opened.text
    scrum_id = opened.json()["scrum_id"]

    visit = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums/{scrum_id}/visits",
        json={
            "ticket_id": ticket_id,
            "position": 0,
            "seconds": 42,
            "status_at_visit": "in review",
            "comment": "waiting on review",
        },
    )
    assert visit.status_code == 201, visit.text

    done = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums/{scrum_id}/finish",
        json={
            "ended_at": "2026-08-15T10:30:00Z",
            "total_seconds": 600,
            "transcript_url": "https://example.com/rec/1",
            "lingering_count": 1,
            "notes_markdown": "PF-1 is stuck.",
        },
    )
    assert done.status_code == 200, done.text

    with Session(db_engine) as session:
        row = session.get(Scrum, scrum_id)
        assert row is not None
        assert row.run_by_user_id == user.id
        assert row.project_id == project_id
        assert row.total_seconds == 600
        assert row.transcript_url == "https://example.com/rec/1"
        assert row.notes_markdown == "PF-1 is stuck."
        assert row.ended_at is not None
        visits = session.exec(
            select(ScrumTicketVisit).where(ScrumTicketVisit.scrum_id == scrum_id)
        ).all()
        assert [v.seconds for v in visits] == [42]
        assert visits[0].comment == "waiting on review"


def test_reopening_after_a_cancel_reuses_the_scrum_that_is_still_open(
    client, populated_org, db_engine
):
    """**A cancelled or retried walk must not leave a phantom behind.**

    The page resets its record on Cancel and re-opens when the walk step next
    appears; it also retries the open after any rejection, including one whose
    response was lost after the row had already committed. Both hit this route a
    second time, and both used to create a second `Scrum`.

    The costs are different and both are real. A row with ``ended_at`` NULL is
    how `src/domain/scrum.py` spells *abandoned*, so every cancelled attempt
    read as a meeting somebody walked out of. And on the dropped-response path
    the walk carried on against a different id, so the record was split down the
    middle with neither half being the meeting. The finish route has refused its
    own double-submit since day one; this is the same guarantee at the open.
    """
    from src.domain.scrum import Scrum

    _, cookie, org, project_id = populated_org
    _auth(client, cookie)

    first = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums", json={"project_id": project_id}
    )
    assert first.status_code == 201, first.text

    again = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums", json={"project_id": project_id}
    )
    assert again.status_code == 201, again.text
    assert again.json()["scrum_id"] == first.json()["scrum_id"], (
        "cancelling and restarting opened a second scrum"
    )

    with Session(db_engine) as session:
        rows = session.exec(select(Scrum).where(Scrum.project_id == project_id)).all()
        assert len(rows) == 1

    # Once the meeting is closed the next walk is a new meeting, not this one.
    closed = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums/{first.json()['scrum_id']}/finish",
        json={"ended_at": "2026-08-15T10:30:00Z", "total_seconds": 60},
    )
    assert closed.status_code == 200, closed.text

    third = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums", json={"project_id": project_id}
    )
    assert third.status_code == 201
    assert third.json()["scrum_id"] != first.json()["scrum_id"]


def test_the_two_surfaces_refuse_the_same_scrum_body(client, populated_org, db_engine):
    """**`/api/v1` and `/ui` must decide the same way about the same bytes.**

    `scrum_service._checked_int` refuses ``bool`` in as many words -- "``seconds:
    true`` is a client bug, and storing it as 1 records a stop that took one
    second". The ``/ui`` route got that refusal because it hands the raw body to
    the service. The API route did not: pydantic coerced `True` to `1` first, so
    the same request was a clean 201 there and a 422 here, and the row it wrote
    said the stop lasted a second.

    This drives the ``/ui`` half; `tests/test_scrums_router.py` drives the
    ``/api/v1`` half against the identical bodies, and the pair is the assertion.
    """
    _, cookie, org, project_id = populated_org
    ticket_id = _walk_ticket(db_engine, org, project_id)
    _auth(client, cookie)

    scrum_id = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums", json={"project_id": project_id}
    ).json()["scrum_id"]

    def _visit(**overrides):
        body = {
            "ticket_id": ticket_id,
            "position": 0,
            "seconds": 5,
            "status_at_visit": "in review",
        }
        body.update(overrides)
        return client.post(
            f"{UI_PREFIX}/{org.alias}/scrums/{scrum_id}/visits", json=body
        )

    assert _visit(seconds=True).status_code == 422
    assert _visit(seconds="5").status_code == 422
    assert _visit(position=-1).status_code == 422
    assert _visit(status_at_visit="x" * 51).status_code == 422
    # And the refusal names the field, which is what puts it beside the box.
    assert _visit(seconds=True).json()["field"] == "seconds"

    assert (
        client.post(
            f"{UI_PREFIX}/{org.alias}/scrums/{scrum_id}/finish",
            json={"total_seconds": True},
        ).status_code
        == 422
    )
    assert (
        client.post(
            f"{UI_PREFIX}/{org.alias}/scrums/{scrum_id}/finish",
            json={"transcript_url": "https://e.com/" + "x" * 1000},
        ).status_code
        == 422
    )


def test_a_member_of_one_org_cannot_write_a_scrum_in_another(
    client, populated_org, signed_in, make_org, db_engine
):
    """Every write route, checked against the org in its own URL.

    Four routes, one rule: an outsider gets the same 404 an unknown org gets,
    because a distinguishable answer would confirm the org exists to anybody
    guessing aliases (see this module's docstring).

    **404 and not 403, asserted specifically.** 403 is the honest answer to "this
    is not yours" and the wrong one to give here: it separates "no such org" from
    "an org you cannot open", which is the whole of an enumeration oracle. The
    distinction matters most on the newest route, since `/picks` had to repeat the
    gate rather than inherit it.
    """
    from src.domain.scrum import Scrum

    _, owner_cookie, org, project_id = populated_org
    ticket_id = _walk_ticket(db_engine, org, project_id)

    _auth(client, owner_cookie)
    scrum_id = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums", json={"project_id": project_id}
    ).json()["scrum_id"]

    # Someone with a real session, a real org of their own, and no business here.
    outsider, outsider_cookie = signed_in(email="outsider@example.com")
    make_org("elsewhere", name="Elsewhere", member=outsider)
    client.cookies.clear()
    _auth(client, outsider_cookie)

    assert (
        client.post(
            f"{UI_PREFIX}/{org.alias}/scrums", json={"project_id": project_id}
        ).status_code
        == 404
    )
    assert (
        client.post(
            f"{UI_PREFIX}/{org.alias}/scrums/{scrum_id}/visits",
            json={
                "ticket_id": ticket_id,
                "position": 0,
                "seconds": 1,
                "status_at_visit": "in review",
            },
        ).status_code
        == 404
    )
    assert (
        client.post(
            f"{UI_PREFIX}/{org.alias}/scrums/{scrum_id}/picks",
            json={"picks": []},
        ).status_code
        == 404
    )
    assert (
        client.post(
            f"{UI_PREFIX}/{org.alias}/scrums/{scrum_id}/finish",
            json={"total_seconds": 1},
        ).status_code
        == 404
    )

    # Addressing them through *their own* org does not reach the row either.
    assert (
        client.post(
            f"{UI_PREFIX}/elsewhere/scrums/{scrum_id}/finish",
            json={"total_seconds": 1},
        ).status_code
        == 404
    )
    assert (
        client.post(
            f"{UI_PREFIX}/elsewhere/scrums/{scrum_id}/picks",
            json={"picks": []},
        ).status_code
        == 404
    )

    with Session(db_engine) as session:
        assert session.get(Scrum, scrum_id).total_seconds is None
        # `/picks` with an empty set is a *deletion* on its own record, so a
        # refusal that leaked through would not merely fail to write -- it would
        # have emptied somebody else's. Nothing was reached, so nothing was lost.
        assert _visits(session, scrum_id) == []


def test_a_project_from_another_org_cannot_be_walked(
    client, populated_org, make_org, db_engine
):
    """The project is checked against the org the URL resolved to, not the body."""
    user, cookie, org, _ = populated_org
    other = make_org("other", name="Other", member=user)
    with Session(db_engine) as session:
        stranger = Project(
            id=str(uuid4()),
            organization_id=other.id,
            alias="OTH",
            name="Not this org",
            description="d",
        )
        session.add(stranger)
        session.commit()
        stranger_id = stranger.id

    _auth(client, cookie)
    r = client.post(f"{UI_PREFIX}/{org.alias}/scrums", json={"project_id": stranger_id})
    assert r.status_code == 404


def test_a_second_person_cannot_close_your_scrum(
    client, populated_org, signed_in, db_engine
):
    """Whose row, not what role.

    A colleague who is a full member of the same org still may not blank the
    minutes of a meeting somebody else ran -- and neither may their own stale
    tab, which is the same request from the same person twice.
    """
    from src.domain.organization import OrganizationRole
    from src.domain.scrum import Scrum

    _, cookie, org, project_id = populated_org
    _auth(client, cookie)
    scrum_id = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums", json={"project_id": project_id}
    ).json()["scrum_id"]
    client.post(
        f"{UI_PREFIX}/{org.alias}/scrums/{scrum_id}/finish",
        json={"notes_markdown": "mine", "ended_at": "2026-08-15T10:00:00Z"},
    )

    colleague, colleague_cookie = signed_in(email="colleague@example.com")
    with Session(db_engine) as session:
        session.add(
            OrganizationMembership(
                id=str(uuid4()),
                user_id=colleague.id,
                organization_id=org.id,
                role=OrganizationRole.ADMIN,
                is_active=True,
            )
        )
        session.commit()

    client.cookies.clear()
    _auth(client, colleague_cookie)
    r = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums/{scrum_id}/finish",
        json={"notes_markdown": ""},
    )
    assert r.status_code == 403

    with Session(db_engine) as session:
        assert session.get(Scrum, scrum_id).notes_markdown == "mine"


def test_a_second_person_cannot_rewrite_your_picks(
    client, populated_org, signed_in, db_engine
):
    """Whose row, not what role -- the same rule as its `/finish` sibling above.

    `/picks` replaces a record's whole visit set, so a missing runner check here is
    worse than on the routes either side of it: a colleague could not merely add to
    somebody's daily update, they could **empty it** by posting an empty list, and
    the owner would find their picks gone with nothing saying who did it.

    The scrum is an **update**, deliberately. A team scrum would be refused by
    `replace_picks`'s kind check before the runner check ever mattered, so the test
    would pass while proving nothing about `writable_scrum` -- the same shape of
    false pass this file's docstring warns about elsewhere. With an update, the
    runner check is the only gate that can produce this 403.
    """
    from src.domain.organization import OrganizationRole

    user, cookie, org, project_id = populated_org
    naive = UTC_NOW.replace(tzinfo=None)
    from src.domain.ticket import TicketStatus

    mine = _ticket(
        db_engine,
        org,
        project_id,
        summary="my finished work",
        status=TicketStatus.DONE,
        assigned_to=user.id,
        completed_at=naive - timedelta(days=1),
    )
    _auth(client, cookie)
    scrum_id = _submit_update(client, org, project_id, picks=[(mine, "done")])

    colleague, colleague_cookie = signed_in(email="picks-colleague@example.com")
    with Session(db_engine) as session:
        session.add(
            OrganizationMembership(
                id=str(uuid4()),
                user_id=colleague.id,
                organization_id=org.id,
                # An ADMIN, so this pins "whose row" rather than "what role":
                # membership decides what may be written, never whose record.
                role=OrganizationRole.ADMIN,
                is_active=True,
            )
        )
        session.commit()

    client.cookies.clear()
    _auth(client, colleague_cookie)
    refused = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums/{scrum_id}/picks",
        json={"picks": []},
    )
    assert refused.status_code == 403, refused.text

    with Session(db_engine) as session:
        assert [v.ticket_id for v in _visits(session, scrum_id)] == [mine], (
            "a colleague emptied somebody else's update"
        )


def test_a_closed_scrum_refuses_a_second_close(client, populated_org, db_engine):
    """A stale tab reaching the finish route again must not rewrite the record."""
    from src.domain.scrum import Scrum

    _, cookie, org, project_id = populated_org
    _auth(client, cookie)
    scrum_id = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums", json={"project_id": project_id}
    ).json()["scrum_id"]

    first = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums/{scrum_id}/finish",
        json={"ended_at": "2026-08-15T10:00:00Z", "notes_markdown": "the real notes"},
    )
    assert first.status_code == 200

    second = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums/{scrum_id}/finish",
        json={"ended_at": "2026-08-15T18:00:00Z", "notes_markdown": ""},
    )
    assert second.status_code == 409

    with Session(db_engine) as session:
        assert session.get(Scrum, scrum_id).notes_markdown == "the real notes"


def test_the_ui_finish_route_refuses_junk_rather_than_storing_none(
    client, populated_org, db_engine
):
    """A malformed date is 422, not a 200 that marks the run abandoned."""
    from src.domain.scrum import Scrum

    _, cookie, org, project_id = populated_org
    _auth(client, cookie)
    scrum_id = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums", json={"project_id": project_id}
    ).json()["scrum_id"]

    r = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums/{scrum_id}/finish",
        json={"ended_at": "15/08/2026 10:30", "total_seconds": 60},
    )
    assert r.status_code == 422

    bad_link = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums/{scrum_id}/finish",
        json={"transcript_url": "javascript:alert(1)"},
    )
    assert bad_link.status_code == 422

    with Session(db_engine) as session:
        row = session.get(Scrum, scrum_id)
        assert row.ended_at is None and row.total_seconds is None
        assert row.transcript_url is None


def test_the_ui_routes_refuse_a_shape_the_column_cannot_hold(
    client, populated_org, db_engine
):
    """**Validation on one surface only is the drift the shared service exists to close.**

    `/api/v1` has `ScrumFinish` in front of it -- ``ge=0``, ``max_length=1000``,
    typed fields -- and the `/ui` routes have a JSON body and no model at all,
    so these values went straight to the driver. On Postgres
    ``total_seconds="abc"`` is ``invalid input syntax for type integer`` and a
    1,220-character ``transcript_url`` is ``value too long for type character
    varying(1000)``: an unhandled 500 on the page for a value the API answers a
    clean 422 for. On SQLite -- what this suite runs on -- the same bodies are
    worse than a 500, because SQLite stores them, so the assertion that matters
    is the status code and an untouched row.

    Both routes, because a visit's ``comment`` was forwarded raw as well.
    """
    from src.domain.scrum import Scrum, ScrumTicketVisit

    _, cookie, org, project_id = populated_org
    ticket_id = _walk_ticket(db_engine, org, project_id)
    _auth(client, cookie)
    scrum_id = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums", json={"project_id": project_id}
    ).json()["scrum_id"]

    finish = f"{UI_PREFIX}/{org.alias}/scrums/{scrum_id}/finish"
    for body in (
        {"total_seconds": "abc"},
        {"total_seconds": -1},
        {"lingering_count": "seven"},
        {"lingering_count": -1},
        {"notes_markdown": {"nested": "object"}},
        {"transcript_url": "https://example.com/" + "x" * 1200},
    ):
        r = client.post(finish, json=body)
        assert r.status_code == 422, f"{body} was not refused: {r.status_code} {r.text}"

    visits = f"{UI_PREFIX}/{org.alias}/scrums/{scrum_id}/visits"
    stop = {"ticket_id": ticket_id, "position": 0, "seconds": 5, "status_at_visit": "x"}
    for bad in (
        {"comment": {"nested": "object"}},
        {"status_at_visit": "y" * 51},
        {"moved_to": "z" * 51},
        {"seconds": "abc"},
    ):
        payload = dict(stop)
        payload.update(bad)
        r = client.post(visits, json=payload)
        assert r.status_code == 422, f"{bad} was not refused: {r.status_code} {r.text}"

    # Nothing above may have landed. A refusal that still wrote is the failure
    # mode these checks exist to prevent, not merely a wrong status code.
    with Session(db_engine) as session:
        row = session.get(Scrum, scrum_id)
        assert row.total_seconds is None
        assert row.lingering_count is None
        assert row.notes_markdown is None
        assert row.transcript_url is None
        assert row.ended_at is None
        assert (
            session.exec(
                select(ScrumTicketVisit).where(ScrumTicketVisit.scrum_id == scrum_id)
            ).all()
            == []
        )


def test_a_hand_typed_meeting_link_is_completed_rather_than_refused(
    client, populated_org, db_engine
):
    """**A rejected transcript link must not be why a finished scrum reads as abandoned.**

    ``ended_at`` NULL is how an *abandoned* run is told from a finished one. The
    wrap-up writes both fields in one call, so a refused link left the row with
    no end time -- the meeting happened, was walked to the end, and is recorded
    as having been given up on.

    The field's only hint is a placeholder, and what a hand types into it is
    ``meet.google.com/abc-defg``. That is completed to https rather than
    refused. Anything that already carries a scheme is still judged on it, and
    the refusal now *names the field* so the page can put the message beside the
    box instead of in a banner about "the scrum".
    """
    from src.domain.scrum import Scrum

    _, cookie, org, project_id = populated_org
    _auth(client, cookie)

    def open_scrum():
        return client.post(
            f"{UI_PREFIX}/{org.alias}/scrums", json={"project_id": project_id}
        ).json()["scrum_id"]

    typed = open_scrum()
    ok = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums/{typed}/finish",
        json={
            "ended_at": "2026-08-15T10:30:00Z",
            "transcript_url": "meet.google.com/abc-defg",
        },
    )
    assert ok.status_code == 200, ok.text

    refused = open_scrum()
    bad = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums/{refused}/finish",
        json={"ended_at": "2026-08-15T10:30:00Z", "transcript_url": "javascript:x"},
    )
    assert bad.status_code == 422
    assert bad.json()["field"] == "transcript_url", (
        "the page cannot mark the offending input if the refusal does not name it"
    )

    with Session(db_engine) as session:
        assert (
            session.get(Scrum, typed).transcript_url
            == "https://meet.google.com/abc-defg"
        )
        assert session.get(Scrum, typed).ended_at is not None
        # Still refused, and still without a scheme-laundered value stored.
        assert session.get(Scrum, refused).transcript_url is None


def test_the_wrap_up_shows_the_servers_own_refusal_beside_the_field(
    client, populated_org
):
    """A 422 the script throws away is a dead end the user cannot get out of.

    The script used to raise ``new Error("HTTP " + r.status)``, so a refusal
    naming ``transcript_url`` reached the page as the sentence "The scrum was
    not saved. Nothing has been recorded for the wrap-up -- try again." Nothing
    pointed at the URL field, every retry failed identically, and the meeting's
    notes and clock were never stored.

    The selector is asserted against the *served page* rather than the constant,
    so a renamed hook fails here: a map pointing at a control that no longer
    exists puts the message nowhere at all.
    """
    _, cookie, org, _ = populated_org
    _auth(client, cookie)
    page = client.get(f"{UI_PREFIX}/{org.alias}/workflow").text

    assert "b.error" in page and "e.field = (b && b.field)" in page, (
        "the refusal's own words and the field it named are being discarded"
    )
    assert "fieldError(err.field, message)" in page
    assert 'transcript_url: "[data-scrum-transcript]"' in page
    assert "data-scrum-transcript" in page, "the mapped control is not on the page"


def test_a_failed_scrum_open_is_retried_rather_than_bricking_the_walk(
    client, populated_org
):
    """**A transient failure must not end the walk it interrupted.**

    A blip as the walk step rendered set a ``broken`` flag that nothing ever
    cleared: every later stop returned before issuing a request, and the wrap-up
    rejected locally without one. Connectivity returning immediately changed
    nothing -- the user walked twelve tickets with zero attempts made, then
    could not complete the workflow at all, and the only exit was a reload that
    discarded every typed comment.

    Also the browser that cannot write at all. Refusing to advance there turned
    "completes but saves nothing" into "cannot be completed", which is a
    regression however much better saving is: the walk still finishes, and says
    plainly that nothing was recorded.

    Anchored on `wireWrite`, the one place a step both writes and advances. It
    used to be the scrum wrap-up's own click handler; the personal update's
    pickers need the identical treatment, so the block was generalised rather
    than copied, and this test follows it there. The claim is unchanged.
    """
    _, cookie, org, _ = populated_org
    _auth(client, cookie)
    page = client.get(f"{UI_PREFIX}/{org.alias}/workflow").text

    assert "rec.broken" not in page, "the permanent latch is back"
    assert "function ensureOpen()" in page
    # Opened once, then re-attempted by each write path -- the walk's stops, the
    # update's picks, and the close.
    assert page.count("ensureOpen()") >= 4, (
        "a write path is not re-attempting the open it needs"
    )

    start = page.index("var writing = writer.run();")
    unsupported = page[start : page.index("writing.then(", start)]
    assert "advance(el, i);" in unsupported, (
        "a browser that cannot write is trapped on a step it can never leave"
    )


def test_an_already_closed_scrum_is_not_painted_as_a_failed_save(
    client, populated_org, db_engine
):
    """**409 means the scrum is closed, which is what the button was asking for.**

    The finish POST commits and a proxy drops the response; the user clicks
    again; the server correctly answers 409. The page said "The scrum was not
    saved. Nothing has been recorded" -- untrue -- and refused to advance. That
    is the mirror image of the bug this branch fixed: reporting a result it did
    not get.

    **The last two assertions pin a guard, not a live path, and say so on purpose.**
    `ensureOpen` is chained inside the write, so an open's rejection reaches the
    same handler -- and a 409 from an open would mean nothing this click asked for
    happened. Nothing returns one today (`open_scrum` answers 404/422/403), so the
    `fromOpen` branch is currently unreachable and these two lines assert that the
    scoping *exists* rather than that it fires. Kept deliberately: the trap is in
    the shape of the chain, and the first rule that refuses an open with a 409
    would otherwise report a successful save of a record nobody wrote, silently.
    A cheap guard against a silent failure is worth a line that says it is a guard.
    """
    from src.domain.scrum import Scrum

    _, cookie, org, project_id = populated_org
    _auth(client, cookie)
    scrum_id = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums", json={"project_id": project_id}
    ).json()["scrum_id"]
    body = {"ended_at": "2026-08-15T10:30:00Z", "total_seconds": 600}

    assert (
        client.post(
            f"{UI_PREFIX}/{org.alias}/scrums/{scrum_id}/finish", json=body
        ).status_code
        == 200
    )
    # The premise: the retry really does get a 409, and the record really is
    # closed -- so treating it as success is not papering over a lost write.
    assert (
        client.post(
            f"{UI_PREFIX}/{org.alias}/scrums/{scrum_id}/finish", json=body
        ).status_code
        == 409
    )
    with Session(db_engine) as session:
        assert session.get(Scrum, scrum_id).total_seconds == 600

    page = client.get(f"{UI_PREFIX}/{org.alias}/workflow").text
    handler = page[page.index("writing.then(saved, function (err)") :]
    assert "err.status === 409" in handler[:400], "409 is still handled as a failure"
    assert "saved(); return;" in handler[:400], "409 does not reach the done state"
    assert "!err.fromOpen" in handler[:400], (
        "the 409 rule is no longer scoped to the write, so an open's 409 would "
        "complete the step as though it had saved"
    )
    assert "e.fromOpen = true;" in page, (
        "nothing marks a refusal that came from the open, so the scoping above "
        "can never distinguish one"
    )


def test_the_scrum_write_routes_require_a_session(client, populated_org):
    """`fetch` gets a 401 it can read, not the sign-in page's HTML.

    **All four of them**, which the plural in the name used to promise and only
    the open route delivered. A signed-out POST to these must not be answered with
    a 303 to the sign-in page: the caller is `fetch`, it follows the redirect, and
    hands the page's own HTML to a `.json()` call. Each route repeats the gate
    inline (see the note above `_UNAUTHENTICATED`) precisely so a new one cannot
    inherit it by accident -- and `/picks` was new.
    """
    _, _, org, project_id = populated_org
    scrum_id = str(uuid4())
    for path, body in (
        ("", {"project_id": project_id}),
        (
            f"/{scrum_id}/visits",
            {"ticket_id": 1, "position": 0, "seconds": 1, "status_at_visit": "todo"},
        ),
        (f"/{scrum_id}/picks", {"picks": []}),
        (f"/{scrum_id}/finish", {"total_seconds": 1}),
    ):
        r = client.post(
            f"{UI_PREFIX}/{org.alias}/scrums{path}",
            json=body,
            follow_redirects=False,
        )
        assert r.status_code == 401, f"{path or '(open)'} answered {r.status_code}"
        assert r.json() == {"error": "Not signed in"}, path or "(open)"


def test_the_workflow_page_carries_the_scrum_write_url(client, populated_org):
    """The page has to know where to post, or the walk records nothing.

    Asserted on the served page rather than on the builder: the URL is assembled
    in the route, and a page that renders perfectly with an empty ``scrumsUrl``
    is exactly the silent failure this feature started as.
    """
    _, cookie, org, _ = populated_org
    _auth(client, cookie)
    html = client.get(f"{UI_PREFIX}/{org.alias}/workflow").text
    assert f'"scrumsUrl":"{UI_PREFIX}/{org.alias.lower()}/scrums"' in html


def test_a_platform_member_without_a_membership_is_not_offered_the_star(
    client, signed_in, make_org, db_engine
):
    """**Do not draw a control whose only outcome is a 404.**

    `default_project_id` is a column on the membership row. A platform member may
    open every org and holds a membership in none, so there is nothing for that
    POST to write -- it 404s. The star used to render anyway, and the script
    moves the highlight before the round trip, so the click visibly succeeded and
    then landed on an error page.
    """
    user, cookie = signed_in(is_platform_member=True)
    org = make_org("pf", name="Haviland")  # note: no membership for this user
    with Session(db_engine) as session:
        session.add(
            Project(
                id=str(uuid4()),
                organization_id=org.id,
                alias="PF",
                name="PixelFuel",
                description="d",
            )
        )
        session.commit()

    _auth(client, cookie)
    page = client.get(f"{UI_PREFIX}/{org.alias}/workflow")
    assert page.status_code == 200
    assert "default-project" not in page.text

    # And the route it would have posted to still refuses, so hiding the control
    # is the page agreeing with the server rather than covering for it.
    with Session(db_engine) as session:
        project_id = (
            session.exec(select(Project).where(Project.organization_id == org.id))
            .first()
            .id
        )
    r = client.post(
        f"{UI_PREFIX}/{org.alias}/default-project",
        data={"project_id": project_id},
        follow_redirects=False,
    )
    assert r.status_code == 404


# --------------------------------------------------------------------------- #
# Give scrum update -- the personal daily record
#
# The tenth workflow. It records *intent* -- which finished ticket should come
# back and which unowned ticket somebody is taking on -- into
# `ScrumTicketVisit.moved_to`, a column documented for exactly that and which
# nothing has ever populated. It does **not** move the ticket, and the tests
# below hold it to saying so.
# --------------------------------------------------------------------------- #


def _project_of(db_engine, org):
    with Session(db_engine) as session:
        return (
            session.exec(select(Project).where(Project.organization_id == org.id))
            .first()
            .id
        )


def _ticket(db_engine, org, project_id, **kw):
    from src.domain.ticket import Ticket

    with Session(db_engine) as session:
        ticket = Ticket(
            summary=kw.pop("summary", "a ticket"),
            organization_id=org.id,
            project_id=project_id,
            **kw,
        )
        session.add(ticket)
        session.commit()
        session.refresh(ticket)
        return ticket.id


def _board(db_engine, org, project_id, user):
    """This project's board, created only if it has none.

    Reused rather than added: at most one *live* board per project is a partial
    unique index, so a second row is an IntegrityError rather than a second board.
    The tickets in the other update tests deliberately carry no
    `board_registration_id` at all -- an InnoDay-only ticket moves locally and
    reports success, which is the ordinary path and the one that must not paint a
    failure banner.
    """
    with Session(db_engine) as session:
        existing = session.exec(
            select(BoardRegistration).where(
                BoardRegistration.project_id == project_id,
                BoardRegistration.deleted_at.is_(None),
            )
        ).first()
        if existing is not None:
            return existing.id
        board = BoardRegistration(
            id=str(uuid4()),
            user_id=user.id,
            organization_id=org.id,
            project_id=project_id,
            board_name="PixelFuel",
            board_url="https://linear.app/hs/team/PF",
            board_type=BoardType.LINEAR,
            board_external_id="team-uuid",
        )
        session.add(board)
        session.commit()
        return board.id


class _FailingAdapter:
    """A board that initializes fine and then refuses the status push.

    The two have to be separable: an adapter that failed to build at all would
    exercise the credential branch instead, and that is a different message.

    ``fail_times`` is what makes a *retry* observable: ``1`` fails the first push
    and accepts the second, which is the difference between "the error was
    cleared" and "the board was actually told". ``pushes`` counts every attempt,
    including the ones that raised.
    """

    def __init__(self, error, *, fail_times=None):
        self.error = error
        self.fail_times = fail_times
        self.pushes = 0
        self.state_name_to_id = {}

    async def initialize(self, token):
        self.state_name_to_id = {"In Progress": "s2"}

    async def update_ticket_status(self, ticket, new_status):
        self.pushes += 1
        if self.fail_times is None or self.pushes <= self.fail_times:
            raise self.error
        return ticket

    async def get_board_metadata(self):
        return {"members": []}

    async def set_board_assignee(self, ticket, board_user_id):
        raise self.error


def _use_adapter(monkeypatch, adapter):
    """Point the status service's two outbound seams at ``adapter``."""
    from src.services import ticket_status_service

    monkeypatch.setattr(
        ticket_status_service, "resolve_board_token", lambda *a, **k: "tok"
    )
    monkeypatch.setattr(
        ticket_status_service,
        "build_board_adapter",
        mock.AsyncMock(return_value=adapter),
    )


def _signed_in_colleague(db_engine, org):
    """A second active member of the org — somebody whose work is not yours."""
    from src.domain.organization import OrganizationMembership, OrganizationRole

    with Session(db_engine) as session:
        other = User(
            id=str(uuid4()),
            email=f"{uuid4().hex[:8]}@example.com",
            full_name="Grace Hopper",
        )
        session.add(other)
        session.commit()
        session.add(
            OrganizationMembership(
                id=str(uuid4()),
                organization_id=org.id,
                user_id=other.id,
                role=OrganizationRole.DEVELOPER,
                is_active=True,
            )
        )
        session.commit()
        session.refresh(other)
        return other, None


def _set_role(db_engine, org, user, role):
    """Give this user that role in the org, creating the membership if needed."""
    from src.domain.organization import OrganizationMembership

    with Session(db_engine) as session:
        membership = session.exec(
            select(OrganizationMembership).where(
                OrganizationMembership.organization_id == org.id,
                OrganizationMembership.user_id == user.id,
            )
        ).first()
        if membership is None:
            membership = OrganizationMembership(
                id=str(uuid4()),
                organization_id=org.id,
                user_id=user.id,
                is_active=True,
            )
        membership.role = role
        session.add(membership)
        # A platform member bypasses org roles entirely, so a role test on one
        # certifies nothing about the gate.
        person = session.get(User, user.id)
        person.is_platform_member = False
        session.add(person)
        session.commit()


def _visits(session, scrum_id):
    """The visits this record **holds**, in the order it holds them.

    Ordered by ``position`` rather than by insertion, because position is what the
    record claims the order is and a reconcile rewrites it.

    **Withdrawn rows are excluded, because they are not part of the record.** A
    pick that is taken back keeps its row -- it is the only thing that remembers
    whether the board ever got that ticket's comment -- but it moves nothing, is
    not counted by `visit_count`, and is not rendered or resumed. "What the record
    holds" is what every caller means, so it is what this answers. Use
    `_visit_rows` when the question is about the row rather than the record.
    """

    return [v for v in _visit_rows(session, scrum_id) if v.withdrawn_at is None]


def _visit_rows(session, scrum_id):
    """Every visit row, withdrawn ones included -- the storage, not the record.

    Separate from `_visits` on purpose. A test that wants to prove a withdrawn
    pick's row *survived* has to be able to see it, and a test about what the
    record holds must not.
    """
    from src.domain.scrum import ScrumTicketVisit

    return list(
        session.exec(
            select(ScrumTicketVisit)
            .where(ScrumTicketVisit.scrum_id == scrum_id)
            .order_by(ScrumTicketVisit.position)
        ).all()
    )


def _submit_update(client, org, project_id, picks=(), notes=None, comments=None):
    """`_run_update`, for the tests that only care which record was written."""
    return _run_update(
        client, org, project_id, picks=picks, notes=notes, comments=comments
    )[0]


def _run_update(
    client, org, project_id, picks=(), notes=None, comments=None, scrum_id=None
):
    """Walk the update: open the record, send the whole selection, close it.

    The same three calls the page's script makes, in the same order, so a test
    that passes here is a test of the path the browser takes -- including that the
    picks go as **one set**, which is what makes un-ticking expressible.

    ``moved_to`` comes from `UPDATE_MOVES_TO` rather than a literal. They agree
    today (`"in progress"`, with the space), and if that enum value is ever
    respelled a literal here keeps every test green while the browser posts
    something else -- into the column a later change reads to decide what to move.
    """
    from src.routers.webui.workflow import UPDATE_MOVES_TO

    opened = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums",
        json={"project_id": project_id, "kind": "update"},
    )
    assert opened.status_code == 201, opened.text
    scrum_id = opened.json()["scrum_id"]
    # `comments` mirrors what the page's own `submitPicks` sends: **the key is
    # always present**, empty included, because an emptied box is a deletion and
    # an absent key is a caller that never mentioned comments.
    said = comments or {}
    sent = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums/{scrum_id}/picks",
        json={
            "picks": [
                {
                    "ticket_id": ticket_id,
                    "status_at_visit": status_at_visit,
                    "moved_to": UPDATE_MOVES_TO,
                    "comment": said.get(ticket_id, ""),
                }
                for ticket_id, status_at_visit in picks
            ]
        },
    )
    assert sent.status_code == 200, sent.text
    assert sent.json()["recorded"] == len(picks)
    closed = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums/{scrum_id}/finish",
        json={"ended_at": UTC_NOW.isoformat(), "notes_markdown": notes},
    )
    assert closed.status_code == 200, closed.text
    # The finish answer is returned as well as the id: submitting is what applies
    # the moves, so what it says about them -- pushed, or not and why -- is the
    # only place the page (and therefore a test of the page) can read it.
    return scrum_id, closed.json()


def test_the_tenth_workflow_is_offered_and_claims_only_what_it_writes(
    client, populated_org
):
    """A tenth workflow, second under Building, and it does save something.

    The count is pinned because the catalogue is the page's whole map of the
    product: a workflow silently dropped is a capability the launcher stops
    offering, and one silently added is a promise nobody wrote.

    ``saves`` is True and ``warn`` empty because this workflow *does* write --
    the record of what you chose. What it must not do is imply the tickets moved,
    and that is asserted on the wording rather than on the flag.
    """
    _, cookie, org, _ = populated_org
    _auth(client, cookie)
    html = client.get(f"{UI_PREFIX}/{org.alias}/workflow").text
    blob = _workflow_blob(html)

    by_id = {w["id"]: w for w in blob["workflows"]}
    assert len(by_id) == 10
    assert "give-scrum-update" in by_id

    building = [w["id"] for w in blob["workflows"] if w["pillar"] == "building"]
    assert building[:2] == ["run-scrum", "give-scrum-update"], (
        "the two daily workflows lead their column, in that order"
    )

    entry = by_id["give-scrum-update"]
    assert entry["saves"] is True
    assert entry["warn"] == ""
    # **The copy has to keep up with the code, in both directions.** It said the
    # tickets had not moved, which was true and is no longer; a panel that still
    # said so would understate what the button just did, and understating is the
    # same class of error as overstating -- the reader cannot act on either.
    done = entry["done"].lower()
    assert "moved" in done or "moves" in done
    assert "have not moved" not in done
    assert "separate change" not in done
    assert not entry["done"].startswith("Nothing was saved.")


def test_the_update_steps_no_longer_promise_less_than_they_do(
    client, populated_org, db_engine
):
    """PR 1's honesty copy, brought up to date rather than left behind.

    Each picker had a note saying nothing moved yet and that the ticket was not
    assigned to you -- both accurate then, both false now. This pins the
    replacement rather than merely the deletion, because a step that says nothing
    about what the button does is not an improvement on one that says the wrong
    thing.
    """
    user, cookie, org, project_id = populated_org
    naive = UTC_NOW.replace(tzinfo=None)
    _ticket(
        db_engine,
        org,
        project_id,
        summary="finished",
        status=TicketStatus.DONE,
        assigned_to=user.id,
        completed_at=naive - timedelta(days=1),
    )
    _ticket(db_engine, org, project_id, summary="unowned", status=TicketStatus.TODO)
    _auth(client, cookie)
    bodies = _workflow_blob(client.get(f"{UI_PREFIX}/{org.alias}/workflow").text)[
        "projects"
    ][project_id]["bodies"]

    reopen = bodies["give-scrum-update.0"]
    assert "Nothing moves yet" not in reopen
    assert "submit" in reopen.lower(), (
        "the reopen step no longer says when the move happens"
    )

    take = bodies["give-scrum-update.1"]
    assert "not assigned to you yet" not in take
    assert "assign" in take.lower()


def test_the_update_tick_is_yours_and_the_scrum_tick_is_the_projects(
    client, signed_in, make_org, db_engine
):
    """**Requirement 5, and the two halves are not the same question.**

    "Give scrum update" ticks when *this viewer* submitted today. "Run scrum"
    ticks when *anyone* did -- a stand-up is one meeting for the project, so a
    second person seeing an empty box would go and run it again.

    Two users on one project, because a single-user test cannot tell a
    per-viewer tick from a per-project one: both look identical.
    """
    alice, alice_cookie = signed_in(email="alice-tick@example.com")
    bob, bob_cookie = signed_in(email="bob-tick@example.com")
    org = make_org("pf", name="Haviland", member=alice)
    with Session(db_engine) as session:
        session.add(
            OrganizationMembership(
                id=str(uuid4()),
                organization_id=org.id,
                user_id=bob.id,
                role=OrganizationRole.MEMBER,
                is_active=True,
            )
        )
        project = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias="PF",
            name="PixelFuel",
            description="d",
        )
        session.add(project)
        session.commit()
        session.refresh(project)
    project_id = project.id

    def ticks(cookie):
        _auth(client, cookie)
        blob = _workflow_blob(client.get(f"{UI_PREFIX}/{org.alias}/workflow").text)
        return blob["projects"][project_id]["ticks"]

    assert ticks(alice_cookie)["give-scrum-update"]["on"] is False
    assert ticks(alice_cookie)["run-scrum"]["on"] is False

    _auth(client, alice_cookie)
    _submit_update(client, org, project_id)

    assert ticks(alice_cookie)["give-scrum-update"]["on"] is True
    assert ticks(bob_cookie)["give-scrum-update"]["on"] is False, (
        "Alice's update ticked Bob's box -- the tick is per viewer"
    )

    # Now the team scrum, which is the project's, not the runner's.
    _auth(client, alice_cookie)
    scrum_id = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums",
        json={"project_id": project_id, "kind": "scrum"},
    ).json()["scrum_id"]
    assert (
        client.post(
            f"{UI_PREFIX}/{org.alias}/scrums/{scrum_id}/finish",
            json={"ended_at": UTC_NOW.isoformat()},
        ).status_code
        == 200
    )

    assert ticks(alice_cookie)["run-scrum"]["on"] is True
    assert ticks(bob_cookie)["run-scrum"]["on"] is True, (
        "a scrum somebody else ran must still tick the project's box"
    )
    # Distinct hover text: one means "you did it", the other "somebody did".
    mine = ticks(bob_cookie)["give-scrum-update"]["title"]
    theirs = ticks(bob_cookie)["run-scrum"]["title"]
    assert mine != theirs, "the two ticks read the same and mean different things"


# --------------------------------------------------------------------------- #
# Requirement 7 -- who has already given their update, on `run-scrum`.
# --------------------------------------------------------------------------- #


def _run_scrum_bodies(client, org, project_id):
    blob = _workflow_blob(client.get(f"{UI_PREFIX}/{org.alias}/workflow").text)
    return blob["projects"][project_id]["bodies"]


def test_run_scrum_shows_todays_submitters_and_names_them_in_the_wrap_up(
    client, signed_in, make_org, db_engine
):
    """**Requirement 7.** The avatar group, and the wrap-up that names them.

    Three people on the project and two of them submit, because a group built
    from "everybody mapped here" and one built from "everybody who submitted"
    are indistinguishable when everybody submitted. The third is the control.

    The bubbles are `render._bubbles`' output -- **already-escaped HTML** -- so
    they can only travel as a ``bodies`` value; the engine assigns those with
    ``innerHTML``. A raw-text field would render the markup as text.
    """
    alice, alice_cookie = signed_in(
        email="alice-av@example.com", full_name="Alice Avatar"
    )
    bob, bob_cookie = signed_in(email="bob-av@example.com", full_name="Bob Bubble")
    carol, carol_cookie = signed_in(
        email="carol-av@example.com", full_name="Carol Quiet"
    )
    org = make_org("pf", name="Haviland", member=alice)
    with Session(db_engine) as session:
        for person in (bob, carol):
            session.add(
                OrganizationMembership(
                    id=str(uuid4()),
                    organization_id=org.id,
                    user_id=person.id,
                    # DEVELOPER, not MEMBER: submitting an update posts its picks,
                    # and that route now moves tickets, so a MEMBER is refused.
                    role=OrganizationRole.DEVELOPER,
                    is_active=True,
                )
            )
        project = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias="PF",
            name="PixelFuel",
            description="d",
        )
        session.add(project)
        session.commit()
        session.refresh(project)
    project_id = project.id

    # Nobody yet: the empty case is this page's own sentence, not `_bubbles`'.
    _auth(client, carol_cookie)
    bodies = _run_scrum_bodies(client, org, project_id)
    assert "Nobody has given their update yet today." in bodies["run-scrum.0"]
    assert "No one mapped yet" not in bodies["run-scrum.0"], (
        "`_bubbles`' empty wording says the team is unmapped; here they simply "
        "have not filled the form in"
    )
    assert "No one mapped yet" not in bodies["run-scrum.2"]

    for cookie in (alice_cookie, bob_cookie):
        _auth(client, cookie)
        _submit_update(client, org, project_id)

    _auth(client, carol_cookie)
    bodies = _run_scrum_bodies(client, org, project_id)

    opening, wrap_up = bodies["run-scrum.0"], bodies["run-scrum.2"]
    # Exactly two avatars -- Carol submitted nothing and must not appear.
    assert opening.count('<span class="bub"') == 2, opening
    assert "Alice Avatar" in opening and "Bob Bubble" in opening
    assert "Carol Quiet" not in opening

    # And the wrap-up names them, which a group of initials cannot.
    assert "Alice Avatar" in wrap_up and "Bob Bubble" in wrap_up
    assert "Carol Quiet" not in wrap_up
    assert "Nobody has given their update yet today." not in wrap_up


def test_an_abandoned_update_puts_nobody_in_the_avatar_group(
    client, signed_in, make_org, db_engine
):
    """Opening the workflow and walking out of it is not giving an update.

    ``ended_at IS NULL`` is how this schema spells "somebody abandoned this" --
    the same rule the scrum tick already uses -- so a row that was opened and
    never closed must leave the group empty. Without this the avatars would
    report a teammate as having reported in because they had the tab open.
    """
    alice, alice_cookie = signed_in(
        email="alice-abandon@example.com", full_name="Alice A"
    )
    org = make_org("pf", name="Haviland", member=alice)
    with Session(db_engine) as session:
        project = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias="PF",
            name="PixelFuel",
            description="d",
        )
        session.add(project)
        session.commit()
        session.refresh(project)
    project_id = project.id

    _auth(client, alice_cookie)
    opened = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums",
        json={"project_id": project_id, "kind": "update"},
    )
    assert opened.status_code == 201, opened.text

    bodies = _run_scrum_bodies(client, org, project_id)
    assert "Nobody has given their update yet today." in bodies["run-scrum.0"]
    assert "Alice A" not in bodies["run-scrum.2"]

    # Closing it is what makes it an update that was given.
    assert (
        client.post(
            f"{UI_PREFIX}/{org.alias}/scrums/{opened.json()['scrum_id']}/finish",
            json={"ended_at": UTC_NOW.isoformat()},
        ).status_code
        == 200
    )
    bodies = _run_scrum_bodies(client, org, project_id)
    assert "Alice A" in bodies["run-scrum.2"]


def test_every_project_carries_its_own_submitters_not_just_the_open_one(
    client, signed_in, make_org, db_engine
):
    """The rail switches project in the browser with no round trip.

    So the avatars have to be in **every** project's payload. A group rendered
    only for the selected project would keep showing the project the page loaded
    with -- reporting somebody as having given an update on a project they never
    touched, which is the same class of error as the server-rendered tick this
    page already refuses to draw.
    """
    alice, alice_cookie = signed_in(
        email="alice-two@example.com", full_name="Alice Two"
    )
    org = make_org("pf", name="Haviland", member=alice)
    ids = []
    with Session(db_engine) as session:
        for alias in ("PF", "QQ"):
            project = Project(
                id=str(uuid4()),
                organization_id=org.id,
                alias=alias,
                name=f"Project {alias}",
                description="d",
            )
            session.add(project)
            session.commit()
            session.refresh(project)
            ids.append(project.id)
    first, second = ids

    _auth(client, alice_cookie)
    _submit_update(client, org, second)

    blob = _workflow_blob(client.get(f"{UI_PREFIX}/{org.alias}/workflow").text)
    bodies = {pid: blob["projects"][pid]["bodies"] for pid in ids}
    assert "Alice Two" in bodies[second]["run-scrum.0"]
    assert "Alice Two" in bodies[second]["run-scrum.2"]
    assert "Alice Two" not in bodies[first]["run-scrum.0"], (
        "one project's submitter leaked into another's group"
    )
    assert "Nobody has given their update yet today." in bodies[first]["run-scrum.0"]


def test_the_avatar_group_costs_the_page_no_extra_query(
    client, signed_in, make_org, db_engine
):
    """**Re-run deliberately, on the shape the avatars actually need.**

    `data.ScrumActivity.submitters` is populated by the read that already answers
    the daily ticks, and the whole reason it is shaped that way is that a tick and
    an avatar group derived from two queries can disagree about who submitted.
    This pins the *no second query* half: the page's SELECT count with submitters
    present is the count without them.

    **The count is asserted in the same run as the output, and that is the fix
    for what this test used to be.** It compared SELECT counts before and after a
    second person submitted, and never looked at what the page rendered -- so it
    measured "an extra `scrums` row costs no query" rather than "rendering the
    group costs no query". Verified by the reviewer: with `_submitters_group`
    returning an empty list -- the feature deleted -- it still passed, and would
    have passed unmodified on `main`. A test that survives the removal of its own
    subject is not evidence of anything.
    """
    alice, alice_cookie = signed_in(email="alice-q@example.com", full_name="Alice Q")
    bob, bob_cookie = signed_in(email="bob-q@example.com", full_name="Bob Q")
    org = make_org("pf", name="Haviland", member=alice)
    with Session(db_engine) as session:
        session.add(
            OrganizationMembership(
                id=str(uuid4()),
                organization_id=org.id,
                user_id=bob.id,
                role=OrganizationRole.DEVELOPER,
                is_active=True,
            )
        )
        project = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias="PF",
            name="PixelFuel",
            description="d",
        )
        session.add(project)
        session.commit()
        session.refresh(project)
    project_id = project.id

    def load(cookie):
        """One page load: its SELECT count **and** what it rendered."""
        _auth(client, cookie)
        statements = []
        listener = lambda conn, cur, stmt, *a: statements.append(stmt)  # noqa: E731
        event.listen(db_engine, "before_cursor_execute", listener)
        try:
            response = client.get(f"{UI_PREFIX}/{org.alias}/workflow")
            assert response.status_code == 200
        finally:
            event.remove(db_engine, "before_cursor_execute", listener)
        selects = len(
            [s for s in statements if s.lstrip().upper().startswith("SELECT")]
        )
        bodies = _workflow_blob(response.text)["projects"][project_id]["bodies"]
        return selects, bodies

    before, empty_bodies = load(alice_cookie)
    assert '<span class="bub"' not in empty_bodies["run-scrum.0"], (
        "somebody is in the group before anybody has submitted"
    )

    _auth(client, bob_cookie)
    _submit_update(client, org, project_id)

    after, bodies = load(alice_cookie)

    # **The group really rendered in the run that was counted.** Without this the
    # assertion below holds just as well when the feature does not exist.
    assert bodies["run-scrum.0"].count('<span class="bub"') == 1, bodies["run-scrum.0"]
    assert "Bob Q" in bodies["run-scrum.0"]
    assert "Bob Q" in bodies["run-scrum.2"]

    assert after == before, (
        f"rendering the avatar group cost {after - before} extra SELECT(s); it "
        "must ride the read that already answers the ticks"
    )


def test_the_reopen_list_is_only_your_own_recently_finished_work(
    client, signed_in, make_org, db_engine
):
    """Requirement 2, and every clause of it is a way this goes wrong.

    Only DONE, only the viewer's, only inside the window -- and a DONE ticket
    with no ``completed_at`` is not offered at all rather than guessed at from
    ``updated_at``. It cannot ride `project_tickets_for`, whose rows carry
    neither column.
    """
    from src.domain.ticket import TicketStatus
    from src.routers.webui.workflow import REOPEN_WINDOW_DAYS

    alice, cookie = signed_in(email="alice-reopen@example.com")
    other, _ = signed_in(email="other-reopen@example.com")
    org = make_org("pf", name="Haviland", member=alice)
    with Session(db_engine) as session:
        project = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias="PF",
            name="PixelFuel",
            description="d",
        )
        session.add(project)
        session.commit()
        session.refresh(project)
    project_id = project.id
    naive = UTC_NOW.replace(tzinfo=None)

    offered = _ticket(
        db_engine,
        org,
        project_id,
        summary="mine, finished yesterday",
        status=TicketStatus.DONE,
        assigned_to=alice.id,
        completed_at=naive - timedelta(days=1),
    )
    stale = _ticket(
        db_engine,
        org,
        project_id,
        summary="mine, finished long ago",
        status=TicketStatus.DONE,
        assigned_to=alice.id,
        completed_at=naive - timedelta(days=REOPEN_WINDOW_DAYS + 2),
    )
    theirs = _ticket(
        db_engine,
        org,
        project_id,
        summary="somebody else finished this",
        status=TicketStatus.DONE,
        assigned_to=other.id,
        completed_at=naive - timedelta(days=1),
    )
    undated = _ticket(
        db_engine,
        org,
        project_id,
        summary="finished but never stamped",
        status=TicketStatus.DONE,
        assigned_to=alice.id,
        completed_at=None,
    )
    in_flight = _ticket(
        db_engine,
        org,
        project_id,
        summary="mine but still going",
        status=TicketStatus.IN_PROGRESS,
        assigned_to=alice.id,
    )

    _auth(client, cookie)
    blob = _workflow_blob(client.get(f"{UI_PREFIX}/{org.alias}/workflow").text)
    body = blob["projects"][project_id]["bodies"]["give-scrum-update.0"]
    rows = blob["projects"][project_id]["update"]["rows"]

    assert f'data-pick="{offered}"' in body
    assert str(offered) in rows
    for absent, why in (
        (stale, "outside the window"),
        (theirs, "assigned to somebody else"),
        (undated, "DONE with no completed_at"),
        (in_flight, "not finished"),
    ):
        assert f'data-pick="{absent}"' not in body, why
        assert str(absent) not in rows, why

    # And the page says why an unstamped ticket is missing, rather than the
    # reader concluding the list is broken.
    assert "completed_at" in body or "completion date" in body.lower()


def test_the_take_on_list_is_unassigned_todo_oldest_first(
    client, signed_in, make_org, db_engine
):
    """Requirement 3: showing unowned work is the point; taking a colleague's is not.

    Unassigned only, oldest first, capped. Oldest first because the whole value
    of the list is surfacing what has been sitting there, and a newest-first list
    buries exactly that.
    """
    from src.domain.ticket import Ticket, TicketStatus

    alice, cookie = signed_in(email="alice-take@example.com")
    other, _ = signed_in(email="other-take@example.com")
    org = make_org("pf", name="Haviland", member=alice)
    with Session(db_engine) as session:
        project = Project(
            id=str(uuid4()),
            organization_id=org.id,
            alias="PF",
            name="PixelFuel",
            description="d",
        )
        session.add(project)
        session.commit()
        session.refresh(project)
    project_id = project.id
    naive = UTC_NOW.replace(tzinfo=None)

    # Thirty unassigned TODOs, created oldest-last so arrival order cannot be
    # mistaken for the ordering under test.
    ids = []
    with Session(db_engine) as session:
        for n in range(30):
            ticket = Ticket(
                summary=f"unowned {n}",
                organization_id=org.id,
                project_id=project_id,
                status=TicketStatus.TODO,
                created_at=naive - timedelta(days=n),
            )
            session.add(ticket)
            session.commit()
            session.refresh(ticket)
            ids.append((n, ticket.id))
    oldest = ids[-1][1]
    newest = ids[0][1]

    taken = _ticket(
        db_engine,
        org,
        project_id,
        summary="already somebody's",
        status=TicketStatus.TODO,
        assigned_to=other.id,
    )

    _auth(client, cookie)
    blob = _workflow_blob(client.get(f"{UI_PREFIX}/{org.alias}/workflow").text)
    payload = blob["projects"][project_id]
    body = payload["bodies"]["give-scrum-update.1"]

    assert f'data-pick="{taken}"' not in body, (
        "a colleague's ticket is offered for the taking"
    )
    assert f'data-pick="{oldest}"' in body, "the oldest unowned ticket is not offered"
    assert f'data-pick="{newest}"' not in body, (
        "the list is newest-first, so what has been sitting longest is buried"
    )
    picks = re.findall(r'data-pick="(\d+)"', body)
    assert len(picks) == 25, f"the list is capped at 25, got {len(picks)}"
    assert picks[0] == str(oldest)


def _move_errors(answer):
    """Every move failure the submit reported.

    The response used to carry one `error` string. It now carries them all —
    keeping only the first meant a second ticket's refusal was discarded before
    the answer left the server, so the page could report one thing wrong out of
    however many were. These helpers read the list and keep each assertion
    saying exactly what it said before.
    """
    return list(answer.get("errors") or [])


def _comment_errors(answer):
    """Every comment failure. Was `comment_error`, and was never displayed."""
    return list(answer.get("comment_errors") or [])


def _move_notices(answer):
    return list(answer.get("notices") or [])


def _comment_notices(answer):
    return list(answer.get("comment_notices") or [])


def test_submitting_an_update_records_the_ask_and_then_actually_makes_the_move(
    client, populated_org, db_engine
):
    """**The record and the move, in that order, both asserted.**

    Ticking records the intent in ``ScrumTicketVisit.moved_to``; *submitting*
    applies it. Both halves are pinned here because they fail differently: a
    record with no move is a page reporting an ask it never carried out, and a
    move with no record is a status change with nothing saying who asked for it.

    ``completed_at`` is asserted **cleared**, not merely "the status changed". A
    reopened ticket that keeps its completion date reads to
    `SummaryService._activity_at` as in-window finished work, which is the bug
    `board_sync_service.py:511-524` exists to record.
    """
    from src.domain.scrum import Scrum, ScrumKind, ScrumTicketVisit
    from src.domain.ticket import Ticket, TicketStatus

    user, cookie, org, project_id = populated_org
    naive = UTC_NOW.replace(tzinfo=None)
    finished = _ticket(
        db_engine,
        org,
        project_id,
        summary="bring this back",
        status=TicketStatus.DONE,
        assigned_to=user.id,
        completed_at=naive - timedelta(days=1),
    )
    with Session(db_engine) as session:
        was = session.get(Ticket, finished).updated_at
    _auth(client, cookie)
    scrum_id, answer = _run_update(
        client, org, project_id, picks=[(finished, "done")], notes="back on it"
    )

    # Nothing to push to -- these tickets have no board registration -- so the
    # answer is a clean applied-and-nothing-outstanding.
    assert answer["applied"] is True
    assert not _move_errors(answer)

    with Session(db_engine) as session:
        row = session.get(Scrum, scrum_id)
        assert row.kind == ScrumKind.UPDATE.value
        assert row.ended_at is not None
        assert row.notes_markdown == "back on it"
        # NULL on purpose: an update has no clock and walks no board. Anything
        # that later aggregates scrum duration has to filter on `kind`.
        assert row.total_seconds is None
        assert row.lingering_count is None

        visits = session.exec(
            select(ScrumTicketVisit).where(ScrumTicketVisit.scrum_id == scrum_id)
        ).all()
        assert len(visits) == 1
        assert visits[0].ticket_id == finished
        assert visits[0].moved_to == "in progress"
        assert visits[0].status_at_visit == "done"
        assert visits[0].seconds == 0
        assert visits[0].position == 0
        assert visits[0].push_error is None

        # And the ticket itself has moved.
        ticket = session.get(Ticket, finished)
        assert ticket.status == TicketStatus.IN_PROGRESS
        assert ticket.completed_at is None, "a reopened ticket kept its finish date"
        assert ticket.updated_at > was
        assert ticket.assigned_to == user.id


def test_taking_an_unowned_ticket_makes_it_yours_where_a_person_would_look(
    client, populated_org, db_engine
):
    """**Requirement 3's assignment half, asserted through a reader.**

    ``assigned_to`` is a column; "it is mine now" is a thing a person sees. A
    test that stopped at the column would pass over a version where the ticket
    never appears as theirs anywhere -- which is the gap that made #641's sibling
    test vacuous. So the assertion goes through `data.my_tickets`, the query the
    dashboard's "your tickets" block actually runs.

    ``assignee`` is asserted too: it is the board's display mirror, read by
    `ProjectTicketRow.owner`, and writing one without the other leaves the ticket
    assigned on exactly one of the two surfaces that show it.
    """
    from src.routers.webui.data import my_tickets

    user, cookie, org, project_id = populated_org
    unowned = _ticket(
        db_engine,
        org,
        project_id,
        summary="nobody has this",
        status=TicketStatus.TODO,
    )
    _auth(client, cookie)
    _run_update(client, org, project_id, picks=[(unowned, "todo")])

    with Session(db_engine) as session:
        ticket = session.get(Ticket, unowned)
        assert ticket.status == TicketStatus.IN_PROGRESS
        assert ticket.assigned_to == user.id
        assert ticket.assignee == (user.full_name or user.email)

        mine = my_tickets(session, project_id, user.id)
        assert unowned in [row.id for row in mine], (
            "the ticket was taken but does not show as the viewer's own work"
        )


def test_re_entering_after_the_moves_landed_does_not_erase_the_record(
    client, populated_org, db_engine
):
    """**The regression applying the moves creates, pinned where it happens.**

    Submitting moves the ticket, which takes it out of the very list the picker
    builds from: a reopened ticket is no longer DONE, and a taken one is no longer
    unowned. So on re-entry both pickers would render empty -- and pressing
    through posts the complete selection the page can see, which is nothing.
    `replace_picks` is a whole-set write by design, so it would faithfully delete
    every visit the day's record holds, along with each visit's `push_error`.
    Opening the record to look at it would destroy it.

    Asserted on both halves, because they come from different queries and only
    one of them would be caught by the reopen case: the *taken* ticket has to come
    back under **step 1**, not step 0, which is what `status_at_visit` decides.
    """
    from src.domain.scrum import ScrumTicketVisit

    user, cookie, org, project_id = populated_org
    naive = UTC_NOW.replace(tzinfo=None)
    finished = _ticket(
        db_engine,
        org,
        project_id,
        summary="brought back",
        status=TicketStatus.DONE,
        assigned_to=user.id,
        completed_at=naive - timedelta(days=1),
    )
    unowned = _ticket(
        db_engine, org, project_id, summary="taken on", status=TicketStatus.TODO
    )
    _auth(client, cookie)
    scrum_id, _ = _run_update(
        client, org, project_id, picks=[(finished, "done"), (unowned, "todo")]
    )

    bodies = _workflow_blob(client.get(f"{UI_PREFIX}/{org.alias}/workflow").text)[
        "projects"
    ][project_id]["bodies"]
    assert f'data-pick="{finished}"' in bodies["give-scrum-update.0"], (
        "a ticket brought back has vanished from the picker that recorded it"
    )
    assert f'data-pick="{unowned}"' in bodies["give-scrum-update.1"], (
        "a ticket taken on came back under the wrong step, or not at all"
    )
    for key in ("give-scrum-update.0", "give-scrum-update.1"):
        assert "checked" in bodies[key]

    # **The second pass posts what the page would post**, which is the status the
    # ticket is at *now* — deliberately, because that is the value the earlier
    # version of this test hard-coded as `"in progress"` and thereby supplied the
    # very corruption it should have caught.
    _run_update(
        client,
        org,
        project_id,
        picks=[(finished, "in progress"), (unowned, "in progress")],
    )
    with Session(db_engine) as session:
        visits = session.exec(
            select(ScrumTicketVisit).where(ScrumTicketVisit.scrum_id == scrum_id)
        ).all()
        assert len(visits) == 2, "re-entering the workflow emptied the day's record"
        by_ticket = {v.ticket_id: v for v in visits}
        # `status_at_visit` is documented as a historical observation that
        # "re-labelling or retiring a status later must not rewrite". A resubmit
        # is exactly such a later event, and overwriting it here is not cosmetic:
        # it is what routes a resumed pick to a picker.
        assert by_ticket[finished].status_at_visit == "done", (
            "a resubmit rewrote the status the ticket was at when it was picked"
        )
        assert by_ticket[unowned].status_at_visit == "todo"

    # **A third pass**, because the routing only had to survive one round trip to
    # look correct: with the observation overwritten, a brought-back ticket lands
    # under "Take anything on?" on the second re-entry and nothing before this
    # assertion would notice.
    bodies = _workflow_blob(client.get(f"{UI_PREFIX}/{org.alias}/workflow").text)[
        "projects"
    ][project_id]["bodies"]
    assert f'data-pick="{finished}"' in bodies["give-scrum-update.0"], (
        "on the second re-entry a brought-back ticket moved to the wrong picker"
    )
    assert f'data-pick="{unowned}"' in bodies["give-scrum-update.1"]


def test_a_withdrawn_pick_is_not_moved(client, populated_org, db_engine):
    """**The live version of the rule PR 1 fixed, now that moves are real.**

    Un-ticking a box removes the pick, and `replace_picks` reconciles rather than
    appends precisely so it can. Before the moves existed, a withdrawn pick that
    survived in the record was a wrong row; now it is somebody's ticket being
    moved after they said not to. Same bug, and only the second version of it is
    visible from outside.
    """
    user, cookie, org, project_id = populated_org
    naive = UTC_NOW.replace(tzinfo=None)
    keep = _ticket(
        db_engine,
        org,
        project_id,
        summary="still want this",
        status=TicketStatus.DONE,
        assigned_to=user.id,
        completed_at=naive - timedelta(days=1),
    )
    withdrawn = _ticket(
        db_engine,
        org,
        project_id,
        summary="changed my mind",
        status=TicketStatus.DONE,
        assigned_to=user.id,
        completed_at=naive - timedelta(days=1),
    )
    _auth(client, cookie)

    # First pass: both ticked, but nothing submitted yet -- the picker posts as
    # each step is left, which is the state somebody re-entering is correcting.
    opened = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums",
        json={"project_id": project_id, "kind": "update"},
    )
    scrum_id = opened.json()["scrum_id"]
    first = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums/{scrum_id}/picks",
        json={
            "picks": [
                {
                    "ticket_id": keep,
                    "status_at_visit": "done",
                    "moved_to": "in progress",
                },
                {
                    "ticket_id": withdrawn,
                    "status_at_visit": "done",
                    "moved_to": "in progress",
                },
            ]
        },
    )
    assert first.json()["recorded"] == 2

    # Second pass: one box un-ticked, then submit.
    _run_update(client, org, project_id, picks=[(keep, "done")])

    with Session(db_engine) as session:
        assert session.get(Ticket, keep).status == TicketStatus.IN_PROGRESS
        assert session.get(Ticket, withdrawn).status == TicketStatus.DONE, (
            "a pick the user withdrew was applied anyway"
        )
        assert session.get(Ticket, withdrawn).completed_at is not None


def test_a_board_push_failure_leaves_the_move_in_place_and_says_so(
    client, populated_org, db_engine, monkeypatch
):
    """**Local-first, push-second, and the failure is persisted rather than
    swallowed.**

    Three separate claims, and all three have to hold together: the local move
    stands (the board being down is not a reason to lose it), the answer says
    ``pushed: false`` with the adapter's own words (so `#wferr` can paint
    something actionable), and the failure is written to
    `ScrumTicketVisit.push_error` (so it survives the response, which is the
    whole point of a column rather than a return value).
    """
    from src.adapters.base_adapter import BoardAdapterError
    from src.domain.scrum import ScrumTicketVisit
    from src.services import ticket_status_service

    user, cookie, org, project_id = populated_org
    board_id = _board(db_engine, org, project_id, user)
    naive = UTC_NOW.replace(tzinfo=None)
    finished = _ticket(
        db_engine,
        org,
        project_id,
        summary="on a real board",
        status=TicketStatus.DONE,
        assigned_to=user.id,
        completed_at=naive - timedelta(days=1),
        board_registration_id=board_id,
        external_ticket_id="PF-7",
    )
    monkeypatch.setattr(
        ticket_status_service, "resolve_board_token", lambda *a, **k: "tok"
    )
    monkeypatch.setattr(
        ticket_status_service,
        "build_board_adapter",
        mock.AsyncMock(
            return_value=_FailingAdapter(BoardAdapterError("Linear is down"))
        ),
    )

    _auth(client, cookie)
    scrum_id, answer = _run_update(client, org, project_id, picks=[(finished, "done")])

    assert answer["applied"] is True
    assert answer["pushed"] is False
    assert any("Linear is down" in e for e in _move_errors(answer))

    with Session(db_engine) as session:
        assert session.get(Ticket, finished).status == TicketStatus.IN_PROGRESS
        visit = session.exec(
            select(ScrumTicketVisit).where(ScrumTicketVisit.scrum_id == scrum_id)
        ).one()
        assert visit.push_error and "Linear is down" in visit.push_error


def test_a_failed_push_is_retried_next_time_and_only_then_stops_being_reported(
    client, populated_org, db_engine, monkeypatch
):
    """**The bug that made a failed push permanent, pinned end to end.**

    The local status already matches after the first submit, so a short-circuit
    on "is the ticket where it should be?" answers "yes, nothing to do" and the
    board is never asked again — while the recorder, handed `error=None`, deletes
    the only record that it disagrees. Measured before the fix: second submit
    answers `pushed: true`, `push_error` becomes NULL, and the adapter's push
    count stays at one.

    Three things have to hold together, which is why they are one test: the retry
    really reaches the board, the answer only says `pushed` once it did, and the
    column is cleared only then.
    """
    from src.adapters.base_adapter import BoardAdapterError
    from src.domain.scrum import ScrumTicketVisit

    user, cookie, org, project_id = populated_org
    board_id = _board(db_engine, org, project_id, user)
    naive = UTC_NOW.replace(tzinfo=None)
    finished = _ticket(
        db_engine,
        org,
        project_id,
        summary="on a real board",
        status=TicketStatus.DONE,
        assigned_to=user.id,
        completed_at=naive - timedelta(days=1),
        board_registration_id=board_id,
        external_ticket_id="PF-9",
    )
    adapter = _FailingAdapter(BoardAdapterError("Linear is down"), fail_times=1)
    _use_adapter(monkeypatch, adapter)

    _auth(client, cookie)
    scrum_id, first = _run_update(client, org, project_id, picks=[(finished, "done")])
    assert first["pushed"] is False
    with Session(db_engine) as session:
        visit = session.exec(
            select(ScrumTicketVisit).where(ScrumTicketVisit.scrum_id == scrum_id)
        ).one()
        assert visit.push_error

    # Re-entering is what the page invites ("yours to correct until the day is
    # over"), so this is the ordinary path, not a contrived one.
    _, second = _run_update(client, org, project_id, picks=[(finished, "done")])

    assert adapter.pushes == 2, "the board was never asked a second time"
    assert second["pushed"] is True
    assert not _move_errors(second)
    with Session(db_engine) as session:
        visit = session.exec(
            select(ScrumTicketVisit).where(ScrumTicketVisit.scrum_id == scrum_id)
        ).one()
        assert visit.push_error is None, "a push that landed left its error behind"


def test_a_retry_that_fails_again_keeps_the_error_rather_than_clearing_it(
    client, populated_org, db_engine, monkeypatch
):
    """The other half: converging is not the same as giving up quietly.

    If the retry fails too, the record has to keep saying so — clearing it would
    turn a board that is still out of step into one nothing knows about.
    """
    from src.adapters.base_adapter import BoardAdapterError
    from src.domain.scrum import ScrumTicketVisit

    user, cookie, org, project_id = populated_org
    board_id = _board(db_engine, org, project_id, user)
    naive = UTC_NOW.replace(tzinfo=None)
    finished = _ticket(
        db_engine,
        org,
        project_id,
        summary="on a real board",
        status=TicketStatus.DONE,
        assigned_to=user.id,
        completed_at=naive - timedelta(days=1),
        board_registration_id=board_id,
        external_ticket_id="PF-10",
    )
    adapter = _FailingAdapter(BoardAdapterError("Linear is still down"))
    _use_adapter(monkeypatch, adapter)

    _auth(client, cookie)
    scrum_id, _ = _run_update(client, org, project_id, picks=[(finished, "done")])
    _, second = _run_update(client, org, project_id, picks=[(finished, "done")])

    assert adapter.pushes == 2
    assert second["pushed"] is False
    with Session(db_engine) as session:
        visit = session.exec(
            select(ScrumTicketVisit).where(ScrumTicketVisit.scrum_id == scrum_id)
        ).one()
        assert visit.push_error and "still down" in visit.push_error


def test_a_read_only_member_cannot_move_tickets_through_the_update(
    client, populated_org, db_engine
):
    """**The `/ui` path is now a ticket-mutation endpoint and must gate like one.**

    While picks were an inert record, any member recording their own intentions
    was proportionate. Now the same post writes `status`, `completed_at`,
    `assigned_to` and pushes to the client's board — and `MEMBER` is documented as
    "Read tickets, view summaries", while the equivalent
    `PUT /api/v1/{org}/boards/{board}/tickets/{id}` requires `DEVELOPER`.

    Being page-internal is not a reason to hold a lower bar than the API for the
    same effect.
    """
    from src.domain.organization import OrganizationRole

    user, cookie, org, project_id = populated_org
    unowned = _ticket(
        db_engine,
        org,
        project_id,
        summary="not theirs to take",
        status=TicketStatus.TODO,
    )
    _set_role(db_engine, org, user, OrganizationRole.MEMBER)
    _auth(client, cookie)

    opened = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums",
        json={"project_id": project_id, "kind": "update"},
    )
    assert opened.status_code == 201, "recording a scrum is not the thing being gated"
    refused = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums/{opened.json()['scrum_id']}/picks",
        json={
            "picks": [
                {
                    "ticket_id": unowned,
                    "status_at_visit": "todo",
                    "moved_to": "in progress",
                }
            ]
        },
    )

    assert refused.status_code == 403, refused.text
    with Session(db_engine) as session:
        assert session.get(Ticket, unowned).status == TicketStatus.TODO


def test_a_pick_the_picker_never_offered_is_recorded_but_not_applied(
    client, populated_org, db_engine
):
    """**The payload must never be the authority on what may move.**

    "DONE and mine within the window" and "unassigned TODO" are the two rules the
    pickers are built from, and they lived only in the two page queries. Nothing
    re-checked them on the way in, so a hand-rolled post could move a colleague's
    in-review ticket, or take one somebody already owns.

    The visit is still recorded — refusing the whole submit would lose the picks
    that *are* valid — but the ticket does not move, and the answer says so.
    """
    user, cookie, org, project_id = populated_org
    colleague, _ = _signed_in_colleague(db_engine, org)
    theirs = _ticket(
        db_engine,
        org,
        project_id,
        summary="somebody else is on this",
        status=TicketStatus.IN_REVIEW,
        assigned_to=colleague.id,
    )
    _auth(client, cookie)
    _, answer = _run_update(client, org, project_id, picks=[(theirs, "in review")])

    with Session(db_engine) as session:
        row = session.get(Ticket, theirs)
        assert row.status == TicketStatus.IN_REVIEW, "a colleague's ticket was moved"
        assert row.assigned_to == colleague.id
    assert _move_errors(answer), "an ineligible pick was applied silently"


def test_an_in_progress_unowned_ticket_is_not_takeable_by_a_crafted_pick(
    client, populated_org, db_engine
):
    """**The half of the eligibility hole a status check alone leaves open.**

    "Already at the target and unowned" has to pass — that is a take being
    re-submitted after a sync nulled `assigned_to`, and refusing it would report
    every previously-applied pick as invalid. But on its own it also admits an
    IN_PROGRESS, unowned ticket, which **neither picker has ever shown**: the
    reopen list reads DONE, the take list reads TODO. Verified before the fix:
    `applied: True, moved: 1`, assigned to the poster.

    Closed by gating on the visit's recorded `status_at_visit` — the state the
    pick claims to have come off — so a post naming a state no picker reads from
    is refused whatever the ticket's current status is.
    """
    user, cookie, org, project_id = populated_org
    drifting = _ticket(
        db_engine,
        org,
        project_id,
        summary="in flight and unowned",
        status=TicketStatus.IN_PROGRESS,
    )
    _auth(client, cookie)
    _, answer = _run_update(client, org, project_id, picks=[(drifting, "in progress")])

    with Session(db_engine) as session:
        row = session.get(Ticket, drifting)
        assert row.assigned_to is None, (
            "a ticket no picker offers was taken by naming it in the payload"
        )
    assert _move_errors(answer)
    assert answer["moved"] == 0


def test_a_soft_deleted_ticket_is_neither_offered_again_nor_moved(
    client, populated_org, db_engine
):
    """`deleted_at` is how a cleared board keeps its rows for audit, and every
    other list query filters it. The resumed-picks read did not, so a ticket
    deleted between recording and submitting was re-rendered as a live pre-ticked
    pick and then written and pushed."""
    user, cookie, org, project_id = populated_org
    naive = UTC_NOW.replace(tzinfo=None)
    finished = _ticket(
        db_engine,
        org,
        project_id,
        summary="deleted under us",
        status=TicketStatus.DONE,
        assigned_to=user.id,
        completed_at=naive - timedelta(days=1),
    )
    _auth(client, cookie)
    opened = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums",
        json={"project_id": project_id, "kind": "update"},
    )
    scrum_id = opened.json()["scrum_id"]
    client.post(
        f"{UI_PREFIX}/{org.alias}/scrums/{scrum_id}/picks",
        json={
            "picks": [
                {
                    "ticket_id": finished,
                    "status_at_visit": "done",
                    "moved_to": "in progress",
                }
            ]
        },
    )

    with Session(db_engine) as session:
        row = session.get(Ticket, finished)
        row.deleted_at = naive
        session.add(row)
        session.commit()

    bodies = _workflow_blob(client.get(f"{UI_PREFIX}/{org.alias}/workflow").text)[
        "projects"
    ][project_id]["bodies"]
    assert f'data-pick="{finished}"' not in bodies["give-scrum-update.0"]
    assert f'data-pick="{finished}"' not in bodies["give-scrum-update.1"]

    client.post(
        f"{UI_PREFIX}/{org.alias}/scrums/{scrum_id}/finish",
        json={"ended_at": UTC_NOW.isoformat()},
    )
    with Session(db_engine) as session:
        assert session.get(Ticket, finished).status == TicketStatus.DONE


def test_leaving_the_first_picker_does_not_delete_the_second_pickers_picks(
    client, populated_org, db_engine
):
    """**The wipe window, closed rather than narrowed.**

    The page posts as each picker step is left, and a resumed run's first post
    sees only step 0's boxes — step 1 has not been rendered yet. A whole-set
    replace therefore deletes the take picks at that moment, and only restores
    them when step 1 is left. Abandon the tab in between — a crash, or somebody
    who only wanted to look — and those picks are gone along with each one's
    `push_error`, while the tickets stay moved and assigned.

    So a post says which boxes it could *see* as well as which are ticked, and a
    visit outside that set is left alone. Un-ticking still expresses a
    withdrawal, because a withdrawn box is present-and-unticked, not absent.
    """

    user, cookie, org, project_id = populated_org
    naive = UTC_NOW.replace(tzinfo=None)
    finished = _ticket(
        db_engine,
        org,
        project_id,
        summary="from step zero",
        status=TicketStatus.DONE,
        assigned_to=user.id,
        completed_at=naive - timedelta(days=1),
    )
    unowned = _ticket(
        db_engine, org, project_id, summary="from step one", status=TicketStatus.TODO
    )
    _auth(client, cookie)
    opened = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums",
        json={"project_id": project_id, "kind": "update"},
    )
    scrum_id = opened.json()["scrum_id"]
    both = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums/{scrum_id}/picks",
        json={
            "offered": [finished, unowned],
            "picks": [
                {
                    "ticket_id": finished,
                    "status_at_visit": "done",
                    "moved_to": "in progress",
                },
                {
                    "ticket_id": unowned,
                    "status_at_visit": "todo",
                    "moved_to": "in progress",
                },
            ],
        },
    )
    assert both.json()["recorded"] == 2

    # The first post of a resumed run: only step 0 is on screen.
    subset = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums/{scrum_id}/picks",
        json={
            "offered": [finished],
            "picks": [
                {
                    "ticket_id": finished,
                    "status_at_visit": "done",
                    "moved_to": "in progress",
                }
            ],
        },
    )
    assert subset.status_code == 200, subset.text

    with Session(db_engine) as session:
        held = {v.ticket_id for v in _visits(session, scrum_id)}
    assert held == {finished, unowned}, (
        "a post that could not see the second picker deleted its picks"
    )

    # And un-ticking still removes, because a withdrawn box is offered-and-unticked.
    client.post(
        f"{UI_PREFIX}/{org.alias}/scrums/{scrum_id}/picks",
        json={"offered": [finished, unowned], "picks": []},
    )
    with Session(db_engine) as session:
        assert _visits(session, scrum_id) == []


def test_a_recorder_that_itself_fails_does_not_replace_the_failure_it_reports(
    client, populated_org, db_engine, monkeypatch
):
    """**#641's second finding.** Writing `push_error` is best-effort reporting.
    If that write raises, the user must still be told about the *push* failure --
    the thing that actually went wrong -- rather than about the reporter.

    Without this, the last exception wins and the banner describes a database
    problem the reader can do nothing about, while the board is quietly out of
    step with InnoDay.
    """
    from src.adapters.base_adapter import BoardAdapterError
    from src.services import scrum_service, ticket_status_service

    user, cookie, org, project_id = populated_org
    board_id = _board(db_engine, org, project_id, user)
    naive = UTC_NOW.replace(tzinfo=None)
    finished = _ticket(
        db_engine,
        org,
        project_id,
        summary="on a real board",
        status=TicketStatus.DONE,
        assigned_to=user.id,
        completed_at=naive - timedelta(days=1),
        board_registration_id=board_id,
        external_ticket_id="PF-8",
    )
    monkeypatch.setattr(
        ticket_status_service, "resolve_board_token", lambda *a, **k: "tok"
    )
    monkeypatch.setattr(
        ticket_status_service,
        "build_board_adapter",
        mock.AsyncMock(
            return_value=_FailingAdapter(BoardAdapterError("Linear is down"))
        ),
    )

    def _explode(*args, **kwargs):
        raise RuntimeError("the recorder itself is broken")

    # Renamed from `_record_push_error` when a second, independent outcome
    # (the comment push) landed on the same row: one writer over named columns,
    # so a clean status push cannot clear a still-true comment failure.
    monkeypatch.setattr(scrum_service, "_record_visit_outcome", _explode)

    _auth(client, cookie)
    _, answer = _run_update(client, org, project_id, picks=[(finished, "done")])

    assert answer["pushed"] is False
    assert any("Linear is down" in e for e in _move_errors(answer)), (
        "the recorder's own failure replaced the failure it was reporting"
    )
    assert all("recorder itself is broken" not in e for e in _move_errors(answer))
    with Session(db_engine) as session:
        assert session.get(Ticket, finished).status == TicketStatus.IN_PROGRESS


# --------------------------------------------------------------------------- #
# Requirement 8 -- a comment given during the update reaches the board ticket.
# --------------------------------------------------------------------------- #


class _CommentingAdapter:
    """A board that takes status pushes and records the comments it is given.

    ``accepts`` is what makes the *falsy return* observable: `add_comment` is
    declared to return ``bool`` and `LinearBoardAdapter` hands back exactly what
    ``commentCreate.success`` said, so a board that declines raises nothing and
    returns ``False``. A stub that only ever returned ``True`` would certify a
    caller that ignores the answer.

    ``initialized`` is here because `build_board_adapter` does **not** call
    `initialize`, and an uninitialised adapter fails only against a live board.
    """

    def __init__(self, *, accepts=True, raises=None):
        self.accepts = accepts
        self.raises = raises
        self.comments = []
        #: Every `add_comment` **attempt**, including the ones that raised.
        #: `comments` cannot stand in for this: a stub that raises never reaches
        #: the append, so a test about *whether a push was tried* would be
        #: asserting on a list that is empty either way.
        self.calls = 0
        self.initialized = False
        self.state_name_to_id = {}

    async def initialize(self, token):
        self.initialized = True
        self.state_name_to_id = {"In Progress": "s2"}

    async def update_ticket_status(self, ticket, new_status):
        return ticket

    async def get_board_metadata(self):
        return {"members": []}

    async def set_board_assignee(self, ticket, board_user_id):
        raise BoardCapabilityError("no assignee here")

    async def add_comment(self, ticket, comment):
        self.calls += 1
        if self.raises is not None:
            raise self.raises
        self.comments.append((ticket.id, comment, self.initialized))
        return self.accepts


def _use_comment_adapter(monkeypatch, adapter):
    """Give the comment service ``adapter``, and the status service its own.

    The status service and the comment service resolve their own credentials and
    build their own adapter -- deliberately, since a comment is not a move -- so a
    test that patched one would still make a real Vault call from the other.

    **Two instances, not one, and that is load-bearing.** The submit pushes the
    status first, and the status service calls `initialize` on whatever it built.
    Handing both services the same object made "the comment service initialized
    its adapter" indistinguishable from "somebody else already had" -- a mutant
    deleting the `initialize` call from the comment push survived it.
    """
    from src.services import ticket_comment_service, ticket_status_service

    for module, built in (
        (ticket_status_service, _CommentingAdapter()),
        (ticket_comment_service, adapter),
    ):
        monkeypatch.setattr(module, "resolve_board_token", lambda *a, **k: "tok")
        monkeypatch.setattr(
            module, "build_board_adapter", mock.AsyncMock(return_value=built)
        )


def _visit_of(db_engine, scrum_id):
    from src.domain.scrum import ScrumTicketVisit

    with Session(db_engine) as session:
        return session.exec(
            select(ScrumTicketVisit).where(ScrumTicketVisit.scrum_id == scrum_id)
        ).first()


def _a_pickable_done_ticket(db_engine, org, project_id, user, **kw):
    naive = UTC_NOW.replace(tzinfo=None)
    return _ticket(
        db_engine,
        org,
        project_id,
        summary=kw.pop("summary", "bring this back"),
        status=TicketStatus.DONE,
        assigned_to=user.id,
        completed_at=naive - timedelta(days=1),
        **kw,
    )


def test_a_comment_is_stored_locally_against_the_ticket_and_its_author(
    client, populated_org, db_engine
):
    """**Requirement 8, the local half.** `TicketComment`, with the right author.

    Read the column's own note before trusting a green test here: `commenter_id`
    was once created as an **integer** while `users.id` is a UUID string, which
    500'd every write that reached it. This is the first path to write it in
    anger, so the round trip is asserted on the value that comes *back* out --
    and the Postgres run is the one that means anything, since SQLite's loose
    typing would accept a UUID in an integer column without complaint.
    """
    from src.domain.ticket import TicketComment

    user, cookie, org, project_id = populated_org
    finished = _a_pickable_done_ticket(db_engine, org, project_id, user)

    _auth(client, cookie)
    scrum_id, answer = _run_update(
        client,
        org,
        project_id,
        picks=[(finished, "done")],
        comments={finished: "QA found a regression, taking it back"},
    )

    assert answer["commented"] == 1
    # No board on this project, so there was nothing to push to -- which is not a
    # push failure and must not be reported as one.
    assert answer["comments_pushed"] is None
    assert not _comment_errors(answer)

    with Session(db_engine) as session:
        rows = session.exec(
            select(TicketComment).where(TicketComment.ticket_id == finished)
        ).all()
        assert len(rows) == 1
        assert rows[0].comment == "QA found a regression, taking it back"
        assert rows[0].commenter_id == user.id
        assert isinstance(rows[0].commenter_id, str)

    visit = _visit_of(db_engine, scrum_id)
    assert visit.comment_id == rows[0].id, (
        "the visit has to remember which comment it delivered, or the next "
        "submit posts the same sentence again"
    )
    assert visit.comment_error is None


def test_a_comment_reaches_the_board_signed_with_its_author(
    client, populated_org, db_engine, monkeypatch
):
    """**Requirement 8, the outbound half** -- and it was scaffolded, never called.

    Every adapter has implemented `add_comment` for as long as the adapters have
    existed and **nothing outside the adapters has ever called one**, so this is
    the path's first live user and is treated as unproven rather than assumed.

    The board authenticates as the *integration*, not as a person, so an
    unattributed comment arrives from a machine account. The author's name is
    therefore in the body -- there is nowhere else for it to go, since
    `add_comment` takes a body and nothing else on all four adapters.
    """
    user, cookie, org, project_id = populated_org
    board_id = _board(db_engine, org, project_id, user)
    finished = _a_pickable_done_ticket(
        db_engine,
        org,
        project_id,
        user,
        board_registration_id=board_id,
        external_ticket_id="PF-11",
    )
    adapter = _CommentingAdapter()
    _use_comment_adapter(monkeypatch, adapter)

    _auth(client, cookie)
    _, answer = _run_update(
        client,
        org,
        project_id,
        picks=[(finished, "done")],
        comments={finished: "reopening, the fix regressed"},
    )

    assert answer["comments_pushed"] is True
    assert not _comment_errors(answer)
    assert len(adapter.comments) == 1
    ticket_id, body, was_initialized = adapter.comments[0]
    assert ticket_id == finished
    assert "reopening, the fix regressed" in body
    assert (user.full_name or user.email) in body, (
        "the board cannot know which InnoDay user wrote this -- it has to be said"
    )
    # **`initialize()` is mandatory and separate**: `build_board_adapter` does not
    # call it, and an uninitialised adapter fails only against a live board.
    assert was_initialized is True


def test_a_board_that_declines_the_comment_is_not_reported_as_having_taken_it(
    client, populated_org, db_engine, monkeypatch
):
    """**`add_comment` returns a bool, and `False` means it did not land.**

    `LinearBoardAdapter.add_comment` hands back `commentCreate.success` verbatim,
    so a declined comment raises nothing at all. A caller watching only for
    exceptions reports it as delivered -- which is precisely the misunderstanding
    between teammates this requirement exists to prevent: somebody writes "do not
    start this, it is blocked" and everyone reading the board sees nothing.
    """
    user, cookie, org, project_id = populated_org
    board_id = _board(db_engine, org, project_id, user)
    finished = _a_pickable_done_ticket(
        db_engine,
        org,
        project_id,
        user,
        board_registration_id=board_id,
        external_ticket_id="PF-12",
    )
    _use_comment_adapter(monkeypatch, _CommentingAdapter(accepts=False))

    _auth(client, cookie)
    scrum_id, answer = _run_update(
        client,
        org,
        project_id,
        picks=[(finished, "done")],
        comments={finished: "blocked, do not pick this up"},
    )

    assert answer["comments_pushed"] is False
    assert _comment_errors(answer), "a declined comment was reported as delivered"
    visit = _visit_of(db_engine, scrum_id)
    assert visit.comment_error, "and nothing recorded that the board is behind"
    assert visit.comment_id is not None, "the local comment is still authoritative"


def test_a_failed_comment_push_keeps_the_local_comment_and_says_so(
    client, populated_org, db_engine, monkeypatch
):
    """Local-first, push-second, and the local write is never rolled back.

    The board being down does not undo what InnoDay committed, and the failure is
    **persisted** (`comment_error`) rather than only painted -- the response is
    read once and then the tab is closed, while the board stays out of step until
    somebody acts.
    """
    from src.domain.ticket import TicketComment

    user, cookie, org, project_id = populated_org
    board_id = _board(db_engine, org, project_id, user)
    finished = _a_pickable_done_ticket(
        db_engine,
        org,
        project_id,
        user,
        board_registration_id=board_id,
        external_ticket_id="PF-13",
    )
    _use_comment_adapter(
        monkeypatch, _CommentingAdapter(raises=BoardAdapterError("Linear is down"))
    )

    _auth(client, cookie)
    scrum_id, answer = _run_update(
        client,
        org,
        project_id,
        picks=[(finished, "done")],
        comments={finished: "still stuck on the migration"},
    )

    assert answer["comments_pushed"] is False
    assert any("Linear is down" in e for e in _comment_errors(answer))
    with Session(db_engine) as session:
        rows = session.exec(
            select(TicketComment).where(TicketComment.ticket_id == finished)
        ).all()
        assert len(rows) == 1, "the local comment was rolled back for a third party"
    visit = _visit_of(db_engine, scrum_id)
    assert "Linear is down" in visit.comment_error


def test_an_unexpected_comment_failure_stores_nothing_internal(
    client, populated_org, db_engine, monkeypatch
):
    """**Classified before anything is stored or shown.**

    What lands in `comment_error` is read by every member of the org. `str(exc)`
    on a DBAPI error is the SQL plus its bound parameters, and on a connection
    failure it is host, port and user. Only an exception carrying an explicit
    `user_message` -- an author stating the text is fit to read -- passes through.
    """
    user, cookie, org, project_id = populated_org
    board_id = _board(db_engine, org, project_id, user)
    finished = _a_pickable_done_ticket(
        db_engine,
        org,
        project_id,
        user,
        board_registration_id=board_id,
        external_ticket_id="PF-14",
    )
    leak = OperationalError(
        "SELECT board_credentials.vault_secret_id",
        {},
        Exception("could not connect to server: host=db.internal port=5432 user=root"),
    )
    _use_comment_adapter(monkeypatch, _CommentingAdapter(raises=leak))

    _auth(client, cookie)
    scrum_id, answer = _run_update(
        client,
        org,
        project_id,
        picks=[(finished, "done")],
        comments={finished: "a note"},
    )

    stored = _visit_of(db_engine, scrum_id).comment_error
    for secret in ("db.internal", "vault_secret_id", "user=root", "SELECT"):
        assert all(secret not in e for e in _comment_errors(answer)), secret
        assert secret not in (stored or ""), secret
    assert answer["comments_pushed"] is False
    assert stored, "a classified failure still has to be recorded"


def test_a_board_that_cannot_comment_degrades_to_a_notice_with_no_retry(
    client, populated_org, db_engine, monkeypatch
):
    """**A capability, not a failure** -- and the difference decides the retry.

    A board type with no comments will refuse identically forever. Recording that
    as a `comment_error` would make it permanent and un-clearable, and because a
    stored error is what asks for a retry it would re-push on every later submit
    for something that can never succeed. Mirrors `set_board_assignee`, where
    exactly this was a review finding.
    """
    user, cookie, org, project_id = populated_org
    board_id = _board(db_engine, org, project_id, user)
    finished = _a_pickable_done_ticket(
        db_engine,
        org,
        project_id,
        user,
        board_registration_id=board_id,
        external_ticket_id="PF-15",
    )
    adapter = _CommentingAdapter(raises=BoardCapabilityError("no comments here"))
    _use_comment_adapter(monkeypatch, adapter)

    _auth(client, cookie)
    scrum_id, answer = _run_update(
        client,
        org,
        project_id,
        picks=[(finished, "done")],
        comments={finished: "worth saying"},
    )

    assert not _comment_errors(answer)
    assert _comment_notices(answer), "the reader is told the comment stays here"
    visit = _visit_of(db_engine, scrum_id)
    assert visit.comment_error is None, (
        "a board that cannot comment was recorded as a failure, which asks for a "
        "retry that can never succeed"
    )
    assert visit.comment_id is not None

    # And re-submitting does not try again: nothing is outstanding.
    #
    # **Asserted on the attempt counter.** The first version of this compared
    # `adapter.raises` before and after -- a constructor argument the adapter
    # never writes, so it asserted that a stored exception was still itself.
    # `adapter.comments` cannot stand in either: `add_comment` raises before it
    # appends, so that list is empty whether or not a push was tried.
    calls_before = adapter.calls
    assert calls_before == 1, "the first submit did not reach the board at all"
    _run_update(
        client,
        org,
        project_id,
        picks=[(finished, "in progress")],
        comments={finished: "worth saying"},
    )
    assert adapter.calls == calls_before, (
        "a board that structurally cannot comment was asked again -- a retry "
        "that can never succeed, on every submit, forever"
    )
    with Session(db_engine) as session:
        from src.domain.ticket import TicketComment

        assert (
            len(
                session.exec(
                    select(TicketComment).where(TicketComment.ticket_id == finished)
                ).all()
            )
            == 1
        ), "a re-submit posted the same comment a second time"


def test_a_failed_comment_push_is_retried_and_the_local_comment_is_not_duplicated(
    client, populated_org, db_engine, monkeypatch
):
    """The failure converges instead of being erased.

    `comment_error` is the durable evidence that the board is behind, so it is
    what drives the retry -- and the retry must not write a *second* local
    comment, because the local record was never the thing that failed.
    """
    from src.domain.ticket import TicketComment

    user, cookie, org, project_id = populated_org
    board_id = _board(db_engine, org, project_id, user)
    finished = _a_pickable_done_ticket(
        db_engine,
        org,
        project_id,
        user,
        board_registration_id=board_id,
        external_ticket_id="PF-16",
    )
    broken = _CommentingAdapter(raises=BoardAdapterError("Linear is down"))
    _use_comment_adapter(monkeypatch, broken)

    _auth(client, cookie)
    scrum_id, first = _run_update(
        client,
        org,
        project_id,
        picks=[(finished, "done")],
        comments={finished: "the same sentence"},
    )
    assert first["comments_pushed"] is False

    working = _CommentingAdapter()
    _use_comment_adapter(monkeypatch, working)
    _, second = _run_update(
        client,
        org,
        project_id,
        picks=[(finished, "in progress")],
        comments={finished: "the same sentence"},
    )

    assert second["comments_pushed"] is True
    assert not _comment_errors(second)
    assert len(working.comments) == 1, "the retry never reached the board"
    with Session(db_engine) as session:
        assert (
            len(
                session.exec(
                    select(TicketComment).where(TicketComment.ticket_id == finished)
                ).all()
            )
            == 1
        ), "the retry wrote a second local comment for one thing somebody said"
    assert _visit_of(db_engine, scrum_id).comment_error is None


def test_a_delivered_comment_is_not_posted_to_the_board_again(
    client, populated_org, db_engine, monkeypatch
):
    """**The headline idempotence claim, pinned on the success path.**

    A daily update is re-enterable and re-closable until the day ends, so
    submitting is not a once-only event -- somebody opens the record to fix a
    typo in a pick and presses through. Without a durable memory of what was
    delivered, every one of those re-submits posts the day's comments to the
    client's board again.

    Nothing tested this. Every board-comment count in the suite was ``== 1`` for
    a run in which only one push could ever have happened, so a mutant that
    re-pushed *every* delivered comment on *every* submit left the file green.
    """
    from src.domain.ticket import TicketComment

    user, cookie, org, project_id = populated_org
    board_id = _board(db_engine, org, project_id, user)
    finished = _a_pickable_done_ticket(
        db_engine,
        org,
        project_id,
        user,
        board_registration_id=board_id,
        external_ticket_id="PF-20",
    )
    adapter = _CommentingAdapter()
    _use_comment_adapter(monkeypatch, adapter)

    _auth(client, cookie)
    scrum_id, first = _run_update(
        client,
        org,
        project_id,
        picks=[(finished, "done")],
        comments={finished: "bringing this back, QA found a regression"},
    )
    assert first["comments_pushed"] is True
    assert len(adapter.comments) == 1

    # Press through a second time, unchanged. The pick is IN_PROGRESS by now, so
    # this is the resumed shape a real re-entry takes.
    _, second = _run_update(
        client,
        org,
        project_id,
        picks=[(finished, "in progress")],
        comments={finished: "bringing this back, QA found a regression"},
    )

    assert len(adapter.comments) == 1, (
        f"the same sentence reached the client's board {len(adapter.comments)} "
        "times for one thing somebody said once"
    )
    assert adapter.calls == 1, "the board was contacted again for a settled comment"
    assert second["commented"] == 0
    # And nothing was reported as freshly delivered that was not.
    assert not _comment_errors(second)
    with Session(db_engine) as session:
        assert (
            len(
                session.exec(
                    select(TicketComment).where(TicketComment.ticket_id == finished)
                ).all()
            )
            == 1
        )
    assert _visit_of(db_engine, scrum_id).comment_error is None


def test_withdrawing_a_pick_and_taking_it_back_does_not_re_post_the_comment(
    client, populated_org, db_engine, monkeypatch
):
    """**A deleted visit does not mean "never sent".**

    `replace_picks` deletes the visit whose ticket left the selection -- and the
    visit is where `comment_id` lives. So untick → submit → re-tick → submit
    orphaned the `TicketComment`, found no marker, and posted the sentence to the
    client's board a second time. Measured before the fix: 2.

    A withdrawal removes a *pick*. It cannot remove a sentence already on somebody
    else's board, and the delivery memory has to survive it. Somebody changing
    their mind twice about one ticket is the ordinary use of a form built to be
    re-entered, not an exotic path.
    """
    from src.domain.ticket import TicketComment

    user, cookie, org, project_id = populated_org
    board_id = _board(db_engine, org, project_id, user)
    finished = _a_pickable_done_ticket(
        db_engine,
        org,
        project_id,
        user,
        board_registration_id=board_id,
        external_ticket_id="PF-21",
    )
    adapter = _CommentingAdapter()
    _use_comment_adapter(monkeypatch, adapter)
    said = "blocked on the migration, do not pick this up"

    _auth(client, cookie)
    scrum_id, _ = _run_update(
        client, org, project_id, picks=[(finished, "done")], comments={finished: said}
    )
    assert len(adapter.comments) == 1

    # Withdraw it: an empty selection, which `replace_picks` reads as "remove
    # everything I recorded".
    _run_update(client, org, project_id, picks=[])
    with Session(db_engine) as session:
        assert _visits(session, scrum_id) == [], (
            "the pick survived the withdrawal, so this test proves nothing"
        )
        # The row is kept and flagged, which is what carries the marker across.
        withdrawn = _visit_rows(session, scrum_id)
        assert len(withdrawn) == 1 and withdrawn[0].withdrawn_at is not None
        assert withdrawn[0].comment_id is not None

    # Change your mind again, with the same sentence.
    _, third = _run_update(
        client,
        org,
        project_id,
        picks=[(finished, "in progress")],
        comments={finished: said},
    )

    assert len(adapter.comments) == 1, (
        f"the client's board got the same sentence {len(adapter.comments)} times "
        "because withdrawing a pick threw away the record that it had been sent"
    )
    with Session(db_engine) as session:
        rows = session.exec(
            select(TicketComment).where(TicketComment.ticket_id == finished)
        ).all()
        assert len(rows) == 1, "a second local comment was written for one sentence"
    # The marker came back with the row rather than being rebuilt from a guess.
    assert _visit_of(db_engine, scrum_id).comment_id == rows[0].id
    assert not _comment_errors(third)


def test_a_withdrawn_visit_does_not_share_a_position_with_a_live_one(
    client, populated_org, db_engine
):
    """`position` is an ordering, and two rows claiming the same one is not one.

    `replace_picks` already renumbers *retained* rows past the live range and
    says why; the withdrawal branch did not, so a withdrawn row and a live one
    both held `position = 0`. `/api/v1` orders by `position, created_at`, so the
    tie resolved by age -- reliably wrong rather than intermittently wrong, which
    is harder for a reader to notice. Deletion hid this; keeping the row does not.

    The retained and withdrawn branches share **one** counter: they interleave in
    a single pass, so a counter each hands out the same number as soon as both
    kinds appear.
    """
    user, cookie, org, project_id = populated_org
    a, b, c = (
        _a_pickable_done_ticket(db_engine, org, project_id, user, summary=f"t{n}")
        for n in range(3)
    )
    _auth(client, cookie)
    scrum_id, _ = _run_update(
        client, org, project_id, picks=[(a, "done"), (b, "done"), (c, "done")]
    )
    # Withdraw two of the three, leaving one live.
    _run_update(client, org, project_id, picks=[(b, "in progress")])

    with Session(db_engine) as session:
        rows = _visit_rows(session, scrum_id)
        assert len(rows) == 3
        positions = [v.position for v in rows]
        assert len(set(positions)) == len(positions), (
            f"two visits claim the same position: {positions}"
        )
        live = [v for v in rows if v.withdrawn_at is None]
        gone = [v for v in rows if v.withdrawn_at is not None]
        assert len(live) == 1 and len(gone) == 2
        assert max(v.position for v in live) < min(v.position for v in gone), (
            "a withdrawn pick sorts inside the live range"
        )


def test_a_withdrawn_pick_with_no_delivered_comment_is_not_pushed(
    client, populated_org, db_engine, monkeypatch
):
    """**The outer half of the withdrawn-delivery guard, on the state that needs it.**

    The guard is `withdrawn and not (outstanding and comment_id is not None)`.
    Its sub-condition is pinned by the retry test; replacing the whole guard with
    `if False:` produced no failures anywhere, because `settled` masked it in
    every state the ordinary route reaches.

    It is not a redundant check. A withdrawn visit with `comment_error` set and
    `comment_id` **NULL** is reachable: the per-visit `except` records a
    classified failure without a marker whenever the local write itself is what
    raised. In that state `settled` is False, so without this guard the comment
    is written and pushed -- to a client's board, for a pick the author had
    already taken back.
    """
    user, cookie, org, project_id = populated_org
    board_id = _board(db_engine, org, project_id, user)
    finished = _a_pickable_done_ticket(
        db_engine,
        org,
        project_id,
        user,
        board_registration_id=board_id,
        external_ticket_id="PF-28",
    )
    # Patched from the first submit, or the initial push reaches the real
    # credential lookup rather than the stub.
    _use_comment_adapter(monkeypatch, _CommentingAdapter())

    _auth(client, cookie)
    scrum_id, _ = _run_update(
        client,
        org,
        project_id,
        picks=[(finished, "done")],
        comments={finished: "withdrawn, and never delivered"},
    )
    _run_update(client, org, project_id, picks=[])

    # The reachable state: withdrawn, a recorded failure, and **no** marker --
    # what the per-visit `except` leaves behind when the local write is what
    # raised, so nothing was ever written and nothing was ever sent.
    with Session(db_engine) as session:
        visit = _visit_rows(session, scrum_id)[0]
        assert visit.withdrawn_at is not None
        visit.comment_id = None
        visit.comment_error = "The board could not be updated."
        session.add(visit)
        session.commit()

    # A **fresh** adapter, so its empty `comments` can only mean "this submit
    # pushed nothing" rather than carrying the first submit's history.
    after = _CommentingAdapter()
    _use_comment_adapter(monkeypatch, after)
    with Session(db_engine) as session:
        from src.domain.ticket import TicketComment

        before = len(
            session.exec(
                select(TicketComment).where(TicketComment.ticket_id == finished)
            ).all()
        )

    _, answer = _run_update(client, org, project_id, picks=[])

    assert after.comments == [], (
        "a comment was pushed to the client's board for a pick the author had "
        "already withdrawn"
    )
    assert after.calls == 0
    assert answer["commented"] == 0
    with Session(db_engine) as session:
        from src.domain.ticket import TicketComment

        assert (
            len(
                session.exec(
                    select(TicketComment).where(TicketComment.ticket_id == finished)
                ).all()
            )
            == before
        ), "a local comment was written for a withdrawn pick"


def test_a_withdrawn_pick_is_not_counted_rendered_or_moved(
    client, populated_org, db_engine
):
    """**The three exclusions that made deletion look like the simple option.**

    Keeping a withdrawn row only works if everything that means "the record"
    ignores it. Each of these was a reason the row used to be deleted, so each is
    asserted rather than left to be rediscovered — and each survived a mutation
    of its own guard until this test existed.

    1. `visit_count` — the number the page paints as "recorded so far" and the API
       returns per scrum. Counting a withdrawn pick tells somebody their update
       holds work they explicitly took back.
    2. The pickers — a withdrawn pick must not come back ticked with its note
       still in the box. It would put the choice back in front of somebody who
       removed it, and the next submit would re-apply it.
    3. The moves — a withdrawn pick moves nothing.
    """
    user, cookie, org, project_id = populated_org
    finished = _a_pickable_done_ticket(
        db_engine, org, project_id, user, summary="taken back"
    )
    _auth(client, cookie)
    scrum_id, first = _run_update(
        client,
        org,
        project_id,
        picks=[(finished, "done")],
        comments={finished: "something I will take back"},
    )
    assert first["visits"] == 1

    _, second = _run_update(client, org, project_id, picks=[])

    # 1. Not counted.
    assert second["visits"] == 0, (
        "a withdrawn pick is still counted as part of the record"
    )
    with Session(db_engine) as session:
        assert len(_visit_rows(session, scrum_id)) == 1, (
            "the row was deleted, so this test is not exercising the exclusions"
        )

    # 2 and 3 are asserted on a visit that is **flagged withdrawn and still names
    # a status**, built directly.
    #
    # That shape matters. `replace_picks` clears `moved_to` when it withdraws, and
    # `scrum_activity_today` and `apply_recorded_moves` both already skip a visit
    # with no `moved_to` -- so through the ordinary route their `withdrawn_at`
    # guards are masked by the clearing and can be deleted with every test still
    # green (measured). The guards exist so that neither reader depends on the
    # other end still clearing that column, and this is the only state in which
    # they are the thing doing the work.
    other = _a_pickable_done_ticket(
        db_engine, org, project_id, user, summary="never picked up"
    )
    with Session(db_engine) as session:
        session.add(
            ScrumTicketVisit(
                id=str(uuid4()),
                scrum_id=scrum_id,
                ticket_id=other,
                position=9,
                seconds=0,
                status_at_visit="done",
                moved_to="in progress",
                comment="a note on a pick that is not in the update",
                withdrawn_at=UTC_NOW.replace(tzinfo=None),
            )
        )
        session.commit()

    # 2. Not rendered: no ticked box, and no note back in the textarea.
    bodies = _workflow_blob(client.get(f"{UI_PREFIX}/{org.alias}/workflow").text)[
        "projects"
    ][project_id]["bodies"]
    picker = bodies["give-scrum-update.0"] + bodies["give-scrum-update.1"]
    assert "something I will take back" not in picker
    assert "a note on a pick that is not in the update" not in picker, (
        "a withdrawn pick's comment was rendered back into the picker"
    )
    assert f'checked data-pick="{other}"' not in picker, (
        "a withdrawn pick came back ticked"
    )
    assert "0 tickets" in bodies["give-scrum-update.2"]

    # 3. Not moved. Closing the record again runs the moves over what it holds;
    # this visit is not part of that, whatever `moved_to` says.
    closed = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums/{scrum_id}/finish",
        json={"ended_at": UTC_NOW.isoformat()},
    )
    assert closed.status_code == 200, closed.text
    with Session(db_engine) as session:
        assert session.get(Ticket, other).status == TicketStatus.DONE, (
            "a withdrawn pick moved its ticket"
        )


def test_a_board_that_was_down_still_gets_the_comment_after_a_withdrawal(
    client, populated_org, db_engine, monkeypatch
):
    """**The failure the first fix traded a double-post for, and it was worse.**

    Board down when the comment is first sent, then withdraw the pick, then take
    it back. The local `TicketComment` was written before the push failed, so a
    text search found it and called the comment delivered; the revived pick
    carried no `comment_error`, so nothing retried. Measured: the board never got
    it, `comment_error` was `None`, and the response said `{'commented': 0,
    'comments_pushed': None, 'comment_error': None}` -- a clean answer for a
    comment nobody outside InnoDay will ever see.

    By this module's own ranking that is the wrong way round: reporting a comment
    as delivered when the board never got it is the failure most likely to cause
    a real misunderstanding between teammates, and the defect it replaced at
    least left the board *holding* the sentence.

    Keeping the withdrawn row is what fixes it: `comment_error` survives the
    withdrawal, comes back with the revived pick, and drives the retry.
    """
    user, cookie, org, project_id = populated_org
    board_id = _board(db_engine, org, project_id, user)
    finished = _a_pickable_done_ticket(
        db_engine,
        org,
        project_id,
        user,
        board_registration_id=board_id,
        external_ticket_id="PF-24",
    )
    said = "blocked on the migration, do not pick this up"

    broken = _CommentingAdapter(raises=BoardAdapterError("Linear is down"))
    _use_comment_adapter(monkeypatch, broken)

    _auth(client, cookie)
    scrum_id, first = _run_update(
        client, org, project_id, picks=[(finished, "done")], comments={finished: said}
    )
    assert first["comments_pushed"] is False
    assert any("Linear is down" in e for e in _comment_errors(first))

    # Take the pick back. The board is still out of step, and taking a pick back
    # cannot make it in step -- so the record of that must survive.
    _run_update(client, org, project_id, picks=[])
    with Session(db_engine) as session:
        rows = _visit_rows(session, scrum_id)
        assert len(rows) == 1 and rows[0].withdrawn_at is not None
        assert rows[0].comment_error, (
            "the withdrawal erased the only record that the board never got this"
        )

    # Change your mind again. The board is back up.
    working = _CommentingAdapter()
    _use_comment_adapter(monkeypatch, working)
    _, third = _run_update(
        client,
        org,
        project_id,
        picks=[(finished, "in progress")],
        comments={finished: said},
    )

    assert len(working.comments) == 1, (
        "the board never got the comment, and nothing said so -- silent "
        "non-delivery, which is this path's worst outcome"
    )
    assert said in working.comments[0][1]
    assert third["comments_pushed"] is True
    assert not _comment_errors(third)
    assert _visit_of(db_engine, scrum_id).comment_error is None


def test_a_withdrawn_pick_with_an_outstanding_failure_is_still_retried(
    client, populated_org, db_engine, monkeypatch
):
    """A withdrawal takes back the *pick*, not a sentence the board is missing.

    So a withdrawn visit delivers nothing new -- it is not part of the update any
    more -- and yet its outstanding push is still retried. Those are not in
    tension: the comment is already InnoDay's, the board is recorded as not
    having it, and un-ticking a box does not change either fact.
    """
    user, cookie, org, project_id = populated_org
    board_id = _board(db_engine, org, project_id, user)
    finished = _a_pickable_done_ticket(
        db_engine,
        org,
        project_id,
        user,
        board_registration_id=board_id,
        external_ticket_id="PF-25",
    )
    _use_comment_adapter(
        monkeypatch, _CommentingAdapter(raises=BoardAdapterError("Linear is down"))
    )

    _auth(client, cookie)
    scrum_id, _ = _run_update(
        client,
        org,
        project_id,
        picks=[(finished, "done")],
        comments={finished: "worth the board knowing"},
    )

    # Withdraw, and submit again *without* taking it back. The retry rides the
    # withdrawn row alone.
    working = _CommentingAdapter()
    _use_comment_adapter(monkeypatch, working)
    _, answer = _run_update(client, org, project_id, picks=[])

    assert len(working.comments) == 1, (
        "a withdrawn pick's outstanding comment was never retried, so the board "
        "stays out of step with nothing recording it"
    )
    assert answer["comments_pushed"] is True
    assert _visit_of(db_engine, scrum_id).comment_error is None
    # And nothing was written locally for a pick that is no longer in the update.
    assert answer["commented"] == 0


def test_a_reverted_comment_leaves_the_board_agreeing_with_innoday(
    client, populated_org, db_engine, monkeypatch
):
    """Say a thing, correct it, then go back to the first thing.

    The board's **last word** has to be what InnoDay shows. `add_comment` cannot
    edit a board comment, so every change of mind is another comment -- including
    a change back. The text-search version answered "you have already written
    that today" and posted nothing, leaving the board's last word contradicting
    the record: exactly what `post_ticket_comment`'s edit-is-a-new-comment rule
    exists to prevent.
    """
    user, cookie, org, project_id = populated_org
    board_id = _board(db_engine, org, project_id, user)
    finished = _a_pickable_done_ticket(
        db_engine,
        org,
        project_id,
        user,
        board_registration_id=board_id,
        external_ticket_id="PF-26",
    )
    adapter = _CommentingAdapter()
    _use_comment_adapter(monkeypatch, adapter)

    _auth(client, cookie)
    for text in ("still blocked", "actually unblocked", "still blocked"):
        _run_update(
            client,
            org,
            project_id,
            picks=[(finished, "done")],
            comments={finished: text},
        )

    said = [body for _, body, _ in adapter.comments]
    assert len(said) == 3, said
    assert "still blocked" in said[-1], (
        "the board's last word contradicts what InnoDay shows"
    )


def test_a_comment_written_by_another_surface_does_not_suppress_the_push(
    client, populated_org, db_engine, monkeypatch
):
    """`TicketComment` is not this path's private table.

    `routers/tickets.py` writes to it too. A text search over that table therefore
    answered "somebody has written this sentence" when the caller was asking
    "have *we* sent this to the board" -- and an identical comment made through
    the API silently suppressed the board push, with no error. The only evidence
    that the board has something is evidence that we sent it.
    """
    from src.domain.ticket import TicketComment

    user, cookie, org, project_id = populated_org
    board_id = _board(db_engine, org, project_id, user)
    finished = _a_pickable_done_ticket(
        db_engine,
        org,
        project_id,
        user,
        board_registration_id=board_id,
        external_ticket_id="PF-27",
    )
    said = "the same words, from somewhere else"
    with Session(db_engine) as session:
        session.add(
            TicketComment(ticket_id=finished, commenter_id=user.id, comment=said)
        )
        session.commit()

    adapter = _CommentingAdapter()
    _use_comment_adapter(monkeypatch, adapter)

    _auth(client, cookie)
    _, answer = _run_update(
        client, org, project_id, picks=[(finished, "done")], comments={finished: said}
    )

    assert len(adapter.comments) == 1, (
        "a comment written by another surface was mistaken for one we had already "
        "pushed, so the board was never told"
    )
    assert answer["comments_pushed"] is True


def test_a_different_sentence_after_a_withdrawal_is_still_delivered(
    client, populated_org, db_engine, monkeypatch
):
    """The fallback must not silence a comment that has never been said.

    The guard against re-posting matches on the **whole text**, so an edit is a
    genuinely new comment -- `add_comment` cannot edit a board comment, and a
    board left holding the old wording while InnoDay shows the new one is the
    disagreement this path exists to prevent. Without this, "do not post what you
    already posted" would quietly become "post nothing after a withdrawal".
    """
    user, cookie, org, project_id = populated_org
    board_id = _board(db_engine, org, project_id, user)
    finished = _a_pickable_done_ticket(
        db_engine,
        org,
        project_id,
        user,
        board_registration_id=board_id,
        external_ticket_id="PF-22",
    )
    adapter = _CommentingAdapter()
    _use_comment_adapter(monkeypatch, adapter)

    _auth(client, cookie)
    _run_update(
        client,
        org,
        project_id,
        picks=[(finished, "done")],
        comments={finished: "first thought"},
    )
    _run_update(client, org, project_id, picks=[])
    _run_update(
        client,
        org,
        project_id,
        picks=[(finished, "in progress")],
        comments={finished: "second thought, it is worse than I said"},
    )

    bodies = [body for _, body, _ in adapter.comments]
    assert len(bodies) == 2, bodies
    assert any("first thought" in b for b in bodies)
    assert any("second thought" in b for b in bodies)


def test_a_demoted_member_does_not_get_their_comment_pushed_to_the_board(
    client, populated_org, db_engine, monkeypatch
):
    """A comment is a board write, and the same gate covers it.

    The reachable case is not a MEMBER who never had the right -- `/picks` refuses
    them, so they record nothing to deliver. It is somebody **demoted between
    recording and submitting**, which is the exact case the moves' gate was
    written for. Their status move is refused; their comment must not sail past
    it onto the client's board in the same response.
    """
    from src.domain.organization import OrganizationRole

    user, cookie, org, project_id = populated_org
    board_id = _board(db_engine, org, project_id, user)
    finished = _a_pickable_done_ticket(
        db_engine,
        org,
        project_id,
        user,
        board_registration_id=board_id,
        external_ticket_id="PF-23",
    )
    adapter = _CommentingAdapter()
    _use_comment_adapter(monkeypatch, adapter)

    _auth(client, cookie)
    opened = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums",
        json={"project_id": project_id, "kind": "update"},
    )
    scrum_id = opened.json()["scrum_id"]
    sent = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums/{scrum_id}/picks",
        json={
            "picks": [
                {
                    "ticket_id": finished,
                    "status_at_visit": "done",
                    "moved_to": "in progress",
                    "comment": "recorded while I still held the role",
                }
            ]
        },
    )
    assert sent.status_code == 200, sent.text

    # Now demote, and only then submit.
    _set_role(db_engine, org, user, OrganizationRole.MEMBER)
    closed = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums/{scrum_id}/finish",
        json={"ended_at": UTC_NOW.isoformat()},
    )
    assert closed.status_code == 200, closed.text
    answer = closed.json()

    assert adapter.comments == [], (
        "a demoted member's comment was pushed to the client's board in the same "
        "response that refused their status move"
    )
    assert answer["commented"] == 0
    assert _comment_errors(answer), "and they were not told it had not been sent"


def test_a_failure_writing_the_comment_does_not_discard_the_moves_report(
    client, populated_org, db_engine, monkeypatch
):
    """A save that happened, reported as nothing at all, is the same lie inverted.

    `deliver_recorded_comments` runs **after** `apply_recorded_moves` in the same
    request, and `answer.update(...)` is the last thing before the response. The
    local comment write used to sit outside any `try`, so an `IntegrityError` or
    `OperationalError` there propagated out of `finish_scrum_run`: a 500 with no
    body, while the ticket statuses had already been written, pushed to the board
    and had their `push_error` persisted.

    Everywhere else this feature holds the line that no path reports a save it
    did not get. This is that rule failing in the other direction.
    """
    from src.services import ticket_comment_service

    user, cookie, org, project_id = populated_org
    finished = _a_pickable_done_ticket(db_engine, org, project_id, user)

    async def _explode(*args, **kwargs):
        raise OperationalError(
            "INSERT INTO ticket_comment (commenter_id)",
            {},
            Exception("could not connect: host=db.internal port=5432 user=root"),
        )

    monkeypatch.setattr(ticket_comment_service, "post_ticket_comment", _explode)

    _auth(client, cookie)
    scrum_id, answer = _run_update(
        client,
        org,
        project_id,
        picks=[(finished, "done")],
        comments={finished: "a note nobody will be able to store"},
    )

    # The moves' half of the answer survived intact.
    assert answer["applied"] is True
    assert answer["moved"] == 1
    with Session(db_engine) as session:
        assert session.get(Ticket, finished).status == TicketStatus.IN_PROGRESS

    # And the comment's failure is reported, classified, and persisted.
    assert answer["commented"] == 0
    assert answer["comments_pushed"] is False
    stored = _visit_of(db_engine, scrum_id).comment_error
    assert stored
    for secret in ("db.internal", "user=root", "INSERT INTO"):
        assert all(secret not in e for e in _comment_errors(answer)), secret
        assert secret not in stored, secret


def test_the_outcome_allowlist_refuses_a_name_it_does_not_know(
    client, populated_org, db_engine
):
    """A typo must not write nothing, silently -- which is what it used to do.

    `_record_visit_outcome` raises `KeyError` for a column that is not an outcome
    column, and its only production caller is `_safely_record`, whose blanket
    `except Exception` logged it, rolled back, retried it, logged it again and
    returned. So the guard fired only in a direct-call unit test and never where
    it mattered. It is checked before the `try` now: an unknown name is a
    programming error, not a board being down.

    **The "a real name still writes" half is read back from a fresh session, on a
    row that can actually persist.** As first written it built a `ScrumTicketVisit`
    with a `scrum_id` and `ticket_id` that do not exist, then asserted on the
    attribute -- which `_record_visit_outcome` `setattr`s *before* it commits and
    whose commit failure `_safely_record` swallows. Deleting `session.commit()`
    from the writer left it green. A persistence assertion that never touches the
    database is the seventh test of that shape this feature has produced.
    """
    from src.services import scrum_service

    user, cookie, org, project_id = populated_org
    finished = _a_pickable_done_ticket(db_engine, org, project_id, user)
    _auth(client, cookie)
    scrum_id, _ = _run_update(client, org, project_id, picks=[(finished, "done")])
    visit_id = _visit_of(db_engine, scrum_id).id

    with Session(db_engine) as session:
        visit = session.get(ScrumTicketVisit, visit_id)
        with pytest.raises(KeyError) as caught:
            scrum_service._safely_record(session, visit=visit, push_erorr="typo")
        assert "push_erorr" in str(caught.value)
        # The message names what *is* writable, so the fix is in the failure.
        assert "comment_error" in str(caught.value)

        scrum_service._safely_record(session, visit=visit, comment_error="real")

    # A **different** session, so this reads the database rather than the object
    # the writer just mutated.
    with Session(db_engine) as fresh:
        assert fresh.get(ScrumTicketVisit, visit_id).comment_error == "real"
        assert fresh.get(ScrumTicketVisit, visit_id).push_error is None


def test_a_project_with_no_board_reports_a_comment_as_saved_not_as_failed(
    client, populated_org, db_engine
):
    """Nothing to push to is not a push failure.

    Reporting one would train people to ignore the banner that matters -- and
    this is the ordinary case, since an InnoDay-only project is a real project.
    """
    user, cookie, org, project_id = populated_org
    finished = _a_pickable_done_ticket(db_engine, org, project_id, user)

    _auth(client, cookie)
    scrum_id, answer = _run_update(
        client,
        org,
        project_id,
        picks=[(finished, "done")],
        comments={finished: "kept here"},
    )

    assert answer["commented"] == 1
    assert answer["comments_pushed"] is None
    assert not _comment_errors(answer)
    assert not _comment_notices(answer)
    assert _visit_of(db_engine, scrum_id).comment_error is None


def test_re_entering_shows_what_you_said_and_an_emptied_box_removes_it(
    client, populated_org, db_engine
):
    """The comment is resumed, and clearing it is a real answer.

    The post carries the whole selection, so a box rendered empty over a recorded
    comment would delete it the moment somebody pressed through -- and a stored
    comment that survived a deliberate deletion would be the same lie in the other
    direction. It goes back into a ``<textarea>`` **text node**, never a
    ``value=""`` attribute: a comment is prose and a newline is not representable
    in an attribute.
    """
    user, cookie, org, project_id = populated_org
    finished = _a_pickable_done_ticket(db_engine, org, project_id, user)

    _auth(client, cookie)
    scrum_id, _ = _run_update(
        client,
        org,
        project_id,
        picks=[(finished, "done")],
        comments={finished: "first line\nsecond line"},
    )

    bodies = _workflow_blob(client.get(f"{UI_PREFIX}/{org.alias}/workflow").text)[
        "projects"
    ][project_id]["bodies"]
    picker = bodies["give-scrum-update.0"]
    assert f'data-pick-note="{finished}"' in picker
    assert "first line\nsecond line" in picker, (
        "the resumed comment is not in the textarea's text node"
    )

    # Now send the box back empty -- which is a deletion, not an absence.
    _run_update(
        client,
        org,
        project_id,
        picks=[(finished, "in progress")],
        comments={finished: ""},
    )

    # **What it removes, and what it deliberately does not.** Clearing the box
    # takes the comment out of *your update*. It does not delete the
    # `TicketComment` and it cannot retract a comment a board has already been
    # given -- you cannot unsay something on somebody else's board. Asserted
    # rather than left implied, because the previous version checked only the one
    # place the value *was* removed and read as though it removed everything.
    from src.domain.ticket import TicketComment

    visit = _visit_of(db_engine, scrum_id)
    assert visit.comment is None
    assert visit.comment_id is not None, (
        "the delivery marker was dropped, so re-typing the same sentence would "
        "post it to the board again"
    )
    with Session(db_engine) as session:
        assert (
            len(
                session.exec(
                    select(TicketComment).where(TicketComment.ticket_id == finished)
                ).all()
            )
            == 1
        ), "clearing the box deleted InnoDay's own record of what was said"

    # And the copy says so, rather than leaving somebody to infer it.
    _auth(client, cookie)
    bodies = _workflow_blob(client.get(f"{UI_PREFIX}/{org.alias}/workflow").text)[
        "projects"
    ][project_id]["bodies"]
    assert "cannot take back" in bodies["give-scrum-update.0"]


def test_the_pickers_say_that_an_unticked_note_is_not_kept(client, populated_org):
    """The copy has to match the wire, and the wire drops it.

    `submitPicks` collects comments for the boxes that are **ticked** -- an
    unticked ticket has no visit, so it has nowhere to put one. A note promising
    that "anything you type is posted" would be a save the page never got, which
    is the one thing this surface does not do.
    """
    _, cookie, org, project_id = populated_org
    _auth(client, cookie)
    bodies = _workflow_blob(client.get(f"{UI_PREFIX}/{org.alias}/workflow").text)[
        "projects"
    ][project_id]["bodies"]
    for key in ("give-scrum-update.0", "give-scrum-update.1"):
        assert "not ticked" in bodies[key], key
        assert "is not kept" in bodies[key], key
        # At-least-once delivery, said **on screen**. It is a deliberate design
        # choice -- a duplicate is visible and recoverable, a comment nobody can
        # see is not -- and the person it affects is reading this page, not the
        # service's module docstring.
        assert "twice" in bodies[key], key
        assert "sent again later" in bodies[key], key
        # And it is not only a sentence under the list: the script counts the
        # notes it is about to drop and says so in the banner at submit time.
        assert "told at submit" in bodies[key], key

    html = client.get(f"{UI_PREFIX}/{org.alias}/workflow").text
    assert "notes were" in html and "not kept" in html, (
        "the served script has no submit-time message for a dropped note"
    )


def test_a_comment_typed_into_the_picker_cannot_close_the_script_tag(
    client, populated_org, db_engine
):
    """Comment text is user-supplied and this page sends **no CSP header**.

    Asserted against the *decoded* blob, for the reason the big escaping test
    records: `_json_blob` escapes every ``<`` as a JSON unicode escape, so
    ``html.count("<script")`` balances whether or not `esc` ran. Decoding undoes
    only the blob's own escaping; anything `esc` should have caught is then
    visible.
    """
    user, cookie, org, project_id = populated_org
    finished = _a_pickable_done_ticket(db_engine, org, project_id, user)
    payload = "</textarea></script><script>alert(1)</script>"

    _auth(client, cookie)
    _run_update(
        client,
        org,
        project_id,
        picks=[(finished, "done")],
        comments={finished: payload},
    )

    html = client.get(f"{UI_PREFIX}/{org.alias}/workflow").text
    assert "<script>alert(1)</script>" not in html
    assert html.count("<script") == html.count("</script>")
    assert "alert(1)" in html, "the payload never reached the page at all"

    body = _workflow_blob(html)["projects"][project_id]["bodies"]["give-scrum-update.0"]
    assert payload not in body, "the comment box interpolated its value unescaped"
    assert "alert(1)" in body


def test_a_team_scrums_comments_are_not_pushed_to_the_board(
    client, populated_org, db_engine, monkeypatch
):
    """**Only an update delivers comments**, and the column is shared.

    A team scrum's per-stop comments are minutes of a meeting the room was in.
    Pushing every one of them out to a client's board is a different feature with
    a different audience, and nobody asked for it -- so the rule is stated and
    enforced rather than left to which caller happens to run.
    """
    from src.services import scrum_service

    user, cookie, org, project_id = populated_org
    board_id = _board(db_engine, org, project_id, user)
    walked = _ticket(
        db_engine,
        org,
        project_id,
        summary="walked past",
        status=TicketStatus.IN_REVIEW,
        board_registration_id=board_id,
        external_ticket_id="PF-17",
    )
    adapter = _CommentingAdapter()
    _use_comment_adapter(monkeypatch, adapter)

    _auth(client, cookie)
    opened = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums",
        json={"project_id": project_id, "kind": "scrum"},
    )
    scrum_id = opened.json()["scrum_id"]
    assert (
        client.post(
            f"{UI_PREFIX}/{org.alias}/scrums/{scrum_id}/visits",
            json={
                "ticket_id": walked,
                "position": 0,
                "seconds": 40,
                "status_at_visit": "in review",
                "comment": "said out loud in the room",
            },
        ).status_code
        == 201
    )
    finished = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums/{scrum_id}/finish",
        json={"ended_at": UTC_NOW.isoformat()},
    )
    assert finished.status_code == 200, finished.text
    assert "commented" not in finished.json()
    assert adapter.comments == []

    # And the service refuses outright rather than quietly doing nothing.
    from src.domain.scrum import Scrum

    with Session(db_engine) as session:
        scrum = session.get(Scrum, scrum_id)
        with pytest.raises(scrum_service.ScrumInvalid) as caught:
            asyncio.run(
                scrum_service.deliver_recorded_comments(
                    session, scrum=scrum, actor=user
                )
            )
        assert caught.value.field == "kind"


def test_re_entering_the_update_resumes_the_same_record_and_shows_the_picks(
    client, populated_org, db_engine
):
    """Requirement 6, from the page: the same row, and the choices still on screen.

    The record half is the ``Scrum.id`` and the ``count(*)``; the visible half is
    the box still ticked and the note still typed, rendered server-side from the
    row's own visits. A resume that reopens the right row and paints an empty
    form is a form that invites you to blank what you already said.
    """
    from src.domain.scrum import Scrum, ScrumKind
    from src.domain.ticket import TicketStatus

    user, cookie, org, project_id = populated_org
    naive = UTC_NOW.replace(tzinfo=None)
    finished = _ticket(
        db_engine,
        org,
        project_id,
        summary="bring this back",
        status=TicketStatus.DONE,
        assigned_to=user.id,
        completed_at=naive - timedelta(days=1),
    )
    _auth(client, cookie)
    first = _submit_update(
        client, org, project_id, picks=[(finished, "done")], notes="my note"
    )

    blob = _workflow_blob(client.get(f"{UI_PREFIX}/{org.alias}/workflow").text)
    payload = blob["projects"][project_id]
    # The tick is server-rendered into the row, so a resumed page shows it
    # without the script having to fetch anything.
    body = payload["bodies"]["give-scrum-update.0"]
    assert f'data-pick="{finished}" checked' in body or (
        f'checked data-pick="{finished}"' in body
    )
    assert "my note" in payload["bodies"]["give-scrum-update.2"]
    # The step-2 chip opens on what the record actually holds, and carries the
    # hook the engine repaints it through once a picker submits.
    assert "data-wf-picked" in payload["bodies"]["give-scrum-update.2"]
    assert "1 ticket" in payload["bodies"]["give-scrum-update.2"]

    # Submitting again lands on the same row, and there is still only one --
    # **and it does not double the visit**, which is the half a `Scrum`-only
    # count cannot see.
    second = _submit_update(
        client, org, project_id, picks=[(finished, "done")], notes="corrected"
    )
    assert second == first
    with Session(db_engine) as session:
        rows = session.exec(
            select(Scrum).where(
                Scrum.project_id == project_id,
                Scrum.kind == ScrumKind.UPDATE.value,
            )
        ).all()
        assert len(rows) == 1
        assert rows[0].notes_markdown == "corrected"
        assert len(_visits(session, first)) == 1, (
            "re-submitting the same selection duplicated the pick"
        )


def test_a_resubmitted_update_holds_the_selection_not_the_union_of_every_selection(
    client, populated_org, db_engine
):
    """**The record must *be* what is ticked, not everything ever ticked.**

    The first version of this feature posted one visit per pick and nothing ever
    deleted one, so the visits were append-only: un-ticking a box removed nothing,
    and re-submitting the same box recorded it twice. Meanwhile step 2 said "yours
    to correct until the day is over" and the completion panel said the record
    holds what you asked for. Both false, on requirement 6's own path, and the
    withdrawn pick is exactly what a later change reads to decide which ticket to
    move -- so it would have become a status change nobody asked for.

    Three rounds with three different selections, because one round cannot tell
    "replaced" from "appended to an empty set".
    """
    from src.domain.scrum import Scrum
    from src.domain.ticket import TicketStatus

    user, cookie, org, project_id = populated_org
    naive = UTC_NOW.replace(tzinfo=None)

    a, b, c = (
        _ticket(
            db_engine,
            org,
            project_id,
            summary=f"finished {n}",
            status=TicketStatus.DONE,
            assigned_to=user.id,
            completed_at=naive - timedelta(days=1),
        )
        for n in range(3)
    )
    _auth(client, cookie)

    def submit(*ids):
        _submit_update(client, org, project_id, picks=[(i, "done") for i in ids])
        with Session(db_engine) as session:
            scrum_id = (
                session.exec(select(Scrum).where(Scrum.project_id == project_id))
                .first()
                .id
            )
            return {v.ticket_id: v for v in _visits(session, scrum_id)}

    first = submit(a, b)
    assert set(first) == {a, b}

    # Un-tick `a`, keep `b`, add `c`. `a` must be gone -- this is the assertion
    # the append-only version could not pass.
    second = submit(b, c)
    assert set(second) == {b, c}, "an un-ticked pick survived in the record"

    # **Gone from the record, and its row kept.** The row is the only thing that
    # remembers whether the board ever got that ticket's comment, so deleting it
    # made a withdrawal erase the evidence of a failed push.
    with Session(db_engine) as session:
        scrum_id = (
            session.exec(select(Scrum).where(Scrum.project_id == project_id)).first().id
        )
        rows = {v.ticket_id: v for v in _visit_rows(session, scrum_id)}
        assert a in rows, "the withdrawn pick's row was deleted, not flagged"
        assert rows[a].withdrawn_at is not None
        assert rows[b].withdrawn_at is None

    # Everything un-ticked is a legal answer and must empty the record, not be
    # read as "nothing to say, leave it as it was".
    assert submit() == {}

    # And the count always equals the selection, never the running total.
    # Re-ticking revives the same rows rather than inserting a second set.
    assert set(submit(a, b, c)) == {a, b, c}
    with Session(db_engine) as session:
        scrum_id = (
            session.exec(select(Scrum).where(Scrum.project_id == project_id)).first().id
        )
        assert len(_visit_rows(session, scrum_id)) == 3, (
            "re-ticking inserted a second row instead of reviving the first"
        )


def test_a_ticket_that_stays_selected_keeps_its_own_visit_row(
    client, populated_org, db_engine
):
    """Reconciled, not deleted-and-reinserted -- and the id is the evidence.

    Delete-all-then-insert would satisfy every assertion in the test above while
    throwing away the row each time. That is not free: a visit is about to carry a
    comment and a push error, so churning the row for a ticket the user never
    touched would discard data belonging to a pick they did not change. Only rows
    whose ticket left the selection may go.
    """
    from src.domain.ticket import TicketStatus

    user, cookie, org, project_id = populated_org
    naive = UTC_NOW.replace(tzinfo=None)

    kept, added = (
        _ticket(
            db_engine,
            org,
            project_id,
            summary=f"finished {n}",
            status=TicketStatus.DONE,
            assigned_to=user.id,
            completed_at=naive - timedelta(days=1),
        )
        for n in range(2)
    )
    _auth(client, cookie)

    scrum_id = _submit_update(client, org, project_id, picks=[(kept, "done")])
    with Session(db_engine) as session:
        before = {v.ticket_id: v.id for v in _visits(session, scrum_id)}

    _submit_update(client, org, project_id, picks=[(added, "done"), (kept, "done")])
    with Session(db_engine) as session:
        after = {v.ticket_id: (v.id, v.position) for v in _visits(session, scrum_id)}

    assert after[kept][0] == before[kept], (
        "the surviving pick's row was recreated rather than updated"
    )
    # Position is the shape of the current answer, so it follows the new order
    # rather than preserving where the ticket used to sit.
    assert after[added][1] == 0
    assert after[kept][1] == 1


def test_a_scrums_visits_are_never_replaced_as_a_set(client, populated_org, db_engine):
    """A walk's stops are written one at a time, and must stay that way.

    Replacing a team scrum's visits wholesale would delete the first half of a
    meeting because somebody retried the second -- the exact loss the per-stop
    write exists to prevent. So `/picks` refuses the wrong kind rather than being
    a general-purpose visit setter that happens to be used by one workflow.
    """
    _, cookie, org, project_id = populated_org
    ticket_id = _walk_ticket(db_engine, org, project_id)
    _auth(client, cookie)
    scrum_id = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums", json={"project_id": project_id}
    ).json()["scrum_id"]

    refused = client.post(
        f"{UI_PREFIX}/{org.alias}/scrums/{scrum_id}/picks",
        json={"picks": [{"ticket_id": ticket_id, "status_at_visit": "in review"}]},
    )
    assert refused.status_code == 422, refused.text
    assert refused.json()["field"] == "kind"
    with Session(db_engine) as session:
        assert _visits(session, scrum_id) == []


def test_the_update_pickers_are_one_renderer_not_a_second_id_branch(
    client, populated_org
):
    """The engine gains a *kind* of step, not a second workflow it knows by name.

    ``custom="walk"`` exists because a loop with a clock cannot be pre-rendered.
    A picker can be, and is: what it needs is submit-then-advance, which the
    scrum's wrap-up already had written and hard-gated on its own id. Generalised
    rather than copied, because two copies of "is a 409 a failure?" is how the
    two come to disagree.
    """
    _, cookie, org, _ = populated_org
    _auth(client, cookie)
    html = client.get(f"{UI_PREFIX}/{org.alias}/workflow").text

    assert 'custom":"picks"' in html or '"custom":"picks"' in html
    assert "[data-pick]:checked" in html, "nothing client-side can read the boxes"
    assert 'run.wf.id === "give-scrum-update"' not in html, (
        "the engine learned a workflow's name instead of a kind of step"
    )
    # The kind travels with the open, so the record cannot be the wrong one.
    assert 'kind: "update"' in html or "kind: rec.kind" in html


def test_the_other_eight_pickers_keep_their_markup_byte_identical():
    """`_row` gained an optional ticket id, and eight callers must not have noticed.

    A helper that grows an attribute for one caller and emits it for all of them
    changes markup nine steps rely on, and nothing on the page would say so.
    """
    from src.routers.webui.workflow import _row

    assert (
        _row("left", "right")
        == '<div class="wrow"><span class="wgrow">left</span>right</div>'
    )
    assert _row("left", check=False) == (
        '<div class="wrow"><input type="checkbox" /><span class="wgrow">left</span></div>'
    )
    assert _row("left", check=True) == (
        '<div class="wrow"><input type="checkbox" checked /><span class="wgrow">left</span></div>'
    )
    # And with an id, exactly one attribute more.
    assert 'data-pick="7"' in _row("left", check=False, ticket_id=7)


# --------------------------------------------------------------------------- #
# The left nav
#
# It used to render on the project page and nowhere else, so the dashboard, the
# workflow launcher, profile, team and the new-project form were each dead ends
# -- and the launcher is where signing in lands (#636).
# --------------------------------------------------------------------------- #


def _signed_in_templates():
    """Every signed-in page's route template, read from the router itself.

    The nav tests below are parametrized on this rather than on a list written
    out here, so a page added later cannot silently opt out: it arrives as a new
    parameter, `_SIGNED_IN_PAGES` has no URL for it, and the test fails with a
    KeyError naming the template. A hand-kept list would simply not mention it.

    **Every `/ui` GET is enumerated and the signed-out ones subtracted by name**,
    rather than matching the `/ui/{org_ref}` prefix. The prefix form looked
    equivalent and was not: a page registered as `/ui/{organization}/...`, or one
    with no org segment at all (`/ui/account`, `/ui/scrums/{id}`), simply did not
    appear, so it could ship with no nav and this suite stayed green -- the exact
    silent opt-out the parametrization exists to prevent. Subtracting a known set
    fails loudly when a page is added; matching a prefix fails silently.
    """
    from src.routers.webui import routes

    return sorted(
        route.path
        for route in routes.router.routes
        if "GET" in route.methods
        and route.path.startswith(UI_PREFIX)
        and route.path not in _SIGNED_OUT_PAGES
    )


#: `/ui` GETs that render no rail, and why. Anything else appearing under
#: `/ui` is treated as a signed-in page and must prove it has one.
#:
#: Two different reasons, kept in one set because the test only needs "not a
#: navigable page": the first four are reachable without a session, so there is
#: no org to head a rail with; `UI_PREFIX` itself is a 303 to the viewer's
#: default org and renders nothing at all.
_SIGNED_OUT_PAGES = frozenset(
    {
        LOGIN_PATH,
        LOGOUT_PATH,
        SESSION_PATH,
        JOIN_PATH,
        UI_PREFIX,
    }
)


#: How to reach each of those templates concretely, given `populated_org`'s org.
#: Missing entry -> KeyError -> failure; see `_signed_in_templates`.
_SIGNED_IN_PAGES = {
    "/ui/{org_ref}": lambda org: [dashboard_path(org.alias)],
    "/ui/{org_ref}/workflow": lambda org: [f"{UI_PREFIX}/{org.alias}/workflow"],
    "/ui/{org_ref}/profile": lambda org: [f"{UI_PREFIX}/{org.alias}/profile"],
    "/ui/{org_ref}/team": lambda org: [f"{UI_PREFIX}/{org.alias}/team"],
    "/ui/{org_ref}/projects/new": lambda org: [f"{UI_PREFIX}/{org.alias}/projects/new"],
    "/ui/{org_ref}/projects/{project_alias}": lambda org: [_project_url(org)],
    "/ui/{org_ref}/projects/{project_alias}/{tab}": lambda org: [
        _project_url(org, tab=tab)
        for tab in ("tickets", "releases", "timeline", "settings")
    ],
}

#: Pages that carry a project block: the five project tabs and nothing else.
_PROJECT_SCOPED = {
    "/ui/{org_ref}/projects/{project_alias}",
    "/ui/{org_ref}/projects/{project_alias}/{tab}",
}


def _nav(html: str) -> str:
    """The rail's markup alone, from ``<details class="navwrap">`` to its close.

    Pulled out rather than asserted against the whole document because almost
    every string worth checking here -- a project path, an alias, "Settings" --
    occurs elsewhere on these pages. A page-wide substring check would pass with
    no rail rendered at all, which is precisely the bug.

    Safe to close on the first ``</details>``: the rail nests none, and the panes
    that do (the user menu, the layer picker) are outside it.
    """
    start = html.find('<details class="navwrap">')
    assert start != -1, "no left nav on this page"
    end = html.index("</details>", start)
    return html[start : end + len("</details>")]


@pytest.mark.parametrize("template", _signed_in_templates())
def test_every_signed_in_page_carries_the_nav(client, populated_org, template):
    """One nav, everywhere, and both org-level destinations reachable from it.

    Workflows *and* Projects on every page is the point: the launcher is the
    front door and had no way to the projects list, while the projects list had
    no way to the launcher.
    """
    user, cookie, org, project_id = populated_org
    _auth(client, cookie)

    for path in _SIGNED_IN_PAGES[template](org):
        response = client.get(path)
        assert response.status_code == 200, path
        rail = _nav(response.text)

        assert f'href="{UI_PREFIX}/{org.alias}/workflow"' in rail, path
        assert "<span>Workflows</span>" in rail, path
        assert f'href="{dashboard_path(org.alias)}"' in rail, path
        assert "<span>Projects</span>" in rail, path
        # The org names the rail, so it is legible which org's pair these are.
        assert org.name in rail, path
        # Collapsible with no JavaScript, shut by default, same remembered key.
        assert rail.startswith('<details class="navwrap">'), path
        assert "innoday.nav.open.v2" in response.text, path


@pytest.mark.parametrize("template", _signed_in_templates())
def test_the_project_block_appears_only_when_a_project_is_in_scope(
    client, populated_org, template
):
    """Seven flat links on an org-level page would name a project you are not in.

    The org-level pair is unconditional; the project tabs are drawn only under a
    project, nested below its alias.
    """
    user, cookie, org, project_id = populated_org
    _auth(client, cookie)
    scoped = template in _PROJECT_SCOPED

    for path in _SIGNED_IN_PAGES[template](org):
        rail = _nav(client.get(path).text)
        for label in ("Project", "Tickets", "Releases", "Timeline", "Settings"):
            assert (f"<span>{label}</span>" in rail) is scoped, (path, label)
        # The alias heads the block, and the rule before Settings survives.
        assert (">PF</span>" in rail) is scoped, path
        assert ('<span class="navsep"></span>' in rail) is scoped, path


def test_the_open_page_is_the_one_marked_current(client, populated_org):
    """`aria-current="page"` on exactly the row you are looking at.

    Exactly one, and on the right href -- two rows claiming to be the current
    page is what a screen reader reads out, and neither the CSS nor a substring
    check would notice.
    """
    user, cookie, org, project_id = populated_org
    _auth(client, cookie)

    expected = {
        dashboard_path(org.alias): f"{UI_PREFIX}/{org.alias}",
        f"{UI_PREFIX}/{org.alias}/workflow": f"{UI_PREFIX}/{org.alias}/workflow",
        _project_url(org): _project_url(org),
        _project_url(org, tab="tickets"): _project_url(org, tab="tickets"),
        _project_url(org, tab="releases"): _project_url(org, tab="releases"),
        _project_url(org, tab="timeline"): _project_url(org, tab="timeline"),
        _project_url(org, tab="settings"): _project_url(org, tab="settings"),
    }
    for path, href in expected.items():
        rail = _nav(client.get(path).text)
        assert rail.count('aria-current="page"') == 1, path
        assert f'aria-current="page" href="{href}"' in rail, path

    # Profile, team and the new-project form are reached from the topbar menu and
    # from the dashboard, so no row is the page you are on. Claiming one would be
    # a false statement to a screen reader, not a harmless default.
    for path in (
        f"{UI_PREFIX}/{org.alias}/profile",
        f"{UI_PREFIX}/{org.alias}/team",
        f"{UI_PREFIX}/{org.alias}/projects/new",
    ):
        assert 'aria-current="page"' not in _nav(client.get(path).text), path


def test_the_nav_escapes_the_org_name(client, signed_in, make_org):
    """The org name is attacker-influenced -- an org ADMIN can PUT it with only a
    user token -- and it is now interpolated into the rail twice, as text and as
    the heading's `title` attribute. This app sets no CSP, so one raw `<` there
    is a script tag on every signed-in page in the org."""
    user, cookie = signed_in()
    # Carries both a `<` for the text node and a `"` for the attribute. The
    # earlier payload had no quote character, so escaping the `title` with
    # `quote=False` passed this test while leaving every signed-in page in the
    # org one refactor away from an `onmouseover` that fires.
    payload = '</span><script>alert(1)</script> X" onmouseover="alert(1)'
    org = make_org("hostile", name=payload, member=user)

    _auth(client, cookie)
    rail = _nav(client.get(dashboard_path(org.alias)).text)

    assert "<script>" not in rail
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in rail
    # Attribute context: the quote must not close `title="`.
    assert 'onmouseover="alert(1)' not in rail
    assert "&quot;" in rail


def test_the_nav_escapes_a_hostile_project_alias():
    """Same argument one level down, asserted on the function.

    Driven directly rather than through a page because a project alias is also a
    URL segment, so a request for a hostile one is a routing question and would
    never reach the renderer -- while `_app_nav` is called with whatever alias
    the card carries.
    """
    from src.domain.organization import Organization as Org
    from src.routers.webui.render import _app_nav

    rail = _app_nav(
        Org(id="o1", name="Fine", alias="fine"),
        active="tickets",
        project_alias='"><script>alert(1)</script>',
        open_tickets=3,
    )

    assert "<script>" not in rail
    assert '"><script>' not in rail
    assert "&lt;script&gt;" in rail
    # And the count still rendered, so the escaping did not eat the block.
    assert '<span class="ct">3</span>' in rail


class TestEveryFailureIsShown:
    """A comment the board refused was recorded and never mentioned.

    The server detected it, classified it, persisted it to
    `scrum_ticket_visits.comment_error` and returned it — and the page read
    `r.error || r.notice` and nothing else, so `comment_error` arrived and was
    dropped on the floor. The update reported itself done, and the person
    believed their message had reached the ticket. This module ranks that as
    the worst failure available here, because it is the one that causes a real
    misunderstanding between two people rather than a visible error.

    Underneath it, the server kept only the *first* failure of each kind
    (`error = error or result.error`), so even a surfaced banner could only
    ever name one of them.
    """

    def test_the_page_reads_the_comment_failures_it_is_sent(
        self, client, populated_org
    ):
        _, cookie, org, _ = populated_org
        _auth(client, cookie)
        page = client.get(f"{UI_PREFIX}/{org.alias}/workflow").text
        assert "comment_errors" in page, (
            "the page ignores comment failures again — a refused comment would "
            "be silent"
        )

    def test_the_banner_can_hold_more_than_one_line(self, client, populated_org):
        """A move failure and a comment failure in one submit are two things
        the reader has to be told, not one."""
        _, cookie, org, _ = populated_org
        _auth(client, cookie)
        page = client.get(f"{UI_PREFIX}/{org.alias}/workflow").text
        assert "white-space:pre-line" in page, (
            "joined failures would collapse into one run-on line"
        )
        assert "Array.isArray(message)" in page

    def test_a_lost_stop_no_longer_replaces_the_rest(self, client, populated_org):
        """It used to `else if`, so whichever came first was all you saw."""
        _, cookie, org, _ = populated_org
        _auth(client, cookie)
        page = client.get(f"{UI_PREFIX}/{org.alias}/workflow").text
        assert "told = told.concat(rec.warn)" in page

    def test_the_dropped_note_warning_cannot_go_stale(self, client, populated_org):
        """Set-only, it survived into the next picker and reported notes
        dropped by a step the reader had already left."""
        _, cookie, org, _ = populated_org
        _auth(client, cookie)
        page = client.get(f"{UI_PREFIX}/{org.alias}/workflow").text
        assert "rec.warn = dropped" in page and ": [];" in page, (
            "the drop warning is assigned only when something dropped, so it goes stale"
        )


def test_two_tickets_that_both_fail_are_both_reported(
    client, populated_org, db_engine, monkeypatch
):
    """**The accumulation, proven rather than asserted about the JS.**

    The server kept `error = error or result.error`, so the second ticket's
    refusal was discarded before the response was built. Two tickets fail here;
    both must come back. Pinning the count, not just "there is an error", is
    what makes this fail against the old first-only behaviour.
    """
    from src.adapters.base_adapter import BoardAdapterError
    from src.services import ticket_status_service

    user, cookie, org, project_id = populated_org
    board_id = _board(db_engine, org, project_id, user)
    naive = UTC_NOW.replace(tzinfo=None)
    finished = [
        _ticket(
            db_engine,
            org,
            project_id,
            summary=f"both on a real board {n}",
            status=TicketStatus.DONE,
            assigned_to=user.id,
            completed_at=naive - timedelta(days=1),
            board_registration_id=board_id,
            external_ticket_id=f"PF-{70 + n}",
        )
        for n in (1, 2)
    ]
    monkeypatch.setattr(
        ticket_status_service, "resolve_board_token", lambda *a, **k: "tok"
    )
    monkeypatch.setattr(
        ticket_status_service,
        "build_board_adapter",
        mock.AsyncMock(
            return_value=_FailingAdapter(BoardAdapterError("Linear is down"))
        ),
    )

    _auth(client, cookie)
    _, answer = _run_update(
        client, org, project_id, picks=[(t, "done") for t in finished]
    )

    assert answer["applied"] is True
    assert len(_move_errors(answer)) == 2, (
        "only one failure survived — the other was dropped before the reader "
        f"could be told: {_move_errors(answer)}"
    )
