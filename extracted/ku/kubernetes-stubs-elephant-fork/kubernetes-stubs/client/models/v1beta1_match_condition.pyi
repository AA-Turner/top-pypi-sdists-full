import datetime
import typing

import kubernetes.client

class V1beta1MatchCondition:
    expression: str
    name: str
    
    def __init__(self, *, expression: str, name: str) -> None:
        ...
    def to_dict(self) -> V1beta1MatchConditionDict:
        ...
class V1beta1MatchConditionDict(typing.TypedDict, total=False):
    expression: str
    name: str
