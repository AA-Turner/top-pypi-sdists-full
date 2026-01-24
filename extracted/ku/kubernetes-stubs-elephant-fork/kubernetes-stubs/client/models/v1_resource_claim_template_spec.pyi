import datetime
import typing

import kubernetes.client

class V1ResourceClaimTemplateSpec:
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: kubernetes.client.V1ResourceClaimSpec
    
    def __init__(self, *, metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: kubernetes.client.V1ResourceClaimSpec) -> None:
        ...
    def to_dict(self) -> V1ResourceClaimTemplateSpecDict:
        ...
class V1ResourceClaimTemplateSpecDict(typing.TypedDict, total=False):
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: kubernetes.client.V1ResourceClaimSpecDict
