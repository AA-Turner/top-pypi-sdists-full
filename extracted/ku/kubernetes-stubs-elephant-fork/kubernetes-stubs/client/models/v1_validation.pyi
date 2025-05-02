import datetime
import typing

import kubernetes.client

class V1Validation:
    expression: str
    message: typing.Optional[str]
    message_expression: typing.Optional[str]
    reason: typing.Optional[str]
    
    def __init__(self, *, expression: str, message: typing.Optional[str] = ..., message_expression: typing.Optional[str] = ..., reason: typing.Optional[str] = ...) -> None:
        ...
    def to_dict(self) -> V1ValidationDict:
        ...
class V1ValidationDict(typing.TypedDict, total=False):
    expression: str
    message: typing.Optional[str]
    messageExpression: typing.Optional[str]
    reason: typing.Optional[str]
