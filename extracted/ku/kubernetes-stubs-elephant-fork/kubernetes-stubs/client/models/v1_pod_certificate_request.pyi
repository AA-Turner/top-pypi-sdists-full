import datetime
import typing

import kubernetes.client

class V1PodCertificateRequest:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: kubernetes.client.V1PodCertificateRequestSpec
    status: typing.Optional[kubernetes.client.V1PodCertificateRequestStatus]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: kubernetes.client.V1PodCertificateRequestSpec, status: typing.Optional[kubernetes.client.V1PodCertificateRequestStatus] = ...) -> None:
        ...
    def to_dict(self) -> V1PodCertificateRequestDict:
        ...
class V1PodCertificateRequestDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: kubernetes.client.V1PodCertificateRequestSpecDict
    status: typing.Optional[kubernetes.client.V1PodCertificateRequestStatusDict]
