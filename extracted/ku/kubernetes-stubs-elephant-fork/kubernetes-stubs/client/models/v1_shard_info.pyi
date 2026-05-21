import datetime
import typing

import kubernetes.client

class V1ShardInfo:
    selector: str
    
    def __init__(self, *, selector: str) -> None:
        ...
    def to_dict(self) -> V1ShardInfoDict:
        ...
class V1ShardInfoDict(typing.TypedDict, total=False):
    selector: str
