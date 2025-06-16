import os

import requests

from dbt_copilot_python.utility import is_copilot


def setup_allowed_hosts(allowed_hosts: list[str]) -> list[str]:
    """
    Add the private IP address of the container to ALLOWED_HOSTS if it's a
    Copilot application.

    Usage in settings.py:

    ALLOWED_HOSTS = setup_allowed_hosts(ALLOWED_HOSTS)
    """

    if is_copilot():
        try:
            aws_metadata = requests.get(
                os.environ["ECS_CONTAINER_METADATA_URI_V4"], timeout=0.01
            ).json()
            allowed_hosts.append(aws_metadata["Networks"][0]["IPv4Addresses"][0])
        except requests.exceptions.RequestException:
            pass

    return allowed_hosts
