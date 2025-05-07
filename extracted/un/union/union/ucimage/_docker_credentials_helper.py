import base64
import json
import logging
import os
import subprocess
import tempfile
from pathlib import Path
from typing import List, Optional, Tuple

logger = logging.getLogger("union.cli.ucimage._docker_credentials_helper")

_CONFIG_JSON = "config.json"
_DEFAULT_CONFIG_PATH = f"~/.docker/{_CONFIG_JSON}"
_CRED_HELPERS = "credHelpers"
_CREDS_STORE = "credsStore"


def _load_docker_config(config_path: str = _DEFAULT_CONFIG_PATH) -> dict:
    """Load Docker config from specified path

    Raises:
        FileNotFoundError: If the config file does not exist
        json.JSONDecodeError: If the config file is not valid JSON
    """
    if not config_path:
        config_path = _DEFAULT_CONFIG_PATH

    config_path = os.path.expanduser(config_path)
    with open(config_path) as f:
        return json.load(f)


def _get_credential_helper(config: dict, registry: Optional[str] = None) -> Optional[str]:
    """Get credential helper for registry or global default"""
    if registry and _CRED_HELPERS in config and registry in config[_CRED_HELPERS]:
        return config[_CRED_HELPERS].get(registry)
    credsStore = config.get(_CREDS_STORE)
    return credsStore


def _get_credentials(helper: str, registry: str) -> Optional[Tuple[str, str]]:
    """Get credentials from system credential helper"""

    # Naming convention established.
    helper_cmd = f"docker-credential-{helper}"

    try:
        process = subprocess.Popen(
            [helper_cmd, "get"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        output, error = process.communicate(input=registry)

        if process.returncode != 0:
            logging.error(f"Credential helper error: {error}")
            return None

        creds = json.loads(output)
        return creds.get("Username"), creds.get("Secret")
    except FileNotFoundError:
        logger.error(f"Credential helper {helper_cmd} not found in PATH")
        return None
    except Exception as e:
        logger.error(f"Error getting credentials: {e!s}")
        return None


def derive_docker_credentials(
    registries: Optional[List[str]], docker_config_path: Optional[Path], output_path: Optional[Path]
) -> Path:
    """
    Create new Docker config file. Targets specific registries if provided, otherwise all registries
    in auths are targeted.

    This function extracts Docker registry credentials from the user's Docker config file
    and creates a new config file containing only the credentials for the specified registries.
    It handles credentials stored directly in the config file as well as those managed by
    credential helpers.

    Args:
        registries: List of registries to extract credentials for. If None, all registries
                   from the config will be used.
        docker_config_path: Path to the Docker config file. If None, the function will look
                          for the config file in the standard locations: first checking the
                          DOCKER_CONFIG environment variable, then falling back to ~/.docker/config.json.
        output_path: Path where the new config file should be written. If None, a temporary
                    directory will be created and the config will be written to
                    {temp_dir}/docker/config.json.

    Returns:
        Path: The path to the newly created Docker config file containing only the
              extracted credentials.
    """

    # Check DOCKER_CONFIG environment variable first
    if not docker_config_path:
        docker_config_env = os.environ.get("DOCKER_CONFIG")
        if docker_config_env:
            docker_config_path = os.path.join(docker_config_env, _CONFIG_JSON)
        else:
            docker_config_path = os.path.expanduser(_DEFAULT_CONFIG_PATH)

    config = _load_docker_config(docker_config_path)

    # Create new config structure with empty auths
    new_config = {"auths": {}}

    registries = registries or config.get("auths", {}).keys()

    for registry in registries:
        registry_config = config.get("auths", {}).get(registry, {})
        if registry_config.get("auth"):
            new_config["auths"][registry] = registry_config.copy()
        else:
            # Try to get credentials from helper
            helper = _get_credential_helper(config, registry)
            if helper:
                creds = _get_credentials(helper, registry)
                if creds:
                    username, password = creds
                    auth_string = f"{username}:{password}"
                    new_config["auths"][registry] = {"auth": base64.b64encode(auth_string.encode()).decode()}

    # Save the new config to the output path or a temporary file
    if not output_path:
        temp_dir = tempfile.mkdtemp()
        docker_dir = os.path.join(temp_dir, "docker")
        os.makedirs(docker_dir, exist_ok=True)
        output_path = os.path.join(docker_dir, _CONFIG_JSON)

    with open(output_path, "w") as f:
        json.dump(new_config, f)

    return output_path
