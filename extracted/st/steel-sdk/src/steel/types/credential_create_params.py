# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Required, Annotated, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo

__all__ = ["CredentialCreateParams"]


class CredentialCreateParams(TypedDict, total=False):
    value: Required[Dict[str, str]]
    """Value for the credential"""

    additional_origins: Annotated[SequenceNotStr[str], PropertyInfo(alias="additionalOrigins")]
    """
    Canonical http(s) origins, besides `origin`, this credential may be filled on,
    such as its login host or identity provider (e.g. `https://login.example.com`).
    Only the credential's origin and these ever match a page, exactly; at most 20.
    """

    label: str
    """Label for the credential"""

    namespace: str
    """The namespace the credential is stored against. Defaults to "default"."""

    origin: str
    """Website origin the credential is for"""

    project_id: Annotated[str, PropertyInfo(alias="projectId")]
    """Project to store the credential in."""
