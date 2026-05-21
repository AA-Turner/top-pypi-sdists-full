import datetime
import typing

import kubernetes.client

class V2APIVersionDiscovery:
    version: str
    resources: typing.Optional[list[kubernetes.client.V2APIResourceDiscovery]]
    freshness: typing.Optional[str]
    
    def __init__(self, *, version: str, resources: typing.Optional[list[kubernetes.client.V2APIResourceDiscovery]] = ..., freshness: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V2APIVersionDiscoveryDict:
        ...
class V2APIVersionDiscoveryDict(typing.TypedDict, total=False):
    version: str
    resources: typing.Optional[list[kubernetes.client.V2APIResourceDiscoveryDict]]
    freshness: typing.Optional[str]
