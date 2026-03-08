"""World-backed integration perf test for the Rust plato-fuse binary."""

from __future__ import annotations

import json
from pathlib import Path
from typing import ClassVar

from plato.agents.runtime.transport import rsync_to
from plato.utils.subprocess import run_local, run_ssh
from plato.v2 import Env
from plato.v2.types import SimConfigCompute
from plato.worlds import BaseWorld, Observation, RunConfig, StepResult, register_world

CREATE_FILE_COUNT = 1200
MODIFY_FILE_COUNT = 200
DELETE_FILE_COUNT = 100
RM_RF_FILE_COUNT = 900
TOTAL_CREATED = CREATE_FILE_COUNT + RM_RF_FILE_COUNT
TOTAL_DELETED = DELETE_FILE_COUNT + RM_RF_FILE_COUNT
SEED_FILE_COUNT = 1800
NFS_MOUNT_OPTS = "vers=3,soft,timeo=30,nolock"


class PlatoFusePerfWorldConfig(RunConfig):
    bundle_root: Path = Path("/tmp/plato-fuse-bundle")
    agent_bundle_root: Path = Path("/tmp/plato-fuse-agent-bundle")
    agent_mount_root: Path = Path("/mnt/plato-fuse-nfs")
    agent_raw_mount_root: Path = Path("/mnt/plato-raw-nfs")


