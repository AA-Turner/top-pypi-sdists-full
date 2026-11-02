from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

pytest.importorskip("harbor")

from harbor.job import Job
from harbor.models.job.config import JobConfig
from harbor.models.trial.config import AgentConfig, EnvironmentConfig, TaskConfig


ROOT = Path(__file__).resolve().parents[1]
HARBOR_ROOT = ROOT / "integrations" / "harbor"
RUNTA_ENV_IMPORT_PATH = "runta_harbor.environment:RuntaEnvironment"

if str(HARBOR_ROOT) not in sys.path:
    sys.path.insert(0, str(HARBOR_ROOT))


pytestmark = pytest.mark.skipif(
    os.getenv("RUNTA_HARBOR_E2E") != "1"
    or not (os.getenv("RUNTA_HARBOR_TOKEN") or os.getenv("RUNTA_TOKEN")),
    reason="set RUNTA_HARBOR_E2E=1 with RUNTA_HARBOR_TOKEN or RUNTA_TOKEN",
)


@pytest.mark.asyncio
async def test_runta_harbor_e2e_parallel_sample_tasks(tmp_path: Path) -> None:
    """Run the packaged Harbor demo tasks concurrently through runta-sdk[harbor]."""

    task_paths = sorted((HARBOR_ROOT / "tasks").glob("square-*"))
    assert len(task_paths) >= 2

    result = await _run_harbor_job(
        tmp_path,
        job_name="runta-harbor-e2e-parallel",
        tasks=[TaskConfig(path=path) for path in task_paths[:2]],
        n_concurrent_trials=2,
        mode="auto",
    )

    _assert_rewards(result, expected_trials=2)


@pytest.mark.asyncio
async def test_runta_harbor_e2e_compose_sidecar_artifact_dir(tmp_path: Path) -> None:
    """Exercise compose sidecar collect plus directory artifact download."""

    task_path = _write_sidecar_artifact_task(tmp_path)

    result = await _run_harbor_job(
        tmp_path,
        job_name="runta-harbor-e2e-sidecar-artifact",
        tasks=[TaskConfig(path=task_path)],
        n_concurrent_trials=1,
        mode="compose",
    )

    _assert_rewards(result, expected_trials=1)
    trial = result.trial_results[0]
    artifacts_dir = (
        tmp_path
        / "jobs"
        / "runta-harbor-e2e-sidecar-artifact"
        / trial.trial_name
        / "artifacts"
    )
    assert (
        artifacts_dir / "sidecar-out" / "result.txt"
    ).read_text() == "sidecar-ok\n"


async def _run_harbor_job(
    tmp_path: Path,
    *,
    job_name: str,
    tasks: list[TaskConfig],
    n_concurrent_trials: int,
    mode: str,
):
    if token := os.getenv("RUNTA_HARBOR_TOKEN"):
        os.environ["RUNTA_TOKEN"] = token

    env_kwargs = {
        "endpoint": os.getenv("RUNTA_HARBOR_ENDPOINT", "https://api.runta.com"),
        "mode": mode,
    }

    job = await Job.create(
        JobConfig(
            job_name=job_name,
            jobs_dir=tmp_path / "jobs",
            n_concurrent_trials=n_concurrent_trials,
            quiet=True,
            agents=[AgentConfig(name="oracle")],
            environment=EnvironmentConfig(
                import_path=RUNTA_ENV_IMPORT_PATH,
                type=None,
                kwargs=env_kwargs,
            ),
            tasks=tasks,
        )
    )
    return await job.run()


def _assert_rewards(result, *, expected_trials: int) -> None:
    assert len(result.trial_results) == expected_trials
    for trial in result.trial_results:
        assert trial.exception_info is None
        assert trial.verifier_result is not None
        assert trial.verifier_result.rewards == {"reward": 1.0}


def _write_sidecar_artifact_task(tmp_path: Path) -> Path:
    task = tmp_path / "sidecar-artifact"
    environment = task / "environment"
    solution = task / "solution"
    tests = task / "tests"
    environment.mkdir(parents=True)
    solution.mkdir()
    tests.mkdir()

    (task / "task.toml").write_text(
        """
schema_version = "1.3"
artifacts = [
  { source = "/evidence/out", destination = "sidecar-out", service = "evidence" },
]

[task]
name = "runta/sidecar-artifact"
description = "Runta Harbor sidecar artifact e2e task."
authors = []
keywords = ["runta", "harbor", "e2e", "compose"]

[verifier]
timeout_sec = 120.0
environment_mode = "separate"

[[verifier.collect]]
service = "evidence"
command = "mkdir -p /evidence/out && printf 'sidecar-ok\\n' > /evidence/out/result.txt"
timeout_sec = 30.0

[verifier.environment]
workdir = "/tests"
cpus = 1
memory_mb = 1024
storage_mb = 1024
gpus = 0

[agent]
timeout_sec = 60.0

[environment]
cpus = 1
memory_mb = 1024
storage_mb = 1024
gpus = 0
""".lstrip()
    )
    (task / "instruction.md").write_text("Run the provided solution.\n")
    (solution / "solve.sh").write_text(
        "#!/bin/sh\n"
        "set -eu\n"
        "mkdir -p /logs/artifacts\n"
        "echo main-ok > /logs/artifacts/main.txt\n"
    )
    (tests / "test.sh").write_text(
        """#!/bin/sh
set -eu
mkdir -p /logs/verifier
if [ "$(cat /evidence/out/result.txt 2>/dev/null || true)" = "sidecar-ok" ]; then
  echo 1 > /logs/verifier/reward.txt
else
  echo 0 > /logs/verifier/reward.txt
fi
"""
    )
    (solution / "solve.sh").chmod(0o755)
    (tests / "test.sh").chmod(0o755)

    (tests / "Dockerfile").write_text(
        """
FROM alpine:3.20
COPY test.sh /tests/test.sh
RUN chmod +x /tests/test.sh && mkdir -p /evidence/out /logs/verifier
""".lstrip()
    )
    (environment / "Dockerfile").write_text("FROM alpine:3.20\n")
    (environment / "docker-compose.yaml").write_text(
        """
services:
  main:
    depends_on:
      evidence:
        condition: service_started
  evidence:
    image: alpine:3.20
    command: ["sh", "-c", "mkdir -p /evidence/out && while true; do sleep 3600; done"]
""".lstrip()
    )
    (tests / "docker-compose.yaml").write_text(
        """
services:
  main:
    build: .
    command: ["sh", "-c", "mkdir -p /evidence/out && while true; do sleep 3600; done"]
""".lstrip()
    )
    return task
