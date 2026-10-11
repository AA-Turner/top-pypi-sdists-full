"""Unit tests for in-memory seed file builders."""

from __future__ import annotations

import io
import zipfile

from tests.fixtures.seed_file_assets import all_seed_files, build_pdf_variants


def test_all_seed_files_count_and_archives():
    files = all_seed_files()
    assert len(files) == 12
    by_ext = {f.filename.split(".")[-1] for f in files}
    assert by_ext == {"pdf", "png", "jpeg", "svg", "docx", "xlsx"}


def test_office_zips_are_valid():
    for sf in all_seed_files():
        if sf.filename.endswith((".docx", ".xlsx")):
            z = zipfile.ZipFile(io.BytesIO(sf.content))
            assert z.testzip() is None


def test_pdf_variants_differ_in_size():
    a, b, c = build_pdf_variants()
    sizes = {len(a.content), len(b.content), len(c.content)}
    assert len(sizes) >= 2
