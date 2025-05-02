import datetime
import typing

import kubernetes.client

class V1alpha3ResourceClaimTemplateList:
    api_version: typing.Optional[str]
    items: list[kubernetes.client.V1alpha3ResourceClaimTemplate]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMeta]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., items: list[kubernetes.client.V1alpha3ResourceClaimTemplate], kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ListMeta] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3ResourceClaimTemplateListDict:
        ...
class V1alpha3ResourceClaimTemplateListDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    items: list[kubernetes.client.V1alpha3ResourceClaimTemplateDict]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMetaDict]
