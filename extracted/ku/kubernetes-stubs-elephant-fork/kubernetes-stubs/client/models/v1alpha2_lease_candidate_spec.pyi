import datetime
import typing

import kubernetes.client

class V1alpha2LeaseCandidateSpec:
    binary_version: str
    emulation_version: typing.Optional[str]
    lease_name: str
    ping_time: typing.Optional[datetime.datetime]
    renew_time: typing.Optional[datetime.datetime]
    strategy: str
    
    def __init__(self, *, binary_version: str, emulation_version: typing.Optional[str] = ..., lease_name: str, ping_time: typing.Optional[datetime.datetime] = ..., renew_time: typing.Optional[datetime.datetime] = ..., strategy: str) -> None:
        ...
    def to_dict(self) -> V1alpha2LeaseCandidateSpecDict:
        ...
class V1alpha2LeaseCandidateSpecDict(typing.TypedDict, total=False):
    binaryVersion: str
    emulationVersion: typing.Optional[str]
    leaseName: str
    pingTime: typing.Optional[datetime.datetime]
    renewTime: typing.Optional[datetime.datetime]
    strategy: str
