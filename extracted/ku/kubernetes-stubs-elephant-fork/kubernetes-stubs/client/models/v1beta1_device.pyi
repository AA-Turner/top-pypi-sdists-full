import datetime
import typing

import kubernetes.client

class V1beta1Device:
    basic: typing.Optional[kubernetes.client.V1beta1BasicDevice]
    name: str
    
    def __init__(self, *, basic: typing.Optional[kubernetes.client.V1beta1BasicDevice] = ..., name: str) -> None:
        ...
    def to_dict(self) -> V1beta1DeviceDict:
        ...
class V1beta1DeviceDict(typing.TypedDict, total=False):
    basic: typing.Optional[kubernetes.client.V1beta1BasicDeviceDict]
    name: str
