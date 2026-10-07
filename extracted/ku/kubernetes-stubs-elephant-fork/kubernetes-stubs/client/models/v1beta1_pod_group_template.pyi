import datetime
import typing

import kubernetes.client

class V1beta1PodGroupTemplate:
    disruption_mode: typing.Optional[kubernetes.client.V1beta1DisruptionMode]
    name: str
    preemption_policy: typing.Optional[str]
    priority: typing.Optional[int]
    priority_class_name: typing.Optional[str]
    resource_claims: typing.Optional[list[kubernetes.client.V1beta1PodGroupResourceClaim]]
    scheduling_constraints: typing.Optional[kubernetes.client.V1beta1PodGroupSchedulingConstraints]
    scheduling_policy: kubernetes.client.V1beta1PodGroupSchedulingPolicy
    
    def __init__(self, *, disruption_mode: typing.Optional[kubernetes.client.V1beta1DisruptionMode] = ..., name: str, preemption_policy: typing.Optional[str] = ..., priority: typing.Optional[int] = ..., priority_class_name: typing.Optional[str] = ..., resource_claims: typing.Optional[list[kubernetes.client.V1beta1PodGroupResourceClaim]] = ..., scheduling_constraints: typing.Optional[kubernetes.client.V1beta1PodGroupSchedulingConstraints] = ..., scheduling_policy: kubernetes.client.V1beta1PodGroupSchedulingPolicy) -> None:
        ...
    def to_dict(self) -> V1beta1PodGroupTemplateDict:
        ...
class V1beta1PodGroupTemplateDict(typing.TypedDict, total=False):
    disruptionMode: typing.Optional[kubernetes.client.V1beta1DisruptionModeDict]
    name: str
    preemptionPolicy: typing.Optional[str]
    priority: typing.Optional[int]
    priorityClassName: typing.Optional[str]
    resourceClaims: typing.Optional[list[kubernetes.client.V1beta1PodGroupResourceClaimDict]]
    schedulingConstraints: typing.Optional[kubernetes.client.V1beta1PodGroupSchedulingConstraintsDict]
    schedulingPolicy: kubernetes.client.V1beta1PodGroupSchedulingPolicyDict
