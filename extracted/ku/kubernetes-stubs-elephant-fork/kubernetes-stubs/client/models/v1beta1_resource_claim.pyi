import datetime
import typing

import kubernetes.client

class V1beta1ResourceClaim:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: kubernetes.client.V1beta1ResourceClaimSpec
    status: typing.Optional[kubernetes.client.V1beta1ResourceClaimStatus]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: kubernetes.client.V1beta1ResourceClaimSpec, status: typing.Optional[kubernetes.client.V1beta1ResourceClaimStatus] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1ResourceClaimDict:
        ...
class V1beta1ResourceClaimDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: kubernetes.client.V1beta1ResourceClaimSpecDict
    status: typing.Optional[kubernetes.client.V1beta1ResourceClaimStatusDict]
