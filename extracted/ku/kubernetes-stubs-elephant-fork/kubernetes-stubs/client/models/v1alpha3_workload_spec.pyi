import datetime
import typing

import kubernetes.client

class V1alpha3WorkloadSpec:
    composite_pod_group_templates: typing.Optional[list[kubernetes.client.V1alpha3CompositePodGroupTemplate]]
    controller_ref: typing.Optional[kubernetes.client.V1alpha3TypedLocalObjectReference]
    pod_group_templates: typing.Optional[list[kubernetes.client.V1alpha3PodGroupTemplate]]
    
    def __init__(self, *, composite_pod_group_templates: typing.Optional[list[kubernetes.client.V1alpha3CompositePodGroupTemplate]] = ..., controller_ref: typing.Optional[kubernetes.client.V1alpha3TypedLocalObjectReference] = ..., pod_group_templates: typing.Optional[list[kubernetes.client.V1alpha3PodGroupTemplate]] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3WorkloadSpecDict:
        ...
class V1alpha3WorkloadSpecDict(typing.TypedDict, total=False):
    compositePodGroupTemplates: typing.Optional[list[kubernetes.client.V1alpha3CompositePodGroupTemplateDict]]
    controllerRef: typing.Optional[kubernetes.client.V1alpha3TypedLocalObjectReferenceDict]
    podGroupTemplates: typing.Optional[list[kubernetes.client.V1alpha3PodGroupTemplateDict]]
