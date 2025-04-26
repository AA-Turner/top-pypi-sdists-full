import os
from typing import Tuple


class MissingEnvVar(Exception):
    def __init__(self, var_name: str):
        super(MissingEnvVar, self).__init__()
        self.var_name = var_name

    def __str__(self) -> str:
        return f"Missing expected env variable of {self.var_name}"


def ensure_token_env_vars() -> Tuple[str, str]:
    """
    Verifies that the MCD_DEFAULT_API_ID and MCD_DEFAULT_API_TOKEN environment
    variables are defined.

    :return: a tuple of the variable values in the form (MCD_DEFAULT_API_ID, MCD_DEFAULT_API_TOKEN)
    :raises SystemExit if an expected variable is missing or empty.
    """
    api_id = os.environ.get("MCD_DEFAULT_API_ID")
    api_token = os.environ.get("MCD_DEFAULT_API_TOKEN")
    if not api_id:
        raise MissingEnvVar(var_name="MCD_DEFAULT_API_ID")
    if not api_token:
        raise MissingEnvVar(var_name="MCD_DEFAULT_API_TOKEN")
    return api_id, api_token


def ensure_endpoint_env_var() -> str:
    """
    Verifies that the MCD_API_ENDPOINT environment variable is defined.

    :return: the value of the variable MCD_API_ENDPOINT
    :raises SystemExit if the expected variable is missing or empty.
    """
    api_url = os.environ.get("MCD_API_ENDPOINT")
    if not api_url:
        raise MissingEnvVar(var_name="MCD_API_ENDPOINT")
    return api_url
