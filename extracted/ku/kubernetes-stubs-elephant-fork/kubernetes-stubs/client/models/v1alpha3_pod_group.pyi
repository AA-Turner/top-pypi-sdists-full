import datetime
import typing

import kubernetes.client

class V1alpha3PodGroup:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: kubernetes.client.V1alpha3PodGroupSpec
    status: typing.Optional[kubernetes.client.V1alpha3PodGroupStatus]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: kubernetes.client.V1alpha3PodGroupSpec, status: typing.Optional[kubernetes.client.V1alpha3PodGroupStatus] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3PodGroupDict:
        ...
class V1alpha3PodGroupDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: kubernetes.client.V1alpha3PodGroupSpecDict
    status: typing.Optional[kubernetes.client.V1alpha3PodGroupStatusDict]
