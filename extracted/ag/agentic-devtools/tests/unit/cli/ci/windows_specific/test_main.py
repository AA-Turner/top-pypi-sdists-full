"""Tests for the trusted Windows CI dispatcher bridge and module entrypoint."""

import json
import runpy
import subprocess
import sys
from unittest.mock import Mock

import pytest

import agentic_devtools.cli.ci.windows_specific as windows_specific
from agentic_devtools.cli.ci import windows_specific_cli


def test_main_passes_named_api_dependencies(monkeypatch):
    dispatch = Mock(return_value=0)
    monkeypatch.setattr(windows_specific, "_run_cli", dispatch)

    result = windows_specific.main(["gate"])

    assert result == 0
    dispatch.assert_called_once_with(
        ["gate"],
        load_policy=windows_specific.load_policy,
        select_groups=windows_specific.select_groups,
        run_selected_tests=windows_specific.run_selected_tests,
        evaluate_gate=windows_specific.evaluate_gate,
    )


def test_main_is_publicly_exported():
    assert "main" in windows_specific.__all__
    assert windows_specific.main.__module__ == windows_specific.__name__


def test_run_module_passes_active_module_api_objects(monkeypatch):
    dispatch = Mock(return_value=0)
    monkeypatch.setattr(windows_specific_cli, "_run_cli", dispatch)
    monkeypatch.setattr(sys, "argv", ["windows_specific", "gate", "--selection-json", "{}"])

    with pytest.raises(SystemExit) as exc_info:
        runpy.run_path(windows_specific.__file__, run_name="__main__")

    assert exc_info.value.code == 0
    dependencies = dispatch.call_args.kwargs
    assert set(dependencies) == {"load_policy", "select_groups", "run_selected_tests", "evaluate_gate"}
    assert all(value.__module__ == "__main__" for value in dependencies.values())
    assert dependencies["load_policy"] is not windows_specific.load_policy


def test_python_module_entrypoint_runs_without_duplicate_module_warning():
    selection = json.dumps(
        {
            "ok": True,
            "product_groups": [],
            "contract_required": False,
            "windows_required": False,
            "bootstrap_allowed": False,
        }
    )
    result = subprocess.run(
        [sys.executable, "-m", "agentic_devtools.cli.ci.windows_specific", "gate", "--selection-json", selection],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == '{"ok":true,"classification":"not-applicable"}'
    assert "RuntimeWarning" not in result.stderr
