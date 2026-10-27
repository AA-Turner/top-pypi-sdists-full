r'''
# AWS::LicenseManagerUserSubscriptions Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_licensemanagerusersubscriptions as licensemanagerusersubscriptions
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for LicenseManagerUserSubscriptions construct libraries](https://constructs.dev/search?q=licensemanagerusersubscriptions)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::LicenseManagerUserSubscriptions resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_LicenseManagerUserSubscriptions.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::LicenseManagerUserSubscriptions](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_LicenseManagerUserSubscriptions.html).

(Read the [CDK Contributing Guide](https://github.com/aws/aws-cdk/blob/main/CONTRIBUTING.md) and submit an RFC if you are interested in contributing to this construct library.)

<!--END CFNONLY DISCLAIMER-->
'''
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


from .._jsii import *

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

    import aws_cdk as _aws_cdk_0cae9daa
    import aws_cdk.interfaces.aws_licensemanagerusersubscriptions as _aws_licensemanagerusersubscriptions_2702c51e
    import constructs as _constructs_77d1e7e8
else:

    _aws_cdk_0cae9daa = _LazyImport("aws_cdk")
    _aws_licensemanagerusersubscriptions_2702c51e = _LazyImport("aws_cdk.interfaces.aws_licensemanagerusersubscriptions")
    _constructs_77d1e7e8 = _LazyImport("constructs")


