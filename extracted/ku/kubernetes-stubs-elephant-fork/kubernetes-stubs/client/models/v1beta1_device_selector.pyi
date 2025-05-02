import datetime
import typing

import kubernetes.client

class V1beta1DeviceSelector:
    cel: typing.Optional[kubernetes.client.V1beta1CELDeviceSelector]
    
    def __init__(self, *, cel: typing.Optional[kubernetes.client.V1beta1CELDeviceSelector] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1DeviceSelectorDict:
        ...
class V1beta1DeviceSelectorDict(typing.TypedDict, total=False):
    cel: typing.Optional[kubernetes.client.V1beta1CELDeviceSelectorDict]
