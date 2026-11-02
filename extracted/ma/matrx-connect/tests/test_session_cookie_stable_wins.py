"""The 2026-08-30 outage's FINAL root cause, pinned: a second AuthMiddleware
constructed without a secret must never clobber the stable registration.

Sequence that broke production: the app middleware registered the stable
host-injected secret; aidream's out-of-band token verifier then constructed a
bare _BaseAuthMiddleware (no guest_fingerprint_secret), whose constructor
registered its per-process random — last-writer-wins replaced the stable
secret with a different random on every container, and all private file
renders 401'd. These tests fail on the pre-fix last-writer-wins semantic.
"""

import logging

import pytest

from matrx_connect.middleware.session_cookie import (
    classify_session_cookie_value,
    get_session_cookie_secret,
    get_session_cookie_secret_source,
    mint_session_cookie_value,
    register_session_cookie_secret,
)


@pytest.fixture(autouse=True)
def _reset_registration():
    import matrx_connect.middleware.session_cookie as sc

    before = (sc._registered_secret, sc._registered_secret_is_ephemeral)
    sc._registered_secret = None
    sc._registered_secret_is_ephemeral = False
    yield
    sc._registered_secret, sc._registered_secret_is_ephemeral = before


def test_ephemeral_never_clobbers_stable(caplog):
    stable = b"stable-secret-from-env"
    register_session_cookie_secret(stable, ephemeral=False)
    with caplog.at_level(logging.WARNING, logger="matrx_connect.auth"):
        register_session_cookie_secret(b"random-per-process", ephemeral=True)
    assert get_session_cookie_secret() == stable
    assert get_session_cookie_secret_source() == "stable"
    assert any("REFUSED an ephemeral secret" in r.message for r in caplog.records)


def test_cookie_survives_second_bare_registration_end_to_end():
    """Mint under stable, let an ephemeral clobber attempt happen, verify OK."""
    stable = b"stable-secret-from-env"
    register_session_cookie_secret(stable, ephemeral=False)
    value = mint_session_cookie_value("11111111-1111-4111-8111-111111111111", stable)
    register_session_cookie_secret(b"another-container-random", ephemeral=True)
    user, reason = classify_session_cookie_value(
        value, get_session_cookie_secret()
    )
    assert reason == "ok"
    assert user == "11111111-1111-4111-8111-111111111111"


def test_ephemeral_registers_when_nothing_stable_exists():
    register_session_cookie_secret(b"first-random", ephemeral=True)
    assert get_session_cookie_secret_source() == "ephemeral"
    # a later stable registration upgrades it
    register_session_cookie_secret(b"now-stable", ephemeral=False)
    assert get_session_cookie_secret() == b"now-stable"
    assert get_session_cookie_secret_source() == "stable"


def test_two_different_stable_secrets_scream_critical(caplog):
    register_session_cookie_secret(b"stable-a", ephemeral=False)
    with caplog.at_level(logging.CRITICAL, logger="matrx_connect.auth"):
        register_session_cookie_secret(b"stable-b", ephemeral=False)
    assert get_session_cookie_secret() == b"stable-b"
    assert any("TWO DIFFERENT STABLE" in r.message for r in caplog.records)


def test_same_stable_secret_is_idempotent_and_silent(caplog):
    register_session_cookie_secret(b"stable-a", ephemeral=False)
    with caplog.at_level(logging.WARNING, logger="matrx_connect.auth"):
        register_session_cookie_secret(b"stable-a", ephemeral=False)
    assert get_session_cookie_secret() == b"stable-a"
    assert not caplog.records
