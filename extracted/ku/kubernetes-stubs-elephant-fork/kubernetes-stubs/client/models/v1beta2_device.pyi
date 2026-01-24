import datetime
import typing

import kubernetes.client

class V1beta2Device:
    all_nodes: typing.Optional[bool]
    allow_multiple_allocations: typing.Optional[bool]
    attributes: typing.Optional[dict[str, kubernetes.client.V1beta2DeviceAttribute]]
    binding_conditions: typing.Optional[list[str]]
    binding_failure_conditions: typing.Optional[list[str]]
    binds_to_node: typing.Optional[bool]
    capacity: typing.Optional[dict[str, kubernetes.client.V1beta2DeviceCapacity]]
    consumes_counters: typing.Optional[list[kubernetes.client.V1beta2DeviceCounterConsumption]]
    name: str
    node_name: typing.Optional[str]
    node_selector: typing.Optional[kubernetes.client.V1NodeSelector]
    taints: typing.Optional[list[kubernetes.client.V1beta2DeviceTaint]]
    
    def __init__(self, *, all_nodes: typing.Optional[bool] = ..., allow_multiple_allocations: typing.Optional[bool] = ..., attributes: typing.Optional[dict[str, kubernetes.client.V1beta2DeviceAttribute]] = ..., binding_conditions: typing.Optional[list[str]] = ..., binding_failure_conditions: typing.Optional[list[str]] = ..., binds_to_node: typing.Optional[bool] = ..., capacity: typing.Optional[dict[str, kubernetes.client.V1beta2DeviceCapacity]] = ..., consumes_counters: typing.Optional[list[kubernetes.client.V1beta2DeviceCounterConsumption]] = ..., name: str, node_name: typing.Optional[str] = ..., node_selector: typing.Optional[kubernetes.client.V1NodeSelector] = ..., taints: typing.Optional[list[kubernetes.client.V1beta2DeviceTaint]] = ...) -> None:
        ...
    def to_dict(self) -> V1beta2DeviceDict:
        ...
class V1beta2DeviceDict(typing.TypedDict, total=False):
    allNodes: typing.Optional[bool]
    allowMultipleAllocations: typing.Optional[bool]
    attributes: typing.Optional[dict[str, kubernetes.client.V1beta2DeviceAttributeDict]]
    bindingConditions: typing.Optional[list[str]]
    bindingFailureConditions: typing.Optional[list[str]]
    bindsToNode: typing.Optional[bool]
    capacity: typing.Optional[dict[str, kubernetes.client.V1beta2DeviceCapacityDict]]
    consumesCounters: typing.Optional[list[kubernetes.client.V1beta2DeviceCounterConsumptionDict]]
    name: str
    nodeName: typing.Optional[str]
    nodeSelector: typing.Optional[kubernetes.client.V1NodeSelectorDict]
    taints: typing.Optional[list[kubernetes.client.V1beta2DeviceTaintDict]]
