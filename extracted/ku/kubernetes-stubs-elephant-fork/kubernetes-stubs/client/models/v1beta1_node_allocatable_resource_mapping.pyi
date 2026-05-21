import datetime
import typing

import kubernetes.client

class V1beta1NodeAllocatableResourceMapping:
    allocation_multiplier: typing.Optional[str]
    capacity_key: typing.Optional[str]
    
    def __init__(self, *, allocation_multiplier: typing.Optional[str] = ..., capacity_key: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1NodeAllocatableResourceMappingDict:
        ...
class V1beta1NodeAllocatableResourceMappingDict(typing.TypedDict, total=False):
    allocationMultiplier: typing.Optional[str]
    capacityKey: typing.Optional[str]
