from typing import Any, List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict

from ..types import Credit, Quota

TASK_TYPE_MAP = {
    str: "text",
    bool: "bool",
    int: "int",
    float: "double",
    bytes: "bytes",
    dict: "json",
}


class Key(BaseModel):
    fqdn: str
    type: str


class Value(BaseModel):
    type: str
    value: Any
    modified: Optional[int] = None


class Attributes(BaseModel):
    data: List[Union[Key, Value]]


class TaskStreamText(BaseModel):
    content: str


class TaskStreamQuotaMetaData(BaseModel):
    updated: Quota
    spent: Credit


class TaskStreamExecutionMetadata(BaseModel):
    attributes: Attributes


class TaskStreamFinishMetadata(BaseModel):
    reason: Literal["stop", "length", "function_call", "tool_call", "unknown"]


class TaskStreamUnknownMetadata(BaseModel):
    """
    Open model that can contain any arbitrary metadata fields
    """

    model_config = ConfigDict(extra="allow")


class TaskStreamFunctionCallMetadata(BaseModel):
    name: Optional[str] = None
    content: str


TaskStreamData = Union[
    TaskStreamText,
    TaskStreamQuotaMetaData,
    TaskStreamExecutionMetadata,
    TaskStreamFinishMetadata,
    TaskStreamUnknownMetadata,
    TaskStreamFunctionCallMetadata,
]


class TaskCallResponse(BaseModel):
    content: str
    quota_metadata: Optional[TaskStreamQuotaMetaData] = None
    execution_metadata: List[TaskStreamExecutionMetadata] = []
    finish_metadata: Optional[TaskStreamFinishMetadata] = None
    unknown_metadata: Optional[TaskStreamUnknownMetadata] = None
    function_call_metadata: Optional[TaskStreamFunctionCallMetadata] = None


class TaskRoster(BaseModel):
    ids: List[str]
