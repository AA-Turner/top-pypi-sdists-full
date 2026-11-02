"""Run the selected PR smart-module test suites with combined coverage."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from agentic_devtools.cli.checks.xdist_policy import get_xdist_args
from agentic_devtools.git_env import sanitize_git_environment

_MODULE_FLAGS_ENV = "AGDT_SMART_MODULE_FLAGS"


@dataclass(frozen=True)
class _ModuleTestSpec:
    """Test paths and coverage packages for one smart-module filter."""

    paths: tuple[str, ...]
    globs: tuple[str, ...]
    coverage: tuple[str, ...]


_MODULE_SPECS = {
    "git": _ModuleTestSpec(("tests/unit/cli/git",), ("tests/test_git_*.py",), ("agentic_devtools/cli/git",)),
    "azure_devops": _ModuleTestSpec(
        ("tests/unit/cli/azure_devops", "tests/azure_devops"),
        (),
        ("agentic_devtools/cli/azure_devops",),
    ),
    "azure_context": _ModuleTestSpec(
        ("tests/unit/cli/azure_context", "tests/azure_context"),
        (),
        ("agentic_devtools/cli/azure_context",),
    ),
    "jira": _ModuleTestSpec(("tests/unit/cli/jira",), (), ("agentic_devtools/cli/jira",)),
    "vpn": _ModuleTestSpec(("tests/unit/cli/vpn", "tests/vpn"), (), ("agentic_devtools/cli/vpn",)),
    "network": _ModuleTestSpec(("tests/unit/cli/network", "tests/network"), (), ("agentic_devtools/cli/network",)),
    "release": _ModuleTestSpec(
        ("tests/unit/cli/release",), ("tests/test_release_*.py",), ("agentic_devtools/cli/release",)
    ),
    "tasks": _ModuleTestSpec(("tests/unit/cli/tasks",), (), ("agentic_devtools/cli/tasks",)),
    "github_module": _ModuleTestSpec(("tests/unit/cli/github",), (), ("agentic_devtools/cli/github",)),
    "copilot": _ModuleTestSpec(("tests/unit/cli/copilot",), (), ("agentic_devtools/cli/copilot",)),
    "ci": _ModuleTestSpec(
        (
            "tests/unit/cli/ci/critique_adjudicator/test_critique_adjudicator.py",
            "tests/unit/cli/ci/pipeline/critique_gate/test_critique_gate_exception_passed.py",
        ),
        (),
        (
            "agentic_devtools.cli.ci.critique_adjudicator",
            "agentic_devtools.cli.ci.pipeline.critique_gate",
        ),
    ),
    "speckit": _ModuleTestSpec(("tests/unit/cli/speckit",), (), ("agentic_devtools/cli/speckit",)),
    "azure": _ModuleTestSpec(("tests/unit/cli/azure",), (), ("agentic_devtools/cli/azure",)),
    "issue_template": _ModuleTestSpec(("tests/unit/cli/issue_template",), (), ("agentic_devtools/cli/issue_template",)),
    "hierarchy": _ModuleTestSpec(
        ("tests/unit/hierarchy", "tests/unit/cli/hierarchy"),
        (),
        ("agentic_devtools/hierarchy", "agentic_devtools/cli/hierarchy"),
    ),
    "workflows": _ModuleTestSpec(("tests/unit/cli/workflows",), (), ("agentic_devtools/cli/workflows",)),
    "core": _ModuleTestSpec(
        (
            "tests/unit/state",
            "tests/unit/background_tasks",
            "tests/unit/config",
            "tests/unit/file_locking",
            "tests/unit/task_state",
            "tests/unit/cli/runner",
            "tests/unit/cli/state",
            "tests/unit/cli/subprocess_utils",
            "tests/unit/cli/testing",
            "tests/test_validate_test_structure.py",
            "tests/test_scaffold_tests.py",
            "tests/test_version.py",
        ),
        (),
        (
            "agentic_devtools.state",
            "agentic_devtools.background_tasks",
            "agentic_devtools.config",
            "agentic_devtools.file_locking",
            "agentic_devtools.task_state",
            "agentic_devtools.cli.runner",
            "agentic_devtools.cli.state",
            "agentic_devtools.cli.subprocess_utils",
            "agentic_devtools.cli.testing",
        ),
    ),
    "orchestration": _ModuleTestSpec(("tests/unit/orchestration",), (), ("agentic_devtools.orchestration",)),
    "tools": _ModuleTestSpec(("tests/unit/tools",), (), ("agentic_devtools.tools",)),
}


class SmartModuleTestRunner:
    """Select and run module-scoped tests using xdist and combined coverage."""

    def __init__(self, selected_modules: list[str], workspace: Path) -> None:
        unknown = sorted(set(selected_modules) - _MODULE_SPECS.keys())
        if unknown:
            raise ValueError(f"Unknown smart module(s): {', '.join(unknown)}")
        self.selected_modules = list(dict.fromkeys(selected_modules))
        self.workspace = workspace

    @classmethod
    def from_environment(cls, *, workspace: Path) -> SmartModuleTestRunner:
        """Build a runner from the JSON flags exported by the PR workflow."""
        raw_flags = os.environ.get(_MODULE_FLAGS_ENV, "{}")
        try:
            flags = json.loads(raw_flags)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{_MODULE_FLAGS_ENV} must be a JSON object of string flags") from exc
        if not isinstance(flags, dict):
            raise ValueError(f"{_MODULE_FLAGS_ENV} must be a JSON object of string flags")
        unknown = sorted(set(flags) - _MODULE_SPECS.keys())
        if unknown:
            raise ValueError(f"{_MODULE_FLAGS_ENV} contains unknown module(s): {', '.join(unknown)}")
        if any(not isinstance(value, str) or value not in {"true", "false"} for value in flags.values()):
            raise ValueError(f"{_MODULE_FLAGS_ENV} values must be 'true' or 'false'")
        return cls([name for name, enabled in flags.items() if enabled == "true"], workspace)

    def pytest_args(self) -> list[str]:
        """Return the selected test paths followed by the original coverage scope."""
        directories: list[str] = []
        files: list[str] = []
        coverage: list[str] = []
        for name in self.selected_modules:
            spec = _MODULE_SPECS[name]
            for relative_path in spec.paths:
                path = self.workspace / relative_path
                if path.is_dir():
                    directories.append(str(path))
                elif path.is_file():
                    files.append(str(path))
            for pattern in spec.globs:
                files.extend(str(path) for path in sorted(self.workspace.glob(pattern)) if path.is_file())
            coverage.extend(f"--cov={package}" for package in spec.coverage)

        # Directories must precede standalone files to avoid pytest package-node caching (#1073).
        test_paths = list(dict.fromkeys([*directories, *files]))
        if not test_paths:
            return []
        xdist_args: list[str] = []
        for directory in directories:
            xdist_args = get_xdist_args(
                Path(directory),
                coverage_workers=1,
                distribution="worksteal",
            )
            if xdist_args:
                break
        return [
            *test_paths,
            *xdist_args,
            *coverage,
            "--cov-report=term-missing",
            "--cov-report=xml",
            "--cov-fail-under=100",
            "--override-ini=addopts=",
        ]

    def run(self) -> int:
        """Run pytest, preserving the workflow's no-tests skip and exit status."""
        args = self.pytest_args()
        if not args:
            print("WARNING: No test paths found for the detected changes — nothing to run.")
            return 0
        path_end = next((index for index, arg in enumerate(args) if arg.startswith("-")), len(args))
        test_paths = args[:path_end]
        coverage_flags = [arg for arg in args if arg.startswith("--cov=")]
        print("Test paths:", *test_paths, sep="\n  ")
        print("Coverage flags:", *coverage_flags, sep="\n  ")
        environment = sanitize_git_environment(os.environ)
        if not environment.get("COVERAGE_CORE"):
            environment["COVERAGE_CORE"] = "sysmon"
        result = subprocess.run(
            [sys.executable, "-m", "pytest", *args],
            cwd=str(self.workspace),
            env=environment,
            shell=False,
        )
        return result.returncode


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(SmartModuleTestRunner.from_environment(workspace=Path.cwd()).run())