@jsii.implements(_aws_cdk_0cae9daa.IInspectable, _aws_licensemanagerusersubscriptions_2702c51e.ILicenseServerEndpointRef, _aws_cdk_0cae9daa.ITaggableV2)
class CfnLicenseServerEndpoint(
    _aws_cdk_0cae9daa.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="aws-cdk-lib.aws_licensemanagerusersubscriptions.CfnLicenseServerEndpoint",
):
    '''Resource Type definition for AWS::LicenseManagerUserSubscriptions::LicenseServerEndpoint.

    A license server endpoint that provides access to Remote Desktop Services Subscriber Access License servers for a registered identity provider.

    :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanagerusersubscriptions-licenseserverendpoint.html
    :cloudformationResource: AWS::LicenseManagerUserSubscriptions::LicenseServerEndpoint
    :exampleMetadata: fixture=_generated

    Example::

        from aws_cdk import CfnTag
        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from aws_cdk import aws_licensemanagerusersubscriptions as licensemanagerusersubscriptions
        
        cfn_license_server_endpoint = licensemanagerusersubscriptions.CfnLicenseServerEndpoint(self, "MyCfnLicenseServerEndpoint",
            identity_provider_arn="identityProviderArn",
        
            # the properties below are optional
            license_server_settings=licensemanagerusersubscriptions.CfnLicenseServerEndpoint.LicenseServerSettingsProperty(
                server_settings=licensemanagerusersubscriptions.CfnLicenseServerEndpoint.ServerSettingsProperty(
                    rds_sal_settings=licensemanagerusersubscriptions.CfnLicenseServerEndpoint.RdsSalSettingsProperty(
                        rds_sal_credentials_provider=licensemanagerusersubscriptions.CfnLicenseServerEndpoint.CredentialsProviderProperty(
                            secrets_manager_credentials_provider=licensemanagerusersubscriptions.CfnLicenseServerEndpoint.SecretsManagerCredentialsProviderProperty(
                                secret_id="secretId"
                            )
                        )
                    )
                ),
                server_type="serverType"
            ),
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: "_constructs_77d1e7e8.Construct",
        id: builtins.str,
        *,
        identity_provider_arn: builtins.str,
        license_server_settings: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnLicenseServerEndpoint.LicenseServerSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::LicenseManagerUserSubscriptions::LicenseServerEndpoint``.

        :param scope: Scope in which this resource is defined.
        :param id: Construct identifier for this resource (unique in its scope).
        :param identity_provider_arn: The Amazon Resource Name (ARN) that identifies the registered identity provider the license server endpoint is created for. For Active Directory, that can be a self-managed Active Directory or an AWS Managed Microsoft AD.
        :param license_server_settings: The settings of the RDS license server to create the endpoint for.
        :param tags: The tags that apply for the license server endpoint. A maximum of 50 tags.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__76b43e6beb229de05293d6de640e2da36af8e3001aa69f658afd85973e7c2509)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLicenseServerEndpointProps(
            identity_provider_arn=identity_provider_arn,
            license_server_settings=license_server_settings,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="arnForLicenseServerEndpoint")
    @builtins.classmethod
    def arn_for_license_server_endpoint(
        cls,
        resource: "_aws_licensemanagerusersubscriptions_2702c51e.ILicenseServerEndpointRef",
    ) -> builtins.str:
        '''
        :param resource: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c0324d16d325aedee08022a18c42042e489d4433ab9a43b5e14f7b97a21c37ff)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arnForLicenseServerEndpoint", [resource]))

    @jsii.member(jsii_name="isCfnLicenseServerEndpoint")
    @builtins.classmethod
    def is_cfn_license_server_endpoint(cls, x: typing.Any) -> builtins.bool:
        '''Checks whether the given object is a CfnLicenseServerEndpoint.

        :param x: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__06aa7576cea3b19b963bdc6d00660dbe530f167c8869cf4efc7448f25837dd43)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isCfnLicenseServerEndpoint", [x]))

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: "_aws_cdk_0cae9daa.TreeInspector") -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__df0a37397c1cdb76a4bb500cf78a3d865deb60e77b850e8979f81de88514378b)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3233ac76e8dfe2559b7a7645ad93fd3a684e080c20c8a1696c72aeb8dfe243fd)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    @builtins.classmethod
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationTime")
    def attr_creation_time(self) -> builtins.str:
        '''The timestamp when License Manager created the license server endpoint.

        :cloudformationAttribute: CreationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="attrLicenseServerEndpointArn")
    def attr_license_server_endpoint_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the license server endpoint.

        :cloudformationAttribute: LicenseServerEndpointArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLicenseServerEndpointArn"))

    @builtins.property
    @jsii.member(jsii_name="attrLicenseServerEndpointId")
    def attr_license_server_endpoint_id(self) -> builtins.str:
        '''The ID of the license server endpoint.

        :cloudformationAttribute: LicenseServerEndpointId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLicenseServerEndpointId"))

    @builtins.property
    @jsii.member(jsii_name="attrLicenseServerEndpointProvisioningStatus")
    def attr_license_server_endpoint_provisioning_status(self) -> builtins.str:
        '''The current state of the provisioning process for the license server endpoint.

        :cloudformationAttribute: LicenseServerEndpointProvisioningStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLicenseServerEndpointProvisioningStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrLicenseServers")
    def attr_license_servers(self) -> "_aws_cdk_0cae9daa.IResolvable":
        '''The license servers that are accessed through this endpoint.

        :cloudformationAttribute: LicenseServers
        '''
        return typing.cast("_aws_cdk_0cae9daa.IResolvable", jsii.get(self, "attrLicenseServers"))

    @builtins.property
    @jsii.member(jsii_name="attrServerEndpoint")
    def attr_server_endpoint(self) -> "_aws_cdk_0cae9daa.IResolvable":
        '''The network address of a license server endpoint.

        :cloudformationAttribute: ServerEndpoint
        '''
        return typing.cast("_aws_cdk_0cae9daa.IResolvable", jsii.get(self, "attrServerEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="attrServerType")
    def attr_server_type(self) -> builtins.str:
        '''The type of license server.

        :cloudformationAttribute: ServerType
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServerType"))

    @builtins.property
    @jsii.member(jsii_name="cdkTagManager")
    def cdk_tag_manager(self) -> "_aws_cdk_0cae9daa.TagManager":
        '''Tag Manager which manages the tags for this resource.'''
        return typing.cast("_aws_cdk_0cae9daa.TagManager", jsii.get(self, "cdkTagManager"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="cfnPropertyNames")
    def _cfn_property_names(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "cfnPropertyNames"))

    @builtins.property
    @jsii.member(jsii_name="licenseServerEndpointRef")
    def license_server_endpoint_ref(
        self,
    ) -> "_aws_licensemanagerusersubscriptions_2702c51e.LicenseServerEndpointReference":
        '''A reference to a LicenseServerEndpoint resource.'''
        return typing.cast("_aws_licensemanagerusersubscriptions_2702c51e.LicenseServerEndpointReference", jsii.get(self, "licenseServerEndpointRef"))

    @builtins.property
    @jsii.member(jsii_name="identityProviderArn")
    def identity_provider_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) that identifies the registered identity provider the license server endpoint is created for.'''
        return typing.cast(builtins.str, jsii.get(self, "identityProviderArn"))

    @identity_provider_arn.setter
    def identity_provider_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__7b0dbefdff097d3e8a0389b369525ce5e31b01f9716bf0e36ea0edefb10801bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityProviderArn", value)

    @builtins.property
    @jsii.member(jsii_name="licenseServerSettings")
    def license_server_settings(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLicenseServerEndpoint.LicenseServerSettingsProperty"]]:
        '''The settings of the RDS license server to create the endpoint for.'''
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLicenseServerEndpoint.LicenseServerSettingsProperty"]], jsii.get(self, "licenseServerSettings"))

    @license_server_settings.setter
    def license_server_settings(
        self,
        value: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLicenseServerEndpoint.LicenseServerSettingsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__73e75d354c2494fb54c74ed20db7e2c4606657a6fc44f51644814c14f0e2e7ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "licenseServerSettings", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''The tags that apply for the license server endpoint.'''
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]],
    ) -> None:
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__22502b40ce7351f570c72c9f4d9ea6623ef0aa8357ab7c27f0a046acce0e2c27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_licensemanagerusersubscriptions.CfnLicenseServerEndpoint.CredentialsProviderProperty",
        jsii_struct_bases=[],
        name_mapping={
            "secrets_manager_credentials_provider": "secretsManagerCredentialsProvider",
        },
    )
    class CredentialsProviderProperty:
        def __init__(
            self,
            *,
            secrets_manager_credentials_provider: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnLicenseServerEndpoint.SecretsManagerCredentialsProviderProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''The source of the credentials that License Manager uses to reach the license server.

            :param secrets_manager_credentials_provider: Credentials held in AWS Secrets Manager.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanagerusersubscriptions-licenseserverendpoint-credentialsprovider.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_licensemanagerusersubscriptions as licensemanagerusersubscriptions
                
                credentials_provider_property = licensemanagerusersubscriptions.CfnLicenseServerEndpoint.CredentialsProviderProperty(
                    secrets_manager_credentials_provider=licensemanagerusersubscriptions.CfnLicenseServerEndpoint.SecretsManagerCredentialsProviderProperty(
                        secret_id="secretId"
                    )
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__df644b87ca4f3752a8338931f8505178541720894cadb5cf93e3df1f431d8e21)
                check_type(argname="argument secrets_manager_credentials_provider", value=secrets_manager_credentials_provider, expected_type=type_hints["secrets_manager_credentials_provider"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "secrets_manager_credentials_provider": secrets_manager_credentials_provider,
            }

        @builtins.property
        def secrets_manager_credentials_provider(
            self,
        ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLicenseServerEndpoint.SecretsManagerCredentialsProviderProperty"]:
            '''Credentials held in AWS Secrets Manager.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanagerusersubscriptions-licenseserverendpoint-credentialsprovider.html#cfn-licensemanagerusersubscriptions-licenseserverendpoint-credentialsprovider-secretsmanagercredentialsprovider
            '''
            result = self._values.get("secrets_manager_credentials_provider")
            assert result is not None, "Required property 'secrets_manager_credentials_provider' is missing"
            return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLicenseServerEndpoint.SecretsManagerCredentialsProviderProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CredentialsProviderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_licensemanagerusersubscriptions.CfnLicenseServerEndpoint.LicenseServerProperty",
        jsii_struct_bases=[],
        name_mapping={
            "health_status": "healthStatus",
            "ipv4_address": "ipv4Address",
            "ipv6_address": "ipv6Address",
            "provisioning_status": "provisioningStatus",
        },
    )
    class LicenseServerProperty:
        def __init__(
            self,
            *,
            health_status: typing.Optional[builtins.str] = None,
            ipv4_address: typing.Optional[builtins.str] = None,
            ipv6_address: typing.Optional[builtins.str] = None,
            provisioning_status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A Remote Desktop Services license server that is accessed through the endpoint.

            :param health_status: The health status of the license server.
            :param ipv4_address: The domain IPv4 address of the license server.
            :param ipv6_address: The domain IPv6 address of the license server.
            :param provisioning_status: The current state of the provisioning process for the license server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanagerusersubscriptions-licenseserverendpoint-licenseserver.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_licensemanagerusersubscriptions as licensemanagerusersubscriptions
                
                license_server_property = licensemanagerusersubscriptions.CfnLicenseServerEndpoint.LicenseServerProperty(
                    health_status="healthStatus",
                    ipv4_address="ipv4Address",
                    ipv6_address="ipv6Address",
                    provisioning_status="provisioningStatus"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__9eb9ca0688f804512abf776c5fa29dde531ddceca90159698b92f42438f1ff38)
                check_type(argname="argument health_status", value=health_status, expected_type=type_hints["health_status"])
                check_type(argname="argument ipv4_address", value=ipv4_address, expected_type=type_hints["ipv4_address"])
                check_type(argname="argument ipv6_address", value=ipv6_address, expected_type=type_hints["ipv6_address"])
                check_type(argname="argument provisioning_status", value=provisioning_status, expected_type=type_hints["provisioning_status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if health_status is not None:
                self._values["health_status"] = health_status
            if ipv4_address is not None:
                self._values["ipv4_address"] = ipv4_address
            if ipv6_address is not None:
                self._values["ipv6_address"] = ipv6_address
            if provisioning_status is not None:
                self._values["provisioning_status"] = provisioning_status

        @builtins.property
        def health_status(self) -> typing.Optional[builtins.str]:
            '''The health status of the license server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanagerusersubscriptions-licenseserverendpoint-licenseserver.html#cfn-licensemanagerusersubscriptions-licenseserverendpoint-licenseserver-healthstatus
            '''
            result = self._values.get("health_status")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ipv4_address(self) -> typing.Optional[builtins.str]:
            '''The domain IPv4 address of the license server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanagerusersubscriptions-licenseserverendpoint-licenseserver.html#cfn-licensemanagerusersubscriptions-licenseserverendpoint-licenseserver-ipv4address
            '''
            result = self._values.get("ipv4_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ipv6_address(self) -> typing.Optional[builtins.str]:
            '''The domain IPv6 address of the license server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanagerusersubscriptions-licenseserverendpoint-licenseserver.html#cfn-licensemanagerusersubscriptions-licenseserverendpoint-licenseserver-ipv6address
            '''
            result = self._values.get("ipv6_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def provisioning_status(self) -> typing.Optional[builtins.str]:
            '''The current state of the provisioning process for the license server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanagerusersubscriptions-licenseserverendpoint-licenseserver.html#cfn-licensemanagerusersubscriptions-licenseserverendpoint-licenseserver-provisioningstatus
            '''
            result = self._values.get("provisioning_status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LicenseServerProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_licensemanagerusersubscriptions.CfnLicenseServerEndpoint.LicenseServerSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "server_settings": "serverSettings",
            "server_type": "serverType",
        },
    )
    class LicenseServerSettingsProperty:
        def __init__(
            self,
            *,
            server_settings: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnLicenseServerEndpoint.ServerSettingsProperty", typing.Dict[builtins.str, typing.Any]]],
            server_type: builtins.str,
        ) -> None:
            '''The settings of the RDS license server to create the endpoint for.

            :param server_settings: The settings of a license server, by server type.
            :param server_type: The type of license server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanagerusersubscriptions-licenseserverendpoint-licenseserversettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_licensemanagerusersubscriptions as licensemanagerusersubscriptions
                
                license_server_settings_property = licensemanagerusersubscriptions.CfnLicenseServerEndpoint.LicenseServerSettingsProperty(
                    server_settings=licensemanagerusersubscriptions.CfnLicenseServerEndpoint.ServerSettingsProperty(
                        rds_sal_settings=licensemanagerusersubscriptions.CfnLicenseServerEndpoint.RdsSalSettingsProperty(
                            rds_sal_credentials_provider=licensemanagerusersubscriptions.CfnLicenseServerEndpoint.CredentialsProviderProperty(
                                secrets_manager_credentials_provider=licensemanagerusersubscriptions.CfnLicenseServerEndpoint.SecretsManagerCredentialsProviderProperty(
                                    secret_id="secretId"
                                )
                            )
                        )
                    ),
                    server_type="serverType"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__d49c15c3c4a076394497482acdcfbb8c7199a87a2e2cd6b7f262572006ccb47b)
                check_type(argname="argument server_settings", value=server_settings, expected_type=type_hints["server_settings"])
                check_type(argname="argument server_type", value=server_type, expected_type=type_hints["server_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "server_settings": server_settings,
                "server_type": server_type,
            }

        @builtins.property
        def server_settings(
            self,
        ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLicenseServerEndpoint.ServerSettingsProperty"]:
            '''The settings of a license server, by server type.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanagerusersubscriptions-licenseserverendpoint-licenseserversettings.html#cfn-licensemanagerusersubscriptions-licenseserverendpoint-licenseserversettings-serversettings
            '''
            result = self._values.get("server_settings")
            assert result is not None, "Required property 'server_settings' is missing"
            return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLicenseServerEndpoint.ServerSettingsProperty"], result)

        @builtins.property
        def server_type(self) -> builtins.str:
            '''The type of license server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanagerusersubscriptions-licenseserverendpoint-licenseserversettings.html#cfn-licensemanagerusersubscriptions-licenseserverendpoint-licenseserversettings-servertype
            '''
            result = self._values.get("server_type")
            assert result is not None, "Required property 'server_type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LicenseServerSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_licensemanagerusersubscriptions.CfnLicenseServerEndpoint.RdsSalSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"rds_sal_credentials_provider": "rdsSalCredentialsProvider"},
    )
    class RdsSalSettingsProperty:
        def __init__(
            self,
            *,
            rds_sal_credentials_provider: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnLicenseServerEndpoint.CredentialsProviderProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''The settings of a Remote Desktop Services Subscriber Access License server.

            :param rds_sal_credentials_provider: The source of the credentials that License Manager uses to reach the license server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanagerusersubscriptions-licenseserverendpoint-rdssalsettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_licensemanagerusersubscriptions as licensemanagerusersubscriptions
                
                rds_sal_settings_property = licensemanagerusersubscriptions.CfnLicenseServerEndpoint.RdsSalSettingsProperty(
                    rds_sal_credentials_provider=licensemanagerusersubscriptions.CfnLicenseServerEndpoint.CredentialsProviderProperty(
                        secrets_manager_credentials_provider=licensemanagerusersubscriptions.CfnLicenseServerEndpoint.SecretsManagerCredentialsProviderProperty(
                            secret_id="secretId"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__4ffa57c503d313fffc89cec1af0aaeae42637fa8809e8a3fd3ad140f8a4f1d40)
                check_type(argname="argument rds_sal_credentials_provider", value=rds_sal_credentials_provider, expected_type=type_hints["rds_sal_credentials_provider"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "rds_sal_credentials_provider": rds_sal_credentials_provider,
            }

        @builtins.property
        def rds_sal_credentials_provider(
            self,
        ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLicenseServerEndpoint.CredentialsProviderProperty"]:
            '''The source of the credentials that License Manager uses to reach the license server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanagerusersubscriptions-licenseserverendpoint-rdssalsettings.html#cfn-licensemanagerusersubscriptions-licenseserverendpoint-rdssalsettings-rdssalcredentialsprovider
            '''
            result = self._values.get("rds_sal_credentials_provider")
            assert result is not None, "Required property 'rds_sal_credentials_provider' is missing"
            return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLicenseServerEndpoint.CredentialsProviderProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RdsSalSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_licensemanagerusersubscriptions.CfnLicenseServerEndpoint.SecretsManagerCredentialsProviderProperty",
        jsii_struct_bases=[],
        name_mapping={"secret_id": "secretId"},
    )
    class SecretsManagerCredentialsProviderProperty:
        def __init__(self, *, secret_id: builtins.str) -> None:
            '''Credentials held in AWS Secrets Manager.

            :param secret_id: The identifier of the Secrets Manager secret that holds the license server administrator credentials. The name of the secret must begin with the prefix license-manager-user-.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanagerusersubscriptions-licenseserverendpoint-secretsmanagercredentialsprovider.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_licensemanagerusersubscriptions as licensemanagerusersubscriptions
                
                secrets_manager_credentials_provider_property = licensemanagerusersubscriptions.CfnLicenseServerEndpoint.SecretsManagerCredentialsProviderProperty(
                    secret_id="secretId"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__62adf6cd9f8d5f58b2c07d0d956cf1e38c691247ae10fb1a8e936cb3c4c42cc8)
                check_type(argname="argument secret_id", value=secret_id, expected_type=type_hints["secret_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "secret_id": secret_id,
            }

        @builtins.property
        def secret_id(self) -> builtins.str:
            '''The identifier of the Secrets Manager secret that holds the license server administrator credentials.

            The name of the secret must begin with the prefix license-manager-user-.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanagerusersubscriptions-licenseserverendpoint-secretsmanagercredentialsprovider.html#cfn-licensemanagerusersubscriptions-licenseserverendpoint-secretsmanagercredentialsprovider-secretid
            '''
            result = self._values.get("secret_id")
            assert result is not None, "Required property 'secret_id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SecretsManagerCredentialsProviderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_licensemanagerusersubscriptions.CfnLicenseServerEndpoint.ServerEndpointProperty",
        jsii_struct_bases=[],
        name_mapping={"endpoint": "endpoint"},
    )
    class ServerEndpointProperty:
        def __init__(self, *, endpoint: typing.Optional[builtins.str] = None) -> None:
            '''The network address of a license server endpoint.

            :param endpoint: The network address of the endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanagerusersubscriptions-licenseserverendpoint-serverendpoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_licensemanagerusersubscriptions as licensemanagerusersubscriptions
                
                server_endpoint_property = licensemanagerusersubscriptions.CfnLicenseServerEndpoint.ServerEndpointProperty(
                    endpoint="endpoint"
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__b39afd220bc78e4fa9d7e71ed038b758d63fe6f45cb3c5029a6a3b6ab7bf0017)
                check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if endpoint is not None:
                self._values["endpoint"] = endpoint

        @builtins.property
        def endpoint(self) -> typing.Optional[builtins.str]:
            '''The network address of the endpoint.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanagerusersubscriptions-licenseserverendpoint-serverendpoint.html#cfn-licensemanagerusersubscriptions-licenseserverendpoint-serverendpoint-endpoint
            '''
            result = self._values.get("endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServerEndpointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="aws-cdk-lib.aws_licensemanagerusersubscriptions.CfnLicenseServerEndpoint.ServerSettingsProperty",
        jsii_struct_bases=[],
        name_mapping={"rds_sal_settings": "rdsSalSettings"},
    )
    class ServerSettingsProperty:
        def __init__(
            self,
            *,
            rds_sal_settings: typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnLicenseServerEndpoint.RdsSalSettingsProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''The settings of a license server, by server type.

            :param rds_sal_settings: The settings of a Remote Desktop Services Subscriber Access License server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanagerusersubscriptions-licenseserverendpoint-serversettings.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from aws_cdk import aws_licensemanagerusersubscriptions as licensemanagerusersubscriptions
                
                server_settings_property = licensemanagerusersubscriptions.CfnLicenseServerEndpoint.ServerSettingsProperty(
                    rds_sal_settings=licensemanagerusersubscriptions.CfnLicenseServerEndpoint.RdsSalSettingsProperty(
                        rds_sal_credentials_provider=licensemanagerusersubscriptions.CfnLicenseServerEndpoint.CredentialsProviderProperty(
                            secrets_manager_credentials_provider=licensemanagerusersubscriptions.CfnLicenseServerEndpoint.SecretsManagerCredentialsProviderProperty(
                                secret_id="secretId"
                            )
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = cached_type_hints(_typecheckingstub__70e631d3a94c93203d4666e59f58f8b2e06671f290dc57b4923a24cd57cf717f)
                check_type(argname="argument rds_sal_settings", value=rds_sal_settings, expected_type=type_hints["rds_sal_settings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "rds_sal_settings": rds_sal_settings,
            }

        @builtins.property
        def rds_sal_settings(
            self,
        ) -> typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLicenseServerEndpoint.RdsSalSettingsProperty"]:
            '''The settings of a Remote Desktop Services Subscriber Access License server.

            :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-licensemanagerusersubscriptions-licenseserverendpoint-serversettings.html#cfn-licensemanagerusersubscriptions-licenseserverendpoint-serversettings-rdssalsettings
            '''
            result = self._values.get("rds_sal_settings")
            assert result is not None, "Required property 'rds_sal_settings' is missing"
            return typing.cast(typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLicenseServerEndpoint.RdsSalSettingsProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ServerSettingsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="aws-cdk-lib.aws_licensemanagerusersubscriptions.CfnLicenseServerEndpointProps",
    jsii_struct_bases=[],
    name_mapping={
        "identity_provider_arn": "identityProviderArn",
        "license_server_settings": "licenseServerSettings",
        "tags": "tags",
    },
)
class CfnLicenseServerEndpointProps:
    def __init__(
        self,
        *,
        identity_provider_arn: builtins.str,
        license_server_settings: typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", typing.Union["CfnLicenseServerEndpoint.LicenseServerSettingsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["_aws_cdk_0cae9daa.CfnTag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnLicenseServerEndpoint``.

        :param identity_provider_arn: The Amazon Resource Name (ARN) that identifies the registered identity provider the license server endpoint is created for. For Active Directory, that can be a self-managed Active Directory or an AWS Managed Microsoft AD.
        :param license_server_settings: The settings of the RDS license server to create the endpoint for.
        :param tags: The tags that apply for the license server endpoint. A maximum of 50 tags.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanagerusersubscriptions-licenseserverendpoint.html
        :exampleMetadata: fixture=_generated

        Example::

            from aws_cdk import CfnTag
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from aws_cdk import aws_licensemanagerusersubscriptions as licensemanagerusersubscriptions
            
            cfn_license_server_endpoint_props = licensemanagerusersubscriptions.CfnLicenseServerEndpointProps(
                identity_provider_arn="identityProviderArn",
            
                # the properties below are optional
                license_server_settings=licensemanagerusersubscriptions.CfnLicenseServerEndpoint.LicenseServerSettingsProperty(
                    server_settings=licensemanagerusersubscriptions.CfnLicenseServerEndpoint.ServerSettingsProperty(
                        rds_sal_settings=licensemanagerusersubscriptions.CfnLicenseServerEndpoint.RdsSalSettingsProperty(
                            rds_sal_credentials_provider=licensemanagerusersubscriptions.CfnLicenseServerEndpoint.CredentialsProviderProperty(
                                secrets_manager_credentials_provider=licensemanagerusersubscriptions.CfnLicenseServerEndpoint.SecretsManagerCredentialsProviderProperty(
                                    secret_id="secretId"
                                )
                            )
                        )
                    ),
                    server_type="serverType"
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c0c5df15011df1445045c000a84210dcb17a1589358e59ea920c31670aa864a9)
            check_type(argname="argument identity_provider_arn", value=identity_provider_arn, expected_type=type_hints["identity_provider_arn"])
            check_type(argname="argument license_server_settings", value=license_server_settings, expected_type=type_hints["license_server_settings"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "identity_provider_arn": identity_provider_arn,
        }
        if license_server_settings is not None:
            self._values["license_server_settings"] = license_server_settings
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def identity_provider_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) that identifies the registered identity provider the license server endpoint is created for.

        For Active Directory, that can be a self-managed Active Directory or an AWS Managed Microsoft AD.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanagerusersubscriptions-licenseserverendpoint.html#cfn-licensemanagerusersubscriptions-licenseserverendpoint-identityproviderarn
        '''
        result = self._values.get("identity_provider_arn")
        assert result is not None, "Required property 'identity_provider_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def license_server_settings(
        self,
    ) -> typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLicenseServerEndpoint.LicenseServerSettingsProperty"]]:
        '''The settings of the RDS license server to create the endpoint for.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanagerusersubscriptions-licenseserverendpoint.html#cfn-licensemanagerusersubscriptions-licenseserverendpoint-licenseserversettings
        '''
        result = self._values.get("license_server_settings")
        return typing.cast(typing.Optional[typing.Union["_aws_cdk_0cae9daa.IResolvable", "CfnLicenseServerEndpoint.LicenseServerSettingsProperty"]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]]:
        '''The tags that apply for the license server endpoint.

        A maximum of 50 tags.

        :see: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-licensemanagerusersubscriptions-licenseserverendpoint.html#cfn-licensemanagerusersubscriptions-licenseserverendpoint-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List["_aws_cdk_0cae9daa.CfnTag"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLicenseServerEndpointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnLicenseServerEndpoint",
    "CfnLicenseServerEndpointProps",
]

publication.publish()

def _typecheckingstub__76b43e6beb229de05293d6de640e2da36af8e3001aa69f658afd85973e7c2509(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    identity_provider_arn: builtins.str,
    license_server_settings: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnLicenseServerEndpoint.LicenseServerSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0324d16d325aedee08022a18c42042e489d4433ab9a43b5e14f7b97a21c37ff(
    resource: _aws_licensemanagerusersubscriptions_2702c51e.ILicenseServerEndpointRef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06aa7576cea3b19b963bdc6d00660dbe530f167c8869cf4efc7448f25837dd43(
    x: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df0a37397c1cdb76a4bb500cf78a3d865deb60e77b850e8979f81de88514378b(
    inspector: _aws_cdk_0cae9daa.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3233ac76e8dfe2559b7a7645ad93fd3a684e080c20c8a1696c72aeb8dfe243fd(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b0dbefdff097d3e8a0389b369525ce5e31b01f9716bf0e36ea0edefb10801bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73e75d354c2494fb54c74ed20db7e2c4606657a6fc44f51644814c14f0e2e7ef(
    value: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, CfnLicenseServerEndpoint.LicenseServerSettingsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22502b40ce7351f570c72c9f4d9ea6623ef0aa8357ab7c27f0a046acce0e2c27(
    value: typing.Optional[typing.List[_aws_cdk_0cae9daa.CfnTag]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df644b87ca4f3752a8338931f8505178541720894cadb5cf93e3df1f431d8e21(
    *,
    secrets_manager_credentials_provider: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnLicenseServerEndpoint.SecretsManagerCredentialsProviderProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eb9ca0688f804512abf776c5fa29dde531ddceca90159698b92f42438f1ff38(
    *,
    health_status: typing.Optional[builtins.str] = None,
    ipv4_address: typing.Optional[builtins.str] = None,
    ipv6_address: typing.Optional[builtins.str] = None,
    provisioning_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d49c15c3c4a076394497482acdcfbb8c7199a87a2e2cd6b7f262572006ccb47b(
    *,
    server_settings: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnLicenseServerEndpoint.ServerSettingsProperty, typing.Dict[builtins.str, typing.Any]]],
    server_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ffa57c503d313fffc89cec1af0aaeae42637fa8809e8a3fd3ad140f8a4f1d40(
    *,
    rds_sal_credentials_provider: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnLicenseServerEndpoint.CredentialsProviderProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62adf6cd9f8d5f58b2c07d0d956cf1e38c691247ae10fb1a8e936cb3c4c42cc8(
    *,
    secret_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b39afd220bc78e4fa9d7e71ed038b758d63fe6f45cb3c5029a6a3b6ab7bf0017(
    *,
    endpoint: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70e631d3a94c93203d4666e59f58f8b2e06671f290dc57b4923a24cd57cf717f(
    *,
    rds_sal_settings: typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnLicenseServerEndpoint.RdsSalSettingsProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0c5df15011df1445045c000a84210dcb17a1589358e59ea920c31670aa864a9(
    *,
    identity_provider_arn: builtins.str,
    license_server_settings: typing.Optional[typing.Union[_aws_cdk_0cae9daa.IResolvable, typing.Union[CfnLicenseServerEndpoint.LicenseServerSettingsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_0cae9daa.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
