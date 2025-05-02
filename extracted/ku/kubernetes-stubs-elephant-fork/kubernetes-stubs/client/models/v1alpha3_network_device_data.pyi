import datetime
import typing

import kubernetes.client

class V1alpha3NetworkDeviceData:
    hardware_address: typing.Optional[str]
    interface_name: typing.Optional[str]
    ips: typing.Optional[list[str]]
    
    def __init__(self, *, hardware_address: typing.Optional[str] = ..., interface_name: typing.Optional[str] = ..., ips: typing.Optional[list[str]] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3NetworkDeviceDataDict:
        ...
class V1alpha3NetworkDeviceDataDict(typing.TypedDict, total=False):
    hardwareAddress: typing.Optional[str]
    interfaceName: typing.Optional[str]
    ips: typing.Optional[list[str]]
