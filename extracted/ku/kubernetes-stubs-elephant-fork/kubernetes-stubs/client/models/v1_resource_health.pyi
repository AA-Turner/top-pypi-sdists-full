import datetime
import typing

import kubernetes.client

class V1ResourceHealth:
    health: typing.Optional[str]
    resource_id: str
    
    def __init__(self, *, health: typing.Optional[str] = ..., resource_id: str) -> None:
        ...
    def to_dict(self) -> V1ResourceHealthDict:
        ...
class V1ResourceHealthDict(typing.TypedDict, total=False):
    health: typing.Optional[str]
    resourceID: str
