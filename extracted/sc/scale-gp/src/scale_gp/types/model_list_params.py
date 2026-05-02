# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from typing_extensions import Literal, TypedDict

__all__ = ["ModelListParams"]


class ModelListParams(TypedDict, total=False):
    account_id: str

    limit: int
    """Maximum number of artifacts to be returned by the given endpoint.

    Defaults to 100 and cannot be greater than 10k.
    """

    model_group_id: Union[int, str]

    model_type: Union[int, str]

    page: int
    """Page number for pagination to be returned by the given endpoint.

    Starts at page 1
    """

    sort_by: List[
        Literal[
            "display_name:asc",
            "display_name:desc",
            "model_vendor:asc",
            "model_vendor:desc",
            "base_model_id:asc",
            "base_model_id:desc",
            "base_model_metadata:asc",
            "base_model_metadata:desc",
            "model_creation_parameters:asc",
            "model_creation_parameters:desc",
            "model_card:asc",
            "model_card:desc",
            "training_data_card:asc",
            "training_data_card:desc",
            "description:asc",
            "description:desc",
            "model_template_id:asc",
            "model_template_id:desc",
            "model_group_id:asc",
            "model_group_id:desc",
            "model_group:asc",
            "model_group:desc",
            "request_schema:asc",
            "request_schema:desc",
            "response_schema:asc",
            "response_schema:desc",
            "deployment_count:asc",
            "deployment_count:desc",
            "supports_multi_turn:asc",
            "supports_multi_turn:desc",
            "deployments:asc",
            "deployments:desc",
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
            "model_type:asc",
            "model_type:desc",
        ]
    ]

    view: List[Literal["Deployments", "ModelGroup"]]
