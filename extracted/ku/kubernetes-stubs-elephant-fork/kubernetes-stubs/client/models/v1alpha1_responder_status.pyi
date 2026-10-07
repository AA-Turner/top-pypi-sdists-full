import datetime
import typing

import kubernetes.client

class V1alpha1ResponderStatus:
    completion_time: typing.Optional[datetime.datetime]
    expected_completion_time: typing.Optional[datetime.datetime]
    heartbeat_time: typing.Optional[datetime.datetime]
    message: typing.Optional[str]
    name: str
    start_time: typing.Optional[datetime.datetime]
    
    def __init__(self, *, completion_time: typing.Optional[datetime.datetime] = ..., expected_completion_time: typing.Optional[datetime.datetime] = ..., heartbeat_time: typing.Optional[datetime.datetime] = ..., message: typing.Optional[str] = ..., name: str, start_time: typing.Optional[datetime.datetime] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha1ResponderStatusDict:
        ...
class V1alpha1ResponderStatusDict(typing.TypedDict, total=False):
    completionTime: typing.Optional[datetime.datetime]
    expectedCompletionTime: typing.Optional[datetime.datetime]
    heartbeatTime: typing.Optional[datetime.datetime]
    message: typing.Optional[str]
    name: str
    startTime: typing.Optional[datetime.datetime]
