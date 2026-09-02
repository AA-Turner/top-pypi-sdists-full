"""Wire-level proof through the standalone FastAPI harness (S4 §10): mint → claim
→ renew → release over real HTTP, asserting the Set-Cookie and the typed-error
HTTP status mapping.
"""

from __future__ import annotations

import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient  # noqa: E402

from matrx_scraper.cloud_browser.streaming.app import build_app  # noqa: E402
from matrx_scraper.cloud_browser.streaming.config import STREAM_COOKIE_NAME  # noqa: E402
from matrx_scraper.cloud_browser.streaming.control_plane import MintService  # noqa: E402
from matrx_scraper.cloud_browser.streaming.gateway import StreamGateway  # noqa: E402

from .harness import ORIGIN, make_harness  # noqa: E402


def _client(h):
    app = build_app(plane=h.plane, gateway=h.gateway, mint=h.mint)
    # https base_url so the Secure, path-scoped stream cookie is stored + resent.
    return TestClient(app, base_url="https://testserver")


def _auth(h):
    return {"Authorization": f"Bearer {h.user_id}", "Origin": ORIGIN}


def test_full_flow_mint_claim_renew_release():
    h = make_harness()
    client = _client(h)
    # mint
    r = client.post(
        f"/browser-manager/handoffs/{h.handoff_id}/stream-ticket",
        json={"takeover": False},
        headers=_auth(h),
    )
    assert r.status_code == 200, r.text
    body = r.json()
    sid = body["stream_session_id"]
    rev = body["control"]["control_revision"]
    assert body["media"]["clipboard"] is False and body["media"]["video"] is True

    # claim -> 204 + Set-Cookie
    r = client.post(f"/stream/{sid}/claim", json={"ticket": body["ticket"]}, headers=_auth(h))
    assert r.status_code == 204, r.text
    set_cookie = r.headers.get("set-cookie", "")
    assert STREAM_COOKIE_NAME in set_cookie and "HttpOnly" in set_cookie

    # renew (cookie carried automatically by the TestClient jar)
    r = client.post(f"/stream/{sid}/renew", json={"control_revision": rev})
    assert r.status_code == 200, r.text
    assert r.json()["next_renew_in_seconds"] == 20

    # release
    r = client.post(
        f"/browser-manager/runs/{h.run_id}/release-control",
        json={"control_revision": rev},
        headers=_auth(h),
    )
    assert r.status_code == 200
    assert r.json()["status"] in ("released", "already_released")


def test_origin_mismatch_maps_to_401():
    h = make_harness()
    client = _client(h)
    r = client.post(
        f"/browser-manager/handoffs/{h.handoff_id}/stream-ticket",
        json={"takeover": False},
        headers=_auth(h),
    )
    body = r.json()
    sid = body["stream_session_id"]
    r = client.post(
        f"/stream/{sid}/claim",
        json={"ticket": body["ticket"]},
        headers={"Authorization": f"Bearer {h.user_id}", "Origin": "https://evil.example"},
    )
    assert r.status_code == 401
    assert r.json()["error"] == "stream_ticket_origin_mismatch"


def test_replay_maps_to_401_and_one_session():
    h = make_harness()
    client = _client(h)
    body = client.post(
        f"/browser-manager/handoffs/{h.handoff_id}/stream-ticket",
        json={"takeover": False},
        headers=_auth(h),
    ).json()
    sid = body["stream_session_id"]
    assert (
        client.post(
            f"/stream/{sid}/claim", json={"ticket": body["ticket"]}, headers=_auth(h)
        ).status_code
        == 204
    )
    r = client.post(f"/stream/{sid}/claim", json={"ticket": body["ticket"]}, headers=_auth(h))
    assert r.status_code == 401
    assert r.json()["error"] == "stream_ticket_already_claimed"
    assert len(h.gateway.sessions.sessions_for_run(h.run_id)) == 1
