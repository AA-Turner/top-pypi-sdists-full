import datetime
import typing

import kubernetes.client

class V1beta1ResourceClaimSpec:
    devices: typing.Optional[kubernetes.client.V1beta1DeviceClaim]
    
    def __init__(self, *, devices: typing.Optional[kubernetes.client.V1beta1DeviceClaim] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1ResourceClaimSpecDict:
        ...
class V1beta1ResourceClaimSpecDict(typing.TypedDict, total=False):
    devices: typing.Optional[kubernetes.client.V1beta1DeviceClaimDict]
