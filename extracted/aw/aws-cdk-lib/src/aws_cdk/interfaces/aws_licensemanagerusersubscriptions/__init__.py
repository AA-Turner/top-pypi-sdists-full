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
    jsii_type="aws-cdk-lib.interfaces.aws_licensemanagerusersubscriptions.ILicenseServerEndpointRef"
)
class ILicenseServerEndpointRef(
    _constructs_77d1e7e8.IConstruct,
    _interfaces_8ca7e747.IEnvironmentAware,
    typing_extensions.Protocol,
):
    '''(experimental) Indicates that this resource can be referenced as a LicenseServerEndpoint.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="licenseServerEndpointRef")
    def license_server_endpoint_ref(self) -> "LicenseServerEndpointReference":
        '''(experimental) A reference to a LicenseServerEndpoint resource.

        :stability: experimental
        '''
        ...


class _ILicenseServerEndpointRefProxy(
    jsii.proxy_for(_constructs_77d1e7e8.IConstruct), # type: ignore[misc]
    jsii.proxy_for(_interfaces_8ca7e747.IEnvironmentAware), # type: ignore[misc]
):
    '''(experimental) Indicates that this resource can be referenced as a LicenseServerEndpoint.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "aws-cdk-lib.interfaces.aws_licensemanagerusersubscriptions.ILicenseServerEndpointRef"

    @builtins.property
    @jsii.member(jsii_name="licenseServerEndpointRef")
    def license_server_endpoint_ref(self) -> "LicenseServerEndpointReference":
        '''(experimental) A reference to a LicenseServerEndpoint resource.

        :stability: experimental
        '''
        return typing.cast("LicenseServerEndpointReference", jsii.get(self, "licenseServerEndpointRef"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ILicenseServerEndpointRef).__jsii_proxy_class__ = lambda : _ILicenseServerEndpointRefProxy


@jsii.data_type(
    jsii_type="aws-cdk-lib.interfaces.aws_licensemanagerusersubscriptions.LicenseServerEndpointReference",
    jsii_struct_bases=[],
    name_mapping={
        "identity_provider_arn": "identityProviderArn",
        "license_server_endpoint_arn": "licenseServerEndpointArn",
    },
)
class LicenseServerEndpointReference:
    def __init__(
        self,
        *,
        identity_provider_arn: builtins.str,
        license_server_endpoint_arn: builtins.str,
    ) -> None:
        '''A reference to a LicenseServerEndpoint resource.

        :param identity_provider_arn: The IdentityProviderArn of the LicenseServerEndpoint resource.
        :param license_server_endpoint_arn: The LicenseServerEndpointArn of the LicenseServerEndpoint resource.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk.interfaces import aws_licensemanagerusersubscriptions as interfaces_licensemanagerusersubscriptions
            
            license_server_endpoint_reference = interfaces_licensemanagerusersubscriptions.LicenseServerEndpointReference(
                identity_provider_arn="identityProviderArn",
                license_server_endpoint_arn="licenseServerEndpointArn"
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__74a692ee825385de479aa4e75eb30c87166d859e14bfe5d61a8dc2636cc3bf0f)
            check_type(argname="argument identity_provider_arn", value=identity_provider_arn, expected_type=type_hints["identity_provider_arn"])
            check_type(argname="argument license_server_endpoint_arn", value=license_server_endpoint_arn, expected_type=type_hints["license_server_endpoint_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "identity_provider_arn": identity_provider_arn,
            "license_server_endpoint_arn": license_server_endpoint_arn,
        }

    @builtins.property
    def identity_provider_arn(self) -> builtins.str:
        '''The IdentityProviderArn of the LicenseServerEndpoint resource.'''
        result = self._values.get("identity_provider_arn")
        assert result is not None, "Required property 'identity_provider_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def license_server_endpoint_arn(self) -> builtins.str:
        '''The LicenseServerEndpointArn of the LicenseServerEndpoint resource.'''
        result = self._values.get("license_server_endpoint_arn")
        assert result is not None, "Required property 'license_server_endpoint_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LicenseServerEndpointReference(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "ILicenseServerEndpointRef",
    "LicenseServerEndpointReference",
]

publication.publish()

def _typecheckingstub__74a692ee825385de479aa4e75eb30c87166d859e14bfe5d61a8dc2636cc3bf0f(
    *,
    identity_provider_arn: builtins.str,
    license_server_endpoint_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

for cls in [ILicenseServerEndpointRef]:
    typing.cast(typing.Any, cls).__protocol_attrs__ = typing.cast(typing.Any, cls).__protocol_attrs__ - set(['__jsii_proxy_class__', '__jsii_type__'])
