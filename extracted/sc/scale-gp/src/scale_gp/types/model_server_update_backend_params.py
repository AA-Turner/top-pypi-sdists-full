# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["ModelServerUpdateBackendParams"]


class ModelServerUpdateBackendParams(TypedDict, total=False):
    new_model_deployment_id: Required[str]
