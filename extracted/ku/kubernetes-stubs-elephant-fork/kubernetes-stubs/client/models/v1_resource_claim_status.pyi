import datetime
import typing

import kubernetes.client

class V1ResourceClaimStatus:
    allocation: typing.Optional[kubernetes.client.V1AllocationResult]
    devices: typing.Optional[list[kubernetes.client.V1AllocatedDeviceStatus]]
    reserved_for: typing.Optional[list[kubernetes.client.V1ResourceClaimConsumerReference]]
    
    def __init__(self, *, allocation: typing.Optional[kubernetes.client.V1AllocationResult] = ..., devices: typing.Optional[list[kubernetes.client.V1AllocatedDeviceStatus]] = ..., reserved_for: typing.Optional[list[kubernetes.client.V1ResourceClaimConsumerReference]] = ...) -> None:
        ...
    def to_dict(self) -> V1ResourceClaimStatusDict:
        ...
class V1ResourceClaimStatusDict(typing.TypedDict, total=False):
    allocation: typing.Optional[kubernetes.client.V1AllocationResultDict]
    devices: typing.Optional[list[kubernetes.client.V1AllocatedDeviceStatusDict]]
    reservedFor: typing.Optional[list[kubernetes.client.V1ResourceClaimConsumerReferenceDict]]
