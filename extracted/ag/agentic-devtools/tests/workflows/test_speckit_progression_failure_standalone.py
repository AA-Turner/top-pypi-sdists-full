"""Workflow integration test for the dependency-free SpecKit failure entrypoint."""

import ast
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.parametrize(
    "python_command",
    [[sys.executable], ["py", "-3.13"] if os.name == "nt" else ["/usr/bin/python3"]],
    ids=["configured-python", "pre-setup-python"],
)
def test_standalone_entrypoint_posts_without_installed_package(tmp_path: Path, python_command: list[str]) -> None:
    args_file = tmp_path / "gh-args.txt"
    body_file = tmp_path / "posted-body.txt"
    env = os.environ.copy()
    env.update(
        {
            "FAKE_GH_ARGS": str(args_file),
            "FAKE_GH_BODY": str(body_file),
            "ISSUE_NUMBER": "42",
            "NEXT_PHASE": "2",
            "NEXT_PHASE_NAME": "clarify",
            "GITHUB_REPOSITORY": "owner/repo",
            "GITHUB_RUN_ID": "123",
            "COMMENT_ON_ISSUE": "true",
            "GATE_RESULT": "fail",
            "CRITICAL_FINDINGS": "not-json",
        }
    )
    script = Path(__file__).resolve().parents[2] / "agentic_devtools" / "cli" / "speckit" / "progression_failure.py"
    ast.parse(script.read_text(encoding="utf-8"), feature_version=(3, 10))
    bootstrap = """
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
from unittest.mock import patch

assert sys.flags.no_site
assert "agentic_devtools" not in sys.modules

def fake_run(args, **kwargs):
    Path(os.environ["FAKE_GH_ARGS"]).write_text(json.dumps(args), encoding="utf-8")
    Path(os.environ["FAKE_GH_BODY"]).write_text(Path(args[-1]).read_text(encoding="utf-8"), encoding="utf-8")
    return subprocess.CompletedProcess(args, 0)

with patch("subprocess.run", side_effect=fake_run):
    runpy.run_path(sys.argv[1], run_name="__main__")
"""

    result = subprocess.run(
        [*python_command, "-S", "-c", bootstrap, str(script)],
        capture_output=True,
        check=False,
        env=env,
        shell=False,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert json.loads(args_file.read_text(encoding="utf-8"))[:7] == [
        "gh",
        "issue",
        "comment",
        "42",
        "--repo",
        "owner/repo",
        "--body-file",
    ]
    assert "_Could not parse findings: not-json_" in body_file.read_text(encoding="utf-8")
