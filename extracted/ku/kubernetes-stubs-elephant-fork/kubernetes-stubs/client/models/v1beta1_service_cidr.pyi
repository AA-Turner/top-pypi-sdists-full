import datetime
import typing

import kubernetes.client

class V1beta1ServiceCIDR:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: typing.Optional[kubernetes.client.V1beta1ServiceCIDRSpec]
    status: typing.Optional[kubernetes.client.V1beta1ServiceCIDRStatus]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: typing.Optional[kubernetes.client.V1beta1ServiceCIDRSpec] = ..., status: typing.Optional[kubernetes.client.V1beta1ServiceCIDRStatus] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1ServiceCIDRDict:
        ...
class V1beta1ServiceCIDRDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: typing.Optional[kubernetes.client.V1beta1ServiceCIDRSpecDict]
    status: typing.Optional[kubernetes.client.V1beta1ServiceCIDRStatusDict]
