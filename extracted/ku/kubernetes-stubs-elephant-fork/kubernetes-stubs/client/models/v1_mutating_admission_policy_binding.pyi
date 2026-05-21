import datetime
import typing

import kubernetes.client

class V1MutatingAdmissionPolicyBinding:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1MutatingAdmissionPolicyBindingSpec]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: typing.Optional[kubernetes.client.V1MutatingAdmissionPolicyBindingSpec] = ...) -> None:
        ...
    def to_dict(self) -> V1MutatingAdmissionPolicyBindingDict:
        ...
class V1MutatingAdmissionPolicyBindingDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V1MutatingAdmissionPolicyBindingSpecDict]
