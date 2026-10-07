import datetime
import typing

import kubernetes.client

class V1alpha3WorkloadPodGroupSchedulingPolicy:
    basic: typing.Optional[typing.Any]
    gang: typing.Optional[kubernetes.client.V1alpha3WorkloadPodGroupGangSchedulingPolicy]
    
    def __init__(self, *, basic: typing.Optional[typing.Any] = ..., gang: typing.Optional[kubernetes.client.V1alpha3WorkloadPodGroupGangSchedulingPolicy] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3WorkloadPodGroupSchedulingPolicyDict:
        ...
class V1alpha3WorkloadPodGroupSchedulingPolicyDict(typing.TypedDict, total=False):
    basic: typing.Optional[typing.Any]
    gang: typing.Optional[kubernetes.client.V1alpha3WorkloadPodGroupGangSchedulingPolicyDict]
