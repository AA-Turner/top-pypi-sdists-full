import datetime
import typing

import kubernetes.client

class V1alpha2PodGroupSchedulingPolicy:
    basic: typing.Optional[typing.Any]
    gang: typing.Optional[kubernetes.client.V1alpha2GangSchedulingPolicy]
    
    def __init__(self, *, basic: typing.Optional[typing.Any] = ..., gang: typing.Optional[kubernetes.client.V1alpha2GangSchedulingPolicy] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha2PodGroupSchedulingPolicyDict:
        ...
class V1alpha2PodGroupSchedulingPolicyDict(typing.TypedDict, total=False):
    basic: typing.Optional[typing.Any]
    gang: typing.Optional[kubernetes.client.V1alpha2GangSchedulingPolicyDict]
