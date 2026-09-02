"""WS-4 Definition-of-Done — S4 §10 assertion table, run standalone.

Each test is one row of the contract's proof table. All run with no Browser
Manager and no ``browser.*`` schema, against the in-memory plane. The one thing a
real deployment adds is a Selkies worker + coTURN; those steps are the operator
runbook (RUNBOOK-real-server-tests.md).
"""

from __future__ import annotations

import time

import jwt
import pytest

from matrx_scraper.cloud_browser.streaming.config import (
    STREAM_AUDIENCE,
    STREAM_ISSUER_NAME,
)
from matrx_scraper.cloud_browser.streaming.errors import StreamError

from .harness import ORIGIN, make_harness


def _mint_and_claim(h, *, origin=ORIGIN, user=None):
    resp = h.mint.mint_control(
        handoff_id=h.handoff_id, user_id=h.user_id, origin=ORIGIN, takeover=False
    )
    h.gateway.claim(
        stream_session_id=resp.stream_session_id,
        ticket=resp.ticket,
        request_origin=origin,
        authenticated_user_id=user or h.user_id,
    )
    return resp


# --- Row: replay the same ticket twice ------------------------------------
def test_replay_same_ticket_rejected_and_one_session():
    h = make_harness()
    resp = h.mint.mint_control(
        handoff_id=h.handoff_id, user_id=h.user_id, origin=ORIGIN, takeover=False
    )
    h.gateway.claim(
        stream_session_id=resp.stream_session_id,
        ticket=resp.ticket,
        request_origin=ORIGIN,
        authenticated_user_id=h.user_id,
    )
    with pytest.raises(StreamError) as ei:
        h.gateway.claim(
            stream_session_id=resp.stream_session_id,
            ticket=resp.ticket,
            request_origin=ORIGIN,
            authenticated_user_id=h.user_id,
        )
    assert ei.value.code == "stream_ticket_already_claimed"
    assert len(h.gateway.sessions.sessions_for_run(h.run_id)) == 1


# --- Row: different Origin -------------------------------------------------
def test_claim_from_different_origin_rejected():
    h = make_harness()
    resp = h.mint.mint_control(
        handoff_id=h.handoff_id, user_id=h.user_id, origin=ORIGIN, takeover=False
    )
    with pytest.raises(StreamError) as ei:
        h.gateway.claim(
            stream_session_id=resp.stream_session_id,
            ticket=resp.ticket,
            request_origin="https://evil.example",
            authenticated_user_id=h.user_id,
        )
    assert ei.value.code == "stream_ticket_origin_mismatch"


# --- Row: different signed-in user ----------------------------------------
def test_claim_as_different_user_rejected():
    h = make_harness()
    resp = h.mint.mint_control(
        handoff_id=h.handoff_id, user_id=h.user_id, origin=ORIGIN, takeover=False
    )
    with pytest.raises(StreamError) as ei:
        h.gateway.claim(
            stream_session_id=resp.stream_session_id,
            ticket=resp.ticket,
            request_origin=ORIGIN,
            authenticated_user_id="mallory",
        )
    assert ei.value.code == "stream_ticket_user_mismatch"


# --- Row: claim 61s after mint (expired) ----------------------------------
def test_expired_ticket_rejected():
    h = make_harness()
    # Craft an already-expired ticket with the real key + correct iss/aud/claims.
    now = int(time.time())
    payload = {
        "iss": STREAM_ISSUER_NAME,
        "aud": STREAM_AUDIENCE,
        "sub": h.user_id,
        "iat": now - 120,
        "exp": now - 60,
        "jti": "expired-1",
        "tier_policy": "none",
        "scopes": ["stream:video", "input:xtest"],
        "mtx_origin": ORIGIN,
        "mtx_stream_session_id": "sess-x",
    }
    token = jwt.encode(payload, h.pem, algorithm="ES256")
    with pytest.raises(StreamError) as ei:
        h.gateway.claim(
            stream_session_id="sess-x",
            ticket=token,
            request_origin=ORIGIN,
            authenticated_user_id=h.user_id,
        )
    assert ei.value.code == "stream_ticket_expired"


