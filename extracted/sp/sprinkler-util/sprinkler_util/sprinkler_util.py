import json
import os
from typing import Any, Optional


class SprinklerSecretNotSetException(Exception):
    """Exception raised when a secret is not found."""


def get_request_body(as_json: bool = False) -> Any:
    """
    Retrieve the request body if it exists.
    Returns None if no body was provided in the webhook
    , or if this was a scheduled run of the task.

    Args:
        as_json (bool, optional): Parse the request body and return . Defaults to False.

    Returns:
        Any: The request body.
    """

    body = json.loads(os.environ.get("SPRINKLER_TASK_INSTANCE_BODY", ""))
    if body == "":
        return None
    if as_json:
        return json.loads(body)
    return body


def send_response(response: Any) -> None:
    """
    Send a response from within a call-and-response type task. May only be used once.
    Internally wraps the response in `json.dumps(response, default=str)`

    Args:
        response (Any): The response to be sent to the requestor.
    """
    print(
        f"""SPRINKLER*_*RESPONSE*_*START*{json.dumps(response, default=str)}*SPRINKLER*_*RESPONSE*_*END"""
    )


def get_secret(key: str, default: Optional[str] = None) -> str:
    """
    Get a secret from the sprinkler secrets store within a Sprinkler task.

    Args:
        key (str): The secret to retrieve (case insensitive)
        default (str, optional): A default value to return when the secret is not found. Defaults to None.

    Raises:
        SprinklerSecretNotSetException: Raised when a secret is not found, and no default value is provided

    Returns:
        str: The secret value.
    """
    secret = os.environ.get(f"SPRINKLER_SECRET_{key.upper()}")
    if secret is None:
        if default is not None:
            return default
        raise SprinklerSecretNotSetException(key)
    return secret
