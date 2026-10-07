import datetime
import typing

import kubernetes.client

class V1VolumeHealthStatus:
    health_conditions: typing.Optional[list[kubernetes.client.V1VolumeHealthCondition]]
    last_transition_time: typing.Optional[datetime.datetime]
    
    def __init__(self, *, health_conditions: typing.Optional[list[kubernetes.client.V1VolumeHealthCondition]] = ..., last_transition_time: typing.Optional[datetime.datetime] = ...) -> None:
        ...
    def to_dict(self) -> V1VolumeHealthStatusDict:
        ...
class V1VolumeHealthStatusDict(typing.TypedDict, total=False):
    healthConditions: typing.Optional[list[kubernetes.client.V1VolumeHealthConditionDict]]
    lastTransitionTime: typing.Optional[datetime.datetime]
