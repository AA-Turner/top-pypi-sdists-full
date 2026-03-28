"""Test world that validates filesystem audit log collection on agent VMs.

Uses the SDK's AgentRunner and PlatoVMRuntime to spawn an agent VM exactly
as production worlds do, then performs file operations via SSH and verifies
that ausearch captures every operation with correct ACTION values.

Flow:
1. self.agent(config, workspaces=[code, reports, scratch]) → AgentRunner (SDK method)
2. runtime.prepare() → spawns agent VM, mounts NFS, installs auditctl rules
3. runner._configure_audit_scopes() → assigns unique per-workspace audit keys
4. runner._write_audit_context() → stamps trace/agent metadata
4. SSH file ops on agent VM (create, write, mkdir, delete, rename, chmod, symlink)
5. runner._collect_and_store_audit() → ausearch raw → parse → scoped JSONL
6. Verify scoped JSONL files and metadata
7. Commit tracked workspaces so upload/cleanup semantics run
8. runtime.cleanup() → tears down agent VM
"""

from __future__ import annotations

import secrets
from pathlib import Path
from typing import Annotated, ClassVar

from plato.agents.runtime.base import AgentContext
from plato.agents.runtime.vm import PlatoVMRuntime
from plato.chronos.models import Operation
from plato.markers import WorkspaceMarker
from plato.utils.audit import parse_audit_raw, read_audit_records
from plato.utils.subprocess import run_ssh
from plato.worlds import BaseWorld, Observation, StepResult
from plato.worlds.base import register_world
from plato.worlds.config import AgentConfig, RunConfig

# Use a real published agent image so PlatoVMRuntime._sync_code can resolve the
# package name and version.  We don't actually run the agent — we just need the
# VM to boot with auditd available.
_AGENT_IMAGE = "383806609161.dkr.ecr.us-west-1.amazonaws.com/vm/rootfs/plato-agents/claude-code:3.0.45"


class AuditTestWorldConfig(RunConfig):
    """Config for the audit test world."""

    code: Annotated[
        Path,
        WorkspaceMarker(
            description="Primary tracked audit test workspace",
            tracked=True,
            mount_path="/workspace/code",
        ),
    ] = Path("/workspace/code")
    reports: Annotated[
        Path,
        WorkspaceMarker(
            description="Secondary tracked audit test workspace",
            tracked=True,
            mount_path="/workspace/reports",
        ),
    ] = Path("/workspace/reports")
    scratch: Annotated[
        Path,
        WorkspaceMarker(
            description="Untracked audit test workspace",
            tracked=False,
            mount_path="/workspace/scratch",
        ),
    ] = Path("/workspace/scratch")


