import datetime
import typing

import kubernetes.client

class V2beta1APIGroupDiscovery:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    versions: typing.Optional[list[kubernetes.client.V2beta1APIVersionDiscovery]]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., versions: typing.Optional[list[kubernetes.client.V2beta1APIVersionDiscovery]] = ...) -> None:
        ...
    def to_dict(self) -> V2beta1APIGroupDiscoveryDict:
        ...
class V2beta1APIGroupDiscoveryDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    versions: typing.Optional[list[kubernetes.client.V2beta1APIVersionDiscoveryDict]]
