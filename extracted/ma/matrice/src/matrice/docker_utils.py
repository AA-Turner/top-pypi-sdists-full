"""Module providing docker_utils functionality."""

import logging
import subprocess
import shutil
import os
from typing import Optional


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
        docker_pull_process = subprocess.Popen(
            [
                shutil.which("docker"),
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
    Check Docker status and installation on the system.
    Installs Docker if not present or repairs corrupted installation.

    Raises:
        Exception: If Docker installation/repair fails
    """
    if not test_docker():
        logging.info("Docker is not installed or not running. Installing/repairing Docker...")
        if try_host_docker():
            logging.info("Docker installed successfully.")
            return
        logging.warning("Failed to use Host Docker. Will try to install manually.")
        _reinstall_docker()


def _reinstall_docker() -> None:
    """
    Helper function to handle Docker reinstallation process

    Raises:
        Exception: If Docker reinstallation fails
    """
    uninstall_docker()
    install_docker()
    start_docker()
    if not test_docker():
        raise Exception("Docker installation failed - system may need manual intervention")


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
    Start the Docker daemon using appropriate method based on system configuration.

    Raises:
        Exception: If starting Docker daemon fails
    """
    try:
        if not os.path.exists("/run/systemd/system"):
            try:
                subprocess.run(
                    ["ulimit", "-n", "524288"],
                    shell=True,
                    check=True,
                    capture_output=True,
                )
            except subprocess.CalledProcessError:
                logging.warning("Failed to set ulimit, continuing anyway...")
            subprocess.run(
                ["/etc/init.d/docker", "start"],
                check=True,
                capture_output=True,
            )
        else:
            subprocess.run(
                ["systemctl", "start", "docker"],
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["systemctl", "enable", "docker"],
                check=True,
                capture_output=True,
            )
        logging.info("Docker daemon started successfully")
    except Exception as e:
        logging.error("Error starting Docker daemon: %s", e)
        raise


def try_host_docker() -> bool:
    """
    Try to install and test Docker using the system's package manager.

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        subprocess.run(
            ["apt-get", "update"],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            [
                "apt-get",
                "install",
                "-y",
                "docker.io",
            ],
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["docker", "run", "hello-world"],
            check=True,
            capture_output=True,
        )
        logging.info("Docker is installed and running correctly.")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(
            "Error installing/testing Docker via package manager: %s",
            e,
        )
        return False


def install_docker() -> None:
    """
    Install Docker on the system using official Docker installation steps.

    Raises:
        subprocess.CalledProcessError: If installation fails
    """
    install_commands = [
        "apt-get update -y",
        "apt-get install ca-certificates curl -y",
        "install -m 0755 -d /etc/apt/keyrings",
        "curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc",
        "chmod a+r /etc/apt/keyrings/docker.asc",
        'echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo ${UBUNTU_CODENAME:-$VERSION_CODENAME}) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null',
        "apt-get update -y",
        "apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y",
    ]
    try:
        for command in install_commands:
            subprocess.run(
                command,
                shell=True,
                check=True,
                capture_output=True,
            )
        logging.info("Docker installed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error("Error installing Docker: %s", e)
        raise


def uninstall_docker() -> None:
    """
    Uninstall Docker and related packages from the system.

    Raises:
        subprocess.CalledProcessError: If uninstallation fails
    """
    try:
        subprocess.run(
            [
                "apt-get",
                "remove",
                "docker.io",
                "docker-doc",
                "docker-compose",
                "docker-compose-v2",
                "podman-docker",
                "containerd",
                "runc",
                "-y",
            ],
            check=True,
            capture_output=True,
        )
        logging.info("Docker uninstalled successfully.")
    except subprocess.CalledProcessError as e:
        logging.error("Error uninstalling Docker: %s", e)
        raise
