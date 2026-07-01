# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["DeploymentExecuteParams"]


class DeploymentExecuteParams(TypedDict, total=False):
    model_instance_id: Required[str]

    stream: bool
    """Flag indicating whether to stream the completion response"""
