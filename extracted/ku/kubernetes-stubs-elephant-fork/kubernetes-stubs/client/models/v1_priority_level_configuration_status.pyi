import datetime
import typing

import kubernetes.client

class V1PriorityLevelConfigurationStatus:
    conditions: typing.Optional[list[kubernetes.client.V1PriorityLevelConfigurationCondition]]
    
    def __init__(self, *, conditions: typing.Optional[list[kubernetes.client.V1PriorityLevelConfigurationCondition]] = ...) -> None:
        ...
    def to_dict(self) -> V1PriorityLevelConfigurationStatusDict:
        ...
class V1PriorityLevelConfigurationStatusDict(typing.TypedDict, total=False):
    conditions: typing.Optional[list[kubernetes.client.V1PriorityLevelConfigurationConditionDict]]
