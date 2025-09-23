r'''
# `aws_workspacesweb_user_settings`

Refer to the Terraform Registry for docs: [`aws_workspacesweb_user_settings`](https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings).
'''
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

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from .._jsii import *

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class WorkspaceswebUserSettings(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.workspaceswebUserSettings.WorkspaceswebUserSettings",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings aws_workspacesweb_user_settings}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        copy_allowed: builtins.str,
        download_allowed: builtins.str,
        paste_allowed: builtins.str,
        print_allowed: builtins.str,
        upload_allowed: builtins.str,
        additional_encryption_context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        cookie_synchronization_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkspaceswebUserSettingsCookieSynchronizationConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        customer_managed_key: typing.Optional[builtins.str] = None,
        deep_link_allowed: typing.Optional[builtins.str] = None,
        disconnect_timeout_in_minutes: typing.Optional[jsii.Number] = None,
        idle_disconnect_timeout_in_minutes: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        toolbar_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkspaceswebUserSettingsToolbarConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings aws_workspacesweb_user_settings} Resource.

        :param scope: The scope in which to define this construct.
        :param id: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param copy_allowed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#copy_allowed WorkspaceswebUserSettings#copy_allowed}.
        :param download_allowed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#download_allowed WorkspaceswebUserSettings#download_allowed}.
        :param paste_allowed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#paste_allowed WorkspaceswebUserSettings#paste_allowed}.
        :param print_allowed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#print_allowed WorkspaceswebUserSettings#print_allowed}.
        :param upload_allowed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#upload_allowed WorkspaceswebUserSettings#upload_allowed}.
        :param additional_encryption_context: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#additional_encryption_context WorkspaceswebUserSettings#additional_encryption_context}.
        :param cookie_synchronization_configuration: cookie_synchronization_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#cookie_synchronization_configuration WorkspaceswebUserSettings#cookie_synchronization_configuration}
        :param customer_managed_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#customer_managed_key WorkspaceswebUserSettings#customer_managed_key}.
        :param deep_link_allowed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#deep_link_allowed WorkspaceswebUserSettings#deep_link_allowed}.
        :param disconnect_timeout_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#disconnect_timeout_in_minutes WorkspaceswebUserSettings#disconnect_timeout_in_minutes}.
        :param idle_disconnect_timeout_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#idle_disconnect_timeout_in_minutes WorkspaceswebUserSettings#idle_disconnect_timeout_in_minutes}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#region WorkspaceswebUserSettings#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#tags WorkspaceswebUserSettings#tags}.
        :param toolbar_configuration: toolbar_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#toolbar_configuration WorkspaceswebUserSettings#toolbar_configuration}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f173e088293ce7963f9ce0fe5acf7faf0bdeb6dccf62adfcfae305b6387b7af0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        config = WorkspaceswebUserSettingsConfig(
            copy_allowed=copy_allowed,
            download_allowed=download_allowed,
            paste_allowed=paste_allowed,
            print_allowed=print_allowed,
            upload_allowed=upload_allowed,
            additional_encryption_context=additional_encryption_context,
            cookie_synchronization_configuration=cookie_synchronization_configuration,
            customer_managed_key=customer_managed_key,
            deep_link_allowed=deep_link_allowed,
            disconnect_timeout_in_minutes=disconnect_timeout_in_minutes,
            idle_disconnect_timeout_in_minutes=idle_disconnect_timeout_in_minutes,
            region=region,
            tags=tags,
            toolbar_configuration=toolbar_configuration,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a WorkspaceswebUserSettings resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the WorkspaceswebUserSettings to import.
        :param import_from_id: The id of the existing WorkspaceswebUserSettings that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the WorkspaceswebUserSettings to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fd0fd8b140f1d01fff2e9bf6af3fcfd4b3afa6b45c3fe46f6ca6ab612181e1b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCookieSynchronizationConfiguration")
    def put_cookie_synchronization_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkspaceswebUserSettingsCookieSynchronizationConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c4a12f573fdb059c7d7dfb7cf6f2c154cea1e48967c112a39a59cb1c4803085)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCookieSynchronizationConfiguration", [value]))

    @jsii.member(jsii_name="putToolbarConfiguration")
    def put_toolbar_configuration(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkspaceswebUserSettingsToolbarConfiguration", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6eb30b385904424a5aaa0439576bfbe0d106045cbacc2523bbb6e1b18662a273)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putToolbarConfiguration", [value]))

    @jsii.member(jsii_name="resetAdditionalEncryptionContext")
    def reset_additional_encryption_context(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalEncryptionContext", []))

    @jsii.member(jsii_name="resetCookieSynchronizationConfiguration")
    def reset_cookie_synchronization_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCookieSynchronizationConfiguration", []))

    @jsii.member(jsii_name="resetCustomerManagedKey")
    def reset_customer_managed_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomerManagedKey", []))

    @jsii.member(jsii_name="resetDeepLinkAllowed")
    def reset_deep_link_allowed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeepLinkAllowed", []))

    @jsii.member(jsii_name="resetDisconnectTimeoutInMinutes")
    def reset_disconnect_timeout_in_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisconnectTimeoutInMinutes", []))

    @jsii.member(jsii_name="resetIdleDisconnectTimeoutInMinutes")
    def reset_idle_disconnect_timeout_in_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdleDisconnectTimeoutInMinutes", []))

    @jsii.member(jsii_name="resetRegion")
    def reset_region(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegion", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetToolbarConfiguration")
    def reset_toolbar_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetToolbarConfiguration", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.member(jsii_name="synthesizeHclAttributes")
    def _synthesize_hcl_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeHclAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="associatedPortalArns")
    def associated_portal_arns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "associatedPortalArns"))

    @builtins.property
    @jsii.member(jsii_name="cookieSynchronizationConfiguration")
    def cookie_synchronization_configuration(
        self,
    ) -> "WorkspaceswebUserSettingsCookieSynchronizationConfigurationList":
        return typing.cast("WorkspaceswebUserSettingsCookieSynchronizationConfigurationList", jsii.get(self, "cookieSynchronizationConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> _cdktf_9a9027ec.StringMap:
        return typing.cast(_cdktf_9a9027ec.StringMap, jsii.get(self, "tagsAll"))

    @builtins.property
    @jsii.member(jsii_name="toolbarConfiguration")
    def toolbar_configuration(
        self,
    ) -> "WorkspaceswebUserSettingsToolbarConfigurationList":
        return typing.cast("WorkspaceswebUserSettingsToolbarConfigurationList", jsii.get(self, "toolbarConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="userSettingsArn")
    def user_settings_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userSettingsArn"))

    @builtins.property
    @jsii.member(jsii_name="additionalEncryptionContextInput")
    def additional_encryption_context_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "additionalEncryptionContextInput"))

    @builtins.property
    @jsii.member(jsii_name="cookieSynchronizationConfigurationInput")
    def cookie_synchronization_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkspaceswebUserSettingsCookieSynchronizationConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkspaceswebUserSettingsCookieSynchronizationConfiguration"]]], jsii.get(self, "cookieSynchronizationConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="copyAllowedInput")
    def copy_allowed_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "copyAllowedInput"))

    @builtins.property
    @jsii.member(jsii_name="customerManagedKeyInput")
    def customer_managed_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customerManagedKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="deepLinkAllowedInput")
    def deep_link_allowed_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deepLinkAllowedInput"))

    @builtins.property
    @jsii.member(jsii_name="disconnectTimeoutInMinutesInput")
    def disconnect_timeout_in_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "disconnectTimeoutInMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="downloadAllowedInput")
    def download_allowed_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "downloadAllowedInput"))

    @builtins.property
    @jsii.member(jsii_name="idleDisconnectTimeoutInMinutesInput")
    def idle_disconnect_timeout_in_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "idleDisconnectTimeoutInMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="pasteAllowedInput")
    def paste_allowed_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pasteAllowedInput"))

    @builtins.property
    @jsii.member(jsii_name="printAllowedInput")
    def print_allowed_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "printAllowedInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="toolbarConfigurationInput")
    def toolbar_configuration_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkspaceswebUserSettingsToolbarConfiguration"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkspaceswebUserSettingsToolbarConfiguration"]]], jsii.get(self, "toolbarConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="uploadAllowedInput")
    def upload_allowed_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uploadAllowedInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalEncryptionContext")
    def additional_encryption_context(
        self,
    ) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "additionalEncryptionContext"))

    @additional_encryption_context.setter
    def additional_encryption_context(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6917526172af65d81a310bb27e05db868031a144ad9c4eb96a7eae9ebb535f8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalEncryptionContext", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="copyAllowed")
    def copy_allowed(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "copyAllowed"))

    @copy_allowed.setter
    def copy_allowed(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a72157d2314b4681716f6078b4426fef78d3230a00506f1a475b40db3875973)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "copyAllowed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="customerManagedKey")
    def customer_managed_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customerManagedKey"))

    @customer_managed_key.setter
    def customer_managed_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fcd7ea35e0eee9a27c8f5c30ebc79788a5b0b82116f8af69e1a4155bcc7e760)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customerManagedKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deepLinkAllowed")
    def deep_link_allowed(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "deepLinkAllowed"))

    @deep_link_allowed.setter
    def deep_link_allowed(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c737b9701a8cd3c87fd92b7ad5eff57e060ecbd59f1f66a45bd5810caee1dae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deepLinkAllowed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disconnectTimeoutInMinutes")
    def disconnect_timeout_in_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "disconnectTimeoutInMinutes"))

    @disconnect_timeout_in_minutes.setter
    def disconnect_timeout_in_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77d833df23a9b4a11dcfbc089f0097012078923fb6e716d8dd946816fd9b00b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disconnectTimeoutInMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="downloadAllowed")
    def download_allowed(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "downloadAllowed"))

    @download_allowed.setter
    def download_allowed(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d66c7d11cfb4a4a0ffe3bf464ceeee15b4c46465f244cb9adc63f5c821697376)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "downloadAllowed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="idleDisconnectTimeoutInMinutes")
    def idle_disconnect_timeout_in_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "idleDisconnectTimeoutInMinutes"))

    @idle_disconnect_timeout_in_minutes.setter
    def idle_disconnect_timeout_in_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dca87ddcd3e0a6cfca352356cc023595d1b4f160d8e0dd80c7233e346ed004ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "idleDisconnectTimeoutInMinutes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pasteAllowed")
    def paste_allowed(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pasteAllowed"))

    @paste_allowed.setter
    def paste_allowed(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70a0ce2130a2d0abee9751d6e6cfe8d8437df0612047ce7447ec074df3a2705f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pasteAllowed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="printAllowed")
    def print_allowed(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "printAllowed"))

    @print_allowed.setter
    def print_allowed(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__081284aac4f79b5e5ee0fee6b90540f28372f8cee0b87be046b9d892129b1533)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "printAllowed", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acde26039c14cf106ef2ee1468eb7ca105577749d3a8e568a707071be817771c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__842c094db88d9611c2c9ba297115fc4eb2995d8d8b7842e2ee4f678615c4945a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uploadAllowed")
    def upload_allowed(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uploadAllowed"))

    @upload_allowed.setter
    def upload_allowed(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__156644b4063c8a017dd8b77b9477cd822e3d9f434476691ccdaf1bd100ebae5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uploadAllowed", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.workspaceswebUserSettings.WorkspaceswebUserSettingsConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "copy_allowed": "copyAllowed",
        "download_allowed": "downloadAllowed",
        "paste_allowed": "pasteAllowed",
        "print_allowed": "printAllowed",
        "upload_allowed": "uploadAllowed",
        "additional_encryption_context": "additionalEncryptionContext",
        "cookie_synchronization_configuration": "cookieSynchronizationConfiguration",
        "customer_managed_key": "customerManagedKey",
        "deep_link_allowed": "deepLinkAllowed",
        "disconnect_timeout_in_minutes": "disconnectTimeoutInMinutes",
        "idle_disconnect_timeout_in_minutes": "idleDisconnectTimeoutInMinutes",
        "region": "region",
        "tags": "tags",
        "toolbar_configuration": "toolbarConfiguration",
    },
)
class WorkspaceswebUserSettingsConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        copy_allowed: builtins.str,
        download_allowed: builtins.str,
        paste_allowed: builtins.str,
        print_allowed: builtins.str,
        upload_allowed: builtins.str,
        additional_encryption_context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        cookie_synchronization_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkspaceswebUserSettingsCookieSynchronizationConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
        customer_managed_key: typing.Optional[builtins.str] = None,
        deep_link_allowed: typing.Optional[builtins.str] = None,
        disconnect_timeout_in_minutes: typing.Optional[jsii.Number] = None,
        idle_disconnect_timeout_in_minutes: typing.Optional[jsii.Number] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        toolbar_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkspaceswebUserSettingsToolbarConfiguration", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param copy_allowed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#copy_allowed WorkspaceswebUserSettings#copy_allowed}.
        :param download_allowed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#download_allowed WorkspaceswebUserSettings#download_allowed}.
        :param paste_allowed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#paste_allowed WorkspaceswebUserSettings#paste_allowed}.
        :param print_allowed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#print_allowed WorkspaceswebUserSettings#print_allowed}.
        :param upload_allowed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#upload_allowed WorkspaceswebUserSettings#upload_allowed}.
        :param additional_encryption_context: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#additional_encryption_context WorkspaceswebUserSettings#additional_encryption_context}.
        :param cookie_synchronization_configuration: cookie_synchronization_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#cookie_synchronization_configuration WorkspaceswebUserSettings#cookie_synchronization_configuration}
        :param customer_managed_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#customer_managed_key WorkspaceswebUserSettings#customer_managed_key}.
        :param deep_link_allowed: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#deep_link_allowed WorkspaceswebUserSettings#deep_link_allowed}.
        :param disconnect_timeout_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#disconnect_timeout_in_minutes WorkspaceswebUserSettings#disconnect_timeout_in_minutes}.
        :param idle_disconnect_timeout_in_minutes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#idle_disconnect_timeout_in_minutes WorkspaceswebUserSettings#idle_disconnect_timeout_in_minutes}.
        :param region: Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#region WorkspaceswebUserSettings#region}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#tags WorkspaceswebUserSettings#tags}.
        :param toolbar_configuration: toolbar_configuration block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#toolbar_configuration WorkspaceswebUserSettings#toolbar_configuration}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b24f302e567a6b561051f43efa80613f85b75cbe13aa336ce1b8ebea0a20e134)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument copy_allowed", value=copy_allowed, expected_type=type_hints["copy_allowed"])
            check_type(argname="argument download_allowed", value=download_allowed, expected_type=type_hints["download_allowed"])
            check_type(argname="argument paste_allowed", value=paste_allowed, expected_type=type_hints["paste_allowed"])
            check_type(argname="argument print_allowed", value=print_allowed, expected_type=type_hints["print_allowed"])
            check_type(argname="argument upload_allowed", value=upload_allowed, expected_type=type_hints["upload_allowed"])
            check_type(argname="argument additional_encryption_context", value=additional_encryption_context, expected_type=type_hints["additional_encryption_context"])
            check_type(argname="argument cookie_synchronization_configuration", value=cookie_synchronization_configuration, expected_type=type_hints["cookie_synchronization_configuration"])
            check_type(argname="argument customer_managed_key", value=customer_managed_key, expected_type=type_hints["customer_managed_key"])
            check_type(argname="argument deep_link_allowed", value=deep_link_allowed, expected_type=type_hints["deep_link_allowed"])
            check_type(argname="argument disconnect_timeout_in_minutes", value=disconnect_timeout_in_minutes, expected_type=type_hints["disconnect_timeout_in_minutes"])
            check_type(argname="argument idle_disconnect_timeout_in_minutes", value=idle_disconnect_timeout_in_minutes, expected_type=type_hints["idle_disconnect_timeout_in_minutes"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument toolbar_configuration", value=toolbar_configuration, expected_type=type_hints["toolbar_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "copy_allowed": copy_allowed,
            "download_allowed": download_allowed,
            "paste_allowed": paste_allowed,
            "print_allowed": print_allowed,
            "upload_allowed": upload_allowed,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if additional_encryption_context is not None:
            self._values["additional_encryption_context"] = additional_encryption_context
        if cookie_synchronization_configuration is not None:
            self._values["cookie_synchronization_configuration"] = cookie_synchronization_configuration
        if customer_managed_key is not None:
            self._values["customer_managed_key"] = customer_managed_key
        if deep_link_allowed is not None:
            self._values["deep_link_allowed"] = deep_link_allowed
        if disconnect_timeout_in_minutes is not None:
            self._values["disconnect_timeout_in_minutes"] = disconnect_timeout_in_minutes
        if idle_disconnect_timeout_in_minutes is not None:
            self._values["idle_disconnect_timeout_in_minutes"] = idle_disconnect_timeout_in_minutes
        if region is not None:
            self._values["region"] = region
        if tags is not None:
            self._values["tags"] = tags
        if toolbar_configuration is not None:
            self._values["toolbar_configuration"] = toolbar_configuration

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(
        self,
    ) -> typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def copy_allowed(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#copy_allowed WorkspaceswebUserSettings#copy_allowed}.'''
        result = self._values.get("copy_allowed")
        assert result is not None, "Required property 'copy_allowed' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def download_allowed(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#download_allowed WorkspaceswebUserSettings#download_allowed}.'''
        result = self._values.get("download_allowed")
        assert result is not None, "Required property 'download_allowed' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def paste_allowed(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#paste_allowed WorkspaceswebUserSettings#paste_allowed}.'''
        result = self._values.get("paste_allowed")
        assert result is not None, "Required property 'paste_allowed' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def print_allowed(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#print_allowed WorkspaceswebUserSettings#print_allowed}.'''
        result = self._values.get("print_allowed")
        assert result is not None, "Required property 'print_allowed' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def upload_allowed(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#upload_allowed WorkspaceswebUserSettings#upload_allowed}.'''
        result = self._values.get("upload_allowed")
        assert result is not None, "Required property 'upload_allowed' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_encryption_context(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#additional_encryption_context WorkspaceswebUserSettings#additional_encryption_context}.'''
        result = self._values.get("additional_encryption_context")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def cookie_synchronization_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkspaceswebUserSettingsCookieSynchronizationConfiguration"]]]:
        '''cookie_synchronization_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#cookie_synchronization_configuration WorkspaceswebUserSettings#cookie_synchronization_configuration}
        '''
        result = self._values.get("cookie_synchronization_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkspaceswebUserSettingsCookieSynchronizationConfiguration"]]], result)

    @builtins.property
    def customer_managed_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#customer_managed_key WorkspaceswebUserSettings#customer_managed_key}.'''
        result = self._values.get("customer_managed_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deep_link_allowed(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#deep_link_allowed WorkspaceswebUserSettings#deep_link_allowed}.'''
        result = self._values.get("deep_link_allowed")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disconnect_timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#disconnect_timeout_in_minutes WorkspaceswebUserSettings#disconnect_timeout_in_minutes}.'''
        result = self._values.get("disconnect_timeout_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def idle_disconnect_timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#idle_disconnect_timeout_in_minutes WorkspaceswebUserSettings#idle_disconnect_timeout_in_minutes}.'''
        result = self._values.get("idle_disconnect_timeout_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''Region where this resource will be `managed <https://docs.aws.amazon.com/general/latest/gr/rande.html#regional-endpoints>`_. Defaults to the Region set in the `provider configuration <https://registry.terraform.io/providers/hashicorp/aws/latest/docs#aws-configuration-reference>`_.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#region WorkspaceswebUserSettings#region}
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#tags WorkspaceswebUserSettings#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def toolbar_configuration(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkspaceswebUserSettingsToolbarConfiguration"]]]:
        '''toolbar_configuration block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#toolbar_configuration WorkspaceswebUserSettings#toolbar_configuration}
        '''
        result = self._values.get("toolbar_configuration")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkspaceswebUserSettingsToolbarConfiguration"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkspaceswebUserSettingsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.workspaceswebUserSettings.WorkspaceswebUserSettingsCookieSynchronizationConfiguration",
    jsii_struct_bases=[],
    name_mapping={"allowlist": "allowlist", "blocklist": "blocklist"},
)
class WorkspaceswebUserSettingsCookieSynchronizationConfiguration:
    def __init__(
        self,
        *,
        allowlist: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkspaceswebUserSettingsCookieSynchronizationConfigurationAllowlistStruct", typing.Dict[builtins.str, typing.Any]]]]] = None,
        blocklist: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WorkspaceswebUserSettingsCookieSynchronizationConfigurationBlocklistStruct", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param allowlist: allowlist block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#allowlist WorkspaceswebUserSettings#allowlist}
        :param blocklist: blocklist block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#blocklist WorkspaceswebUserSettings#blocklist}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79e926ef18b80fa43d3e8938c6e521227eb67e3737426a3babc5c0c310e0924d)
            check_type(argname="argument allowlist", value=allowlist, expected_type=type_hints["allowlist"])
            check_type(argname="argument blocklist", value=blocklist, expected_type=type_hints["blocklist"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowlist is not None:
            self._values["allowlist"] = allowlist
        if blocklist is not None:
            self._values["blocklist"] = blocklist

    @builtins.property
    def allowlist(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkspaceswebUserSettingsCookieSynchronizationConfigurationAllowlistStruct"]]]:
        '''allowlist block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#allowlist WorkspaceswebUserSettings#allowlist}
        '''
        result = self._values.get("allowlist")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkspaceswebUserSettingsCookieSynchronizationConfigurationAllowlistStruct"]]], result)

    @builtins.property
    def blocklist(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkspaceswebUserSettingsCookieSynchronizationConfigurationBlocklistStruct"]]]:
        '''blocklist block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#blocklist WorkspaceswebUserSettings#blocklist}
        '''
        result = self._values.get("blocklist")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WorkspaceswebUserSettingsCookieSynchronizationConfigurationBlocklistStruct"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkspaceswebUserSettingsCookieSynchronizationConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.workspaceswebUserSettings.WorkspaceswebUserSettingsCookieSynchronizationConfigurationAllowlistStruct",
    jsii_struct_bases=[],
    name_mapping={"domain": "domain", "name": "name", "path": "path"},
)
class WorkspaceswebUserSettingsCookieSynchronizationConfigurationAllowlistStruct:
    def __init__(
        self,
        *,
        domain: builtins.str,
        name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#domain WorkspaceswebUserSettings#domain}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#name WorkspaceswebUserSettings#name}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#path WorkspaceswebUserSettings#path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94a79bba752d8eb740a5242d6ad3259c27a77043869aa179f0f25c2c7b4af6ef)
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain": domain,
        }
        if name is not None:
            self._values["name"] = name
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def domain(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#domain WorkspaceswebUserSettings#domain}.'''
        result = self._values.get("domain")
        assert result is not None, "Required property 'domain' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#name WorkspaceswebUserSettings#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#path WorkspaceswebUserSettings#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkspaceswebUserSettingsCookieSynchronizationConfigurationAllowlistStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkspaceswebUserSettingsCookieSynchronizationConfigurationAllowlistStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.workspaceswebUserSettings.WorkspaceswebUserSettingsCookieSynchronizationConfigurationAllowlistStructList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79436ae774fac70e3b3240b112a6451a1886ae82dcbede0b8239829115956b8f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WorkspaceswebUserSettingsCookieSynchronizationConfigurationAllowlistStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe21b26b40649237cd5319c21894bbd6a2b1c46602fbe357d0c8fbf81f7f0d93)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkspaceswebUserSettingsCookieSynchronizationConfigurationAllowlistStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14f3452009f0635383d05694c8ce3940c81a7f6e7d6c97d7d22f25327a9ed50c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf3b62a04a5f9a9460812836817691ebb3489f29d9ccc226e65140a41cd33acc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a240d72627135e9f06b380271b65c41f4b1ee4475f46e37615f1814c4be9dd84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebUserSettingsCookieSynchronizationConfigurationAllowlistStruct]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebUserSettingsCookieSynchronizationConfigurationAllowlistStruct]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebUserSettingsCookieSynchronizationConfigurationAllowlistStruct]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad96f7adfe22277f23bbf53037aadf2d9fd71e5d537554cc42a21b0138abe6c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkspaceswebUserSettingsCookieSynchronizationConfigurationAllowlistStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.workspaceswebUserSettings.WorkspaceswebUserSettingsCookieSynchronizationConfigurationAllowlistStructOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef01e82f6344415343f56e4e6fd2b4006f9f5089d71d2edd47fbbc845f8146e0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @builtins.property
    @jsii.member(jsii_name="domainInput")
    def domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0141cbf93907c3e18f3f55473be0ad54aa8b1809f257082c9b78fcf0604e9e4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29ac9e17ac475a8d8e3911c28ef6dc0b470d84ebe65a41dcd957c501b3f3824f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52f2fa1319dae2279c7b62d1ed5f92c02809bfcbd483196f6c89cad76a105ed8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkspaceswebUserSettingsCookieSynchronizationConfigurationAllowlistStruct]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkspaceswebUserSettingsCookieSynchronizationConfigurationAllowlistStruct]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkspaceswebUserSettingsCookieSynchronizationConfigurationAllowlistStruct]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d4dab68a6ae1a0fe089fce895d4ca5f886f1e080fd63da2f741719e9f4902d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.workspaceswebUserSettings.WorkspaceswebUserSettingsCookieSynchronizationConfigurationBlocklistStruct",
    jsii_struct_bases=[],
    name_mapping={"domain": "domain", "name": "name", "path": "path"},
)
class WorkspaceswebUserSettingsCookieSynchronizationConfigurationBlocklistStruct:
    def __init__(
        self,
        *,
        domain: builtins.str,
        name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param domain: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#domain WorkspaceswebUserSettings#domain}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#name WorkspaceswebUserSettings#name}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#path WorkspaceswebUserSettings#path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b69e25488c6a210f35e4fb5ab8dc8af8aef930ccb9dc5701b5ca7ec2aa3a1911)
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain": domain,
        }
        if name is not None:
            self._values["name"] = name
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def domain(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#domain WorkspaceswebUserSettings#domain}.'''
        result = self._values.get("domain")
        assert result is not None, "Required property 'domain' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#name WorkspaceswebUserSettings#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#path WorkspaceswebUserSettings#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkspaceswebUserSettingsCookieSynchronizationConfigurationBlocklistStruct(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkspaceswebUserSettingsCookieSynchronizationConfigurationBlocklistStructList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.workspaceswebUserSettings.WorkspaceswebUserSettingsCookieSynchronizationConfigurationBlocklistStructList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1631272e3f693cf001c1ffd93246a4a7068d2a54f218550254b5618d1666830a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WorkspaceswebUserSettingsCookieSynchronizationConfigurationBlocklistStructOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7205b471933b6bb1313fe71b8af67a25dd5dd3daaecf8c9127f4a0b58e42216d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkspaceswebUserSettingsCookieSynchronizationConfigurationBlocklistStructOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea57d7e47403cd0df735121583ceade2a63d1c45fb79bc719dbea41ea71dcc1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c612c365a41de0c4387f565aaf3757990f239496d747a0f83291e1065bdc90b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f83fb2e269a4432417c6ca2b90e26e5c5f9f564b46fd98d75cb8f49ad4ab1609)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebUserSettingsCookieSynchronizationConfigurationBlocklistStruct]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebUserSettingsCookieSynchronizationConfigurationBlocklistStruct]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebUserSettingsCookieSynchronizationConfigurationBlocklistStruct]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f1a2e830e6858381bede9ce9e83c8801096cc22fe484d903324db05e8d03818)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkspaceswebUserSettingsCookieSynchronizationConfigurationBlocklistStructOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.workspaceswebUserSettings.WorkspaceswebUserSettingsCookieSynchronizationConfigurationBlocklistStructOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90961d316f58fb75541ee230c362c5d79cb09e5149411dc4651463f45dc2f55a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @builtins.property
    @jsii.member(jsii_name="domainInput")
    def domain_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="domain")
    def domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domain"))

    @domain.setter
    def domain(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e359388b4f045601d3076efe7ca0940a2bd7903791f850e1ef1c572719d1c95e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domain", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__653599872e00b7d183fa8e373ceb50eeb7e912193e30721cf0638b9fd9716ce0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4198687c368a6dd6e8ac1790d732b98ca0c853c418d2aa72323dd73a50fd94c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkspaceswebUserSettingsCookieSynchronizationConfigurationBlocklistStruct]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkspaceswebUserSettingsCookieSynchronizationConfigurationBlocklistStruct]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkspaceswebUserSettingsCookieSynchronizationConfigurationBlocklistStruct]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44b7023c02d000e32547b5ccb882f99fa5f4b4c8d8e47beba03a78cbdd7367b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkspaceswebUserSettingsCookieSynchronizationConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.workspaceswebUserSettings.WorkspaceswebUserSettingsCookieSynchronizationConfigurationList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da850a709512e2b812a5fbb7c7f0ff74d87e95daf6f86c6c738a88891cdd7627)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WorkspaceswebUserSettingsCookieSynchronizationConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac6e29086be566cf5ea22527c4da59f785d7c2eff5d2b02a92e44c82891818fc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkspaceswebUserSettingsCookieSynchronizationConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7df0ba82c58a9e8b8a985180bedf862985fcc43ea0c04b922cc3dae4d600558f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ad9c5b297f1042c8fa1b4a7ce6cc9777af52226c0c44a3d20163ec900ac0171)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e9690eafd3f4b8f1b68b931fc598961037b2f787a2c6343e69aff8ececb2e7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebUserSettingsCookieSynchronizationConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebUserSettingsCookieSynchronizationConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebUserSettingsCookieSynchronizationConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__381f98e6c44061032a8e98473943a03b4c84cf535f56a1080872b783a59c5fac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkspaceswebUserSettingsCookieSynchronizationConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.workspaceswebUserSettings.WorkspaceswebUserSettingsCookieSynchronizationConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0769b22d01e4bb1040377ebb5b69227a360d150d3b289f76c6fefd368e2787ee)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAllowlist")
    def put_allowlist(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkspaceswebUserSettingsCookieSynchronizationConfigurationAllowlistStruct, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b06315475e9f9a9f52d52c7624cd1f9702678bdd26915b940fd8b8d59eadfdfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAllowlist", [value]))

    @jsii.member(jsii_name="putBlocklist")
    def put_blocklist(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkspaceswebUserSettingsCookieSynchronizationConfigurationBlocklistStruct, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__999ae2b8097033420c3f4163a385912052e2b036cc684831f95ad53cbf0d17cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putBlocklist", [value]))

    @jsii.member(jsii_name="resetAllowlist")
    def reset_allowlist(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowlist", []))

    @jsii.member(jsii_name="resetBlocklist")
    def reset_blocklist(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBlocklist", []))

    @builtins.property
    @jsii.member(jsii_name="allowlist")
    def allowlist(
        self,
    ) -> WorkspaceswebUserSettingsCookieSynchronizationConfigurationAllowlistStructList:
        return typing.cast(WorkspaceswebUserSettingsCookieSynchronizationConfigurationAllowlistStructList, jsii.get(self, "allowlist"))

    @builtins.property
    @jsii.member(jsii_name="blocklist")
    def blocklist(
        self,
    ) -> WorkspaceswebUserSettingsCookieSynchronizationConfigurationBlocklistStructList:
        return typing.cast(WorkspaceswebUserSettingsCookieSynchronizationConfigurationBlocklistStructList, jsii.get(self, "blocklist"))

    @builtins.property
    @jsii.member(jsii_name="allowlistInput")
    def allowlist_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebUserSettingsCookieSynchronizationConfigurationAllowlistStruct]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebUserSettingsCookieSynchronizationConfigurationAllowlistStruct]]], jsii.get(self, "allowlistInput"))

    @builtins.property
    @jsii.member(jsii_name="blocklistInput")
    def blocklist_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebUserSettingsCookieSynchronizationConfigurationBlocklistStruct]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebUserSettingsCookieSynchronizationConfigurationBlocklistStruct]]], jsii.get(self, "blocklistInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkspaceswebUserSettingsCookieSynchronizationConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkspaceswebUserSettingsCookieSynchronizationConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkspaceswebUserSettingsCookieSynchronizationConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a334d44c8a4a4c7e9a202f188b753d31651b9661f9ba565326c92565d88c8756)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.workspaceswebUserSettings.WorkspaceswebUserSettingsToolbarConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "hidden_toolbar_items": "hiddenToolbarItems",
        "max_display_resolution": "maxDisplayResolution",
        "toolbar_type": "toolbarType",
        "visual_mode": "visualMode",
    },
)
class WorkspaceswebUserSettingsToolbarConfiguration:
    def __init__(
        self,
        *,
        hidden_toolbar_items: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_display_resolution: typing.Optional[builtins.str] = None,
        toolbar_type: typing.Optional[builtins.str] = None,
        visual_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param hidden_toolbar_items: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#hidden_toolbar_items WorkspaceswebUserSettings#hidden_toolbar_items}.
        :param max_display_resolution: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#max_display_resolution WorkspaceswebUserSettings#max_display_resolution}.
        :param toolbar_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#toolbar_type WorkspaceswebUserSettings#toolbar_type}.
        :param visual_mode: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#visual_mode WorkspaceswebUserSettings#visual_mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14b06e409331f85cedccc68cb93952824a3e2d1bafc05c6fd1dade521c78361c)
            check_type(argname="argument hidden_toolbar_items", value=hidden_toolbar_items, expected_type=type_hints["hidden_toolbar_items"])
            check_type(argname="argument max_display_resolution", value=max_display_resolution, expected_type=type_hints["max_display_resolution"])
            check_type(argname="argument toolbar_type", value=toolbar_type, expected_type=type_hints["toolbar_type"])
            check_type(argname="argument visual_mode", value=visual_mode, expected_type=type_hints["visual_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if hidden_toolbar_items is not None:
            self._values["hidden_toolbar_items"] = hidden_toolbar_items
        if max_display_resolution is not None:
            self._values["max_display_resolution"] = max_display_resolution
        if toolbar_type is not None:
            self._values["toolbar_type"] = toolbar_type
        if visual_mode is not None:
            self._values["visual_mode"] = visual_mode

    @builtins.property
    def hidden_toolbar_items(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#hidden_toolbar_items WorkspaceswebUserSettings#hidden_toolbar_items}.'''
        result = self._values.get("hidden_toolbar_items")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def max_display_resolution(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#max_display_resolution WorkspaceswebUserSettings#max_display_resolution}.'''
        result = self._values.get("max_display_resolution")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def toolbar_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#toolbar_type WorkspaceswebUserSettings#toolbar_type}.'''
        result = self._values.get("toolbar_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def visual_mode(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/aws/6.14.1/docs/resources/workspacesweb_user_settings#visual_mode WorkspaceswebUserSettings#visual_mode}.'''
        result = self._values.get("visual_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkspaceswebUserSettingsToolbarConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WorkspaceswebUserSettingsToolbarConfigurationList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.workspaceswebUserSettings.WorkspaceswebUserSettingsToolbarConfigurationList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d52ffd7b4595d088268f724350c12ab216f466f1497c5619358c347919f39dd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "WorkspaceswebUserSettingsToolbarConfigurationOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__866e2dce490430262f69aec4469511aaa4ec2f8e22574452220afbd2d70080e0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WorkspaceswebUserSettingsToolbarConfigurationOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8593f7569e668bdc4914a21ae9a801a2d5d7b17d914041bfae50b8c78dc8ab53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58d9e332b042d84ba58535c1d28569f1cd4b04b6e15ceca49ca658869e65d3bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f6b8c516e54cdd2902b5df0f99dcb042b6bc3767faf540e1594960f8508f06d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebUserSettingsToolbarConfiguration]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebUserSettingsToolbarConfiguration]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebUserSettingsToolbarConfiguration]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e7b96da8b0705f7cada26c2c2e127e1dcb77f0c19e4b37e5fae2947a44fe0ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WorkspaceswebUserSettingsToolbarConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.workspaceswebUserSettings.WorkspaceswebUserSettingsToolbarConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2958a190b51c64be41a6521d7d6b863706d449c23c968b711f31e5ad91caf8e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetHiddenToolbarItems")
    def reset_hidden_toolbar_items(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHiddenToolbarItems", []))

    @jsii.member(jsii_name="resetMaxDisplayResolution")
    def reset_max_display_resolution(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxDisplayResolution", []))

    @jsii.member(jsii_name="resetToolbarType")
    def reset_toolbar_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetToolbarType", []))

    @jsii.member(jsii_name="resetVisualMode")
    def reset_visual_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVisualMode", []))

    @builtins.property
    @jsii.member(jsii_name="hiddenToolbarItemsInput")
    def hidden_toolbar_items_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "hiddenToolbarItemsInput"))

    @builtins.property
    @jsii.member(jsii_name="maxDisplayResolutionInput")
    def max_display_resolution_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "maxDisplayResolutionInput"))

    @builtins.property
    @jsii.member(jsii_name="toolbarTypeInput")
    def toolbar_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "toolbarTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="visualModeInput")
    def visual_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "visualModeInput"))

    @builtins.property
    @jsii.member(jsii_name="hiddenToolbarItems")
    def hidden_toolbar_items(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "hiddenToolbarItems"))

    @hidden_toolbar_items.setter
    def hidden_toolbar_items(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c23cab0f0960b1104e6eca8a69434ac08e093e9b6a7b01ba5a23b689cd680077)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hiddenToolbarItems", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxDisplayResolution")
    def max_display_resolution(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "maxDisplayResolution"))

    @max_display_resolution.setter
    def max_display_resolution(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeeb8a59a9c2a7e57602e74ad790d41135dc1b7c1dc7c00d75c2cf3c2e108f6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxDisplayResolution", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="toolbarType")
    def toolbar_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "toolbarType"))

    @toolbar_type.setter
    def toolbar_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__603df078b93a389115df7283196f9ae25ff0790f06f1f09d7969069c476f7362)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "toolbarType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="visualMode")
    def visual_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "visualMode"))

    @visual_mode.setter
    def visual_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0511e24063877428e7f10038a43faf2f4563abe1bb3d97d5caf171a8721e7ce6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "visualMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkspaceswebUserSettingsToolbarConfiguration]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkspaceswebUserSettingsToolbarConfiguration]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkspaceswebUserSettingsToolbarConfiguration]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c3cfb83f3981b85d215706fa562f6899e65cab0b05de1c6235d68ee8cd32e56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "WorkspaceswebUserSettings",
    "WorkspaceswebUserSettingsConfig",
    "WorkspaceswebUserSettingsCookieSynchronizationConfiguration",
    "WorkspaceswebUserSettingsCookieSynchronizationConfigurationAllowlistStruct",
    "WorkspaceswebUserSettingsCookieSynchronizationConfigurationAllowlistStructList",
    "WorkspaceswebUserSettingsCookieSynchronizationConfigurationAllowlistStructOutputReference",
    "WorkspaceswebUserSettingsCookieSynchronizationConfigurationBlocklistStruct",
    "WorkspaceswebUserSettingsCookieSynchronizationConfigurationBlocklistStructList",
    "WorkspaceswebUserSettingsCookieSynchronizationConfigurationBlocklistStructOutputReference",
    "WorkspaceswebUserSettingsCookieSynchronizationConfigurationList",
    "WorkspaceswebUserSettingsCookieSynchronizationConfigurationOutputReference",
    "WorkspaceswebUserSettingsToolbarConfiguration",
    "WorkspaceswebUserSettingsToolbarConfigurationList",
    "WorkspaceswebUserSettingsToolbarConfigurationOutputReference",
]

