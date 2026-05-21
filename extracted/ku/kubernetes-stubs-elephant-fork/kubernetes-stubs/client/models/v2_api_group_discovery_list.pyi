import datetime
import typing

import kubernetes.client

class V2APIGroupDiscoveryList:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMeta]
    items: list[kubernetes.client.V2APIGroupDiscovery]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ListMeta] = ..., items: list[kubernetes.client.V2APIGroupDiscovery]) -> None:
        ...
    def to_dict(self) -> V2APIGroupDiscoveryListDict:
        ...
class V2APIGroupDiscoveryListDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMetaDict]
    items: list[kubernetes.client.V2APIGroupDiscoveryDict]
