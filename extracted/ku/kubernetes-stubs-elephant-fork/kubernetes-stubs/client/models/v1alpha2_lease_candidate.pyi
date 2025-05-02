import datetime
import typing

import kubernetes.client

class V1alpha2LeaseCandidate:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1alpha2LeaseCandidateSpec]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: typing.Optional[kubernetes.client.V1alpha2LeaseCandidateSpec] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha2LeaseCandidateDict:
        ...
class V1alpha2LeaseCandidateDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V1alpha2LeaseCandidateSpecDict]
