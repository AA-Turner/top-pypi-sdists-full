import datetime
import typing

import kubernetes.client

class V1beta1MutatingAdmissionPolicy:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1beta1MutatingAdmissionPolicySpec]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: typing.Optional[kubernetes.client.V1beta1MutatingAdmissionPolicySpec] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1MutatingAdmissionPolicyDict:
        ...
class V1beta1MutatingAdmissionPolicyDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V1beta1MutatingAdmissionPolicySpecDict]
