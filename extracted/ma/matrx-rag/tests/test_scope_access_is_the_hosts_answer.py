"""A scope-narrowed search asks the HOST which scopes the person may open — lane SCOPES-READS-SERVER.

A scope is a Record of the host's record store; matrx-rag owns no scope table and reads none. The
search keeps exactly the scopes the host's ``scope_access`` seam answers, and with a person and no
seam wired it refuses by name instead of guessing. RED on HEAD: the search read the host's old
``context.scopes`` model (``get_db_model("Scopes")``) and never asked the seam.
"""

from __future__ import annotations

import pytest

from matrx_rag import _ext
from matrx_rag.search import _check_scope_access

MATTER = "5b8e2f4a-6c1d-4e7f-8a9b-0c1d2e3f4a5b"
OTHER_FIRM = "9a8b7c6d-5e4f-4a3b-8c2d-1e0f9a8b7c6d"
PERSON = "87a6e699-3622-4869-8843-d0867456c0dd"


async def test_only_the_scopes_the_host_opens_are_searched(monkeypatch: pytest.MonkeyPatch) -> None:
    asked: list[tuple[list[str], str]] = []

    async def access(scope_ids: list[str], user_id: str) -> list[str]:
        asked.append((scope_ids, user_id))
        return [MATTER]

    monkeypatch.setitem(_ext._registry, "scope_access", access)
    kept = await _check_scope_access(scope_ids=[MATTER, OTHER_FIRM], user_id=PERSON)
    assert kept == [MATTER]
    assert asked == [([MATTER, OTHER_FIRM], PERSON)]


async def test_no_seam_is_a_refusal_not_a_guess(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delitem(_ext._registry, "scope_access", raising=False)
    with pytest.raises(RuntimeError, match="scope_access"):
        await _check_scope_access(scope_ids=[MATTER], user_id=PERSON)


async def test_an_admin_bypass_caller_is_not_narrowed() -> None:
    assert await _check_scope_access(scope_ids=[MATTER], user_id=None) == [MATTER]
