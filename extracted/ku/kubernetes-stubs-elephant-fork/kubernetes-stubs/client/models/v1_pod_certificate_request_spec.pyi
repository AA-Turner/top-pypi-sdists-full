import datetime
import typing

import kubernetes.client

class V1PodCertificateRequestSpec:
    max_expiration_seconds: typing.Optional[int]
    node_name: str
    node_uid: str
    pod_name: str
    pod_uid: str
    service_account_name: str
    service_account_uid: str
    signer_name: str
    stub_pkcs10_request: str
    unverified_user_annotations: typing.Optional[dict[str, str]]
    
    def __init__(self, *, max_expiration_seconds: typing.Optional[int] = ..., node_name: str, node_uid: str, pod_name: str, pod_uid: str, service_account_name: str, service_account_uid: str, signer_name: str, stub_pkcs10_request: str, unverified_user_annotations: typing.Optional[dict[str, str]] = ...) -> None:
        ...
    def to_dict(self) -> V1PodCertificateRequestSpecDict:
        ...
class V1PodCertificateRequestSpecDict(typing.TypedDict, total=False):
    maxExpirationSeconds: typing.Optional[int]
    nodeName: str
    nodeUID: str
    podName: str
    podUID: str
    serviceAccountName: str
    serviceAccountUID: str
    signerName: str
    stubPKCS10Request: str
    unverifiedUserAnnotations: typing.Optional[dict[str, str]]
