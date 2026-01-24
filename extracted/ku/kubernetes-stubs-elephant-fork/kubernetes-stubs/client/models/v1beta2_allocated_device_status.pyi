import datetime
import typing

import kubernetes.client

class V1beta2AllocatedDeviceStatus:
    conditions: typing.Optional[list[kubernetes.client.V1Condition]]
    data: typing.Optional[typing.Any]
    device: str
    driver: str
    network_data: typing.Optional[kubernetes.client.V1beta2NetworkDeviceData]
    pool: str
    share_id: typing.Optional[str]
    
    def __init__(self, *, conditions: typing.Optional[list[kubernetes.client.V1Condition]] = ..., data: typing.Optional[typing.Any] = ..., device: str, driver: str, network_data: typing.Optional[kubernetes.client.V1beta2NetworkDeviceData] = ..., pool: str, share_id: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1beta2AllocatedDeviceStatusDict:
        ...
class V1beta2AllocatedDeviceStatusDict(typing.TypedDict, total=False):
    conditions: typing.Optional[list[kubernetes.client.V1ConditionDict]]
    data: typing.Optional[typing.Any]
    device: str
    driver: str
    networkData: typing.Optional[kubernetes.client.V1beta2NetworkDeviceDataDict]
    pool: str
    shareID: typing.Optional[str]
