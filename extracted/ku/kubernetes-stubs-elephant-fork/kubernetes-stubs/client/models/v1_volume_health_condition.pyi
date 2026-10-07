import datetime
import typing

import kubernetes.client

class V1VolumeHealthCondition:
    message: typing.Optional[str]
    reason: str
    status: str
    
    def __init__(self, *, message: typing.Optional[str] = ..., reason: str, status: str) -> None:
        ...
    def to_dict(self) -> V1VolumeHealthConditionDict:
        ...
class V1VolumeHealthConditionDict(typing.TypedDict, total=False):
    message: typing.Optional[str]
    reason: str
    status: str
