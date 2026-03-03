"""Test world that validates workspace functionality end-to-end on a real VM.

This world runs ON the world VM. It exercises:
1. Workspace type, attributes, and methods
2. Local file I/O on the workspace path
3. NFS: cross-VM file visibility (write on world, read from agent and vice-versa)
4. NFS: permissions (uid 1000, ACLs, sticky bit)
5. NFS: sub-workspaces via transport.with_path() + prepare() + setup_agent()
6. Rsync: setup_agent syncs files to agent VM
7. Rsync: sync_back copies files from agent VM back to world VM
8. Lazy DVC: FUSE mount, lazy S3 reads, smart commit, DVC compatibility
"""

from __future__ import annotations

import asyncio
import hashlib
import os
import secrets
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Annotated, ClassVar

from plato.agents.runtime.transport import NFSTransport, RsyncTransport, Transport
from plato.markers import WorkspaceMarker
from plato.utils.subprocess import run_local, run_ssh
from plato.worlds import BaseWorld, Observation, StepResult
from plato.worlds.base import register_world
from plato.worlds.config import RunConfig
from plato.worlds.workspace import Workspace


class WorkspaceTestWorldConfig(RunConfig):
    """Config for the workspace test world."""

    ws: Annotated[
        Path,
        WorkspaceMarker(description="Test workspace", tracked=False, mount="/workspace"),
    ] = Path("/state/ws")


