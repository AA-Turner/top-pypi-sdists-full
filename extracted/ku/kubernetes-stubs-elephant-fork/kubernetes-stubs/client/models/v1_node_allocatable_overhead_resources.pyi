import datetime
import typing

import kubernetes.client

class V1NodeAllocatableOverheadResources:
    name: str
    per_container: typing.Optional[str]
    per_pod: typing.Optional[str]
    
    def __init__(self, *, name: str, per_container: typing.Optional[str] = ..., per_pod: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1NodeAllocatableOverheadResourcesDict:
        ...
class V1NodeAllocatableOverheadResourcesDict(typing.TypedDict, total=False):
    name: str
    perContainer: typing.Optional[str]
    perPod: typing.Optional[str]
