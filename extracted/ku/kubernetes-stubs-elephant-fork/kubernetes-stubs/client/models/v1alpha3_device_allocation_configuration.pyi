import datetime
import typing

import kubernetes.client

class V1alpha3DeviceAllocationConfiguration:
    opaque: typing.Optional[kubernetes.client.V1alpha3OpaqueDeviceConfiguration]
    requests: typing.Optional[list[str]]
    source: str
    
    def __init__(self, *, opaque: typing.Optional[kubernetes.client.V1alpha3OpaqueDeviceConfiguration] = ..., requests: typing.Optional[list[str]] = ..., source: str) -> None:
        ...
    def to_dict(self) -> V1alpha3DeviceAllocationConfigurationDict:
        ...
class V1alpha3DeviceAllocationConfigurationDict(typing.TypedDict, total=False):
    opaque: typing.Optional[kubernetes.client.V1alpha3OpaqueDeviceConfigurationDict]
    requests: typing.Optional[list[str]]
    source: str
