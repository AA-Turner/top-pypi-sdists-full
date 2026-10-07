import datetime
import typing

import kubernetes.client

class V1beta1PodGroupSchedulingPolicy:
    basic: typing.Optional[typing.Any]
    gang: typing.Optional[kubernetes.client.V1beta1GangSchedulingPolicy]
    
    def __init__(self, *, basic: typing.Optional[typing.Any] = ..., gang: typing.Optional[kubernetes.client.V1beta1GangSchedulingPolicy] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1PodGroupSchedulingPolicyDict:
        ...
class V1beta1PodGroupSchedulingPolicyDict(typing.TypedDict, total=False):
    basic: typing.Optional[typing.Any]
    gang: typing.Optional[kubernetes.client.V1beta1GangSchedulingPolicyDict]
