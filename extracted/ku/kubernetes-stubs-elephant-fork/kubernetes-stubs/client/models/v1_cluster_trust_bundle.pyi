import datetime
import typing

import kubernetes.client

class V1ClusterTrustBundle:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: kubernetes.client.V1ClusterTrustBundleSpec
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: kubernetes.client.V1ClusterTrustBundleSpec) -> None:
        ...
    def to_dict(self) -> V1ClusterTrustBundleDict:
        ...
class V1ClusterTrustBundleDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: kubernetes.client.V1ClusterTrustBundleSpecDict
