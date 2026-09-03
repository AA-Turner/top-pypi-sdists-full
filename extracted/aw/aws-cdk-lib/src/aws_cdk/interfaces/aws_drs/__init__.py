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


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_drs.ISourceNetworkRef")
class ISourceNetworkRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a SourceNetwork.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="sourceNetworkRef")
    def source_network_ref(self) -> "SourceNetworkReference":
        '''(experimental) A reference to a SourceNetwork resource.

        :stability: experimental
        '''
        ...


class _ISourceNetworkRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a SourceNetwork.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_drs.ISourceNetworkRef"

    @builtins.property
    @jsii.member(jsii_name="sourceNetworkRef")
    def source_network_ref(self) -> "SourceNetworkReference":
        '''(experimental) A reference to a SourceNetwork resource.

        :stability: experimental
        '''
        return typing.cast("SourceNetworkReference", jsii.get(self, "sourceNetworkRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISourceNetworkRef).__jsii_proxy_class__ = lambda : _ISourceNetworkRefProxy


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_drs.SourceNetworkReference",
    jsii_struct_bases=[],
    name_mapping={"source_network_arn": "sourceNetworkArn"},
)
class SourceNetworkReference:
    def __init__(self, *, source_network_arn: builtins.str) -> None:
        '''A reference to a SourceNetwork resource.

        :param source_network_arn: The Arn of the SourceNetwork resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_drs as interfaces_drs
            
            source_network_reference = interfaces_drs.SourceNetworkReference(
                source_network_arn="sourceNetworkArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1a58b357a9776e9a00ee15c041375d33ac5d4ecb8f9a9c0c37c98cee7821227e)
            check_type(argname="argument source_network_arn", value=source_network_arn, expected_type=type_hints["source_network_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source_network_arn": source_network_arn,
        }

    @builtins.property
    def source_network_arn(self) -> builtins.str:
        '''The Arn of the SourceNetwork resource.'''
        result = self._values.get("source_network_arn")
        assert result is not None, "Required property 'source_network_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SourceNetworkReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ISourceNetworkRef",
    "SourceNetworkReference",
]

publication.publish()

def _typecheckingstub__1a58b357a9776e9a00ee15c041375d33ac5d4ecb8f9a9c0c37c98cee7821227e(
    *,
    source_network_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

for cls in [ISourceNetworkRef]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
