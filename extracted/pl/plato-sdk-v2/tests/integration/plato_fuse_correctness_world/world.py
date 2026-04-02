"""World-backed correctness test for the Rust plato-fuse binary.

Tests:
1. Lazy loading — files aren't fetched until first read
2. All filesystem operations work through FUSE (create, write, rename, etc.)
3. Metadata tracking — meta.json correctly reports created/modified/deleted
4. Cross-VM NFS sync — agent writes through NFS→FUSE, world VM sees changes
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import ClassVar

from plato.transports import NFSTransport, rsync_to
from plato.utils.subprocess import run_local, run_ssh
from plato.v2 import Env
from plato.v2.types import SimConfigCompute
from plato.worlds import BaseWorld, Observation, RunConfig, StepResult, register_world

SEED_FILE_COUNT = 20
UNKNOWN_SIZE_RELPATH = "store/unknown_size/file.txt"
UNKNOWN_SIZE_CONTENT = "unknown-size fixture\n"
MISSING_RELPATH = "store/missing_size/file.txt"


class FuseCorrectnessConfig(RunConfig):
    bundle_root: Path = Path("/tmp/plato-fuse-bundle")
    agent_bundle_root: Path = Path("/tmp/plato-fuse-agent-bundle")
    agent_mount_root: Path = Path("/mnt/plato-fuse-nfs")


@register_world("plato-world-fuse-correctness")
class FuseCorrectnessWorld(BaseWorld[FuseCorrectnessConfig]):
    name: ClassVar[str] = "fuse-correctness"
    description: ClassVar[str] = "Correctness tests for Rust plato-fuse + NFS"

    async def reset(self) -> Observation:
        assert self.plato_session is not None
        assert self._ssh_key_path is not None

        bundle_root = self.config.bundle_root
        results: dict[str, object] = {}
        try:
            # --- Test 1: Lazy loading through FUSE ---
            self.logger.info("=== Test 1: Lazy Loading ===")
            await self._reset_fuse_state(bundle_root)
            await self._start_fuse(bundle_root)
            try:
                results["lazy_load"] = await self._test_lazy_load(bundle_root)
            finally:
                await self._stop_fuse(bundle_root)

            # --- Test 2: File operations through FUSE ---
            self.logger.info("=== Test 2: File Operations ===")
            await self._reset_fuse_state(bundle_root)
            await self._start_fuse(bundle_root)
            try:
                results["file_ops"] = await self._test_file_operations(bundle_root)
            finally:
                await self._stop_fuse(bundle_root)

            # --- Test 3: Metadata tracking ---
            self.logger.info("=== Test 3: Metadata Tracking ===")
            await self._reset_fuse_state(bundle_root)
            await self._start_fuse(bundle_root)
            try:
                results["metadata"] = await self._test_metadata_tracking(bundle_root)
            finally:
                await self._stop_fuse(bundle_root)

            # --- Test 4: Cross-VM NFS over FUSE ---
            self.logger.info("=== Test 4: Cross-VM NFS Sync ===")
            results["cross_vm"] = await self._test_cross_vm_sync(bundle_root)

            self.logger.info("Results: %s", json.dumps(results, indent=2))
            for test_name, result in results.items():
                if isinstance(result, dict):
                    assert result.get("pass"), f"{test_name} failed: {result.get('errors', result)}"
        finally:
            (bundle_root / "test_results.json").write_text(json.dumps(results, indent=2))

        return Observation(data=results)

    async def step(self) -> StepResult:
        return StepResult(observation=Observation(data={"status": "passed"}), done=True)

    # ------------------------------------------------------------------
    # Test implementations
    # ------------------------------------------------------------------

    async def _test_lazy_load(self, bundle_root: Path) -> dict:
        """Files are stat-able and readable through FUSE mount."""
        mount = bundle_root / "mnt"
        seed_relpaths = [f"store/pkg_{i:03d}/file_{i:04d}.json" for i in range(SEED_FILE_COUNT)]
        expected_arg = ",".join(seed_relpaths)

        stdout = await self._run_local_ok(
            f"python3 {bundle_root}/workload.py --check lazy_load --expected-files '{expected_arg}' {mount}",
            timeout=60,
        )
        result = json.loads(stdout.strip().splitlines()[-1])

        stat_size = await self._run_local_ok(
            f"python3 -c \"from pathlib import Path; print(Path('{mount}/{UNKNOWN_SIZE_RELPATH}').stat().st_size)\"",
            timeout=10,
        )
        if stat_size.strip() != str(len(UNKNOWN_SIZE_CONTENT)):
            result.setdefault("errors", []).append(f"unknown-size stat mismatch: {stat_size!r}")
            result["pass"] = False

        cat_output = await self._run_local_ok(
            f"timeout 5 cat {mount}/{UNKNOWN_SIZE_RELPATH}",
            timeout=10,
        )
        if cat_output != UNKNOWN_SIZE_CONTENT:
            result.setdefault("errors", []).append(f"unknown-size cat mismatch: {cat_output!r}")
            result["pass"] = False

        missing_stat_size = await self._run_local_ok(
            f"python3 -c \"from pathlib import Path; print(Path('{mount}/{MISSING_RELPATH}').stat().st_size)\"",
            timeout=10,
        )
        if missing_stat_size.strip() != "0":
            result.setdefault("errors", []).append(f"missing-object stat mismatch: {missing_stat_size!r}")
            result["pass"] = False

        exit_code, stdout, stderr = await run_local(
            f"timeout 5 cat {mount}/{MISSING_RELPATH}",
            timeout=10,
        )
        if exit_code == 124:
            result.setdefault("errors", []).append("missing-object cat timed out locally")
            result["pass"] = False
        elif stdout:
            result.setdefault("errors", []).append(f"missing-object cat unexpectedly produced output: {stdout!r}")
            result["pass"] = False

        return result

    async def _test_file_operations(self, bundle_root: Path) -> dict:
        """All filesystem ops work through FUSE."""
        mount = bundle_root / "mnt"
        stdout = await self._run_local_ok(
            f"python3 {bundle_root}/workload.py --check file_ops {mount}",
            timeout=120,
        )
        return json.loads(stdout.strip().splitlines()[-1])

    async def _test_metadata_tracking(self, bundle_root: Path) -> dict:
        """After ops, meta.json reports created/modified/deleted correctly."""
        mount = bundle_root / "mnt"
        errors: list[str] = []

        # Create a file
        await self._run_local_ok(
            f"python3 -c \"from pathlib import Path; Path('{mount}/meta_test_created.txt').write_text('new file')\"",
            timeout=10,
        )

        # Modify a seed file
        first_seed = "store/pkg_000/file_0000.json"
        await self._run_local_ok(
            f'python3 -c "'
            f"from pathlib import Path; "
            f"p = Path('{mount}/{first_seed}'); "
            f"p.write_text(p.read_text() + '\\nmodified')\"",
            timeout=10,
        )

        # Delete a seed file
        second_seed = "store/pkg_001/file_0001.json"
        await self._run_local_ok(f"rm {mount}/{second_seed}", timeout=10)

        await self._stop_fuse(bundle_root)

        meta = await self._read_meta(bundle_root)
        created = set(meta.get("created", []))
        modified = set(meta.get("modified", []))
        deleted = set(meta.get("deleted", []))

        if "meta_test_created.txt" not in created:
            errors.append(f"created file not in meta.created: {created}")
        if first_seed not in modified:
            errors.append(f"modified file not in meta.modified: {modified}")
        if second_seed not in deleted:
            errors.append(f"deleted file not in meta.deleted: {deleted}")

        return {"pass": len(errors) == 0, "errors": errors, "meta": meta}

    async def _test_cross_vm_sync(self, bundle_root: Path) -> dict:
        """Agent writes through NFS→FUSE, world VM sees the change."""
        agent_env = None
        agent_ip = None
        errors: list[str] = []
        agent_bundle_root = self.config.agent_bundle_root
        agent_mount_root = self.config.agent_mount_root
        try:
            # Spin up agent VM
            agent_env = await self.plato_session.add_env(
                Env.resource(
                    simulator="fuse-correctness-agent",
                    sim_config=SimConfigCompute(cpus=2, memory=4096, disk=20480),
                    alias="fuse-correctness-agent",
                ),
                timeout=300,
            )
            pub_key = Path(str(self._ssh_key_path) + ".pub").read_text().strip()
            await self.plato_session.add_ssh_key(pub_key)
            agent_ip = await agent_env.get_mesh_ip()
            if not agent_ip:
                raise RuntimeError("Agent VM has no mesh IP")

            world_env = self.get_env("runtime")
            if world_env is None:
                raise RuntimeError("Runtime env missing")
            world_ip = await world_env.get_mesh_ip()
            if not world_ip:
                raise RuntimeError("World VM has no mesh IP")

            self.logger.info("Agent ready: ip=%s, world_ip=%s", agent_ip, world_ip)

            # Install NFS on agent
            await run_ssh(
                self._ssh_key_path,
                agent_ip,
                "which mount.nfs > /dev/null 2>&1 || (apt-get update -qq && apt-get install -y -qq nfs-common)",
                timeout=120,
            )

            # Copy workload script to agent
            await rsync_to(
                self._ssh_key_path,
                bundle_root,
                str(agent_bundle_root),
                agent_ip,
            )

            # Start FUSE and export via NFS
            await self._reset_fuse_state(bundle_root)
            await self._start_fuse(bundle_root)

            fuse_mount = bundle_root / "mnt"
            transport = NFSTransport(
                str(fuse_mount),
                world_ip,
                self._ssh_key_path,
                str(agent_mount_root),
            )
            await transport.initialize()
            await transport.setup_agent(agent_env, agent_ip)

            # Test 4a: Agent can read seed files through NFS→FUSE
            seed_relpaths = [f"store/pkg_{i:03d}/file_{i:04d}.json" for i in range(SEED_FILE_COUNT)]
            expected_arg = ",".join(seed_relpaths)
            exit_code, stdout, stderr = await run_ssh(
                self._ssh_key_path,
                agent_ip,
                f"python3 {agent_bundle_root}/workload.py --check lazy_load "
                f"--expected-files '{expected_arg}' {agent_mount_root}",
                timeout=60,
            )
            if exit_code != 0:
                errors.append(f"agent lazy_load failed: {stderr}")
            else:
                agent_lazy = json.loads(stdout.strip().splitlines()[-1])
                if not agent_lazy.get("pass"):
                    errors.append(f"agent lazy_load: {agent_lazy.get('errors')}")

            exit_code, stdout, stderr = await run_ssh(
                self._ssh_key_path,
                agent_ip,
                'python3 -c "'
                "from pathlib import Path; "
                f"print(Path('{agent_mount_root}/{UNKNOWN_SIZE_RELPATH}').stat().st_size)\"",
                timeout=10,
            )
            if exit_code != 0:
                errors.append(f"agent unknown-size stat failed: {stderr}")
            elif stdout.strip() != str(len(UNKNOWN_SIZE_CONTENT)):
                errors.append(f"agent unknown-size stat mismatch: {stdout!r}")

            exit_code, stdout, stderr = await run_ssh(
                self._ssh_key_path,
                agent_ip,
                f"timeout 5 cat {agent_mount_root}/{UNKNOWN_SIZE_RELPATH}",
                timeout=10,
            )
            if exit_code != 0:
                errors.append(f"agent unknown-size cat failed: {stderr}")
            elif stdout != UNKNOWN_SIZE_CONTENT:
                errors.append(f"agent unknown-size cat mismatch: {stdout!r}")

            exit_code, stdout, stderr = await run_ssh(
                self._ssh_key_path,
                agent_ip,
                'python3 -c "'
                "from pathlib import Path; "
                f"print(Path('{agent_mount_root}/{MISSING_RELPATH}').stat().st_size)\"",
                timeout=10,
            )
            if exit_code != 0:
                errors.append(f"agent missing-object stat failed: {stderr}")
            elif stdout.strip() != "0":
                errors.append(f"agent missing-object stat mismatch: {stdout!r}")

            exit_code, stdout, stderr = await run_ssh(
                self._ssh_key_path,
                agent_ip,
                f"timeout 5 cat {agent_mount_root}/{MISSING_RELPATH}",
                timeout=10,
            )
            if exit_code == 124:
                errors.append("agent missing-object cat timed out")
            elif stdout:
                errors.append(f"agent missing-object cat unexpectedly produced output: {stdout!r}")

            # Test 4b: Agent can do file ops through NFS→FUSE
            exit_code, stdout, stderr = await run_ssh(
                self._ssh_key_path,
                agent_ip,
                f"python3 {agent_bundle_root}/workload.py --check file_ops {agent_mount_root}",
                timeout=120,
            )
            if exit_code != 0:
                errors.append(f"agent file_ops failed: {stderr}")
            else:
                agent_ops = json.loads(stdout.strip().splitlines()[-1])
                if not agent_ops.get("pass"):
                    errors.append(f"agent file_ops: {agent_ops.get('errors')}")
                else:
                    expected_world_content = await self._run_local_ok(
                        f"cat {fuse_mount}/ops/renamed.txt",
                        timeout=10,
                    )
                    if expected_world_content.strip() != "trun":
                        errors.append(f"world VM did not observe agent file_ops result: {expected_world_content!r}")
                    exit_code2, _, _ = await run_local(
                        f"test ! -e {fuse_mount}/ops/hardlinked.txt",
                        timeout=10,
                    )
                    if exit_code2 != 0:
                        errors.append("world VM still sees removed hardlink after agent unlink")
                    world_pg_mode = await self._run_local_ok(
                        f"stat -c '%a' {fuse_mount}/.runtime/postgres/data",
                        timeout=10,
                    )
                    if world_pg_mode.strip() != "750":
                        errors.append(f"world VM sees wrong postgres dir mode after agent chmod: {world_pg_mode!r}")

            # Test 4c: Agent writes sentinel, world VM sees it
            exit_code, stdout, stderr = await run_ssh(
                self._ssh_key_path,
                agent_ip,
                f"python3 {agent_bundle_root}/workload.py --check cross_vm {agent_mount_root}",
                timeout=30,
            )
            if exit_code != 0:
                errors.append(f"agent cross_vm write failed: {stderr}")
            else:
                # Verify world VM can see the sentinel through FUSE mount
                sentinel = fuse_mount / "cross_vm_sentinel.txt"
                exit_code2, content, _ = await run_local(f"cat {sentinel}", timeout=10)
                if exit_code2 != 0 or content.strip() != "written-by-agent":
                    errors.append(f"world VM cannot see agent sentinel: exit={exit_code2} content={content!r}")

            # Test 4d: World writes, agent reads
            await self._run_local_ok(
                f'python3 -c "'
                f"from pathlib import Path; "
                f"Path('{fuse_mount}/world_sentinel.txt').write_text('written-by-world')\"",
                timeout=10,
            )
            exit_code, stdout, stderr = await run_ssh(
                self._ssh_key_path,
                agent_ip,
                f"cat {agent_mount_root}/world_sentinel.txt",
                timeout=10,
            )
            if exit_code != 0 or stdout.strip() != "written-by-world":
                errors.append(f"agent cannot see world sentinel: exit={exit_code} content={stdout!r}")

        finally:
            # Cleanup
            if agent_env is not None and agent_ip:
                try:
                    await run_ssh(
                        self._ssh_key_path,
                        agent_ip,
                        f"mountpoint -q {agent_mount_root} && umount {agent_mount_root} || true",
                        timeout=30,
                    )
                except Exception:
                    pass
            await self._stop_fuse(bundle_root)
            if agent_env is not None:
                await self.plato_session.remove_env(agent_env)

        return {"pass": len(errors) == 0, "errors": errors}

    # ------------------------------------------------------------------
    # FUSE lifecycle helpers
    # ------------------------------------------------------------------

    async def _reset_fuse_state(self, bundle_root: Path) -> None:
        await self._run_local_ok(
            f"mountpoint -q {bundle_root}/mnt && fusermount3 -u {bundle_root}/mnt || true; "
            f"rm -rf {bundle_root}/cache-root/overlay {bundle_root}/cache-root/meta.json {bundle_root}/mnt && "
            f"mkdir -p {bundle_root}/cache-root/overlay {bundle_root}/mnt",
            timeout=60,
        )

    async def _start_fuse(self, bundle_root: Path) -> None:
        self.logger.info("Starting plato-fuse at %s", bundle_root)
        # Launch in a new session so it survives parent shell exit
        await self._run_local_ok(
            "python3 - <<'PY'\n"
            "import pathlib\n"
            "import subprocess\n"
            f"root = pathlib.Path('{bundle_root}')\n"
            "stdout = (root / 'plato-fuse.stdout').open('w')\n"
            "stderr = (root / 'plato-fuse.stderr').open('w')\n"
            "proc = subprocess.Popen(\n"
            "    [str(root / 'plato-fuse'), str(root / 'config.json')],\n"
            "    cwd=root,\n"
            "    stdin=subprocess.DEVNULL,\n"
            "    stdout=stdout,\n"
            "    stderr=stderr,\n"
            "    start_new_session=True,\n"
            ")\n"
            "(root / 'plato-fuse.pid').write_text(str(proc.pid))\n"
            "print(proc.pid)\n"
            "PY",
            timeout=30,
        )
        # Wait for mount
        await self._run_local_ok(
            "python3 - <<'PY'\n"
            "import os\n"
            "import pathlib\n"
            "import subprocess\n"
            "import time\n"
            f"mountpoint = pathlib.Path('{bundle_root}/mnt')\n"
            f"pid_path = pathlib.Path('{bundle_root}/plato-fuse.pid')\n"
            f"stderr_path = pathlib.Path('{bundle_root}/plato-fuse.stderr')\n"
            "deadline = time.time() + 30\n"
            "while time.time() < deadline:\n"
            "    if subprocess.run(['mountpoint', '-q', str(mountpoint)]).returncode == 0:\n"
            "        raise SystemExit(0)\n"
            "    if pid_path.exists():\n"
            "        pid = int(pid_path.read_text().strip())\n"
            "        try:\n"
            "            os.kill(pid, 0)\n"
            "        except OSError:\n"
            "            raise RuntimeError(stderr_path.read_text())\n"
            "    time.sleep(0.2)\n"
            "raise RuntimeError('timed out waiting for fuse mount')\n"
            "PY",
            timeout=40,
        )

    async def _stop_fuse(self, bundle_root: Path) -> None:
        await self._run_local_ok(
            f"mountpoint -q {bundle_root}/mnt && fusermount3 -u {bundle_root}/mnt || true; "
            f"if [ -f {bundle_root}/plato-fuse.pid ]; then "
            f"pid=$(cat {bundle_root}/plato-fuse.pid); "
            f'for _ in $(seq 1 100); do kill -0 "$pid" 2>/dev/null || break; sleep 0.1; done; '
            f'kill "$pid" 2>/dev/null || true; '
            f"fi",
            timeout=30,
        )

    async def _read_meta(self, bundle_root: Path) -> dict:
        stdout = await self._run_local_ok(
            f"test -f {bundle_root}/cache-root/meta.json && cat {bundle_root}/cache-root/meta.json || echo '{{}}'",
            timeout=10,
        )
        return json.loads(stdout)

    async def _run_local_ok(self, cmd: str, timeout: int = 120) -> str:
        exit_code, stdout, stderr = await run_local(cmd, timeout=timeout)
        if exit_code != 0:
            raise RuntimeError(f"Command failed (exit {exit_code}): {cmd}\nstderr: {stderr}\nstdout: {stdout}")
        return stdout

    async def _run_ssh_ok(self, hostname: str, cmd: str, timeout: int = 120) -> str:
        exit_code, stdout, stderr = await run_ssh(self._ssh_key_path, hostname, cmd, timeout=timeout)
        if exit_code != 0:
            raise RuntimeError(f"SSH command failed (exit {exit_code}): {cmd}\nstderr: {stderr}\nstdout: {stdout}")
        return stdout
