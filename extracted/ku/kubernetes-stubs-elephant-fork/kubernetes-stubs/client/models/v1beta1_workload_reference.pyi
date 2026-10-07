import datetime
import typing

import kubernetes.client

class V1beta1WorkloadReference:
    template_name: str
    workload_name: str
    
    def __init__(self, *, template_name: str, workload_name: str) -> None:
        ...
    def to_dict(self) -> V1beta1WorkloadReferenceDict:
        ...
class V1beta1WorkloadReferenceDict(typing.TypedDict, total=False):
    templateName: str
    workloadName: str
