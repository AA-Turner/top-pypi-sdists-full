# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, TypedDict

__all__ = ["DeploymentListAllParams"]


class DeploymentListAllParams(TypedDict, total=False):
    account_id: str
    """Optional filter by account id"""

    limit: int
    """Maximum number of artifacts to be returned by the given endpoint.

    Defaults to 100 and cannot be greater than 10k.
    """

    page: int
    """Page number for pagination to be returned by the given endpoint.

    Starts at page 1
    """

    sort_by: List[
        Literal[
            "model_creation_parameters:asc",
            "model_creation_parameters:desc",
            "model_endpoint_id:asc",
            "model_endpoint_id:desc",
            "model_instance_id:asc",
            "model_instance_id:desc",
            "vendor_configuration:asc",
            "vendor_configuration:desc",
            "deployment_metadata:asc",
            "deployment_metadata:desc",
            "status:asc",
            "status:desc",
            "id:asc",
            "id:desc",
            "created_at:asc",
            "created_at:desc",
            "account_id:asc",
            "account_id:desc",
            "created_by_user_id:asc",
            "created_by_user_id:desc",
            "created_by_identity_type:asc",
            "created_by_identity_type:desc",
            "name:asc",
            "name:desc",
        ]
    ]
