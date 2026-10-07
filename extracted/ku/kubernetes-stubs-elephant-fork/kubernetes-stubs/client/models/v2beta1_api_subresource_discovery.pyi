import datetime
import typing

import kubernetes.client

class V2beta1APISubresourceDiscovery:
    subresource: str
    response_kind: typing.Optional[kubernetes.client.V1GroupVersionKind]
    verbs: list[str]
    accepted_types: typing.Optional[list[kubernetes.client.V1GroupVersionKind]]
    
    def __init__(self, *, subresource: str, response_kind: typing.Optional[kubernetes.client.V1GroupVersionKind] = ..., verbs: list[str], accepted_types: typing.Optional[list[kubernetes.client.V1GroupVersionKind]] = ...) -> None:
        ...
    def to_dict(self) -> V2beta1APISubresourceDiscoveryDict:
        ...
class V2beta1APISubresourceDiscoveryDict(typing.TypedDict, total=False):
    subresource: str
    responseKind: typing.Optional[kubernetes.client.V1GroupVersionKindDict]
    verbs: list[str]
    acceptedTypes: typing.Optional[list[kubernetes.client.V1GroupVersionKindDict]]
