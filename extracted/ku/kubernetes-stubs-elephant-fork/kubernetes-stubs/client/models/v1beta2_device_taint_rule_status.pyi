import datetime
import typing

import kubernetes.client

class V1beta2DeviceTaintRuleStatus:
    conditions: typing.Optional[list[kubernetes.client.V1Condition]]
    
    def __init__(self, *, conditions: typing.Optional[list[kubernetes.client.V1Condition]] = ...) -> None:
        ...
    def to_dict(self) -> V1beta2DeviceTaintRuleStatusDict:
        ...
class V1beta2DeviceTaintRuleStatusDict(typing.TypedDict, total=False):
    conditions: typing.Optional[list[kubernetes.client.V1ConditionDict]]
