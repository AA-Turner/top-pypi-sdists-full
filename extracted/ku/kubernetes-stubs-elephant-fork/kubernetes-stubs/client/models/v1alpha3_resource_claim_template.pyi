import datetime
import typing

import kubernetes.client

class V1alpha3ResourceClaimTemplate:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: kubernetes.client.V1alpha3ResourceClaimTemplateSpec
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: kubernetes.client.V1alpha3ResourceClaimTemplateSpec) -> None:
        ...
    def to_dict(self) -> V1alpha3ResourceClaimTemplateDict:
        ...
class V1alpha3ResourceClaimTemplateDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: kubernetes.client.V1alpha3ResourceClaimTemplateSpecDict
