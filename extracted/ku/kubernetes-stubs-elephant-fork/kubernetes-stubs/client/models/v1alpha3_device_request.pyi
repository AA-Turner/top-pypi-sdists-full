import datetime
import typing

import kubernetes.client

class V1alpha3DeviceRequest:
    admin_access: typing.Optional[bool]
    allocation_mode: typing.Optional[str]
    count: typing.Optional[int]
    device_class_name: str
    name: str
    selectors: typing.Optional[list[kubernetes.client.V1alpha3DeviceSelector]]
    
    def __init__(self, *, admin_access: typing.Optional[bool] = ..., allocation_mode: typing.Optional[str] = ..., count: typing.Optional[int] = ..., device_class_name: str, name: str, selectors: typing.Optional[list[kubernetes.client.V1alpha3DeviceSelector]] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3DeviceRequestDict:
        ...
class V1alpha3DeviceRequestDict(typing.TypedDict, total=False):
    adminAccess: typing.Optional[bool]
    allocationMode: typing.Optional[str]
    count: typing.Optional[int]
    deviceClassName: str
    name: str
    selectors: typing.Optional[list[kubernetes.client.V1alpha3DeviceSelectorDict]]