# --- Row: grant revision bumped after mint --------------------------------
def test_grant_bumped_after_mint_rejected_no_session():
    h = make_harness()
    resp = h.mint.mint_control(
        handoff_id=h.handoff_id, user_id=h.user_id, origin=ORIGIN, takeover=False
    )
    # Admin lowers/re-grants access after the ticket was minted -> revision bumps.
    h.access.lower(user_id=h.user_id, profile_id=h.profile_id, level="editor")
    with pytest.raises(StreamError) as ei:
        h.gateway.claim(
            stream_session_id=resp.stream_session_id,
            ticket=resp.ticket,
            request_origin=ORIGIN,
            authenticated_user_id=h.user_id,
        )
    assert ei.value.code == "grant_revoked"
    assert h.gateway.sessions.sessions_for_run(h.run_id) == []


# --- Row: control_revision one behind -------------------------------------
def test_stale_control_revision_rejected():
    h = make_harness()
    resp = h.mint.mint_control(
        handoff_id=h.handoff_id, user_id=h.user_id, origin=ORIGIN, takeover=False
    )
    # Something bumps the lease after mint (e.g. a competing claim / owner action).
    h.plane.runs.force_revoke(run_id=h.run_id)
    with pytest.raises(StreamError) as ei:
        h.gateway.claim(
            stream_session_id=resp.stream_session_id,
            ticket=resp.ticket,
            request_origin=ORIGIN,
            authenticated_user_id=h.user_id,
        )
    assert ei.value.code in ("control_lease_lost",)


# --- Row: revoke mid-session, then send a keystroke (assert AT THE WORKER)--
def test_revoke_kills_input_at_worker_immediately():
    h = make_harness()
    resp = _mint_and_claim(h)
    ch = h.worker_channel()
    # Input works while controlling.
    ch.inject(
        stream_session_id=resp.stream_session_id,
        control_revision=resp.control.control_revision,
        event={"type": "key", "k": "a"},
    )
    assert ch.injected_count == 1
    assert ch.input_live is True

    # Owner revokes control (confirmed). Needs admin.
    h.access.grant(user_id=h.user_id, profile_id=h.profile_id, level="admin")
    h.mint.revoke_control(
        run_id=h.run_id,
        user_id=h.user_id,
        control_revision=resp.control.control_revision,
        reason="owner_revoked",
        confirm=True,
    )

    assert ch.input_live is False
    with pytest.raises(StreamError):
        ch.inject(
            stream_session_id=resp.stream_session_id,
            control_revision=resp.control.control_revision,
            event={"type": "key", "k": "b"},
        )
    assert ch.injected_count == 1  # the post-revoke keystroke never landed


# --- Row: revoke, then reconnect with the SAME ticket ---------------------
def test_reconnect_with_same_ticket_refused():
    h = make_harness()
    resp = _mint_and_claim(h)
    h.mint.release_control(
        run_id=h.run_id,
        user_id=h.user_id,
        control_revision=resp.control.control_revision,
        reason="returned",
    )
    # The ticket is burnt (claimed) and the session is gone -> re-claim refused.
    with pytest.raises(StreamError) as ei:
        h.gateway.claim(
            stream_session_id=resp.stream_session_id,
            ticket=resp.ticket,
            request_origin=ORIGIN,
            authenticated_user_id=h.user_id,
        )
    assert ei.value.code in ("stream_ticket_already_claimed", "stream_ticket_revoked")


