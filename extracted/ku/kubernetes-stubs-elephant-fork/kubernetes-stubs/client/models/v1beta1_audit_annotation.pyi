import datetime
import typing

import kubernetes.client

class V1beta1AuditAnnotation:
    key: str
    value_expression: str
    
    def __init__(self, *, key: str, value_expression: str) -> None:
        ...
    def to_dict(self) -> V1beta1AuditAnnotationDict:
        ...
class V1beta1AuditAnnotationDict(typing.TypedDict, total=False):
    key: str
    valueExpression: str
