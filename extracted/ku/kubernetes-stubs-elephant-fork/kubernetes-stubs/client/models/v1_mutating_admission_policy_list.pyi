import datetime
import typing

import kubernetes.client

class V1MutatingAdmissionPolicyList:
    api_version: typing.Optional[str]
    items: list[kubernetes.client.V1MutatingAdmissionPolicy]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMeta]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., items: list[kubernetes.client.V1MutatingAdmissionPolicy], kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ListMeta] = ...) -> None:
        ...
    def to_dict(self) -> V1MutatingAdmissionPolicyListDict:
        ...
class V1MutatingAdmissionPolicyListDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    items: list[kubernetes.client.V1MutatingAdmissionPolicyDict]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMetaDict]
