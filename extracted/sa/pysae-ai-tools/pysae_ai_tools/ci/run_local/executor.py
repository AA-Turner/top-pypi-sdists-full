"""Execute the generated runner, on the host shell or inside the job's image."""

import subprocess
import sys
from pathlib import Path

from ...common.glab.runner import gitlab_token, glab_api, run_glab

# Where the generated scripts are mounted inside the container.
CONTAINER_RUN_DIR = "/tmp/run-local"

# Pick bash when the image has it, else fall back to sh (alpine/busybox images).
# Runs as ``sh -c '<dispatch>' <runner>`` so the runner path lands in $0.
_SHELL_DISPATCH = 'if command -v bash >/dev/null 2>&1; then exec bash "$0"; else exec sh "$0"; fi'


def run_host(runner_path: Path) -> int:
    """Run ``runner.sh`` directly on the host with bash (output streams live)."""
    try:
        result = subprocess.run(["bash", str(runner_path)])
    except FileNotFoundError:
        print("bash is not available on this host.", file=sys.stderr)
        return 127
    return result.returncode


def _run(cmd: list[str], *, stdin_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        input=stdin_text,
    )


def _glab_token() -> str:
    """Best-effort read of the glab token (never printed)."""
    res = run_glab("auth", "token")
    if res.ok and res.stdout:
        return res.stdout
    return gitlab_token()


def _glab_username() -> str:
    data = glab_api("user")
    if isinstance(data, dict) and isinstance(data.get("username"), str):
        return str(data["username"])
    return ""


def _try_registry_login(image: str, warnings: list[str]) -> bool:
    """Attempt a ``docker login`` for a GitLab registry image using the glab token."""
    registry_host = image.split("/", 1)[0]
    if "." not in registry_host:  # bare image like "python:3.12" — Docker Hub, no login
        return False
    token = _glab_token()
    if not token:
        return False
    username = _glab_username() or "oauth2"
    try:
        # Token is passed via stdin only — never on the command line or printed.
        login = _run(
            ["docker", "login", registry_host, "-u", username, "--password-stdin"],
            stdin_text=token,
        )
    except FileNotFoundError:
        return False
    if login.returncode != 0:
        warnings.append(f"docker login to {registry_host} failed — run it manually if the image is private.")
        return False
    return True


def ensure_image(image: str, pull: bool, warnings: list[str]) -> bool:
    """Make sure ``image`` is available locally, pulling (and logging in) if asked."""
    if not pull:
        return True
    pulled = _run(["docker", "pull", image])
    if pulled.returncode == 0:
        return True
    # Retry once after a best-effort registry login.
    if _try_registry_login(image, warnings):
        pulled = _run(["docker", "pull", image])
        if pulled.returncode == 0:
            return True
    warnings.append(
        f"Could not pull '{image}'. If it is private, run `docker login {image.split('/', 1)[0]}` and retry, "
        "or use --no-pull if it is already present locally."
    )
    return False


def run_docker(
    *,
    image: str,
    run_dir_host: Path,
    workdir_host: Path,
    container_project_dir: str,
    pull: bool,
    warnings: list[str],
) -> int:
    """Run the generated ``runner.sh`` inside ``image`` via ``docker run``."""
    ensure_image(image, pull, warnings)
    cmd = [
        "docker",
        "run",
        "--rm",
        "--entrypoint",
        "",
        "-v",
        f"{workdir_host}:{container_project_dir}",
        "-v",
        f"{run_dir_host}:{CONTAINER_RUN_DIR}:ro",
        "-w",
        container_project_dir,
        image,
        "sh",
        "-c",
        _SHELL_DISPATCH,
        f"{CONTAINER_RUN_DIR}/runner.sh",
    ]
    try:
        result = subprocess.run(cmd)
    except FileNotFoundError:
        print("docker is not installed or not in PATH.", file=sys.stderr)
        return 127
    return result.returncode
