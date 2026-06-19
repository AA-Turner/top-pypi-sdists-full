"""Tests for the CLI-command-count and LLM-backend-count rules in
`scripts/check-docs.py::check_doc` (added 2026-06-14).

Bug class: prose numeric claims that nothing previously gate-asserted.
The README drifted to "46 CLI commands" (runtime 57) and "Three LLM
backends" (LLMConfig admits 5 after the OpenAI v0.1.213 + bedrock_openai
v0.1.217 backends shipped). CLI_REFERENCE_RE validated that *named*
commands exist but never the count; backends had no rule at all. These
two rules pin both numbers to their runtime sources.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_check_docs():
    path = REPO_ROOT / "scripts" / "check-docs.py"
    spec = importlib.util.spec_from_file_location("check_docs", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["check_docs"] = module
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def cd(monkeypatch: pytest.MonkeyPatch, tmp_path: Path):
    module = _load_check_docs()
    monkeypatch.setattr(module, "REPO_ROOT", tmp_path)
    return module


def _expected(**over: int) -> dict[str, int]:
    base = {
        "tests": 100,
        "detectors": 66,
        "indicators": 60,
        "source_files": 298,
        "cli_commands": 57,
        "backends": 5,
    }
    base.update(over)
    return base


def _write(tmp_path: Path, body: str) -> Path:
    p = tmp_path / "doc.md"
    p.write_text(body, encoding="utf-8")
    return p


# --- CLI command count -----------------------------------------------------


def test_wrong_cli_command_count_emits_finding(cd, tmp_path: Path) -> None:
    doc = _write(tmp_path, "mypy strict clean; 46 CLI commands; E2E smoke runs.\n")
    findings = cd.check_doc(doc, _expected(cli_commands=57), set())
    assert len(findings) == 1
    assert "46 CLI commands" in findings[0]
    assert "57" in findings[0]


def test_correct_cli_command_count_emits_no_finding(cd, tmp_path: Path) -> None:
    doc = _write(tmp_path, "ruff clean; 57 CLI commands; full smoke.\n")
    assert cd.check_doc(doc, _expected(cli_commands=57), set()) == []


# --- LLM backend count (number word OR digit) ------------------------------


def test_wrong_backend_count_word_emits_finding(cd, tmp_path: Path) -> None:
    doc = _write(tmp_path, "- **Three LLM backends (maintainer-validated):** Anthropic ...\n")
    findings = cd.check_doc(doc, _expected(backends=5), set())
    assert len(findings) == 1
    assert "Three LLM backends" in findings[0]
    assert "admits 5" in findings[0]


def test_wrong_backend_count_digit_emits_finding(cd, tmp_path: Path) -> None:
    doc = _write(tmp_path, "We ship 4 LLM backends today.\n")
    findings = cd.check_doc(doc, _expected(backends=5), set())
    assert len(findings) == 1
    assert "4 LLM backends" in findings[0]


def test_correct_backend_count_emits_no_finding(cd, tmp_path: Path) -> None:
    doc = _write(tmp_path, "- **Five LLM backends** — Anthropic, Bedrock, ...\n")
    assert cd.check_doc(doc, _expected(backends=5), set()) == []


def test_runtime_backend_count_matches_llmconfig(cd) -> None:
    """The runtime source-of-truth helper reads the LLMConfig.backend
    Literal — 5 today (anthropic / bedrock / claude_code / openai /
    bedrock_openai). A floor guard so a gross config break is visible."""
    n = cd.runtime_backend_count()
    assert n >= 4
    import typing

    from efterlev.config import LLMConfig

    literals = typing.get_args(LLMConfig.model_fields["backend"].annotation)
    assert n == len([a for a in literals if isinstance(a, str)])
