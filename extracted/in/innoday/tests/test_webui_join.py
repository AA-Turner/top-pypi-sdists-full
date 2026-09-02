"""The team-secret-gated request-for-access page.

This exists because of a failure that was invisible from the user's side. Three
people held an InnoDay account and a Supabase identity that had never been
confirmed. `[auth] enable_signup = false` makes GoTrue route an unconfirmed
user's magic link through its *signup* path, so `/auth/v1/otp` answers
`422 signup_disabled` -- while the sign-in page still renders "check your email".
They could not get in, were told nothing was wrong, and no amount of retrying
would have helped.

The page splits on whether an account already exists, and the split is the design:

* **has an account** -- someone already authorised them, so send a fresh invite
  through the admin endpoint, which is the one path that reaches an unconfirmed
  identity. Nothing to approve.
* **no account** -- queue it. The team secret is shared, static and attributable
  to nobody, so holding it shows proximity to the team, not authorisation.

Tests are grouped by failure mode rather than by function; the ones worth more
than their coverage are the gate itself, and the fact that a failed provision
leaves the request PENDING rather than silently approved.
"""

from uuid import uuid4

import pytest
from sqlmodel import Session, select

from src.domain.organization import (
    OrganizationMembership,
    OrganizationRole,
)
from src.domain.signup_request import SignupRequest, SignupRequestStatus
from src.domain.user import User
from src.page_paths import JOIN_PATH, LOGIN_PATH, UI_PREFIX
from src.routers.webui.session import COOKIE_NAME

SECRET = "correct-horse-battery-staple"


@pytest.fixture(autouse=True)
def _gate(monkeypatch):
    monkeypatch.setenv("TEAM_ACCESS_SECRET", SECRET)


@pytest.fixture
def sent(monkeypatch):
    """Record invites instead of emailing. Returns the list of addresses."""
    addresses = []

    def _resend(email):
        addresses.append(email)
        return None

    monkeypatch.setattr("src.routers.webui.routes.resend_invite", _resend)
    return addresses


def _post(client, **fields):
    body = {"email": "new@example.com", "team_secret": SECRET}
    body.update(fields)
    return client.post(JOIN_PATH, data=body)


# --------------------------------------------------------------------------- #
# The gate
# --------------------------------------------------------------------------- #


def test_page_refuses_to_open_when_no_team_secret_is_configured(client, monkeypatch):
    """ "Not configured" must never read as "gate passed".

    That is the failure where a permissive local default ships to production. A
    deployment with no secret has no gate, so the page does not open at all --
    on GET or POST, because a form that never renders can still be posted to.
    """
    monkeypatch.delenv("TEAM_ACCESS_SECRET", raising=False)

    assert "Not available" in client.get(JOIN_PATH).text
    # A non-empty value on purpose: an empty field is rejected by FastAPI as
    # missing (422) before the handler runs, which would test the form schema
    # rather than the gate.
    assert "Not available" in _post(client, team_secret="anything").text


def test_wrong_secret_is_rejected_identically_whoever_asks(client, db_engine, sent):
    """One message for a wrong secret, whatever the address.

    Anything else turns the form into an oracle: try a known address and an
    unknown one, compare the answers, and you learn whether your secret guess
    was the thing that failed.
    """
    with Session(db_engine) as session:
        session.add(User(id=str(uuid4()), email="known@example.com", full_name="K"))
        session.commit()

    known = _post(client, email="known@example.com", team_secret="nope")
    unknown = _post(client, email="nobody@example.com", team_secret="nope")

    assert "not right" in known.text and "not right" in unknown.text
    assert known.text == unknown.text.replace("nobody@example.com", "known@example.com")
    assert sent == [], "a bad secret must never send email"
    with Session(db_engine) as session:
        assert session.exec(select(SignupRequest)).all() == []


# --------------------------------------------------------------------------- #
# The two outcomes
# --------------------------------------------------------------------------- #


