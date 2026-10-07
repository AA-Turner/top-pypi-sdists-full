import datetime
import typing

import kubernetes.client

class V1alpha3CompositePodGroupSchedulingPolicy:
    basic: typing.Optional[typing.Any]
    gang: typing.Optional[kubernetes.client.V1alpha3CompositeGangSchedulingPolicy]
    
    def __init__(self, *, basic: typing.Optional[typing.Any] = ..., gang: typing.Optional[kubernetes.client.V1alpha3CompositeGangSchedulingPolicy] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3CompositePodGroupSchedulingPolicyDict:
        ...
class V1alpha3CompositePodGroupSchedulingPolicyDict(typing.TypedDict, total=False):
    basic: typing.Optional[typing.Any]
    gang: typing.Optional[kubernetes.client.V1alpha3CompositeGangSchedulingPolicyDict]
