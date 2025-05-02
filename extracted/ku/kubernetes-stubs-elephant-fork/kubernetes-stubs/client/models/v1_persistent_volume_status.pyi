import datetime
import typing

import kubernetes.client

class V1PersistentVolumeStatus:
    last_phase_transition_time: typing.Optional[datetime.datetime]
    message: typing.Optional[str]
    phase: typing.Optional[str]
    reason: typing.Optional[str]
    
    def __init__(self, *, last_phase_transition_time: typing.Optional[datetime.datetime] = ..., message: typing.Optional[str] = ..., phase: typing.Optional[str] = ..., reason: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1PersistentVolumeStatusDict:
        ...
class V1PersistentVolumeStatusDict(typing.TypedDict, total=False):
    lastPhaseTransitionTime: typing.Optional[datetime.datetime]
    message: typing.Optional[str]
    phase: typing.Optional[str]
    reason: typing.Optional[str]
