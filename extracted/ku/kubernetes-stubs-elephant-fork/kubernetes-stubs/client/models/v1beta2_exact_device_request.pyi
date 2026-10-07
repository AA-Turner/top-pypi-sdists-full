import datetime
import typing

import kubernetes.client

class V1beta2ExactDeviceRequest:
    admin_access: typing.Optional[bool]
    allocation_mode: typing.Optional[str]
    capacity: typing.Optional[kubernetes.client.V1beta2CapacityRequirements]
    count: typing.Optional[int]
    derived_attributes: typing.Optional[list[kubernetes.client.V1beta2DeviceDerivedAttribute]]
    device_class_name: str
    selectors: typing.Optional[list[kubernetes.client.V1beta2DeviceSelector]]
    tolerations: typing.Optional[list[kubernetes.client.V1beta2DeviceToleration]]
    
    def __init__(self, *, admin_access: typing.Optional[bool] = ..., allocation_mode: typing.Optional[str] = ..., capacity: typing.Optional[kubernetes.client.V1beta2CapacityRequirements] = ..., count: typing.Optional[int] = ..., derived_attributes: typing.Optional[list[kubernetes.client.V1beta2DeviceDerivedAttribute]] = ..., device_class_name: str, selectors: typing.Optional[list[kubernetes.client.V1beta2DeviceSelector]] = ..., tolerations: typing.Optional[list[kubernetes.client.V1beta2DeviceToleration]] = ...) -> None:
        ...
    def to_dict(self) -> V1beta2ExactDeviceRequestDict:
        ...
class V1beta2ExactDeviceRequestDict(typing.TypedDict, total=False):
    adminAccess: typing.Optional[bool]
    allocationMode: typing.Optional[str]
    capacity: typing.Optional[kubernetes.client.V1beta2CapacityRequirementsDict]
    count: typing.Optional[int]
    derivedAttributes: typing.Optional[list[kubernetes.client.V1beta2DeviceDerivedAttributeDict]]
    deviceClassName: str
    selectors: typing.Optional[list[kubernetes.client.V1beta2DeviceSelectorDict]]
    tolerations: typing.Optional[list[kubernetes.client.V1beta2DeviceTolerationDict]]
