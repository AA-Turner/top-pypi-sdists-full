import datetime
import typing

import kubernetes.client

class V1alpha3PodGroupTemplate:
    disruption_mode: typing.Optional[kubernetes.client.V1alpha3DisruptionMode]
    name: str
    preemption_policy: typing.Optional[str]
    priority: typing.Optional[int]
    priority_class_name: typing.Optional[str]
    resource_claims: typing.Optional[list[kubernetes.client.V1alpha3PodGroupResourceClaim]]
    scheduling_constraints: typing.Optional[kubernetes.client.V1alpha3PodGroupSchedulingConstraints]
    scheduling_policy: kubernetes.client.V1alpha3PodGroupSchedulingPolicy
    
    def __init__(self, *, disruption_mode: typing.Optional[kubernetes.client.V1alpha3DisruptionMode] = ..., name: str, preemption_policy: typing.Optional[str] = ..., priority: typing.Optional[int] = ..., priority_class_name: typing.Optional[str] = ..., resource_claims: typing.Optional[list[kubernetes.client.V1alpha3PodGroupResourceClaim]] = ..., scheduling_constraints: typing.Optional[kubernetes.client.V1alpha3PodGroupSchedulingConstraints] = ..., scheduling_policy: kubernetes.client.V1alpha3PodGroupSchedulingPolicy) -> None:
        ...
    def to_dict(self) -> V1alpha3PodGroupTemplateDict:
        ...
class V1alpha3PodGroupTemplateDict(typing.TypedDict, total=False):
    disruptionMode: typing.Optional[kubernetes.client.V1alpha3DisruptionModeDict]
    name: str
    preemptionPolicy: typing.Optional[str]
    priority: typing.Optional[int]
    priorityClassName: typing.Optional[str]
    resourceClaims: typing.Optional[list[kubernetes.client.V1alpha3PodGroupResourceClaimDict]]
    schedulingConstraints: typing.Optional[kubernetes.client.V1alpha3PodGroupSchedulingConstraintsDict]
    schedulingPolicy: kubernetes.client.V1alpha3PodGroupSchedulingPolicyDict
