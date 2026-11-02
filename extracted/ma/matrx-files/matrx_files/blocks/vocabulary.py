# File: matrx_files/blocks/vocabulary.py
"""The closed vocabulary this package's block announcements use.

The canonical, platform-wide vocabulary is `matrx_scraper.blocks.vocabulary`
(engines, source types) — repeated here, not duplicated by accident, for the
same reason `matrx_scraper.blocks.vocabulary` repeats the database's CHECK
constraints: matrx-files cannot import matrx-scraper (independence boundary,
`matrx-files/CLAUDE.md`), so when this package IS the host writing the row
(the standalone `matrx_files.standalone.app` service), it needs its own
closed set to refuse an unrecognised token before it reaches the database.

`ENGINE` and `SOURCE_TYPE` are the SAME two tokens matrx_scraper's canonical
vocabulary already reserves for file readers (`"file_reader"` / `"file"`) —
this package only ever writes those two, so a row this store creates and a
row aidream's richer sink creates for the identical wall look identical on
the Blocks screen.

`ERROR_CLASSES` is the set this package's own codec refusals actually raise.
Adding a new one here is a two-place change: mirror the lawful route in
`unblock.py`, and (if a human should read a friendlier sentence when the
SAME error class is announced through aidream's richer sink) add the same
key to `matrx_scraper.blocks.unblock`'s `_ROUTES`.
"""

from __future__ import annotations

__all__ = ["ENGINE", "SOURCE_TYPE", "ERROR_CLASSES"]

#: This package announces as exactly one engine — matrx_scraper's canonical
#: `"file_reader"` token.
ENGINE = "file_reader"

#: ...against exactly one source type — matrx_scraper's canonical `"file"` token.
SOURCE_TYPE = "file"

#: The refusals this package's own readers can raise. Free text error classes
#: are technically accepted downstream (matrx_scraper's `record_block` does not
#: enforce a closed error-class vocabulary — only engine/source_type/rung), but
#: THIS store enforces one anyway: an error class this package never named is
#: very likely a caller typo, and refusing it loudly here is cheaper than a
#: mystery row on the Blocks screen with a blank lawful route.
ERROR_CLASSES: tuple[str, ...] = (
    "drm_protected",
    "unsupported_format",
    "empty_file",
    "ocr_binary_missing",
)
