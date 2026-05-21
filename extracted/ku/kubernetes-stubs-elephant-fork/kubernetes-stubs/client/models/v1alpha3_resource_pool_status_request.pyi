import datetime
import typing

import kubernetes.client

class V1alpha3ResourcePoolStatusRequest:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: kubernetes.client.V1ObjectMeta
    spec: kubernetes.client.V1alpha3ResourcePoolStatusRequestSpec
    status: typing.Optional[kubernetes.client.V1alpha3ResourcePoolStatusRequestStatus]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: kubernetes.client.V1ObjectMeta, spec: kubernetes.client.V1alpha3ResourcePoolStatusRequestSpec, status: typing.Optional[kubernetes.client.V1alpha3ResourcePoolStatusRequestStatus] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha3ResourcePoolStatusRequestDict:
        ...
class V1alpha3ResourcePoolStatusRequestDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: kubernetes.client.V1ObjectMetaDict
    spec: kubernetes.client.V1alpha3ResourcePoolStatusRequestSpecDict
    status: typing.Optional[kubernetes.client.V1alpha3ResourcePoolStatusRequestStatusDict]
