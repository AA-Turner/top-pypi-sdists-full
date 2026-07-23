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
    jsii_type="aws-cdk-lib.interfaces.aws_dataexchange.EntitledDataSetsReference",
    jsii_struct_bases=[],
    name_mapping={
        "entitled_data_sets_arn": "entitledDataSetsArn",
        "entitled_data_sets_id": "entitledDataSetsId",
    },
)
class EntitledDataSetsReference:
    def __init__(
        self,
        *,
        entitled_data_sets_arn: builtins.str,
        entitled_data_sets_id: builtins.str,
    ) -> None:
        '''A reference to a EntitledDataSets resource.

        :param entitled_data_sets_arn: The ARN of the EntitledDataSets resource.
        :param entitled_data_sets_id: The Id of the EntitledDataSets resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_dataexchange as interfaces_dataexchange
            
            entitled_data_sets_reference = interfaces_dataexchange.EntitledDataSetsReference(
                entitled_data_sets_arn="entitledDataSetsArn",
                entitled_data_sets_id="entitledDataSetsId"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__bef5190a7bea29d982e8b64def067d6bd5c865d8b90bc51defa2048b1b289b7a)
            check_type(argname="argument entitled_data_sets_arn", value=entitled_data_sets_arn, expected_type=type_hints["entitled_data_sets_arn"])
            check_type(argname="argument entitled_data_sets_id", value=entitled_data_sets_id, expected_type=type_hints["entitled_data_sets_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "entitled_data_sets_arn": entitled_data_sets_arn,
            "entitled_data_sets_id": entitled_data_sets_id,
        }

    @builtins.property
    def entitled_data_sets_arn(self) -> builtins.str:
        '''The ARN of the EntitledDataSets resource.'''
        result = self._values.get("entitled_data_sets_arn")
        assert result is not None, "Required property 'entitled_data_sets_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def entitled_data_sets_id(self) -> builtins.str:
        '''The Id of the EntitledDataSets resource.'''
        result = self._values.get("entitled_data_sets_id")
        assert result is not None, "Required property 'entitled_data_sets_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EntitledDataSetsReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(
    jsii_type="aws-cdk-lib.interfaces.aws_dataexchange.IEntitledDataSetsRef"
)
class IEntitledDataSetsRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a EntitledDataSets.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="entitledDataSetsRef")
    def entitled_data_sets_ref(self) -> "EntitledDataSetsReference":
        '''(experimental) A reference to a EntitledDataSets resource.

        :stability: experimental
        '''
        ...


class _IEntitledDataSetsRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a EntitledDataSets.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_dataexchange.IEntitledDataSetsRef"

    @builtins.property
    @jsii.member(jsii_name="entitledDataSetsRef")
    def entitled_data_sets_ref(self) -> "EntitledDataSetsReference":
        '''(experimental) A reference to a EntitledDataSets resource.

        :stability: experimental
        '''
        return typing.cast("EntitledDataSetsReference", jsii.get(self, "entitledDataSetsRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IEntitledDataSetsRef).__jsii_proxy_class__ = lambda : _IEntitledDataSetsRefProxy


__all__ = [
    "EntitledDataSetsReference",
    "IEntitledDataSetsRef",
]

publication.publish()

def _typecheckingstub__bef5190a7bea29d982e8b64def067d6bd5c865d8b90bc51defa2048b1b289b7a(
    *,
    entitled_data_sets_arn: builtins.str,
    entitled_data_sets_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

for cls in [IEntitledDataSetsRef]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
