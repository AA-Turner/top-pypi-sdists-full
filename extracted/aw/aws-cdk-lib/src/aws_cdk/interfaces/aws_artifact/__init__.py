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


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_artifact.IReportRef")
class IReportRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a Report.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="reportRef")
    def report_ref(self) -> "ReportReference":
        '''(experimental) A reference to a Report resource.

        :stability: experimental
        '''
        ...


class _IReportRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a Report.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_artifact.IReportRef"

    @builtins.property
    @jsii.member(jsii_name="reportRef")
    def report_ref(self) -> "ReportReference":
        '''(experimental) A reference to a Report resource.

        :stability: experimental
        '''
        return typing.cast("ReportReference", jsii.get(self, "reportRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IReportRef).__jsii_proxy_class__ = lambda : _IReportRefProxy


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_artifact.ReportReference",
    jsii_struct_bases=[],
    name_mapping={"report_arn": "reportArn"},
)
class ReportReference:
    def __init__(self, *, report_arn: builtins.str) -> None:
        '''A reference to a Report resource.

        :param report_arn: The Arn of the Report resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_artifact as interfaces_artifact
            
            report_reference = interfaces_artifact.ReportReference(
                report_arn="reportArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6aa70bfc263351144e435b9b0fab9cffdb56954713b829a76a6c02348620f908)
            check_type(argname="argument report_arn", value=report_arn, expected_type=type_hints["report_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "report_arn": report_arn,
        }

    @builtins.property
    def report_arn(self) -> builtins.str:
        '''The Arn of the Report resource.'''
        result = self._values.get("report_arn")
        assert result is not None, "Required property 'report_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReportReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "IReportRef",
    "ReportReference",
]

publication.publish()

def _typecheckingstub__6aa70bfc263351144e435b9b0fab9cffdb56954713b829a76a6c02348620f908(
    *,
    report_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

for cls in [IReportRef]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
