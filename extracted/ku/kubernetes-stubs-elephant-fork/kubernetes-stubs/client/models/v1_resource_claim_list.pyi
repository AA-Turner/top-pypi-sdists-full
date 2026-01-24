import datetime
import typing

import kubernetes.client

class V1ResourceClaimList:
    api_version: typing.Optional[str]
    items: list[kubernetes.client.ResourceV1ResourceClaim]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMeta]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., items: list[kubernetes.client.ResourceV1ResourceClaim], kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ListMeta] = ...) -> None:
        ...
    def to_dict(self) -> V1ResourceClaimListDict:
        ...
class V1ResourceClaimListDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    items: list[kubernetes.client.ResourceV1ResourceClaimDict]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMetaDict]
