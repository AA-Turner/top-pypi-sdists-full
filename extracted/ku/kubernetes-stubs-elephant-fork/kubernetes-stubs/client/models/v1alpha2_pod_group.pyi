import datetime
import typing

import kubernetes.client

class V1alpha2PodGroup:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: kubernetes.client.V1alpha2PodGroupSpec
    status: typing.Optional[kubernetes.client.V1alpha2PodGroupStatus]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: kubernetes.client.V1alpha2PodGroupSpec, status: typing.Optional[kubernetes.client.V1alpha2PodGroupStatus] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha2PodGroupDict:
        ...
class V1alpha2PodGroupDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: kubernetes.client.V1alpha2PodGroupSpecDict
    status: typing.Optional[kubernetes.client.V1alpha2PodGroupStatusDict]
