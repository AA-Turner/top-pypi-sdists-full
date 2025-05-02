import datetime
import typing

import kubernetes.client

class V1alpha3DeviceAllocationResult:
    config: typing.Optional[list[kubernetes.client.V1alpha3DeviceAllocationConfiguration]]
    results: typing.Optional[list[kubernetes.client.V1alpha3DeviceRequestAllocationResult]]
    
    def __init__(self, *, config: typing.Optional[list[kubernetes.client.V1alpha3DeviceAllocationConfiguration]] = ..., results: typing.Optional[list[kubernetes.client.V1alpha3DeviceRequestAllocationResult]] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3DeviceAllocationResultDict:
        ...
class V1alpha3DeviceAllocationResultDict(typing.TypedDict, total=False):
    config: typing.Optional[list[kubernetes.client.V1alpha3DeviceAllocationConfigurationDict]]
    results: typing.Optional[list[kubernetes.client.V1alpha3DeviceRequestAllocationResultDict]]
