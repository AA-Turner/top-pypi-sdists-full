import datetime
import typing

import kubernetes.client

class V1alpha3PoolStatus:
    allocated_devices: typing.Optional[int]
    available_devices: typing.Optional[int]
    driver: str
    generation: int
    node_name: typing.Optional[str]
    partition_summary: typing.Optional[list[kubernetes.client.V1alpha3PartitionTypeStatus]]
    pool_name: str
    resource_slice_count: typing.Optional[int]
    shareable_summary: typing.Optional[kubernetes.client.V1alpha3ShareableSummaryStatus]
    total_devices: typing.Optional[int]
    unavailable_devices: typing.Optional[int]
    validation_error: typing.Optional[str]
    
    def __init__(self, *, allocated_devices: typing.Optional[int] = ..., available_devices: typing.Optional[int] = ..., driver: str, generation: int, node_name: typing.Optional[str] = ..., partition_summary: typing.Optional[list[kubernetes.client.V1alpha3PartitionTypeStatus]] = ..., pool_name: str, resource_slice_count: typing.Optional[int] = ..., shareable_summary: typing.Optional[kubernetes.client.V1alpha3ShareableSummaryStatus] = ..., total_devices: typing.Optional[int] = ..., unavailable_devices: typing.Optional[int] = ..., validation_error: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3PoolStatusDict:
        ...
class V1alpha3PoolStatusDict(typing.TypedDict, total=False):
    allocatedDevices: typing.Optional[int]
    availableDevices: typing.Optional[int]
    driver: str
    generation: int
    nodeName: typing.Optional[str]
    partitionSummary: typing.Optional[list[kubernetes.client.V1alpha3PartitionTypeStatusDict]]
    poolName: str
    resourceSliceCount: typing.Optional[int]
    shareableSummary: typing.Optional[kubernetes.client.V1alpha3ShareableSummaryStatusDict]
    totalDevices: typing.Optional[int]
    unavailableDevices: typing.Optional[int]
    validationError: typing.Optional[str]
