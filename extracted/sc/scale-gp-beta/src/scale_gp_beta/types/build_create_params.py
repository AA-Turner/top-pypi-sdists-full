# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .._types import FileTypes

__all__ = ["BuildCreateParams"]


class BuildCreateParams(TypedDict, total=False):
    agent_name: Required[str]
    """Name of the agent that this build belongs to"""

    context_archive: Required[FileTypes]
    """
    tar.gz archive containing the build context (Dockerfile and any files needed for
    the build)
    """

    image_name: Required[str]
    """Name for the built image"""

    build_args: str
    """JSON string of build arguments"""

    image_tag: str
    """Tag for the built image"""
