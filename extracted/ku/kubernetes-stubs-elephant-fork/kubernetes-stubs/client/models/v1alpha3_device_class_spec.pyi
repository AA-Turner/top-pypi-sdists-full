import datetime
import typing

import kubernetes.client

class V1alpha3DeviceClassSpec:
    config: typing.Optional[list[kubernetes.client.V1alpha3DeviceClassConfiguration]]
    selectors: typing.Optional[list[kubernetes.client.V1alpha3DeviceSelector]]
    
    def __init__(self, *, config: typing.Optional[list[kubernetes.client.V1alpha3DeviceClassConfiguration]] = ..., selectors: typing.Optional[list[kubernetes.client.V1alpha3DeviceSelector]] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3DeviceClassSpecDict:
        ...
class V1alpha3DeviceClassSpecDict(typing.TypedDict, total=False):
    config: typing.Optional[list[kubernetes.client.V1alpha3DeviceClassConfigurationDict]]
    selectors: typing.Optional[list[kubernetes.client.V1alpha3DeviceSelectorDict]]
