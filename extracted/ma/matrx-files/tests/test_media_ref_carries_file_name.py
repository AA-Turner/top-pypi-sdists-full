"""A resolved file reference keeps the file's own name beside its bytes (real test PB-05)."""

from __future__ import annotations

from matrx_files.cloud_sync._media_resolution import _carry_file_name
from matrx_files.cloud_sync.media_ref import MediaRef


def test_resolution_carries_the_file_name():
    ref = MediaRef(file_id="e820ba04-0fdc-4adf-a139-e98601e6339a")
    _carry_file_name(ref, {"file_name": "handover-note.docx"})
    assert ref.metadata["file_name"] == "handover-note.docx"


def test_first_name_wins_over_a_variant_row():
    ref = MediaRef(file_id="4e01f58b-704a-4ac1-86f5-11b32c5cbf92", metadata={"file_name": "IMG_2291.jpg"})
    _carry_file_name(ref, {"file_name": "eda53aff-8ed2-4238-a128-09c348aaac01.jpg"})
    assert ref.metadata["file_name"] == "IMG_2291.jpg"
