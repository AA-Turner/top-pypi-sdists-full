import datetime
import typing

import kubernetes.client

class V1beta1ExpressionWarning:
    field_ref: str
    warning: str
    
    def __init__(self, *, field_ref: str, warning: str) -> None:
        ...
    def to_dict(self) -> V1beta1ExpressionWarningDict:
        ...
class V1beta1ExpressionWarningDict(typing.TypedDict, total=False):
    fieldRef: str
    warning: str
