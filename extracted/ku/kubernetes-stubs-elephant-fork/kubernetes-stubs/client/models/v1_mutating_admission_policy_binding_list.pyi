import datetime
import typing

import kubernetes.client

class V1MutatingAdmissionPolicyBindingList:
    api_version: typing.Optional[str]
    items: list[kubernetes.client.V1MutatingAdmissionPolicyBinding]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMeta]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., items: list[kubernetes.client.V1MutatingAdmissionPolicyBinding], kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ListMeta] = ...) -> None:
        ...
    def to_dict(self) -> V1MutatingAdmissionPolicyBindingListDict:
        ...
class V1MutatingAdmissionPolicyBindingListDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    items: list[kubernetes.client.V1MutatingAdmissionPolicyBindingDict]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMetaDict]
