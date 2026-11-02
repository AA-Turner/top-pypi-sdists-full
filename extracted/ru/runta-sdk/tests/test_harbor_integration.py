from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

harbor = pytest.importorskip("harbor")

from harbor.job import Job
from harbor.models.job.config import JobConfig
from harbor.models.trial.config import AgentConfig, EnvironmentConfig, TaskConfig


ROOT = Path(__file__).resolve().parents[1]
HARBOR_ROOT = ROOT / "integrations" / "harbor"
RUNTA_ENV_IMPORT_PATH = "runta_harbor.environment:RuntaEnvironment"

if str(HARBOR_ROOT) not in sys.path:
    sys.path.insert(0, str(HARBOR_ROOT))


pytestmark = pytest.mark.skipif(
    os.getenv("RUNTA_HARBOR_LIVE") != "1"
    or not (os.getenv("RUNTA_HARBOR_TOKEN") or os.getenv("RUNTA_TOKEN")),
    reason="set RUNTA_HARBOR_LIVE=1 with RUNTA_HARBOR_TOKEN or RUNTA_TOKEN",
)


@pytest.mark.asyncio
async def test_runta_harbor_direct_mode(tmp_path: Path) -> None:
    task = _write_square_task(tmp_path, "direct", answer="4", expected="4", dockerfile=True)
    result = await _run_harbor_task(tmp_path, task, mode="direct")

    _assert_success(result)


@pytest.mark.asyncio
async def test_runta_harbor_docker_mode(tmp_path: Path) -> None:
    task = _write_square_task(tmp_path, "docker", answer="9", expected="9", dockerfile=True)
    result = await _run_harbor_task(tmp_path, task, mode="docker")

    _assert_success(result)


@pytest.mark.asyncio
async def test_runta_harbor_compose_mode(tmp_path: Path) -> None:
    task = _write_square_task(tmp_path, "compose", answer="16", expected="16", compose=True)
    result = await _run_harbor_task(tmp_path, task, mode="compose")

    _assert_success(result)


async def _run_harbor_task(tmp_path: Path, task_path: Path, *, mode: str):
    endpoint = os.getenv("RUNTA_HARBOR_ENDPOINT", "https://api.runta.com")
    if token := os.getenv("RUNTA_HARBOR_TOKEN"):
        os.environ["RUNTA_TOKEN"] = token
    job = await Job.create(
        JobConfig(
            job_name=f"runta-harbor-{mode}-integration",
            jobs_dir=tmp_path / "jobs",
            n_concurrent_trials=1,
            quiet=True,
            agents=[AgentConfig(name="oracle")],
            environment=EnvironmentConfig(
                import_path=RUNTA_ENV_IMPORT_PATH,
                type=None,
                kwargs={
                    "endpoint": endpoint,
                    "mode": mode,
                },
            ),
            tasks=[TaskConfig(path=task_path)],
        )
    )
    return await job.run()


def _assert_success(result) -> None:
    assert len(result.trial_results) == 1
    trial = result.trial_results[0]
    assert trial.exception_info is None
    assert trial.verifier_result is not None
    assert trial.verifier_result.rewards == {"reward": 1.0}


def _write_square_task(
    tmp_path: Path,
    name: str,
    *,
    answer: str,
    expected: str,
    dockerfile: bool = False,
    compose: bool = False,
) -> Path:
    task = tmp_path / f"square-{name}"
    environment = task / "environment"
    solution = task / "solution"
    tests = task / "tests"
    environment.mkdir(parents=True)
    solution.mkdir(parents=True)
    tests.mkdir(parents=True)

    (task / "task.toml").write_text(
        f"""
schema_version = "1.1"

[task]
name = "runta/square-{name}"
description = "Runta Harbor {name} mode integration task."
authors = []
keywords = ["runta", "harbor", "integration"]

[verifier]
timeout_sec = 60.0

[agent]
timeout_sec = 60.0

[environment]
cpus = 1
memory_mb = 1024
storage_mb = 1024
gpus = 0
""".lstrip()
    )
    (task / "instruction.md").write_text(f"Write {expected} to /tmp/answer.txt.\n")
    (solution / "solve.sh").write_text(f"#!/bin/sh\nset -eu\necho {answer} > /tmp/answer.txt\n")
    (tests / "test.sh").write_text(
        f"""#!/bin/sh
set -eu
mkdir -p /logs/verifier
if [ "$(cat /tmp/answer.txt 2>/dev/null || true)" = "{expected}" ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
"""
    )
    (solution / "solve.sh").chmod(0o755)
    (tests / "test.sh").chmod(0o755)

    if dockerfile:
        (environment / "Dockerfile").write_text("FROM bash:5.2.37-alpine3.22\n")
    if compose:
        (environment / "Dockerfile").write_text("FROM bash:5.2.37-alpine3.22\n")
        (environment / "docker-compose.yaml").write_text(
            """
services:
  main: {}
""".lstrip()
        )

    return task
