# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable
from typing_extensions import Literal, Required, TypedDict

from ..._types import SequenceNotStr

__all__ = ["TestCaseResultBatchParams", "Item"]


class TestCaseResultBatchParams(TypedDict, total=False):
    items: Required[Iterable[Item]]


class Item(TypedDict, total=False):
    application_spec_id: Required[str]

    evaluation_dataset_version_num: Required[str]

    test_case_evaluation_data: Required[Dict[str, object]]

    test_case_id: Required[str]

    account_id: str

    annotated_by_identity_type: Literal["user", "service_account"]

    annotated_by_user_id: str

    audit_comment: str

    audit_required: bool

    audit_status: Literal["UNAUDITED", "FIXED", "APPROVED"]

    edited_by_identity_type: Literal["user", "service_account"]

    label_status: Literal["PENDING", "COMPLETED", "FAILED"]

    result: Dict[str, Union[str, bool, float, SequenceNotStr[Union[str, float, bool]]]]

    time_spent_labeling_s: int
