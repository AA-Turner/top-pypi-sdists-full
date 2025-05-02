import datetime
import typing

import kubernetes.client

class V1alpha3DeviceClaim:
    config: typing.Optional[list[kubernetes.client.V1alpha3DeviceClaimConfiguration]]
    constraints: typing.Optional[list[kubernetes.client.V1alpha3DeviceConstraint]]
    requests: typing.Optional[list[kubernetes.client.V1alpha3DeviceRequest]]
    
    def __init__(self, *, config: typing.Optional[list[kubernetes.client.V1alpha3DeviceClaimConfiguration]] = ..., constraints: typing.Optional[list[kubernetes.client.V1alpha3DeviceConstraint]] = ..., requests: typing.Optional[list[kubernetes.client.V1alpha3DeviceRequest]] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3DeviceClaimDict:
        ...
class V1alpha3DeviceClaimDict(typing.TypedDict, total=False):
    config: typing.Optional[list[kubernetes.client.V1alpha3DeviceClaimConfigurationDict]]
    constraints: typing.Optional[list[kubernetes.client.V1alpha3DeviceConstraintDict]]
    requests: typing.Optional[list[kubernetes.client.V1alpha3DeviceRequestDict]]
