import datetime
import typing

import kubernetes.client

class V1alpha3PodGroupSpec:
    disruption_mode: typing.Optional[kubernetes.client.V1alpha3DisruptionMode]
    parent_composite_pod_group_name: typing.Optional[str]
    preemption_policy: typing.Optional[str]
    priority: typing.Optional[int]
    priority_class_name: typing.Optional[str]
    resource_claims: typing.Optional[list[kubernetes.client.V1alpha3PodGroupResourceClaim]]
    scheduling_constraints: typing.Optional[kubernetes.client.V1alpha3PodGroupSchedulingConstraints]
    scheduling_policy: kubernetes.client.V1alpha3PodGroupSchedulingPolicy
    workload_ref: typing.Optional[kubernetes.client.V1alpha3WorkloadReference]
    
    def __init__(self, *, disruption_mode: typing.Optional[kubernetes.client.V1alpha3DisruptionMode] = ..., parent_composite_pod_group_name: typing.Optional[str] = ..., preemption_policy: typing.Optional[str] = ..., priority: typing.Optional[int] = ..., priority_class_name: typing.Optional[str] = ..., resource_claims: typing.Optional[list[kubernetes.client.V1alpha3PodGroupResourceClaim]] = ..., scheduling_constraints: typing.Optional[kubernetes.client.V1alpha3PodGroupSchedulingConstraints] = ..., scheduling_policy: kubernetes.client.V1alpha3PodGroupSchedulingPolicy, workload_ref: typing.Optional[kubernetes.client.V1alpha3WorkloadReference] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3PodGroupSpecDict:
        ...
class V1alpha3PodGroupSpecDict(typing.TypedDict, total=False):
    disruptionMode: typing.Optional[kubernetes.client.V1alpha3DisruptionModeDict]
    parentCompositePodGroupName: typing.Optional[str]
    preemptionPolicy: typing.Optional[str]
    priority: typing.Optional[int]
    priorityClassName: typing.Optional[str]
    resourceClaims: typing.Optional[list[kubernetes.client.V1alpha3PodGroupResourceClaimDict]]
    schedulingConstraints: typing.Optional[kubernetes.client.V1alpha3PodGroupSchedulingConstraintsDict]
    schedulingPolicy: kubernetes.client.V1alpha3PodGroupSchedulingPolicyDict
    workloadRef: typing.Optional[kubernetes.client.V1alpha3WorkloadReferenceDict]
