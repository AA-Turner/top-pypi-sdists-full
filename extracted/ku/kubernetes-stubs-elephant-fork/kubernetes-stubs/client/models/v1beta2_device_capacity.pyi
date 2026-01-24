import datetime
import typing

import kubernetes.client

class V1beta2DeviceCapacity:
    request_policy: typing.Optional[kubernetes.client.V1beta2CapacityRequestPolicy]
    value: str
    
    def __init__(self, *, request_policy: typing.Optional[kubernetes.client.V1beta2CapacityRequestPolicy] = ..., value: str) -> None:
        ...
    def to_dict(self) -> V1beta2DeviceCapacityDict:
        ...
class V1beta2DeviceCapacityDict(typing.TypedDict, total=False):
    requestPolicy: typing.Optional[kubernetes.client.V1beta2CapacityRequestPolicyDict]
    value: str
