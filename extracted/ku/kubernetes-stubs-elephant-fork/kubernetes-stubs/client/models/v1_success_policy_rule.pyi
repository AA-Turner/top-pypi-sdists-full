import datetime
import typing

import kubernetes.client

class V1SuccessPolicyRule:
    succeeded_count: typing.Optional[int]
    succeeded_indexes: typing.Optional[str]
    
    def __init__(self, *, succeeded_count: typing.Optional[int] = ..., succeeded_indexes: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1SuccessPolicyRuleDict:
        ...
class V1SuccessPolicyRuleDict(typing.TypedDict, total=False):
    succeededCount: typing.Optional[int]
    succeededIndexes: typing.Optional[str]
