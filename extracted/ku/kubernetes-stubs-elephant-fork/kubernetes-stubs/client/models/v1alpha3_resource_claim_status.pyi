import datetime
import typing

import kubernetes.client

class V1alpha3ResourceClaimStatus:
    allocation: typing.Optional[kubernetes.client.V1alpha3AllocationResult]
    devices: typing.Optional[list[kubernetes.client.V1alpha3AllocatedDeviceStatus]]
    reserved_for: typing.Optional[list[kubernetes.client.V1alpha3ResourceClaimConsumerReference]]
    
    def __init__(self, *, allocation: typing.Optional[kubernetes.client.V1alpha3AllocationResult] = ..., devices: typing.Optional[list[kubernetes.client.V1alpha3AllocatedDeviceStatus]] = ..., reserved_for: typing.Optional[list[kubernetes.client.V1alpha3ResourceClaimConsumerReference]] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3ResourceClaimStatusDict:
        ...
class V1alpha3ResourceClaimStatusDict(typing.TypedDict, total=False):
    allocation: typing.Optional[kubernetes.client.V1alpha3AllocationResultDict]
    devices: typing.Optional[list[kubernetes.client.V1alpha3AllocatedDeviceStatusDict]]
    reservedFor: typing.Optional[list[kubernetes.client.V1alpha3ResourceClaimConsumerReferenceDict]]
