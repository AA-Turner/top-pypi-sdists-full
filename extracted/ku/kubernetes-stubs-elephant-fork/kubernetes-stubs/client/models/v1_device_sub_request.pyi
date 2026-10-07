import datetime
import typing

import kubernetes.client

class V1DeviceSubRequest:
    allocation_mode: typing.Optional[str]
    capacity: typing.Optional[kubernetes.client.V1CapacityRequirements]
    count: typing.Optional[int]
    derived_attributes: typing.Optional[list[kubernetes.client.V1DeviceDerivedAttribute]]
    device_class_name: str
    name: str
    selectors: typing.Optional[list[kubernetes.client.V1DeviceSelector]]
    tolerations: typing.Optional[list[kubernetes.client.V1DeviceToleration]]
    
    def __init__(self, *, allocation_mode: typing.Optional[str] = ..., capacity: typing.Optional[kubernetes.client.V1CapacityRequirements] = ..., count: typing.Optional[int] = ..., derived_attributes: typing.Optional[list[kubernetes.client.V1DeviceDerivedAttribute]] = ..., device_class_name: str, name: str, selectors: typing.Optional[list[kubernetes.client.V1DeviceSelector]] = ..., tolerations: typing.Optional[list[kubernetes.client.V1DeviceToleration]] = ...) -> None:
        ...
    def to_dict(self) -> V1DeviceSubRequestDict:
        ...
class V1DeviceSubRequestDict(typing.TypedDict, total=False):
    allocationMode: typing.Optional[str]
    capacity: typing.Optional[kubernetes.client.V1CapacityRequirementsDict]
    count: typing.Optional[int]
    derivedAttributes: typing.Optional[list[kubernetes.client.V1DeviceDerivedAttributeDict]]
    deviceClassName: str
    name: str
    selectors: typing.Optional[list[kubernetes.client.V1DeviceSelectorDict]]
    tolerations: typing.Optional[list[kubernetes.client.V1DeviceTolerationDict]]
