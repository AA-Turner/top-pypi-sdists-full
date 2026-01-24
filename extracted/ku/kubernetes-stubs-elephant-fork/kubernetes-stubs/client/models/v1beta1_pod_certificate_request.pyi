import datetime
import typing

import kubernetes.client

class V1beta1PodCertificateRequest:
    api_version: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMeta]
    spec: kubernetes.client.V1beta1PodCertificateRequestSpec
    status: typing.Optional[kubernetes.client.V1beta1PodCertificateRequestStatus]
    
    def __init__(self, *, api_version: typing.Optional[str] = ..., kind: typing.Optional[str] = ..., metadata: typing.Optional[kubernetes.client.V1ObjectMeta] = ..., spec: kubernetes.client.V1beta1PodCertificateRequestSpec, status: typing.Optional[kubernetes.client.V1beta1PodCertificateRequestStatus] = ...) -> None:
        ...
    def to_dict(self) -> V1beta1PodCertificateRequestDict:
        ...
class V1beta1PodCertificateRequestDict(typing.TypedDict, total=False):
    apiVersion: typing.Optional[str]
    kind: typing.Optional[str]
    metadata: typing.Optional[kubernetes.client.V1ObjectMetaDict]
    spec: kubernetes.client.V1beta1PodCertificateRequestSpecDict
    status: typing.Optional[kubernetes.client.V1beta1PodCertificateRequestStatusDict]
