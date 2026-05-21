import datetime
import typing

import kubernetes.client

class V2beta1APIVersionDiscovery:
    version: str
    resources: typing.Optional[list[kubernetes.client.V2beta1APIResourceDiscovery]]
    freshness: typing.Optional[str]
    
    def __init__(self, *, version: str, resources: typing.Optional[list[kubernetes.client.V2beta1APIResourceDiscovery]] = ..., freshness: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V2beta1APIVersionDiscoveryDict:
        ...
class V2beta1APIVersionDiscoveryDict(typing.TypedDict, total=False):
    version: str
    resources: typing.Optional[list[kubernetes.client.V2beta1APIResourceDiscoveryDict]]
    freshness: typing.Optional[str]
