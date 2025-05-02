import datetime
import typing

import kubernetes.client

class V1FlowSchemaStatus:
    conditions: typing.Optional[list[kubernetes.client.V1FlowSchemaCondition]]
    
    def __init__(self, *, conditions: typing.Optional[list[kubernetes.client.V1FlowSchemaCondition]] = ...) -> None:
        ...
    def to_dict(self) -> V1FlowSchemaStatusDict:
        ...
class V1FlowSchemaStatusDict(typing.TypedDict, total=False):
    conditions: typing.Optional[list[kubernetes.client.V1FlowSchemaConditionDict]]
