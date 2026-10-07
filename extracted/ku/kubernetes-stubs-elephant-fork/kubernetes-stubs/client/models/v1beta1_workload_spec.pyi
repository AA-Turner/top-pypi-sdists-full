import datetime
import typing

import kubernetes.client

class V1beta1WorkloadSpec:
    composite_pod_group_templates: typing.Optional[list[kubernetes.client.V1beta1CompositePodGroupTemplate]]
    controller_ref: typing.Optional[kubernetes.client.V1beta1TypedLocalObjectReference]
    pod_group_templates: typing.Optional[list[kubernetes.client.V1beta1PodGroupTemplate]]
    
    def __init__(self, *, composite_pod_group_templates: typing.Optional[list[kubernetes.client.V1beta1CompositePodGroupTemplate]] = ..., controller_ref: typing.Optional[kubernetes.client.V1beta1TypedLocalObjectReference] = ..., pod_group_templates: typing.Optional[list[kubernetes.client.V1beta1PodGroupTemplate]] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1WorkloadSpecDict:
        ...
class V1beta1WorkloadSpecDict(typing.TypedDict, total=False):
    compositePodGroupTemplates: typing.Optional[list[kubernetes.client.V1beta1CompositePodGroupTemplateDict]]
    controllerRef: typing.Optional[kubernetes.client.V1beta1TypedLocalObjectReferenceDict]
    podGroupTemplates: typing.Optional[list[kubernetes.client.V1beta1PodGroupTemplateDict]]
