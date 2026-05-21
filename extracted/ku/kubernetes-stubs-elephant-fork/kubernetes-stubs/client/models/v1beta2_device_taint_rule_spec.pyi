import datetime
import typing

import kubernetes.client

class V1beta2DeviceTaintRuleSpec:
    device_selector: typing.Optional[kubernetes.client.V1beta2DeviceTaintSelector]
    taint: kubernetes.client.V1beta2DeviceTaint
    
    def __init__(self, *, device_selector: typing.Optional[kubernetes.client.V1beta2DeviceTaintSelector] = ..., taint: kubernetes.client.V1beta2DeviceTaint) -> None:
        ...
    def to_dict(self) -> V1beta2DeviceTaintRuleSpecDict:
        ...
class V1beta2DeviceTaintRuleSpecDict(typing.TypedDict, total=False):
    deviceSelector: typing.Optional[kubernetes.client.V1beta2DeviceTaintSelectorDict]
    taint: kubernetes.client.V1beta2DeviceTaintDict
