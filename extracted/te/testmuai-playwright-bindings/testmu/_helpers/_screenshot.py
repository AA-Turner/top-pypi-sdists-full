"""Internal helper: wait briefly then take a page screenshot.

Single source of truth for binding screenshot defaults. Used by every
binding code path that screenshots the page (vision, wait, assertion,
autoheal). Not exported on the testmu namespace — internal use only
(leading underscore).

Defaults:
- 300ms settle gives in-flight animations / lazy reflows a chance to land
- timeout=60000ms (over Playwright's 30s default — large/animated DOMs
  occasionally exceed it on a settling screenshot)
- type="jpeg", quality=80 (smaller payloads for vision-API uploads)
- scale="css" (CSS pixels, not device pixels — consistent dimensions
  across HiDPI and SD runners)
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Literal, Sequence

_DEFAULT_TIMEOUT_MS = 60_000
_DEFAULT_QUALITY = 80
_SETTLE_MS = 300


async def take_screenshot(
    page,
    *,
    full_page: bool = False,
    timeout: float = _DEFAULT_TIMEOUT_MS,
    type: Literal["jpeg", "png"] = "jpeg",
    quality: int = _DEFAULT_QUALITY,
    scale: Literal["css", "device"] = "css",
    path: str | Path | None = None,
    omit_background: bool | None = None,
    clip: Any = None,
    animations: Literal["allow", "disabled"] | None = None,
    caret: Literal["hide", "initial"] | None = None,
    mask: Sequence[Any] | None = None,
    mask_color: str | None = None,
    style: str | None = None,
) -> bytes:
    """Page.screenshot with binding defaults. Returns raw bytes."""
    await page.wait_for_timeout(_SETTLE_MS)
    q = quality if type == "jpeg" else None
    omit_bg = omit_background if type == "png" else None
    return await page.screenshot(
        full_page=full_page,
        timeout=timeout,
        type=type,
        quality=q,
        scale=scale,
        path=path,
        omit_background=omit_bg,
        clip=clip,
        animations=animations,
        caret=caret,
        mask=mask,
        mask_color=mask_color,
        style=style,
    )
