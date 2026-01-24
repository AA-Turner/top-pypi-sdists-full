import datetime
import typing

import kubernetes.client

class V1ResourceClaimTemplateList:
    api_version: typing.Optional[str]
    items: list[kubernetes.client.V1ResourceClaimTemplate]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMeta]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., items: list[kubernetes.client.V1ResourceClaimTemplate], kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ListMeta] = ...) -> None:
        ...
    def to_dict(self) -> V1ResourceClaimTemplateListDict:
        ...
class V1ResourceClaimTemplateListDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    items: list[kubernetes.client.V1ResourceClaimTemplateDict]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMetaDict]