def test_existing_user_is_re_invited_and_never_queued(client, db_engine, sent):
    """The case this page was built for: authorised already, just stuck.

    Nothing to approve -- someone decided long ago. Queuing them would put a
    person who already has an account in front of an admin for no reason.
    """
    with Session(db_engine) as session:
        session.add(User(id=str(uuid4()), email="stuck@example.com", full_name="S"))
        session.commit()

    r = _post(client, email="  Stuck@Example.com  ")

    assert r.status_code == 200
    assert "Check your email" in r.text
    assert sent == ["stuck@example.com"], "trimmed and lowercased"
    with Session(db_engine) as session:
        assert session.exec(select(SignupRequest)).all() == [], "must not queue"


def test_unknown_address_is_queued_and_told_so(client, db_engine, sent):
    r = _post(client, email="newcomer@example.com", full_name="New Comer", note="PF")

    assert "Request received" in r.text
    assert sent == [], "queuing must not email anyone yet"
    with Session(db_engine) as session:
        row = session.exec(select(SignupRequest)).one()
        assert row.email == "newcomer@example.com"
        assert row.full_name == "New Comer"
        assert row.note == "PF"
        assert row.status == SignupRequestStatus.PENDING


def test_asking_twice_does_not_create_a_second_pending_row(client, db_engine, sent):
    """At most one PENDING row per address.

    The table has no unique constraint on purpose -- a denied request must not
    bar an address forever -- so this is enforced here, and it is the constraint
    that actually matters.
    """
    _post(client, email="eager@example.com")
    # Second attempt is throttled anyway; clear it so this tests dedup, not the
    # throttle.
    from src.routers.webui.routes import _last_request

    _last_request["join"].clear()
    _post(client, email="eager@example.com")

    with Session(db_engine) as session:
        assert len(session.exec(select(SignupRequest)).all()) == 1


def test_repeat_requests_are_throttled(client, db_engine, sent):
    """Both this route and sign-in send email on an unauthenticated POST, and
    email is a finite shared resource. Separate buckets, so being throttled on
    one does not lock you out of the other."""
    with Session(db_engine) as session:
        session.add(User(id=str(uuid4()), email="rapid@example.com", full_name="R"))
        session.commit()

    _post(client, email="rapid@example.com")
    _post(client, email="rapid@example.com")

    assert sent == ["rapid@example.com"], "second attempt suppressed"


# --------------------------------------------------------------------------- #
# Approval
# --------------------------------------------------------------------------- #


@pytest.fixture
def platform_admin(db_engine, signed_in, make_org):
    """A signed-in platform member with an org to look at, plus one pending row."""
    user, cookie = signed_in(is_platform_member=True)
    org = make_org("acme", member=user)
    with Session(db_engine) as session:
        req = SignupRequest(email="hopeful@example.com", full_name="Hope Ful")
        session.add(req)
        session.commit()
        session.refresh(req)
        return user, cookie, org, req.id


def test_queue_is_visible_only_to_platform_members(
    client, db_engine, signed_in, make_org, platform_admin
):
    """A non-platform member must not learn the queue exists.

    They cannot act on it, and the addresses in it are other people's.
    """
    admin_user, admin_cookie, org, _ = platform_admin

    client.cookies.set(COOKIE_NAME, admin_cookie)
    assert "hopeful@example.com" in client.get(f"{UI_PREFIX}/{org.alias}").text

    ordinary, cookie = signed_in()
    with Session(db_engine) as session:
        session.add(
            OrganizationMembership(
                id=str(uuid4()),
                user_id=ordinary.id,
                organization_id=org.id,
                role=OrganizationRole.ADMIN,
                is_active=True,
            )
        )
        session.commit()
    client.cookies.set(COOKIE_NAME, cookie)
    body = client.get(f"{UI_PREFIX}/{org.alias}").text
    assert "hopeful@example.com" not in body, "an org ADMIN is not a platform member"


