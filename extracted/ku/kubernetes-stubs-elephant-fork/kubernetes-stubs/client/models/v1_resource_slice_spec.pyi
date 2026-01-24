import datetime
import typing

import kubernetes.client

class V1ResourceSliceSpec:
    all_nodes: typing.Optional[bool]
    devices: typing.Optional[list[kubernetes.client.V1Device]]
    driver: str
    node_name: typing.Optional[str]
    node_selector: typing.Optional[kubernetes.client.V1NodeSelector]
    per_device_node_selection: typing.Optional[bool]
    pool: kubernetes.client.V1ResourcePool
    shared_counters: typing.Optional[list[kubernetes.client.V1CounterSet]]
    
    def __init__(self, *, all_nodes: typing.Optional[bool] = ..., devices: typing.Optional[list[kubernetes.client.V1Device]] = ..., driver: str, node_name: typing.Optional[str] = ..., node_selector: typing.Optional[kubernetes.client.V1NodeSelector] = ..., per_device_node_selection: typing.Optional[bool] = ..., pool: kubernetes.client.V1ResourcePool, shared_counters: typing.Optional[list[kubernetes.client.V1CounterSet]] = ...) -> None:
        ...
    def to_dict(self) -> V1ResourceSliceSpecDict:
        ...
class V1ResourceSliceSpecDict(typing.TypedDict, total=False):
    allNodes: typing.Optional[bool]
    devices: typing.Optional[list[kubernetes.client.V1DeviceDict]]
    driver: str
    nodeName: typing.Optional[str]
    nodeSelector: typing.Optional[kubernetes.client.V1NodeSelectorDict]
    perDeviceNodeSelection: typing.Optional[bool]
    pool: kubernetes.client.V1ResourcePoolDict
    sharedCounters: typing.Optional[list[kubernetes.client.V1CounterSetDict]]
