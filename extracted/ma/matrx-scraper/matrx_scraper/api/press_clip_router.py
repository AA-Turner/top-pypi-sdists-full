"""A narrow authenticated rendering door for press clips."""
from __future__ import annotations
import base64
from typing import Any, Literal
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from matrx_scraper.ai_browser.url_guard import UnsafeUrlError
from matrx_scraper.press_clip.renderer import render_clip_document

router = APIRouter()

class PressClipRenderRequest(BaseModel):
    url: str
    client_name: str = ""
    scope: Literal["whole", "section"] = "whole"
    section_heading: str | None = None
    drop: list[str] = Field(default_factory=list)
    keep: list[str] = Field(default_factory=list)
    root: str | None = None
    logo_url: str | None = None

@router.post("/press-clips/render", summary="Render a cookie-free press clip")
async def render_press_clip(body: PressClipRenderRequest) -> dict[str, Any]:
    try:
        rendered = await render_clip_document(**body.model_dump())
    except UnsafeUrlError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"press clip render failed: {type(exc).__name__}: {exc}") from exc
    return {"pdf_base64": base64.b64encode(rendered.pdf).decode(), "preview_png_base64": base64.b64encode(rendered.preview_png).decode(), "page_rasters_base64": [base64.b64encode(p).decode() for p in rendered.page_rasters], "logo": {"source": rendered.logo.source, "url": rendered.logo.url, "svg": rendered.logo.svg, "notes": rendered.logo.notes}, "meta": rendered.meta, "report": rendered.report, "blocked_request_count": rendered.blocked_request_count, "blocked_hosts": rendered.blocked_hosts, "scope_applied": rendered.scope_applied, "final_url": rendered.final_url, "notes": rendered.notes}
