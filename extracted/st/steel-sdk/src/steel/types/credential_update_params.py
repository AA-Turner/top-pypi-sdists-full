# File generated from our OpenAPI spec. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Annotated, TypedDict

from .._types import SequenceNotStr
from .._utils import PropertyInfo

__all__ = ["CredentialUpdateParams"]


class CredentialUpdateParams(TypedDict, total=False):
    additional_origins: Annotated[SequenceNotStr[str], PropertyInfo(alias="additionalOrigins")]
    """
    Canonical http(s) origins, besides `origin`, this credential may be filled on,
    such as its login host or identity provider (e.g. `https://login.example.com`).
    Only the credential's origin and these ever match a page, exactly; at most 20.
    Replaces the current list; [] clears it.
    """

    label: str
    """Label for the credential"""

    namespace: str
    """The namespace the credential is stored against. Defaults to "default"."""

    origin: str
    """Website origin the credential is for"""

    project_id: Annotated[str, PropertyInfo(alias="projectId")]
    """Project to update the credential in."""

    value: Dict[str, str]
    """Value for the credential"""
