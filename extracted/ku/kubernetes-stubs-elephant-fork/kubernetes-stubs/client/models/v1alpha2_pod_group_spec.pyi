import datetime
import typing

import kubernetes.client

class V1alpha2PodGroupSpec:
    disruption_mode: typing.Optional[str]
    pod_group_template_ref: typing.Optional[kubernetes.client.V1alpha2PodGroupTemplateReference]
    priority: typing.Optional[int]
    priority_class_name: typing.Optional[str]
    resource_claims: typing.Optional[list[kubernetes.client.V1alpha2PodGroupResourceClaim]]
    scheduling_constraints: typing.Optional[kubernetes.client.V1alpha2PodGroupSchedulingConstraints]
    scheduling_policy: kubernetes.client.V1alpha2PodGroupSchedulingPolicy
    
    def __init__(self, *, disruption_mode: typing.Optional[str] = ..., pod_group_template_ref: typing.Optional[kubernetes.client.V1alpha2PodGroupTemplateReference] = ..., priority: typing.Optional[int] = ..., priority_class_name: typing.Optional[str] = ..., resource_claims: typing.Optional[list[kubernetes.client.V1alpha2PodGroupResourceClaim]] = ..., scheduling_constraints: typing.Optional[kubernetes.client.V1alpha2PodGroupSchedulingConstraints] = ..., scheduling_policy: kubernetes.client.V1alpha2PodGroupSchedulingPolicy) -> None:
        ...
    def to_dict(self) -> V1alpha2PodGroupSpecDict:
        ...
class V1alpha2PodGroupSpecDict(typing.TypedDict, total=False):
    disruptionMode: typing.Optional[str]
    podGroupTemplateRef: typing.Optional[kubernetes.client.V1alpha2PodGroupTemplateReferenceDict]
    priority: typing.Optional[int]
    priorityClassName: typing.Optional[str]
    resourceClaims: typing.Optional[list[kubernetes.client.V1alpha2PodGroupResourceClaimDict]]
    schedulingConstraints: typing.Optional[kubernetes.client.V1alpha2PodGroupSchedulingConstraintsDict]
    schedulingPolicy: kubernetes.client.V1alpha2PodGroupSchedulingPolicyDict
