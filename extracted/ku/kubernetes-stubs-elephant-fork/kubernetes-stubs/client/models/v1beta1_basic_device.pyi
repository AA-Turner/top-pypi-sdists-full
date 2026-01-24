import datetime
import typing

import kubernetes.client

class V1beta1BasicDevice:
    all_nodes: typing.Optional[bool]
    allow_multiple_allocations: typing.Optional[bool]
    attributes: typing.Optional[dict[str, kubernetes.client.V1beta1DeviceAttribute]]
    binding_conditions: typing.Optional[list[str]]
    binding_failure_conditions: typing.Optional[list[str]]
    binds_to_node: typing.Optional[bool]
    capacity: typing.Optional[dict[str, kubernetes.client.V1beta1DeviceCapacity]]
    consumes_counters: typing.Optional[list[kubernetes.client.V1beta1DeviceCounterConsumption]]
    node_name: typing.Optional[str]
    node_selector: typing.Optional[kubernetes.client.V1NodeSelector]
    taints: typing.Optional[list[kubernetes.client.V1beta1DeviceTaint]]
    
    def __init__(self, *, all_nodes: typing.Optional[bool] = ..., allow_multiple_allocations: typing.Optional[bool] = ..., attributes: typing.Optional[dict[str, kubernetes.client.V1beta1DeviceAttribute]] = ..., binding_conditions: typing.Optional[list[str]] = ..., binding_failure_conditions: typing.Optional[list[str]] = ..., binds_to_node: typing.Optional[bool] = ..., capacity: typing.Optional[dict[str, kubernetes.client.V1beta1DeviceCapacity]] = ..., consumes_counters: typing.Optional[list[kubernetes.client.V1beta1DeviceCounterConsumption]] = ..., node_name: typing.Optional[str] = ..., node_selector: typing.Optional[kubernetes.client.V1NodeSelector] = ..., taints: typing.Optional[list[kubernetes.client.V1beta1DeviceTaint]] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1BasicDeviceDict:
        ...
class V1beta1BasicDeviceDict(typing.TypedDict, total=False):
    allNodes: typing.Optional[bool]
    allowMultipleAllocations: typing.Optional[bool]
    attributes: typing.Optional[dict[str, kubernetes.client.V1beta1DeviceAttributeDict]]
    bindingConditions: typing.Optional[list[str]]
    bindingFailureConditions: typing.Optional[list[str]]
    bindsToNode: typing.Optional[bool]
    capacity: typing.Optional[dict[str, kubernetes.client.V1beta1DeviceCapacityDict]]
    consumesCounters: typing.Optional[list[kubernetes.client.V1beta1DeviceCounterConsumptionDict]]
    nodeName: typing.Optional[str]
    nodeSelector: typing.Optional[kubernetes.client.V1NodeSelectorDict]
    taints: typing.Optional[list[kubernetes.client.V1beta1DeviceTaintDict]]
