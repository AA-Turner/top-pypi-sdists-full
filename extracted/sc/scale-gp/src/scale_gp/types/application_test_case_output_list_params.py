# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from typing_extensions import Literal, TypedDict

__all__ = ["ApplicationTestCaseOutputListParams"]


class ApplicationTestCaseOutputListParams(TypedDict, total=False):
    account_id: str

    application_test_case_output_group_id: Union[int, str]

    application_variant_id: Union[int, str]

    application_variant_report_id: Union[int, str]

    evaluation_dataset_id: Union[int, str]

    evaluation_dataset_version_num: Union[int, str]

    limit: int
    """Maximum number of artifacts to be returned by the given endpoint.

    Defaults to 100 and cannot be greater than 10k.
    """

    page: int
    """Page number for pagination to be returned by the given endpoint.

    Starts at page 1
    """

    view: List[Literal["MetricScores", "TestCaseVersion", "Trace"]]
