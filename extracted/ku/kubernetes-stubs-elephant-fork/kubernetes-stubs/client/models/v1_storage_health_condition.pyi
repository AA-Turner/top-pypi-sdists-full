import datetime
import typing

import kubernetes.client

class V1StorageHealthCondition:
    access_mode: typing.Optional[str]
    last_transition_time: typing.Optional[datetime.datetime]
    message: typing.Optional[str]
    reason: str
    status: str
    volume_mode: typing.Optional[str]
    
    def __init__(self, *, access_mode: typing.Optional[str] = ..., last_transition_time: typing.Optional[datetime.datetime] = ..., message: typing.Optional[str] = ..., reason: str, status: str, volume_mode: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1StorageHealthConditionDict:
        ...
class V1StorageHealthConditionDict(typing.TypedDict, total=False):
    accessMode: typing.Optional[str]
    lastTransitionTime: typing.Optional[datetime.datetime]
    message: typing.Optional[str]
    reason: str
    status: str
    volumeMode: typing.Optional[str]
