"""The sign-in-link endpoint's security properties.

Each test here pins something that, if it broke, would break quietly: an oracle
that leaks which addresses have accounts, or a path that lets a stranger
provision an identity.
"""

from unittest.mock import patch

import pytest
from sqlmodel import Session

from src.domain.user import User
from src.services import sign_in_link
from src.services.supabase_invite import MagicLinkResult


@pytest.fixture(autouse=True)
def _clear_throttle():
    sign_in_link._last_request.clear()
    yield
    sign_in_link._last_request.clear()


@pytest.fixture
def session(db_engine):
    with Session(db_engine) as db_session:
        yield db_session


@pytest.fixture
def known_user(session: Session) -> User:
    user = User(email="known@example.test", full_name="Known Person")
    session.add(user)
    session.commit()
    return user


def _configured():
    return patch("src.services.sign_in_link.magic_link_configured", return_value=True)


def test_unknown_address_never_reaches_supabase(session: Session):
    """The allowlist check is the thing stopping a stranger provisioning an identity."""
    with _configured(), patch("src.services.sign_in_link.send_magic_link") as send:
        reason = sign_in_link.request_sign_in_link(
            session, email="stranger@example.test", redirect_to="https://x.test/cb"
        )

    assert reason is None  # same answer a known address gets
    send.assert_not_called()


def test_known_address_is_sent_a_link(session: Session, known_user: User):
    with (
        _configured(),
        patch(
            "src.services.sign_in_link.send_magic_link",
            return_value=MagicLinkResult(configured=True, sent=True),
        ) as send,
    ):
        assert (
            sign_in_link.request_sign_in_link(
                session, email="known@example.test", redirect_to="https://x.test/cb"
            )
            is None
        )

    send.assert_called_once()
    assert send.call_args.kwargs["redirect_to"] == "https://x.test/cb"


def test_address_is_matched_case_insensitively(session: Session, known_user: User):
    with (
        _configured(),
        patch(
            "src.services.sign_in_link.send_magic_link",
            return_value=MagicLinkResult(configured=True, sent=True),
        ) as send,
    ):
        sign_in_link.request_sign_in_link(
            session, email="  KNOWN@Example.TEST  ", redirect_to="https://x.test/cb"
        )

    send.assert_called_once()


def test_unconfirmed_user_falls_back_to_a_fresh_invite(
    session: Session, known_user: User
):
    """`422 signup_disabled` means "never clicked their link", not "broken config".

    Without the fallback the page says "check your email" and no email ever
    arrives -- permanently, with nothing to notice it.
    """
    refused = MagicLinkResult(
        configured=True, sent=False, status_code=422, error="Signup disabled"
    )
    with (
        _configured(),
        patch("src.services.sign_in_link.send_magic_link", return_value=refused),
        patch("src.services.sign_in_link.resend_invite", return_value=None) as invite,
    ):
        sign_in_link.request_sign_in_link(
            session, email="known@example.test", redirect_to="https://x.test/cb"
        )

    invite.assert_called_once_with("known@example.test")


def test_other_422s_do_not_email_anybody(session: Session, known_user: User):
    """422 is reused for ordinary validation failures; re-inviting on one of those
    would email a person for no reason."""
    other = MagicLinkResult(
        configured=True, sent=False, status_code=422, error="Invalid email format"
    )
    with (
        _configured(),
        patch("src.services.sign_in_link.send_magic_link", return_value=other),
        patch("src.services.sign_in_link.resend_invite") as invite,
    ):
        sign_in_link.request_sign_in_link(
            session, email="known@example.test", redirect_to="https://x.test/cb"
        )

    invite.assert_not_called()


def test_a_second_request_is_throttled(session: Session, known_user: User):
    with (
        _configured(),
        patch(
            "src.services.sign_in_link.send_magic_link",
            return_value=MagicLinkResult(configured=True, sent=True),
        ) as send,
    ):
        for _ in range(3):
            sign_in_link.request_sign_in_link(
                session, email="known@example.test", redirect_to="https://x.test/cb"
            )

    assert send.call_count == 1


def test_throttle_does_not_grow_without_bound(session: Session):
    """The route is reachable by anyone, so "distinct addresses seen" is
    attacker-controlled and the map must be swept."""
    sign_in_link._last_request.update(
        {f"a{i}@x.test": 0.0 for i in range(sign_in_link.TRACKING_LIMIT + 5)}
    )
    with _configured(), patch("src.services.sign_in_link.send_magic_link"):
        sign_in_link.request_sign_in_link(
            session, email="fresh@x.test", redirect_to="https://x.test/cb"
        )

    assert len(sign_in_link._last_request) <= sign_in_link.TRACKING_LIMIT


def test_an_unconfigured_deployment_says_so(session: Session):
    """The one distinguishable answer, and it is true for every caller equally."""
    with patch("src.services.sign_in_link.magic_link_configured", return_value=False):
        assert (
            sign_in_link.request_sign_in_link(
                session, email="known@example.test", redirect_to="https://x.test/cb"
            )
            == "not_configured"
        )
