import datetime
import typing

import kubernetes.client

class V1alpha1WorkloadSpec:
    controller_ref: typing.Optional[kubernetes.client.V1alpha1TypedLocalObjectReference]
    pod_groups: list[kubernetes.client.V1alpha1PodGroup]
    
    def __init__(self, *, controller_ref: typing.Optional[kubernetes.client.V1alpha1TypedLocalObjectReference] = ..., pod_groups: list[kubernetes.client.V1alpha1PodGroup]) -> None:
        ...
    def to_dict(self) -> V1alpha1WorkloadSpecDict:
        ...
class V1alpha1WorkloadSpecDict(typing.TypedDict, total=False):
    controllerRef: typing.Optional[kubernetes.client.V1alpha1TypedLocalObjectReferenceDict]
    podGroups: list[kubernetes.client.V1alpha1PodGroupDict]
