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


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_osis.IPipelineBlueprintRef")
class IPipelineBlueprintRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a PipelineBlueprint.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="pipelineBlueprintRef")
    def pipeline_blueprint_ref(self) -> "PipelineBlueprintReference":
        '''(experimental) A reference to a PipelineBlueprint resource.

        :stability: experimental
        '''
        ...


class _IPipelineBlueprintRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a PipelineBlueprint.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_osis.IPipelineBlueprintRef"

    @builtins.property
    @jsii.member(jsii_name="pipelineBlueprintRef")
    def pipeline_blueprint_ref(self) -> "PipelineBlueprintReference":
        '''(experimental) A reference to a PipelineBlueprint resource.

        :stability: experimental
        '''
        return typing.cast("PipelineBlueprintReference", jsii.get(self, "pipelineBlueprintRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPipelineBlueprintRef).__jsii_proxy_class__ = lambda : _IPipelineBlueprintRefProxy


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_osis.IPipelineRef")
class IPipelineRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a Pipeline.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="pipelineRef")
    def pipeline_ref(self) -> "PipelineReference":
        '''(experimental) A reference to a Pipeline resource.

        :stability: experimental
        '''
        ...


class _IPipelineRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a Pipeline.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_osis.IPipelineRef"

    @builtins.property
    @jsii.member(jsii_name="pipelineRef")
    def pipeline_ref(self) -> "PipelineReference":
        '''(experimental) A reference to a Pipeline resource.

        :stability: experimental
        '''
        return typing.cast("PipelineReference", jsii.get(self, "pipelineRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPipelineRef).__jsii_proxy_class__ = lambda : _IPipelineRefProxy


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_osis.PipelineBlueprintReference",
    jsii_struct_bases=[],
    name_mapping={"pipeline_blueprint_arn": "pipelineBlueprintArn"},
)
class PipelineBlueprintReference:
    def __init__(self, *, pipeline_blueprint_arn: builtins.str) -> None:
        '''A reference to a PipelineBlueprint resource.

        :param pipeline_blueprint_arn: The Arn of the PipelineBlueprint resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_osis as interfaces_osis
            
            pipeline_blueprint_reference = interfaces_osis.PipelineBlueprintReference(
                pipeline_blueprint_arn="pipelineBlueprintArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1583f2143a1d49dd235c62f24892e0435bcf3cf11edd5f612f04871af6c66130)
            check_type(argname="argument pipeline_blueprint_arn", value=pipeline_blueprint_arn, expected_type=type_hints["pipeline_blueprint_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pipeline_blueprint_arn": pipeline_blueprint_arn,
        }

    @builtins.property
    def pipeline_blueprint_arn(self) -> builtins.str:
        '''The Arn of the PipelineBlueprint resource.'''
        result = self._values.get("pipeline_blueprint_arn")
        assert result is not None, "Required property 'pipeline_blueprint_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipelineBlueprintReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_osis.PipelineReference",
    jsii_struct_bases=[],
    name_mapping={"pipeline_arn": "pipelineArn"},
)
class PipelineReference:
    def __init__(self, *, pipeline_arn: builtins.str) -> None:
        '''A reference to a Pipeline resource.

        :param pipeline_arn: The PipelineArn of the Pipeline resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_osis as interfaces_osis
            
            pipeline_reference = interfaces_osis.PipelineReference(
                pipeline_arn="pipelineArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__5a1c8d90d5a4774bab00e23378d24796245018abfab541e57a022417378e6eb0)
            check_type(argname="argument pipeline_arn", value=pipeline_arn, expected_type=type_hints["pipeline_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "pipeline_arn": pipeline_arn,
        }

    @builtins.property
    def pipeline_arn(self) -> builtins.str:
        '''The PipelineArn of the Pipeline resource.'''
        result = self._values.get("pipeline_arn")
        assert result is not None, "Required property 'pipeline_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipelineReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "IPipelineBlueprintRef",
    "IPipelineRef",
    "PipelineBlueprintReference",
    "PipelineReference",
]

publication.publish()

def _typecheckingstub__1583f2143a1d49dd235c62f24892e0435bcf3cf11edd5f612f04871af6c66130(
    *,
    pipeline_blueprint_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a1c8d90d5a4774bab00e23378d24796245018abfab541e57a022417378e6eb0(
    *,
    pipeline_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

for cls in [IPipelineBlueprintRef, IPipelineRef]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
