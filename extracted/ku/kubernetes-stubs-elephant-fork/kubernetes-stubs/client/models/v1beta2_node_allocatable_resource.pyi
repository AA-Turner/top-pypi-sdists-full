import datetime
import typing

import kubernetes.client

class V1beta2NodeAllocatableResource:
    mapping: typing.Optional[kubernetes.client.V1beta2NodeAllocatableMapping]
    overhead: typing.Optional[kubernetes.client.V1beta2NodeAllocatableOverhead]
    
    def __init__(self, *, mapping: typing.Optional[kubernetes.client.V1beta2NodeAllocatableMapping] = ..., overhead: typing.Optional[kubernetes.client.V1beta2NodeAllocatableOverhead] = ...) -> None:
        ...
    def to_dict(self) -> V1beta2NodeAllocatableResourceDict:
        ...
class V1beta2NodeAllocatableResourceDict(typing.TypedDict, total=False):
    mapping: typing.Optional[kubernetes.client.V1beta2NodeAllocatableMappingDict]
    overhead: typing.Optional[kubernetes.client.V1beta2NodeAllocatableOverheadDict]
