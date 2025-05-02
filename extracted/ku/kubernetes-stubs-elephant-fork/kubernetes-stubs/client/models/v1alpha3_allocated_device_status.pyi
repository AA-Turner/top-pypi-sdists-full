import datetime
import typing

import kubernetes.client

class V1alpha3AllocatedDeviceStatus:
    conditions: typing.Optional[list[kubernetes.client.V1Condition]]
    data: typing.Optional[typing.Any]
    device: str
    driver: str
    network_data: typing.Optional[kubernetes.client.V1alpha3NetworkDeviceData]
    pool: str
    
    def __init__(self, *, conditions: typing.Optional[list[kubernetes.client.V1Condition]] = ..., data: typing.Optional[typing.Any] = ..., device: str, driver: str, network_data: typing.Optional[kubernetes.client.V1alpha3NetworkDeviceData] = ..., pool: str) -> None:
        ...
    def to_dict(self) -> V1alpha3AllocatedDeviceStatusDict:
        ...
class V1alpha3AllocatedDeviceStatusDict(typing.TypedDict, total=False):
    conditions: typing.Optional[list[kubernetes.client.V1ConditionDict]]
    data: typing.Optional[typing.Any]
    device: str
    driver: str
    networkData: typing.Optional[kubernetes.client.V1alpha3NetworkDeviceDataDict]
    pool: str
