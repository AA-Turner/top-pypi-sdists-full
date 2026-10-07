import datetime
import typing

import kubernetes.client

class V1beta1CompositePodGroupSchedulingPolicy:
    basic: typing.Optional[typing.Any]
    gang: typing.Optional[kubernetes.client.V1beta1CompositeGangSchedulingPolicy]
    
    def __init__(self, *, basic: typing.Optional[typing.Any] = ..., gang: typing.Optional[kubernetes.client.V1beta1CompositeGangSchedulingPolicy] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1CompositePodGroupSchedulingPolicyDict:
        ...
class V1beta1CompositePodGroupSchedulingPolicyDict(typing.TypedDict, total=False):
    basic: typing.Optional[typing.Any]
    gang: typing.Optional[kubernetes.client.V1beta1CompositeGangSchedulingPolicyDict]
