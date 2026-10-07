import datetime
import typing

import kubernetes.client

class V1StorageHealth:
    health_conditions: typing.Optional[list[kubernetes.client.V1StorageHealthCondition]]
    name: str
    
    def __init__(self, *, health_conditions: typing.Optional[list[kubernetes.client.V1StorageHealthCondition]] = ..., name: str) -> None:
        ...
    def to_dict(self) -> V1StorageHealthDict:
        ...
class V1StorageHealthDict(typing.TypedDict, total=False):
    healthConditions: typing.Optional[list[kubernetes.client.V1StorageHealthConditionDict]]
    name: str
