# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Required, TypedDict

__all__ = ["CredentialCreateParams"]


class CredentialCreateParams(TypedDict, total=False):
    name: Required[str]
    """User-friendly name for the credential"""

    payload: Required[str]
    """The credential payload to be encrypted"""

    type: Required[str]
    """Type of credential: key or json"""

    credential_metadata: Dict[str, object]
    """Optional unencrypted credential_metadata"""

    description: str
    """Optional description"""
