import datetime
import typing

import kubernetes.client

class V1beta1AllocationResult:
    allocation_timestamp: typing.Optional[datetime.datetime]
    devices: typing.Optional[kubernetes.client.V1beta1DeviceAllocationResult]
    node_selector: typing.Optional[kubernetes.client.V1NodeSelector]
    
    def __init__(self, *, allocation_timestamp: typing.Optional[datetime.datetime] = ..., devices: typing.Optional[kubernetes.client.V1beta1DeviceAllocationResult] = ..., node_selector: typing.Optional[kubernetes.client.V1NodeSelector] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1AllocationResultDict:
        ...
class V1beta1AllocationResultDict(typing.TypedDict, total=False):
    allocationTimestamp: typing.Optional[datetime.datetime]
    devices: typing.Optional[kubernetes.client.V1beta1DeviceAllocationResultDict]
    nodeSelector: typing.Optional[kubernetes.client.V1NodeSelectorDict]
