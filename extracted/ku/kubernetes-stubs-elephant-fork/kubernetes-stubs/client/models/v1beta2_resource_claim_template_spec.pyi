import datetime
import typing

import kubernetes.client

class V1beta2ResourceClaimTemplateSpec:
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1beta2ResourceClaimSpec]
    
    def __init__(self, *, metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: typing.Optional[kubernetes.client.V1beta2ResourceClaimSpec] = ...) -> None:
        ...
    def to_dict(self) -> V1beta2ResourceClaimTemplateSpecDict:
        ...
class V1beta2ResourceClaimTemplateSpecDict(typing.TypedDict, total=False):
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V1beta2ResourceClaimSpecDict]
