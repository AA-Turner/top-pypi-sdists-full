import datetime
import typing

import kubernetes.client

class V1beta2DeviceSubRequest:
    allocation_mode: typing.Optional[str]
    capacity: typing.Optional[kubernetes.client.V1beta2CapacityRequirements]
    count: typing.Optional[int]
    device_class_name: str
    name: str
    selectors: typing.Optional[list[kubernetes.client.V1beta2DeviceSelector]]
    tolerations: typing.Optional[list[kubernetes.client.V1beta2DeviceToleration]]
    
    def __init__(self, *, allocation_mode: typing.Optional[str] = ..., capacity: typing.Optional[kubernetes.client.V1beta2CapacityRequirements] = ..., count: typing.Optional[int] = ..., device_class_name: str, name: str, selectors: typing.Optional[list[kubernetes.client.V1beta2DeviceSelector]] = ..., tolerations: typing.Optional[list[kubernetes.client.V1beta2DeviceToleration]] = ...) -> None:
        ...
    def to_dict(self) -> V1beta2DeviceSubRequestDict:
        ...
class V1beta2DeviceSubRequestDict(typing.TypedDict, total=False):
    allocationMode: typing.Optional[str]
    capacity: typing.Optional[kubernetes.client.V1beta2CapacityRequirementsDict]
    count: typing.Optional[int]
    deviceClassName: str
    name: str
    selectors: typing.Optional[list[kubernetes.client.V1beta2DeviceSelectorDict]]
    tolerations: typing.Optional[list[kubernetes.client.V1beta2DeviceTolerationDict]]
