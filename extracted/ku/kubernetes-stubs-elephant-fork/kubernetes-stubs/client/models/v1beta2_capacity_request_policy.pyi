import datetime
import typing

import kubernetes.client

class V1beta2CapacityRequestPolicy:
    default: typing.Optional[str]
    valid_range: typing.Optional[kubernetes.client.V1beta2CapacityRequestPolicyRange]
    valid_values: typing.Optional[list[str]]
    
    def __init__(self, *, default: typing.Optional[str] = ..., valid_range: typing.Optional[kubernetes.client.V1beta2CapacityRequestPolicyRange] = ..., valid_values: typing.Optional[list[str]] = ...) -> None:
        ...
    def to_dict(self) -> V1beta2CapacityRequestPolicyDict:
        ...
class V1beta2CapacityRequestPolicyDict(typing.TypedDict, total=False):
    default: typing.Optional[str]
    validRange: typing.Optional[kubernetes.client.V1beta2CapacityRequestPolicyRangeDict]
    validValues: typing.Optional[list[str]]
