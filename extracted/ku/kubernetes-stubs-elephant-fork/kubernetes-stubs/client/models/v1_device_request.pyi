import datetime
import typing

import kubernetes.client

class V1DeviceRequest:
    exactly: typing.Optional[kubernetes.client.V1ExactDeviceRequest]
    first_available: typing.Optional[list[kubernetes.client.V1DeviceSubRequest]]
    name: str
    
    def __init__(self, *, exactly: typing.Optional[kubernetes.client.V1ExactDeviceRequest] = ..., first_available: typing.Optional[list[kubernetes.client.V1DeviceSubRequest]] = ..., name: str) -> None:
        ...
    def to_dict(self) -> V1DeviceRequestDict:
        ...
class V1DeviceRequestDict(typing.TypedDict, total=False):
    exactly: typing.Optional[kubernetes.client.V1ExactDeviceRequestDict]
    firstAvailable: typing.Optional[list[kubernetes.client.V1DeviceSubRequestDict]]
    name: str
