# File: matrx_files/blocks/unblock.py
"""What would unblock it — one lawful route per error class this package raises.

Kept in sync BY HAND with the matching entries in `matrx_scraper.blocks.unblock`
(the canonical, platform-wide table) — see `vocabulary.py`'s module docstring
for why this package cannot import that module directly. The wording here is
the SAME sentence, so a person reading the Blocks screen never sees two
different explanations for the identical wall depending on which host wrote
the row.
"""

from __future__ import annotations

from dataclasses import dataclass

__all__ = ["Unblock", "unblock_for"]


@dataclass(frozen=True)
class Unblock:
    route: str | None
    note: str
    #: True when clearing this needs Arman, not an agent (HUNTER-RULES law 6) —
    #: mirrors `matrx_scraper.blocks.unblock.Unblock.is_decision`.
    is_decision: bool = False


_NOTHING = Unblock(route=None, note="", is_decision=False)

_ROUTES: dict[str, Unblock] = {
    "drm_protected": Unblock(
        "decision",
        "The file is copy-protected and we will never strip a publisher's protection. What "
        "does work: the expert's own highlights and notes export, a DRM-free copy from the "
        "publisher, the audiobook, or the library's lending copy.",
        is_decision=True,
    ),
    "unsupported_format": Unblock(
        "convert",
        "We recognise this file but cannot read this format yet. Exporting or saving it as "
        "PDF, EPUB, DOCX or plain text gets it in today.",
    ),
    "empty_file": Unblock(
        None,
        "The file opened but produced no readable words. It may be a scan — in which case the "
        "route is reading the images, not the text layer.",
    ),
    "ocr_binary_missing": Unblock(
        "settings",
        "This scan needs OCR to read, and the OCR engine is not installed on this server. "
        "That is an infrastructure gap, not something about this file — install Tesseract "
        "(or the configured OCR provider) on the host and reprocess.",
    ),
}


def unblock_for(error_class: str) -> Unblock:
    """The lawful route for a class, or an honest blank when we do not know one."""
    return _ROUTES.get(error_class, _NOTHING)
