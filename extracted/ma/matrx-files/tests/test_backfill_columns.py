"""Forcing-function test: the backfill's column list IS the generator's row.

The backfill selects a fixed column tuple (``_BACKFILL_COLUMNS``) and hands
the resulting dict to ``generate_thumbnail_for_file(record=...)``, which
never re-reads the row. So the tuple is the generator's entire view of the
file.

That coupling fails SILENTLY. A column the generator reads but the backfill
never selected does not raise — ``record.get("x")`` just returns ``None``
and the generator takes the wrong branch. Two live instances of this exact
class already shipped:

  - ``owner_id`` — absent from a bare DB row; blew up only on the WRITE
    path, so the whole universal backfill was inert while printing DONE
    (2026-08-08, now reconciled in ``_reconcile_owner_id``).
  - ``size_bytes`` — never selected, so ``use_streaming`` was always False
    and the Phase 6b bounded-memory path was dead for every backfilled
    row: the backfill read multi-GB media whole into RAM where the upload
    path streamed it to a temp file.

Neither produced an error message. This test is the layer that does.
"""

from __future__ import annotations

import re

from matrx_utils.source_guard import stable_source

from matrx_files.cloud_sync.backfill.thumbnails import _BACKFILL_COLUMNS
from matrx_files.cloud_sync.processing import thumbnails as _generator

# Read the generator through the IMPORT system, never a source-tree relative
# path. The independence gate installs this package into a bare venv and runs
# tests/ from a temp dir with no repo checkout beside it, so
# ``Path(__file__).parents[1] / "matrx_files" / …`` does not exist there.
# stable_source (inspect-based) works in both places.

# Keys the generator reads that are deliberately NOT selectable columns.
# Each needs a reason — an unexplained entry here is how a real omission
# gets waved through.
_NOT_COLUMNS = {
    # Consolidated into ``storage_uri`` by cloud_sync migration 007. The
    # generator still probes it first for pre-migration callers; there is
    # no such column to select.
    "canonical_storage_uri",
    # Python-side name for the DB's ``created_by``. The read-path shim in
    # db.py maps it; the backfill selects ``created_by`` and
    # ``_reconcile_owner_id`` derives it.
    "owner_id",
}


def _keys_read_by_generator() -> set[str]:
    src = stable_source(_generator)
    return set(re.findall(r'record\.get\("([a-z_]+)"\)', src)) | set(
        re.findall(r'record\["([a-z_]+)"\]', src)
    )


def test_generator_reads_nothing_the_backfill_does_not_select():
    read = _keys_read_by_generator()
    assert read, "regex found no record reads — the scan broke, not the code"

    missing = sorted(read - set(_BACKFILL_COLUMNS) - _NOT_COLUMNS)

    assert not missing, (
        f"cloud_sync/processing/thumbnails.py reads {missing} off the record, "
        f"but cloud_sync/backfill/thumbnails.py::_BACKFILL_COLUMNS never selects "
        f"it. This does NOT raise — the generator sees None and silently takes "
        f"the wrong branch for every backfilled row. Add the column to "
        f"_BACKFILL_COLUMNS, or add it to _NOT_COLUMNS here WITH a reason if it "
        f"is genuinely not a column."
    )


def test_size_bytes_is_selected_so_the_bounded_memory_path_can_arm():
    """Named explicitly: this one was missing and cost the streaming path.

    ``_generate_impl`` gates the Phase 6b temp-file path on
    ``record.get("size_bytes") >= LARGE_MEDIA_THRESHOLD_BYTES``. Unselected,
    that comparison is always ``0 >= threshold`` — False forever.
    """
    assert "size_bytes" in _BACKFILL_COLUMNS, (
        "without size_bytes the backfill reads every large file whole into "
        "memory; LARGE_MEDIA_THRESHOLD_BYTES becomes dead code"
    )
