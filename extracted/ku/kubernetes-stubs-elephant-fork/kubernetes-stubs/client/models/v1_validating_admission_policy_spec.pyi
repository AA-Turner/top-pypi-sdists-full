import datetime
import typing

import kubernetes.client

class V1ValidatingAdmissionPolicySpec:
    audit_annotations: typing.Optional[list[kubernetes.client.V1AuditAnnotation]]
    failure_policy: typing.Optional[str]
    match_conditions: typing.Optional[list[kubernetes.client.V1MatchCondition]]
    match_constraints: typing.Optional[kubernetes.client.V1MatchResources]
    param_kind: typing.Optional[kubernetes.client.V1ParamKind]
    validations: typing.Optional[list[kubernetes.client.V1Validation]]
    variables: typing.Optional[list[kubernetes.client.V1Variable]]
    
    def __init__(self, *, audit_annotations: typing.Optional[list[kubernetes.client.V1AuditAnnotation]] = ..., failure_policy: typing.Optional[str] = ..., match_conditions: typing.Optional[list[kubernetes.client.V1MatchCondition]] = ..., match_constraints: typing.Optional[kubernetes.client.V1MatchResources] = ..., param_kind: typing.Optional[kubernetes.client.V1ParamKind] = ..., validations: typing.Optional[list[kubernetes.client.V1Validation]] = ..., variables: typing.Optional[list[kubernetes.client.V1Variable]] = ...) -> None:
        ...
    def to_dict(self) -> V1ValidatingAdmissionPolicySpecDict:
        ...
class V1ValidatingAdmissionPolicySpecDict(typing.TypedDict, total=False):
    auditAnnotations: typing.Optional[list[kubernetes.client.V1AuditAnnotationDict]]
    failurePolicy: typing.Optional[str]
    matchConditions: typing.Optional[list[kubernetes.client.V1MatchConditionDict]]
    matchConstraints: typing.Optional[kubernetes.client.V1MatchResourcesDict]
    paramKind: typing.Optional[kubernetes.client.V1ParamKindDict]
    validations: typing.Optional[list[kubernetes.client.V1ValidationDict]]
    variables: typing.Optional[list[kubernetes.client.V1VariableDict]]
