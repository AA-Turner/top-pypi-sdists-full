import datetime
import typing

import kubernetes.client

class V1beta1DeviceCapacity:
    request_policy: typing.Optional[kubernetes.client.V1beta1CapacityRequestPolicy]
    value: str
    
    def __init__(self, *, request_policy: typing.Optional[kubernetes.client.V1beta1CapacityRequestPolicy] = ..., value: str) -> None:
        ...
    def to_dict(self) -> V1beta1DeviceCapacityDict:
        ...
class V1beta1DeviceCapacityDict(typing.TypedDict, total=False):
    requestPolicy: typing.Optional[kubernetes.client.V1beta1CapacityRequestPolicyDict]
    value: str
