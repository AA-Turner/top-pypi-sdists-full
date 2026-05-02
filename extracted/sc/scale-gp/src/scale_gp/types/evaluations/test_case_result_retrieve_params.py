# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Required, TypedDict

__all__ = ["TestCaseResultRetrieveParams"]


class TestCaseResultRetrieveParams(TypedDict, total=False):
    evaluation_id: Required[str]

    view: List[
        Literal["AnnotationResults", "AuditTasks", "CustomMetrics", "Metrics", "Task", "TestCaseVersion", "Trace"]
    ]
