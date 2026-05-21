import datetime
import typing

import kubernetes.client

class V1beta2NodeAllocatableResourceMapping:
    allocation_multiplier: typing.Optional[str]
    capacity_key: typing.Optional[str]
    
    def __init__(self, *, allocation_multiplier: typing.Optional[str] = ..., capacity_key: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1beta2NodeAllocatableResourceMappingDict:
        ...
class V1beta2NodeAllocatableResourceMappingDict(typing.TypedDict, total=False):
    allocationMultiplier: typing.Optional[str]
    capacityKey: typing.Optional[str]
