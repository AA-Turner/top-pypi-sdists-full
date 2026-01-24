import datetime
import typing

import kubernetes.client

class V1ResourceClaimConsumerReference:
    api_group: typing.Optional[str]
    name: str
    resource: str
    uid: str
    
    def __init__(self, *, api_group: typing.Optional[str] = ..., name: str, resource: str, uid: str) -> None:
        ...
    def to_dict(self) -> V1ResourceClaimConsumerReferenceDict:
        ...
class V1ResourceClaimConsumerReferenceDict(typing.TypedDict, total=False):
    apiGroup: typing.Optional[str]
    name: str
    resource: str
    uid: str
