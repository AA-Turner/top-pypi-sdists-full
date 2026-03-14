"""Test world that validates workspace functionality end-to-end on a real VM.

This world runs ON the world VM via BaseWorld, exercising the full production
code path: workspace init → ensure_fuse_mount → NFS export → agent mount.

Tests:
1. Workspace declaration, init, tracked/untracked semantics
2. FUSE mount on overlayfs (ensure_fuse_mount) — production path
3. NFS export of FUSE mounts — production path
4. Cross-VM reads/writes through NFS → FUSE
5. Lazy DVC: commit, restore, smart commit, file sizes
6. Agent writes to FUSE mount over NFS (webclone pattern)
7. Multiple workspace NFS exports
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import secrets
import shutil
import sys
from pathlib import Path
from typing import Annotated, ClassVar

from plato.agents.runtime.transport import NFSTransport
from plato.markers import WorkspaceMarker
from plato.utils.subprocess import run_local, run_ssh
from plato.worlds import BaseWorld, Observation, StepResult
from plato.worlds.base import register_world
from plato.worlds.config import RunConfig
from plato.worlds.workspace import Workspace


class WorkspaceTestWorldConfig(RunConfig):
    """Config for the workspace test world.

    Paths are on overlayfs (VM root). BaseWorld._start_transport() will call
    ensure_fuse_mount() to put FUSE on them, then NFS exports the FUSE mounts.
    This is the exact production code path.
    """

    ws: Annotated[
        Path,
        WorkspaceMarker(description="Test workspace", tracked=False, mount_path="/workspace"),
    ] = Path("/workspace/ws")

    tracked_ws: Annotated[
        Path,
        WorkspaceMarker(
            description="Tracked workspace for DVC tests",
            tracked=True,
            mount_path="/tracked",
            dvcignore=["*.tmp", "dist"],
        ),
    ] = Path("/workspace/tracked_ws")


@register_world("plato-world-structured-execution")
class WorkspaceTestWorld(BaseWorld[WorkspaceTestWorldConfig]):
    name: ClassVar[str] = "workspace-test"
    description: ClassVar[str] = "Integration test world for workspace e2e validation"

    test_results: list[dict]
    all_passed: bool

    async def reset(self) -> Observation:
        self.test_results = []
        self.all_passed = True
        self._agent_env = None
        self._agent_hostname = None

        try:
            # These workspaces went through the full production path:
            # _init_declared_workspaces → ensure_fuse_mount → _start_transport
            self._ws = self.workspace("ws")
            self._tracked = self.workspace("tracked_ws")

            # --- Verify production setup worked ---
            await self._run_setup_verification_tests()

            # --- Basic workspace attribute tests ---
            self._run_basic_tests()

            # --- Tracked workspace tests ---
            self._run_tracked_ws_tests()

            # --- Local file I/O through FUSE ---
            await self._run_fuse_io_tests()

            # --- Cross-VM tests (spawn agent, verify NFS) ---
            await self._run_cross_vm_tests()

            # --- Lazy DVC cycle: commit → restore → smart commit ---
            await self._run_lazy_dvc_tests()

            passed = sum(1 for t in self.test_results if t["passed"])
            failed = sum(1 for t in self.test_results if not t["passed"])
            self.logger.info(f"=== Workspace Tests: {passed} passed, {failed} failed ===")
            for t in self.test_results:
                status = "PASS" if t["passed"] else "FAIL"
                self.logger.info(f"  [{status}] {t['name']}: {t.get('error', 'ok')}")

            if not self.all_passed:
                failures = [t for t in self.test_results if not t["passed"]]
                raise RuntimeError(f"Workspace tests failed: {failures}")

            return Observation(data={"test_results": self.test_results, "passed": passed, "failed": failed})
        finally:
            await self._cleanup_agent_env()

    async def step(self) -> StepResult:
        return StepResult(
            observation=Observation(data={"test_results": self.test_results, "all_passed": self.all_passed}),
            done=True,
        )

    # ---------------------------------------------------------------
    # Test helpers
    # ---------------------------------------------------------------

    def _test(self, name: str, check, error_msg: str) -> None:
        try:
            result = check()
            if result:
                self.test_results.append({"name": name, "passed": True})
                self.logger.info(f"  [PASS] {name}")
            else:
                self.test_results.append({"name": name, "passed": False, "error": error_msg})
                self.logger.error(f"  [FAIL] {name}: {error_msg}")
                self.all_passed = False
        except Exception as e:
            self.test_results.append({"name": name, "passed": False, "error": str(e)})
            self.logger.error(f"  [FAIL] {name}: {e}")
            self.all_passed = False

    async def _atest(self, name: str, check, error_msg: str) -> None:
        try:
            result = await check()
            if result:
                self.test_results.append({"name": name, "passed": True})
                self.logger.info(f"  [PASS] {name}")
            else:
                self.test_results.append({"name": name, "passed": False, "error": error_msg})
                self.logger.error(f"  [FAIL] {name}: {error_msg}")
                self.all_passed = False
        except Exception as e:
            self.test_results.append({"name": name, "passed": False, "error": str(e)})
            self.logger.error(f"  [FAIL] {name}: {e}")
            self.all_passed = False

    # ---------------------------------------------------------------
    # Setup verification — did production code do its job?
    # ---------------------------------------------------------------

    async def _run_setup_verification_tests(self) -> None:
        self.logger.info("=== Verifying production setup ===")
        ws = self._ws
        tracked = self._tracked

        # Workspaces exist and have transports (assigned by _start_transport)
        self._test("ws_exists", lambda: ws is not None, "ws should exist")
        self._test(
            "ws_has_transport", lambda: ws.transport is not None, "ws should have transport from _start_transport"
        )
        self._test(
            "ws_transport_is_nfs",
            lambda: isinstance(ws.transport, NFSTransport),
            f"ws transport should be NFS, got {type(ws.transport)}",
        )
        self._test("tracked_exists", lambda: tracked is not None, "tracked_ws should exist")
        self._test("tracked_has_transport", lambda: tracked.transport is not None, "tracked_ws should have transport")
        self._test(
            "tracked_transport_is_nfs",
            lambda: isinstance(tracked.transport, NFSTransport),
            f"tracked transport should be NFS, got {type(tracked.transport)}",
        )

        # Content paths should be FUSE mounts (ensure_fuse_mount on overlayfs)
        await self._atest(
            "ws_is_fuse_mount",
            lambda: self._is_mountpoint(ws.path),
            f"ws.path ({ws.path}) should be a FUSE mount (ensure_fuse_mount)",
        )
        await self._atest(
            "tracked_is_fuse_mount",
            lambda: self._is_mountpoint(tracked.path),
            f"tracked.path ({tracked.path}) should be a FUSE mount",
        )

        # Verify FUSE filesystem type
        await self._atest(
            "ws_fuse_fstype",
            lambda: self._check_fstype(ws.path, "fuse"),
            "ws.path should be on fuse filesystem",
        )

        # NFS exports should exist
        await self._atest(
            "nfs_exports_exist",
            lambda: self._check_exports_contain(str(ws.path)),
            f"NFS exports should contain {ws.path}",
        )
        await self._atest(
            "nfs_exports_tracked",
            lambda: self._check_exports_contain(str(tracked.path)),
            f"NFS exports should contain {tracked.path}",
        )

    async def _is_mountpoint(self, path: Path) -> bool:
        ec, _, _ = await run_local(f"mountpoint -q {path}", timeout=5)
        return ec == 0

    async def _check_fstype(self, path: Path, expected_prefix: str) -> bool:
        ec, stdout, _ = await run_local(f"findmnt -n -o FSTYPE --target {path}", timeout=5)
        return ec == 0 and stdout.strip().lower().startswith(expected_prefix)

    async def _check_exports_contain(self, path: str) -> bool:
        ec, stdout, _ = await run_local("exportfs -s", timeout=5)
        return ec == 0 and path in stdout

    # ---------------------------------------------------------------
    # Basic attribute tests
    # ---------------------------------------------------------------

    def _run_basic_tests(self) -> None:
        self.logger.info("=== Basic workspace attribute tests ===")
        ws = self._ws

        self._test("ws_is_workspace", lambda: isinstance(ws, Workspace), f"Expected Workspace, got {type(ws)}")
        self._test("ws_path_exists", lambda: ws.path.exists(), f"ws.path ({ws.path}) should exist")
        self._test("ws_not_tracked", lambda: not ws.tracked, "ws should not be tracked")
        self._test(
            "ws_mount_path",
            lambda: ws.mount_path == "/workspace",
            f"ws.mount_path should be /workspace, got {ws.mount_path}",
        )

    # ---------------------------------------------------------------
    # Tracked workspace tests
    # ---------------------------------------------------------------

    def _run_tracked_ws_tests(self) -> None:
        self.logger.info("=== Tracked workspace tests ===")
        tracked = self._tracked

        self._test("tracked_is_tracked", lambda: tracked.tracked, "tracked_ws should be tracked")
        self._test("tracked_has_s3_bucket", lambda: bool(tracked.s3_bucket), "tracked should have s3_bucket")
        self._test("tracked_has_s3_prefix", lambda: bool(tracked.s3_prefix), "tracked should have s3_prefix")
        self._test(
            "tracked_mount_path",
            lambda: tracked.mount_path == "/tracked",
            f"mount_path should be /tracked, got {tracked.mount_path}",
        )
        self._test(
            "tracked_path_is_data_subdir",
            lambda: tracked.path.name == "data",
            f"tracked.path should end in /data, got {tracked.path}",
        )
        self._test(
            "tracked_repo_root", lambda: tracked._repo_root == tracked.path.parent, "repo_root should be parent of path"
        )
        self._test(
            "tracked_repo_root_exists",
            lambda: tracked._repo_root.is_dir(),
            "tracked repo root should exist after init",
        )

        dvcignore = tracked._repo_root / ".dvcignore"
        if dvcignore.exists():
            content = dvcignore.read_text()
            self._test(
                "tracked_dvcignore_defaults", lambda: "node_modules" in content, "Default dvcignore should be present"
            )
            self._test(
                "tracked_dvcignore_custom",
                lambda: "*.tmp" in content and "dist" in content,
                "Custom dvcignore should be present",
            )

    # ---------------------------------------------------------------
    # Local file I/O through FUSE
    # ---------------------------------------------------------------

    async def _run_fuse_io_tests(self) -> None:
        self.logger.info("=== FUSE I/O tests ===")
        ws_path = self._ws.path
        tag = secrets.token_hex(4)

        # Write and read
        test_file = ws_path / f"test_{tag}.txt"
        test_file.write_text(f"hello-{tag}")
        self._test("fuse_write_read", lambda: test_file.read_text() == f"hello-{tag}", "Write/read through FUSE")

        # Large file
        large_data = os.urandom(2 * 1024 * 1024)
        large_file = ws_path / f"large_{tag}.bin"
        large_file.write_bytes(large_data)
        self._test(
            "fuse_large_file", lambda: large_file.read_bytes() == large_data, "Large file write/read through FUSE"
        )

        # Mkdir + nested write
        nested = ws_path / f"nested_{tag}" / "a" / "b"
        nested.mkdir(parents=True, exist_ok=True)
        (nested / "deep.txt").write_text("deep")
        self._test(
            "fuse_nested_write", lambda: (nested / "deep.txt").read_text() == "deep", "Nested dir write through FUSE"
        )

        # Cleanup
        test_file.unlink(missing_ok=True)
        large_file.unlink(missing_ok=True)
        shutil.rmtree(ws_path / f"nested_{tag}", ignore_errors=True)

    # ---------------------------------------------------------------
    # Cross-VM tests — use production transport.setup_agent
    # ---------------------------------------------------------------

    async def _run_cross_vm_tests(self) -> None:
        self.logger.info("=== Cross-VM tests ===")

        if not self.plato_session:
            self.logger.warning("No plato_session, skipping cross-VM tests")
            return

        ssh_key_path = self._ssh_key_path
        try:
            agent_env, agent_hostname = await self._spawn_agent_env()

            # Mount workspace on agent using production transport.setup_agent
            ws_transport = self._ws.transport
            tracked_transport = self._tracked.transport

            await self._atest(
                "nfs_setup_agent_ws",
                lambda: self._do_setup_agent(ws_transport, agent_env, agent_hostname),
                "transport.setup_agent() for ws should succeed",
            )
            await self._atest(
                "nfs_setup_agent_tracked",
                lambda: self._do_setup_agent(tracked_transport, agent_env, agent_hostname),
                "transport.setup_agent() for tracked_ws should succeed",
            )

            # --- World write → agent read ---
            await self._test_world_write_agent_read(ssh_key_path, agent_hostname)

            # --- Agent write → world read ---
            await self._test_agent_write_world_read(ssh_key_path, agent_hostname)

            # --- Agent writes to FUSE mount (webclone pattern) ---
            await self._test_agent_fuse_writes(ssh_key_path, agent_hostname)

            # --- Multiple workspace isolation ---
            await self._test_multi_workspace(ssh_key_path, agent_hostname)

            # --- Concurrent writes ---
            await self._test_concurrent_writes(ssh_key_path, agent_hostname)

            # --- NFS write under backpressure (reproduce EIO) ---
            await self._test_nfs_write_under_backpressure(ssh_key_path, agent_hostname)

        except Exception as e:
            self.test_results.append({"name": "cross_vm_setup", "passed": False, "error": f"Failed: {e}"})
            self.all_passed = False
            self.logger.error(f"Cross-VM test setup failed: {e}", exc_info=True)

    async def _spawn_agent_env(self):
        from plato.v2 import Env
        from plato.v2.types import SimConfigCompute

        ssh_key_path = self._ssh_key_path
        self.logger.info("Spawning agent VM...")
        agent_env = await self.plato_session.add_env(
            Env.resource(
                simulator="workspace-test-agent",
                sim_config=SimConfigCompute(cpus=1, memory=2048, disk=10240),
                alias=f"test-agent-{secrets.token_hex(4)}",
            ),
            timeout=300,
        )
        self.logger.info(f"Agent VM spawned: job_id={agent_env.job_id}")

        pub_key = Path(str(ssh_key_path) + ".pub").read_text().strip()
        await self.plato_session.add_ssh_key(pub_key)

        agent_hostname = await agent_env.get_mesh_ip()
        if not agent_hostname:
            raise RuntimeError("Agent VM has no mesh IP")
        self.logger.info(f"Agent mesh IP: {agent_hostname}")

        await run_ssh(
            ssh_key_path,
            agent_hostname,
            "which mount.nfs > /dev/null 2>&1 || (apt-get update -qq && apt-get install -y -qq nfs-common)",
            timeout=60,
        )

        self._agent_env = agent_env
        self._agent_hostname = agent_hostname
        return agent_env, agent_hostname

    async def _cleanup_agent_env(self) -> None:
        if self._agent_env:
            try:
                await self.plato_session.remove_env(self._agent_env)
            except Exception:
                pass
            finally:
                self._agent_env = None
                self._agent_hostname = None

    async def _recreate_tracked_agent(self) -> None:
        """Tear down the old agent, re-export all workspaces via NFS, spawn a new agent."""
        await self._cleanup_agent_env()

        # After FUSE unmount/remount the NFS exports become stale because the
        # underlying filesystem changed.  exportfs -ra alone won't recover them.
        # Re-write /etc/exports with fresh lines for every workspace, then re-export.
        ws_paths = [self._ws.path, self._tracked.path]
        export_lines = []
        for i, p in enumerate(ws_paths):
            export_lines.append(
                f"{p} *(rw,sync,fsid={i},crossmnt,no_subtree_check,all_squash,anonuid=1000,anongid=1000)"
            )
        exports_content = "\n".join(export_lines)
        await run_local(f"printf '%s\\n' '{exports_content}' > /etc/exports", timeout=10)
        await run_local("exportfs -ra", timeout=10)

        _, exports_after, _ = await run_local("exportfs -s", timeout=5)
        self.logger.info(f"NFS exports after re-add:\n{exports_after.strip()}")

        agent_env, agent_hostname = await self._spawn_agent_env()
        await self._tracked.transport.setup_agent(agent_env, agent_hostname)

    async def _do_setup_agent(self, transport, agent_env, hostname) -> bool:
        await transport.setup_agent(agent_env, hostname)
        return True

    def _ws_agent_path(self, filename: str) -> str:
        return f"{self._ws.transport.agent_mount_path}/{filename}"

    def _tracked_agent_path(self, filename: str) -> str:
        return f"{self._tracked.transport.agent_mount_path}/{filename}"

    async def _test_world_write_agent_read(self, ssh_key_path, hostname) -> None:
        self.logger.info("--- World write → agent read ---")
        tag = secrets.token_hex(4)
        ws_path = self._ws.path

        # Write file on world
        (ws_path / f"world_{tag}.txt").write_text(f"from-world-{tag}")

        await self._atest(
            "world_write_agent_read",
            lambda: self._ssh_cat(ssh_key_path, hostname, self._ws_agent_path(f"world_{tag}.txt"), f"from-world-{tag}"),
            "File written on world should be readable from agent via NFS",
        )

        # Large file
        large_data = os.urandom(5 * 1024 * 1024)
        (ws_path / f"large_{tag}.bin").write_bytes(large_data)

        await self._atest(
            "world_write_large_agent_read",
            lambda: self._ssh_file_size(
                ssh_key_path, hostname, self._ws_agent_path(f"large_{tag}.bin"), len(large_data)
            ),
            "5MB file should be correct size on agent",
        )

        # Nested dirs
        nested = ws_path / f"tree_{tag}" / "a" / "b"
        nested.mkdir(parents=True, exist_ok=True)
        (nested / "deep.txt").write_text("deep")

        await self._atest(
            "world_write_nested_agent_read",
            lambda: self._ssh_cat(ssh_key_path, hostname, self._ws_agent_path(f"tree_{tag}/a/b/deep.txt"), "deep"),
            "Nested directory tree should be visible on agent",
        )

        # Cleanup
        (ws_path / f"world_{tag}.txt").unlink(missing_ok=True)
        (ws_path / f"large_{tag}.bin").unlink(missing_ok=True)
        shutil.rmtree(ws_path / f"tree_{tag}", ignore_errors=True)

    async def _test_agent_write_world_read(self, ssh_key_path, hostname) -> None:
        self.logger.info("--- Agent write → world read ---")
        tag = secrets.token_hex(4)
        ws_path = self._ws.path

        # Agent writes a file
        await run_ssh(
            ssh_key_path,
            hostname,
            f"echo -n 'from-agent-{tag}' > {self._ws_agent_path(f'agent_{tag}.txt')}",
            timeout=10,
        )
        self._test(
            "agent_write_world_read",
            lambda: (ws_path / f"agent_{tag}.txt").read_text() == f"from-agent-{tag}",
            "File written by agent should be visible on world via NFS",
        )

        # Agent writes JSON
        json_content = json.dumps({"key": f"value-{tag}"})
        await run_ssh(
            ssh_key_path,
            hostname,
            f"echo -n '{json_content}' > {self._ws_agent_path(f'output_{tag}.json')}",
            timeout=10,
        )
        self._test(
            "agent_write_json",
            lambda: json.loads((ws_path / f"output_{tag}.json").read_text()) == {"key": f"value-{tag}"},
            "Agent-written JSON should be valid and readable on world",
        )

        # Agent writes large file
        await run_ssh(
            ssh_key_path,
            hostname,
            f"dd if=/dev/urandom of={self._ws_agent_path(f'agent_large_{tag}.bin')} bs=1M count=2 2>/dev/null",
            timeout=30,
        )
        self._test(
            "agent_write_large",
            lambda: (ws_path / f"agent_large_{tag}.bin").stat().st_size == 2 * 1024 * 1024,
            "Agent-written 2MB file should be correct size on world",
        )

        # Cleanup
        for f in [f"agent_{tag}.txt", f"output_{tag}.json", f"agent_large_{tag}.bin"]:
            (ws_path / f).unlink(missing_ok=True)

    async def _test_agent_fuse_writes(self, ssh_key_path, hostname) -> None:
        """Test agent writes to FUSE mount over NFS (replicates webclone pattern)."""
        self.logger.info("--- Agent FUSE writes (webclone pattern) ---")
        tag = secrets.token_hex(4)
        ws_path = self._ws.path

        # Agent creates nested dirs and writes (like inferred_model/merged.json)
        nested_agent = f"{self._ws_agent_path(f'backend_{tag}')}/inferred_model"
        ec, _, stderr = await run_ssh(
            ssh_key_path,
            hostname,
            f"mkdir -p {nested_agent}",
            timeout=10,
        )
        self._test(
            "agent_fuse_mkdir_nested",
            lambda: self._ok(ec),
            f"Agent mkdir -p nested dirs over NFS→FUSE should work: {stderr}",
        )

        ec, _, stderr = await run_ssh(
            ssh_key_path,
            hostname,
            f"""echo -n '{{"model": "test-{tag}"}}' > {nested_agent}/merged.json""",
            timeout=10,
        )
        self._test(
            "agent_fuse_write_nested",
            lambda: self._ok(ec),
            f"Agent write to nested dir over NFS→FUSE should work: {stderr}",
        )

        # Verify on world
        merged = ws_path / f"backend_{tag}" / "inferred_model" / "merged.json"
        self._test(
            "agent_fuse_nested_visible",
            lambda: merged.exists() and json.loads(merged.read_text())["model"] == f"test-{tag}",
            "Agent-created nested file should be visible on world through FUSE",
        )

        # Agent touches a file (exact webclone failure pattern)
        ec, _, stderr = await run_ssh(
            ssh_key_path,
            hostname,
            f"touch {nested_agent}/touched.json",
            timeout=10,
        )
        self._test(
            "agent_fuse_touch",
            lambda: self._ok(ec),
            f"Agent touch over NFS→FUSE should work: {stderr}",
        )

        # Agent writes into world-created subdir
        world_subdir = ws_path / f"world_created_{tag}"
        world_subdir.mkdir(parents=True, exist_ok=True)
        ec, _, _ = await run_ssh(
            ssh_key_path,
            hostname,
            f"echo -n 'in-world-dir' > {self._ws_agent_path(f'world_created_{tag}/agent_file.txt')}",
            timeout=10,
        )
        self._test(
            "agent_write_world_subdir",
            lambda: (world_subdir / "agent_file.txt").read_text() == "in-world-dir",
            "Agent should write into world-created subdir via NFS",
        )

        # Cleanup
        shutil.rmtree(ws_path / f"backend_{tag}", ignore_errors=True)
        shutil.rmtree(world_subdir, ignore_errors=True)

    async def _test_multi_workspace(self, ssh_key_path, hostname) -> None:
        """Test both workspaces are independently NFS-mounted."""
        self.logger.info("--- Multi-workspace isolation ---")
        tag = secrets.token_hex(4)
        ws_path = self._ws.path
        tracked_path = self._tracked.path

        # Write to ws
        (ws_path / f"ws_{tag}.txt").write_text(f"ws-{tag}")
        # Write to tracked
        (tracked_path / f"tracked_{tag}.txt").write_text(f"tracked-{tag}")

        # Agent reads from ws
        await self._atest(
            "multi_ws_agent_read_ws",
            lambda: self._ssh_cat(ssh_key_path, hostname, self._ws_agent_path(f"ws_{tag}.txt"), f"ws-{tag}"),
            "Agent should read ws file",
        )

        # Agent reads from tracked
        await self._atest(
            "multi_ws_agent_read_tracked",
            lambda: self._ssh_cat(
                ssh_key_path, hostname, self._tracked_agent_path(f"tracked_{tag}.txt"), f"tracked-{tag}"
            ),
            "Agent should read tracked file",
        )

        # Isolation: ws file not in tracked
        await self._atest(
            "multi_ws_isolation",
            lambda: self._ssh_file_absent(ssh_key_path, hostname, self._tracked_agent_path(f"ws_{tag}.txt")),
            "ws file should NOT appear in tracked mount",
        )

        # Agent writes to tracked
        await run_ssh(
            ssh_key_path,
            hostname,
            f"echo -n 'agent-tracked-{tag}' > {self._tracked_agent_path(f'agent_{tag}.txt')}",
            timeout=10,
        )
        self._test(
            "multi_ws_agent_write_tracked",
            lambda: (tracked_path / f"agent_{tag}.txt").read_text() == f"agent-tracked-{tag}",
            "Agent write to tracked_ws should be visible on world",
        )

        # Cleanup
        (ws_path / f"ws_{tag}.txt").unlink(missing_ok=True)
        (tracked_path / f"tracked_{tag}.txt").unlink(missing_ok=True)
        (tracked_path / f"agent_{tag}.txt").unlink(missing_ok=True)

    async def _test_concurrent_writes(self, ssh_key_path, hostname) -> None:
        self.logger.info("--- Concurrent writes ---")
        tag = secrets.token_hex(4)
        ws_path = self._ws.path

        async def write_world():
            (ws_path / f"conc_world_{tag}.txt").write_text(f"world-{tag}")

        async def write_agent():
            await run_ssh(
                ssh_key_path,
                hostname,
                f"echo -n 'agent-{tag}' > {self._ws_agent_path(f'conc_agent_{tag}.txt')}",
                timeout=10,
            )

        await asyncio.gather(write_world(), write_agent())
        await asyncio.sleep(0.5)

        world_ok = (ws_path / f"conc_world_{tag}.txt").read_text() == f"world-{tag}"
        agent_ok = (ws_path / f"conc_agent_{tag}.txt").read_text() == f"agent-{tag}"

        self._test("concurrent_writes", lambda: world_ok and agent_ok, "Concurrent writes should not corrupt data")

        (ws_path / f"conc_world_{tag}.txt").unlink(missing_ok=True)
        (ws_path / f"conc_agent_{tag}.txt").unlink(missing_ok=True)

    # ---------------------------------------------------------------
    # NFS backpressure tests — reproduce Input/Output error (EIO)
    # ---------------------------------------------------------------

    async def _test_nfs_write_under_backpressure(self, ssh_key_path, hostname) -> None:
        """Verify NFS mount options are resilient to transient server stalls.

        The agent VM mounts NFS with soft,timeo=150,retrans=5 (15s timeout,
        5 retries = ~75s total). We block NFS traffic on the agent for 10s
        then unblock — the write should survive because the NFS client retries
        within the timeout window. This validates that transient FUSE stalls
        or load spikes on the world VM don't cause EIO on the agent.
        """
        import base64

        self.logger.info("--- NFS write under backpressure ---")
        tag = secrets.token_hex(4)

        # Baseline: agent can write normally
        await run_ssh(
            ssh_key_path,
            hostname,
            f"echo -n 'baseline-{tag}' > {self._ws_agent_path(f'bp_baseline_{tag}.txt')}",
            timeout=10,
        )
        baseline_ok = (self._ws.path / f"bp_baseline_{tag}.txt").read_text() == f"baseline-{tag}"
        self._test(
            "nfs_backpressure_baseline",
            lambda: baseline_ok,
            "Agent write should succeed without NFS disruption",
        )

        # Helper: run a python write script on the agent via SSH
        async def agent_write(filename: str, content: str, timeout_s: int = 30) -> tuple[int, str, str]:
            script = (
                f"import sys, os\n"
                f"try:\n"
                f"    with open('{self._ws_agent_path(filename)}', 'w') as f:\n"
                f"        f.write('{content}')\n"
                f"        f.flush()\n"
                f"        os.fsync(f.fileno())\n"
                f"    print('OK')\n"
                f"except OSError as e:\n"
                f"    print(f'ERROR:{{e}}', file=sys.stderr)\n"
                f"    sys.exit(1)\n"
            )
            b64 = base64.b64encode(script.encode()).decode()
            return await run_ssh(ssh_key_path, hostname, f"echo {b64} | base64 -d | python3", timeout=timeout_s)

        # Helper: block/unblock NFS on agent VM
        world_ip = self._ws.transport.world_vm_ip
        self.logger.info(f"World VM NFS IP: {world_ip}, Agent: {hostname}")

        async def block_nfs():
            await run_ssh(
                ssh_key_path,
                hostname,
                f"iptables -I OUTPUT -d {world_ip} -p tcp --dport 2049 -j DROP && "
                f"iptables -I OUTPUT -d {world_ip} -p udp --dport 2049 -j DROP && "
                f"iptables -I INPUT -s {world_ip} -p tcp --sport 2049 -j DROP && "
                f"iptables -I INPUT -s {world_ip} -p udp --sport 2049 -j DROP",
                timeout=10,
            )

        async def unblock_nfs():
            await run_ssh(
                ssh_key_path,
                hostname,
                f"iptables -D OUTPUT -d {world_ip} -p tcp --dport 2049 -j DROP 2>/dev/null || true && "
                f"iptables -D OUTPUT -d {world_ip} -p udp --dport 2049 -j DROP 2>/dev/null || true && "
                f"iptables -D INPUT -s {world_ip} -p tcp --sport 2049 -j DROP 2>/dev/null || true && "
                f"iptables -D INPUT -s {world_ip} -p udp --sport 2049 -j DROP 2>/dev/null || true",
                timeout=10,
            )

        # Log mount options for diagnostics
        ec, mount_info, _ = await run_ssh(
            ssh_key_path,
            hostname,
            "mount | grep nfs || true",
            timeout=10,
        )
        self.logger.info(f"Agent NFS mounts:\n{mount_info.strip()}")

        # Test 1: Transient 10s block — write should SURVIVE.
        # With timeo=150 (15s) the first retry alone covers 10s of downtime.
        # We block NFS, start the write (which will stall), then unblock after 10s.
        test_file_survive = f"bp_survive_{tag}.txt"
        test_content_survive = f"survive-{tag}"
        try:
            await block_nfs()
            self.logger.info("Blocked NFS traffic on agent VM (10s transient)")

            # Start the agent write — it will stall waiting for NFS
            write_task = asyncio.create_task(agent_write(test_file_survive, test_content_survive, timeout_s=120))

            # Unblock after 10s to simulate a transient stall
            await asyncio.sleep(10)
            await unblock_nfs()
            self.logger.info("Unblocked NFS after 10s")

            ec, stdout, stderr = await write_task

            if ec == 0:
                try:
                    content = (self._ws.path / test_file_survive).read_text()
                    survive_ok = content == test_content_survive
                except OSError:
                    survive_ok = False
                self.logger.info(f"  Transient block: write {'succeeded' if survive_ok else 'content mismatch'}")
            else:
                survive_ok = False
                self.logger.info(f"  Transient block: write failed — {stderr.strip()[:200]}")

            self._test(
                "nfs_backpressure_survive_10s",
                lambda: survive_ok,
                f"Agent write should survive 10s NFS block with timeo=150, got ec={ec} stderr={stderr.strip()[:200] if not survive_ok else ''}",
            )
        except Exception as e:
            await unblock_nfs()
            self._test("nfs_backpressure_survive_10s", lambda: False, f"Unexpected error: {e}")

        await asyncio.sleep(2)

        # Test 2: Sustained block (>75s) — write SHOULD fail with EIO.
        # This confirms soft mount still has a finite timeout.
        test_file_fail = f"bp_fail_{tag}.txt"
        test_content_fail = f"fail-{tag}"
        try:
            await block_nfs()
            self.logger.info("Blocked NFS traffic on agent VM (sustained)")

            # Agent write should eventually fail with EIO
            ec, stdout, stderr = await agent_write(test_file_fail, test_content_fail, timeout_s=180)

            if ec != 0:
                is_eio = "Input/output error" in stderr or "Errno 5" in stderr
                self.logger.info(f"  Sustained block: write failed as expected, eio={is_eio}")
                self._test(
                    "nfs_backpressure_fail_sustained",
                    lambda: is_eio,
                    f"Sustained NFS block should cause EIO, got: {stderr.strip()[:200]}",
                )
            else:
                self.logger.error("  Sustained block: write unexpectedly succeeded")
                self._test(
                    "nfs_backpressure_fail_sustained",
                    lambda: False,
                    "Agent write should fail when NFS is blocked indefinitely",
                )
        finally:
            await unblock_nfs()
            self.logger.info("Removed iptables NFS block on agent VM")

        # Wait for NFS to recover
        await asyncio.sleep(3)

        # Test 3: Recovery — writes should work after unblocking
        recovery_file = f"bp_recovery_{tag}.txt"
        recovery_content = f"recovery-{tag}"
        ec, _, stderr = await agent_write(recovery_file, recovery_content)
        if ec == 0:
            try:
                recovery_ok = (self._ws.path / recovery_file).read_text() == recovery_content
            except OSError:
                recovery_ok = False
        else:
            recovery_ok = False
            self.logger.warning(f"Recovery write failed: {stderr.strip()[:200]}")
        self._test(
            "nfs_backpressure_recovery",
            lambda: recovery_ok,
            "Agent write should succeed after NFS traffic is unblocked",
        )

        # Cleanup
        for f in [f"bp_baseline_{tag}.txt", test_file_survive, test_file_fail, recovery_file]:
            (self._ws.path / f).unlink(missing_ok=True)

    # ---------------------------------------------------------------
    # Lazy DVC tests — uses the declared tracked_ws (production path)
    # ---------------------------------------------------------------

    async def _run_lazy_dvc_tests(self) -> None:
        self.logger.info("=== Lazy DVC tests ===")

        await run_local(
            "grep -q 'user_allow_other' /etc/fuse.conf 2>/dev/null || echo 'user_allow_other' >> /etc/fuse.conf",
            timeout=5,
        )

        tracked = self._tracked
        content_dir = tracked.path  # /workspace/tracked_ws/data

        # Write test data
        (content_dir / "file1.txt").write_text("hello world")
        (content_dir / "file2.txt").write_text("second file content")
        sub = content_dir / "sub"
        sub.mkdir(exist_ok=True)
        (sub / "nested.txt").write_text("nested content here")
        postgres_dir = content_dir / ".runtime" / "postgres" / "data"
        postgres_dir.mkdir(parents=True, exist_ok=True)
        postgres_dir.chmod(0o700)
        empty_dir = content_dir / "empty_dir"
        empty_dir.mkdir(exist_ok=True)
        large_data = os.urandom(512 * 1024)
        (content_dir / "large.bin").write_bytes(large_data)
        large_md5 = hashlib.md5(large_data).hexdigest()

        # Commit (production code: workspace.commit)
        await self._atest(
            "lazy_dvc_commit",
            lambda: self._async_ok(tracked.commit("lazy_test_step_1")),
            "DVC commit should succeed",
        )

        # Unmount current FUSE, wipe data, restore lazily
        from plato.worlds.lazy_dvc import unmount_lazy

        for mount in list(tracked._lazy_mounts.values()):
            await unmount_lazy(mount)
        tracked._lazy_mounts.clear()

        await self._reset_mount_dir(content_dir)
        shutil.rmtree(tracked._repo_root / ".lazy_cache", ignore_errors=True)

        # Restore (production code: workspace.restore → FUSE mount)
        await self._atest(
            "lazy_dvc_restore",
            lambda: self._async_ok(tracked.restore("lazy_test_step_1")),
            "Lazy FUSE restore should succeed",
        )
        await self._recreate_tracked_agent()

        # Verify FUSE mount exists
        await self._atest(
            "lazy_dvc_is_mount",
            lambda: self._is_mountpoint(content_dir),
            f"{content_dir} should be a FUSE mount after restore",
        )

        # Verify listing
        await self._atest(
            "lazy_dvc_listing",
            lambda: self._ls_contains(content_dir, {"file1.txt", "file2.txt", "large.bin", "sub"}),
            "All files should appear in listing",
        )

        # Read files
        await self._atest(
            "lazy_dvc_read_text",
            lambda: self._cat(content_dir / "file1.txt", "hello world"),
            "Lazy text read should return correct content",
        )
        await self._atest(
            "lazy_dvc_read_nested",
            lambda: self._cat(content_dir / "sub" / "nested.txt", "nested content here"),
            "Nested file read should work",
        )
        await self._atest(
            "lazy_dvc_read_large",
            lambda: self._md5sum(content_dir / "large.bin", large_md5),
            "Large file content should match",
        )

        # File size accuracy (no 1GB sentinel)
        await self._atest(
            "lazy_dvc_size_text",
            lambda: self._stat_size(content_dir / "file1.txt", len("hello world")),
            "File size should match actual content length",
        )
        await self._atest(
            "lazy_dvc_size_large",
            lambda: self._stat_size(content_dir / "large.bin", len(large_data)),
            "Large file size should match",
        )
        await self._atest(
            "lazy_dvc_size_not_sentinel",
            lambda: self._stat_not_sentinel(content_dir / "file1.txt"),
            "File size should not be 1GB sentinel",
        )
        await self._atest(
            "lazy_dvc_restore_dir_mode_initial",
            lambda: self._stat_mode(postgres_dir, 0o700),
            "Postgres data dir should restore with mode 0700",
        )
        await self._atest(
            "lazy_dvc_restore_empty_dir_initial",
            lambda: self._dir_exists(empty_dir),
            "Empty directory should survive first restore",
        )
        if self._agent_hostname:
            await self._atest(
                "lazy_dvc_restore_dir_mode_initial_agent",
                lambda: self._ssh_stat_mode(
                    self._ssh_key_path,
                    self._agent_hostname,
                    self._tracked_agent_path(".runtime/postgres/data"),
                    0o700,
                ),
                "Agent should observe restored Postgres data dir mode 0700",
            )
            await self._atest(
                "lazy_dvc_restore_empty_dir_initial_agent",
                lambda: self._ssh_dir_exists(
                    self._ssh_key_path,
                    self._agent_hostname,
                    self._tracked_agent_path("empty_dir"),
                ),
                "Agent should observe restored empty directory",
            )

        # Modify, create, delete through FUSE
        await self._atest(
            "lazy_dvc_write_new",
            lambda: self._shell_write(content_dir / "new_file.txt", "brand new content"),
            "Creating new file through FUSE should work",
        )
        await self._atest(
            "lazy_dvc_modify",
            lambda: self._shell_write(content_dir / "file1.txt", "modified content"),
            "Modifying file through FUSE should work",
        )
        await self._atest(
            "lazy_dvc_delete",
            lambda: self._shell_rm(content_dir / "file2.txt"),
            "Deleting file through FUSE should work",
        )

        # Symlink
        await self._atest(
            "lazy_dvc_symlink",
            lambda: self._shell_symlink(content_dir / "link_to_file1.txt", "file1.txt"),
            "Creating symlink through FUSE should work",
        )
        await self._atest(
            "lazy_dvc_readlink",
            lambda: self._shell_readlink(content_dir / "link_to_file1.txt", "file1.txt"),
            "readlink should return correct target",
        )
        await self._atest(
            "lazy_dvc_dir_mode_update",
            lambda: self._shell_chmod(postgres_dir, 0o750),
            "Changing Postgres data dir mode through FUSE should work",
        )

        # Smart commit (production code: workspace.commit with lazy mounts)
        await self._atest(
            "lazy_dvc_smart_commit",
            lambda: self._async_ok(tracked.commit("lazy_test_step_2")),
            "Smart commit should succeed",
        )

        # Restore the smart-committed version
        for mount in list(tracked._lazy_mounts.values()):
            await unmount_lazy(mount)
        tracked._lazy_mounts.clear()

        await self._reset_mount_dir(content_dir)
        shutil.rmtree(tracked._repo_root / ".lazy_cache", ignore_errors=True)

        await self._atest(
            "lazy_dvc_restore_smart",
            lambda: self._async_ok(tracked.restore("lazy_test_step_2")),
            "Restore of smart-committed data should work",
        )
        await self._recreate_tracked_agent()

        # Verify smart commit changes persisted
        await self._atest(
            "lazy_dvc_verify_modified",
            lambda: self._cat(content_dir / "file1.txt", "modified content"),
            "Modified file should have new content",
        )
        await self._atest(
            "lazy_dvc_verify_new",
            lambda: self._cat(content_dir / "new_file.txt", "brand new content"),
            "New file should exist",
        )
        await self._atest(
            "lazy_dvc_verify_deleted",
            lambda: self._file_absent(content_dir / "file2.txt"),
            "Deleted file should not exist",
        )
        await self._atest(
            "lazy_dvc_verify_untouched",
            lambda: self._cat(content_dir / "sub" / "nested.txt", "nested content here"),
            "Untouched file should have original content",
        )
        await self._atest(
            "lazy_dvc_verify_symlink",
            lambda: self._shell_readlink(content_dir / "link_to_file1.txt", "file1.txt"),
            "Symlink should survive commit/restore cycle",
        )
        await self._atest(
            "lazy_dvc_verify_dir_mode_restored",
            lambda: self._stat_mode(postgres_dir, 0o750),
            "Postgres data dir should survive commit/restore with mode 0750",
        )
        await self._atest(
            "lazy_dvc_verify_empty_dir_restored",
            lambda: self._dir_exists(empty_dir),
            "Empty directory should survive smart commit restore",
        )
        if self._agent_hostname:
            await self._atest(
                "lazy_dvc_verify_dir_mode_restored_agent",
                lambda: self._ssh_stat_mode(
                    self._ssh_key_path,
                    self._agent_hostname,
                    self._tracked_agent_path(".runtime/postgres/data"),
                    0o750,
                ),
                "Agent should observe restored Postgres data dir mode 0750",
            )
            await self._atest(
                "lazy_dvc_verify_empty_dir_restored_agent",
                lambda: self._ssh_dir_exists(
                    self._ssh_key_path,
                    self._agent_hostname,
                    self._tracked_agent_path("empty_dir"),
                ),
                "Agent should observe restored empty directory after smart commit",
            )

    # ---------------------------------------------------------------
    # SSH / shell helpers
    # ---------------------------------------------------------------

    async def _ssh_cat(self, ssh_key_path, hostname, filepath, expected) -> bool:
        ec, stdout, _ = await run_ssh(ssh_key_path, hostname, f"cat {filepath}", timeout=10)
        return ec == 0 and stdout == expected

    async def _ssh_file_size(self, ssh_key_path, hostname, filepath, expected_size) -> bool:
        ec, stdout, _ = await run_ssh(ssh_key_path, hostname, f"stat -c '%s' {filepath}", timeout=10)
        return ec == 0 and stdout.strip() == str(expected_size)

    async def _ssh_file_absent(self, ssh_key_path, hostname, filepath) -> bool:
        ec, _, _ = await run_ssh(ssh_key_path, hostname, f"test ! -f {filepath}", timeout=10)
        return ec == 0

    async def _ssh_stat_mode(self, ssh_key_path, hostname, filepath, expected_mode: int) -> bool:
        ec, stdout, _ = await run_ssh(ssh_key_path, hostname, f"stat -c '%a' {filepath}", timeout=10)
        return ec == 0 and stdout.strip() == format(expected_mode, "o")

    async def _ssh_dir_exists(self, ssh_key_path, hostname, filepath) -> bool:
        ec, _, _ = await run_ssh(ssh_key_path, hostname, f"test -d {filepath}", timeout=10)
        return ec == 0

    def _ok(self, exit_code) -> bool:
        return exit_code == 0

    async def _async_ok(self, coro) -> bool:
        await coro
        return True

    async def _cat(self, path: Path, expected: str) -> bool:
        ec, stdout, _ = await run_local(f"cat {path}", timeout=30)
        return ec == 0 and stdout == expected

    async def _md5sum(self, path: Path, expected_md5: str) -> bool:
        ec, stdout, _ = await run_local(f"md5sum {path}", timeout=30)
        return ec == 0 and stdout.strip().split()[0] == expected_md5

    async def _ls_contains(self, path: Path, expected: set[str]) -> bool:
        ec, stdout, _ = await run_local(f"ls {path}", timeout=10)
        return ec == 0 and expected.issubset(set(stdout.strip().split()))

    async def _stat_size(self, path: Path, expected_size: int) -> bool:
        ec, stdout, _ = await run_local(f"stat -c '%s' {path}", timeout=10)
        return ec == 0 and int(stdout.strip()) == expected_size

    async def _stat_not_sentinel(self, path: Path) -> bool:
        ec, stdout, _ = await run_local(f"stat -c '%s' {path}", timeout=10)
        return ec == 0 and int(stdout.strip()) != (1 << 30)

    async def _file_absent(self, path: Path) -> bool:
        ec, _, _ = await run_local(f"test ! -f {path}", timeout=5)
        return ec == 0

    async def _reset_mount_dir(self, path: Path) -> None:
        await run_local(
            f"fusermount3 -uz '{path}' 2>/dev/null || fusermount3 -u '{path}' 2>/dev/null || true",
            timeout=10,
        )
        await asyncio.sleep(1)
        await run_local(f"rm -rf '{path}' && mkdir -p '{path}'", timeout=10)

    async def _stat_mode(self, path: Path, expected_mode: int) -> bool:
        ec, stdout, _ = await run_local(f"stat -c '%a' {path}", timeout=10)
        return ec == 0 and stdout.strip() == format(expected_mode, "o")

    async def _dir_exists(self, path: Path) -> bool:
        ec, _, _ = await run_local(f"test -d {path}", timeout=5)
        return ec == 0

    async def _shell_write(self, path: Path, content: str) -> bool:
        ec, _, _ = await run_local(
            f"{sys.executable} -c \"from pathlib import Path; Path('{path}').write_text('{content}')\"",
            timeout=60,
        )
        return ec == 0

    async def _shell_rm(self, path: Path) -> bool:
        ec, _, _ = await run_local(f"rm -f {path}", timeout=10)
        return ec == 0

    async def _shell_symlink(self, link_path: Path, target: str) -> bool:
        ec, _, _ = await run_local(f"ln -s '{target}' '{link_path}'", timeout=10)
        return ec == 0

    async def _shell_readlink(self, path: Path, expected: str) -> bool:
        ec, stdout, _ = await run_local(f"readlink '{path}'", timeout=10)
        return ec == 0 and stdout.strip() == expected

    async def _shell_chmod(self, path: Path, mode: int) -> bool:
        ec, _, _ = await run_local(f"chmod {format(mode, 'o')} '{path}'", timeout=10)
        return ec == 0