# --- Row: view-mode session attempts input (refused at worker) ------------
def test_view_session_cannot_inject_at_worker():
    h = make_harness(multi_view_low_latency=True)
    h.access.grant(user_id="viewer-bob", profile_id=h.profile_id, level="viewer")
    resp = h.mint.mint_view(run_id=h.run_id, user_id="viewer-bob", origin=ORIGIN)
    h.gateway.claim(
        stream_session_id=resp.stream_session_id,
        ticket=resp.ticket,
        request_origin=ORIGIN,
        authenticated_user_id="viewer-bob",
    )
    # The worker refuses to even bind an input path for a session lacking input:xtest.
    ch = h.worker_channel()
    with pytest.raises(StreamError) as ei:
        ch.enable_input(
            stream_session_id=resp.stream_session_id,
            control_revision=0,
            scopes=frozenset({"stream:video"}),
        )
    assert ei.value.code == "input_not_permitted"


# --- Row: view low-latency mint refused in v1 -----------------------------
def test_view_low_latency_refused_by_default():
    h = make_harness()  # multi_view_low_latency=False
    h.access.grant(user_id="viewer-bob", profile_id=h.profile_id, level="viewer")
    with pytest.raises(StreamError) as ei:
        h.mint.mint_view(run_id=h.run_id, user_id="viewer-bob", origin=ORIGIN)
    assert ei.value.code == "multi_view_not_enabled"


# --- Row: second control tab ----------------------------------------------
def test_second_control_tab_rejected_then_takeover():
    h = make_harness()
    resp1 = _mint_and_claim(h)
    # Second tab, same user, while a live control session exists -> rejected.
    with pytest.raises(StreamError) as ei:
        h.mint.mint_control(
            handoff_id=h.handoff_id, user_id=h.user_id, origin=ORIGIN, takeover=False
        )
    assert ei.value.code == "stream_already_connected"

    # Explicit takeover supersedes the old session and bumps the revision.
    resp2 = h.mint.mint_control(
        handoff_id=h.handoff_id, user_id=h.user_id, origin=ORIGIN, takeover=True
    )
    assert resp2.control.control_revision > resp1.control.control_revision
    old = h.gateway.sessions.get(resp1.stream_session_id)
    assert old is not None and old.live is False


# --- Row: stop renewing for 60s -------------------------------------------
def test_lease_expiry_closes_session_input_dead():
    h = make_harness()
    resp = _mint_and_claim(h)
    ch = h.worker_channel()
    # Force the lease to look expired, then a renewal fails and revokes.
    run = h.plane.runs.get(h.run_id)
    run.control_lease_expires_at = time.time() - 1
    sess = h.gateway.sessions.get(resp.stream_session_id)
    with pytest.raises(StreamError) as ei:
        h.gateway.renew(
            stream_session_id=resp.stream_session_id,
            cookie_value=sess.cookie_value,
            control_revision=resp.control.control_revision,
        )
    assert ei.value.code == "control_lease_lost"
    assert ch.input_live is False
    # Handoff still claimable inside the grace window (not returned/cancelled).
    assert run.handoff_returned is False and run.handoff_cancelled is False


# --- Row: grep for secrets — no raw ticket/cookie/turn/worker addr leak ----
def test_no_secret_material_in_responses():
    h = make_harness()
    resp = h.mint.mint_control(
        handoff_id=h.handoff_id, user_id=h.user_id, origin=ORIGIN, takeover=False
    )
    # The ticket itself is the only place the JWT appears; the stored record is a
    # hash, and no session/event echoes the raw ticket, cookie, or TURN secret.
    from matrx_scraper.cloud_browser.streaming.ticket_store import ticket_hash

    store = h.plane.tickets
    # The record is keyed by hash and stores no raw ticket field.
    rec = store._by_hash[ticket_hash(resp.ticket)]
    assert not hasattr(rec, "ticket")
    assert resp.ticket not in repr(rec)
    # The TURN shared secret is never in the client bundle.
    assert h.config.turn_shared_secret not in resp.ice.turn_credential
    assert h.config.turn_shared_secret not in resp.model_dump_json()
    # No worker address/port in the client-visible endpoint or ICE.
    assert h.worker_id not in resp.endpoint
    assert h.worker_id not in resp.model_dump_json()
