import datetime
import typing

import kubernetes.client

class V1alpha2PodGroupTemplateReference:
    workload: typing.Optional[kubernetes.client.V1alpha2WorkloadPodGroupTemplateReference]
    
    def __init__(self, *, workload: typing.Optional[kubernetes.client.V1alpha2WorkloadPodGroupTemplateReference] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha2PodGroupTemplateReferenceDict:
        ...
class V1alpha2PodGroupTemplateReferenceDict(typing.TypedDict, total=False):
    workload: typing.Optional[kubernetes.client.V1alpha2WorkloadPodGroupTemplateReferenceDict]
