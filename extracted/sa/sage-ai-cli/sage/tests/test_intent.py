"""Tests for read-only vs implementation vs multi-task prompt routing."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from sage.cli_core import (
    _build_cloud_deployment_context,
    _clear_classification,
    _expand_prompt,
    _is_readonly_analysis_request,
    _resolve_cloud_provider_preference,
    _wants_code_changes,
)


@pytest.fixture(autouse=True)
def _reset_request_classification():
    """Avoid cross-test pollution of global classification used by _expand_prompt."""
    _clear_classification()
    yield
    _clear_classification()


# ── Read-only analysis detection ──────────────────────────────────────


def test_readonly_analysis_user_request():
    q = (
        "Analyze this codebase and tell me what needs to be fixed and improved, "
        "list the items by priority"
    )
    assert _is_readonly_analysis_request(q)
    assert not _wants_code_changes(q.lower())
    out = _expand_prompt(q)
    assert "read-only analysis mode" in out.lower()
    assert "NEVER create tests" in out or "Do NOT create tests" in out


def test_review_code_is_readonly():
    q = "Review the code and tell me what's wrong"
    assert _is_readonly_analysis_request(q)


def test_audit_is_readonly():
    q = "Audit this project for security gaps"
    assert _is_readonly_analysis_request(q)


def test_implementation_and_analyze_is_not_readonly():
    q = "Analyze the bug and fix the Dockerfile"
    assert not _is_readonly_analysis_request(q)
    assert _wants_code_changes(q.lower())


def test_explicit_no_code_overrides():
    q = "Analyze this but don't write code, analysis only"
    assert _is_readonly_analysis_request(q)


def test_fix_this_is_implementation():
    q = "fix this regression in auth"
    assert not _is_readonly_analysis_request(q)


# ── Multi-task / "fix all" detection ──────────────────────────────────


def test_fix_all_triggers_task_list_workflow():
    q = "Fix all of these points"
    out = _expand_prompt(q)
    assert "TASK-LIST WORKFLOW" in out
    assert "Task K/N" in out
    assert "READ:" in out


def test_fix_these_triggers_task_list():
    q = "fix these issues that were identified"
    out = _expand_prompt(q)
    assert "TASK-LIST WORKFLOW" in out


def test_address_all_triggers_task_list():
    q = "address all items in the list above"
    out = _expand_prompt(q)
    assert "TASK-LIST WORKFLOW" in out


def test_implement_all_triggers_task_list():
    q = "implement all the recommendations"
    out = _expand_prompt(q)
    assert "TASK-LIST WORKFLOW" in out


def test_every_point_triggers_task_list():
    q = "go through every point and fix them"
    out = _expand_prompt(q)
    assert "TASK-LIST WORKFLOW" in out


def test_single_fix_does_not_trigger_task_list():
    q = "fix the broken import in utils.py"
    out = _expand_prompt(q)
    assert "TASK-LIST WORKFLOW" not in out


# ── Vague implementation triggers ─────────────────────────────────────


def test_improve_this_triggers_implementation():
    q = "improve this codebase"
    out = _expand_prompt(q)
    assert "READ: every file you plan to modify" in out
    assert "TASK-LIST WORKFLOW" not in out


def test_refactor_this_triggers_implementation():
    q = "refactor this module"
    out = _expand_prompt(q)
    assert "READ: every file you plan to modify" in out


def test_secret_prompt_requires_real_env_bootstrap_not_placeholders():
    q = "Set up API keys and the database url in a .env file"
    out = _expand_prompt(q)
    assert "placeholder values only" not in out
    assert "Reuse the real `.env`" in out
    assert "NEVER fabricate third-party API keys" in out


def test_deploy_prompt_requires_cloud_choice_and_provider_native_guidance():
    q = "Deploy this service to the cloud"
    out = _expand_prompt(q)
    assert "ask them to choose one" in out
    assert "Stay provider-native" in out


def test_cloud_deployment_context_requires_user_choice_when_missing():
    out = _build_cloud_deployment_context("Deploy this service")
    assert "ask the user which cloud they want" in out
    assert "Do NOT guess a cloud vendor" in out


def test_resolve_cloud_provider_preference_prompts_and_persists(monkeypatch):
    import sage.main as main
    from sage.config import SageConfig

    saved_preferences: list[str] = []
    monkeypatch.setattr(main, "save_config", lambda cfg: saved_preferences.append(cfg.preferred_cloud))

    cfg = SageConfig()
    provider = _resolve_cloud_provider_preference(
        "Deploy this service",
        cfg,
        prompt_user=lambda _: "gcloud",
    )

    assert provider == "gcp"
    assert cfg.preferred_cloud == "gcp"
    assert saved_preferences == ["gcp"]
