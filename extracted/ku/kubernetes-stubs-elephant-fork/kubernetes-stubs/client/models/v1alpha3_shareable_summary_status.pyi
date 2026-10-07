import datetime
import typing

import kubernetes.client

class V1alpha3ShareableSummaryStatus:
    capacity: typing.Optional[list[kubernetes.client.V1alpha3ShareableCapacityStatus]]
    fully_available_devices: int
    partially_available_devices: int
    
    def __init__(self, *, capacity: typing.Optional[list[kubernetes.client.V1alpha3ShareableCapacityStatus]] = ..., fully_available_devices: int, partially_available_devices: int) -> None:
        ...
    def to_dict(self) -> V1alpha3ShareableSummaryStatusDict:
        ...
class V1alpha3ShareableSummaryStatusDict(typing.TypedDict, total=False):
    capacity: typing.Optional[list[kubernetes.client.V1alpha3ShareableCapacityStatusDict]]
    fullyAvailableDevices: int
    partiallyAvailableDevices: int
