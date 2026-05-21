import datetime
import typing

import kubernetes.client

class V2APISubresourceDiscovery:
    subresource: str
    response_kind: typing.Optional[kubernetes.client.IoK8sApimachineryPkgApisMetaV1GroupVersionKind]
    accepted_types: typing.Optional[list[kubernetes.client.IoK8sApimachineryPkgApisMetaV1GroupVersionKind]]
    verbs: list[str]
    
    def __init__(self, *, subresource: str, response_kind: typing.Optional[kubernetes.client.IoK8sApimachineryPkgApisMetaV1GroupVersionKind] = ..., accepted_types: typing.Optional[list[kubernetes.client.IoK8sApimachineryPkgApisMetaV1GroupVersionKind]] = ..., verbs: list[str]) -> None:
        ...
    def to_dict(self) -> V2APISubresourceDiscoveryDict:
        ...
class V2APISubresourceDiscoveryDict(typing.TypedDict, total=False):
    subresource: str
    responseKind: typing.Optional[kubernetes.client.IoK8sApimachineryPkgApisMetaV1GroupVersionKindDict]
    acceptedTypes: typing.Optional[list[kubernetes.client.IoK8sApimachineryPkgApisMetaV1GroupVersionKindDict]]
    verbs: list[str]
