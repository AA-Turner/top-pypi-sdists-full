import datetime
import typing

import kubernetes.client

class V1DeviceClassConfiguration:
    opaque: typing.Optional[kubernetes.client.V1OpaqueDeviceConfiguration]
    
    def __init__(self, *, opaque: typing.Optional[kubernetes.client.V1OpaqueDeviceConfiguration] = ...) -> None:
        ...
    def to_dict(self) -> V1DeviceClassConfigurationDict:
        ...
class V1DeviceClassConfigurationDict(typing.TypedDict, total=False):
    opaque: typing.Optional[kubernetes.client.V1OpaqueDeviceConfigurationDict]
