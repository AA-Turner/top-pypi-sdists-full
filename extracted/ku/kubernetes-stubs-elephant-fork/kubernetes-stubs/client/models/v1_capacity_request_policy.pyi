import datetime
import typing

import kubernetes.client

class V1CapacityRequestPolicy:
    default: typing.Optional[str]
    valid_range: typing.Optional[kubernetes.client.V1CapacityRequestPolicyRange]
    valid_values: typing.Optional[list[str]]
    
    def __init__(self, *, default: typing.Optional[str] = ..., valid_range: typing.Optional[kubernetes.client.V1CapacityRequestPolicyRange] = ..., valid_values: typing.Optional[list[str]] = ...) -> None:
        ...
    def to_dict(self) -> V1CapacityRequestPolicyDict:
        ...
class V1CapacityRequestPolicyDict(typing.TypedDict, total=False):
    default: typing.Optional[str]
    validRange: typing.Optional[kubernetes.client.V1CapacityRequestPolicyRangeDict]
    validValues: typing.Optional[list[str]]
