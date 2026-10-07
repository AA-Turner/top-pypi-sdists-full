import datetime
import typing

import kubernetes.client

class V1NodeAllocatableOverhead:
    per_container: typing.Optional[str]
    per_pod: typing.Optional[str]
    
    def __init__(self, *, per_container: typing.Optional[str] = ..., per_pod: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1NodeAllocatableOverheadDict:
        ...
class V1NodeAllocatableOverheadDict(typing.TypedDict, total=False):
    perContainer: typing.Optional[str]
    perPod: typing.Optional[str]