@register_world("plato-world-plato-fuse-perf-test")
class PlatoFusePerfWorld(BaseWorld[PlatoFusePerfWorldConfig]):
    name: ClassVar[str] = "plato-fuse-perf-test"
    description: ClassVar[str] = "Perf comparison world for plain vs FUSE vs NFS-over-FUSE"

    async def reset(self) -> Observation:
        assert self.plato_session is not None, "Plato session required"
        assert self._ssh_key_path is not None, "SSH key path required"

        bundle_root = self.config.bundle_root
        agent_bundle_root = self.config.agent_bundle_root
        agent_mount_root = self.config.agent_mount_root
        agent_raw_mount_root = self.config.agent_raw_mount_root

        self.logger.info("=== Plato FUSE Perf Comparison ===")
        self.logger.info("Bundle root: %s", bundle_root)

        world_plain = await self._run_world_plain_baseline(bundle_root)
        world_fuse, world_meta = await self._run_world_fuse(bundle_root)
        agent_raw_nfs, agent_nfs_fuse, agent_meta = await self._run_cross_vm(
            bundle_root, agent_bundle_root, agent_raw_mount_root, agent_mount_root
        )

        metrics = {
            "world_plain_baseline": world_plain,
            "world_fuse": world_fuse,
            "agent_raw_nfs": agent_raw_nfs,
            "agent_nfs_fuse": agent_nfs_fuse,
            "ratios_vs_plain": {
                "world_fuse_cold_read": round(world_fuse["cold_read_seed_s"] / world_plain["cold_read_seed_s"], 3),
                "agent_raw_nfs_cold_read": round(
                    agent_raw_nfs["cold_read_seed_s"] / world_plain["cold_read_seed_s"], 3
                ),
                "agent_nfs_fuse_cold_read": round(
                    agent_nfs_fuse["cold_read_seed_s"] / world_plain["cold_read_seed_s"], 3
                ),
                "world_fuse_parallel": round(
                    world_fuse["parallel_stat_read_s"] / world_plain["parallel_stat_read_s"], 3
                ),
                "agent_raw_nfs_parallel": round(
                    agent_raw_nfs["parallel_stat_read_s"] / world_plain["parallel_stat_read_s"], 3
                ),
                "agent_nfs_fuse_parallel": round(
                    agent_nfs_fuse["parallel_stat_read_s"] / world_plain["parallel_stat_read_s"], 3
                ),
                "world_fuse_rm_rf": round(world_fuse["rm_rf_tree_delete_s"] / world_plain["rm_rf_tree_delete_s"], 3),
                "agent_raw_nfs_rm_rf": round(
                    agent_raw_nfs["rm_rf_tree_delete_s"] / world_plain["rm_rf_tree_delete_s"], 3
                ),
                "agent_nfs_fuse_rm_rf": round(
                    agent_nfs_fuse["rm_rf_tree_delete_s"] / world_plain["rm_rf_tree_delete_s"], 3
                ),
            },
            "world_fuse_meta": world_meta,
            "agent_nfs_fuse_meta": agent_meta,
        }

        (bundle_root / "perf_metrics.json").write_text(json.dumps(metrics, sort_keys=True, indent=2))
        self.logger.info("Plato FUSE metric summary: %s", json.dumps(metrics, sort_keys=True))
        self._assert_metrics(world_plain, world_fuse, agent_raw_nfs, agent_nfs_fuse, world_meta, agent_meta)
        return Observation(data=metrics)

    async def step(self) -> StepResult:
        return StepResult(observation=Observation(data={"status": "passed"}), done=True)

    def _assert_metrics(
        self,
        world_plain: dict,
        world_fuse: dict,
        agent_raw_nfs: dict,
        agent_nfs_fuse: dict,
        world_meta: dict,
        agent_meta: dict,
    ) -> None:
        assert world_plain["seed_files"] == SEED_FILE_COUNT
        assert world_fuse["seed_files"] == SEED_FILE_COUNT
        assert agent_raw_nfs["seed_files"] == SEED_FILE_COUNT
        assert agent_nfs_fuse["seed_files"] == SEED_FILE_COUNT
        assert len(world_meta.get("created", [])) == TOTAL_CREATED
        assert len(world_meta.get("modified", [])) == MODIFY_FILE_COUNT
        assert len(world_meta.get("deleted", [])) == TOTAL_DELETED
        self.logger.info(
            "Cross-VM FUSE metadata counts: created=%d modified=%d deleted=%d",
            len(agent_meta.get("created", [])),
            len(agent_meta.get("modified", [])),
            len(agent_meta.get("deleted", [])),
        )
        assert agent_nfs_fuse["create_small_files_s"] > 0
        assert agent_nfs_fuse["modify_existing_s"] > 0
        assert agent_nfs_fuse["delete_existing_s"] > 0

    async def _run_world_plain_baseline(self, bundle_root: Path) -> dict:
        self.logger.info("=== World Plain Baseline ===")
        await self._run_local_ok(
            f"rm -rf {bundle_root}/plain-root && "
            f"mkdir -p {bundle_root}/plain-root && "
            f"cp -a {bundle_root}/cache-root/cache/store {bundle_root}/plain-root/store",
            timeout=60,
        )
        return await self._run_local_workload(bundle_root, bundle_root / "plain-root", "world_plain_baseline")

    async def _run_world_fuse(self, bundle_root: Path) -> tuple[dict, dict]:
        self.logger.info("=== World Local FUSE ===")
        await self._reset_fuse_state(bundle_root)
        await self._start_fuse(bundle_root)
        try:
            metrics = await self._run_local_workload(bundle_root, bundle_root / "mnt", "world_fuse")
        finally:
            await self._stop_fuse(bundle_root)
        meta = await self._read_meta(bundle_root)
        return metrics, meta

    async def _run_cross_vm(
        self,
        bundle_root: Path,
        agent_bundle_root: Path,
        agent_raw_mount_root: Path,
        agent_mount_root: Path,
    ) -> tuple[dict, dict, dict]:
        self.logger.info("=== Cross-VM Raw NFS + NFS over FUSE ===")
        raw_export_root = bundle_root / "raw-export-root"

        agent_env = None
        agent_hostname: str | None = None
        raw_metrics: dict | None = None
        fuse_metrics: dict | None = None
        try:
            agent_env = await self.plato_session.add_env(
                Env.resource(
                    simulator="plato-fuse-perf-agent",
                    sim_config=SimConfigCompute(cpus=2, memory=4096, disk=20480),
                    alias="plato-fuse-perf-agent",
                ),
                timeout=300,
            )
            pub_key = Path(str(self._ssh_key_path) + ".pub").read_text().strip()
            await self.plato_session.add_ssh_key(pub_key)
            agent_hostname = await agent_env.get_mesh_ip()
            if not agent_hostname:
                raise RuntimeError("Agent VM has no mesh IP")
            world_env = self.get_env("runtime")
            if world_env is None:
                raise RuntimeError("Runtime env missing")
            world_ip = await world_env.get_mesh_ip()
            if not world_ip:
                raise RuntimeError("World VM has no mesh IP")

            self.logger.info("Agent ready: job=%s ip=%s world_ip=%s", agent_env.job_id, agent_hostname, world_ip)

            await run_ssh(
                self._ssh_key_path,
                agent_hostname,
                "which rsync > /dev/null 2>&1 || (apt-get update -qq && apt-get install -y -qq rsync); "
                "which mount.nfs > /dev/null 2>&1 || (apt-get update -qq && apt-get install -y -qq nfs-common)",
                timeout=120,
            )
            await rsync_to(self._ssh_key_path, bundle_root, str(agent_bundle_root), agent_hostname)

            await self._prepare_exportable_raw_root(bundle_root, raw_export_root)
            await self._export_nfs(raw_export_root)
            await run_ssh(
                self._ssh_key_path,
                agent_hostname,
                f"mkdir -p {agent_raw_mount_root} && "
                f"mount -t nfs -o {NFS_MOUNT_OPTS} {world_ip}:{raw_export_root} {agent_raw_mount_root}",
                timeout=60,
            )
            stdout = await self._run_ssh_ok(
                agent_hostname,
                f"python3 {agent_bundle_root}/run_smallfile_workload.py --label agent_raw_nfs {agent_raw_mount_root}",
                timeout=600,
            )
            raw_metrics = json.loads(stdout.strip().splitlines()[-1])
            await run_ssh(
                self._ssh_key_path,
                agent_hostname,
                f"mountpoint -q {agent_raw_mount_root} && umount {agent_raw_mount_root} || true",
                timeout=30,
            )

            await self._reset_fuse_state(bundle_root)
            await self._start_fuse(bundle_root)
            try:
                await self._export_nfs(bundle_root / "mnt")
                await run_ssh(
                    self._ssh_key_path,
                    agent_hostname,
                    f"mkdir -p {agent_mount_root} && "
                    f"mount -t nfs -o {NFS_MOUNT_OPTS} {world_ip}:{bundle_root}/mnt {agent_mount_root}",
                    timeout=60,
                )

                stdout = await self._run_ssh_ok(
                    agent_hostname,
                    f"python3 {agent_bundle_root}/run_smallfile_workload.py --label agent_nfs_fuse {agent_mount_root}",
                    timeout=600,
                )
                fuse_metrics = json.loads(stdout.strip().splitlines()[-1])
            finally:
                try:
                    await run_ssh(
                        self._ssh_key_path,
                        agent_hostname,
                        f"mountpoint -q {agent_mount_root} && umount {agent_mount_root} || true",
                        timeout=30,
                    )
                except Exception:
                    pass
                await self._stop_fuse(bundle_root)
        finally:
            if agent_env is not None and agent_hostname is not None:
                try:
                    await run_ssh(
                        self._ssh_key_path,
                        agent_hostname,
                        f"mountpoint -q {agent_mount_root} && umount {agent_mount_root} || true",
                        timeout=30,
                    )
                except Exception:
                    pass
            if agent_env is not None:
                await self.plato_session.remove_env(agent_env)
            await self._cleanup_exportable_raw_root(bundle_root, raw_export_root)

        meta = await self._read_meta(bundle_root)
        if raw_metrics is None or fuse_metrics is None:
            raise RuntimeError("Cross-VM metrics were not fully collected")
        return raw_metrics, fuse_metrics, meta

    async def _run_local_workload(self, bundle_root: Path, root: Path, label: str) -> dict:
        self.logger.info("Running workload label=%s root=%s", label, root)
        stdout = await self._run_local_ok(
            f"python3 {bundle_root}/run_smallfile_workload.py --label {label} {root}",
            timeout=600,
        )
        metrics = json.loads(stdout.strip().splitlines()[-1])
        self.logger.info("Workload metrics (%s): %s", label, json.dumps(metrics, sort_keys=True))
        return metrics

    async def _prepare_plain_root(self, bundle_root: Path) -> None:
        await self._run_local_ok(
            f"rm -rf {bundle_root}/plain-root && "
            f"mkdir -p {bundle_root}/plain-root && "
            f"cp -a {bundle_root}/cache-root/cache/store {bundle_root}/plain-root/store",
            timeout=60,
        )

    async def _prepare_exportable_raw_root(self, bundle_root: Path, raw_export_root: Path) -> None:
        img_path = bundle_root / "raw-export.img"
        await self._cleanup_exportable_raw_root(bundle_root, raw_export_root)
        await self._run_local_ok(
            f"truncate -s 512M {img_path} && "
            f"mkfs.ext4 -q -F {img_path} && "
            f"mkdir -p {raw_export_root} && "
            f"mount -o loop {img_path} {raw_export_root} && "
            f"cp -a {bundle_root}/cache-root/cache/store {raw_export_root}/store && "
            f"chown -R 1000:1000 {raw_export_root} && "
            f"chmod -R u+rwX,g+rwX,o+rX {raw_export_root}",
            timeout=180,
        )

    async def _cleanup_exportable_raw_root(self, bundle_root: Path, raw_export_root: Path) -> None:
        img_path = bundle_root / "raw-export.img"
        await self._run_local_ok(
            f"exportfs -u '*:{raw_export_root}' 2>/dev/null || true; "
            f"mountpoint -q {raw_export_root} && umount -l {raw_export_root} || true; "
            f"rm -rf {raw_export_root} {img_path}",
            timeout=60,
        )

    async def _export_nfs(self, path: Path) -> None:
        await self._run_local_ok(
            "which exportfs > /dev/null 2>&1 || (apt-get update -qq && apt-get install -y -qq nfs-kernel-server)",
            timeout=120,
        )
        await self._run_local_ok(
            f"printf '%s\\n' '{path} "
            "*(rw,sync,fsid=0,crossmnt,no_subtree_check,all_squash,anonuid=1000,anongid=1000)' "
            "> /etc/exports && "
            "modprobe nfsd 2>/dev/null; "
            "mkdir -p /proc/fs/nfsd && "
            "mountpoint -q /proc/fs/nfsd || mount -t nfsd nfsd /proc/fs/nfsd && "
            "systemctl start rpcbind && "
            "systemctl reset-failed proc-fs-nfsd.mount 2>/dev/null && "
            "exportfs -ra && "
            "systemctl start nfs-kernel-server",
            timeout=120,
        )

    async def _reset_fuse_state(self, bundle_root: Path) -> None:
        await self._run_local_ok(
            f"mountpoint -q {bundle_root}/mnt && fusermount3 -u {bundle_root}/mnt || true; "
            f"rm -rf {bundle_root}/cache-root/overlay {bundle_root}/cache-root/meta.json {bundle_root}/mnt && "
            f"mkdir -p {bundle_root}/cache-root/overlay {bundle_root}/mnt",
            timeout=60,
        )

    async def _start_fuse(self, bundle_root: Path) -> None:
        self.logger.info("Starting rust plato-fuse at %s", bundle_root)
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
            timeout=30,
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
