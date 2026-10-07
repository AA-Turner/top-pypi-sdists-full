import datetime
import typing

import kubernetes.client

class V1alpha1EvictionRequest:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: kubernetes.client.V1alpha1EvictionRequestSpec
    status: typing.Optional[kubernetes.client.V1alpha1EvictionRequestStatus]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: kubernetes.client.V1alpha1EvictionRequestSpec, status: typing.Optional[kubernetes.client.V1alpha1EvictionRequestStatus] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha1EvictionRequestDict:
        ...
class V1alpha1EvictionRequestDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: kubernetes.client.V1alpha1EvictionRequestSpecDict
    status: typing.Optional[kubernetes.client.V1alpha1EvictionRequestStatusDict]
