"""Docker-compose wrapper used by `innoday platform start/stop/restart/logs`."""

import os
import shutil
import subprocess
from typing import List, Optional

DOCKER_REQUIRED_MESSAGE = (
    "Docker is required to run InnoDay locally. "
    "Install Docker Desktop or Docker Engine and retry."
)

VALID_ENVS = {"local", "dev", "test"}

# `prod` is intentionally excluded: there is no .env.prod file (production
# deployments inject vars directly via the hosting platform -- Render/Railway/
# Fly.io -- per CLAUDE.md), so `--env-file .env.prod` has nothing correct to
# point at. The docker-compose.yml `prod` profile is a local
# production-*like* SQLite profile for testing container behavior, not a way
# to reach real production -- routing `platform start --env prod` through
# this same --env-file mechanism would silently do the wrong thing.

_ACTION_ARGS = {
    "up": ["up", "-d"],
    "down": ["down"],
    "restart": ["restart"],
    "logs": ["logs", "-f"],
}


def find_compose_binary() -> Optional[List[str]]:
    """Detect an available docker-compose binary, preferring the v2 plugin."""
    try:
        result = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True,
            check=False,
        )
        if result.returncode == 0:
            return ["docker", "compose"]
    except FileNotFoundError:
        pass

    if shutil.which("docker-compose"):
        return ["docker-compose"]

    return None


def validate_env(env: str) -> None:
    """Raise ValueError if env is not a supported local environment."""
    if env not in VALID_ENVS:
        raise ValueError(
            f"Invalid environment '{env}'. Must be one of: {sorted(VALID_ENVS)}"
        )


def build_compose_command(
    action: str,
    env: Optional[str] = None,
    compose_base: Optional[List[str]] = None,
    service: Optional[str] = None,
) -> List[str]:
    """Build the full argv list for a docker-compose action. Pure, no subprocess calls."""
    compose_base = compose_base or ["docker", "compose"]
    command = list(compose_base)

    if action == "up" and env:
        command += ["--env-file", f".env.{env}"]

    command += _ACTION_ARGS[action]

    if action == "logs" and service:
        command.append(service)

    return command


def run_compose(
    action: str,
    env: Optional[str] = None,
    follow: bool = False,
    service: Optional[str] = None,
) -> int:
    """Resolve the compose binary and run the requested action, returning the exit code."""
    compose_base = find_compose_binary()
    if compose_base is None:
        print(DOCKER_REQUIRED_MESSAGE)
        return 1

    command = build_compose_command(
        action, env=env, compose_base=compose_base, service=service
    )
    run_env = {**os.environ}
    if env:
        run_env["ENVIRONMENT"] = env

    if follow:
        process = subprocess.Popen(command, env=run_env)
        return process.wait()

    result = subprocess.run(command, env=run_env, check=False)
    return result.returncode
