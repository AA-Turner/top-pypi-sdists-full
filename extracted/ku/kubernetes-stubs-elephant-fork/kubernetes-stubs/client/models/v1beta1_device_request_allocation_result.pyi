import datetime
import typing

import kubernetes.client

class V1beta1DeviceRequestAllocationResult:
    admin_access: typing.Optional[bool]
    device: str
    driver: str
    pool: str
    request: str
    
    def __init__(self, *, admin_access: typing.Optional[bool] = ..., device: str, driver: str, pool: str, request: str) -> None:
        ...
    def to_dict(self) -> V1beta1DeviceRequestAllocationResultDict:
        ...
class V1beta1DeviceRequestAllocationResultDict(typing.TypedDict, total=False):
    adminAccess: typing.Optional[bool]
    device: str
    driver: str
    pool: str
    request: str
