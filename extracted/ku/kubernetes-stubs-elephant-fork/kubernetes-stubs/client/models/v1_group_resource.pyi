import datetime
import typing

import kubernetes.client

class V1GroupResource:
    group: str
    resource: str
    
    def __init__(self, *, group: str, resource: str) -> None:
        ...
    def to_dict(self) -> V1GroupResourceDict:
        ...
class V1GroupResourceDict(typing.TypedDict, total=False):
    group: str
    resource: str
