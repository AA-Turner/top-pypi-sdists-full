import datetime
import typing

import kubernetes.client

class V1beta1NodeAllocatableResource:
    mapping: typing.Optional[kubernetes.client.V1beta1NodeAllocatableMapping]
    overhead: typing.Optional[kubernetes.client.V1beta1NodeAllocatableOverhead]
    
    def __init__(self, *, mapping: typing.Optional[kubernetes.client.V1beta1NodeAllocatableMapping] = ..., overhead: typing.Optional[kubernetes.client.V1beta1NodeAllocatableOverhead] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1NodeAllocatableResourceDict:
        ...
class V1beta1NodeAllocatableResourceDict(typing.TypedDict, total=False):
    mapping: typing.Optional[kubernetes.client.V1beta1NodeAllocatableMappingDict]
    overhead: typing.Optional[kubernetes.client.V1beta1NodeAllocatableOverheadDict]
