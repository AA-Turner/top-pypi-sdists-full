"""A Supabase sign-in may attach to an existing InnoDay user by email only when
the email is confirmed and that user isn't already attached to a different
Supabase identity (PF-465).

Before this, a JWT for a *new* Supabase identity carrying an unconfirmed email
that matched an existing user -- a platform admin, say -- resolved to that user,
guarded only by REQUIRE_VERIFIED_EMAIL, which is off by default.
"""

from uuid import uuid4

import pytest
from sqlmodel import Session, select

from src.domain.user import User
from src.middleware import token_auth

EMAIL = "admin@example.com"


@pytest.fixture
def idp(monkeypatch):
    """What Supabase's own record says; default: unreadable (fail closed)."""
    record = {}
    monkeypatch.setattr(
        token_auth,
        "fetch_identity_confirmation",
        lambda sub: record.get(sub),
    )
    return record


@pytest.fixture
def identity(monkeypatch, idp):
    """Set what the (mocked) verified JWT says about its bearer."""
    claims = {}
    monkeypatch.setattr(token_auth, "supabase_auth_configured", lambda: True)
    monkeypatch.setattr(token_auth, "verify_supabase_jwt", lambda _t: {})
    monkeypatch.setattr(token_auth, "extract_identity", lambda _c: dict(claims))

    def _set(**kw):
        claims.clear()
        claims.update(kw)

    return _set


def _admin(session, supabase_user_id=None) -> User:
    user = User(
        id=str(uuid4()),
        email=EMAIL,
        full_name="Admin",
        is_platform_member=True,
        supabase_user_id=supabase_user_id,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.mark.parametrize("record_use", [True, False])
def test_an_unconfirmed_email_does_not_take_over_an_existing_user(
    db_engine, identity, record_use
):
    identity(supabase_user_id="attacker-sub", email=EMAIL, email_confirmed_at=None)
    with Session(db_engine) as s:
        admin = _admin(s)
        resolved = token_auth._user_from_supabase_jwt("jwt", s, record_use=record_use)
        assert resolved is None or resolved.id != admin.id
        s.refresh(admin)
        assert admin.supabase_user_id is None  # not linked to the attacker


@pytest.mark.parametrize("record_use", [True, False])
def test_a_user_linked_to_another_identity_is_not_relinked(
    db_engine, identity, record_use
):
    identity(
        supabase_user_id="attacker-sub",
        email=EMAIL,
        email_confirmed_at="2026-09-25T00:00:00Z",
    )
    with Session(db_engine) as s:
        admin = _admin(s, supabase_user_id="the-real-sub")
        resolved = token_auth._user_from_supabase_jwt("jwt", s, record_use=record_use)
        assert resolved is None or resolved.id != admin.id
        s.refresh(admin)
        assert admin.supabase_user_id == "the-real-sub"


def test_a_confirmed_first_sign_in_still_links_the_existing_user(db_engine, identity):
    """The legitimate case -- an invitee's first sign-in -- keeps working."""
    identity(
        supabase_user_id="real-sub",
        email=EMAIL,
        email_confirmed_at="2026-09-25T00:00:00Z",
    )
    with Session(db_engine) as s:
        admin = _admin(s)
        resolved = token_auth._user_from_supabase_jwt("jwt", s)
        assert resolved is not None and resolved.id == admin.id
        s.refresh(admin)
        assert admin.supabase_user_id == "real-sub"


def test_an_already_linked_user_signs_in_as_before(db_engine, identity):
    identity(supabase_user_id="real-sub", email=EMAIL, email_confirmed_at=None)
    with Session(db_engine) as s:
        admin = _admin(s, supabase_user_id="real-sub")
        assert token_auth._user_from_supabase_jwt("jwt", s).id == admin.id


def test_a_refused_link_does_not_create_a_duplicate_user(db_engine, identity):
    identity(supabase_user_id="attacker-sub", email=EMAIL, email_confirmed_at=None)
    with Session(db_engine) as s:
        _admin(s)
        token_auth._user_from_supabase_jwt("jwt", s)
        assert len(s.exec(select(User).where(User.email == EMAIL)).all()) == 1


def _confirmed(sub, email):
    from src.services.supabase_invite import IdPConfirmation

    return IdPConfirmation(
        supabase_user_id=sub, email=email, email_confirmed_at="2026-09-25T00:00:00Z"
    )


def test_the_idp_record_can_confirm_a_first_sign_in(db_engine, identity, idp):
    """Real JWTs carry no top-level confirmation; Supabase's record does."""
    identity(supabase_user_id="real-sub", email=EMAIL, email_confirmed_at=None)
    idp["real-sub"] = _confirmed("real-sub", EMAIL)
    with Session(db_engine) as s:
        admin = _admin(s)
        assert token_auth._user_from_supabase_jwt("jwt", s).id == admin.id


def test_the_idp_confirming_a_different_email_does_not_count(db_engine, identity, idp):
    identity(supabase_user_id="sub-x", email=EMAIL, email_confirmed_at=None)
    idp["sub-x"] = _confirmed("sub-x", "someone-else@example.com")
    with Session(db_engine) as s:
        _admin(s)
        assert token_auth._user_from_supabase_jwt("jwt", s) is None


def test_email_case_does_not_split_the_account(db_engine, identity):
    identity(
        supabase_user_id="real-sub",
        email="admin@example.com",
        email_confirmed_at="2026-09-25T00:00:00Z",
    )
    with Session(db_engine) as s:
        user = User(id=str(uuid4()), email="Admin@Example.com", full_name="A")
        s.add(user)
        s.commit()
        assert token_auth._user_from_supabase_jwt("jwt", s).id == user.id
        assert len(s.exec(select(User)).all()) == 1


def test_user_metadata_cannot_supply_the_email_or_the_confirmation():
    """Any signed-in user can write their own user_metadata."""
    from src.services.supabase_auth import extract_identity

    ident = extract_identity(
        {
            "sub": "s",
            "user_metadata": {"email": EMAIL, "email_verified": True},
        }
    )
    assert ident["email"] is None
    assert ident["email_confirmed_at"] is None
