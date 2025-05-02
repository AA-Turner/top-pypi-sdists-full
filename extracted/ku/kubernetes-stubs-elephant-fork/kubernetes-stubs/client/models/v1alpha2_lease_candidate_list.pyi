import datetime
import typing

import kubernetes.client

class V1alpha2LeaseCandidateList:
    api_version: typing.Optional[str]
    items: list[kubernetes.client.V1alpha2LeaseCandidate]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMeta]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., items: list[kubernetes.client.V1alpha2LeaseCandidate], kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ListMeta] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha2LeaseCandidateListDict:
        ...
class V1alpha2LeaseCandidateListDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    items: list[kubernetes.client.V1alpha2LeaseCandidateDict]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMetaDict]
