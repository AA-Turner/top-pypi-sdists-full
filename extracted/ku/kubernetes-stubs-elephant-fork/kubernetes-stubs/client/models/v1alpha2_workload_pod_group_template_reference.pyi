import datetime
import typing

import kubernetes.client

class V1alpha2WorkloadPodGroupTemplateReference:
    pod_group_template_name: str
    workload_name: str
    
    def __init__(self, *, pod_group_template_name: str, workload_name: str) -> None:
        ...
    def to_dict(self) -> V1alpha2WorkloadPodGroupTemplateReferenceDict:
        ...
class V1alpha2WorkloadPodGroupTemplateReferenceDict(typing.TypedDict, total=False):
    podGroupTemplateName: str
    workloadName: str
