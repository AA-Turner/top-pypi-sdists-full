# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import TypedDict

__all__ = ["CredentialUpdateParams"]


class CredentialUpdateParams(TypedDict, total=False):
    credential_metadata: Dict[str, object]
    """Optional unencrypted credential_metadata"""

    description: str
    """Optional description"""

    name: str
    """User-friendly name for the credential"""

    payload: str
    """The credential payload to be encrypted"""

    type: str
    """Type of credential: key or json"""
