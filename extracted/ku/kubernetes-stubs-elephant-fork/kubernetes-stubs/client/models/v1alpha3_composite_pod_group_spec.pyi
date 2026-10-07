import datetime
import typing

import kubernetes.client

class V1alpha3CompositePodGroupSpec:
    disruption_mode: typing.Optional[kubernetes.client.V1alpha3CompositeDisruptionMode]
    parent_composite_pod_group_name: typing.Optional[str]
    preemption_policy: typing.Optional[str]
    priority: typing.Optional[int]
    priority_class_name: typing.Optional[str]
    scheduling_constraints: typing.Optional[kubernetes.client.V1alpha3CompositePodGroupSchedulingConstraints]
    scheduling_policy: kubernetes.client.V1alpha3CompositePodGroupSchedulingPolicy
    workload_ref: kubernetes.client.V1alpha3WorkloadReference
    
    def __init__(self, *, disruption_mode: typing.Optional[kubernetes.client.V1alpha3CompositeDisruptionMode] = ..., parent_composite_pod_group_name: typing.Optional[str] = ..., preemption_policy: typing.Optional[str] = ..., priority: typing.Optional[int] = ..., priority_class_name: typing.Optional[str] = ..., scheduling_constraints: typing.Optional[kubernetes.client.V1alpha3CompositePodGroupSchedulingConstraints] = ..., scheduling_policy: kubernetes.client.V1alpha3CompositePodGroupSchedulingPolicy, workload_ref: kubernetes.client.V1alpha3WorkloadReference) -> None:
        ...
    def to_dict(self) -> V1alpha3CompositePodGroupSpecDict:
        ...
class V1alpha3CompositePodGroupSpecDict(typing.TypedDict, total=False):
    disruptionMode: typing.Optional[kubernetes.client.V1alpha3CompositeDisruptionModeDict]
    parentCompositePodGroupName: typing.Optional[str]
    preemptionPolicy: typing.Optional[str]
    priority: typing.Optional[int]
    priorityClassName: typing.Optional[str]
    schedulingConstraints: typing.Optional[kubernetes.client.V1alpha3CompositePodGroupSchedulingConstraintsDict]
    schedulingPolicy: kubernetes.client.V1alpha3CompositePodGroupSchedulingPolicyDict
    workloadRef: kubernetes.client.V1alpha3WorkloadReferenceDict
