import datetime
import typing

import kubernetes.client

class V1beta1CompositePodGroupTemplate:
    composite_pod_group_templates: typing.Optional[list[kubernetes.client.V1beta1CompositePodGroupTemplate]]
    disruption_mode: typing.Optional[kubernetes.client.V1beta1CompositeDisruptionMode]
    name: str
    pod_group_templates: typing.Optional[list[kubernetes.client.V1beta1PodGroupTemplate]]
    preemption_policy: typing.Optional[str]
    priority: typing.Optional[int]
    priority_class_name: typing.Optional[str]
    scheduling_constraints: typing.Optional[kubernetes.client.V1beta1CompositePodGroupSchedulingConstraints]
    scheduling_policy: kubernetes.client.V1beta1CompositePodGroupSchedulingPolicy
    
    def __init__(self, *, composite_pod_group_templates: typing.Optional[list[kubernetes.client.V1beta1CompositePodGroupTemplate]] = ..., disruption_mode: typing.Optional[kubernetes.client.V1beta1CompositeDisruptionMode] = ..., name: str, pod_group_templates: typing.Optional[list[kubernetes.client.V1beta1PodGroupTemplate]] = ..., preemption_policy: typing.Optional[str] = ..., priority: typing.Optional[int] = ..., priority_class_name: typing.Optional[str] = ..., scheduling_constraints: typing.Optional[kubernetes.client.V1beta1CompositePodGroupSchedulingConstraints] = ..., scheduling_policy: kubernetes.client.V1beta1CompositePodGroupSchedulingPolicy) -> None:
        ...
    def to_dict(self) -> V1beta1CompositePodGroupTemplateDict:
        ...
class V1beta1CompositePodGroupTemplateDict(typing.TypedDict, total=False):
    compositePodGroupTemplates: typing.Optional[list[kubernetes.client.V1beta1CompositePodGroupTemplateDict]]
    disruptionMode: typing.Optional[kubernetes.client.V1beta1CompositeDisruptionModeDict]
    name: str
    podGroupTemplates: typing.Optional[list[kubernetes.client.V1beta1PodGroupTemplateDict]]
    preemptionPolicy: typing.Optional[str]
    priority: typing.Optional[int]
    priorityClassName: typing.Optional[str]
    schedulingConstraints: typing.Optional[kubernetes.client.V1beta1CompositePodGroupSchedulingConstraintsDict]
    schedulingPolicy: kubernetes.client.V1beta1CompositePodGroupSchedulingPolicyDict
