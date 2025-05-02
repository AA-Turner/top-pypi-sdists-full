import datetime
import typing

import kubernetes.client

class V1ClusterTrustBundleProjection:
    label_selector: typing.Optional[kubernetes.client.V1LabelSelector]
    name: typing.Optional[str]
    optional: typing.Optional[bool]
    path: str
    signer_name: typing.Optional[str]
    
    def __init__(self, *, label_selector: typing.Optional[kubernetes.client.V1LabelSelector] = ..., name: typing.Optional[str] = ..., optional: typing.Optional[bool] = ..., path: str, signer_name: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1ClusterTrustBundleProjectionDict:
        ...
class V1ClusterTrustBundleProjectionDict(typing.TypedDict, total=False):
    labelSelector: typing.Optional[kubernetes.client.V1LabelSelectorDict]
    name: typing.Optional[str]
    optional: typing.Optional[bool]
    path: str
    signerName: typing.Optional[str]
