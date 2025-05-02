import datetime
import typing

import kubernetes.client

class V1beta1ServiceCIDRList:
    api_version: typing.Optional[str]
    items: list[kubernetes.client.V1beta1ServiceCIDR]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMeta]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., items: list[kubernetes.client.V1beta1ServiceCIDR], kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ListMeta] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1ServiceCIDRListDict:
        ...
class V1beta1ServiceCIDRListDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    items: list[kubernetes.client.V1beta1ServiceCIDRDict]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMetaDict]
