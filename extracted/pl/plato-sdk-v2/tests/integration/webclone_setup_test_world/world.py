"""Test world that validates webclone workspace setup on FUSE.

Runs on a real VM via BaseWorld, exercising the production code path:
FUSE mount → prepare_template_workspace (template copy + bun install) → verify.

Results are written to /tmp/webclone-setup-test-results.json.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Annotated, ClassVar

from plato.markers import WorkspaceMarker
from plato.worlds import BaseWorld, Observation, StepResult
from plato.worlds.base import register_world
from plato.worlds.config import RunConfig

RESULTS_PATH = Path("/tmp/webclone-setup-test-results.json")


class WebcloneSetupTestConfig(RunConfig):
    code_ws: Annotated[
        Path,
        WorkspaceMarker(
            description="Code workspace for template setup",
            tracked=True,
            mount_path="/workspace/code",
        ),
    ] = Path("/workspace/code")


@register_world("plato-world-webclone-setup-test")
class WebcloneSetupTestWorld(BaseWorld[WebcloneSetupTestConfig]):
    name: ClassVar[str] = "webclone-setup-test"
    description: ClassVar[str] = "Test webclone workspace setup on FUSE"

    async def reset(self) -> Observation:
        return {"status": "ready"}

    async def step(self) -> StepResult:
        results: dict[str, dict] = {}
        code_ws = self.workspace("code_ws")
        workspace_path = code_ws.path / "data"
        workspace_path.mkdir(parents=True, exist_ok=True)

        # Test 1: prepare_template_workspace (copies template + bun install)
        try:
            from webclone.stages.template_workspace import prepare_template_workspace

            outputs = await prepare_template_workspace(
                workspace_path=workspace_path,
                template_name="sohan",
            )
            results["prepare_template"] = {
                "pass": True,
                "summary": outputs.summary,
            }
        except Exception as e:
            results["prepare_template"] = {"pass": False, "error": str(e)}
            self._write_results(results)
            return StepResult(observation={"results": results}, done=True)

        # Test 2: Verify workspace structure
        checks = {
            "package_json": (workspace_path / "web" / "package.json").exists(),
            "node_modules": (workspace_path / "web" / "node_modules").is_dir(),
            "next_bin": (workspace_path / "web" / "node_modules" / ".bin" / "next").exists(),
            "start_sh": (workspace_path / "start.sh").exists(),
            "validate_sh": (workspace_path / "validate.sh").exists(),
            "schema_ts": (workspace_path / "web" / "db" / "schema.ts").exists(),
            "git_dir": (workspace_path / ".git").is_dir(),
        }
        missing = [k for k, v in checks.items() if not v]
        results["workspace_structure"] = {
            "pass": len(missing) == 0,
            "checks": checks,
            "errors": missing if missing else None,
        }

        # Test 3: Verify next.js is runnable
        try:
            proc = subprocess.run(
                ["bun", "run", "next", "--help"],
                cwd=str(workspace_path / "web"),
                capture_output=True,
                timeout=30,
            )
            results["bun_next"] = {
                "pass": proc.returncode == 0,
                "error": proc.stderr.decode()[:500] if proc.returncode != 0 else None,
            }
        except Exception as e:
            results["bun_next"] = {"pass": False, "error": str(e)}

        # Test 4: Smart commit the workspace with node_modules present
        try:
            ref = await code_ws.commit("post_setup")
            results["smart_commit"] = {"pass": True, "ref": ref}
        except Exception as e:
            results["smart_commit"] = {"pass": False, "error": str(e)}

        self._write_results(results)

        all_passed = all(r.get("pass") for r in results.values())
        if not all_passed:
            failed = [k for k, v in results.items() if not v.get("pass")]
            raise RuntimeError(f"Tests failed: {failed}")

        return StepResult(observation={"results": results}, done=True)

    def _write_results(self, results: dict) -> None:
        RESULTS_PATH.write_text(json.dumps(results, indent=2, default=str))
        self.logger.info("Test results written to %s", RESULTS_PATH)
