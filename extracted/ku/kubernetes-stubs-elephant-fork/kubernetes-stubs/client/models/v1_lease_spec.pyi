import datetime
import typing

import kubernetes.client

class V1LeaseSpec:
    acquire_time: typing.Optional[datetime.datetime]
    holder_identity: typing.Optional[str]
    lease_duration_seconds: typing.Optional[int]
    lease_transitions: typing.Optional[int]
    preferred_holder: typing.Optional[str]
    renew_time: typing.Optional[datetime.datetime]
    strategy: typing.Optional[str]
    
    def __init__(self, *, acquire_time: typing.Optional[datetime.datetime] = ..., holder_identity: typing.Optional[str] = ..., lease_duration_seconds: typing.Optional[int] = ..., lease_transitions: typing.Optional[int] = ..., preferred_holder: typing.Optional[str] = ..., renew_time: typing.Optional[datetime.datetime] = ..., strategy: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1LeaseSpecDict:
        ...
class V1LeaseSpecDict(typing.TypedDict, total=False):
    acquireTime: typing.Optional[datetime.datetime]
    holderIdentity: typing.Optional[str]
    leaseDurationSeconds: typing.Optional[int]
    leaseTransitions: typing.Optional[int]
    preferredHolder: typing.Optional[str]
    renewTime: typing.Optional[datetime.datetime]
    strategy: typing.Optional[str]
