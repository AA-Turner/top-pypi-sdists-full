import datetime
import typing

import kubernetes.client

class V2beta1APIGroupDiscoveryList:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMeta]
    items: list[kubernetes.client.V2beta1APIGroupDiscovery]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ListMeta] = ..., items: list[kubernetes.client.V2beta1APIGroupDiscovery]) -> None:
        ...
    def to_dict(self) -> V2beta1APIGroupDiscoveryListDict:
        ...
class V2beta1APIGroupDiscoveryListDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMetaDict]
    items: list[kubernetes.client.V2beta1APIGroupDiscoveryDict]
