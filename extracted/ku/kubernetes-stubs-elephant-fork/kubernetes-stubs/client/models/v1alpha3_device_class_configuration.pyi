import datetime
import typing

import kubernetes.client

class V1alpha3DeviceClassConfiguration:
    opaque: typing.Optional[kubernetes.client.V1alpha3OpaqueDeviceConfiguration]
    
    def __init__(self, *, opaque: typing.Optional[kubernetes.client.V1alpha3OpaqueDeviceConfiguration] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3DeviceClassConfigurationDict:
        ...
class V1alpha3DeviceClassConfigurationDict(typing.TypedDict, total=False):
    opaque: typing.Optional[kubernetes.client.V1alpha3OpaqueDeviceConfigurationDict]
