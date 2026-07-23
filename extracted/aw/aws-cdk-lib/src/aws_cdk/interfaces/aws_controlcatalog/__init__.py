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
    jsii_type="aws-cdk-lib.interfaces.aws_controlcatalog.CommonControlReference",
    jsii_struct_bases=[],
    name_mapping={
        "common_control_arn": "commonControlArn",
        "common_control_id": "commonControlId",
    },
)
class CommonControlReference:
    def __init__(
        self,
        *,
        common_control_arn: builtins.str,
        common_control_id: builtins.str,
    ) -> None:
        '''A reference to a CommonControl resource.

        :param common_control_arn: The ARN of the CommonControl resource.
        :param common_control_id: The CommonControlId of the CommonControl resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_controlcatalog as interfaces_controlcatalog
            
            common_control_reference = interfaces_controlcatalog.CommonControlReference(
                common_control_arn="commonControlArn",
                common_control_id="commonControlId"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__198e0cc329831450fa6fa227d6d6b0fd045c952c1c2aa37066757102ae9fed73)
            check_type(argname="argument common_control_arn", value=common_control_arn, expected_type=type_hints["common_control_arn"])
            check_type(argname="argument common_control_id", value=common_control_id, expected_type=type_hints["common_control_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "common_control_arn": common_control_arn,
            "common_control_id": common_control_id,
        }

    @builtins.property
    def common_control_arn(self) -> builtins.str:
        '''The ARN of the CommonControl resource.'''
        result = self._values.get("common_control_arn")
        assert result is not None, "Required property 'common_control_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def common_control_id(self) -> builtins.str:
        '''The CommonControlId of the CommonControl resource.'''
        result = self._values.get("common_control_id")
        assert result is not None, "Required property 'common_control_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommonControlReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_controlcatalog.ControlReference",
    jsii_struct_bases=[],
    name_mapping={"control_arn": "controlArn", "control_id": "controlId"},
)
class ControlReference:
    def __init__(self, *, control_arn: builtins.str, control_id: builtins.str) -> None:
        '''A reference to a Control resource.

        :param control_arn: The ARN of the Control resource.
        :param control_id: The ControlId of the Control resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_controlcatalog as interfaces_controlcatalog
            
            control_reference = interfaces_controlcatalog.ControlReference(
                control_arn="controlArn",
                control_id="controlId"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__46ebbd706ce6b217b81d62532354401ccc2bc91030402ce44ee4b757fa209c02)
            check_type(argname="argument control_arn", value=control_arn, expected_type=type_hints["control_arn"])
            check_type(argname="argument control_id", value=control_id, expected_type=type_hints["control_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "control_arn": control_arn,
            "control_id": control_id,
        }

    @builtins.property
    def control_arn(self) -> builtins.str:
        '''The ARN of the Control resource.'''
        result = self._values.get("control_arn")
        assert result is not None, "Required property 'control_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def control_id(self) -> builtins.str:
        '''The ControlId of the Control resource.'''
        result = self._values.get("control_id")
        assert result is not None, "Required property 'control_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ControlReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(
    jsii_type="aws-cdk-lib.interfaces.aws_controlcatalog.ICommonControlRef"
)
class ICommonControlRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a CommonControl.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="commonControlRef")
    def common_control_ref(self) -> "CommonControlReference":
        '''(experimental) A reference to a CommonControl resource.

        :stability: experimental
        '''
        ...


class _ICommonControlRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a CommonControl.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_controlcatalog.ICommonControlRef"

    @builtins.property
    @jsii.member(jsii_name="commonControlRef")
    def common_control_ref(self) -> "CommonControlReference":
        '''(experimental) A reference to a CommonControl resource.

        :stability: experimental
        '''
        return typing.cast("CommonControlReference", jsii.get(self, "commonControlRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICommonControlRef).__jsii_proxy_class__ = lambda : _ICommonControlRefProxy


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_controlcatalog.IControlRef")
class IControlRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a Control.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="controlRef")
    def control_ref(self) -> "ControlReference":
        '''(experimental) A reference to a Control resource.

        :stability: experimental
        '''
        ...


class _IControlRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a Control.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_controlcatalog.IControlRef"

    @builtins.property
    @jsii.member(jsii_name="controlRef")
    def control_ref(self) -> "ControlReference":
        '''(experimental) A reference to a Control resource.

        :stability: experimental
        '''
        return typing.cast("ControlReference", jsii.get(self, "controlRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IControlRef).__jsii_proxy_class__ = lambda : _IControlRefProxy


__all__ = [
    "CommonControlReference",
    "ControlReference",
    "ICommonControlRef",
    "IControlRef",
]

publication.publish()

def _typecheckingstub__198e0cc329831450fa6fa227d6d6b0fd045c952c1c2aa37066757102ae9fed73(
    *,
    common_control_arn: builtins.str,
    common_control_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46ebbd706ce6b217b81d62532354401ccc2bc91030402ce44ee4b757fa209c02(
    *,
    control_arn: builtins.str,
    control_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

for cls in [ICommonControlRef, IControlRef]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
