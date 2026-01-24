import datetime
import typing

import kubernetes.client

class V1alpha3DeviceTaintRuleStatus:
    conditions: typing.Optional[list[kubernetes.client.V1Condition]]
    
    def __init__(self, *, conditions: typing.Optional[list[kubernetes.client.V1Condition]] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3DeviceTaintRuleStatusDict:
        ...
class V1alpha3DeviceTaintRuleStatusDict(typing.TypedDict, total=False):
    conditions: typing.Optional[list[kubernetes.client.V1ConditionDict]]
