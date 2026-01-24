import datetime
import typing

import kubernetes.client

class V1beta1CapacityRequestPolicyRange:
    max: typing.Optional[str]
    min: str
    step: typing.Optional[str]
    
    def __init__(self, *, max: typing.Optional[str] = ..., min: str, step: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1CapacityRequestPolicyRangeDict:
        ...
class V1beta1CapacityRequestPolicyRangeDict(typing.TypedDict, total=False):
    max: typing.Optional[str]
    min: str
    step: typing.Optional[str]
