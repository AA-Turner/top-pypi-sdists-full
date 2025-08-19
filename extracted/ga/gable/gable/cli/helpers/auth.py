import os
from pathlib import Path

import click
from loguru import logger

from gable.openapi import GetNpmCredentialsResponse, GetPipCredentialsResponse

AUTH_BLOCK_START = "### Gable Auth Block Start ###"
AUTH_BLOCK_END = "### Gable Auth Block End ###"


def format_npmrc_credentials(npm_credentials: GetNpmCredentialsResponse) -> str:
    """
    Format the NPM credentials as a string for writing to the .npmrc file
    """

    registry_endpoint_http_trimmed = npm_credentials.repositoryEndpoint[
        npm_credentials.repositoryEndpoint.find("//") :
    ]
    return f"""
@gable-eng:registry={npm_credentials.repositoryEndpoint}
{registry_endpoint_http_trimmed}:_authToken={npm_credentials.authToken}
{registry_endpoint_http_trimmed}:always-auth=true
    """.strip()


def set_npm_config_credentials(npm_credentials: GetNpmCredentialsResponse):
    """
    Set the NPM_CONFIG environment variables for the credentials
    """

    registry_endpoint_http_trimmed = npm_credentials.repositoryEndpoint[
        npm_credentials.repositoryEndpoint.find("//") :
    ]
    os.environ["NPM_CONFIG_@gable-eng:REGISTRY"] = npm_credentials.repositoryEndpoint
    os.environ[f"NPM_CONFIG_{registry_endpoint_http_trimmed}:_authToken"] = (
        npm_credentials.authToken
    )


def write_npm_credentials(
    creds: GetNpmCredentialsResponse, npmrcPath: str = "~/.npmrc"
):
    """
    Write or update the Gable NPM credentials to the user's .npmrc file
    """

    # Expand the home directory path and resolve it to an absolute path
    npmrcPath = Path(npmrcPath).expanduser().resolve().as_posix()

    text = (
        AUTH_BLOCK_START
        + "\n"
        + format_npmrc_credentials(creds)
        + "\n"
        + AUTH_BLOCK_END
        + "\n"
    )

    # If the file exists, update the existing block or add a new one
    if os.path.exists(os.path.realpath(npmrcPath)):
        # Read the file contents
        with open(npmrcPath, "r") as f:
            content = f.read()
            if AUTH_BLOCK_START in content and AUTH_BLOCK_END in content:
                # Replace the existing block
                start = content.find(AUTH_BLOCK_START) + len(AUTH_BLOCK_START)
                end = content.find(AUTH_BLOCK_END)
                text = (
                    content[:start]
                    + "\n"
                    + format_npmrc_credentials(creds)
                    + "\n"
                    + content[end:]
                )
            else:
                # Add a new block
                text = content + "\n\n" + text

    # Write the file contents
    with open(npmrcPath, "w") as f:
        f.write(text)


def set_pip_config_credentials(
    pip_credentials: GetPipCredentialsResponse, file_path: str = None  # type: ignore
):
    """
    Set the PIP_CONFIG environment variables for the credentials
    and optionally write them to a file if file_path is provided
    """
    # Set environment variables using AWS CodeArtifact format
    os.environ["CODEARTIFACT_AUTH_TOKEN"] = pip_credentials.authToken
    # Format index URL according to AWS CodeArtifact expectation
    index_url = f"https://aws:{pip_credentials.authToken}@{pip_credentials.repositoryEndpoint.split('//')[1]}"
    os.environ["PIP_INDEX_URL"] = index_url
    os.environ["PIP_EXTRA_INDEX_URL"] = "https://pypi.org/simple"

    logger.debug(
        f"Set CODEARTIFACT_AUTH_TOKEN environment variable for Gable libraries"
    )
    logger.debug(f"Set PIP_INDEX_URL to use AWS CodeArtifact format")

    # Write the credentials to file if file_path is provided
    if file_path:
        write_pip_credentials_to_env_file(pip_credentials, file_path)


def write_pip_credentials_to_env_file(
    pip_credentials: GetPipCredentialsResponse, file_path: str = "~/.gable/.env"
):
    """
    Write PIP credentials to a .env file under user's home directory
    in ~/.gable/.env or specified file path
    """
    # Expand the home directory path
    expanded_file_path = os.path.expanduser(file_path)

    # Get the directory from the file path
    dir_path = os.path.dirname(expanded_file_path)

    # Create the directory if it doesn't exist
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        logger.debug(f"Created directory: {dir_path}")

    # Format the credentials for the .env file following AWS CodeArtifact format
    env_content = f"""# Gable PIP Authentication Configuration
# Generated on {os.popen('date').read().strip()}
# AWS CodeArtifact format for pip configuration
export PIP_INDEX_URL=https://aws:{pip_credentials.authToken}@{pip_credentials.repositoryEndpoint.split('//')[1]}
export PIP_EXTRA_INDEX_URL=https://pypi.org/simple
"""

    # Write the file
    with open(expanded_file_path, "w") as f:
        f.write(env_content)

    logger.debug(f"PIP authentication credentials written to {expanded_file_path}")
    logger.debug(
        f"You can load these credentials by running: source {expanded_file_path}"
    )
