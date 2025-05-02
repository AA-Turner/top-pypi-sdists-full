import datetime
import typing

import kubernetes.client

class V1beta1DeviceAllocationResult:
    config: typing.Optional[list[kubernetes.client.V1beta1DeviceAllocationConfiguration]]
    results: typing.Optional[list[kubernetes.client.V1beta1DeviceRequestAllocationResult]]
    
    def __init__(self, *, config: typing.Optional[list[kubernetes.client.V1beta1DeviceAllocationConfiguration]] = ..., results: typing.Optional[list[kubernetes.client.V1beta1DeviceRequestAllocationResult]] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1DeviceAllocationResultDict:
        ...
class V1beta1DeviceAllocationResultDict(typing.TypedDict, total=False):
    config: typing.Optional[list[kubernetes.client.V1beta1DeviceAllocationConfigurationDict]]
    results: typing.Optional[list[kubernetes.client.V1beta1DeviceRequestAllocationResultDict]]
