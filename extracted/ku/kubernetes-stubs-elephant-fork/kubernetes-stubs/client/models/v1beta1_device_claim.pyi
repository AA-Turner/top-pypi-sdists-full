import datetime
import typing

import kubernetes.client

class V1beta1DeviceClaim:
    config: typing.Optional[list[kubernetes.client.V1beta1DeviceClaimConfiguration]]
    constraints: typing.Optional[list[kubernetes.client.V1beta1DeviceConstraint]]
    requests: typing.Optional[list[kubernetes.client.V1beta1DeviceRequest]]
    
    def __init__(self, *, config: typing.Optional[list[kubernetes.client.V1beta1DeviceClaimConfiguration]] = ..., constraints: typing.Optional[list[kubernetes.client.V1beta1DeviceConstraint]] = ..., requests: typing.Optional[list[kubernetes.client.V1beta1DeviceRequest]] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1DeviceClaimDict:
        ...
class V1beta1DeviceClaimDict(typing.TypedDict, total=False):
    config: typing.Optional[list[kubernetes.client.V1beta1DeviceClaimConfigurationDict]]
    constraints: typing.Optional[list[kubernetes.client.V1beta1DeviceConstraintDict]]
    requests: typing.Optional[list[kubernetes.client.V1beta1DeviceRequestDict]]
