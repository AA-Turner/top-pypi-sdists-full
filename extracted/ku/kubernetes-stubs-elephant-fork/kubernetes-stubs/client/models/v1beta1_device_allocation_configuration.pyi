import datetime
import typing

import kubernetes.client

class V1beta1DeviceAllocationConfiguration:
    opaque: typing.Optional[kubernetes.client.V1beta1OpaqueDeviceConfiguration]
    requests: typing.Optional[list[str]]
    source: str
    
    def __init__(self, *, opaque: typing.Optional[kubernetes.client.V1beta1OpaqueDeviceConfiguration] = ..., requests: typing.Optional[list[str]] = ..., source: str) -> None:
        ...
    def to_dict(self) -> V1beta1DeviceAllocationConfigurationDict:
        ...
class V1beta1DeviceAllocationConfigurationDict(typing.TypedDict, total=False):
    opaque: typing.Optional[kubernetes.client.V1beta1OpaqueDeviceConfigurationDict]
    requests: typing.Optional[list[str]]
    source: str
