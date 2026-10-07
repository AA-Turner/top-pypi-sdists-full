import datetime
import typing

import kubernetes.client

class V1DeviceTaintRuleSpec:
    device_selector: typing.Optional[kubernetes.client.V1DeviceTaintSelector]
    taint: kubernetes.client.V1DeviceTaint
    
    def __init__(self, *, device_selector: typing.Optional[kubernetes.client.V1DeviceTaintSelector] = ..., taint: kubernetes.client.V1DeviceTaint) -> None:
        ...
    def to_dict(self) -> V1DeviceTaintRuleSpecDict:
        ...
class V1DeviceTaintRuleSpecDict(typing.TypedDict, total=False):
    deviceSelector: typing.Optional[kubernetes.client.V1DeviceTaintSelectorDict]
    taint: kubernetes.client.V1DeviceTaintDict
