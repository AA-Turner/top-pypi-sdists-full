"""Checks on the tracked ``report.pdf`` fixture at the repository root.

WHY THESE TESTS CHANGED
-----------------------
They used a bare relative ``Path("report.pdf")``, which resolves against the
CURRENT WORKING DIRECTORY of the pytest process. That made them silently
order-dependent: ``tests/real_functional_suite/test_cli_core.py`` called
``os.chdir(tmp_path)`` without ever restoring it, so once that test had run in a
worker, every later relative path in the same process pointed inside a pytest
temp directory. These two tests then failed with "report.pdf was not created"
while passing perfectly in isolation -- which reads as flakiness but was in fact
deterministic, ordering-dependent breakage.

The ``os.chdir`` leak is fixed at its source (that test now uses
``monkeypatch.chdir``, which restores at teardown). These tests are additionally
anchored to the repository root so that no future stray ``chdir`` anywhere in the
suite can break them again. A test that silently depends on the process-wide cwd
is not testing what it claims to test.

Note also that the previous docstring claimed to "verify that report.pdf is
created". Nothing in this suite creates it -- it is a git-TRACKED 480-byte
fixture committed at the repo root. The assertions below say what is actually
being checked, so nobody reads this file as proof that report generation ran.
"""

from pathlib import Path

import pytest

# tests/test_report_generation.py -> repo root is one level up from tests/.
# Anchored to THIS FILE, never to the process cwd.
_REPO_ROOT = Path(__file__).resolve().parent.parent
_REPORT_PDF = _REPO_ROOT / "report.pdf"


def test_report_pdf_fixture_exists_and_is_not_empty():
    """The tracked report.pdf fixture is present and has content."""
    assert _REPORT_PDF.exists(), (
        f"tracked fixture {_REPORT_PDF} is missing. It is committed to the repo; "
        "restore it with: git checkout -- report.pdf"
    )
    assert _REPORT_PDF.stat().st_size > 0, f"{_REPORT_PDF} is empty"


def test_report_pdf_contains_expected_text():
    """The fixture PDF still contains its expected literal text.

    Read as bytes deliberately: this is a flat, uncompressed PDF, so the literal
    appears in the raw stream. If the fixture is ever regenerated with
    compression this will need a real parser (e.g. pypdf) rather than a
    substring check -- the assertion message says so, so the next person is not
    left guessing.
    """
    if not _REPORT_PDF.exists():
        pytest.skip(
            f"tracked fixture {_REPORT_PDF} is missing; "
            "restore it with: git checkout -- report.pdf"
        )
    content = _REPORT_PDF.read_bytes()
    assert b"Quarterly results" in content, (
        "'Quarterly results' not found in the raw bytes of "
        f"{_REPORT_PDF}. If the fixture was regenerated with stream compression, "
        "parse it with pypdf instead of doing a byte-substring check."
    )
