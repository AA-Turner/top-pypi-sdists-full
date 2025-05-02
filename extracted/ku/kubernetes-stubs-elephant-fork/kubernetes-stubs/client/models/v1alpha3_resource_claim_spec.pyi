import datetime
import typing

import kubernetes.client

class V1alpha3ResourceClaimSpec:
    devices: typing.Optional[kubernetes.client.V1alpha3DeviceClaim]
    
    def __init__(self, *, devices: typing.Optional[kubernetes.client.V1alpha3DeviceClaim] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3ResourceClaimSpecDict:
        ...
class V1alpha3ResourceClaimSpecDict(typing.TypedDict, total=False):
    devices: typing.Optional[kubernetes.client.V1alpha3DeviceClaimDict]
