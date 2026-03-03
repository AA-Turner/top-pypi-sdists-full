"""VM integration test — runs the workspace test world on a real Plato VM.

Spins up a VM, syncs the SDK + test world package, then invokes
``plato-world-runner run --world plato-world-structured-execution``
inside the VM.  All actual test logic (NFS, rsync, permissions, lazy DVC)
lives in ``workspace_test_world/world.py``.

Requires: PLATO_API_KEY
"""

from __future__ import annotations

import asyncio
import base64
import json
import logging
import os
import subprocess
from pathlib import Path

import pytest

logger = logging.getLogger(__name__)

pytestmark = pytest.mark.skipif(
    not os.environ.get("PLATO_API_KEY"),
    reason="PLATO_API_KEY not set",
)

WORLD_IMAGE = "383806609161.dkr.ecr.us-west-1.amazonaws.com/vm/rootfs/plato-worlds/webclone:0.2.14"
SDK_ROOT = Path(__file__).resolve().parent.parent.parent  # python-sdk/
TEST_WORLD_DIR = Path(__file__).resolve().parent / "workspace_test_world"
CHRONOS_URL = "https://chronos.plato.so"


def _run_async(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


class _VM:
    """Manages a Plato VM session for testing."""

    def __init__(self):
        self.plato = None
        self.session = None
        self.env = None
        self.chronos_session_id = None

    async def start(self):
        import httpx

        from plato.chronos.api.sessions import create_session
        from plato.chronos.models import CreateSessionRequest
        from plato.cli.chronos.dev.ssh import SSHKeyPair
        from plato.v2 import AsyncPlato, Env
        from plato.v2.types import SimConfigCompute

        self.plato = AsyncPlato()
        self.session = await self.plato.sessions.create(
            envs=[
                Env.resource(
                    simulator="workspace-vm-test",
                    sim_config=SimConfigCompute(cpus=2, memory=4096, disk=20480),
                    alias="runtime",
                    docker_image_url=WORLD_IMAGE,
                    upload_rootfs=False,
                    rootfs_storage_backend="snapshot-store",
                )
            ],
            timeout=3600,
            connect_network=True,
        )
        self.env = self.session.envs[0]

        # Create Chronos session (like `plato chronos dev` does)
        async with httpx.AsyncClient(
            base_url=CHRONOS_URL,
            timeout=30.0,
        ) as client:
            resp = await create_session.asyncio(
                client,
                body=CreateSessionRequest(
                    world_name="plato-world-workspace-test",
                    world_config={},
                ),
                x_api_key=os.environ["PLATO_API_KEY"],
            )
        self.chronos_session_id = resp.public_id

        # Setup SSH key and copy to VM (like dev runner does)
        self._ssh_key = SSHKeyPair.generate()
        await self.session.add_ssh_key(self._ssh_key.public_key)
        private_key = self._ssh_key.private_key_path.read_text()
        public_key = self._ssh_key.public_key
        escaped_private = private_key.replace("'", "'\\''")
        escaped_public = public_key.replace("'", "'\\''")
        await self.env.execute(
            f"mkdir -p /root/.ssh && "
            f"echo '{escaped_private}' > /root/.ssh/agent_key && chmod 600 /root/.ssh/agent_key && "
            f"echo '{escaped_public}' > /root/.ssh/agent_key.pub && chmod 644 /root/.ssh/agent_key.pub",
            timeout=30,
        )

    async def exec(self, cmd: str, timeout: int = 120) -> tuple[int, str, str]:
        result = await self.env.execute(cmd, timeout=timeout)
        return result.exit_code, result.stdout or "", result.stderr or ""

    async def exec_ok(self, cmd: str, timeout: int = 120) -> str:
        code, out, err = await self.exec(cmd, timeout=timeout)
        assert code == 0, f"Command failed (exit {code}):\ncmd: {cmd}\nstderr: {err}\nstdout: {out}"
        return out

    def rsync_to(self, local_path: str, remote_path: str) -> None:
        from plato.cli.chronos.dev.ssh import SSHKeyPair, build_ssh_command_string

        if not hasattr(self, "_ssh_key"):
            self._ssh_key = SSHKeyPair.generate()
            _run_async(self.session.add_ssh_key(self._ssh_key.public_key))

        ssh_str = build_ssh_command_string(self.env.job_id, self._ssh_key.private_key_path)
        host = f"root@{self.env.job_id}.plato"
        cmd = [
            "rsync",
            "-az",
            "--delete",
            "--exclude",
            "__pycache__",
            "--exclude",
            ".git",
            "--exclude",
            "*.pyc",
            "--exclude",
            ".venv",
            "--exclude",
            "node_modules",
            "--exclude",
            "dist",
            "-e",
            ssh_str,
            f"{local_path}/",
            f"{host}:{remote_path}/",
        ]
        proc = subprocess.run(cmd, capture_output=True, timeout=120)
        assert proc.returncode == 0, f"rsync failed: {proc.stderr.decode()}"

    async def close(self):
        if self.session:
            await self.session.close()
        if self.plato:
            await self.plato.close()


@pytest.fixture(scope="module")
def vm():
    """Spin up a VM, sync SDK + test world, install them."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    v = _VM()
    try:
        loop.run_until_complete(v.start())
        logger.info(f"VM ready: {v.env.job_id}")

        # Sync and install SDK + test world
        v.rsync_to(str(SDK_ROOT), "/sdk")
        v.rsync_to(str(TEST_WORLD_DIR), "/test-world")
        loop.run_until_complete(
            v.exec_ok(
                "which rsync || (apt-get update && apt-get install -y rsync)",
                timeout=60,
            )
        )
        loop.run_until_complete(
            v.exec_ok(
                "uv pip install --system -e /sdk -e /test-world 2>&1",
                timeout=300,
            )
        )

        # DVC is needed for lazy DVC tests (workspace.init() calls `dvc init`)
        code, _, _ = loop.run_until_complete(v.exec("which dvc"))
        if code != 0:
            loop.run_until_complete(
                v.exec_ok(
                    "uv pip install --system 'dvc[s3]' 2>&1",
                    timeout=120,
                )
            )

        yield v
    finally:
        loop.run_until_complete(v.close())
        loop.close()


class TestWorkspaceVM:
    def test_workspace_world(self, vm: _VM):
        """Run the workspace test world — exercises NFS, rsync, perms, lazy DVC."""
        config = {
            "world": {
                "package": "plato-world-workspace-test:0.0.1",
                "runtime": {"type": "vm", "vm": {"cpus": 2, "memory": 4096, "disk": 20480}},
                "config": {},
            },
            "session": {
                "session_id": vm.chronos_session_id,
                "plato_session": vm.session.dump().model_dump(),
                "chronos_url": CHRONOS_URL,
            },
            "dev": {
                "ssh_key_path": "/root/.ssh/agent_key",
            },
        }

        # Write config via base64 to avoid shell escaping
        config_b64 = base64.b64encode(json.dumps(config).encode()).decode()
        _run_async(
            vm.exec_ok(
                f"echo '{config_b64}' | base64 -d > /tmp/config.json",
                timeout=10,
            )
        )

        code, stdout, stderr = _run_async(
            vm.exec(
                f"PLATO_API_KEY='{os.environ['PLATO_API_KEY']}' "
                f"plato-world-runner run "
                f"--world plato-world-structured-execution "
                f"--config /tmp/config.json -v",
                timeout=600,
            )
        )

        print(f"STDOUT:\n{stdout}")
        if stderr:
            print(f"STDERR:\n{stderr}")

        assert code == 0, f"Workspace test world failed (exit {code})"
