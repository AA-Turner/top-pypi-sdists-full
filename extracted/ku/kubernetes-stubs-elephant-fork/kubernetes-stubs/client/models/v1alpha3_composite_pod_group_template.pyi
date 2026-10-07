import datetime
import typing

import kubernetes.client

class V1alpha3CompositePodGroupTemplate:
    composite_pod_group_templates: typing.Optional[list[kubernetes.client.V1alpha3CompositePodGroupTemplate]]
    disruption_mode: typing.Optional[kubernetes.client.V1alpha3CompositeDisruptionMode]
    name: str
    pod_group_templates: typing.Optional[list[kubernetes.client.V1alpha3PodGroupTemplate]]
    preemption_policy: typing.Optional[str]
    priority: typing.Optional[int]
    priority_class_name: typing.Optional[str]
    scheduling_constraints: typing.Optional[kubernetes.client.V1alpha3CompositePodGroupSchedulingConstraints]
    scheduling_policy: kubernetes.client.V1alpha3CompositePodGroupSchedulingPolicy
    
    def __init__(self, *, composite_pod_group_templates: typing.Optional[list[kubernetes.client.V1alpha3CompositePodGroupTemplate]] = ..., disruption_mode: typing.Optional[kubernetes.client.V1alpha3CompositeDisruptionMode] = ..., name: str, pod_group_templates: typing.Optional[list[kubernetes.client.V1alpha3PodGroupTemplate]] = ..., preemption_policy: typing.Optional[str] = ..., priority: typing.Optional[int] = ..., priority_class_name: typing.Optional[str] = ..., scheduling_constraints: typing.Optional[kubernetes.client.V1alpha3CompositePodGroupSchedulingConstraints] = ..., scheduling_policy: kubernetes.client.V1alpha3CompositePodGroupSchedulingPolicy) -> None:
        ...
    def to_dict(self) -> V1alpha3CompositePodGroupTemplateDict:
        ...
class V1alpha3CompositePodGroupTemplateDict(typing.TypedDict, total=False):
    compositePodGroupTemplates: typing.Optional[list[kubernetes.client.V1alpha3CompositePodGroupTemplateDict]]
    disruptionMode: typing.Optional[kubernetes.client.V1alpha3CompositeDisruptionModeDict]
    name: str
    podGroupTemplates: typing.Optional[list[kubernetes.client.V1alpha3PodGroupTemplateDict]]
    preemptionPolicy: typing.Optional[str]
    priority: typing.Optional[int]
    priorityClassName: typing.Optional[str]
    schedulingConstraints: typing.Optional[kubernetes.client.V1alpha3CompositePodGroupSchedulingConstraintsDict]
    schedulingPolicy: kubernetes.client.V1alpha3CompositePodGroupSchedulingPolicyDict
