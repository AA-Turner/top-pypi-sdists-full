"""Module providing docker_utils functionality."""

import logging
import shutil
import subprocess
from typing import Optional

# Guidance surfaced when Docker is not usable. We no longer shell out to
# apt-get / systemctl / tee /etc/apt (which all require root). Instead we fail
# loudly with actionable steps so the operator (not this process) provisions
# Docker with the right privileges.
_DOCKER_SETUP_HINT = (
    "Docker is not installed or not usable by the current user. This process "
    "no longer auto-installs Docker (that requires root). Please install "
    "Docker and grant the runtime user access, e.g.:\n"
    "  # Install Docker Engine (see https://docs.docker.com/engine/install/)\n"
    "  sudo apt-get update && sudo apt-get install -y docker.io\n"
    "  # Allow the current user to use Docker without root:\n"
    '  sudo usermod -aG docker "$USER" && newgrp docker\n'
    "  # Ensure the daemon is running:\n"
    "  sudo systemctl enable --now docker\n"
    "Then re-run this command."
)


def pull_docker_image(
    docker_image: str,
) -> Optional[subprocess.Popen]:
    """
    Download a docker image.

    Args:
        docker_image: Name/URL of the docker image to pull

    Returns:
        subprocess.Popen object if successful, None if failed

    Raises:
        Exception: If docker pull fails
    """
    try:
        check_docker()
        logging.info(
            "Starting download of docker image: %s",
            docker_image,
        )
        docker_bin = shutil.which("docker")
        if docker_bin is None:
            raise FileNotFoundError("Docker binary not found in PATH")
        docker_pull_process = subprocess.Popen(
            [
                docker_bin,
                "pull",
                docker_image,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        logging.info("Docker pull command initiated successfully")
        return docker_pull_process
    except Exception as e:
        logging.error(
            "Docker image download failed with error: %s",
            str(e),
            exc_info=True,
        )
        raise


def check_docker() -> None:
    """
    Check that Docker is installed and usable by the current (non-root) user.

    This no longer auto-installs Docker (which requires root). If Docker is
    already usable it returns; otherwise it raises with operator guidance.

    Raises:
        RuntimeError: If Docker is not installed / not usable.
    """
    if test_docker():
        return
    logging.error("Docker is not usable by the current user; auto-install is disabled.")
    raise RuntimeError(_DOCKER_SETUP_HINT)


def _reinstall_docker() -> None:
    """
    Deprecated: Docker (re)installation requires root and is no longer performed
    automatically. Kept for backward compatibility; raises with guidance.

    Raises:
        RuntimeError: Always, unless Docker is already usable (then no-op).
    """
    if test_docker():
        logging.info("Docker already usable; nothing to reinstall.")
        return
    raise RuntimeError(_DOCKER_SETUP_HINT)


def test_docker() -> bool:
    """
    Test if Docker is installed and running properly.

    Returns:
        bool: True if Docker is installed and running correctly, False otherwise
    """
    docker_path = shutil.which("docker")
    if docker_path is None:
        logging.warning("Docker binary not found in system PATH")
        return False
    try:
        subprocess.run(
            [docker_path, "run", "hello-world"],
            check=True,
            capture_output=True,
        )
        logging.info("Docker is installed and running correctly.")
        return True
    except subprocess.CalledProcessError as e:
        logging.error("Error running Docker test: %s", e)
        return False


def start_docker() -> None:
    """
    Ensure the Docker daemon is usable.

    Starting the daemon (systemctl / init.d) requires root, so this no longer
    shells out to start it. If Docker is already usable this is a no-op;
    otherwise it raises with operator guidance.

    Raises:
        RuntimeError: If the Docker daemon is not usable.
    """
    if test_docker():
        logging.info("Docker daemon is already running.")
        return
    logging.error("Docker daemon is not usable; auto-start is disabled (requires root).")
    raise RuntimeError(_DOCKER_SETUP_HINT)


def try_host_docker() -> bool:
    """
    Check whether the host already has a usable Docker.

    Previously this ran ``apt-get install`` (root). It now only *checks* the
    existing host Docker and never installs.

    Returns:
        bool: True if host Docker is usable, False otherwise.
    """
    return test_docker()


def install_docker() -> None:
    """
    No-op if Docker is already usable; otherwise raise with guidance.

    Docker installation requires root (apt-get / tee /etc/apt / systemctl), so
    it is no longer performed automatically. The public name/signature is kept
    for backward compatibility with callers.

    Raises:
        RuntimeError: If Docker is not installed / not usable.
    """
    if test_docker():
        logging.info("Docker already installed and usable; skipping install.")
        return
    logging.error("Docker is not installed; automatic install is disabled (requires root).")
    raise RuntimeError(_DOCKER_SETUP_HINT)


def uninstall_docker() -> None:
    """
    Deprecated no-op: uninstalling Docker requires root and is no longer
    performed automatically. Kept for backward compatibility.

    Raises:
        RuntimeError: Always — signals that manual, privileged action is needed.
    """
    logging.error("Automatic Docker uninstall is disabled (requires root).")
    raise RuntimeError(
        "Automatic Docker uninstall is disabled because it requires root. "
        "If you need to remove Docker, do so manually with appropriate privileges."
    )
