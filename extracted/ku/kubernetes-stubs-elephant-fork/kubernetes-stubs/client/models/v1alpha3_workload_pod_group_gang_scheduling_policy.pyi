import datetime
import typing

import kubernetes.client

class V1alpha3WorkloadPodGroupGangSchedulingPolicy:
    min_count: typing.Optional[int]
    
    def __init__(self, *, min_count: typing.Optional[int] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3WorkloadPodGroupGangSchedulingPolicyDict:
        ...
class V1alpha3WorkloadPodGroupGangSchedulingPolicyDict(typing.TypedDict, total=False):
    minCount: typing.Optional[int]
