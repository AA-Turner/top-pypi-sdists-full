import datetime
import typing

import kubernetes.client

class V1beta1LeaseCandidate:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: kubernetes.client.V1beta1LeaseCandidateSpec
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: kubernetes.client.V1beta1LeaseCandidateSpec) -> None:
        ...
    def to_dict(self) -> V1beta1LeaseCandidateDict:
        ...
class V1beta1LeaseCandidateDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: kubernetes.client.V1beta1LeaseCandidateSpecDict
