"""Backfill scripts — idempotent, resumable maintenance jobs.

Portable: each entry-point takes a configured ``FileManager`` rather
than reaching into host wiring. Hosts run them via thin CLI wrappers
that bootstrap their own settings + context.
"""

from .rekey import rekey_one_file, run_rekey_backfill
from .restamp_headers import run_restamp_headers_backfill
from .thumbnails import run_thumbnail_backfill

__all__ = [
    "rekey_one_file",
    "run_rekey_backfill",
    "run_restamp_headers_backfill",
    "run_thumbnail_backfill",
]
