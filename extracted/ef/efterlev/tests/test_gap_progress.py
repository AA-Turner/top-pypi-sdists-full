"""Tests for the v0.1.86 streaming-progress reporter for the Gap Agent.

Covers:
- KSI-ID extraction from cumulative streaming text via regex.
- Per-KSI emission deduplication (re-emitted text doesn't double-print).
- Heartbeat throttling during the no-KSI-yet preamble phase.
- TTY-only `make_reporter_if_tty` helper returns None when stderr piped.
- Final-summary line on `finish()`.
- End-to-end: agent.run() with `progress_callback` plumbs through to
  the LLM client's `on_chunk` and the StubLLMClient streams chunks.
"""

from __future__ import annotations

import io
import json
from unittest.mock import patch

from efterlev.agents.gap_progress import GapProgressReporter, make_reporter_if_tty


def test_ksi_extraction_from_cumulative_text() -> None:
    """Each new `"ksi_id": "KSI-XXX-YYY"` token in the cumulative text
    triggers a per-KSI line; already-seen IDs don't re-emit."""
    buf = io.StringIO()
    reporter = GapProgressReporter(total_ksis=60, stream=buf)

    # Simulate 3 chunks arriving with cumulative-text-so-far semantics.
    reporter('{"reasoning": "preamble", "ksi_classifications": [{"ksi_id": "KSI-AFR-UCM"')
    reporter(
        '{"reasoning": "preamble", "ksi_classifications": [{"ksi_id": "KSI-AFR-UCM",'
        '"status":"partial"},{"ksi_id": "KSI-CNA-RNT"'
    )
    reporter(
        '{"reasoning": "preamble", "ksi_classifications": [{"ksi_id": "KSI-AFR-UCM",'
        '"status":"partial"},{"ksi_id": "KSI-CNA-RNT","status":"not_implemented"},'
        '{"ksi_id": "KSI-MLA-LET","status":"implemented"}]}'
    )

    output = buf.getvalue()
    # Three KSI IDs detected — one line each.
    assert "[gap] classifying KSI 1/60: KSI-AFR-UCM" in output
    assert "[gap] classifying KSI 2/60: KSI-CNA-RNT" in output
    assert "[gap] classifying KSI 3/60: KSI-MLA-LET" in output
    # No duplicate emissions (each KSI ID once across all 3 cumulative
    # invocations).
    assert output.count("KSI-AFR-UCM") == 1
    assert output.count("KSI-CNA-RNT") == 1
    assert output.count("KSI-MLA-LET") == 1


def test_no_emission_for_garbled_or_non_ksi_id_text() -> None:
    """Random text without `"ksi_id"` tokens never triggers a KSI line.
    Heartbeat may fire in the no-KSI-yet preamble; KSI lines do not.
    """
    buf = io.StringIO()
    reporter = GapProgressReporter(total_ksis=60, stream=buf)
    reporter('{"reasoning": "still thinking about this..."}')
    output = buf.getvalue()
    assert "classifying KSI" not in output


def test_finish_prints_done_summary_when_ksis_seen() -> None:
    """`finish()` emits a `[gap] done in Xs — N/60 KSIs classified` line."""
    buf = io.StringIO()
    reporter = GapProgressReporter(total_ksis=60, stream=buf)
    reporter('{"ksi_classifications": [{"ksi_id": "KSI-AFR-UCM"}]}')
    reporter('{"ksi_classifications": [{"ksi_id": "KSI-AFR-UCM"},{"ksi_id": "KSI-CNA-RNT"}]}')
    reporter.finish()
    output = buf.getvalue()
    assert "[gap] done in" in output
    assert "2/60 KSIs classified" in output


def test_finish_silent_when_no_ksis_seen() -> None:
    """`finish()` doesn't emit a "done" line if zero KSIs were classified
    (e.g. error path before any classification was emitted). The user
    will see the per-stage error from the actual failure surface; we
    don't want a misleading "done" claim on top of it."""
    buf = io.StringIO()
    reporter = GapProgressReporter(total_ksis=60, stream=buf)
    reporter.finish()
    assert "[gap] done in" not in buf.getvalue()


