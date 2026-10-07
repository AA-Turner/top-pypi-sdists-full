import datetime
import typing

import kubernetes.client

class V1beta2ResourceClaim:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1beta2ResourceClaimSpec]
    status: typing.Optional[kubernetes.client.V1beta2ResourceClaimStatus]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: typing.Optional[kubernetes.client.V1beta2ResourceClaimSpec] = ..., status: typing.Optional[kubernetes.client.V1beta2ResourceClaimStatus] = ...) -> None:
        ...
    def to_dict(self) -> V1beta2ResourceClaimDict:
        ...
class V1beta2ResourceClaimDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V1beta2ResourceClaimSpecDict]
    status: typing.Optional[kubernetes.client.V1beta2ResourceClaimStatusDict]
