import datetime
import typing

import kubernetes.client

class V1beta1PodGroup:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: kubernetes.client.V1beta1PodGroupSpec
    status: typing.Optional[kubernetes.client.V1beta1PodGroupStatus]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: kubernetes.client.V1beta1PodGroupSpec, status: typing.Optional[kubernetes.client.V1beta1PodGroupStatus] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1PodGroupDict:
        ...
class V1beta1PodGroupDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: kubernetes.client.V1beta1PodGroupSpecDict
    status: typing.Optional[kubernetes.client.V1beta1PodGroupStatusDict]
