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
    jsii_type="aws-cdk-lib.interfaces.aws_licensemanagerlinuxsubscriptions.ISubscriptionProviderRef"
)
class ISubscriptionProviderRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a SubscriptionProvider.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="subscriptionProviderRef")
    def subscription_provider_ref(self) -> "SubscriptionProviderReference":
        '''(experimental) A reference to a SubscriptionProvider resource.

        :stability: experimental
        '''
        ...


class _ISubscriptionProviderRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a SubscriptionProvider.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_licensemanagerlinuxsubscriptions.ISubscriptionProviderRef"

    @builtins.property
    @jsii.member(jsii_name="subscriptionProviderRef")
    def subscription_provider_ref(self) -> "SubscriptionProviderReference":
        '''(experimental) A reference to a SubscriptionProvider resource.

        :stability: experimental
        '''
        return typing.cast("SubscriptionProviderReference", jsii.get(self, "subscriptionProviderRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISubscriptionProviderRef).__jsii_proxy_class__ = lambda : _ISubscriptionProviderRefProxy


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_licensemanagerlinuxsubscriptions.SubscriptionProviderReference",
    jsii_struct_bases=[],
    name_mapping={"subscription_provider_arn": "subscriptionProviderArn"},
)
class SubscriptionProviderReference:
    def __init__(self, *, subscription_provider_arn: builtins.str) -> None:
        '''A reference to a SubscriptionProvider resource.

        :param subscription_provider_arn: The SubscriptionProviderArn of the SubscriptionProvider resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_licensemanagerlinuxsubscriptions as interfaces_licensemanagerlinuxsubscriptions
            
            subscription_provider_reference = interfaces_licensemanagerlinuxsubscriptions.SubscriptionProviderReference(
                subscription_provider_arn="subscriptionProviderArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__74bd6292ead4520514eee35c0800679ab570becf96be438f19ca3efd2722f6cd)
            check_type(argname="argument subscription_provider_arn", value=subscription_provider_arn, expected_type=type_hints["subscription_provider_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subscription_provider_arn": subscription_provider_arn,
        }

    @builtins.property
    def subscription_provider_arn(self) -> builtins.str:
        '''The SubscriptionProviderArn of the SubscriptionProvider resource.'''
        result = self._values.get("subscription_provider_arn")
        assert result is not None, "Required property 'subscription_provider_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SubscriptionProviderReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ISubscriptionProviderRef",
    "SubscriptionProviderReference",
]

publication.publish()

def _typecheckingstub__74bd6292ead4520514eee35c0800679ab570becf96be438f19ca3efd2722f6cd(
    *,
    subscription_provider_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

for cls in [ISubscriptionProviderRef]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
