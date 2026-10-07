import datetime
import typing

import kubernetes.client

class V1beta2ResourceSliceSpec:
    all_nodes: typing.Optional[bool]
    devices: typing.Optional[list[kubernetes.client.V1beta2Device]]
    driver: str
    node_name: typing.Optional[str]
    node_selector: typing.Optional[kubernetes.client.V1NodeSelector]
    partition_type_attribute: typing.Optional[str]
    per_device_node_selection: typing.Optional[bool]
    pool: kubernetes.client.V1beta2ResourcePool
    shared_counters: typing.Optional[list[kubernetes.client.V1beta2CounterSet]]
    skip_node_operations: typing.Optional[list[str]]
    
    def __init__(self, *, all_nodes: typing.Optional[bool] = ..., devices: typing.Optional[list[kubernetes.client.V1beta2Device]] = ..., driver: str, node_name: typing.Optional[str] = ..., node_selector: typing.Optional[kubernetes.client.V1NodeSelector] = ..., partition_type_attribute: typing.Optional[str] = ..., per_device_node_selection: typing.Optional[bool] = ..., pool: kubernetes.client.V1beta2ResourcePool, shared_counters: typing.Optional[list[kubernetes.client.V1beta2CounterSet]] = ..., skip_node_operations: typing.Optional[list[str]] = ...) -> None:
        ...
    def to_dict(self) -> V1beta2ResourceSliceSpecDict:
        ...
class V1beta2ResourceSliceSpecDict(typing.TypedDict, total=False):
    allNodes: typing.Optional[bool]
    devices: typing.Optional[list[kubernetes.client.V1beta2DeviceDict]]
    driver: str
    nodeName: typing.Optional[str]
    nodeSelector: typing.Optional[kubernetes.client.V1NodeSelectorDict]
    partitionTypeAttribute: typing.Optional[str]
    perDeviceNodeSelection: typing.Optional[bool]
    pool: kubernetes.client.V1beta2ResourcePoolDict
    sharedCounters: typing.Optional[list[kubernetes.client.V1beta2CounterSetDict]]
    skipNodeOperations: typing.Optional[list[str]]
