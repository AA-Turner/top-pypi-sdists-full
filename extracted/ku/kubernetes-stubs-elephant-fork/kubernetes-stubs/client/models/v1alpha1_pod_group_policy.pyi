import datetime
import typing

import kubernetes.client

class V1alpha1PodGroupPolicy:
    basic: typing.Optional[typing.Any]
    gang: typing.Optional[kubernetes.client.V1alpha1GangSchedulingPolicy]
    
    def __init__(self, *, basic: typing.Optional[typing.Any] = ..., gang: typing.Optional[kubernetes.client.V1alpha1GangSchedulingPolicy] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha1PodGroupPolicyDict:
        ...
class V1alpha1PodGroupPolicyDict(typing.TypedDict, total=False):
    basic: typing.Optional[typing.Any]
    gang: typing.Optional[kubernetes.client.V1alpha1GangSchedulingPolicyDict]
