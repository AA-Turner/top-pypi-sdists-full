import datetime
import typing

import kubernetes.client

class V1ResourceStatus:
    name: str
    resources: typing.Optional[list[kubernetes.client.V1ResourceHealth]]
    
    def __init__(self, *, name: str, resources: typing.Optional[list[kubernetes.client.V1ResourceHealth]] = ...) -> None:
        ...
    def to_dict(self) -> V1ResourceStatusDict:
        ...
class V1ResourceStatusDict(typing.TypedDict, total=False):
    name: str
    resources: typing.Optional[list[kubernetes.client.V1ResourceHealthDict]]
