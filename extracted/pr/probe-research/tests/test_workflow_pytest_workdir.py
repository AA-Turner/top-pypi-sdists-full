"""Every `pytest` step in a workflow that tests agent/ must run IN agent/.

deploy-mcp.yml and release.yml drive the agent suite from the repo ROOT, so each
pytest step carries its own `working-directory: agent`; neither file has a
`defaults:` block to fall back on. Drop that key from one step and pytest
happily collects the BACKEND suite at the root instead -- `tests/unit`,
`app/...` -- and dies on `ModuleNotFoundError: No module named 'asyncpg'`,
because those dependencies were never installed in that job.

That is exactly what happened on 2026-09-09: splitting the single `pytest -q`
into two steps left the trailing `working-directory: agent` attached only to the
second, and main's MCP deploy broke. The PR could not have caught it --
deploy-mcp.yml runs on `push` to main and `workflow_dispatch`, never on a pull
request -- but agent-ci DOES run on any edit to that file (its path filter names
it, for test_deploy_scope.py's sake), so an assertion here catches it on the PR
where the edit is made.

agent-ci.yml itself is exempt: it declares `defaults.run.working-directory:
agent` once for the whole workflow, which is checked rather than assumed.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml  # via [dev] -> datamodel-code-generator; test_skills_sync.py imports it too.

# Deliberately NOT `pytest.importorskip`: a guard that disables itself when a
# dependency goes missing reports green for the thing it was written to catch.

_WORKFLOWS = Path(__file__).resolve().parents[2] / ".github" / "workflows"

# Workflows that run the agent suite from the repo root, so every pytest step
# there must name its own working directory.
_PER_STEP = ("deploy-mcp.yml", "release.yml")


def _pytest_steps(job: dict) -> list[dict]:
    return [s for s in job.get("steps", []) if "pytest" in str(s.get("run", ""))]


@pytest.mark.parametrize("workflow", _PER_STEP)
def test_every_pytest_step_names_its_working_directory(workflow: str):
    spec = yaml.safe_load((_WORKFLOWS / workflow).read_text())
    default = (spec.get("defaults") or {}).get("run", {}).get("working-directory")

    offenders = []
    for job_name, job in spec["jobs"].items():
        job_default = (job.get("defaults") or {}).get("run", {}).get("working-directory")
        for step in _pytest_steps(job):
            where = step.get("working-directory") or job_default or default
            if where != "agent":
                offenders.append(
                    f"{workflow}::{job_name} -> `{str(step.get('run', '')).strip()[:60]}` "
                    f"(working-directory={where!r})"
                )

    assert not offenders, (
        "these pytest steps would collect the repo-root backend suite instead of "
        "agent/, and fail on backend dependencies this job never installs:\n  "
        + "\n  ".join(offenders)
    )


def test_agent_ci_sets_the_working_directory_once_for_the_whole_workflow():
    """agent-ci is exempt from the rule above only because of this default."""
    spec = yaml.safe_load((_WORKFLOWS / "agent-ci.yml").read_text())
    assert (spec.get("defaults") or {}).get("run", {}).get("working-directory") == "agent", (
        "agent-ci.yml no longer defaults to agent/; either restore it or give "
        "every pytest step its own working-directory and add it to _PER_STEP here"
    )
