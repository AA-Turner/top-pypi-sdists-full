import datetime
import typing

import kubernetes.client

class V1FileKeySelector:
    key: str
    optional: typing.Optional[bool]
    path: str
    volume_name: str
    
    def __init__(self, *, key: str, optional: typing.Optional[bool] = ..., path: str, volume_name: str) -> None:
        ...
    def to_dict(self) -> V1FileKeySelectorDict:
        ...
class V1FileKeySelectorDict(typing.TypedDict, total=False):
    key: str
    optional: typing.Optional[bool]
    path: str
    volumeName: str
