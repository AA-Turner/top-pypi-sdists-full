"""DO NOT EDIT THIS FILE!

This file is automatically @generated by githubkit using the follow command:

bash ./scripts/run-codegen.sh

See https://github.com/github/rest-api-description for more information.
"""

from __future__ import annotations

from datetime import datetime
from typing import Literal
from typing_extensions import NotRequired, TypedDict


class RuleSuitesItemsType(TypedDict):
    """RuleSuitesItems"""

    id: NotRequired[int]
    actor_id: NotRequired[int]
    actor_name: NotRequired[str]
    before_sha: NotRequired[str]
    after_sha: NotRequired[str]
    ref: NotRequired[str]
    repository_id: NotRequired[int]
    repository_name: NotRequired[str]
    pushed_at: NotRequired[datetime]
    result: NotRequired[Literal["pass", "fail", "bypass"]]
    evaluation_result: NotRequired[Literal["pass", "fail", "bypass"]]


__all__ = ("RuleSuitesItemsType",)
