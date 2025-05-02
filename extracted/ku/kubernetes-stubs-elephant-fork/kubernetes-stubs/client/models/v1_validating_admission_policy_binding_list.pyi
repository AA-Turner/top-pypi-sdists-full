import datetime
import typing

import kubernetes.client

class V1ValidatingAdmissionPolicyBindingList:
    api_version: typing.Optional[str]
    items: list[kubernetes.client.V1ValidatingAdmissionPolicyBinding]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMeta]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., items: list[kubernetes.client.V1ValidatingAdmissionPolicyBinding], kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ListMeta] = ...) -> None:
        ...
    def to_dict(self) -> V1ValidatingAdmissionPolicyBindingListDict:
        ...
class V1ValidatingAdmissionPolicyBindingListDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    items: list[kubernetes.client.V1ValidatingAdmissionPolicyBindingDict]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ListMetaDict]
