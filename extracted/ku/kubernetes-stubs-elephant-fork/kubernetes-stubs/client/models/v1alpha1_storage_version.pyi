import datetime
import typing

import kubernetes.client

class V1alpha1StorageVersion:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: kubernetes.client.V1ObjectMeta
    spec: typing.Optional[typing.Any]
    status: typing.Optional[kubernetes.client.V1alpha1StorageVersionStatus]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: kubernetes.client.V1ObjectMeta, spec: typing.Optional[typing.Any] = ..., status: typing.Optional[kubernetes.client.V1alpha1StorageVersionStatus] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha1StorageVersionDict:
        ...
class V1alpha1StorageVersionDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: kubernetes.client.V1ObjectMetaDict
    spec: typing.Optional[typing.Any]
    status: typing.Optional[kubernetes.client.V1alpha1StorageVersionStatusDict]
