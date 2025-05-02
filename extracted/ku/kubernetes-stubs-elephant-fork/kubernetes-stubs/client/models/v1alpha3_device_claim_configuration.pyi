import datetime
import typing

import kubernetes.client

class V1alpha3DeviceClaimConfiguration:
    opaque: typing.Optional[kubernetes.client.V1alpha3OpaqueDeviceConfiguration]
    requests: typing.Optional[list[str]]
    
    def __init__(self, *, opaque: typing.Optional[kubernetes.client.V1alpha3OpaqueDeviceConfiguration] = ..., requests: typing.Optional[list[str]] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3DeviceClaimConfigurationDict:
        ...
class V1alpha3DeviceClaimConfigurationDict(typing.TypedDict, total=False):
    opaque: typing.Optional[kubernetes.client.V1alpha3OpaqueDeviceConfigurationDict]
    requests: typing.Optional[list[str]]
