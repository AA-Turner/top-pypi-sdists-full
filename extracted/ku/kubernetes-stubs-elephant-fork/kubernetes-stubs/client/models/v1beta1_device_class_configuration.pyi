import datetime
import typing

import kubernetes.client

class V1beta1DeviceClassConfiguration:
    opaque: typing.Optional[kubernetes.client.V1beta1OpaqueDeviceConfiguration]
    
    def __init__(self, *, opaque: typing.Optional[kubernetes.client.V1beta1OpaqueDeviceConfiguration] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1DeviceClassConfigurationDict:
        ...
class V1beta1DeviceClassConfigurationDict(typing.TypedDict, total=False):
    opaque: typing.Optional[kubernetes.client.V1beta1OpaqueDeviceConfigurationDict]
