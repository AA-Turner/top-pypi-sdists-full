"""POST /files/session survives third-party-cookie blocking (CHIPS).

The durable private render lane is a cookie on the files host
(``files.matrxserver.com`` / ``server.app.matrxserver.com``) set from the
app origin (``aimatrx.com``) — by definition a THIRD-PARTY cookie. Any
browser mode that blocks third-party cookies (Chrome with the setting on,
Chrome Incognito, Safari always, Brave always) discards the ``Set-Cookie``
at mint time; the mint still answers 200, so nothing on either side
notices, and every private ``<img>`` 401s forever (Arman's Chrome,
2026-09-16, ``chat/4b332114``: mint 200 + 200, render 401, re-mint 200,
render 401 — "Image unavailable").

The only cookie such a browser will store and send for a cross-site
``<img>`` is a CHIPS-partitioned one (``Partitioned`` attribute, keyed by
the embedding top-level site). The mint therefore emits the cookie TWICE:
the classic unpartitioned shape (top-level opens, older engines that ignore
``Partitioned``) and the partitioned shape. Same name, same value; a
browser without CHIPS support treats the second as an overwrite of the
first, which is harmless.
"""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from matrx_connect.middleware import session_cookie as sc
from matrx_connect.middleware.session_cookie import (
    SESSION_COOKIE_NAME,
    register_session_cookie_secret,
)

from matrx_files.api.router_files import build_file_router


@pytest.fixture(autouse=True)
def _isolate_registered_secret():
    saved = (sc._registered_secret, sc._registered_secret_is_ephemeral)
    yield
    sc._registered_secret, sc._registered_secret_is_ephemeral = saved


def _client() -> TestClient:
    app = FastAPI()
    app.include_router(build_file_router(file_service=None))
    return TestClient(app)


def test_mint_emits_a_partitioned_copy_of_the_session_cookie() -> None:
    register_session_cookie_secret(b"one-stable-secret-on-every-container")
    resp = _client().post("/files/session")
    assert resp.status_code == 200

    set_cookies = resp.headers.get_list("set-cookie")
    ours = [h for h in set_cookies if h.startswith(f"{SESSION_COOKIE_NAME}=")]
    assert len(ours) == 2, set_cookies

    unpartitioned = [h for h in ours if "Partitioned" not in h]
    partitioned = [h for h in ours if "Partitioned" in h]
    assert len(unpartitioned) == 1 and len(partitioned) == 1, ours

    # Same value in both shapes — one signature, one identity.
    value_of = lambda h: h.split(";", 1)[0]  # noqa: E731
    assert value_of(unpartitioned[0]) == value_of(partitioned[0])

    # CHIPS preconditions: a partitioned cookie MUST be Secure + SameSite=None
    # (+ HttpOnly, Path=/ for the lane's own contract).
    for h in ours:
        assert "Secure" in h
        assert "SameSite=None" in h
        assert "HttpOnly" in h
        assert "Path=/" in h
