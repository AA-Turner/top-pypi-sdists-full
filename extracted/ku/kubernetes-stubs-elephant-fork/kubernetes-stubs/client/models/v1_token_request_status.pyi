import datetime
import typing

import kubernetes.client

class V1TokenRequestStatus:
    expiration_timestamp: typing.Optional[datetime.datetime]
    token: typing.Optional[str]
    
    def __init__(self, *, expiration_timestamp: typing.Optional[datetime.datetime] = ..., token: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1TokenRequestStatusDict:
        ...
class V1TokenRequestStatusDict(typing.TypedDict, total=False):
    expirationTimestamp: typing.Optional[datetime.datetime]
    token: typing.Optional[str]