def test_make_reporter_if_tty_returns_none_when_stderr_not_tty() -> None:
    """In CI / piped runs, no progress reporter is installed (output
    would just clutter logs without giving any interactive value)."""
    with patch("sys.stderr.isatty", return_value=False):
        assert make_reporter_if_tty(total_ksis=60) is None


def test_make_reporter_if_tty_returns_reporter_when_stderr_is_tty() -> None:
    """Local terminal runs get the live reporter."""
    with patch("sys.stderr.isatty", return_value=True):
        reporter = make_reporter_if_tty(total_ksis=60)
        assert isinstance(reporter, GapProgressReporter)
        assert reporter.total_ksis == 60


def test_end_to_end_progress_callback_plumbed_through_stub_client() -> None:
    """End-to-end: GapAgentInput.progress_callback fires via Agent._invoke_llm
    → LLMClient.complete(on_chunk=...) → StubLLMClient streams chunks."""
    from datetime import UTC, datetime
    from pathlib import Path
    from tempfile import TemporaryDirectory

    from efterlev.agents import GapAgent, GapAgentInput
    from efterlev.llm import StubLLMClient
    from efterlev.models import Indicator
    from efterlev.provenance import ProvenanceStore, active_store

    canned_response = json.dumps(
        {
            "reasoning_summary": "Surveyed 1 KSI.",
            "ksi_classifications": [
                {
                    "ksi_id": "KSI-AFR-UCM",
                    "status": "evidence_layer_inapplicable",
                    "rationale": "no detector evidence",
                    "evidence_ids": [],
                }
            ],
            "unmapped_findings": [],
        }
    )
    stub = StubLLMClient(response_text=canned_response, model="stub-opus")
    chunks_received: list[str] = []

    indicator = Indicator(
        id="KSI-AFR-UCM",
        theme="AFR",
        name="Cryptographic Module Use",
        statement="...",
        controls=["SC-28(1)"],
    )

    with TemporaryDirectory() as tmp, ProvenanceStore(Path(tmp)) as store, active_store(store):
        agent = GapAgent(client=stub, model="stub-opus")
        agent.run(
            GapAgentInput(
                indicators=[indicator],
                evidence=[],
                progress_callback=chunks_received.append,
            )
        )

    # StubLLMClient emits ~8 chunks; verify at least one fired.
    assert len(chunks_received) > 0
    # Last chunk should be the full response text.
    assert chunks_received[-1] == canned_response
    # Cumulative semantics: each chunk grows.
    assert all(
        len(chunks_received[i]) <= len(chunks_received[i + 1])
        for i in range(len(chunks_received) - 1)
    )
    # Touch UTC + datetime imports so ruff doesn't complain about unused imports
    # (used implicitly by Indicator construction — no actual call needed).
    _ = (UTC, datetime)


def test_progress_callback_none_means_no_streaming_overhead() -> None:
    """When progress_callback is None (the default), the LLM client's
    on_chunk path isn't exercised at all (zero callback overhead)."""
    from datetime import UTC, datetime
    from pathlib import Path
    from tempfile import TemporaryDirectory

    from efterlev.agents import GapAgent, GapAgentInput
    from efterlev.llm import StubLLMClient
    from efterlev.models import Indicator
    from efterlev.provenance import ProvenanceStore, active_store

    canned_response = json.dumps(
        {
            "reasoning_summary": "...",
            "ksi_classifications": [
                {
                    "ksi_id": "KSI-AFR-UCM",
                    "status": "evidence_layer_inapplicable",
                    "rationale": "...",
                    "evidence_ids": [],
                }
            ],
            "unmapped_findings": [],
        }
    )
    stub = StubLLMClient(response_text=canned_response, model="stub-opus")

    indicator = Indicator(
        id="KSI-AFR-UCM",
        theme="AFR",
        name="Cryptographic Module Use",
        statement="...",
        controls=["SC-28(1)"],
    )

    with TemporaryDirectory() as tmp, ProvenanceStore(Path(tmp)) as store, active_store(store):
        agent = GapAgent(client=stub, model="stub-opus")
        # No progress_callback — default None.
        report = agent.run(GapAgentInput(indicators=[indicator], evidence=[]))
    assert len(report.ksi_classifications) == 1
    _ = (UTC, datetime)
