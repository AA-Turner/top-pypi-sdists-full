"""Integration test for webclone workspace setup on a real Plato VM.

Spins up a VM with the webclone image, syncs the local fuse binary, SDK, and
webclone world, then runs a test world that exercises:
- FUSE mount on workspace directory
- prepare_template_workspace (template copy + bun install on FUSE)
- workspace structure verification
- smart commit with node_modules present

Requires: PLATO_API_KEY
"""

from __future__ import annotations

import asyncio
import base64
import json
import logging
import os
from pathlib import Path

import pytest

from .conftest import CI_SESSION_BASE_TAG
from .test_workspace_vm import _VM, CHRONOS_URL, SDK_ROOT, _run_async

logger = logging.getLogger(__name__)

pytestmark = pytest.mark.skipif(
    not os.environ.get("PLATO_API_KEY"),
    reason="PLATO_API_KEY not set",
)

WEBCLONE_IMAGE = "383806609161.dkr.ecr.us-west-1.amazonaws.com/vm/rootfs/plato-worlds/webclone:0.2.14"
WEBCLONE_WORLD_DIR = Path(__file__).resolve().parents[2].parent / "worlds" / "webclone"
TEST_WORLD_DIR = Path(__file__).resolve().parent / "webclone_setup_test_world"
RESULTS_PATH = "/tmp/webclone-setup-test-results.json"


@pytest.fixture(scope="module")
def webclone_vm():
    """Spin up a VM with the webclone image, sync SDK + worlds.

    If PLATO_FUSE_BINARY is set, syncs that binary to the VM.
    Otherwise the SDK downloads from S3 at runtime (same as production).
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    v = _VM(
        world_name="plato-world-webclone-setup-test",
        tags=[CI_SESSION_BASE_TAG, "webclone-setup"],
        image=WEBCLONE_IMAGE,
    )
    try:
        loop.run_until_complete(v.start())
        logger.info("VM ready: %s", v.env.job_id)

        v.rsync_to(str(SDK_ROOT), "/sdk")
        v.rsync_to(str(WEBCLONE_WORLD_DIR), "/world")
        v.rsync_to(str(TEST_WORLD_DIR), "/test-world")

        fuse_binary = os.environ.get("PLATO_FUSE_BINARY")
        if fuse_binary and Path(fuse_binary).is_file():
            logger.info("Syncing PLATO_FUSE_BINARY: %s", fuse_binary)
            v.rsync_to(str(Path(fuse_binary).parent), "/tmp/plato-fuse-bin")

        # fuse3 userspace tools needed by plato-fuse
        loop.run_until_complete(
            v.exec_ok(
                "dpkg -s fuse3 > /dev/null 2>&1 || "
                "(apt-get update -qq && apt-get install -y -qq fuse3) > /dev/null 2>&1",
                timeout=60,
            )
        )
        loop.run_until_complete(
            v.exec_ok(
                "uv pip install --system -e '/sdk[worlds]' -e /world -e /test-world 2>&1",
                timeout=300,
            )
        )

        yield v
    finally:
        loop.run_until_complete(v.close())
        loop.close()


class TestWebcloneWorkspaceSetup:
    def test_workspace_setup_on_fuse(self, webclone_vm: _VM) -> None:
        """Run the webclone setup test world on a real VM with FUSE."""
        config = {
            "world": {
                "package": "plato-world-webclone-setup-test:0.0.1",
                "runtime": {
                    "type": "vm",
                    "vm": {"cpus": 2, "memory": 4096, "disk": 20480},
                },
                "config": {},
            },
            "session": {
                "session_id": webclone_vm.chronos_session_id,
                "plato_session": webclone_vm.session.dump().model_dump(),
                "chronos_url": CHRONOS_URL,
                "otel_url": webclone_vm.otel_url or "",
                "transport_mode": "nfs_kernel",
            },
            "dev": {
                "ssh_key_path": "/root/.ssh/agent_key",
            },
        }

        config_path = "/tmp/webclone-setup-test-config.json"
        config_b64 = base64.b64encode(json.dumps(config).encode()).decode()
        _run_async(
            webclone_vm.exec_ok(
                f"echo '{config_b64}' | base64 -d > {config_path}",
                timeout=10,
            )
        )

        log_file = "/tmp/webclone-setup-test-runner.log"
        code, stdout, stderr = _run_async(
            webclone_vm.exec(
                f"PLATO_API_KEY='{os.environ['PLATO_API_KEY']}' "
                + ("PLATO_FUSE_BINARY='/tmp/plato-fuse-bin/plato-fuse' " if os.environ.get("PLATO_FUSE_BINARY") else "")
                + f"plato-world-runner run "
                f"--world plato-world-webclone-setup-test "
                f"--config {config_path} -v "
                f"> {log_file} 2>&1; "
                f"status=$?; echo EXIT_CODE=$status; exit $status",
                timeout=600,
            )
        )

        # Collect logs
        try:
            log_code, log_output, _ = _run_async(webclone_vm.exec(f"tail -n 200 {log_file}", timeout=30))
            if log_code == 0:
                print(f"WORLD RUNNER LOG:\n{log_output}")
        except Exception as exc:
            log_output = f"<log unavailable: {exc}>"

        # Collect results
        try:
            rc, results_json, err = _run_async(webclone_vm.exec(f"cat {RESULTS_PATH}", timeout=10))
            results = json.loads(results_json) if rc == 0 else None
        except Exception:
            results = None

        if results:
            print(f"TEST RESULTS:\n{json.dumps(results, indent=2)}")

        assert code == 0, (
            f"Webclone setup test world failed (exit {code})\n"
            f"stdout: {stdout}\nstderr: {stderr}\n"
            f"log: {log_output}\n"
            f"results: {json.dumps(results, indent=2) if results else 'missing'}"
        )

        assert results is not None, f"No results JSON. stdout: {stdout}"
        for test_name, result in results.items():
            assert result.get("pass"), f"{test_name}: {result.get('error') or result.get('errors')}"
