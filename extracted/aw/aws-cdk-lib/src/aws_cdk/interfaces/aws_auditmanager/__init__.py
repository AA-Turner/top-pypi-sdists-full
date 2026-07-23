from __future__ import annotations

from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from jsii._type_checking import cached_type_hints, check_type


from ..._jsii import *

class _LazyImport:
    def __init__(self, module_name: str) -> None:
        self._module_name = module_name
        self._module: typing.Any = None
    def __getattr__(self, name: str) -> typing.Any:
        if self._module is None:
            import importlib
            self._module = importlib.import_module(self._module_name)
        return getattr(self._module, name)

if typing.TYPE_CHECKING:

    import aws_cdk.interfaces as _interfaces_8ca7e747
    import constructs as _constructs_77d1e7e8
else:

    _constructs_77d1e7e8 = _LazyImport("constructs")
    _interfaces_8ca7e747 = _LazyImport("aws_cdk.interfaces")


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_auditmanager.AssessmentReference",
    jsii_struct_bases=[],
    name_mapping={"assessment_arn": "assessmentArn", "assessment_id": "assessmentId"},
)
class AssessmentReference:
    def __init__(
        self,
        *,
        assessment_arn: builtins.str,
        assessment_id: builtins.str,
    ) -> None:
        '''A reference to a Assessment resource.

        :param assessment_arn: The ARN of the Assessment resource.
        :param assessment_id: The AssessmentId of the Assessment resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_auditmanager as interfaces_auditmanager
            
            assessment_reference = interfaces_auditmanager.AssessmentReference(
                assessment_arn="assessmentArn",
                assessment_id="assessmentId"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__de10267600e85034426d281b45a0dc9fe3aa0af3b64372d487bbf7eb03b31f1a)
            check_type(argname="argument assessment_arn", value=assessment_arn, expected_type=type_hints["assessment_arn"])
            check_type(argname="argument assessment_id", value=assessment_id, expected_type=type_hints["assessment_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "assessment_arn": assessment_arn,
            "assessment_id": assessment_id,
        }

    @builtins.property
    def assessment_arn(self) -> builtins.str:
        '''The ARN of the Assessment resource.'''
        result = self._values.get("assessment_arn")
        assert result is not None, "Required property 'assessment_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def assessment_id(self) -> builtins.str:
        '''The AssessmentId of the Assessment resource.'''
        result = self._values.get("assessment_id")
        assert result is not None, "Required property 'assessment_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssessmentReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_auditmanager.IAssessmentRef")
class IAssessmentRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a Assessment.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="assessmentRef")
    def assessment_ref(self) -> "AssessmentReference":
        '''(experimental) A reference to a Assessment resource.

        :stability: experimental
        '''
        ...


class _IAssessmentRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a Assessment.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_auditmanager.IAssessmentRef"

    @builtins.property
    @jsii.member(jsii_name="assessmentRef")
    def assessment_ref(self) -> "AssessmentReference":
        '''(experimental) A reference to a Assessment resource.

        :stability: experimental
        '''
        return typing.cast("AssessmentReference", jsii.get(self, "assessmentRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAssessmentRef).__jsii_proxy_class__ = lambda : _IAssessmentRefProxy


__all__ = [
    "AssessmentReference",
    "IAssessmentRef",
]

publication.publish()

def _typecheckingstub__de10267600e85034426d281b45a0dc9fe3aa0af3b64372d487bbf7eb03b31f1a(
    *,
    assessment_arn: builtins.str,
    assessment_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

for cls in [IAssessmentRef]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
