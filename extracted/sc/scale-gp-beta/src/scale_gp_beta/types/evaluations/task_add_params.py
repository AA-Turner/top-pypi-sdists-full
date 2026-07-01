# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["TaskAddParams"]


class TaskAddParams(TypedDict, total=False):
    task: Required["EvaluationTaskParam"]
    """New test criteria to add to the evaluation.

    Rejected when contributor annotation tasks for this evaluation have already been
    claimed or completed. Triggers a rerun so the new task executes against existing
    items.
    """


from ..evaluation_task_param import EvaluationTaskParam
