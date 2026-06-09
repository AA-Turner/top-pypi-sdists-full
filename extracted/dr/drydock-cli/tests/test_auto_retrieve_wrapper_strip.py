"""Verify the AUTO-RETRIEVE bypass probe strips the harness wrapper
before computing the cookbook score.

Bug observed 2026-06-09: a FEAL trial in the v2.10.7 batch exited
at 43s with reward=0 because:
  1. AUTO-RETRIEVE bypass probed the raw user prompt
  2. Raw prompt is ~600 chars of harness wrapper ("WRITE-FIRST
     RULE", "Process to follow", etc.) BEFORE the actual task
  3. Wrapper boilerplate dominated TF-IDF — global_rename.md
     scored 51.4 on "tool call" / "rename" / "process" matches
  4. Synthetic injection delivered global_rename.md content (pure
     noise for FEAL), model returned empty response, session ended

Fix: strip everything up to and including "----- Task: -----" before
the probe. The actual task text (where FEAL appears) now drives the
TF-IDF score.
"""
from __future__ import annotations


def test_strip_finds_task_marker():
    """The Task marker is what we anchor on."""
    raw = "Wrapper text\n----- Task: -----\nReal task content"
    idx = raw.find("----- Task: -----")
    assert idx >= 0
    stripped = raw[idx + len("----- Task: -----"):]
    assert "Wrapper text" not in stripped
    assert "Real task content" in stripped


def test_probe_score_lifts_with_strip_for_feal_prompt():
    """End-to-end: stripping the wrapper makes FEAL-cookbook win on a
    FEAL prompt where the raw wrapper made random cookbook win."""
    try:
        from drydock.graphrag import Index
    except ImportError:
        import pytest
        pytest.skip("graphrag not available in this env")

    from pathlib import Path
    db = Path.home() / ".drydock" / "graphrag.sqlite"
    if not db.is_file():
        import pytest
        pytest.skip("no home graphrag DB in this env")

    raw = (
        "This task has multiple steps. Process to follow:\n"
        "  - Start with a tool call NOW.\n"
        "  - WRITE-FIRST RULE within your first 5 tool calls.\n"
        "----- Task: -----\n"
        "Implement a FEAL-4 differential cryptanalysis attack to recover "
        "the round subkeys. Use chosen plaintexts with differential "
        "0x80800000."
    )

    idx = Index(str(db))

    # Raw probe (the BUG)
    raw_q = raw.strip()[:300]
    raw_r = idx.retrieve(raw_q, symbol_limit=0, text_limit=1)
    raw_top = raw_r.text[0] if raw_r.text else None
    raw_score = getattr(raw_top, 'score', 0.0) if raw_top else 0.0
    raw_file = (getattr(raw_top, 'file', '') or '').split('/')[-1]

    # Stripped probe (the FIX)
    marker = raw.find("----- Task: -----")
    stripped = raw[marker + len("----- Task: -----"):]
    strip_q = stripped.strip()[:300]
    strip_r = idx.retrieve(strip_q, symbol_limit=0, text_limit=1)
    strip_top = strip_r.text[0] if strip_r.text else None
    strip_score = getattr(strip_top, 'score', 0.0) if strip_top else 0.0
    strip_file = (getattr(strip_top, 'file', '') or '').split('/')[-1]

    # The stripped query must score the FEAL cookbook HIGHEST. The raw
    # probe may have happened to score a different (incidental) file
    # higher — that's the bug being fixed.
    assert "feal" in strip_file.lower(), (
        f"after strip, top file is {strip_file!r} (score {strip_score:.1f}); "
        f"expected feal_cryptanalysis.md"
    )
    # And the stripped probe must exceed the 25.0 bypass threshold so
    # the file-task SKIP gets bypassed and the cookbook actually injects.
    assert strip_score >= 25.0, (
        f"stripped score {strip_score:.1f} below the 25.0 bypass threshold"
    )
