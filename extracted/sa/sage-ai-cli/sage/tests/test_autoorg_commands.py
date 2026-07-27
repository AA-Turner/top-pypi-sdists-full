"""Tests for autonomous command parsing and /autoorg role planning."""

from __future__ import annotations

import pytest

from sage.cli_core import (
    TaskType,
    _autoorg_response_requests_user_input,
    _build_autoorg_business_brief,
    _parse_autonomous_command_args,
    _plan_autoorg_roles,
)


class TestAutonomousCommandParsing:
    """Shared option parsing for /autopolit and /autoorg."""

    def test_parse_autopolit_focus_and_mode(self):
        options = _parse_autonomous_command_args(
            "5 --smart stabilize the auth runtime",
            default_use_intelligent=False,
        )

        assert options.max_cycles == 5
        assert options.use_intelligent is True
        assert options.focus == "stabilize the auth runtime"
        assert options.max_workers == 3

    def test_parse_autoorg_workers_and_model(self):
        options = _parse_autonomous_command_args(
            "--workers 4 --model llama_cpp:qwen2.5-coder-3b launch this product",
            default_use_intelligent=True,
        )

        assert options.use_intelligent is True
        assert options.max_workers == 4
        assert options.model == "llama_cpp:qwen2.5-coder-3b"
        assert options.focus == "launch this product"

    def test_parse_supports_keep_model_flag(self):
        options = _parse_autonomous_command_args(
            "--keep-model improve onboarding docs",
            default_use_intelligent=False,
        )

        assert options.keep_current_model is True
        assert options.focus == "improve onboarding docs"

    def test_parse_rejects_invalid_worker_count(self):
        with pytest.raises(ValueError):
            _parse_autonomous_command_args(
                "--workers 0 do the work",
                default_use_intelligent=True,
            )


class TestAutoOrgRolePlanning:
    """Dependency-aware role planning for /autoorg."""

    def test_business_brief_detects_integrations_and_browser_work(self):
        brief = _build_autoorg_business_brief(
            "Create a SaaS business, sign up for third-party services, retrieve API keys, "
            "launch the mobile app, and grow revenue with sales outreach"
        )

        assert brief.is_business_build is True
        assert brief.business_type in {"saas", "mobile", "business"}
        assert "developer_platforms" in brief.service_domains
        assert "crm" in brief.service_domains
        assert "mobile_release" in brief.service_domains
        assert "API key retrieval and integration setup" in brief.browser_workflows
        assert "mobile app submission workflows" in brief.browser_workflows
        assert "api keys" in brief.sensitive_operations

    def test_business_goal_includes_business_roles(self):
        roles = _plan_autoorg_roles(
            "Launch this SaaS product, grow adoption, and manage sales outreach"
        )
        by_id = {role.id: role for role in roles}

        assert "plan" in by_id
        assert "product" in by_id
        assert "engineering" in by_id
        assert "integrations" in by_id
        assert "marketing" in by_id
        assert "sales" in by_id
        assert "ops" in by_id
        assert "customer" in by_id
        assert "integrate" in by_id

        assert by_id["marketing"].dependencies == ["plan"]
        assert by_id["sales"].dependencies == ["marketing"]
        assert by_id["ops"].dependencies == ["plan", "integrations"]
        assert "marketing" in by_id["integrate"].dependencies
        assert "sales" in by_id["integrate"].dependencies
        assert "ops" in by_id["integrate"].dependencies

    def test_engineering_goal_stays_engineering_focused(self):
        roles = _plan_autoorg_roles("Fix the auth bug and improve runtime reliability")
        role_ids = {role.id for role in roles}

        assert {
            "plan",
            "engineering",
            "integrations",
            "quality",
            "security",
            "docs",
            "integrate",
        } <= role_ids
        assert "marketing" not in role_ids
        assert "sales" not in role_ids
        assert "ops" not in role_ids

    def test_browser_heavy_goal_adds_operator_and_launch_roles(self):
        roles = _plan_autoorg_roles(
            "Launch a mobile app business, sign up for providers, get API keys, and submit to the App Store"
        )
        by_id = {role.id: role for role in roles}

        assert "operator" in by_id
        assert "launch" in by_id
        assert "compliance" in by_id
        assert by_id["operator"].dependencies[0] == "integrations"
        assert "engineering" in by_id["launch"].dependencies

    def test_roles_map_to_existing_task_types(self):
        roles = _plan_autoorg_roles("Launch a new product and grow adoption")
        valid_types = {
            TaskType.ARCHITECTURE,
            TaskType.IMPLEMENTATION,
            TaskType.TESTING,
            TaskType.SECURITY,
            TaskType.DOCUMENTATION,
            TaskType.REVIEW,
        }

        assert all(role.task_type in valid_types for role in roles)


class TestAutoOrgAutonomyGuardrails:
    """AutoOrg should avoid prompting the user until truly blocked."""

    def test_detects_premature_request_for_user_input(self):
        assert _autoorg_response_requests_user_input(
            "Please provide more details about the business before I continue."
        )

    def test_allows_human_only_blocker_requests(self):
        assert not _autoorg_response_requests_user_input(
            "I need the App Store Connect verification code before I can finish submission."
        )
