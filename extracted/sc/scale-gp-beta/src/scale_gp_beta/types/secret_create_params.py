# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["SecretCreateParams"]


class SecretCreateParams(TypedDict, total=False):
    key: Required[str]
    """Secret name (e.g.

    openai-api-key). Must be lowercase alphanumeric with hyphens (no dots or
    underscores), so it maps 1:1 to a valid secret name on every cloud backend (AWS
    / Azure Key Vault / GCP Secret Manager).
    """

    value: Required[str]
    """The secret value to store"""

    description: str
    """Optional human-readable description"""
