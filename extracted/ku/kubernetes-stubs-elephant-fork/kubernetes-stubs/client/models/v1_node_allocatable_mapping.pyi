import datetime
import typing

import kubernetes.client

class V1NodeAllocatableMapping:
    capacity_key: typing.Optional[str]
    capacity_multiplier: typing.Optional[str]
    device_multiplier: typing.Optional[str]
    
    def __init__(self, *, capacity_key: typing.Optional[str] = ..., capacity_multiplier: typing.Optional[str] = ..., device_multiplier: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1NodeAllocatableMappingDict:
        ...
class V1NodeAllocatableMappingDict(typing.TypedDict, total=False):
    capacityKey: typing.Optional[str]
    capacityMultiplier: typing.Optional[str]
    deviceMultiplier: typing.Optional[str]
