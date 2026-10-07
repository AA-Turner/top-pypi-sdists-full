import datetime
import typing

import kubernetes.client

class V1PodCertificateRequestStatus:
    begin_refresh_at: typing.Optional[datetime.datetime]
    certificate_chain: typing.Optional[str]
    conditions: typing.Optional[list[kubernetes.client.V1Condition]]
    not_after: typing.Optional[datetime.datetime]
    not_before: typing.Optional[datetime.datetime]
    
    def __init__(self, *, begin_refresh_at: typing.Optional[datetime.datetime] = ..., certificate_chain: typing.Optional[str] = ..., conditions: typing.Optional[list[kubernetes.client.V1Condition]] = ..., not_after: typing.Optional[datetime.datetime] = ..., not_before: typing.Optional[datetime.datetime] = ...) -> None:
        ...
    def to_dict(self) -> V1PodCertificateRequestStatusDict:
        ...
class V1PodCertificateRequestStatusDict(typing.TypedDict, total=False):
    beginRefreshAt: typing.Optional[datetime.datetime]
    certificateChain: typing.Optional[str]
    conditions: typing.Optional[list[kubernetes.client.V1ConditionDict]]
    notAfter: typing.Optional[datetime.datetime]
    notBefore: typing.Optional[datetime.datetime]
