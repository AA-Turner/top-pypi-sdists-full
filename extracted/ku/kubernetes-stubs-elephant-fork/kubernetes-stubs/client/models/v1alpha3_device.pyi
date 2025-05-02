import datetime
import typing

import kubernetes.client

class V1alpha3Device:
    basic: typing.Optional[kubernetes.client.V1alpha3BasicDevice]
    name: str
    
    def __init__(self, *, basic: typing.Optional[kubernetes.client.V1alpha3BasicDevice] = ..., name: str) -> None:
        ...
    def to_dict(self) -> V1alpha3DeviceDict:
        ...
class V1alpha3DeviceDict(typing.TypedDict, total=False):
    basic: typing.Optional[kubernetes.client.V1alpha3BasicDeviceDict]
    name: str