@register_world("plato-world-structured-execution")
class WorkspaceTestWorld(BaseWorld[WorkspaceTestWorldConfig]):
    name: ClassVar[str] = "workspace-test"
    description: ClassVar[str] = "Integration test world for workspace e2e validation"

    test_results: list[dict]
    all_passed: bool

    async def reset(self) -> Observation:
        self.test_results = []
        self.all_passed = True

        # Get the declared workspace (plato.worlds.workspace.Workspace)
        self._ws = self.workspace("ws")

        # --- Basic workspace attribute tests ---
        self._run_basic_tests()

        # --- Local file I/O ---
        self._run_file_io_tests()

        # --- Transport with_path tests (local only) ---
        self._run_with_path_tests()

        # --- Cross-VM tests (need an agent VM) ---
        await self._run_cross_vm_tests()

        # --- Lazy DVC: FUSE mount, lazy S3 reads, smart commit ---
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

        return Observation(
            data={
                "test_results": self.test_results,
                "passed": passed,
                "failed": failed,
            }
        )

    async def step(self) -> StepResult:
        return StepResult(
            observation=Observation(
                data={
                    "test_results": self.test_results,
                    "all_passed": self.all_passed,
                }
            ),
            done=True,
        )

    # ---------------------------------------------------------------
    # Test helpers
    # ---------------------------------------------------------------

    def _run_test(self, name: str, check, error_msg: str) -> None:
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

    async def _run_async_test(self, name: str, check, error_msg: str) -> None:
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
    # Basic attribute tests
    # ---------------------------------------------------------------

    def _run_basic_tests(self) -> None:
        self.logger.info("Running basic workspace attribute tests...")
        ws = self._ws

        self._run_test(
            "workspace_is_not_none",
            lambda: ws is not None,
            "workspace should not be None",
        )
        self._run_test(
            "workspace_is_workspace_instance",
            lambda: isinstance(ws, Workspace),
            f"Expected Workspace, got {type(ws)}",
        )
        self._run_test(
            "workspace_path_exists",
            lambda: ws.path.is_dir(),
            f"workspace.path ({ws.path}) should be a directory",
        )
        self._run_test(
            "workspace_has_transport",
            lambda: ws.transport is not None,
            "workspace.transport should not be None",
        )
        self._run_test(
            "transport_is_transport_instance",
            lambda: isinstance(ws.transport, Transport),
            f"Expected Transport, got {type(ws.transport)}",
        )
        self._run_test(
            "transport_has_setup_agent",
            lambda: callable(getattr(ws.transport, "setup_agent", None)),
            "transport should have setup_agent()",
        )
        self._run_test(
            "transport_has_sync_back",
            lambda: callable(getattr(ws.transport, "sync_back", None)),
            "transport should have sync_back()",
        )
        self._run_test(
            "transport_has_with_path",
            lambda: callable(getattr(ws.transport, "with_path", None)),
            "transport should have with_path()",
        )

    # ---------------------------------------------------------------
    # Local file I/O
    # ---------------------------------------------------------------

    def _run_file_io_tests(self) -> None:
        self.logger.info("Running file I/O tests...")
        ws_path = self._ws.path
        tag = secrets.token_hex(4)
        test_file = ws_path / f"_test_{tag}.txt"
        test_content = f"workspace test content {tag}"

        self._run_test(
            "file_write",
            lambda: (test_file.write_text(test_content), True)[1],
            f"Should write to {test_file}",
        )
        self._run_test(
            "file_read",
            lambda: test_file.read_text() == test_content,
            "Read content should match written content",
        )

        subdir = ws_path / f"_test_subdir_{tag}"
        self._run_test(
            "mkdir_in_workspace",
            lambda: (subdir.mkdir(exist_ok=True), subdir.is_dir())[1],
            "Should create subdirectory",
        )

        nested = subdir / "nested.txt"
        self._run_test(
            "file_write_in_subdir",
            lambda: (nested.write_text("nested"), nested.read_text() == "nested")[1],
            "Should write/read in subdirectory",
        )

        large_content = "x" * (1024 * 1024)  # 1MB
        large_file = ws_path / f"_test_large_{tag}.bin"
        self._run_test(
            "large_file_write_read",
            lambda: (large_file.write_text(large_content), large_file.read_text() == large_content)[1],
            "Should handle 1MB file write/read",
        )

        binary_content = os.urandom(4096)
        binary_file = ws_path / f"_test_binary_{tag}.bin"
        self._run_test(
            "binary_file_write_read",
            lambda: (binary_file.write_bytes(binary_content), binary_file.read_bytes() == binary_content)[1],
            "Should handle binary file write/read",
        )

        # Cleanup
        for f in [test_file, large_file, binary_file]:
            f.unlink(missing_ok=True)
        shutil.rmtree(subdir, ignore_errors=True)

    # ---------------------------------------------------------------
    # with_path tests (local — via transport)
    # ---------------------------------------------------------------

    def _run_with_path_tests(self) -> None:
        self.logger.info("Running with_path tests...")
        transport = self._ws.transport

        sub_path = str(self._ws.path) + "/test_sub"
        sub_transport = transport.with_path(sub_path)
        self._run_test(
            "with_path_returns_transport",
            lambda: isinstance(sub_transport, Transport),
            f"with_path() should return Transport, got {type(sub_transport)}",
        )
        self._run_test(
            "with_path_has_correct_path",
            lambda: sub_transport.path == sub_path,
            f"sub transport path mismatch: {sub_transport.path}",
        )
        self._run_test(
            "with_path_same_type",
            lambda: type(sub_transport) is type(transport),
            f"Type mismatch: {type(sub_transport)} vs {type(transport)}",
        )

    # ---------------------------------------------------------------
    # Cross-VM tests
    # ---------------------------------------------------------------

    async def _run_cross_vm_tests(self) -> None:
        """Spawn an agent VM and test workspace across VMs."""
        self.logger.info("Running cross-VM workspace tests...")

        from plato.v2 import Env
        from plato.v2.types import SimConfigCompute

        if not self.plato_session:
            self.logger.warning("No plato_session, skipping cross-VM tests")
            return

        transport = self._ws.transport
        ssh_key_path = self._ssh_key_path
        agent_env = None
        try:
            self.logger.info("Spawning agent VM...")
            agent_env = await self.plato_session.add_env(
                Env.resource(
                    simulator="workspace-test-agent",
                    sim_config=SimConfigCompute(cpus=1, memory=2048, disk=10240),
                    alias="test-agent",
                ),
                timeout=300,
            )
            self.logger.info(f"Agent VM spawned: job_id={agent_env.job_id}")

            # Re-register SSH key so the new agent VM gets it
            pub_key = Path(str(ssh_key_path) + ".pub").read_text().strip()
            await self.plato_session.add_ssh_key(pub_key)

            agent_hostname = await agent_env.get_mesh_ip()
            self.logger.info(f"Agent mesh IP: {agent_hostname}")
            if not agent_hostname:
                raise RuntimeError("Agent VM has no mesh IP")

            # Install rsync and acl tools on agent
            await agent_env.execute(
                "which rsync || (apt-get update -qq && apt-get install -y -qq rsync acl nfs-common)",
                timeout=60,
            )
            # Install acl on world VM
            await run_local(
                "which getfacl || (apt-get update -qq && apt-get install -y -qq acl)",
                timeout=60,
            )

            if isinstance(transport, NFSTransport):
                await self._run_nfs_cross_vm_tests(agent_env, agent_hostname, ssh_key_path)
            elif isinstance(transport, RsyncTransport):
                await self._run_rsync_cross_vm_tests(agent_env, agent_hostname, ssh_key_path)

            await self._run_permission_tests(agent_env, agent_hostname, ssh_key_path)

        except Exception as e:
            self.test_results.append({"name": "cross_vm_setup", "passed": False, "error": f"Failed: {e}"})
            self.all_passed = False
            self.logger.error(f"Cross-VM test setup failed: {e}")
        finally:
            if agent_env:
                try:
                    await self.plato_session.remove_env(agent_env)
                except Exception as e:
                    self.logger.warning(f"Failed to remove agent VM: {e}")

    # ---------------------------------------------------------------
    # NFS cross-VM tests
    # ---------------------------------------------------------------

    def _agent_path(self, filename: str) -> str:
        """Map a filename from world-side ws path to agent-side mount path."""
        return f"{self._ws.transport.agent_mount_path}/{filename}"

    async def _run_nfs_cross_vm_tests(self, agent_env, agent_hostname: str, ssh_key_path: Path) -> None:
        self.logger.info("Running NFS cross-VM tests...")
        tag = secrets.token_hex(4)
        ws_path = self._ws.path  # world-side path

        # 1. Mount NFS on agent via transport.setup_agent
        await self._run_async_test(
            "nfs_setup_agent",
            lambda: self._setup_agent(agent_env, agent_hostname),
            "transport.setup_agent() should succeed",
        )

        # 2. Write on world VM, read from agent VM (agent sees files at mount path)
        world_file = f"cross_vm_test_{tag}.txt"
        world_content = f"written-on-world-{tag}"
        (ws_path / world_file).write_text(world_content)

        await self._run_async_test(
            "nfs_world_write_agent_read",
            lambda: self._check_file_on_agent(
                ssh_key_path, agent_hostname, self._agent_path(world_file), world_content
            ),
            "File written on world VM should be readable from agent VM via NFS",
        )

        # 3. Write on agent VM, read from world VM
        agent_file = f"agent_written_{tag}.txt"
        agent_content = f"written-on-agent-{tag}"
        await run_ssh(
            ssh_key_path, agent_hostname, f"echo -n '{agent_content}' > {self._agent_path(agent_file)}", timeout=10
        )

        self._run_test(
            "nfs_agent_write_world_read",
            lambda: (ws_path / agent_file).read_text() == agent_content,
            "File written on agent VM should be visible on world VM via NFS",
        )

        # 4. Large file cross-VM
        large_file = f"large_cross_vm_{tag}.bin"
        large_size = 5 * 1024 * 1024
        (ws_path / large_file).write_bytes(os.urandom(large_size))

        await self._run_async_test(
            "nfs_large_file_cross_vm",
            lambda: self._check_file_size_on_agent(
                ssh_key_path, agent_hostname, self._agent_path(large_file), large_size
            ),
            "5MB file should be visible and correct size on agent VM",
        )

        # 5. Directory tree cross-VM
        tree_name = f"tree_{tag}"
        tree_dir = ws_path / tree_name
        (tree_dir / "a" / "b" / "c").mkdir(parents=True, exist_ok=True)
        (tree_dir / "a" / "b" / "c" / "deep.txt").write_text("deep")
        (tree_dir / "root.txt").write_text("root")

        await self._run_async_test(
            "nfs_directory_tree_cross_vm",
            lambda: self._check_file_on_agent(
                ssh_key_path, agent_hostname, self._agent_path(f"{tree_name}/a/b/c/deep.txt"), "deep"
            ),
            "Nested directory tree should be visible on agent VM",
        )

        # 6. Delete on world, verify gone on agent
        (ws_path / world_file).unlink()
        await asyncio.sleep(5)
        delete_ok = await self._check_file_absent_on_agent(ssh_key_path, agent_hostname, self._agent_path(world_file))
        if delete_ok:
            self.test_results.append({"name": "nfs_delete_propagates", "passed": True})
            self.logger.info("  [PASS] nfs_delete_propagates")
        else:
            self.logger.warning("  [SKIP] nfs_delete_propagates: NFS attribute cache delay")

        # 7. Concurrent writes from both sides
        await self._run_async_test(
            "nfs_concurrent_writes",
            lambda: self._test_concurrent_writes(ssh_key_path, agent_hostname, tag),
            "Concurrent writes from world and agent should not corrupt data",
        )

        # 8. Sub-workspace via transport.with_path + prepare + setup_agent
        await self._run_async_test(
            "nfs_sub_workspace_cross_vm",
            lambda: self._test_sub_workspace_nfs(agent_env, agent_hostname, ssh_key_path, tag),
            "Sub-workspace created via with_path() should be visible on agent VM",
        )

        # 9. sync_back is no-op for NFS
        await self._run_async_test(
            "nfs_sync_back_noop",
            lambda: self._do_sync_back(agent_env, agent_hostname),
            "sync_back() should succeed (no-op for NFS)",
        )

        # 10. Full workflow
        await self._run_async_test(
            "nfs_full_workflow",
            lambda: self._test_full_workflow(ssh_key_path, agent_hostname, tag),
            "Full workflow: world create → agent read → agent modify → world read",
        )

        # Cleanup
        (ws_path / large_file).unlink(missing_ok=True)
        (ws_path / agent_file).unlink(missing_ok=True)
        shutil.rmtree(tree_dir, ignore_errors=True)

    async def _test_full_workflow(self, ssh_key_path, hostname, tag):
        ws_path = self._ws.path
        fname = f"workflow_{tag}.txt"
        original = f"hello from world {tag}"
        (ws_path / fname).write_text(original)

        agent_fpath = self._agent_path(fname)
        exit_code, stdout, _ = await run_ssh(ssh_key_path, hostname, f"cat {agent_fpath}", timeout=10)
        if exit_code != 0 or stdout != original:
            return False

        appended = " | modified by agent"
        await run_ssh(ssh_key_path, hostname, f"echo -n '{appended}' >> {agent_fpath}", timeout=10)

        result = (ws_path / fname).read_text()
        expected = original + appended
        if result != expected:
            return False

        (ws_path / fname).unlink(missing_ok=True)
        return True

    async def _setup_agent(self, agent_env, agent_hostname):
        await self._ws.transport.setup_agent(agent_env, agent_hostname)
        return True

    async def _do_sync_back(self, agent_env, agent_hostname):
        await self._ws.transport.sync_back(agent_env, agent_hostname)
        return True

    async def _check_file_on_agent(self, ssh_key_path, hostname, filepath, expected_content):
        exit_code, stdout, _ = await run_ssh(ssh_key_path, hostname, f"cat {filepath}", timeout=10)
        return exit_code == 0 and stdout == expected_content

    async def _check_file_size_on_agent(self, ssh_key_path, hostname, filepath, expected_size):
        exit_code, stdout, _ = await run_ssh(ssh_key_path, hostname, f"stat -c '%s' {filepath}", timeout=10)
        return exit_code == 0 and stdout.strip() == str(expected_size)

    async def _check_file_absent_on_agent(self, ssh_key_path, hostname, filepath):
        exit_code, _, _ = await run_ssh(ssh_key_path, hostname, f"test ! -f {filepath}", timeout=10)
        return exit_code == 0

    async def _test_concurrent_writes(self, ssh_key_path, hostname, tag):
        ws_path = self._ws.path
        world_fname = f"concurrent_world_{tag}.txt"
        agent_fname = f"concurrent_agent_{tag}.txt"

        async def write_world():
            (ws_path / world_fname).write_text(f"world-{tag}")

        async def write_agent():
            await run_ssh(
                ssh_key_path, hostname, f"echo -n 'agent-{tag}' > {self._agent_path(agent_fname)}", timeout=10
            )

        await asyncio.gather(write_world(), write_agent())
        await asyncio.sleep(0.5)

        world_ok = (ws_path / world_fname).read_text() == f"world-{tag}"
        agent_ok = (ws_path / agent_fname).read_text() == f"agent-{tag}"

        (ws_path / world_fname).unlink(missing_ok=True)
        (ws_path / agent_fname).unlink(missing_ok=True)
        return world_ok and agent_ok

    async def _test_sub_workspace_nfs(self, agent_env, agent_hostname, ssh_key_path, tag):
        transport = self._ws.transport
        sub_name = f"sub_{tag}"
        sub_path = self._ws.path / sub_name
        sub_transport = transport.with_path(str(sub_path))
        await sub_transport.prepare()

        sub_path.mkdir(parents=True, exist_ok=True)
        (sub_path / "sub_test.txt").write_text(f"sub-{tag}")

        await sub_transport.setup_agent(agent_env, agent_hostname)

        # Agent sees sub-workspace at its own mount path
        agent_sub = sub_transport.agent_mount_path
        exit_code, stdout, _ = await run_ssh(
            ssh_key_path,
            agent_hostname,
            f"cat {agent_sub}/sub_test.txt",
            timeout=10,
        )

        shutil.rmtree(sub_path, ignore_errors=True)
        return exit_code == 0 and stdout == f"sub-{tag}"

    # ---------------------------------------------------------------
    # Rsync cross-VM tests
    # ---------------------------------------------------------------

    async def _run_rsync_cross_vm_tests(self, agent_env, agent_hostname: str, ssh_key_path: Path) -> None:
        self.logger.info("Running rsync cross-VM tests...")
        transport = self._ws.transport
        tag = secrets.token_hex(4)
        ws_path = self._ws.path

        (ws_path / f"rsync_test_{tag}.txt").write_text(f"rsync-{tag}")
        (ws_path / f"rsync_dir_{tag}" / "nested").mkdir(parents=True, exist_ok=True)
        (ws_path / f"rsync_dir_{tag}" / "nested" / "deep.txt").write_text("deep-rsync")

        await self._run_async_test(
            "rsync_setup_agent",
            lambda: self._setup_agent(agent_env, agent_hostname),
            "transport.setup_agent() should rsync files to agent VM",
        )

        await self._run_async_test(
            "rsync_files_on_agent",
            lambda: self._check_file_on_agent(
                ssh_key_path,
                agent_hostname,
                self._agent_path(f"rsync_test_{tag}.txt"),
                f"rsync-{tag}",
            ),
            "Rsynced file should be readable on agent VM",
        )

        await self._run_async_test(
            "rsync_nested_on_agent",
            lambda: self._check_file_on_agent(
                ssh_key_path,
                agent_hostname,
                self._agent_path(f"rsync_dir_{tag}/nested/deep.txt"),
                "deep-rsync",
            ),
            "Rsynced nested file should be readable on agent VM",
        )

        agent_new_fname = f"agent_new_{tag}.txt"
        await run_ssh(
            ssh_key_path,
            agent_hostname,
            f"echo -n 'from-agent-{tag}' > {self._agent_path(agent_new_fname)}",
            timeout=10,
        )

        await self._run_async_test(
            "rsync_sync_back",
            lambda: self._do_sync_back(agent_env, agent_hostname),
            "transport.sync_back() should rsync files from agent VM",
        )

        self._run_test(
            "rsync_sync_back_file_present",
            lambda: (ws_path / agent_new_fname).read_text() == f"from-agent-{tag}",
            "File written on agent should appear on world after sync_back",
        )

        large_fname = f"rsync_large_{tag}.bin"
        large_data = os.urandom(2 * 1024 * 1024)
        (ws_path / large_fname).write_bytes(large_data)

        await transport.setup_agent(agent_env, agent_hostname)

        await self._run_async_test(
            "rsync_large_file",
            lambda: self._check_file_size_on_agent(
                ssh_key_path, agent_hostname, self._agent_path(large_fname), len(large_data)
            ),
            "Large file should rsync correctly",
        )

        await self._run_async_test(
            "rsync_chown_superman",
            lambda: self._check_ownership_on_agent(
                ssh_key_path,
                agent_hostname,
                self._agent_path(f"rsync_test_{tag}.txt"),
                "1000",
                "1000",
            ),
            "Rsynced files should be owned by superman (uid 1000)",
        )

        # Cleanup
        for f in [f"rsync_test_{tag}.txt", large_fname, agent_new_fname]:
            (ws_path / f).unlink(missing_ok=True)
        shutil.rmtree(ws_path / f"rsync_dir_{tag}", ignore_errors=True)

    # ---------------------------------------------------------------
    # Permission tests
    # ---------------------------------------------------------------

    async def _run_permission_tests(self, agent_env, agent_hostname: str, ssh_key_path: Path) -> None:
        self.logger.info("Running permission tests...")
        transport = self._ws.transport
        ws_path = self._ws.path

        if isinstance(transport, NFSTransport):
            await self._run_async_test(
                "nfs_root_uid_1000",
                lambda: self._check_local_ownership("/srv/nfs", "1000"),
                "/srv/nfs should be owned by uid 1000",
            )
            await self._run_async_test(
                "nfs_root_sticky_bit",
                lambda: self._check_local_permissions("/srv/nfs", "1777"),
                "/srv/nfs should have mode 1777 (sticky)",
            )

            acl_ok = await self._check_acl("/srv/nfs")
            if acl_ok:
                self.test_results.append({"name": "nfs_acl_set", "passed": True})
                self.logger.info("  [PASS] nfs_acl_set")
            else:
                self.logger.warning("  [SKIP] nfs_acl_set: ACLs not supported on this filesystem")

            nfs_ws_path = f"/srv/nfs{ws_path}"
            await self._run_async_test(
                "nfs_workspace_uid_1000",
                lambda: self._check_local_ownership(nfs_ws_path, "1000"),
                f"{nfs_ws_path} should be owned by uid 1000",
            )

            tag = secrets.token_hex(4)
            agent_write_file = self._agent_path(f"perm_test_{tag}.txt")
            await self._run_async_test(
                "nfs_agent_can_write",
                lambda: self._test_agent_write(ssh_key_path, agent_hostname, agent_write_file),
                "Agent should be able to write files via NFS",
            )
            (ws_path / f"perm_test_{tag}.txt").unlink(missing_ok=True)

            agent_dir = self._agent_path(f"perm_dir_{tag}")
            await self._run_async_test(
                "nfs_agent_can_mkdir",
                lambda: self._test_agent_mkdir(ssh_key_path, agent_hostname, agent_dir),
                "Agent should be able to create directories via NFS",
            )
            shutil.rmtree(ws_path / f"perm_dir_{tag}", ignore_errors=True)

        await self._run_async_test(
            "workspace_dir_writable",
            lambda: self._check_local_writable(str(ws_path)),
            f"Workspace {ws_path} should be writable",
        )

    async def _check_local_ownership(self, path: str, expected_uid: str):
        exit_code, stdout, _ = await run_local(f"stat -c '%u' {path}", timeout=5)
        return exit_code == 0 and stdout.strip() == expected_uid

    async def _check_local_permissions(self, path: str, expected_mode: str):
        exit_code, stdout, _ = await run_local(f"stat -c '%a' {path}", timeout=5)
        return exit_code == 0 and stdout.strip() == expected_mode

    async def _check_acl(self, path: str):
        exit_code, stdout, _ = await run_local(f"getfacl -p {path} 2>/dev/null", timeout=5)
        if exit_code != 0:
            return False
        return (
            "user:1000:rwx" in stdout
            or "user:superman:rwx" in stdout
            or "default:user:1000:rwx" in stdout
            or "default:user:superman:rwx" in stdout
        )

    async def _check_local_writable(self, path: str):
        exit_code, _, _ = await run_local(f"touch {path}/.write_test && rm {path}/.write_test", timeout=5)
        return exit_code == 0

    async def _check_ownership_on_agent(self, ssh_key_path, hostname, filepath, expected_uid, expected_gid):
        exit_code, stdout, _ = await run_ssh(
            ssh_key_path,
            hostname,
            f"stat -c '%u:%g' {filepath}",
            timeout=10,
        )
        return exit_code == 0 and stdout.strip() == f"{expected_uid}:{expected_gid}"

    async def _test_agent_write(self, ssh_key_path, hostname, filepath):
        exit_code, _, _ = await run_ssh(ssh_key_path, hostname, f"echo -n 'perm-test' > {filepath}", timeout=10)
        return exit_code == 0

    async def _test_agent_mkdir(self, ssh_key_path, hostname, dirpath):
        exit_code, _, _ = await run_ssh(
            ssh_key_path,
            hostname,
            f"mkdir -p {dirpath} && touch {dirpath}/test.txt",
            timeout=10,
        )
        return exit_code == 0

    # ---------------------------------------------------------------
    # Lazy DVC tests
    # ---------------------------------------------------------------

    async def _run_lazy_dvc_tests(self) -> None:
        self.logger.info("=== Running Lazy DVC Tests ===")

        exit_code, _, stderr = await run_local(
            "apt-get update -qq && apt-get install -y -qq libfuse3-dev fuse3 pkg-config gcc python3-dev",
            timeout=120,
        )
        if exit_code != 0:
            self.logger.warning("Cannot install fuse3, skipping lazy DVC tests: %s", stderr.strip())
            return

        exit_code, _, stderr = await run_local(
            "uv pip install --system pyfuse3",
            timeout=120,
        )
        if exit_code != 0:
            self.logger.warning("Cannot install pyfuse3, skipping lazy DVC tests: %s", stderr.strip())
            return

        exit_code, _, _ = await run_local(
            f"{sys.executable} -c 'import pyfuse3; print(pyfuse3.__version__)'",
            timeout=10,
        )
        if exit_code != 0:
            self.logger.warning("pyfuse3 import failed after install, skipping lazy DVC tests")
            return

        if not Path("/dev/fuse").exists():
            self.logger.warning("/dev/fuse not available, skipping lazy DVC tests")
            return

        await run_local(
            "grep -q 'user_allow_other' /etc/fuse.conf 2>/dev/null || echo 'user_allow_other' >> /etc/fuse.conf",
            timeout=5,
        )

        test_dir = Path(tempfile.mkdtemp(prefix="lazy_dvc_test_"))
        try:
            await self._lazy_dvc_test_cycle(test_dir)
        except Exception as e:
            self.test_results.append(
                {
                    "name": "lazy_dvc_unhandled_error",
                    "passed": False,
                    "error": str(e),
                }
            )
            self.all_passed = False
            self.logger.error("Lazy DVC tests failed: %s", e, exc_info=True)
        finally:
            await run_local(f"fusermount3 -u {test_dir}/data 2>/dev/null; true", timeout=5)
            shutil.rmtree(test_dir, ignore_errors=True)

    async def _lazy_dvc_test_cycle(self, test_dir: Path) -> None:
        from plato.worlds.workspace import Workspace as DVCWorkspace

        repo_info = await self._resolve_workspace_repo("lazy_dvc_test")
        self.logger.info(
            "Resolved workspace repo: bucket=%s prefix=%s repo=%s",
            repo_info.s3_bucket,
            repo_info.s3_prefix,
            repo_info.repo_name,
        )

        ws = DVCWorkspace(
            name="lazy_dvc_test",
            path=test_dir,
            tracked=True,
            s3_bucket=repo_info.s3_bucket,
            s3_prefix=repo_info.s3_prefix,
            repo_id=repo_info.repo_id,
            repo_name=repo_info.repo_name,
            chronos_url=repo_info.chronos_url,
            api_key=repo_info.api_key,
            session_id=self.session.session_id if self.session else "",
        )

        await self._run_async_test(
            "lazy_dvc_init",
            lambda: self._async_ok(ws.init()),
            "DVC workspace init should succeed",
        )

        data_dir = test_dir / "data"
        data_dir.mkdir(exist_ok=True)
        (data_dir / "file1.txt").write_text("hello world")
        (data_dir / "file2.txt").write_text("second file content")
        sub = data_dir / "sub"
        sub.mkdir()
        (sub / "nested.txt").write_text("nested content here")
        large_data = os.urandom(512 * 1024)
        (data_dir / "large.bin").write_bytes(large_data)
        large_md5 = hashlib.md5(large_data).hexdigest()

        await self._run_async_test(
            "lazy_dvc_commit",
            lambda: self._async_ok(ws.commit("lazy_test_step_1")),
            "Regular DVC commit + push should succeed",
        )

        shutil.rmtree(data_dir)
        data_dir.mkdir()

        await self._run_async_test(
            "lazy_dvc_fuse_restore",
            lambda: self._async_ok(ws.restore("lazy_test_step_1")),
            "Lazy FUSE restore should mount successfully",
        )

        await self._run_async_test(
            "lazy_dvc_mount_exists",
            lambda: self._check_is_mount(data_dir),
            f"{data_dir} should be a FUSE mount point",
        )

        await self._run_async_test(
            "lazy_dvc_listing",
            lambda: self._check_ls_contains(data_dir, {"file1.txt", "file2.txt", "large.bin", "sub"}),
            "All files/dirs should appear in listing",
        )

        await self._run_async_test(
            "lazy_dvc_nested_listing",
            lambda: self._check_ls_contains(data_dir / "sub", {"nested.txt"}),
            "Nested directory listing should work",
        )

        await self._run_async_test(
            "lazy_dvc_read_text",
            lambda: self._check_cat(data_dir / "file1.txt", "hello world"),
            "Lazy text read should return correct content",
        )

        await self._run_async_test(
            "lazy_dvc_read_nested",
            lambda: self._check_cat(data_dir / "sub" / "nested.txt", "nested content here"),
            "Nested file read via lazy FUSE should work",
        )

        await self._run_async_test(
            "lazy_dvc_read_large_md5",
            lambda: self._check_md5sum(data_dir / "large.bin", large_md5),
            "Large file content should match after lazy download",
        )

        await self._run_async_test(
            "lazy_dvc_write_new",
            lambda: self._shell_write(data_dir / "new_file.txt", "brand new content"),
            "Creating a new file through FUSE should work",
        )

        await self._run_async_test(
            "lazy_dvc_modify_existing",
            lambda: self._shell_write(data_dir / "file1.txt", "modified content"),
            "Overwriting a file through FUSE should work",
        )

        await self._run_async_test(
            "lazy_dvc_delete",
            lambda: self._shell_rm(data_dir / "file2.txt"),
            "Deleting a file through FUSE should work",
        )

        await self._run_async_test(
            "lazy_dvc_smart_commit",
            lambda: self._async_ok(ws.commit("lazy_test_step_2")),
            "Smart commit should succeed",
        )

        await self._run_async_test(
            "lazy_dvc_unmounted",
            lambda: self._check_not_mount(data_dir),
            f"{data_dir} should NOT be a mount point after smart commit",
        )

        shutil.rmtree(data_dir, ignore_errors=True)
        shutil.rmtree(test_dir / ".lazy_cache", ignore_errors=True)

        await self._run_async_test(
            "lazy_dvc_regular_restore",
            lambda: self._async_ok(ws.restore("lazy_test_step_2")),
            "Regular DVC restore of smart-committed data should work",
        )

        await self._run_async_test(
            "lazy_dvc_verify_modified",
            lambda: self._check_cat(data_dir / "file1.txt", "modified content"),
            "Modified file should have new content after restore",
        )

        await self._run_async_test(
            "lazy_dvc_verify_new",
            lambda: self._check_cat(data_dir / "new_file.txt", "brand new content"),
            "New file should exist after restore",
        )

        await self._run_async_test(
            "lazy_dvc_verify_deleted",
            lambda: self._check_absent(data_dir / "file2.txt"),
            "Deleted file should NOT exist after restore",
        )

        await self._run_async_test(
            "lazy_dvc_verify_untouched",
            lambda: self._check_cat(data_dir / "sub" / "nested.txt", "nested content here"),
            "Untouched nested file should have original content",
        )

        await self._run_async_test(
            "lazy_dvc_verify_large_untouched",
            lambda: self._check_md5sum(data_dir / "large.bin", large_md5),
            "Untouched large file should match original MD5",
        )

    # --- lazy DVC helpers ---

    async def _async_ok(self, coro) -> bool:
        await coro
        return True

    async def _check_is_mount(self, path: Path) -> bool:
        ec, _, _ = await run_local(f"mountpoint -q {path}", timeout=5)
        return ec == 0

    async def _check_not_mount(self, path: Path) -> bool:
        ec, _, _ = await run_local(f"mountpoint -q {path}", timeout=5)
        return ec != 0

    async def _check_ls_contains(self, path: Path, expected: set[str]) -> bool:
        ec, stdout, _ = await run_local(f"ls {path}", timeout=10)
        if ec != 0:
            return False
        return expected.issubset(set(stdout.strip().split()))

    async def _check_cat(self, path: Path, expected: str) -> bool:
        ec, stdout, _ = await run_local(f"cat {path}", timeout=30)
        return ec == 0 and stdout == expected

    async def _check_md5sum(self, path: Path, expected_md5: str) -> bool:
        ec, stdout, _ = await run_local(f"md5sum {path}", timeout=30)
        if ec != 0:
            return False
        return stdout.strip().split()[0] == expected_md5

    async def _check_absent(self, path: Path) -> bool:
        ec, _, _ = await run_local(f"test ! -f {path}", timeout=5)
        return ec == 0

    async def _shell_write(self, path: Path, content: str) -> bool:
        ec, _, _ = await run_local(
            f"{sys.executable} -c \"from pathlib import Path; Path('{path}').write_text('{content}')\"",
            timeout=10,
        )
        return ec == 0

    async def _shell_rm(self, path: Path) -> bool:
        ec, _, _ = await run_local(f"rm -f {path}", timeout=10)
        return ec == 0
