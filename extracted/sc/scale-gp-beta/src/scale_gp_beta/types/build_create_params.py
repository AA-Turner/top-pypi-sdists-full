# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

from .._types import FileTypes

__all__ = ["BuildCreateParams"]


class BuildCreateParams(TypedDict, total=False):
    context_archive: Required[FileTypes]
    """
    tar.gz archive containing the build context (Dockerfile and any files needed for
    the build)
    """

    image_name: Required[str]
    """Name for the built image"""

    agent_id: str
    """ID of the existing agent this build targets"""

    agent_name: str
    """Name of the brand-new agent to create from this build"""

    build_args: str
    """JSON string of build arguments"""

    image_tag: str
    """Tag for the built image"""

    platform: Literal["linux/amd64", "linux/arm64", "linux/arm/v7"]
    """Target platform for the Docker build.

    Defaults to the build host's native architecture when not specified.
    """
