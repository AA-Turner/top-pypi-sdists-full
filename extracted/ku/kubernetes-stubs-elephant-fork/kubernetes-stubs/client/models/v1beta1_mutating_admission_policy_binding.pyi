import datetime
import typing

import kubernetes.client

class V1beta1MutatingAdmissionPolicyBinding:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1beta1MutatingAdmissionPolicyBindingSpec]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: typing.Optional[kubernetes.client.V1beta1MutatingAdmissionPolicyBindingSpec] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1MutatingAdmissionPolicyBindingDict:
        ...
class V1beta1MutatingAdmissionPolicyBindingDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V1beta1MutatingAdmissionPolicyBindingSpecDict]
