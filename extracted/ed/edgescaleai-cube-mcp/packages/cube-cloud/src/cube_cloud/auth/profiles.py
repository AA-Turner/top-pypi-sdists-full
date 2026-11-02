"""Profile-to-Apollo-credentials mapping via AWS Secrets Manager."""

from __future__ import annotations

import json

import boto3
from botocore.exceptions import ClientError

from cube_cloud.config import settings


class ProfileSecretNotFound(ValueError):
    """The profile has no secret at all. A subclass, so callers catching ValueError
    (every `get_credentials` caller) are unchanged; `auth/app_companies.py` alone needs
    to tell "absent" apart from "denied" or "corrupt"."""


def read_profile_secret(profile: str) -> dict:
    """The profile's whole secret JSON. Raises ValueError if it cannot be used:
    `ProfileSecretNotFound` when it does not exist, a plain ValueError when access is
    denied or the body is not a JSON object.

    Two readers share it: `get_credentials` (the Apollo client pair) and
    `auth/app_companies.py` (the non-secret ``app_companies`` field that
    `scripts/provision-access.py` stores beside them).
    """
    client = boto3.client("secretsmanager", region_name=settings.aws_region)
    secret_name = f"{settings.secrets_prefix}{profile}"

    try:
        resp = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        code = e.response["Error"]["Code"]
        if code == "ResourceNotFoundException":
            raise ProfileSecretNotFound(f"No credentials found for profile '{profile}'") from e
        if code == "AccessDeniedException":
            raise ValueError(f"No credentials found for profile '{profile}'") from e
        raise

    secret = json.loads(resp["SecretString"])
    if not isinstance(secret, dict):
        raise ValueError(f"Profile '{profile}' secret is not a JSON object")
    return secret


def get_credentials(profile: str) -> tuple[str, str]:
    """Get Apollo client_id and client_secret for a profile.

    Reads from Secrets Manager at: {prefix}{profile}
    Secret value JSON: {"client_id": "...", "client_secret": "...", "app_companies": [...]}
    (``app_companies`` is optional and read by `auth/app_companies.py`, not here.)

    Returns (client_id, client_secret). Raises ValueError if not found.
    """
    secret = read_profile_secret(profile)
    client_id = secret.get("client_id", "")
    client_secret = secret.get("client_secret", "")

    if not client_id or not client_secret:
        raise ValueError(f"Profile '{profile}' secret is missing client_id or client_secret")

    return client_id, client_secret
