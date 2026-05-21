import datetime
import typing

import kubernetes.client

class V1alpha2WorkloadSpec:
    controller_ref: typing.Optional[kubernetes.client.V1alpha2TypedLocalObjectReference]
    pod_group_templates: list[kubernetes.client.V1alpha2PodGroupTemplate]
    
    def __init__(self, *, controller_ref: typing.Optional[kubernetes.client.V1alpha2TypedLocalObjectReference] = ..., pod_group_templates: list[kubernetes.client.V1alpha2PodGroupTemplate]) -> None:
        ...
    def to_dict(self) -> V1alpha2WorkloadSpecDict:
        ...
class V1alpha2WorkloadSpecDict(typing.TypedDict, total=False):
    controllerRef: typing.Optional[kubernetes.client.V1alpha2TypedLocalObjectReferenceDict]
    podGroupTemplates: list[kubernetes.client.V1alpha2PodGroupTemplateDict]
