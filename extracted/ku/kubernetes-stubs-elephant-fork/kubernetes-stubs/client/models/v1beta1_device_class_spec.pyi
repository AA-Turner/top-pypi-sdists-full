import datetime
import typing

import kubernetes.client

class V1beta1DeviceClassSpec:
    config: typing.Optional[list[kubernetes.client.V1beta1DeviceClassConfiguration]]
    selectors: typing.Optional[list[kubernetes.client.V1beta1DeviceSelector]]
    
    def __init__(self, *, config: typing.Optional[list[kubernetes.client.V1beta1DeviceClassConfiguration]] = ..., selectors: typing.Optional[list[kubernetes.client.V1beta1DeviceSelector]] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1DeviceClassSpecDict:
        ...
class V1beta1DeviceClassSpecDict(typing.TypedDict, total=False):
    config: typing.Optional[list[kubernetes.client.V1beta1DeviceClassConfigurationDict]]
    selectors: typing.Optional[list[kubernetes.client.V1beta1DeviceSelectorDict]]
