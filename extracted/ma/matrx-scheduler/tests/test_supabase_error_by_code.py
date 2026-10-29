"""_classify_supabase_error maps the PostgREST / SQLSTATE code, never the message words."""

from __future__ import annotations

from matrx_scheduler.api.router_scheduler import _classify_supabase_error


class _ApiError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def test_codes_decide() -> None:
    assert _classify_supabase_error(_ApiError("42501", "nope"))[0] == 403
    assert _classify_supabase_error(_ApiError("PGRST116", "zero"))[0] == 404
    assert _classify_supabase_error(_ApiError("PGRST301", "bad token"))[0] == 401
    # the old word match turned these into 403/404; words alone decide nothing now
    assert _classify_supabase_error(_ApiError("23505", "permission row not found"))[0] == 400
