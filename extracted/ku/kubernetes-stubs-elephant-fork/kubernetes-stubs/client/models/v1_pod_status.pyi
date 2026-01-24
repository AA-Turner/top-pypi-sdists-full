import datetime
import typing

import kubernetes.client

class V1PodStatus:
    allocated_resources: typing.Optional[dict[str, str]]
    conditions: typing.Optional[list[kubernetes.client.V1PodCondition]]
    container_statuses: typing.Optional[list[kubernetes.client.V1ContainerStatus]]
    ephemeral_container_statuses: typing.Optional[list[kubernetes.client.V1ContainerStatus]]
    extended_resource_claim_status: typing.Optional[kubernetes.client.V1PodExtendedResourceClaimStatus]
    host_ip: typing.Optional[str]
    host_i_ps: typing.Optional[list[kubernetes.client.V1HostIP]]
    init_container_statuses: typing.Optional[list[kubernetes.client.V1ContainerStatus]]
    message: typing.Optional[str]
    nominated_node_name: typing.Optional[str]
    observed_generation: typing.Optional[int]
    phase: typing.Optional[str]
    pod_ip: typing.Optional[str]
    pod_i_ps: typing.Optional[list[kubernetes.client.V1PodIP]]
    qos_class: typing.Optional[str]
    reason: typing.Optional[str]
    resize: typing.Optional[str]
    resource_claim_statuses: typing.Optional[list[kubernetes.client.V1PodResourceClaimStatus]]
    resources: typing.Optional[kubernetes.client.V1ResourceRequirements]
    start_time: typing.Optional[datetime.datetime]
    
    def __init__(self, *, allocated_resources: typing.Optional[dict[str, str]] = ..., conditions: typing.Optional[list[kubernetes.client.V1PodCondition]] = ..., container_statuses: typing.Optional[list[kubernetes.client.V1ContainerStatus]] = ..., ephemeral_container_statuses: typing.Optional[list[kubernetes.client.V1ContainerStatus]] = ..., extended_resource_claim_status: typing.Optional[kubernetes.client.V1PodExtendedResourceClaimStatus] = ..., host_ip: typing.Optional[str] = ..., host_i_ps: typing.Optional[list[kubernetes.client.V1HostIP]] = ..., init_container_statuses: typing.Optional[list[kubernetes.client.V1ContainerStatus]] = ..., message: typing.Optional[str] = ..., nominated_node_name: typing.Optional[str] = ..., observed_generation: typing.Optional[int] = ..., phase: typing.Optional[str] = ..., pod_ip: typing.Optional[str] = ..., pod_i_ps: typing.Optional[list[kubernetes.client.V1PodIP]] = ..., qos_class: typing.Optional[str] = ..., reason: typing.Optional[str] = ..., resize: typing.Optional[str] = ..., resource_claim_statuses: typing.Optional[list[kubernetes.client.V1PodResourceClaimStatus]] = ..., resources: typing.Optional[kubernetes.client.V1ResourceRequirements] = ..., start_time: typing.Optional[datetime.datetime] = ...) -> None:
        ...
    def to_dict(self) -> V1PodStatusDict:
        ...
class V1PodStatusDict(typing.TypedDict, total=False):
    allocatedResources: typing.Optional[dict[str, str]]
    conditions: typing.Optional[list[kubernetes.client.V1PodConditionDict]]
    containerStatuses: typing.Optional[list[kubernetes.client.V1ContainerStatusDict]]
    ephemeralContainerStatuses: typing.Optional[list[kubernetes.client.V1ContainerStatusDict]]
    extendedResourceClaimStatus: typing.Optional[kubernetes.client.V1PodExtendedResourceClaimStatusDict]
    hostIP: typing.Optional[str]
    hostIPs: typing.Optional[list[kubernetes.client.V1HostIPDict]]
    initContainerStatuses: typing.Optional[list[kubernetes.client.V1ContainerStatusDict]]
    message: typing.Optional[str]
    nominatedNodeName: typing.Optional[str]
    observedGeneration: typing.Optional[int]
    phase: typing.Optional[str]
    podIP: typing.Optional[str]
    podIPs: typing.Optional[list[kubernetes.client.V1PodIPDict]]
    qosClass: typing.Optional[str]
    reason: typing.Optional[str]
    resize: typing.Optional[str]
    resourceClaimStatuses: typing.Optional[list[kubernetes.client.V1PodResourceClaimStatusDict]]
    resources: typing.Optional[kubernetes.client.V1ResourceRequirementsDict]
    startTime: typing.Optional[datetime.datetime]
