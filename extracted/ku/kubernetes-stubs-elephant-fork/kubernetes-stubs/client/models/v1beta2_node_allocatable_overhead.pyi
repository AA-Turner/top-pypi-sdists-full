import datetime
import typing

import kubernetes.client

class V1beta2NodeAllocatableOverhead:
    per_container: typing.Optional[str]
    per_pod: typing.Optional[str]
    
    def __init__(self, *, per_container: typing.Optional[str] = ..., per_pod: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1beta2NodeAllocatableOverheadDict:
        ...
class V1beta2NodeAllocatableOverheadDict(typing.TypedDict, total=False):
    perContainer: typing.Optional[str]
    perPod: typing.Optional[str]
