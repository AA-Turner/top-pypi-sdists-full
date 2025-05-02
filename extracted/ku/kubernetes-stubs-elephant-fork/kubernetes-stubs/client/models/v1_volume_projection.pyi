import datetime
import typing

import kubernetes.client

class V1VolumeProjection:
    cluster_trust_bundle: typing.Optional[kubernetes.client.V1ClusterTrustBundleProjection]
    config_map: typing.Optional[kubernetes.client.V1ConfigMapProjection]
    downward_api: typing.Optional[kubernetes.client.V1DownwardAPIProjection]
    secret: typing.Optional[kubernetes.client.V1SecretProjection]
    service_account_token: typing.Optional[kubernetes.client.V1ServiceAccountTokenProjection]
    
    def __init__(self, *, cluster_trust_bundle: typing.Optional[kubernetes.client.V1ClusterTrustBundleProjection] = ..., config_map: typing.Optional[kubernetes.client.V1ConfigMapProjection] = ..., downward_api: typing.Optional[kubernetes.client.V1DownwardAPIProjection] = ..., secret: typing.Optional[kubernetes.client.V1SecretProjection] = ..., service_account_token: typing.Optional[kubernetes.client.V1ServiceAccountTokenProjection] = ...) -> None:
        ...
    def to_dict(self) -> V1VolumeProjectionDict:
        ...
class V1VolumeProjectionDict(typing.TypedDict, total=False):
    clusterTrustBundle: typing.Optional[kubernetes.client.V1ClusterTrustBundleProjectionDict]
    configMap: typing.Optional[kubernetes.client.V1ConfigMapProjectionDict]
    downwardAPI: typing.Optional[kubernetes.client.V1DownwardAPIProjectionDict]
    secret: typing.Optional[kubernetes.client.V1SecretProjectionDict]
    serviceAccountToken: typing.Optional[kubernetes.client.V1ServiceAccountTokenProjectionDict]
