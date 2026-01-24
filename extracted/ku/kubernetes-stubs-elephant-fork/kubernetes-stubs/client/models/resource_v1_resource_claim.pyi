import datetime
import typing

import kubernetes.client

class ResourceV1ResourceClaim:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: kubernetes.client.V1ResourceClaimSpec
    status: typing.Optional[kubernetes.client.V1ResourceClaimStatus]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: kubernetes.client.V1ResourceClaimSpec, status: typing.Optional[kubernetes.client.V1ResourceClaimStatus] = ...) -> None:
        ...
    def to_dict(self) -> ResourceV1ResourceClaimDict:
        ...
class ResourceV1ResourceClaimDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: kubernetes.client.V1ResourceClaimSpecDict
    status: typing.Optional[kubernetes.client.V1ResourceClaimStatusDict]
