import datetime
import typing

import kubernetes.client

class V1MutatingAdmissionPolicy:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1MutatingAdmissionPolicySpec]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: typing.Optional[kubernetes.client.V1MutatingAdmissionPolicySpec] = ...) -> None:
        ...
    def to_dict(self) -> V1MutatingAdmissionPolicyDict:
        ...
class V1MutatingAdmissionPolicyDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V1MutatingAdmissionPolicySpecDict]
