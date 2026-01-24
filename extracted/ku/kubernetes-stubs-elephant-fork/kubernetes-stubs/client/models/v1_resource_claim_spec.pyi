import datetime
import typing

import kubernetes.client

class V1ResourceClaimSpec:
    devices: typing.Optional[kubernetes.client.V1DeviceClaim]
    
    def __init__(self, *, devices: typing.Optional[kubernetes.client.V1DeviceClaim] = ...) -> None:
        ...
    def to_dict(self) -> V1ResourceClaimSpecDict:
        ...
class V1ResourceClaimSpecDict(typing.TypedDict, total=False):
    devices: typing.Optional[kubernetes.client.V1DeviceClaimDict]
