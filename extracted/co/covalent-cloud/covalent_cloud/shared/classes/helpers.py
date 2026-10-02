# Copyright 2023 Agnostiq Inc.

import sys
import time
from typing import Callable, Optional

import requests

from .api import APIClient
from .exceptions import CovalentSDKError
from .settings import Settings, settings


def check_env_is_ready(
    env_name: str,
    settings: Settings = settings,
    wait: Optional[bool] = False,
    timeout: Optional[int] = 1800,
) -> Callable:
    """
    Checks if the environment is ready.

    Args:
        env_name: Name of the environment to check.
        settings: Settings object with the dispatcher URI.
        wait: If True, waits until the environment is ready before returning.
        timeout: Timeout in seconds for the environment to be ready.

    Returns:
        True if the environment is ready, False otherwise.
        Environment response if the environment is ready.

    """
    is_env_ready = False
    dispatcher_addr = settings.dispatcher_uri
    dispatcher_port = settings.dispatcher_port
    env_response = {}
    try:
        client = APIClient(host_uri=dispatcher_addr, settings=settings, port=dispatcher_port)
        endpoint = "/api/v2/envs"
        request_options = {"params": {"name": env_name}}

        if wait:
            end_time = time.time() + timeout
            interval = 5
            print(f"Waiting for environment {env_name} to be ready...", end="", flush=True)
            while time.time() < end_time:
                is_env_ready, env_response = _get_env_status(
                    env_name, client, endpoint, request_options, wait
                )
                if is_env_ready:
                    break
                else:
                    time.sleep(interval)
                print(".", end="", flush=True)

            print()
            if not is_env_ready:
                raise CovalentSDKError(
                    f'Environment creation timed out, "{env_name}" is not ready.'
                )
        else:
            is_env_ready, env_response = _get_env_status(
                env_name, client, endpoint, request_options, wait
            )

    except requests.exceptions.HTTPError as e:
        print(e.response.text, file=sys.stderr)
        raise e

    return is_env_ready, env_response


def _get_env_status(
    env_name: str, client: APIClient, endpoint: str, request_options, wait: bool = False
):
    """
    Gets the status of the environment.

    Args:
        env_name: Name of the environment to check.
        client: APIClient object.
        endpoint: Endpoint to send the request to.
        request_options: Options to send with the request.
        wait: If True, waits until the environment is ready before returning.

    Returns:
        True if the environment is ready, False otherwise.
        Environment response if the environment is ready.

    """
    is_env_ready = False

    env_response = client.get(endpoint, request_options).json()

    if len(env_response["records"]) == 0:
        raise CovalentSDKError(f'Environment "{env_name}" does not exist.')

    if env_response["records"][0]["status"] == "READY":
        is_env_ready = True
    elif env_response["records"][0]["status"] == "ERROR":
        raise CovalentSDKError(
            f"Failed to create environment '{env_name}'. "
            "Please check build logs and package dependencies."
        )
    elif not wait:
        raise CovalentSDKError(f'Environment "{env_name}" is not ready.')

    return is_env_ready, env_response
