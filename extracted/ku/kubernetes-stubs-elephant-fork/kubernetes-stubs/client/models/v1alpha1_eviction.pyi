import datetime
import typing

import kubernetes.client

class V1alpha1Eviction:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: kubernetes.client.V1alpha1EvictionSpec
    status: typing.Optional[kubernetes.client.V1alpha1EvictionStatus]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: kubernetes.client.V1alpha1EvictionSpec, status: typing.Optional[kubernetes.client.V1alpha1EvictionStatus] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha1EvictionDict:
        ...
class V1alpha1EvictionDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: kubernetes.client.V1alpha1EvictionSpecDict
    status: typing.Optional[kubernetes.client.V1alpha1EvictionStatusDict]
