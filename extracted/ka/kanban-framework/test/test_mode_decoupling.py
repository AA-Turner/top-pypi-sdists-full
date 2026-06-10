"""Regression tests for mode decoupling — verify built-in and custom modes use the same loading path."""
import json
import pytest
from pathlib import Path


class TestDefaultMode:
    def test_default_mode_is_lightweight(self):
        from kanban_framework.infra.consts import Consts
        assert Consts.DEFAULT_MODE == "lightweight"


class TestTemplateLoading:
    def test_load_lightweight_template(self):
        from kanban_framework.domain.steps_loader import _load_template_steps
        result = _load_template_steps("lightweight")
        assert result is not None
        assert "plan" in result
        assert "execute" in result
        assert any(s.id == "plan.plan_A" for s in result["plan"])

    def test_load_quick_template(self):
        from kanban_framework.domain.steps_loader import _load_template_steps
        result = _load_template_steps("quick")
        assert result is not None
        assert "execute" in result
        assert "plan" in result  # quick now has plan (knowledge_search + user_confirm)

    def test_load_nonexistent_template_returns_none(self):
        from kanban_framework.domain.steps_loader import _load_template_steps
        result = _load_template_steps("nonexistent_mode")
        assert result is None


class TestStepsLoaderUniformity:
    def test_builtin_and_custom_same_loading_function(self, tmp_path):
        """Built-in and custom modes load through the same load_steps_for_mode function."""
        from kanban_framework.domain.steps_loader import load_steps_for_mode

        # Create a custom mode in tmp workflows dir
        wf_dir = tmp_path / "workflows"
        wf_dir.mkdir()
        custom_wf = {
            "phase_order": ["plan", "archive"],
            "phases": [
                {"id": "plan", "steps": [
                    {"id": "plan.custom_step", "description": "custom step"}
                ]},
                {"id": "archive", "steps": [
                    {"id": "archive.cleanup", "description": "cleanup"}
                ]},
            ],
        }
        (wf_dir / "my_custom.json").write_text(json.dumps(custom_wf), encoding="utf-8")

        # Load custom mode
        custom_result = load_steps_for_mode({}, "my_custom", kanban_dir=tmp_path)
        assert "plan" in custom_result
        assert any(s.id == "plan.custom_step" for s in custom_result["plan"])

        # Load built-in mode through same function — should also work
        builtin_result = load_steps_for_mode({}, "lightweight", kanban_dir=tmp_path)
        assert "plan" in builtin_result


class TestGetModesDiscovery:
    def test_discovers_package_workflows(self):
        from kanban_framework.infra.scheduler import Scheduler
        modes = Scheduler.get_modes()
        assert "lightweight" in modes
        assert "quick" in modes

    def test_discovers_user_workflows(self, tmp_path):
        from kanban_framework.infra.scheduler import Scheduler
        wf_dir = tmp_path / "workflows"
        wf_dir.mkdir()
        custom_wf = {"phase_order": ["execute", "archive"]}
        (wf_dir / "my_mode.json").write_text(json.dumps(custom_wf), encoding="utf-8")

        modes = Scheduler.get_modes(kanban_dir=tmp_path)
        assert "my_mode" in modes

    def test_workflow_json_modes_override(self):
        from kanban_framework.infra.scheduler import Scheduler
        from kanban_framework.types import Phase
        workflow = {
            "modes": {
                "lightweight": {
                    "phase_order": ["execute", "archive"]
                }
            }
        }
        modes = Scheduler.get_modes(workflow=workflow)
        assert "lightweight" in modes
        phase_values = [p.value if hasattr(p, "value") else str(p) for p in modes["lightweight"]]
        assert phase_values == ["execute", "archive"]


class TestNoBuiltinModeNamesReferences:
    def test_no_builtin_mode_names_in_source(self):
        """Verify BUILTIN_MODE_NAMES has been fully removed."""
        import subprocess
        result = subprocess.run(
            ["grep", "-rn", "BUILTIN_MODE_NAMES", "kanban_framework/"],
            capture_output=True, text=True,
        )
        assert result.returncode != 0, f"Found BUILTIN_MODE_NAMES references:\n{result.stdout}"

    def test_no_full_fallback_in_source(self):
        """Verify getattr(task, 'mode', 'full') has been fully removed."""
        import subprocess
        result = subprocess.run(
            ["grep", "-rn", "getattr.*mode.*'full'", "kanban_framework/"],
            capture_output=True, text=True,
        )
        assert result.returncode != 0, f"Found 'full' fallback references:\n{result.stdout}"


class TestEvalRolesConfigDriven:
    def test_quick_mode_no_eval_falls_back_to_default(self):
        """Quick mode has no evaluate phase, so _derive_eval_roles falls back to EVAL_ROLES."""
        from kanban_framework.infra.scheduler import Scheduler
        roles = Scheduler.eval_roles(mode="quick")
        # Quick has no evaluate phase in its steps, so falls back to default 3-role EVAL_ROLES
        assert len(roles) == 3
        role_names = [r["name"] for r in roles]
        assert "code_reviewer" in role_names
        assert "qa" in role_names
        assert "product_reviewer" in role_names

    def test_lightweight_mode_has_reviewer(self):
        from kanban_framework.infra.scheduler import Scheduler
        roles = Scheduler.eval_roles(mode="lightweight")
        assert len(roles) >= 1
        assert any("review" in r["name"] for r in roles)
