import datetime
import typing

import kubernetes.client

class V1PodVolumeHealth:
    health_conditions: typing.Optional[list[kubernetes.client.V1VolumeHealthCondition]]
    last_transition_time: typing.Optional[datetime.datetime]
    name: str
    
    def __init__(self, *, health_conditions: typing.Optional[list[kubernetes.client.V1VolumeHealthCondition]] = ..., last_transition_time: typing.Optional[datetime.datetime] = ..., name: str) -> None:
        ...
    def to_dict(self) -> V1PodVolumeHealthDict:
        ...
class V1PodVolumeHealthDict(typing.TypedDict, total=False):
    healthConditions: typing.Optional[list[kubernetes.client.V1VolumeHealthConditionDict]]
    lastTransitionTime: typing.Optional[datetime.datetime]
    name: str
