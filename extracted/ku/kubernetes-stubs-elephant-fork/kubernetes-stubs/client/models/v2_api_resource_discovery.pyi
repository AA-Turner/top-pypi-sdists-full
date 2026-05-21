import datetime
import typing

import kubernetes.client

class V2APIResourceDiscovery:
    resource: str
    response_kind: typing.Optional[kubernetes.client.IoK8sApimachineryPkgApisMetaV1GroupVersionKind]
    scope: str
    singular_resource: str
    verbs: list[str]
    short_names: typing.Optional[list[str]]
    categories: typing.Optional[list[str]]
    subresources: typing.Optional[list[kubernetes.client.V2APISubresourceDiscovery]]
    
    def __init__(self, *, resource: str, response_kind: typing.Optional[kubernetes.client.IoK8sApimachineryPkgApisMetaV1GroupVersionKind] = ..., scope: str, singular_resource: str, verbs: list[str], short_names: typing.Optional[list[str]] = ..., categories: typing.Optional[list[str]] = ..., subresources: typing.Optional[list[kubernetes.client.V2APISubresourceDiscovery]] = ...) -> None:
        ...
    def to_dict(self) -> V2APIResourceDiscoveryDict:
        ...
class V2APIResourceDiscoveryDict(typing.TypedDict, total=False):
    resource: str
    responseKind: typing.Optional[kubernetes.client.IoK8sApimachineryPkgApisMetaV1GroupVersionKindDict]
    scope: str
    singularResource: str
    verbs: list[str]
    shortNames: typing.Optional[list[str]]
    categories: typing.Optional[list[str]]
    subresources: typing.Optional[list[kubernetes.client.V2APISubresourceDiscoveryDict]]
