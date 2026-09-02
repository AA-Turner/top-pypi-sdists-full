"""Component-level proofs backing the S4 contract: the single input path, TURN
credential scope, the cookie shape, ticket claim hygiene, grant isolation, and
the not-configured 503.
"""

from __future__ import annotations

import time

import pytest

from matrx_scraper.cloud_browser.streaming.config import (
    STREAM_COOKIE_NAME,
    StreamingConfig,
    StreamTicketNotConfigured,
)
from matrx_scraper.cloud_browser.streaming.errors import StreamError
from matrx_scraper.cloud_browser.streaming.turn_credentials import mint_turn_credential
from matrx_scraper.cloud_browser.streaming.worker_input import WorkerInputChannel

from .harness import ORIGIN, make_harness


# --- exactly ONE input path per run ---------------------------------------
def test_only_one_input_path_exists():
    ch = WorkerInputChannel("run-x")
    scopes = frozenset({"stream:video", "input:xtest"})
    ch.enable_input(stream_session_id="s1", control_revision=5, scopes=scopes)
    # A newer controller binds; the old session's path dies — never two writable.
    ch.enable_input(stream_session_id="s2", control_revision=6, scopes=scopes)
    with pytest.raises(StreamError):
        ch.inject(stream_session_id="s1", control_revision=5, event={})
    ch.inject(stream_session_id="s2", control_revision=6, event={})
    assert ch.injected_count == 1


def test_stale_revision_refused_by_worker():
    ch = WorkerInputChannel("run-x")
    ch.enable_input(
        stream_session_id="s2",
        control_revision=6,
        scopes=frozenset({"stream:video", "input:xtest"}),
    )
    # A stale gateway that lost the CAS race carries revision 5 < 6.
    with pytest.raises(StreamError) as ei:
        ch.inject(stream_session_id="s2", control_revision=5, event={})
    assert ei.value.code == "input_not_permitted"


def test_kill_input_is_idempotent_and_final():
    ch = WorkerInputChannel("run-x")
    ch.enable_input(
        stream_session_id="s1",
        control_revision=1,
        scopes=frozenset({"stream:video", "input:xtest"}),
    )
    ch.kill_input()
    ch.kill_input()  # idempotent
    assert ch.input_live is False
    with pytest.raises(StreamError):
        ch.inject(stream_session_id="s1", control_revision=1, event={})


# --- TURN credentials (S4 §8) ---------------------------------------------
def test_turn_credential_is_short_lived_and_secretless():
    cfg = StreamingConfig(
        turn_shared_secret="topsecret", turn_urls=("turn:t:3478",), stun_urls=("stun:t:3478",)
    )
    now = time.time()
    cred = mint_turn_credential(cfg, stream_session_id="sess-9", now=now)
    # username embeds session id, not user/origin.
    assert cred.username.endswith(":sess-9")
    assert cred.expires_at == int(now) + 120
    # the shared secret never appears in the client-visible credential.
    assert "topsecret" not in cred.credential
    assert "topsecret" not in cred.username


def test_turn_without_secret_is_stun_only_not_a_fallback():
    cfg = StreamingConfig(
        turn_shared_secret=None, stun_urls=("stun:t:3478",), turn_urls=("turn:t:3478",)
    )
    cred = mint_turn_credential(cfg, stream_session_id="s")
    assert cred.turn_urls == ()  # no relay offered without a configured secret
    assert cred.credential == ""


# --- cookie shape (S4 §4.2) -----------------------------------------------
def test_cookie_is_secure_httponly_pathscoped_strict():
    h = make_harness()
    resp = h.mint.mint_control(
        handoff_id=h.handoff_id, user_id=h.user_id, origin=ORIGIN, takeover=False
    )
    result = h.gateway.claim(
        stream_session_id=resp.stream_session_id,
        ticket=resp.ticket,
        request_origin=ORIGIN,
        authenticated_user_id=h.user_id,
    )
    c = result.cookie_header
    assert c.startswith(f"{STREAM_COOKIE_NAME}=")
    assert "__Secure-" in c  # host-only, not __Host- (path scoping needed)
    assert "Domain=" not in c  # host-only scope
    assert f"Path=/stream/{resp.stream_session_id}" in c
    assert "Secure" in c and "HttpOnly" in c and "SameSite=Strict" in c
    assert "Max-Age=120" in c


# --- ticket claim hygiene (S4 §3.1) ---------------------------------------
def test_ticket_claims_carry_no_forbidden_material():
    h = make_harness()
    resp = h.mint.mint_control(
        handoff_id=h.handoff_id, user_id=h.user_id, origin=ORIGIN, takeover=False
    )
    claims = h.plane.signer.verify(resp.ticket)
    # bound identity fields present…
    assert claims.origin == ORIGIN
    assert claims.mode == "control"
    assert claims.allows_input is True
    # …and the whole decoded token carries no worker address, no secret.
    import jwt

    decoded = jwt.decode(resp.ticket, options={"verify_signature": False})
    blob = str(decoded)
    assert h.config.turn_shared_secret not in blob
    # worker_id IS bound (mtx_worker_id) but is an opaque id, never an address:
    assert "://" not in str(decoded.get("mtx_worker_id", ""))
    assert ":3478" not in blob


# --- grant revocation isolation (S4 §6 invariant 2) -----------------------
def test_revoking_one_user_does_not_disturb_another():
    h = make_harness(multi_view_low_latency=True)
    # Bob is a viewer on the same profile with a live view session.
    h.access.grant(user_id="bob", profile_id=h.profile_id, level="viewer")
    vresp = h.mint.mint_view(run_id=h.run_id, user_id="bob", origin=ORIGIN)
    h.gateway.claim(
        stream_session_id=vresp.stream_session_id,
        ticket=vresp.ticket,
        request_origin=ORIGIN,
        authenticated_user_id="bob",
    )
    # Arman (the controller) has his grant revoked.
    h.gateway.revoker.revoke_grant(
        user_id=h.user_id, profile_id=h.profile_id, reason="grant_revoked"
    )
    # Bob's session is untouched — the profile stays alive for other users.
    bob_sess = h.gateway.sessions.get(vresp.stream_session_id)
    assert bob_sess is not None and bob_sess.live is True


# --- not-configured -> loud 503 -------------------------------------------
def test_missing_signing_key_is_loud_not_silent():
    cfg = StreamingConfig(stream_signing_key_pem=None)
    with pytest.raises(StreamTicketNotConfigured):
        cfg.require_signing_key()
