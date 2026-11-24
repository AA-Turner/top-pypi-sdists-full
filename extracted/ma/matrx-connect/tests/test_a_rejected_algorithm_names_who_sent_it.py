"""A token refused for its algorithm still says whose it claims to be.

Live 2026-11-06: 275 "JWT alg='HS256' not in allow-list" lines a day, none naming a caller,
so the client still holding a legacy-secret token could not be found.
"""

from __future__ import annotations

import jwt as pyjwt

from matrx_connect.middleware.auth.jwt import JwtLane


def _origin(token: str) -> str:
    return JwtLane._unverified_origin(token, pyjwt.get_unverified_header(token))


def test_a_refused_token_names_its_issuer_and_role_but_never_the_token() -> None:
    token = pyjwt.encode(
        {"iss": "https://db.matrxserver.com/auth/v1", "role": "authenticated", "sub": "u-1"},
        "x" * 32,
        algorithm="HS256",
    )
    out = _origin(token)
    assert "iss='https://db.matrxserver.com/auth/v1'" in out
    assert "role='authenticated'" in out
    assert token not in out


def test_an_undecodable_token_adds_nothing() -> None:
    assert JwtLane._unverified_origin("not-a-jwt", {}) == ""
