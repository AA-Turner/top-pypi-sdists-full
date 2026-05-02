# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from typing_extensions import Literal, TypedDict

__all__ = ["EvaluationListParams"]


class EvaluationListParams(TypedDict, total=False):
    account_id: str

    application_spec_id: Union[int, str]

    include_archived: bool

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
            "status:asc",
            "status:desc",
            "application_spec_id:asc",
            "application_spec_id:desc",
            "application_spec:asc",
            "application_spec:desc",
            "application_variant_id:asc",
            "application_variant_id:desc",
            "application_variant:asc",
            "application_variant:desc",
            "evaluation_config_id:asc",
            "evaluation_config_id:desc",
            "completed_at:asc",
            "completed_at:desc",
            "total_test_case_result_count:asc",
            "total_test_case_result_count:desc",
            "completed_test_case_result_count:asc",
            "completed_test_case_result_count:desc",
            "annotation_config:asc",
            "annotation_config:desc",
            "question_id_to_annotation_config:asc",
            "question_id_to_annotation_config:desc",
            "metric_config:asc",
            "metric_config:desc",
            "evaluation_config_expanded:asc",
            "evaluation_config_expanded:desc",
            "test_case_results:asc",
            "test_case_results:desc",
            "async_jobs:asc",
            "async_jobs:desc",
            "evaluation_datasets:asc",
            "evaluation_datasets:desc",
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
            "archived_at:asc",
            "archived_at:desc",
            "name:asc",
            "name:desc",
            "description:asc",
            "description:desc",
            "tags:asc",
            "tags:desc",
            "evaluation_config:asc",
            "evaluation_config:desc",
        ]
    ]

    view: List[Literal["ApplicationSpec", "AsyncJobs", "EvaluationConfig", "EvaluationDatasets"]]