@register_world("plato-world-audit-test")
class AuditTestWorld(BaseWorld[AuditTestWorldConfig]):
    name: ClassVar[str] = "audit-test"
    description: ClassVar[str] = "Integration test for filesystem audit log collection"

    test_results: list[dict]
    all_passed: bool

    async def reset(self) -> Observation:
        self.test_results = []
        self.all_passed = True

        code_ws = self.workspace("code")
        reports_ws = self.workspace("reports")
        scratch_ws = self.workspace("scratch")
        tracked_workspaces = [code_ws, reports_ws]

        # --- Build AgentRunner via the SDK's self.agent() ---
        agent_config = AgentConfig(image=_AGENT_IMAGE)
        runner = self.agent(
            agent_config,
            display_name="audit-test-agent",
            workspaces=[code_ws, reports_ws, scratch_ws],
        )
        scopes = runner._configure_audit_scopes("audit-test-agent")

        runtime: PlatoVMRuntime = runner._runtime  # type: ignore[assignment]
        assert isinstance(runtime, PlatoVMRuntime), f"Expected PlatoVMRuntime, got {type(runtime).__name__}"

        # --- prepare(): spawn VM, mount NFS, install auditctl rules ---
        # Set workspace on runtime (normally done inside AgentRunner.run())
        runtime.workspace = runner._workspace
        runtime.workspaces = runner._default_workspaces or []

        self.logger.info("=== Preparing agent VM via PlatoVMRuntime.prepare() ===")
        runtime_dict = agent_config.runtime.model_dump()
        prep_ctx = AgentContext(
            image=agent_config.image,
            config=agent_config.config,
            instruction="",
            display_name="audit-test-agent",
            workspace=str(code_ws.path),
            runtime=runtime_dict,
        )
        prepared = await runtime.prepare(prep_ctx)
        self.logger.info(
            "Agent VM ready: agent_id=%s hostname=%s",
            prepared.agent_id,
            prepared.hostname,
        )

        try:
            # --- Write audit context (like the real AgentRunner.run() does) ---
            await runner._write_audit_context(
                prepared,
                scopes,
                display_name="audit-test-agent",
            )

            # --- Verify auditctl rule is installed ---
            await self._atest(
                "auditctl_rule_installed",
                lambda: self._check_audit_rule(runtime, prepared.hostname, scopes),
                "auditctl rule should be installed for tracked workspace paths with scoped keys",
            )

            # --- Perform file operations on agent VM ---
            tag = secrets.token_hex(4)
            await self._perform_agent_file_ops(
                runtime,
                prepared.hostname,
                code_ws.mount_path,
                tag,
            )
            await self._perform_agent_file_ops(
                runtime,
                prepared.hostname,
                reports_ws.mount_path,
                tag,
            )
            await self._perform_agent_file_ops(
                runtime,
                prepared.hostname,
                scratch_ws.mount_path,
                tag,
            )

            # --- Collect audit log via ausearch (the SDK method) ---
            await runner._collect_and_store_audit(
                prepared,
                scopes,
                display_name="audit-test-agent",
            )

            for scope in scopes:
                rows = self._read_scope_rows(scope.repo_root, scope.workspace_name)
                self._test(
                    f"jsonl_created_{scope.workspace_name}",
                    lambda rows=rows: len(rows) > 0,
                    f"should have created scoped JSONL rows for workspace {scope.workspace_name}",
                )
                if rows:
                    self._test(
                        f"context_stamped_agent_name_{scope.workspace_name}",
                        lambda rows=rows: all(getattr(row, "agent_name", None) for row in rows),
                        f"all stored events should have agent_name for workspace {scope.workspace_name}",
                    )
                    self._test(
                        f"metadata_contains_scope_{scope.workspace_name}",
                        lambda rows=rows, scope=scope: all(
                            self._metadata_field(row, "workspace_name") == scope.workspace_name
                            and self._metadata_field(row, "audit_run_id") == scope.audit_run_id
                            and self._metadata_field(row, "audit_key") == scope.audit_key
                            for row in rows
                        ),
                        f"all rows for {scope.workspace_name} should include scoped metadata",
                    )

            self._test(
                "untracked_workspace_not_spooled",
                lambda: not self._scope_dir_for_workspace(scratch_ws).exists(),
                "untracked workspace should not create audit spool files",
            )

            raw_events: list[object] = []
            for scope in scopes:
                raw_log = await scope.transport.collect_audit_log(
                    prepared.hostname,
                    audit_key=scope.audit_key,
                )
                self._test(
                    f"ausearch_raw_collected_{scope.workspace_name}",
                    lambda raw_log=raw_log: raw_log is not None and len(raw_log) > 0,
                    f"ausearch --format raw should return data for workspace {scope.workspace_name}",
                )
                if raw_log:
                    raw_events.extend(list(parse_audit_raw(raw_log)))

            self._verify_operations(raw_events, tag)

            for workspace in tracked_workspaces:
                await workspace.commit(f"audit-test-{workspace.name}")

            for workspace in tracked_workspaces:
                self._test(
                    f"spool_cleaned_after_commit_{workspace.name}",
                    lambda workspace=workspace: not self._scope_dir_for_workspace(workspace).exists()
                    or not any(self._scope_dir_for_workspace(workspace).glob("*.jsonl")),
                    f"tracked workspace {workspace.name} should clean scoped JSONL files after commit/upload",
                )

        finally:
            # --- cleanup(): tear down agent VM ---
            self.logger.info("Cleaning up agent VM %s", prepared.agent_id)
            await runtime.cleanup(prepared.agent_id)

        return self._finish()

    async def step(self) -> StepResult:
        return StepResult(
            observation=Observation(data={"test_results": self.test_results, "all_passed": self.all_passed}),
            done=True,
        )

    # ---------------------------------------------------------------
    # Helpers
    # ---------------------------------------------------------------

    def _finish(self) -> Observation:
        passed = sum(1 for t in self.test_results if t["passed"])
        failed = sum(1 for t in self.test_results if not t["passed"])
        self.logger.info("=== Audit Tests: %d passed, %d failed ===", passed, failed)
        for t in self.test_results:
            status = "PASS" if t["passed"] else "FAIL"
            self.logger.info("  [%s] %s: %s", status, t["name"], t.get("error", "ok"))

        if not self.all_passed:
            failures = [t for t in self.test_results if not t["passed"]]
            raise RuntimeError(f"Audit tests failed: {failures}")

        return Observation(data={"test_results": self.test_results, "passed": passed, "failed": failed})

    def _test(self, name: str, check: object, error_msg: str) -> None:
        try:
            result = check()  # type: ignore[operator]
            if result:
                self.test_results.append({"name": name, "passed": True})
                self.logger.info("  [PASS] %s", name)
            else:
                self.test_results.append({"name": name, "passed": False, "error": error_msg})
                self.logger.error("  [FAIL] %s: %s", name, error_msg)
                self.all_passed = False
        except Exception as e:
            self.test_results.append({"name": name, "passed": False, "error": str(e)})
            self.logger.error("  [FAIL] %s: %s", name, e)
            self.all_passed = False

    async def _atest(self, name: str, check: object, error_msg: str) -> None:
        try:
            result = await check()  # type: ignore[operator]
            if result:
                self.test_results.append({"name": name, "passed": True})
                self.logger.info("  [PASS] %s", name)
            else:
                self.test_results.append({"name": name, "passed": False, "error": error_msg})
                self.logger.error("  [FAIL] %s: %s", name, error_msg)
                self.all_passed = False
        except Exception as e:
            self.test_results.append({"name": name, "passed": False, "error": str(e)})
            self.logger.error("  [FAIL] %s: %s", name, e)
            self.all_passed = False

    def _scope_dir_for_workspace(self, workspace) -> Path:
        return workspace._repo_root / ".plato" / "audit" / workspace.name

    def _read_scope_rows(self, repo_root: Path, workspace_name: str) -> list[object]:
        rows: list[object] = []
        scope_dir = repo_root / ".plato" / "audit" / workspace_name
        if not scope_dir.exists():
            return rows
        for path in sorted(scope_dir.glob("*.jsonl")):
            rows.extend(read_audit_records(path))
        return rows

    def _metadata_field(self, row: object, key: str) -> object | None:
        metadata = getattr(row, "metadata", None)
        if not isinstance(metadata, dict):
            return None
        return metadata.get(key)

    def _verify_operations(self, events: list[object], tag: str) -> None:
        if not events:
            return

        ops = {ev.operation.value if isinstance(ev.operation, Operation) else ev.operation for ev in events}
        self.logger.info("Operations seen: %s", ops)

        expected_file = f"test_{tag}.txt"
        file_events = [ev for ev in events if expected_file in ev.path]
        self._test(
            "opened_file_for_create",
            lambda: any(
                (ev.operation.value if isinstance(ev.operation, Operation) else ev.operation) == "opened-file"
                for ev in file_events
            ),
            f"creating/writing {expected_file} should produce opened-file, "
            f"got: {[(ev.operation, ev.path) for ev in file_events]}",
        )

        expected_dir = f"subdir_{tag}"
        dir_events = [ev for ev in events if expected_dir in ev.path]
        self._test(
            "created_directory_for_mkdir",
            lambda: any(
                (ev.operation.value if isinstance(ev.operation, Operation) else ev.operation) == "created-directory"
                for ev in dir_events
            ),
            f"mkdir should produce created-directory for {expected_dir}, "
            f"got: {[(ev.operation, ev.path) for ev in dir_events]}",
        )

        self._test(
            "deleted_for_rm",
            lambda: "deleted" in ops,
            f"rm should produce deleted, got: {ops}",
        )
        self._test(
            "renamed_for_mv",
            lambda: "renamed" in ops,
            f"mv should produce renamed, got: {ops}",
        )
        self._test(
            "changed_permissions_for_chmod",
            lambda: "changed-file-permissions-of" in ops,
            f"chmod should produce changed-file-permissions-of, got: {ops}",
        )
        self._test(
            "symlinked_for_ln",
            lambda: "symlinked" in ops,
            f"ln -s should produce symlinked, got: {ops}",
        )

        valid_ops = {op.value for op in Operation}
        self._test(
            "all_operations_valid",
            lambda: ops.issubset(valid_ops),
            f"all operations should be valid ausearch types, unexpected: {ops - valid_ops}",
        )
        self._test(
            "events_have_timestamps",
            lambda: all(ev.timestamp is not None for ev in events),
            "all events should have timestamps",
        )
        self._test(
            "events_have_paths",
            lambda: all(ev.path for ev in events),
            "all events should have non-empty paths",
        )

    async def _check_audit_rule(
        self,
        runtime: PlatoVMRuntime,
        hostname: str,
        scopes: list[object],
    ) -> bool:
        """Check that auditctl rule exists on agent VM."""
        assert runtime.ssh_key_path is not None
        exit_code, stdout, _ = await run_ssh(
            runtime.ssh_key_path,
            hostname,
            "auditctl -l 2>/dev/null || true",
            timeout=10,
        )
        if exit_code != 0:
            return False
        for scope in scopes:
            if scope.audit_key not in stdout or scope.mount_path not in stdout:
                return False
        return "scratch" not in stdout

    async def _perform_agent_file_ops(self, runtime: PlatoVMRuntime, hostname: str, mount_path: str, tag: str) -> None:
        """Perform file operations that exercise all major ausearch ACTION types."""
        self.logger.info("Performing file operations on agent VM at %s", mount_path)

        ops_script = f"""
set -e
# opened-file: create a file
echo -n 'hello-{tag}' > {mount_path}/test_{tag}.txt

# opened-file: append to existing file
echo -n 'updated-{tag}' >> {mount_path}/test_{tag}.txt

# created-directory: mkdir
mkdir -p {mount_path}/subdir_{tag}

# opened-file: create file in subdirectory
echo -n 'nested-{tag}' > {mount_path}/subdir_{tag}/nested.txt

# deleted: create then remove a file
echo -n 'delete-me' > {mount_path}/to_delete_{tag}.txt
rm {mount_path}/to_delete_{tag}.txt

# renamed: create then rename a file
echo -n 'rename-me' > {mount_path}/before_{tag}.txt
mv {mount_path}/before_{tag}.txt {mount_path}/after_{tag}.txt

# changed-file-permissions-of: chmod
chmod 755 {mount_path}/test_{tag}.txt

# symlinked: create a symlink
ln -s {mount_path}/test_{tag}.txt {mount_path}/link_{tag}.txt

# Allow audit log to flush
sleep 1

echo 'File operations complete'
"""
        assert runtime.ssh_key_path is not None
        exit_code, stdout, stderr = await run_ssh(
            runtime.ssh_key_path,
            hostname,
            ops_script,
            timeout=30,
        )
        if exit_code != 0:
            self.logger.error("File ops failed: exit=%d, stderr=%s", exit_code, stderr)
        else:
            self.logger.info("File ops completed: %s", stdout.strip())
