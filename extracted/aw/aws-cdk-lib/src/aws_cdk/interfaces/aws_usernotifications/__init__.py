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


@jsii.interface(
    jsii_type="aws-cdk-lib.interfaces.aws_usernotifications.IManagedNotificationConfigurationRef"
)
class IManagedNotificationConfigurationRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a ManagedNotificationConfiguration.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="managedNotificationConfigurationRef")
    def managed_notification_configuration_ref(
        self,
    ) -> "ManagedNotificationConfigurationReference":
        '''(experimental) A reference to a ManagedNotificationConfiguration resource.

        :stability: experimental
        '''
        ...


class _IManagedNotificationConfigurationRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a ManagedNotificationConfiguration.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_usernotifications.IManagedNotificationConfigurationRef"

    @builtins.property
    @jsii.member(jsii_name="managedNotificationConfigurationRef")
    def managed_notification_configuration_ref(
        self,
    ) -> "ManagedNotificationConfigurationReference":
        '''(experimental) A reference to a ManagedNotificationConfiguration resource.

        :stability: experimental
        '''
        return typing.cast("ManagedNotificationConfigurationReference", jsii.get(self, "managedNotificationConfigurationRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IManagedNotificationConfigurationRef).__jsii_proxy_class__ = lambda : _IManagedNotificationConfigurationRefProxy


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_usernotifications.ManagedNotificationConfigurationReference",
    jsii_struct_bases=[],
    name_mapping={
        "managed_notification_configuration_arn": "managedNotificationConfigurationArn",
    },
)
class ManagedNotificationConfigurationReference:
    def __init__(self, *, managed_notification_configuration_arn: builtins.str) -> None:
        '''A reference to a ManagedNotificationConfiguration resource.

        :param managed_notification_configuration_arn: The Arn of the ManagedNotificationConfiguration resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_usernotifications as interfaces_usernotifications
            
            managed_notification_configuration_reference = interfaces_usernotifications.ManagedNotificationConfigurationReference(
                managed_notification_configuration_arn="managedNotificationConfigurationArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__67347b06dd73ec9bc6cbab0b821ab2d0b23a58409dd59d2b2eb539d23732032b)
            check_type(argname="argument managed_notification_configuration_arn", value=managed_notification_configuration_arn, expected_type=type_hints["managed_notification_configuration_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "managed_notification_configuration_arn": managed_notification_configuration_arn,
        }

    @builtins.property
    def managed_notification_configuration_arn(self) -> builtins.str:
        '''The Arn of the ManagedNotificationConfiguration resource.'''
        result = self._values.get("managed_notification_configuration_arn")
        assert result is not None, "Required property 'managed_notification_configuration_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManagedNotificationConfigurationReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "IManagedNotificationConfigurationRef",
    "ManagedNotificationConfigurationReference",
]

publication.publish()

def _typecheckingstub__67347b06dd73ec9bc6cbab0b821ab2d0b23a58409dd59d2b2eb539d23732032b(
    *,
    managed_notification_configuration_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

for cls in [IManagedNotificationConfigurationRef]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
