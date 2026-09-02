"""Quick site preview HTTP API.

Exposes `matrx_scraper.preview.quick_preview` over HTTP so aidream and any
other host can get a robots + homepage SEO + screenshot summary without
running Playwright themselves. Same payload shape as the in-process call.

Mounted under `Depends(require_authenticated)` in matrx_scraper.server.app —
admin-tier callers (e.g. aidream's /scraper/admin/preview) will be allowed
through with their existing JWT/admin token.

The SSRF gate lives inside `quick_preview` itself (pre-validate the target,
re-validate the final url after httpx redirects and after the browser
navigates), so direct Python callers get it too. A blocked target returns the
function's normal `{"ok": False, "error": ...}` shape.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from matrx_scraper.preview import quick_preview

router = APIRouter()


class PreviewRequest(BaseModel):
    url: str = Field(
        ..., description="URL to preview; will be normalised (so 'abc.com' → 'https://abc.com/')"
    )


@router.post(
    "/preview", summary="Quick site preview: robots + homepage SEO audit + desktop screenshot"
)
async def preview(body: PreviewRequest) -> dict[str, Any]:
    return await quick_preview(body.url)
