import datetime
import typing

import kubernetes.client

class V1NodeAllocatableResource:
    mapping: typing.Optional[kubernetes.client.V1NodeAllocatableMapping]
    overhead: typing.Optional[kubernetes.client.V1NodeAllocatableOverhead]
    
    def __init__(self, *, mapping: typing.Optional[kubernetes.client.V1NodeAllocatableMapping] = ..., overhead: typing.Optional[kubernetes.client.V1NodeAllocatableOverhead] = ...) -> None:
        ...
    def to_dict(self) -> V1NodeAllocatableResourceDict:
        ...
class V1NodeAllocatableResourceDict(typing.TypedDict, total=False):
    mapping: typing.Optional[kubernetes.client.V1NodeAllocatableMappingDict]
    overhead: typing.Optional[kubernetes.client.V1NodeAllocatableOverheadDict]
