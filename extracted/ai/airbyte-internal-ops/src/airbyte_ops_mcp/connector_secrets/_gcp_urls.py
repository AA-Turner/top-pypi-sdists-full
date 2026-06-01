# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""URL and name helpers for GSM secrets.

Kept in a separate module so that both `exceptions` and `gsm` can import them
without a circular dependency. Named with a `_gcp_` prefix to leave room for
future per-backend helpers (e.g. 1Password) alongside these.
"""

from __future__ import annotations


def extract_gcp_secret_name(secret_name: str) -> str:
    """Return the bare secret name, stripping any `projects/.../secrets/` prefix.

    Handles both fully-qualified paths (`projects/<id>/secrets/<name>`) and
    bare names.
    """
    if "/secrets/" in secret_name:
        return secret_name.split("/secrets/")[-1]
    return secret_name


def get_gcp_secret_url(secret_name: str, gcp_project_id: str) -> str:
    """Return the GCP console URL for a secret.

    The URL itself contains no sensitive data and is safe to log; it only
    resolves for users who can already authenticate to the project.
    """
    secret_name = extract_gcp_secret_name(secret_name)
    return (
        "https://console.cloud.google.com/security/secret-manager/secret/"
        f"{secret_name}/versions?hl=en&project={gcp_project_id}"
    )
