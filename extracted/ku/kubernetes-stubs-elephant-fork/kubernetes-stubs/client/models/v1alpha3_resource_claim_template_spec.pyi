import datetime
import typing

import kubernetes.client

class V1alpha3ResourceClaimTemplateSpec:
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: kubernetes.client.V1alpha3ResourceClaimSpec
    
    def __init__(self, *, metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: kubernetes.client.V1alpha3ResourceClaimSpec) -> None:
        ...
    def to_dict(self) -> V1alpha3ResourceClaimTemplateSpecDict:
        ...
class V1alpha3ResourceClaimTemplateSpecDict(typing.TypedDict, total=False):
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: kubernetes.client.V1alpha3ResourceClaimSpecDict