publication.publish()

def _typecheckingstub__f173e088293ce7963f9ce0fe5acf7faf0bdeb6dccf62adfcfae305b6387b7af0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    copy_allowed: builtins.str,
    download_allowed: builtins.str,
    paste_allowed: builtins.str,
    print_allowed: builtins.str,
    upload_allowed: builtins.str,
    additional_encryption_context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    cookie_synchronization_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkspaceswebUserSettingsCookieSynchronizationConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    customer_managed_key: typing.Optional[builtins.str] = None,
    deep_link_allowed: typing.Optional[builtins.str] = None,
    disconnect_timeout_in_minutes: typing.Optional[jsii.Number] = None,
    idle_disconnect_timeout_in_minutes: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    toolbar_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkspaceswebUserSettingsToolbarConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fd0fd8b140f1d01fff2e9bf6af3fcfd4b3afa6b45c3fe46f6ca6ab612181e1b(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c4a12f573fdb059c7d7dfb7cf6f2c154cea1e48967c112a39a59cb1c4803085(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkspaceswebUserSettingsCookieSynchronizationConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eb30b385904424a5aaa0439576bfbe0d106045cbacc2523bbb6e1b18662a273(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkspaceswebUserSettingsToolbarConfiguration, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6917526172af65d81a310bb27e05db868031a144ad9c4eb96a7eae9ebb535f8e(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a72157d2314b4681716f6078b4426fef78d3230a00506f1a475b40db3875973(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fcd7ea35e0eee9a27c8f5c30ebc79788a5b0b82116f8af69e1a4155bcc7e760(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c737b9701a8cd3c87fd92b7ad5eff57e060ecbd59f1f66a45bd5810caee1dae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77d833df23a9b4a11dcfbc089f0097012078923fb6e716d8dd946816fd9b00b8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d66c7d11cfb4a4a0ffe3bf464ceeee15b4c46465f244cb9adc63f5c821697376(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dca87ddcd3e0a6cfca352356cc023595d1b4f160d8e0dd80c7233e346ed004ba(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70a0ce2130a2d0abee9751d6e6cfe8d8437df0612047ce7447ec074df3a2705f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__081284aac4f79b5e5ee0fee6b90540f28372f8cee0b87be046b9d892129b1533(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acde26039c14cf106ef2ee1468eb7ca105577749d3a8e568a707071be817771c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__842c094db88d9611c2c9ba297115fc4eb2995d8d8b7842e2ee4f678615c4945a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__156644b4063c8a017dd8b77b9477cd822e3d9f434476691ccdaf1bd100ebae5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b24f302e567a6b561051f43efa80613f85b75cbe13aa336ce1b8ebea0a20e134(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    copy_allowed: builtins.str,
    download_allowed: builtins.str,
    paste_allowed: builtins.str,
    print_allowed: builtins.str,
    upload_allowed: builtins.str,
    additional_encryption_context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    cookie_synchronization_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkspaceswebUserSettingsCookieSynchronizationConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
    customer_managed_key: typing.Optional[builtins.str] = None,
    deep_link_allowed: typing.Optional[builtins.str] = None,
    disconnect_timeout_in_minutes: typing.Optional[jsii.Number] = None,
    idle_disconnect_timeout_in_minutes: typing.Optional[jsii.Number] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    toolbar_configuration: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkspaceswebUserSettingsToolbarConfiguration, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79e926ef18b80fa43d3e8938c6e521227eb67e3737426a3babc5c0c310e0924d(
    *,
    allowlist: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkspaceswebUserSettingsCookieSynchronizationConfigurationAllowlistStruct, typing.Dict[builtins.str, typing.Any]]]]] = None,
    blocklist: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkspaceswebUserSettingsCookieSynchronizationConfigurationBlocklistStruct, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94a79bba752d8eb740a5242d6ad3259c27a77043869aa179f0f25c2c7b4af6ef(
    *,
    domain: builtins.str,
    name: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79436ae774fac70e3b3240b112a6451a1886ae82dcbede0b8239829115956b8f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe21b26b40649237cd5319c21894bbd6a2b1c46602fbe357d0c8fbf81f7f0d93(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14f3452009f0635383d05694c8ce3940c81a7f6e7d6c97d7d22f25327a9ed50c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf3b62a04a5f9a9460812836817691ebb3489f29d9ccc226e65140a41cd33acc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a240d72627135e9f06b380271b65c41f4b1ee4475f46e37615f1814c4be9dd84(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad96f7adfe22277f23bbf53037aadf2d9fd71e5d537554cc42a21b0138abe6c7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebUserSettingsCookieSynchronizationConfigurationAllowlistStruct]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef01e82f6344415343f56e4e6fd2b4006f9f5089d71d2edd47fbbc845f8146e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0141cbf93907c3e18f3f55473be0ad54aa8b1809f257082c9b78fcf0604e9e4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29ac9e17ac475a8d8e3911c28ef6dc0b470d84ebe65a41dcd957c501b3f3824f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52f2fa1319dae2279c7b62d1ed5f92c02809bfcbd483196f6c89cad76a105ed8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d4dab68a6ae1a0fe089fce895d4ca5f886f1e080fd63da2f741719e9f4902d1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkspaceswebUserSettingsCookieSynchronizationConfigurationAllowlistStruct]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b69e25488c6a210f35e4fb5ab8dc8af8aef930ccb9dc5701b5ca7ec2aa3a1911(
    *,
    domain: builtins.str,
    name: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1631272e3f693cf001c1ffd93246a4a7068d2a54f218550254b5618d1666830a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7205b471933b6bb1313fe71b8af67a25dd5dd3daaecf8c9127f4a0b58e42216d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea57d7e47403cd0df735121583ceade2a63d1c45fb79bc719dbea41ea71dcc1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c612c365a41de0c4387f565aaf3757990f239496d747a0f83291e1065bdc90b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f83fb2e269a4432417c6ca2b90e26e5c5f9f564b46fd98d75cb8f49ad4ab1609(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f1a2e830e6858381bede9ce9e83c8801096cc22fe484d903324db05e8d03818(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebUserSettingsCookieSynchronizationConfigurationBlocklistStruct]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90961d316f58fb75541ee230c362c5d79cb09e5149411dc4651463f45dc2f55a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e359388b4f045601d3076efe7ca0940a2bd7903791f850e1ef1c572719d1c95e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__653599872e00b7d183fa8e373ceb50eeb7e912193e30721cf0638b9fd9716ce0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4198687c368a6dd6e8ac1790d732b98ca0c853c418d2aa72323dd73a50fd94c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44b7023c02d000e32547b5ccb882f99fa5f4b4c8d8e47beba03a78cbdd7367b3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkspaceswebUserSettingsCookieSynchronizationConfigurationBlocklistStruct]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da850a709512e2b812a5fbb7c7f0ff74d87e95daf6f86c6c738a88891cdd7627(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac6e29086be566cf5ea22527c4da59f785d7c2eff5d2b02a92e44c82891818fc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7df0ba82c58a9e8b8a985180bedf862985fcc43ea0c04b922cc3dae4d600558f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ad9c5b297f1042c8fa1b4a7ce6cc9777af52226c0c44a3d20163ec900ac0171(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e9690eafd3f4b8f1b68b931fc598961037b2f787a2c6343e69aff8ececb2e7a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__381f98e6c44061032a8e98473943a03b4c84cf535f56a1080872b783a59c5fac(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebUserSettingsCookieSynchronizationConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0769b22d01e4bb1040377ebb5b69227a360d150d3b289f76c6fefd368e2787ee(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b06315475e9f9a9f52d52c7624cd1f9702678bdd26915b940fd8b8d59eadfdfc(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkspaceswebUserSettingsCookieSynchronizationConfigurationAllowlistStruct, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__999ae2b8097033420c3f4163a385912052e2b036cc684831f95ad53cbf0d17cd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WorkspaceswebUserSettingsCookieSynchronizationConfigurationBlocklistStruct, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a334d44c8a4a4c7e9a202f188b753d31651b9661f9ba565326c92565d88c8756(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkspaceswebUserSettingsCookieSynchronizationConfiguration]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14b06e409331f85cedccc68cb93952824a3e2d1bafc05c6fd1dade521c78361c(
    *,
    hidden_toolbar_items: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_display_resolution: typing.Optional[builtins.str] = None,
    toolbar_type: typing.Optional[builtins.str] = None,
    visual_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d52ffd7b4595d088268f724350c12ab216f466f1497c5619358c347919f39dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__866e2dce490430262f69aec4469511aaa4ec2f8e22574452220afbd2d70080e0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8593f7569e668bdc4914a21ae9a801a2d5d7b17d914041bfae50b8c78dc8ab53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58d9e332b042d84ba58535c1d28569f1cd4b04b6e15ceca49ca658869e65d3bc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f6b8c516e54cdd2902b5df0f99dcb042b6bc3767faf540e1594960f8508f06d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e7b96da8b0705f7cada26c2c2e127e1dcb77f0c19e4b37e5fae2947a44fe0ff(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WorkspaceswebUserSettingsToolbarConfiguration]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2958a190b51c64be41a6521d7d6b863706d449c23c968b711f31e5ad91caf8e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c23cab0f0960b1104e6eca8a69434ac08e093e9b6a7b01ba5a23b689cd680077(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeeb8a59a9c2a7e57602e74ad790d41135dc1b7c1dc7c00d75c2cf3c2e108f6e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__603df078b93a389115df7283196f9ae25ff0790f06f1f09d7969069c476f7362(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0511e24063877428e7f10038a43faf2f4563abe1bb3d97d5caf171a8721e7ce6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c3cfb83f3981b85d215706fa562f6899e65cab0b05de1c6235d68ee8cd32e56(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WorkspaceswebUserSettingsToolbarConfiguration]],
) -> None:
    """Type checking stubs"""
    pass
