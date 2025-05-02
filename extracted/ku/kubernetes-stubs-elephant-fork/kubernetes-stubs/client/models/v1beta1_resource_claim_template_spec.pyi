import datetime
import typing

import kubernetes.client

class V1beta1ResourceClaimTemplateSpec:
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: kubernetes.client.V1beta1ResourceClaimSpec
    
    def __init__(self, *, metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: kubernetes.client.V1beta1ResourceClaimSpec) -> None:
        ...
    def to_dict(self) -> V1beta1ResourceClaimTemplateSpecDict:
        ...
class V1beta1ResourceClaimTemplateSpecDict(typing.TypedDict, total=False):
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: kubernetes.client.V1beta1ResourceClaimSpecDict
