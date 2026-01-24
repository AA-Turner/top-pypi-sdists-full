import datetime
import typing

import kubernetes.client

class V1DeviceClaimConfiguration:
    opaque: typing.Optional[kubernetes.client.V1OpaqueDeviceConfiguration]
    requests: typing.Optional[list[str]]
    
    def __init__(self, *, opaque: typing.Optional[kubernetes.client.V1OpaqueDeviceConfiguration] = ..., requests: typing.Optional[list[str]] = ...) -> None:
        ...
    def to_dict(self) -> V1DeviceClaimConfigurationDict:
        ...
class V1DeviceClaimConfigurationDict(typing.TypedDict, total=False):
    opaque: typing.Optional[kubernetes.client.V1OpaqueDeviceConfigurationDict]
    requests: typing.Optional[list[str]]
