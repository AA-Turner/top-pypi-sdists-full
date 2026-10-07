import datetime
import typing

import kubernetes.client

class V1alpha3PodGroupSchedulingPolicy:
    basic: typing.Optional[typing.Any]
    gang: typing.Optional[kubernetes.client.V1alpha3GangSchedulingPolicy]
    
    def __init__(self, *, basic: typing.Optional[typing.Any] = ..., gang: typing.Optional[kubernetes.client.V1alpha3GangSchedulingPolicy] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3PodGroupSchedulingPolicyDict:
        ...
class V1alpha3PodGroupSchedulingPolicyDict(typing.TypedDict, total=False):
    basic: typing.Optional[typing.Any]
    gang: typing.Optional[kubernetes.client.V1alpha3GangSchedulingPolicyDict]
