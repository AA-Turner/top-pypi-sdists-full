import datetime
import typing

import kubernetes.client

class V1beta1PodGroupSpec:
    disruption_mode: typing.Optional[kubernetes.client.V1beta1DisruptionMode]
    parent_composite_pod_group_name: typing.Optional[str]
    preemption_policy: typing.Optional[str]
    priority: typing.Optional[int]
    priority_class_name: typing.Optional[str]
    resource_claims: typing.Optional[list[kubernetes.client.V1beta1PodGroupResourceClaim]]
    scheduling_constraints: typing.Optional[kubernetes.client.V1beta1PodGroupSchedulingConstraints]
    scheduling_policy: kubernetes.client.V1beta1PodGroupSchedulingPolicy
    workload_ref: typing.Optional[kubernetes.client.V1beta1WorkloadReference]
    
    def __init__(self, *, disruption_mode: typing.Optional[kubernetes.client.V1beta1DisruptionMode] = ..., parent_composite_pod_group_name: typing.Optional[str] = ..., preemption_policy: typing.Optional[str] = ..., priority: typing.Optional[int] = ..., priority_class_name: typing.Optional[str] = ..., resource_claims: typing.Optional[list[kubernetes.client.V1beta1PodGroupResourceClaim]] = ..., scheduling_constraints: typing.Optional[kubernetes.client.V1beta1PodGroupSchedulingConstraints] = ..., scheduling_policy: kubernetes.client.V1beta1PodGroupSchedulingPolicy, workload_ref: typing.Optional[kubernetes.client.V1beta1WorkloadReference] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1PodGroupSpecDict:
        ...
class V1beta1PodGroupSpecDict(typing.TypedDict, total=False):
    disruptionMode: typing.Optional[kubernetes.client.V1beta1DisruptionModeDict]
    parentCompositePodGroupName: typing.Optional[str]
    preemptionPolicy: typing.Optional[str]
    priority: typing.Optional[int]
    priorityClassName: typing.Optional[str]
    resourceClaims: typing.Optional[list[kubernetes.client.V1beta1PodGroupResourceClaimDict]]
    schedulingConstraints: typing.Optional[kubernetes.client.V1beta1PodGroupSchedulingConstraintsDict]
    schedulingPolicy: kubernetes.client.V1beta1PodGroupSchedulingPolicyDict
    workloadRef: typing.Optional[kubernetes.client.V1beta1WorkloadReferenceDict]
