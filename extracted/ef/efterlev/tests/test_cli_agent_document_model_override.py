"""Tests for `efterlev agent document --llm-model` (v0.1.227).

The 2026-06-11 onboarding run had a Haiku-cached gap report and needed
Sonnet for the narrative pass (Haiku deterministically fabricated on
KSI-IAM-ELP) — and had no way to express it. The flag overrides the
workspace model for ONE documentation run; config.toml is untouched.
"""

from __future__ import annotations

import re
from pathlib import Path

from efterlev.config import LLMConfig


def test_llm_config_model_copy_overrides_without_mutating_original() -> None:
    """The override mechanism: model_copy on the frozen LLMConfig swaps the
    model for this run; the original config object is untouched (so nothing
    downstream can accidentally persist the override)."""
    base = LLMConfig(backend="claude_code", model="claude-haiku-4-5")
    overridden = base.model_copy(update={"model": "claude-sonnet-4-6"})
    assert overridden.model == "claude-sonnet-4-6"
    assert overridden.backend == "claude_code"
    assert base.model == "claude-haiku-4-5"


def test_agent_document_cli_wires_llm_model_override() -> None:
    """Source-level pin (v0.1.23-27 pattern): agent_document must build
    `llm_config` from the --llm-model override and pass THAT (not the raw
    config.llm) to both the agent's model and the client factory. Without
    this pin a refactor could silently re-wire config.llm and turn the
    flag into a no-op."""
    src = Path("src/efterlev/cli/main.py").read_text(encoding="utf-8")
    m = re.search(r"\ndef agent_document\(.*?(?=\ndef [a-zA-Z_])", src, re.DOTALL)
    assert m is not None, "agent_document not found"
    body = m.group(0)
    assert '"--llm-model"' in body, "agent_document lost its --llm-model option"
    assert 'model_copy(update={"model": llm_model})' in body.replace("'", '"'), (
        "the override must model_copy the frozen LLMConfig"
    )
    assert "model=llm_config.model" in body, "DocumentationAgent must receive the overridden model"
    assert re.search(r"get_client_from_config\(\s*\n?\s*llm_config", body), (
        "the client factory must receive the overridden config"
    )
