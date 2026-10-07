import datetime
import typing

import kubernetes.client

class V1DeviceDerivedAttribute:
    expression: str
    name: str
    
    def __init__(self, *, expression: str, name: str) -> None:
        ...
    def to_dict(self) -> V1DeviceDerivedAttributeDict:
        ...
class V1DeviceDerivedAttributeDict(typing.TypedDict, total=False):
    expression: str
    name: str
