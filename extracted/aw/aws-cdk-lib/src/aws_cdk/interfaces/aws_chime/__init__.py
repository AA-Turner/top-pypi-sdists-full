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
    jsii_type="aws-cdk-lib.interfaces.aws_chime.AppInstanceBotReference",
    jsii_struct_bases=[],
    name_mapping={"app_instance_bot_arn": "appInstanceBotArn"},
)
class AppInstanceBotReference:
    def __init__(self, *, app_instance_bot_arn: builtins.str) -> None:
        '''A reference to a AppInstanceBot resource.

        :param app_instance_bot_arn: The AppInstanceBotArn of the AppInstanceBot resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_chime as interfaces_chime
            
            app_instance_bot_reference = interfaces_chime.AppInstanceBotReference(
                app_instance_bot_arn="appInstanceBotArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d94314e184ef238bc15359652813db5a17decbc7880453c10eebfdb5aee1574b)
            check_type(argname="argument app_instance_bot_arn", value=app_instance_bot_arn, expected_type=type_hints["app_instance_bot_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_instance_bot_arn": app_instance_bot_arn,
        }

    @builtins.property
    def app_instance_bot_arn(self) -> builtins.str:
        '''The AppInstanceBotArn of the AppInstanceBot resource.'''
        result = self._values.get("app_instance_bot_arn")
        assert result is not None, "Required property 'app_instance_bot_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppInstanceBotReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_chime.AppInstanceReference",
    jsii_struct_bases=[],
    name_mapping={"app_instance_arn": "appInstanceArn"},
)
class AppInstanceReference:
    def __init__(self, *, app_instance_arn: builtins.str) -> None:
        '''A reference to a AppInstance resource.

        :param app_instance_arn: The AppInstanceArn of the AppInstance resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_chime as interfaces_chime
            
            app_instance_reference = interfaces_chime.AppInstanceReference(
                app_instance_arn="appInstanceArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__ce7a63f08f74043f81dd278aff7af9a1fbed0722dd9d181168266b0223b7dd9a)
            check_type(argname="argument app_instance_arn", value=app_instance_arn, expected_type=type_hints["app_instance_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_instance_arn": app_instance_arn,
        }

    @builtins.property
    def app_instance_arn(self) -> builtins.str:
        '''The AppInstanceArn of the AppInstance resource.'''
        result = self._values.get("app_instance_arn")
        assert result is not None, "Required property 'app_instance_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppInstanceReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_chime.AppInstanceUserReference",
    jsii_struct_bases=[],
    name_mapping={"app_instance_user_arn": "appInstanceUserArn"},
)
class AppInstanceUserReference:
    def __init__(self, *, app_instance_user_arn: builtins.str) -> None:
        '''A reference to a AppInstanceUser resource.

        :param app_instance_user_arn: The AppInstanceUserArn of the AppInstanceUser resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_chime as interfaces_chime
            
            app_instance_user_reference = interfaces_chime.AppInstanceUserReference(
                app_instance_user_arn="appInstanceUserArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__0a21d6b54c1a60d27402b1eed938ae67bfee72c94f33036fdd030210620f2b08)
            check_type(argname="argument app_instance_user_arn", value=app_instance_user_arn, expected_type=type_hints["app_instance_user_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_instance_user_arn": app_instance_user_arn,
        }

    @builtins.property
    def app_instance_user_arn(self) -> builtins.str:
        '''The AppInstanceUserArn of the AppInstanceUser resource.'''
        result = self._values.get("app_instance_user_arn")
        assert result is not None, "Required property 'app_instance_user_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppInstanceUserReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_chime.ChannelFlowReference",
    jsii_struct_bases=[],
    name_mapping={"channel_flow_arn": "channelFlowArn"},
)
class ChannelFlowReference:
    def __init__(self, *, channel_flow_arn: builtins.str) -> None:
        '''A reference to a ChannelFlow resource.

        :param channel_flow_arn: The Arn of the ChannelFlow resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_chime as interfaces_chime
            
            channel_flow_reference = interfaces_chime.ChannelFlowReference(
                channel_flow_arn="channelFlowArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__61d260a072d1387d8809a2f6808a63d6814fb8a1f1a8f87644726b5cbb1a26a5)
            check_type(argname="argument channel_flow_arn", value=channel_flow_arn, expected_type=type_hints["channel_flow_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "channel_flow_arn": channel_flow_arn,
        }

    @builtins.property
    def channel_flow_arn(self) -> builtins.str:
        '''The Arn of the ChannelFlow resource.'''
        result = self._values.get("channel_flow_arn")
        assert result is not None, "Required property 'channel_flow_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChannelFlowReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_chime.IAppInstanceBotRef")
class IAppInstanceBotRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a AppInstanceBot.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="appInstanceBotRef")
    def app_instance_bot_ref(self) -> "AppInstanceBotReference":
        '''(experimental) A reference to a AppInstanceBot resource.

        :stability: experimental
        '''
        ...


class _IAppInstanceBotRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a AppInstanceBot.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_chime.IAppInstanceBotRef"

    @builtins.property
    @jsii.member(jsii_name="appInstanceBotRef")
    def app_instance_bot_ref(self) -> "AppInstanceBotReference":
        '''(experimental) A reference to a AppInstanceBot resource.

        :stability: experimental
        '''
        return typing.cast("AppInstanceBotReference", jsii.get(self, "appInstanceBotRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAppInstanceBotRef).__jsii_proxy_class__ = lambda : _IAppInstanceBotRefProxy


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_chime.IAppInstanceRef")
class IAppInstanceRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a AppInstance.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="appInstanceRef")
    def app_instance_ref(self) -> "AppInstanceReference":
        '''(experimental) A reference to a AppInstance resource.

        :stability: experimental
        '''
        ...


class _IAppInstanceRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a AppInstance.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_chime.IAppInstanceRef"

    @builtins.property
    @jsii.member(jsii_name="appInstanceRef")
    def app_instance_ref(self) -> "AppInstanceReference":
        '''(experimental) A reference to a AppInstance resource.

        :stability: experimental
        '''
        return typing.cast("AppInstanceReference", jsii.get(self, "appInstanceRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAppInstanceRef).__jsii_proxy_class__ = lambda : _IAppInstanceRefProxy


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_chime.IAppInstanceUserRef")
class IAppInstanceUserRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a AppInstanceUser.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="appInstanceUserRef")
    def app_instance_user_ref(self) -> "AppInstanceUserReference":
        '''(experimental) A reference to a AppInstanceUser resource.

        :stability: experimental
        '''
        ...


class _IAppInstanceUserRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a AppInstanceUser.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_chime.IAppInstanceUserRef"

    @builtins.property
    @jsii.member(jsii_name="appInstanceUserRef")
    def app_instance_user_ref(self) -> "AppInstanceUserReference":
        '''(experimental) A reference to a AppInstanceUser resource.

        :stability: experimental
        '''
        return typing.cast("AppInstanceUserReference", jsii.get(self, "appInstanceUserRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAppInstanceUserRef).__jsii_proxy_class__ = lambda : _IAppInstanceUserRefProxy


@jsii.interface(jsii_type="aws-cdk-lib.interfaces.aws_chime.IChannelFlowRef")
class IChannelFlowRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a ChannelFlow.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="channelFlowRef")
    def channel_flow_ref(self) -> "ChannelFlowReference":
        '''(experimental) A reference to a ChannelFlow resource.

        :stability: experimental
        '''
        ...


class _IChannelFlowRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a ChannelFlow.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_chime.IChannelFlowRef"

    @builtins.property
    @jsii.member(jsii_name="channelFlowRef")
    def channel_flow_ref(self) -> "ChannelFlowReference":
        '''(experimental) A reference to a ChannelFlow resource.

        :stability: experimental
        '''
        return typing.cast("ChannelFlowReference", jsii.get(self, "channelFlowRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IChannelFlowRef).__jsii_proxy_class__ = lambda : _IChannelFlowRefProxy


__all__ = [
    "AppInstanceBotReference",
    "AppInstanceReference",
    "AppInstanceUserReference",
    "ChannelFlowReference",
    "IAppInstanceBotRef",
    "IAppInstanceRef",
    "IAppInstanceUserRef",
    "IChannelFlowRef",
]

publication.publish()

def _typecheckingstub__d94314e184ef238bc15359652813db5a17decbc7880453c10eebfdb5aee1574b(
    *,
    app_instance_bot_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce7a63f08f74043f81dd278aff7af9a1fbed0722dd9d181168266b0223b7dd9a(
    *,
    app_instance_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a21d6b54c1a60d27402b1eed938ae67bfee72c94f33036fdd030210620f2b08(
    *,
    app_instance_user_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61d260a072d1387d8809a2f6808a63d6814fb8a1f1a8f87644726b5cbb1a26a5(
    *,
    channel_flow_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

for cls in [IAppInstanceBotRef, IAppInstanceRef, IAppInstanceUserRef, IChannelFlowRef]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
