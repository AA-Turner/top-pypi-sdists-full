# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["DeployCreateParams"]


class DeployCreateParams(TypedDict, total=False):
    environment_config: Required[str]

    manifest_file: Required[str]

    build_id: str
    """The build_id of the cloud build.

    Required if image_name and image_tag are not provided.
    """

    image_name: str
    """Name of the image to deploy. Required if build_id is not provided."""

    image_tag: str
    """Tag of the image to deploy. Required if build_id is not provided."""

    preview: bool
    """
    When True, creates a preview deployment with a unique slug appended to the helm
    release name.
    """
