import datetime
import typing

import kubernetes.client

class V1alpha1MutatingAdmissionPolicyBinding:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1alpha1MutatingAdmissionPolicyBindingSpec]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: typing.Optional[kubernetes.client.V1alpha1MutatingAdmissionPolicyBindingSpec] = ...) -> None:
        ...
    def to_dict(self) -> V1alpha1MutatingAdmissionPolicyBindingDict:
        ...
class V1alpha1MutatingAdmissionPolicyBindingDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V1alpha1MutatingAdmissionPolicyBindingSpecDict]
