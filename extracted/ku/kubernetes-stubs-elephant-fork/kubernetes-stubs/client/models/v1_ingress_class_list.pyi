import datetime
import typing

import kubernetes.client

class V1IngressClassList:
    api_version: typing.Optional[str]
    items: list[kubernetes.client.V1IngressClass]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMeta]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., items: list[kubernetes.client.V1IngressClass], kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ListMeta] = ...) -> None:
        ...
    def to_dict(self) -> V1IngressClassListDict:
        ...
class V1IngressClassListDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    items: list[kubernetes.client.V1IngressClassDict]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMetaDict]
