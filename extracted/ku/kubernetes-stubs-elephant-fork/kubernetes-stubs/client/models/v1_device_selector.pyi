import datetime
import typing

import kubernetes.client

class V1DeviceSelector:
    cel: typing.Optional[kubernetes.client.V1CELDeviceSelector]
    
    def __init__(self, *, cel: typing.Optional[kubernetes.client.V1CELDeviceSelector] = ...) -> None:
        ...
    def to_dict(self) -> V1DeviceSelectorDict:
        ...
class V1DeviceSelectorDict(typing.TypedDict, total=False):
    cel: typing.Optional[kubernetes.client.V1CELDeviceSelectorDict]
