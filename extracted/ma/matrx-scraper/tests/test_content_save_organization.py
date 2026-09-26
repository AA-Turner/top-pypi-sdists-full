"""`/ext/content/save` lands a parsed page as a Source — so it names its tenant.

The Source it creates (a `docproc.processed_documents` row and its identity row in
`scraper.scrape_parsed_page`) is organization-scoped, and the organization is already on the wire
for every call this host admits (`X-Organization-Id`, matrx_connect.service_auth). The route
resolves it at the boundary and hands it to the landing door; a context without one is refused
there rather than defaulted below it. (SOURCE-CONVERGENCE §4.4: the save no longer writes the page
cache — the landing is the save.)
"""

from __future__ import annotations

import importlib
from types import SimpleNamespace
from typing import Any

import pytest
from fastapi import HTTPException

from matrx_scraper import _ext

ext_router = importlib.import_module("matrx_scraper.api.ext_router")

ORG_ID = "7f1d7b9e-3c9a-4a6d-9c3b-2a4b6d8e0f11"
USER_ID = "4cf62e4e-2679-484a-a652-8ee8ce4ef9f2"


def _ctx(organization_id: str | None = ORG_ID) -> SimpleNamespace:
    return SimpleNamespace(
        organization_id=organization_id,
        user_id=USER_ID,
        auth_type="token",
        is_authenticated=True,
    )


class RecordingHook:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    async def __call__(self, landing: dict[str, Any]) -> dict[str, Any]:
        self.calls.append(landing)
        return {"processed_document_id": "doc-1", "source_id": "spp-1", "notices": []}


def _request() -> Any:
    return ext_router.ContentSaveRequest(
        url="https://example.com/a",
        page_name="example_com__a",
        content={"text_data": "hello"},
        content_type="html",
        char_count=5,
    )


@pytest.fixture
def hook(monkeypatch: pytest.MonkeyPatch) -> RecordingHook:
    recording = RecordingHook()
    monkeypatch.setattr(_ext, "_registry", {"source_landing": recording})
    return recording


@pytest.mark.asyncio
async def test_content_save_lands_under_the_admitted_organization(hook: RecordingHook) -> None:
    result = await ext_router.content_save(request=_request(), ctx=_ctx())

    assert result["status"] == "saved"
    assert result["processed_document_id"] == "doc-1"
    assert hook.calls[0]["organization_id"] == ORG_ID


@pytest.mark.asyncio
async def test_content_save_refuses_a_context_with_no_organization(hook: RecordingHook) -> None:
    with pytest.raises(HTTPException) as excinfo:
        await ext_router.content_save(request=_request(), ctx=_ctx(organization_id=None))

    assert excinfo.value.detail["code"] == "organization_required"
    assert hook.calls == []
