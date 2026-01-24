import datetime
import typing

import kubernetes.client

class V1beta1DeviceRequest:
    admin_access: typing.Optional[bool]
    allocation_mode: typing.Optional[str]
    capacity: typing.Optional[kubernetes.client.V1beta1CapacityRequirements]
    count: typing.Optional[int]
    device_class_name: typing.Optional[str]
    first_available: typing.Optional[list[kubernetes.client.V1beta1DeviceSubRequest]]
    name: str
    selectors: typing.Optional[list[kubernetes.client.V1beta1DeviceSelector]]
    tolerations: typing.Optional[list[kubernetes.client.V1beta1DeviceToleration]]
    
    def __init__(self, *, admin_access: typing.Optional[bool] = ..., allocation_mode: typing.Optional[str] = ..., capacity: typing.Optional[kubernetes.client.V1beta1CapacityRequirements] = ..., count: typing.Optional[int] = ..., device_class_name: typing.Optional[str] = ..., first_available: typing.Optional[list[kubernetes.client.V1beta1DeviceSubRequest]] = ..., name: str, selectors: typing.Optional[list[kubernetes.client.V1beta1DeviceSelector]] = ..., tolerations: typing.Optional[list[kubernetes.client.V1beta1DeviceToleration]] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1DeviceRequestDict:
        ...
class V1beta1DeviceRequestDict(typing.TypedDict, total=False):
    adminAccess: typing.Optional[bool]
    allocationMode: typing.Optional[str]
    capacity: typing.Optional[kubernetes.client.V1beta1CapacityRequirementsDict]
    count: typing.Optional[int]
    deviceClassName: typing.Optional[str]
    firstAvailable: typing.Optional[list[kubernetes.client.V1beta1DeviceSubRequestDict]]
    name: str
    selectors: typing.Optional[list[kubernetes.client.V1beta1DeviceSelectorDict]]
    tolerations: typing.Optional[list[kubernetes.client.V1beta1DeviceTolerationDict]]