def test_non_platform_member_gets_404_not_403_on_approve(
    client, db_engine, signed_in, make_org, platform_admin
):
    """404: a 403 would confirm that this request id is real."""
    _, _, org, request_id = platform_admin

    ordinary, cookie = signed_in()
    with Session(db_engine) as session:
        session.add(
            OrganizationMembership(
                id=str(uuid4()),
                user_id=ordinary.id,
                organization_id=org.id,
                role=OrganizationRole.ADMIN,
                is_active=True,
            )
        )
        session.commit()

    client.cookies.set(COOKIE_NAME, cookie)
    r = client.post(f"{UI_PREFIX}/{org.alias}/signup-requests/{request_id}/approve")
    assert r.status_code == 404

    with Session(db_engine) as session:
        assert (
            session.get(SignupRequest, request_id).status is SignupRequestStatus.PENDING
        )


def test_approving_provisions_a_user_and_links_it(
    client, db_engine, platform_admin, monkeypatch
):
    admin_user, cookie, org, request_id = platform_admin

    created = {}

    def _provision(session, *, email, full_name, **kw):
        from src.services.user_provisioning import ProvisionedUser

        user = User(
            id=str(uuid4()), email=email, full_name=full_name, supabase_user_id="sb-1"
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        # Capture the id, not the object: the route's session closes before the
        # assertions run, and a detached instance cannot be refreshed.
        created["id"] = user.id
        return ProvisionedUser(user=user, supabase_user_id="sb-1")

    monkeypatch.setattr("src.routers.webui.routes.provision_user", _provision)

    client.cookies.set(COOKIE_NAME, cookie)
    r = client.post(f"{UI_PREFIX}/{org.alias}/signup-requests/{request_id}/approve")

    assert r.status_code == 200 and "approved" in r.text
    with Session(db_engine) as session:
        row = session.get(SignupRequest, request_id)
        assert row.status is SignupRequestStatus.APPROVED
        assert row.decided_by == admin_user.id
        assert row.decided_at is not None
        assert row.created_user_id == created["id"]


def test_failed_provisioning_leaves_the_request_pending(
    client, db_engine, platform_admin, monkeypatch
):
    """A failure to provision is not a decision.

    Marking it APPROVED anyway would strand someone with no account, no invite,
    and no way to ask again -- the request would no longer be in the queue.
    """
    _, cookie, org, request_id = platform_admin

    def _boom(session, **kw):
        from src.services.user_provisioning import UserProvisioningError

        raise UserProvisioningError("upstream", "Supabase said no")

    monkeypatch.setattr("src.routers.webui.routes.provision_user", _boom)

    client.cookies.set(COOKIE_NAME, cookie)
    r = client.post(f"{UI_PREFIX}/{org.alias}/signup-requests/{request_id}/approve")

    assert "Could not create the account" in r.text
    with Session(db_engine) as session:
        assert (
            session.get(SignupRequest, request_id).status is SignupRequestStatus.PENDING
        )


def test_denying_records_the_decision_without_creating_anything(
    client, db_engine, platform_admin
):
    admin_user, cookie, org, request_id = platform_admin

    client.cookies.set(COOKIE_NAME, cookie)
    r = client.post(f"{UI_PREFIX}/{org.alias}/signup-requests/{request_id}/deny")

    assert "Denied access" in r.text
    with Session(db_engine) as session:
        row = session.get(SignupRequest, request_id)
        assert row.status is SignupRequestStatus.DENIED
        assert row.decided_by == admin_user.id
        assert row.created_user_id is None
        assert (
            session.exec(
                select(User).where(User.email == "hopeful@example.com")
            ).first()
            is None
        )


def test_join_page_is_reachable_without_a_session(client):
    """It is for people who cannot sign in; requiring a session would be circular."""
    r = client.get(JOIN_PATH)
    assert r.status_code == 200
    assert LOGIN_PATH in r.text, "and offers a way back to sign-in"
