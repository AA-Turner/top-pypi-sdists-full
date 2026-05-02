from typing import Literal

from workflow_server.core.type_checker.base import WorkflowTypeChecker
from workflow_server.core.type_checker.mypy import MypyWorkflowTypeChecker
from workflow_server.core.type_checker.zuban import ZubanWorkflowTypeChecker

__all__ = ["get_checker"]


def get_checker(
    type_checker: Literal["zuban", "mypy"] = "zuban",
) -> WorkflowTypeChecker:
    if type_checker == "zuban":
        return ZubanWorkflowTypeChecker()
    elif type_checker == "mypy":
        return MypyWorkflowTypeChecker()
    else:
        raise NotImplementedError(f"Unsupported type checker: {type_checker}")
