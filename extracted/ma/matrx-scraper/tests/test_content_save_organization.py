"""`/ext/content/save` stores a parsed page — so it names its tenant.

The row it writes (`scraper.scrape_parsed_page`) is organization-scoped, and
the organization is already on the wire for every call this host admits
(`X-Organization-Id`, matrx_connect.service_auth). The route resolves it at the
boundary and hands it to the cache; a context without one is refused there
rather than defaulted below it.
"""

from __future__ import annotations

import importlib
from types import SimpleNamespace
from typing import Any

import pytest
from fastapi import HTTPException

ext_router = importlib.import_module("matrx_scraper.api.ext_router")

ORG_ID = "7f1d7b9e-3c9a-4a6d-9c3b-2a4b6d8e0f11"


def _ctx(organization_id: str | None = ORG_ID) -> SimpleNamespace:
    return SimpleNamespace(
        organization_id=organization_id,
        user_id="",
        auth_type="token",
        is_authenticated=True,
    )


class RecordingCache:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def set(self, **kwargs: Any) -> None:
        self.calls.append(kwargs)


def _request() -> Any:
    return ext_router.ContentSaveRequest(
        url="https://example.com/a",
        page_name="example_com__a",
        content={"text": "hello"},
        content_type="html",
        char_count=5,
    )


@pytest.mark.asyncio
async def test_content_save_stores_under_the_admitted_organization(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    cache = RecordingCache()
    # ext_router binds `has_ext`/`get_ext` at import, so the patch goes on the
    # router module's own names.
    monkeypatch.setattr(ext_router, "has_ext", lambda _name: True)
    monkeypatch.setattr(ext_router, "get_ext", lambda _name: cache)

    result = await ext_router.content_save(request=_request(), ctx=_ctx())

    assert result["status"] == "saved"
    assert cache.calls[0]["organization_id"] == ORG_ID


@pytest.mark.asyncio
async def test_content_save_refuses_a_context_with_no_organization(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    cache = RecordingCache()
    # ext_router binds `has_ext`/`get_ext` at import, so the patch goes on the
    # router module's own names.
    monkeypatch.setattr(ext_router, "has_ext", lambda _name: True)
    monkeypatch.setattr(ext_router, "get_ext", lambda _name: cache)

    with pytest.raises(HTTPException) as excinfo:
        await ext_router.content_save(request=_request(), ctx=_ctx(organization_id=None))

    assert excinfo.value.detail["code"] == "organization_required"
    assert cache.calls == []
