import datetime
import typing

import kubernetes.client

class V1beta1DeviceSubRequest:
    allocation_mode: typing.Optional[str]
    capacity: typing.Optional[kubernetes.client.V1beta1CapacityRequirements]
    count: typing.Optional[int]
    device_class_name: str
    name: str
    selectors: typing.Optional[list[kubernetes.client.V1beta1DeviceSelector]]
    tolerations: typing.Optional[list[kubernetes.client.V1beta1DeviceToleration]]
    
    def __init__(self, *, allocation_mode: typing.Optional[str] = ..., capacity: typing.Optional[kubernetes.client.V1beta1CapacityRequirements] = ..., count: typing.Optional[int] = ..., device_class_name: str, name: str, selectors: typing.Optional[list[kubernetes.client.V1beta1DeviceSelector]] = ..., tolerations: typing.Optional[list[kubernetes.client.V1beta1DeviceToleration]] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1DeviceSubRequestDict:
        ...
class V1beta1DeviceSubRequestDict(typing.TypedDict, total=False):
    allocationMode: typing.Optional[str]
    capacity: typing.Optional[kubernetes.client.V1beta1CapacityRequirementsDict]
    count: typing.Optional[int]
    deviceClassName: str
    name: str
    selectors: typing.Optional[list[kubernetes.client.V1beta1DeviceSelectorDict]]
    tolerations: typing.Optional[list[kubernetes.client.V1beta1DeviceTolerationDict]]
