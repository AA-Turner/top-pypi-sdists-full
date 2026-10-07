import datetime
import typing

import kubernetes.client

class V1alpha3PodGroupList:
    api_version: typing.Optional[str]
    items: list[kubernetes.client.V1alpha3PodGroup]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMeta]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., items: list[kubernetes.client.V1alpha3PodGroup], kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ListMeta] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3PodGroupListDict:
        ...
class V1alpha3PodGroupListDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    items: list[kubernetes.client.V1alpha3PodGroupDict]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMetaDict]
