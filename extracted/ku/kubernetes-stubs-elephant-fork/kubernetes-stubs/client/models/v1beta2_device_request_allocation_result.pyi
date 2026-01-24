import datetime
import typing

import kubernetes.client

class V1beta2DeviceRequestAllocationResult:
    admin_access: typing.Optional[bool]
    binding_conditions: typing.Optional[list[str]]
    binding_failure_conditions: typing.Optional[list[str]]
    consumed_capacity: typing.Optional[dict[str, str]]
    device: str
    driver: str
    pool: str
    request: str
    share_id: typing.Optional[str]
    tolerations: typing.Optional[list[kubernetes.client.V1beta2DeviceToleration]]
    
    def __init__(self, *, admin_access: typing.Optional[bool] = ..., binding_conditions: typing.Optional[list[str]] = ..., binding_failure_conditions: typing.Optional[list[str]] = ..., consumed_capacity: typing.Optional[dict[str, str]] = ..., device: str, driver: str, pool: str, request: str, share_id: typing.Optional[str] = ..., tolerations: typing.Optional[list[kubernetes.client.V1beta2DeviceToleration]] = ...) -> None:
        ...
    def to_dict(self) -> V1beta2DeviceRequestAllocationResultDict:
        ...
class V1beta2DeviceRequestAllocationResultDict(typing.TypedDict, total=False):
    adminAccess: typing.Optional[bool]
    bindingConditions: typing.Optional[list[str]]
    bindingFailureConditions: typing.Optional[list[str]]
    consumedCapacity: typing.Optional[dict[str, str]]
    device: str
    driver: str
    pool: str
    request: str
    shareID: typing.Optional[str]
    tolerations: typing.Optional[list[kubernetes.client.V1beta2DeviceTolerationDict]]
