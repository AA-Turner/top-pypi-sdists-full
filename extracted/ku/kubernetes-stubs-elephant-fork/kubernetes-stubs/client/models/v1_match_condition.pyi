import datetime
import typing

import kubernetes.client

class V1MatchCondition:
    expression: str
    name: str
    
    def __init__(self, *, expression: str, name: str) -> None:
        ...
    def to_dict(self) -> V1MatchConditionDict:
        ...
class V1MatchConditionDict(typing.TypedDict, total=False):
    expression: str
    name: str
