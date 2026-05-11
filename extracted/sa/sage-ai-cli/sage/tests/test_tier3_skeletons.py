"""TDD tests for Tier 3 features: T7, T9, T11, T13.

T7: Project-skeleton bootstrapper — match task → seed real boilerplate
T9: Shipped templates per task type
T11: Two-model pipeline as default for `sage run`
T13: Sage run readiness check — quick "can this model handle a hello-world?"
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest


# ════════════════════════════════════════════════════════════════════════
# T7 + T9: Skeletons + templates
# ════════════════════════════════════════════════════════════════════════

def test_skeleton_registry_has_basic_templates():
    from sage.core.skeletons import SKELETONS
    names = {s.name for s in SKELETONS}
    # Core templates we ship
    assert "react-vite" in names
    assert "node-express" in names
    assert "fastapi" in names
    assert "fullstack-react-node" in names


def test_skeleton_match_recognizes_react_node_task():
    from sage.core.skeletons import match_skeleton
    s = match_skeleton(
        "Build an app where a user can manage pets and medical records "
        "in React and Node.js"
    )
    assert s is not None
    # Should pick fullstack since both React + Node mentioned
    assert "react" in s.name.lower() or "fullstack" in s.name.lower()


def test_skeleton_match_recognizes_fastapi_task():
    from sage.core.skeletons import match_skeleton
    s = match_skeleton("Create a Python FastAPI service for user management")
    assert s is not None
    assert "fastapi" in s.name.lower()


def test_skeleton_match_returns_none_for_irrelevant_prompts():
    from sage.core.skeletons import match_skeleton
    assert match_skeleton("explain how OAuth works") is None
    assert match_skeleton("what is the difference between TCP and UDP") is None


def test_skeleton_files_have_real_content():
    """Templates must contain actual boilerplate, not placeholders."""
    from sage.core.skeletons import SKELETONS
    for s in SKELETONS:
        for path, content in s.files.items():
            # __init__.py is intentionally empty in some packages
            if path.endswith("__init__.py"):
                continue
            assert content.strip(), f"{s.name}:{path} is empty"
            # Must not contain SAGE protocol leak markers
            assert "## TASK:" not in content
            assert "Plan ID:" not in content


def test_skeleton_apply_writes_all_files(tmp_path):
    from sage.core.skeletons import apply_skeleton, SKELETONS
    s = next(s for s in SKELETONS if s.name == "node-express")
    written = apply_skeleton(s, target=tmp_path, overwrite=False)
    assert len(written) == len(s.files)
    for path in s.files:
        assert (tmp_path / path).exists()


def test_skeleton_apply_skips_existing_files_unless_overwrite(tmp_path):
    from sage.core.skeletons import apply_skeleton, SKELETONS
    s = next(s for s in SKELETONS if s.name == "node-express")
    # Pre-create one file
    first_file = next(iter(s.files))
    (tmp_path / first_file).parent.mkdir(parents=True, exist_ok=True)
    (tmp_path / first_file).write_text("user content")
    written = apply_skeleton(s, target=tmp_path, overwrite=False)
    assert first_file not in written
    # Existing content preserved
    assert (tmp_path / first_file).read_text() == "user content"


def test_skeleton_apply_overwrites_when_flag_set(tmp_path):
    from sage.core.skeletons import apply_skeleton, SKELETONS
    s = next(s for s in SKELETONS if s.name == "node-express")
    first_file = next(iter(s.files))
    (tmp_path / first_file).parent.mkdir(parents=True, exist_ok=True)
    (tmp_path / first_file).write_text("user content")
    written = apply_skeleton(s, target=tmp_path, overwrite=True)
    assert first_file in written
    # Skeleton content now in place
    assert (tmp_path / first_file).read_text() != "user content"


def test_react_vite_skeleton_has_valid_package_json():
    """The package.json we ship must NOT be poison (regression: Novellia)."""
    from sage.core.content_validator import validate_content
    from sage.core.skeletons import SKELETONS
    s = next(s for s in SKELETONS if s.name == "react-vite")
    pkg = s.files.get("package.json", "")
    assert pkg.strip()
    result = validate_content("package.json", pkg)
    assert result.ok, result.reason


# ════════════════════════════════════════════════════════════════════════
# T11: Two-model pipeline as default
# ════════════════════════════════════════════════════════════════════════

def test_dual_pipeline_picks_default_planner_and_coder():
    """The two-model pipeline must have sensible defaults from a model list."""
    from sage.core.dual_pipeline import resolve_planner_coder
    available = [
        "ollama:llama3.2:latest",          # 3B
        "ollama:qwen3-coder-next:latest",  # 30B+
        "ollama:llama3.3:latest",          # 70B
    ]
    planner, coder = resolve_planner_coder(available)
    # Planner should be smaller/faster than coder
    assert planner != coder
    # Coder should be a coding-specialist
    assert "coder" in coder.lower() or "code" in coder.lower()


def test_dual_pipeline_returns_same_model_when_only_one_available():
    from sage.core.dual_pipeline import resolve_planner_coder
    planner, coder = resolve_planner_coder(["ollama:qwen3-coder-next:latest"])
    assert planner == coder


def test_dual_pipeline_returns_empty_when_no_models():
    from sage.core.dual_pipeline import resolve_planner_coder
    planner, coder = resolve_planner_coder([])
    assert planner == ""
    assert coder == ""


# ════════════════════════════════════════════════════════════════════════
# T13: Readiness check
# ════════════════════════════════════════════════════════════════════════

def test_readiness_check_passes_for_capable_response():
    from sage.core.readiness import check_readiness, ReadinessResult
    def good_send(prompt: str, *, model: str, system: str) -> str:
        return "FILE: hello.js\n```javascript\nconsole.log('hi');\n```"
    result = check_readiness(model="ollama:qwen3-coder-next", send_fn=good_send)
    assert result.ok is True
    assert result.model_responded is True


def test_readiness_check_fails_when_no_file_block():
    from sage.core.readiness import check_readiness
    def chatty(prompt: str, *, model: str, system: str) -> str:
        return "I would write a hello world. Let me think about it..."
    result = check_readiness(model="ollama:tiny", send_fn=chatty)
    assert result.ok is False
    assert "FILE:" in result.detail or "protocol" in result.detail.lower()


def test_readiness_check_fails_on_send_exception():
    from sage.core.readiness import check_readiness
    def boom(prompt: str, *, model: str, system: str) -> str:
        raise RuntimeError("model offline")
    result = check_readiness(model="ollama:dead", send_fn=boom)
    assert result.ok is False
    assert "offline" in result.detail


def test_readiness_check_rejects_protocol_leaked_response():
    from sage.core.readiness import check_readiness
    def leaky(prompt: str, *, model: str, system: str) -> str:
        return ("FILE: hello.js\n```javascript\n## TASK: write hello\n"
                "Plan ID: plan_x\nconsole.log('hi');\n```")
    result = check_readiness(model="ollama:weak", send_fn=leaky)
    assert result.ok is False
