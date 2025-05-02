import datetime
import typing

import kubernetes.client

class V1beta1VolumeAttributesClass:
    api_version: typing.Optional[str]
    driver_name: str
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    parameters: typing.Optional[dict[str, str]]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., driver_name: str, kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., parameters: typing.Optional[dict[str, str]] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1VolumeAttributesClassDict:
        ...
class V1beta1VolumeAttributesClassDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    driverName: str
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    parameters: typing.Optional[dict[str, str]]
