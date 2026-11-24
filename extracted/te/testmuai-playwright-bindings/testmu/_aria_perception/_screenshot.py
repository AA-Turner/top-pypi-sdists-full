"""Engine-neutral screenshot (no ``Page.captureScreenshot``)."""
from __future__ import annotations

import asyncio
import base64
import contextlib

# Firefox can leave document.fonts.status 'loading' forever, and
# page.screenshot waits on fonts.ready; loading a missing face settles it.
_FONTS_NUDGE_JS = "async () => { if (document.fonts.status !== 'loading') return; const face = new FontFace('testmu-fonts-nudge', 'local(testmu-fonts-nudge-missing)'); document.fonts.add(face); try { await face.load(); } catch (e) {} document.fonts.delete(face); }"


async def nudge_fonts(page, *, timeout_s: float = 2.0) -> None:
    """Settle a stuck ``document.fonts`` before a screenshot. Bounded; errors ignored."""
    with contextlib.suppress(Exception):
        await asyncio.wait_for(page.evaluate(_FONTS_NUDGE_JS), timeout_s)


async def screenshot_png_b64(page, *, full_page: bool = False) -> str:
    """PNG screenshot of the page in CSS pixels, base64-encoded."""
    data = await page.screenshot(type="png", scale="css", full_page=full_page)
    return base64.b64encode(data).decode("ascii")
