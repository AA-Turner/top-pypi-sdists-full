import datetime
import typing

import kubernetes.client

class V1ControllerRevision:
    api_version: typing.Optional[str]
    data: typing.Any
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    revision: typing.Optional[int]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., data: typing.Any, kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., revision: typing.Optional[int] = ...) -> None:
        ...
    def to_dict(self) -> V1ControllerRevisionDict:
        ...
class V1ControllerRevisionDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    data: typing.Any
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    revision: typing.Optional[int]
