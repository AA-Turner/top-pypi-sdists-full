r'''
# `azurerm_linux_function_app_slot`

Refer to the Terraform Registry for docs: [`azurerm_linux_function_app_slot`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot).
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


class LinuxFunctionAppSlot(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlot",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot azurerm_linux_function_app_slot}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        function_app_id: builtins.str,
        name: builtins.str,
        site_config: typing.Union["LinuxFunctionAppSlotSiteConfig", typing.Dict[builtins.str, typing.Any]],
        app_settings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        auth_settings: typing.Optional[typing.Union["LinuxFunctionAppSlotAuthSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        auth_settings_v2: typing.Optional[typing.Union["LinuxFunctionAppSlotAuthSettingsV2", typing.Dict[builtins.str, typing.Any]]] = None,
        backup: typing.Optional[typing.Union["LinuxFunctionAppSlotBackup", typing.Dict[builtins.str, typing.Any]]] = None,
        builtin_logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_certificate_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_certificate_exclusion_paths: typing.Optional[builtins.str] = None,
        client_certificate_mode: typing.Optional[builtins.str] = None,
        connection_string: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LinuxFunctionAppSlotConnectionString", typing.Dict[builtins.str, typing.Any]]]]] = None,
        content_share_force_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        daily_memory_time_quota: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ftp_publish_basic_authentication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        functions_extension_version: typing.Optional[builtins.str] = None,
        https_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["LinuxFunctionAppSlotIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        key_vault_reference_identity_id: typing.Optional[builtins.str] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        service_plan_id: typing.Optional[builtins.str] = None,
        storage_account: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LinuxFunctionAppSlotStorageAccount", typing.Dict[builtins.str, typing.Any]]]]] = None,
        storage_account_access_key: typing.Optional[builtins.str] = None,
        storage_account_name: typing.Optional[builtins.str] = None,
        storage_key_vault_secret_id: typing.Optional[builtins.str] = None,
        storage_uses_managed_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["LinuxFunctionAppSlotTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_network_backup_restore_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        virtual_network_subnet_id: typing.Optional[builtins.str] = None,
        vnet_image_pull_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        webdeploy_publish_basic_authentication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot azurerm_linux_function_app_slot} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param function_app_id: The ID of the Linux Function App this Slot is a member of. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#function_app_id LinuxFunctionAppSlot#function_app_id}
        :param name: Specifies the name of the Function App Slot. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#name LinuxFunctionAppSlot#name}
        :param site_config: site_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#site_config LinuxFunctionAppSlot#site_config}
        :param app_settings: A map of key-value pairs for `App Settings <https://docs.microsoft.com/en-us/azure/azure-functions/functions-app-settings>`_ and custom values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#app_settings LinuxFunctionAppSlot#app_settings}
        :param auth_settings: auth_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#auth_settings LinuxFunctionAppSlot#auth_settings}
        :param auth_settings_v2: auth_settings_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#auth_settings_v2 LinuxFunctionAppSlot#auth_settings_v2}
        :param backup: backup block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#backup LinuxFunctionAppSlot#backup}
        :param builtin_logging_enabled: Should built in logging be enabled. Configures ``AzureWebJobsDashboard`` app setting based on the configured storage setting. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#builtin_logging_enabled LinuxFunctionAppSlot#builtin_logging_enabled}
        :param client_certificate_enabled: Should the Function App Slot use Client Certificates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_certificate_enabled LinuxFunctionAppSlot#client_certificate_enabled}
        :param client_certificate_exclusion_paths: Paths to exclude when using client certificates, separated by ; Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_certificate_exclusion_paths LinuxFunctionAppSlot#client_certificate_exclusion_paths}
        :param client_certificate_mode: The mode of the Function App Slot's client certificates requirement for incoming requests. Possible values are ``Required``, ``Optional``, and ``OptionalInteractiveUser``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_certificate_mode LinuxFunctionAppSlot#client_certificate_mode}
        :param connection_string: connection_string block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#connection_string LinuxFunctionAppSlot#connection_string}
        :param content_share_force_disabled: Force disable the content share settings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#content_share_force_disabled LinuxFunctionAppSlot#content_share_force_disabled}
        :param daily_memory_time_quota: The amount of memory in gigabyte-seconds that your application is allowed to consume per day. Setting this value only affects function apps in Consumption Plans. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#daily_memory_time_quota LinuxFunctionAppSlot#daily_memory_time_quota}
        :param enabled: Is the Linux Function App Slot enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#enabled LinuxFunctionAppSlot#enabled}
        :param ftp_publish_basic_authentication_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#ftp_publish_basic_authentication_enabled LinuxFunctionAppSlot#ftp_publish_basic_authentication_enabled}.
        :param functions_extension_version: The runtime version associated with the Function App Slot. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#functions_extension_version LinuxFunctionAppSlot#functions_extension_version}
        :param https_only: Can the Function App Slot only be accessed via HTTPS? Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#https_only LinuxFunctionAppSlot#https_only}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#id LinuxFunctionAppSlot#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#identity LinuxFunctionAppSlot#identity}
        :param key_vault_reference_identity_id: The User Assigned Identity to use for Key Vault access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#key_vault_reference_identity_id LinuxFunctionAppSlot#key_vault_reference_identity_id}
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#public_network_access_enabled LinuxFunctionAppSlot#public_network_access_enabled}.
        :param service_plan_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#service_plan_id LinuxFunctionAppSlot#service_plan_id}.
        :param storage_account: storage_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#storage_account LinuxFunctionAppSlot#storage_account}
        :param storage_account_access_key: The access key which will be used to access the storage account for the Function App Slot. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#storage_account_access_key LinuxFunctionAppSlot#storage_account_access_key}
        :param storage_account_name: The backend storage account name which will be used by this Function App Slot. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#storage_account_name LinuxFunctionAppSlot#storage_account_name}
        :param storage_key_vault_secret_id: The Key Vault Secret ID, including version, that contains the Connection String to connect to the storage account for this Function App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#storage_key_vault_secret_id LinuxFunctionAppSlot#storage_key_vault_secret_id}
        :param storage_uses_managed_identity: Should the Function App Slot use its Managed Identity to access storage? Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#storage_uses_managed_identity LinuxFunctionAppSlot#storage_uses_managed_identity}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#tags LinuxFunctionAppSlot#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#timeouts LinuxFunctionAppSlot#timeouts}
        :param virtual_network_backup_restore_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#virtual_network_backup_restore_enabled LinuxFunctionAppSlot#virtual_network_backup_restore_enabled}.
        :param virtual_network_subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#virtual_network_subnet_id LinuxFunctionAppSlot#virtual_network_subnet_id}.
        :param vnet_image_pull_enabled: Is container image pull over virtual network enabled? Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#vnet_image_pull_enabled LinuxFunctionAppSlot#vnet_image_pull_enabled}
        :param webdeploy_publish_basic_authentication_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#webdeploy_publish_basic_authentication_enabled LinuxFunctionAppSlot#webdeploy_publish_basic_authentication_enabled}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78df0419662a3e06e4f514a5d781b72538709f9932eaae4a4f6c5940d9fbecc0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LinuxFunctionAppSlotConfig(
            function_app_id=function_app_id,
            name=name,
            site_config=site_config,
            app_settings=app_settings,
            auth_settings=auth_settings,
            auth_settings_v2=auth_settings_v2,
            backup=backup,
            builtin_logging_enabled=builtin_logging_enabled,
            client_certificate_enabled=client_certificate_enabled,
            client_certificate_exclusion_paths=client_certificate_exclusion_paths,
            client_certificate_mode=client_certificate_mode,
            connection_string=connection_string,
            content_share_force_disabled=content_share_force_disabled,
            daily_memory_time_quota=daily_memory_time_quota,
            enabled=enabled,
            ftp_publish_basic_authentication_enabled=ftp_publish_basic_authentication_enabled,
            functions_extension_version=functions_extension_version,
            https_only=https_only,
            id=id,
            identity=identity,
            key_vault_reference_identity_id=key_vault_reference_identity_id,
            public_network_access_enabled=public_network_access_enabled,
            service_plan_id=service_plan_id,
            storage_account=storage_account,
            storage_account_access_key=storage_account_access_key,
            storage_account_name=storage_account_name,
            storage_key_vault_secret_id=storage_key_vault_secret_id,
            storage_uses_managed_identity=storage_uses_managed_identity,
            tags=tags,
            timeouts=timeouts,
            virtual_network_backup_restore_enabled=virtual_network_backup_restore_enabled,
            virtual_network_subnet_id=virtual_network_subnet_id,
            vnet_image_pull_enabled=vnet_image_pull_enabled,
            webdeploy_publish_basic_authentication_enabled=webdeploy_publish_basic_authentication_enabled,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="generateConfigForImport")
    @builtins.classmethod
    def generate_config_for_import(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        import_to_id: builtins.str,
        import_from_id: builtins.str,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    ) -> _cdktf_9a9027ec.ImportableResource:
        '''Generates CDKTF code for importing a LinuxFunctionAppSlot resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the LinuxFunctionAppSlot to import.
        :param import_from_id: The id of the existing LinuxFunctionAppSlot that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the LinuxFunctionAppSlot to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ab1e0843eb08debf9e943c8639d6c59440e40f1e9ed376ebcc43567b7abecc6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAuthSettings")
    def put_auth_settings(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        active_directory: typing.Optional[typing.Union["LinuxFunctionAppSlotAuthSettingsActiveDirectory", typing.Dict[builtins.str, typing.Any]]] = None,
        additional_login_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        allowed_external_redirect_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_provider: typing.Optional[builtins.str] = None,
        facebook: typing.Optional[typing.Union["LinuxFunctionAppSlotAuthSettingsFacebook", typing.Dict[builtins.str, typing.Any]]] = None,
        github: typing.Optional[typing.Union["LinuxFunctionAppSlotAuthSettingsGithub", typing.Dict[builtins.str, typing.Any]]] = None,
        google: typing.Optional[typing.Union["LinuxFunctionAppSlotAuthSettingsGoogle", typing.Dict[builtins.str, typing.Any]]] = None,
        issuer: typing.Optional[builtins.str] = None,
        microsoft: typing.Optional[typing.Union["LinuxFunctionAppSlotAuthSettingsMicrosoft", typing.Dict[builtins.str, typing.Any]]] = None,
        runtime_version: typing.Optional[builtins.str] = None,
        token_refresh_extension_hours: typing.Optional[jsii.Number] = None,
        token_store_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        twitter: typing.Optional[typing.Union["LinuxFunctionAppSlotAuthSettingsTwitter", typing.Dict[builtins.str, typing.Any]]] = None,
        unauthenticated_client_action: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Should the Authentication / Authorization feature be enabled? Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#enabled LinuxFunctionAppSlot#enabled}
        :param active_directory: active_directory block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#active_directory LinuxFunctionAppSlot#active_directory}
        :param additional_login_parameters: Specifies a map of Login Parameters to send to the OpenID Connect authorization endpoint when a user logs in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#additional_login_parameters LinuxFunctionAppSlot#additional_login_parameters}
        :param allowed_external_redirect_urls: Specifies a list of External URLs that can be redirected to as part of logging in or logging out of the Windows Web App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#allowed_external_redirect_urls LinuxFunctionAppSlot#allowed_external_redirect_urls}
        :param default_provider: The default authentication provider to use when multiple providers are configured. Possible values include: ``AzureActiveDirectory``, ``Facebook``, ``Google``, ``MicrosoftAccount``, ``Twitter``, ``Github``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#default_provider LinuxFunctionAppSlot#default_provider}
        :param facebook: facebook block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#facebook LinuxFunctionAppSlot#facebook}
        :param github: github block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#github LinuxFunctionAppSlot#github}
        :param google: google block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#google LinuxFunctionAppSlot#google}
        :param issuer: The OpenID Connect Issuer URI that represents the entity which issues access tokens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#issuer LinuxFunctionAppSlot#issuer}
        :param microsoft: microsoft block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#microsoft LinuxFunctionAppSlot#microsoft}
        :param runtime_version: The RuntimeVersion of the Authentication / Authorization feature in use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#runtime_version LinuxFunctionAppSlot#runtime_version}
        :param token_refresh_extension_hours: The number of hours after session token expiration that a session token can be used to call the token refresh API. Defaults to ``72`` hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#token_refresh_extension_hours LinuxFunctionAppSlot#token_refresh_extension_hours}
        :param token_store_enabled: Should the Windows Web App durably store platform-specific security tokens that are obtained during login flows? Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#token_store_enabled LinuxFunctionAppSlot#token_store_enabled}
        :param twitter: twitter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#twitter LinuxFunctionAppSlot#twitter}
        :param unauthenticated_client_action: The action to take when an unauthenticated client attempts to access the app. Possible values include: ``RedirectToLoginPage``, ``AllowAnonymous``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#unauthenticated_client_action LinuxFunctionAppSlot#unauthenticated_client_action}
        '''
        value = LinuxFunctionAppSlotAuthSettings(
            enabled=enabled,
            active_directory=active_directory,
            additional_login_parameters=additional_login_parameters,
            allowed_external_redirect_urls=allowed_external_redirect_urls,
            default_provider=default_provider,
            facebook=facebook,
            github=github,
            google=google,
            issuer=issuer,
            microsoft=microsoft,
            runtime_version=runtime_version,
            token_refresh_extension_hours=token_refresh_extension_hours,
            token_store_enabled=token_store_enabled,
            twitter=twitter,
            unauthenticated_client_action=unauthenticated_client_action,
        )

        return typing.cast(None, jsii.invoke(self, "putAuthSettings", [value]))

    @jsii.member(jsii_name="putAuthSettingsV2")
    def put_auth_settings_v2(
        self,
        *,
        login: typing.Union["LinuxFunctionAppSlotAuthSettingsV2Login", typing.Dict[builtins.str, typing.Any]],
        active_directory_v2: typing.Optional[typing.Union["LinuxFunctionAppSlotAuthSettingsV2ActiveDirectoryV2", typing.Dict[builtins.str, typing.Any]]] = None,
        apple_v2: typing.Optional[typing.Union["LinuxFunctionAppSlotAuthSettingsV2AppleV2", typing.Dict[builtins.str, typing.Any]]] = None,
        auth_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        azure_static_web_app_v2: typing.Optional[typing.Union["LinuxFunctionAppSlotAuthSettingsV2AzureStaticWebAppV2", typing.Dict[builtins.str, typing.Any]]] = None,
        config_file_path: typing.Optional[builtins.str] = None,
        custom_oidc_v2: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LinuxFunctionAppSlotAuthSettingsV2CustomOidcV2", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_provider: typing.Optional[builtins.str] = None,
        excluded_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        facebook_v2: typing.Optional[typing.Union["LinuxFunctionAppSlotAuthSettingsV2FacebookV2", typing.Dict[builtins.str, typing.Any]]] = None,
        forward_proxy_convention: typing.Optional[builtins.str] = None,
        forward_proxy_custom_host_header_name: typing.Optional[builtins.str] = None,
        forward_proxy_custom_scheme_header_name: typing.Optional[builtins.str] = None,
        github_v2: typing.Optional[typing.Union["LinuxFunctionAppSlotAuthSettingsV2GithubV2", typing.Dict[builtins.str, typing.Any]]] = None,
        google_v2: typing.Optional[typing.Union["LinuxFunctionAppSlotAuthSettingsV2GoogleV2", typing.Dict[builtins.str, typing.Any]]] = None,
        http_route_api_prefix: typing.Optional[builtins.str] = None,
        microsoft_v2: typing.Optional[typing.Union["LinuxFunctionAppSlotAuthSettingsV2MicrosoftV2", typing.Dict[builtins.str, typing.Any]]] = None,
        require_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_https: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        runtime_version: typing.Optional[builtins.str] = None,
        twitter_v2: typing.Optional[typing.Union["LinuxFunctionAppSlotAuthSettingsV2TwitterV2", typing.Dict[builtins.str, typing.Any]]] = None,
        unauthenticated_action: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param login: login block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#login LinuxFunctionAppSlot#login}
        :param active_directory_v2: active_directory_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#active_directory_v2 LinuxFunctionAppSlot#active_directory_v2}
        :param apple_v2: apple_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#apple_v2 LinuxFunctionAppSlot#apple_v2}
        :param auth_enabled: Should the AuthV2 Settings be enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#auth_enabled LinuxFunctionAppSlot#auth_enabled}
        :param azure_static_web_app_v2: azure_static_web_app_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#azure_static_web_app_v2 LinuxFunctionAppSlot#azure_static_web_app_v2}
        :param config_file_path: The path to the App Auth settings. **Note:** Relative Paths are evaluated from the Site Root directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#config_file_path LinuxFunctionAppSlot#config_file_path}
        :param custom_oidc_v2: custom_oidc_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#custom_oidc_v2 LinuxFunctionAppSlot#custom_oidc_v2}
        :param default_provider: The Default Authentication Provider to use when the ``unauthenticated_action`` is set to ``RedirectToLoginPage``. Possible values include: ``apple``, ``azureactivedirectory``, ``facebook``, ``github``, ``google``, ``twitter`` and the ``name`` of your ``custom_oidc_v2`` provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#default_provider LinuxFunctionAppSlot#default_provider}
        :param excluded_paths: The paths which should be excluded from the ``unauthenticated_action`` when it is set to ``RedirectToLoginPage``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#excluded_paths LinuxFunctionAppSlot#excluded_paths}
        :param facebook_v2: facebook_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#facebook_v2 LinuxFunctionAppSlot#facebook_v2}
        :param forward_proxy_convention: The convention used to determine the url of the request made. Possible values include ``ForwardProxyConventionNoProxy``, ``ForwardProxyConventionStandard``, ``ForwardProxyConventionCustom``. Defaults to ``ForwardProxyConventionNoProxy`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#forward_proxy_convention LinuxFunctionAppSlot#forward_proxy_convention}
        :param forward_proxy_custom_host_header_name: The name of the header containing the host of the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#forward_proxy_custom_host_header_name LinuxFunctionAppSlot#forward_proxy_custom_host_header_name}
        :param forward_proxy_custom_scheme_header_name: The name of the header containing the scheme of the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#forward_proxy_custom_scheme_header_name LinuxFunctionAppSlot#forward_proxy_custom_scheme_header_name}
        :param github_v2: github_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#github_v2 LinuxFunctionAppSlot#github_v2}
        :param google_v2: google_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#google_v2 LinuxFunctionAppSlot#google_v2}
        :param http_route_api_prefix: The prefix that should precede all the authentication and authorisation paths. Defaults to ``/.auth``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#http_route_api_prefix LinuxFunctionAppSlot#http_route_api_prefix}
        :param microsoft_v2: microsoft_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#microsoft_v2 LinuxFunctionAppSlot#microsoft_v2}
        :param require_authentication: Should the authentication flow be used for all requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#require_authentication LinuxFunctionAppSlot#require_authentication}
        :param require_https: Should HTTPS be required on connections? Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#require_https LinuxFunctionAppSlot#require_https}
        :param runtime_version: The Runtime Version of the Authentication and Authorisation feature of this App. Defaults to ``~1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#runtime_version LinuxFunctionAppSlot#runtime_version}
        :param twitter_v2: twitter_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#twitter_v2 LinuxFunctionAppSlot#twitter_v2}
        :param unauthenticated_action: The action to take for requests made without authentication. Possible values include ``RedirectToLoginPage``, ``AllowAnonymous``, ``Return401``, and ``Return403``. Defaults to ``RedirectToLoginPage``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#unauthenticated_action LinuxFunctionAppSlot#unauthenticated_action}
        '''
        value = LinuxFunctionAppSlotAuthSettingsV2(
            login=login,
            active_directory_v2=active_directory_v2,
            apple_v2=apple_v2,
            auth_enabled=auth_enabled,
            azure_static_web_app_v2=azure_static_web_app_v2,
            config_file_path=config_file_path,
            custom_oidc_v2=custom_oidc_v2,
            default_provider=default_provider,
            excluded_paths=excluded_paths,
            facebook_v2=facebook_v2,
            forward_proxy_convention=forward_proxy_convention,
            forward_proxy_custom_host_header_name=forward_proxy_custom_host_header_name,
            forward_proxy_custom_scheme_header_name=forward_proxy_custom_scheme_header_name,
            github_v2=github_v2,
            google_v2=google_v2,
            http_route_api_prefix=http_route_api_prefix,
            microsoft_v2=microsoft_v2,
            require_authentication=require_authentication,
            require_https=require_https,
            runtime_version=runtime_version,
            twitter_v2=twitter_v2,
            unauthenticated_action=unauthenticated_action,
        )

        return typing.cast(None, jsii.invoke(self, "putAuthSettingsV2", [value]))

    @jsii.member(jsii_name="putBackup")
    def put_backup(
        self,
        *,
        name: builtins.str,
        schedule: typing.Union["LinuxFunctionAppSlotBackupSchedule", typing.Dict[builtins.str, typing.Any]],
        storage_account_url: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: The name which should be used for this Backup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#name LinuxFunctionAppSlot#name}
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#schedule LinuxFunctionAppSlot#schedule}
        :param storage_account_url: The SAS URL to the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#storage_account_url LinuxFunctionAppSlot#storage_account_url}
        :param enabled: Should this backup job be enabled? Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#enabled LinuxFunctionAppSlot#enabled}
        '''
        value = LinuxFunctionAppSlotBackup(
            name=name,
            schedule=schedule,
            storage_account_url=storage_account_url,
            enabled=enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putBackup", [value]))

    @jsii.member(jsii_name="putConnectionString")
    def put_connection_string(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LinuxFunctionAppSlotConnectionString", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7990af5003871d0e8a0a991327e4104d3161383ad27c45e47af5e6042eec787f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConnectionString", [value]))

    @jsii.member(jsii_name="putIdentity")
    def put_identity(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#type LinuxFunctionAppSlot#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#identity_ids LinuxFunctionAppSlot#identity_ids}.
        '''
        value = LinuxFunctionAppSlotIdentity(type=type, identity_ids=identity_ids)

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

    @jsii.member(jsii_name="putSiteConfig")
    def put_site_config(
        self,
        *,
        always_on: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        api_definition_url: typing.Optional[builtins.str] = None,
        api_management_api_id: typing.Optional[builtins.str] = None,
        app_command_line: typing.Optional[builtins.str] = None,
        application_insights_connection_string: typing.Optional[builtins.str] = None,
        application_insights_key: typing.Optional[builtins.str] = None,
        application_stack: typing.Optional[typing.Union["LinuxFunctionAppSlotSiteConfigApplicationStack", typing.Dict[builtins.str, typing.Any]]] = None,
        app_scale_limit: typing.Optional[jsii.Number] = None,
        app_service_logs: typing.Optional[typing.Union["LinuxFunctionAppSlotSiteConfigAppServiceLogs", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_swap_slot_name: typing.Optional[builtins.str] = None,
        container_registry_managed_identity_client_id: typing.Optional[builtins.str] = None,
        container_registry_use_managed_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cors: typing.Optional[typing.Union["LinuxFunctionAppSlotSiteConfigCors", typing.Dict[builtins.str, typing.Any]]] = None,
        default_documents: typing.Optional[typing.Sequence[builtins.str]] = None,
        elastic_instance_minimum: typing.Optional[jsii.Number] = None,
        ftps_state: typing.Optional[builtins.str] = None,
        health_check_eviction_time_in_min: typing.Optional[jsii.Number] = None,
        health_check_path: typing.Optional[builtins.str] = None,
        http2_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ip_restriction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LinuxFunctionAppSlotSiteConfigIpRestriction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ip_restriction_default_action: typing.Optional[builtins.str] = None,
        load_balancing_mode: typing.Optional[builtins.str] = None,
        managed_pipeline_mode: typing.Optional[builtins.str] = None,
        minimum_tls_version: typing.Optional[builtins.str] = None,
        pre_warmed_instance_count: typing.Optional[jsii.Number] = None,
        remote_debugging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        remote_debugging_version: typing.Optional[builtins.str] = None,
        runtime_scale_monitoring_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        scm_ip_restriction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LinuxFunctionAppSlotSiteConfigScmIpRestriction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        scm_ip_restriction_default_action: typing.Optional[builtins.str] = None,
        scm_minimum_tls_version: typing.Optional[builtins.str] = None,
        scm_use_main_ip_restriction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use32_bit_worker: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vnet_route_all_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        websockets_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        worker_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param always_on: If this Linux Web App is Always On enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#always_on LinuxFunctionAppSlot#always_on}
        :param api_definition_url: The URL of the API definition that describes this Linux Function App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#api_definition_url LinuxFunctionAppSlot#api_definition_url}
        :param api_management_api_id: The ID of the API Management API for this Linux Function App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#api_management_api_id LinuxFunctionAppSlot#api_management_api_id}
        :param app_command_line: The program and any arguments used to launch this app via the command line. (Example ``node myapp.js``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#app_command_line LinuxFunctionAppSlot#app_command_line}
        :param application_insights_connection_string: The Connection String for linking the Linux Function App to Application Insights. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#application_insights_connection_string LinuxFunctionAppSlot#application_insights_connection_string}
        :param application_insights_key: The Instrumentation Key for connecting the Linux Function App to Application Insights. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#application_insights_key LinuxFunctionAppSlot#application_insights_key}
        :param application_stack: application_stack block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#application_stack LinuxFunctionAppSlot#application_stack}
        :param app_scale_limit: The number of workers this function app can scale out to. Only applicable to apps on the Consumption and Premium plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#app_scale_limit LinuxFunctionAppSlot#app_scale_limit}
        :param app_service_logs: app_service_logs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#app_service_logs LinuxFunctionAppSlot#app_service_logs}
        :param auto_swap_slot_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#auto_swap_slot_name LinuxFunctionAppSlot#auto_swap_slot_name}.
        :param container_registry_managed_identity_client_id: The Client ID of the Managed Service Identity to use for connections to the Azure Container Registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#container_registry_managed_identity_client_id LinuxFunctionAppSlot#container_registry_managed_identity_client_id}
        :param container_registry_use_managed_identity: Should connections for Azure Container Registry use Managed Identity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#container_registry_use_managed_identity LinuxFunctionAppSlot#container_registry_use_managed_identity}
        :param cors: cors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#cors LinuxFunctionAppSlot#cors}
        :param default_documents: Specifies a list of Default Documents for the Linux Web App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#default_documents LinuxFunctionAppSlot#default_documents}
        :param elastic_instance_minimum: The number of minimum instances for this Linux Function App. Only affects apps on Elastic Premium plans. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#elastic_instance_minimum LinuxFunctionAppSlot#elastic_instance_minimum}
        :param ftps_state: State of FTP / FTPS service for this function app. Possible values include: ``AllAllowed``, ``FtpsOnly`` and ``Disabled``. Defaults to ``Disabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#ftps_state LinuxFunctionAppSlot#ftps_state}
        :param health_check_eviction_time_in_min: The amount of time in minutes that a node is unhealthy before being removed from the load balancer. Possible values are between ``2`` and ``10``. Defaults to ``10``. Only valid in conjunction with ``health_check_path`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#health_check_eviction_time_in_min LinuxFunctionAppSlot#health_check_eviction_time_in_min}
        :param health_check_path: The path to be checked for this function app health. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#health_check_path LinuxFunctionAppSlot#health_check_path}
        :param http2_enabled: Specifies if the http2 protocol should be enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#http2_enabled LinuxFunctionAppSlot#http2_enabled}
        :param ip_restriction: ip_restriction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#ip_restriction LinuxFunctionAppSlot#ip_restriction}
        :param ip_restriction_default_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#ip_restriction_default_action LinuxFunctionAppSlot#ip_restriction_default_action}.
        :param load_balancing_mode: The Site load balancing mode. Possible values include: ``WeightedRoundRobin``, ``LeastRequests``, ``LeastResponseTime``, ``WeightedTotalTraffic``, ``RequestHash``, ``PerSiteRoundRobin``. Defaults to ``LeastRequests`` if omitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#load_balancing_mode LinuxFunctionAppSlot#load_balancing_mode}
        :param managed_pipeline_mode: The Managed Pipeline mode. Possible values include: ``Integrated``, ``Classic``. Defaults to ``Integrated``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#managed_pipeline_mode LinuxFunctionAppSlot#managed_pipeline_mode}
        :param minimum_tls_version: The configures the minimum version of TLS required for SSL requests. Possible values include: ``1.0``, ``1.1``, ``1.2`` and ``1.3``. Defaults to ``1.2``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#minimum_tls_version LinuxFunctionAppSlot#minimum_tls_version}
        :param pre_warmed_instance_count: The number of pre-warmed instances for this function app. Only affects apps on an Elastic Premium plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#pre_warmed_instance_count LinuxFunctionAppSlot#pre_warmed_instance_count}
        :param remote_debugging_enabled: Should Remote Debugging be enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#remote_debugging_enabled LinuxFunctionAppSlot#remote_debugging_enabled}
        :param remote_debugging_version: The Remote Debugging Version. Currently only ``VS2022`` is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#remote_debugging_version LinuxFunctionAppSlot#remote_debugging_version}
        :param runtime_scale_monitoring_enabled: Should Functions Runtime Scale Monitoring be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#runtime_scale_monitoring_enabled LinuxFunctionAppSlot#runtime_scale_monitoring_enabled}
        :param scm_ip_restriction: scm_ip_restriction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#scm_ip_restriction LinuxFunctionAppSlot#scm_ip_restriction}
        :param scm_ip_restriction_default_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#scm_ip_restriction_default_action LinuxFunctionAppSlot#scm_ip_restriction_default_action}.
        :param scm_minimum_tls_version: Configures the minimum version of TLS required for SSL requests to the SCM site Possible values include: ``1.0``, ``1.1``, ``1.2`` and ``1.3``. Defaults to ``1.2``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#scm_minimum_tls_version LinuxFunctionAppSlot#scm_minimum_tls_version}
        :param scm_use_main_ip_restriction: Should the Linux Function App ``ip_restriction`` configuration be used for the SCM also. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#scm_use_main_ip_restriction LinuxFunctionAppSlot#scm_use_main_ip_restriction}
        :param use32_bit_worker: Should the Linux Web App use a 32-bit worker. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#use_32_bit_worker LinuxFunctionAppSlot#use_32_bit_worker}
        :param vnet_route_all_enabled: Should all outbound traffic to have Virtual Network Security Groups and User Defined Routes applied? Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#vnet_route_all_enabled LinuxFunctionAppSlot#vnet_route_all_enabled}
        :param websockets_enabled: Should Web Sockets be enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#websockets_enabled LinuxFunctionAppSlot#websockets_enabled}
        :param worker_count: The number of Workers for this Linux Function App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#worker_count LinuxFunctionAppSlot#worker_count}
        '''
        value = LinuxFunctionAppSlotSiteConfig(
            always_on=always_on,
            api_definition_url=api_definition_url,
            api_management_api_id=api_management_api_id,
            app_command_line=app_command_line,
            application_insights_connection_string=application_insights_connection_string,
            application_insights_key=application_insights_key,
            application_stack=application_stack,
            app_scale_limit=app_scale_limit,
            app_service_logs=app_service_logs,
            auto_swap_slot_name=auto_swap_slot_name,
            container_registry_managed_identity_client_id=container_registry_managed_identity_client_id,
            container_registry_use_managed_identity=container_registry_use_managed_identity,
            cors=cors,
            default_documents=default_documents,
            elastic_instance_minimum=elastic_instance_minimum,
            ftps_state=ftps_state,
            health_check_eviction_time_in_min=health_check_eviction_time_in_min,
            health_check_path=health_check_path,
            http2_enabled=http2_enabled,
            ip_restriction=ip_restriction,
            ip_restriction_default_action=ip_restriction_default_action,
            load_balancing_mode=load_balancing_mode,
            managed_pipeline_mode=managed_pipeline_mode,
            minimum_tls_version=minimum_tls_version,
            pre_warmed_instance_count=pre_warmed_instance_count,
            remote_debugging_enabled=remote_debugging_enabled,
            remote_debugging_version=remote_debugging_version,
            runtime_scale_monitoring_enabled=runtime_scale_monitoring_enabled,
            scm_ip_restriction=scm_ip_restriction,
            scm_ip_restriction_default_action=scm_ip_restriction_default_action,
            scm_minimum_tls_version=scm_minimum_tls_version,
            scm_use_main_ip_restriction=scm_use_main_ip_restriction,
            use32_bit_worker=use32_bit_worker,
            vnet_route_all_enabled=vnet_route_all_enabled,
            websockets_enabled=websockets_enabled,
            worker_count=worker_count,
        )

        return typing.cast(None, jsii.invoke(self, "putSiteConfig", [value]))

    @jsii.member(jsii_name="putStorageAccount")
    def put_storage_account(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LinuxFunctionAppSlotStorageAccount", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d5f3fde315b4bc3d9aa5bb90eb97f4718be8c7ff7f6bd5e3d35c142bc4eb19a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putStorageAccount", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#create LinuxFunctionAppSlot#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#delete LinuxFunctionAppSlot#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#read LinuxFunctionAppSlot#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#update LinuxFunctionAppSlot#update}.
        '''
        value = LinuxFunctionAppSlotTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAppSettings")
    def reset_app_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppSettings", []))

    @jsii.member(jsii_name="resetAuthSettings")
    def reset_auth_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthSettings", []))

    @jsii.member(jsii_name="resetAuthSettingsV2")
    def reset_auth_settings_v2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthSettingsV2", []))

    @jsii.member(jsii_name="resetBackup")
    def reset_backup(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBackup", []))

    @jsii.member(jsii_name="resetBuiltinLoggingEnabled")
    def reset_builtin_logging_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuiltinLoggingEnabled", []))

    @jsii.member(jsii_name="resetClientCertificateEnabled")
    def reset_client_certificate_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertificateEnabled", []))

    @jsii.member(jsii_name="resetClientCertificateExclusionPaths")
    def reset_client_certificate_exclusion_paths(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertificateExclusionPaths", []))

    @jsii.member(jsii_name="resetClientCertificateMode")
    def reset_client_certificate_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientCertificateMode", []))

    @jsii.member(jsii_name="resetConnectionString")
    def reset_connection_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionString", []))

    @jsii.member(jsii_name="resetContentShareForceDisabled")
    def reset_content_share_force_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContentShareForceDisabled", []))

    @jsii.member(jsii_name="resetDailyMemoryTimeQuota")
    def reset_daily_memory_time_quota(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDailyMemoryTimeQuota", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetFtpPublishBasicAuthenticationEnabled")
    def reset_ftp_publish_basic_authentication_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFtpPublishBasicAuthenticationEnabled", []))

    @jsii.member(jsii_name="resetFunctionsExtensionVersion")
    def reset_functions_extension_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFunctionsExtensionVersion", []))

    @jsii.member(jsii_name="resetHttpsOnly")
    def reset_https_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpsOnly", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetKeyVaultReferenceIdentityId")
    def reset_key_vault_reference_identity_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyVaultReferenceIdentityId", []))

    @jsii.member(jsii_name="resetPublicNetworkAccessEnabled")
    def reset_public_network_access_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicNetworkAccessEnabled", []))

    @jsii.member(jsii_name="resetServicePlanId")
    def reset_service_plan_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServicePlanId", []))

    @jsii.member(jsii_name="resetStorageAccount")
    def reset_storage_account(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageAccount", []))

    @jsii.member(jsii_name="resetStorageAccountAccessKey")
    def reset_storage_account_access_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageAccountAccessKey", []))

    @jsii.member(jsii_name="resetStorageAccountName")
    def reset_storage_account_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageAccountName", []))

    @jsii.member(jsii_name="resetStorageKeyVaultSecretId")
    def reset_storage_key_vault_secret_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageKeyVaultSecretId", []))

    @jsii.member(jsii_name="resetStorageUsesManagedIdentity")
    def reset_storage_uses_managed_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageUsesManagedIdentity", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVirtualNetworkBackupRestoreEnabled")
    def reset_virtual_network_backup_restore_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualNetworkBackupRestoreEnabled", []))

    @jsii.member(jsii_name="resetVirtualNetworkSubnetId")
    def reset_virtual_network_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualNetworkSubnetId", []))

    @jsii.member(jsii_name="resetVnetImagePullEnabled")
    def reset_vnet_image_pull_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVnetImagePullEnabled", []))

    @jsii.member(jsii_name="resetWebdeployPublishBasicAuthenticationEnabled")
    def reset_webdeploy_publish_basic_authentication_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebdeployPublishBasicAuthenticationEnabled", []))

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
    @jsii.member(jsii_name="authSettings")
    def auth_settings(self) -> "LinuxFunctionAppSlotAuthSettingsOutputReference":
        return typing.cast("LinuxFunctionAppSlotAuthSettingsOutputReference", jsii.get(self, "authSettings"))

    @builtins.property
    @jsii.member(jsii_name="authSettingsV2")
    def auth_settings_v2(self) -> "LinuxFunctionAppSlotAuthSettingsV2OutputReference":
        return typing.cast("LinuxFunctionAppSlotAuthSettingsV2OutputReference", jsii.get(self, "authSettingsV2"))

    @builtins.property
    @jsii.member(jsii_name="backup")
    def backup(self) -> "LinuxFunctionAppSlotBackupOutputReference":
        return typing.cast("LinuxFunctionAppSlotBackupOutputReference", jsii.get(self, "backup"))

    @builtins.property
    @jsii.member(jsii_name="connectionString")
    def connection_string(self) -> "LinuxFunctionAppSlotConnectionStringList":
        return typing.cast("LinuxFunctionAppSlotConnectionStringList", jsii.get(self, "connectionString"))

    @builtins.property
    @jsii.member(jsii_name="customDomainVerificationId")
    def custom_domain_verification_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customDomainVerificationId"))

    @builtins.property
    @jsii.member(jsii_name="defaultHostname")
    def default_hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultHostname"))

    @builtins.property
    @jsii.member(jsii_name="hostingEnvironmentId")
    def hosting_environment_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostingEnvironmentId"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "LinuxFunctionAppSlotIdentityOutputReference":
        return typing.cast("LinuxFunctionAppSlotIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="kind")
    def kind(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "kind"))

    @builtins.property
    @jsii.member(jsii_name="outboundIpAddresses")
    def outbound_ip_addresses(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outboundIpAddresses"))

    @builtins.property
    @jsii.member(jsii_name="outboundIpAddressList")
    def outbound_ip_address_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "outboundIpAddressList"))

    @builtins.property
    @jsii.member(jsii_name="possibleOutboundIpAddresses")
    def possible_outbound_ip_addresses(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "possibleOutboundIpAddresses"))

    @builtins.property
    @jsii.member(jsii_name="possibleOutboundIpAddressList")
    def possible_outbound_ip_address_list(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "possibleOutboundIpAddressList"))

    @builtins.property
    @jsii.member(jsii_name="siteConfig")
    def site_config(self) -> "LinuxFunctionAppSlotSiteConfigOutputReference":
        return typing.cast("LinuxFunctionAppSlotSiteConfigOutputReference", jsii.get(self, "siteConfig"))

    @builtins.property
    @jsii.member(jsii_name="siteCredential")
    def site_credential(self) -> "LinuxFunctionAppSlotSiteCredentialList":
        return typing.cast("LinuxFunctionAppSlotSiteCredentialList", jsii.get(self, "siteCredential"))

    @builtins.property
    @jsii.member(jsii_name="storageAccount")
    def storage_account(self) -> "LinuxFunctionAppSlotStorageAccountList":
        return typing.cast("LinuxFunctionAppSlotStorageAccountList", jsii.get(self, "storageAccount"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "LinuxFunctionAppSlotTimeoutsOutputReference":
        return typing.cast("LinuxFunctionAppSlotTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="appSettingsInput")
    def app_settings_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "appSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="authSettingsInput")
    def auth_settings_input(
        self,
    ) -> typing.Optional["LinuxFunctionAppSlotAuthSettings"]:
        return typing.cast(typing.Optional["LinuxFunctionAppSlotAuthSettings"], jsii.get(self, "authSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="authSettingsV2Input")
    def auth_settings_v2_input(
        self,
    ) -> typing.Optional["LinuxFunctionAppSlotAuthSettingsV2"]:
        return typing.cast(typing.Optional["LinuxFunctionAppSlotAuthSettingsV2"], jsii.get(self, "authSettingsV2Input"))

    @builtins.property
    @jsii.member(jsii_name="backupInput")
    def backup_input(self) -> typing.Optional["LinuxFunctionAppSlotBackup"]:
        return typing.cast(typing.Optional["LinuxFunctionAppSlotBackup"], jsii.get(self, "backupInput"))

    @builtins.property
    @jsii.member(jsii_name="builtinLoggingEnabledInput")
    def builtin_logging_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "builtinLoggingEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateEnabledInput")
    def client_certificate_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "clientCertificateEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateExclusionPathsInput")
    def client_certificate_exclusion_paths_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertificateExclusionPathsInput"))

    @builtins.property
    @jsii.member(jsii_name="clientCertificateModeInput")
    def client_certificate_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientCertificateModeInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionStringInput")
    def connection_string_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LinuxFunctionAppSlotConnectionString"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LinuxFunctionAppSlotConnectionString"]]], jsii.get(self, "connectionStringInput"))

    @builtins.property
    @jsii.member(jsii_name="contentShareForceDisabledInput")
    def content_share_force_disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "contentShareForceDisabledInput"))

    @builtins.property
    @jsii.member(jsii_name="dailyMemoryTimeQuotaInput")
    def daily_memory_time_quota_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dailyMemoryTimeQuotaInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="ftpPublishBasicAuthenticationEnabledInput")
    def ftp_publish_basic_authentication_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ftpPublishBasicAuthenticationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="functionAppIdInput")
    def function_app_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionAppIdInput"))

    @builtins.property
    @jsii.member(jsii_name="functionsExtensionVersionInput")
    def functions_extension_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "functionsExtensionVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="httpsOnlyInput")
    def https_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "httpsOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional["LinuxFunctionAppSlotIdentity"]:
        return typing.cast(typing.Optional["LinuxFunctionAppSlotIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="keyVaultReferenceIdentityIdInput")
    def key_vault_reference_identity_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyVaultReferenceIdentityIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="publicNetworkAccessEnabledInput")
    def public_network_access_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "publicNetworkAccessEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="servicePlanIdInput")
    def service_plan_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "servicePlanIdInput"))

    @builtins.property
    @jsii.member(jsii_name="siteConfigInput")
    def site_config_input(self) -> typing.Optional["LinuxFunctionAppSlotSiteConfig"]:
        return typing.cast(typing.Optional["LinuxFunctionAppSlotSiteConfig"], jsii.get(self, "siteConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountAccessKeyInput")
    def storage_account_access_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountAccessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountInput")
    def storage_account_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LinuxFunctionAppSlotStorageAccount"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LinuxFunctionAppSlotStorageAccount"]]], jsii.get(self, "storageAccountInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountNameInput")
    def storage_account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="storageKeyVaultSecretIdInput")
    def storage_key_vault_secret_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageKeyVaultSecretIdInput"))

    @builtins.property
    @jsii.member(jsii_name="storageUsesManagedIdentityInput")
    def storage_uses_managed_identity_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "storageUsesManagedIdentityInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "LinuxFunctionAppSlotTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "LinuxFunctionAppSlotTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkBackupRestoreEnabledInput")
    def virtual_network_backup_restore_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "virtualNetworkBackupRestoreEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkSubnetIdInput")
    def virtual_network_subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualNetworkSubnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="vnetImagePullEnabledInput")
    def vnet_image_pull_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "vnetImagePullEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="webdeployPublishBasicAuthenticationEnabledInput")
    def webdeploy_publish_basic_authentication_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "webdeployPublishBasicAuthenticationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="appSettings")
    def app_settings(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "appSettings"))

    @app_settings.setter
    def app_settings(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa604fa0b3da185a6c3585ce559531c5aa994c66e0a3554b8e219b372c22b44d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appSettings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="builtinLoggingEnabled")
    def builtin_logging_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "builtinLoggingEnabled"))

    @builtin_logging_enabled.setter
    def builtin_logging_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f029c15f87483faeff23949ed3e1e488ace2529fb2c9f2c4b019fbc4ee1c333)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "builtinLoggingEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCertificateEnabled")
    def client_certificate_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "clientCertificateEnabled"))

    @client_certificate_enabled.setter
    def client_certificate_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ac4d056771532a4a4cebbe26558de52c3358f121edb6d2cc374697c29703463)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificateEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCertificateExclusionPaths")
    def client_certificate_exclusion_paths(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificateExclusionPaths"))

    @client_certificate_exclusion_paths.setter
    def client_certificate_exclusion_paths(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b59fe8b3c06e46ec0357ef37fc5db3ba98eca21e1f95e3689d49c2c4168d3e79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificateExclusionPaths", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCertificateMode")
    def client_certificate_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificateMode"))

    @client_certificate_mode.setter
    def client_certificate_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f85b35dce986505903dc5dfaf2821df1c1419c88351770ee87ea88ba62a007e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificateMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="contentShareForceDisabled")
    def content_share_force_disabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "contentShareForceDisabled"))

    @content_share_force_disabled.setter
    def content_share_force_disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__225d802254c0a0f5d3c1b7a8bb94e3f07f7640a2bc1dc1b3aa468d7754796f05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentShareForceDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dailyMemoryTimeQuota")
    def daily_memory_time_quota(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dailyMemoryTimeQuota"))

    @daily_memory_time_quota.setter
    def daily_memory_time_quota(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72563994f81a07e9472b1e7a66078fbaa9513b0008db6cfc6a2824c73e5bbe24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dailyMemoryTimeQuota", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d91cabea7bbd9434eaadc2469d5cfb679c4e37d06483498370bed867690bc60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ftpPublishBasicAuthenticationEnabled")
    def ftp_publish_basic_authentication_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ftpPublishBasicAuthenticationEnabled"))

    @ftp_publish_basic_authentication_enabled.setter
    def ftp_publish_basic_authentication_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__838bf1886db7a66af93c96892dea18d1e8d15a3752aa4962af20277860c2fff9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ftpPublishBasicAuthenticationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="functionAppId")
    def function_app_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionAppId"))

    @function_app_id.setter
    def function_app_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5cb7bfb5260e2ae57a538a44c50c4c8534d7b1e8e6d88da53e31898782849e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionAppId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="functionsExtensionVersion")
    def functions_extension_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "functionsExtensionVersion"))

    @functions_extension_version.setter
    def functions_extension_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a13e732252f18ec7810da0aca8ad793f5b53c8978d6d51a076b8378f563abd00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "functionsExtensionVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpsOnly")
    def https_only(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "httpsOnly"))

    @https_only.setter
    def https_only(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11aa8338f3c3937bbdc5bebb8462fbc39a6e9f641a9ba3254b5c774d8a41a6a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86ba1724106db3333d9cd00875872f9e81ac2d5743e357be79569eafdc91f37c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyVaultReferenceIdentityId")
    def key_vault_reference_identity_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyVaultReferenceIdentityId"))

    @key_vault_reference_identity_id.setter
    def key_vault_reference_identity_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__728a26fa49201905f106f0a4cbbffacba36b7a4e4cb4eda3d6aa20d4a71cad45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyVaultReferenceIdentityId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea798b3118a5c5ef774db0addf8e3ace14e55a22dd3f1d5fb43d2ebadc256e38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publicNetworkAccessEnabled")
    def public_network_access_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "publicNetworkAccessEnabled"))

    @public_network_access_enabled.setter
    def public_network_access_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf428b6ccbc0486462a14c2acf6e535cd8f9ace6ea58e254a69035827a933843)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicNetworkAccessEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="servicePlanId")
    def service_plan_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "servicePlanId"))

    @service_plan_id.setter
    def service_plan_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51d882abee194b112fe9bf241fbb14bd70166ceb82710a1dfb22c5713237ec27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "servicePlanId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountAccessKey")
    def storage_account_access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountAccessKey"))

    @storage_account_access_key.setter
    def storage_account_access_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cadbdfa274bddf868efa2c8e78d9bad7f62aaed4ef3050f01dbab2cbf3a34788)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountAccessKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountName")
    def storage_account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountName"))

    @storage_account_name.setter
    def storage_account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a19aafa7deae0233ee064d64aba7636eef7c4a99325534762074200fa7dfd2c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageKeyVaultSecretId")
    def storage_key_vault_secret_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageKeyVaultSecretId"))

    @storage_key_vault_secret_id.setter
    def storage_key_vault_secret_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f57aadfd8056829d12978d6e3c0deaff46d9db31794ded5f22f5f6e9b0515c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageKeyVaultSecretId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageUsesManagedIdentity")
    def storage_uses_managed_identity(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "storageUsesManagedIdentity"))

    @storage_uses_managed_identity.setter
    def storage_uses_managed_identity(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f61511be1ed233d174620fbc622a6fe8620215e74b36de921265b03246cf6923)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageUsesManagedIdentity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__834ead9eb54c179b92c6af6a50427e0e4d463dcd5fe3e77cd59f2b3402d55faa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkBackupRestoreEnabled")
    def virtual_network_backup_restore_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "virtualNetworkBackupRestoreEnabled"))

    @virtual_network_backup_restore_enabled.setter
    def virtual_network_backup_restore_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e0921a9e1b51e14e8c77ca4e5ef6cd3068722c5c85163087b5209b2654bc414)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkBackupRestoreEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkSubnetId")
    def virtual_network_subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkSubnetId"))

    @virtual_network_subnet_id.setter
    def virtual_network_subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb430714bfaa0f6fd9e4c9e4d20990c1c840c36fbbf93073557aea70c5cae4ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkSubnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vnetImagePullEnabled")
    def vnet_image_pull_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "vnetImagePullEnabled"))

    @vnet_image_pull_enabled.setter
    def vnet_image_pull_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__001bd18f55fac43c5ec603afc17161d630fdc3c94db85141be6b105ad1279090)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vnetImagePullEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webdeployPublishBasicAuthenticationEnabled")
    def webdeploy_publish_basic_authentication_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "webdeployPublishBasicAuthenticationEnabled"))

    @webdeploy_publish_basic_authentication_enabled.setter
    def webdeploy_publish_basic_authentication_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2efab8c919e07809e3889d7c8b0bf0ea2442041a28ddcd6c092af63f7c356aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webdeployPublishBasicAuthenticationEnabled", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettings",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "active_directory": "activeDirectory",
        "additional_login_parameters": "additionalLoginParameters",
        "allowed_external_redirect_urls": "allowedExternalRedirectUrls",
        "default_provider": "defaultProvider",
        "facebook": "facebook",
        "github": "github",
        "google": "google",
        "issuer": "issuer",
        "microsoft": "microsoft",
        "runtime_version": "runtimeVersion",
        "token_refresh_extension_hours": "tokenRefreshExtensionHours",
        "token_store_enabled": "tokenStoreEnabled",
        "twitter": "twitter",
        "unauthenticated_client_action": "unauthenticatedClientAction",
    },
)
class LinuxFunctionAppSlotAuthSettings:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        active_directory: typing.Optional[typing.Union["LinuxFunctionAppSlotAuthSettingsActiveDirectory", typing.Dict[builtins.str, typing.Any]]] = None,
        additional_login_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        allowed_external_redirect_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_provider: typing.Optional[builtins.str] = None,
        facebook: typing.Optional[typing.Union["LinuxFunctionAppSlotAuthSettingsFacebook", typing.Dict[builtins.str, typing.Any]]] = None,
        github: typing.Optional[typing.Union["LinuxFunctionAppSlotAuthSettingsGithub", typing.Dict[builtins.str, typing.Any]]] = None,
        google: typing.Optional[typing.Union["LinuxFunctionAppSlotAuthSettingsGoogle", typing.Dict[builtins.str, typing.Any]]] = None,
        issuer: typing.Optional[builtins.str] = None,
        microsoft: typing.Optional[typing.Union["LinuxFunctionAppSlotAuthSettingsMicrosoft", typing.Dict[builtins.str, typing.Any]]] = None,
        runtime_version: typing.Optional[builtins.str] = None,
        token_refresh_extension_hours: typing.Optional[jsii.Number] = None,
        token_store_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        twitter: typing.Optional[typing.Union["LinuxFunctionAppSlotAuthSettingsTwitter", typing.Dict[builtins.str, typing.Any]]] = None,
        unauthenticated_client_action: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Should the Authentication / Authorization feature be enabled? Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#enabled LinuxFunctionAppSlot#enabled}
        :param active_directory: active_directory block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#active_directory LinuxFunctionAppSlot#active_directory}
        :param additional_login_parameters: Specifies a map of Login Parameters to send to the OpenID Connect authorization endpoint when a user logs in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#additional_login_parameters LinuxFunctionAppSlot#additional_login_parameters}
        :param allowed_external_redirect_urls: Specifies a list of External URLs that can be redirected to as part of logging in or logging out of the Windows Web App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#allowed_external_redirect_urls LinuxFunctionAppSlot#allowed_external_redirect_urls}
        :param default_provider: The default authentication provider to use when multiple providers are configured. Possible values include: ``AzureActiveDirectory``, ``Facebook``, ``Google``, ``MicrosoftAccount``, ``Twitter``, ``Github``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#default_provider LinuxFunctionAppSlot#default_provider}
        :param facebook: facebook block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#facebook LinuxFunctionAppSlot#facebook}
        :param github: github block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#github LinuxFunctionAppSlot#github}
        :param google: google block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#google LinuxFunctionAppSlot#google}
        :param issuer: The OpenID Connect Issuer URI that represents the entity which issues access tokens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#issuer LinuxFunctionAppSlot#issuer}
        :param microsoft: microsoft block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#microsoft LinuxFunctionAppSlot#microsoft}
        :param runtime_version: The RuntimeVersion of the Authentication / Authorization feature in use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#runtime_version LinuxFunctionAppSlot#runtime_version}
        :param token_refresh_extension_hours: The number of hours after session token expiration that a session token can be used to call the token refresh API. Defaults to ``72`` hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#token_refresh_extension_hours LinuxFunctionAppSlot#token_refresh_extension_hours}
        :param token_store_enabled: Should the Windows Web App durably store platform-specific security tokens that are obtained during login flows? Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#token_store_enabled LinuxFunctionAppSlot#token_store_enabled}
        :param twitter: twitter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#twitter LinuxFunctionAppSlot#twitter}
        :param unauthenticated_client_action: The action to take when an unauthenticated client attempts to access the app. Possible values include: ``RedirectToLoginPage``, ``AllowAnonymous``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#unauthenticated_client_action LinuxFunctionAppSlot#unauthenticated_client_action}
        '''
        if isinstance(active_directory, dict):
            active_directory = LinuxFunctionAppSlotAuthSettingsActiveDirectory(**active_directory)
        if isinstance(facebook, dict):
            facebook = LinuxFunctionAppSlotAuthSettingsFacebook(**facebook)
        if isinstance(github, dict):
            github = LinuxFunctionAppSlotAuthSettingsGithub(**github)
        if isinstance(google, dict):
            google = LinuxFunctionAppSlotAuthSettingsGoogle(**google)
        if isinstance(microsoft, dict):
            microsoft = LinuxFunctionAppSlotAuthSettingsMicrosoft(**microsoft)
        if isinstance(twitter, dict):
            twitter = LinuxFunctionAppSlotAuthSettingsTwitter(**twitter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9f434d3380681049777a602ae400de79c9711afec806ec4b54cc70f7028219e)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument active_directory", value=active_directory, expected_type=type_hints["active_directory"])
            check_type(argname="argument additional_login_parameters", value=additional_login_parameters, expected_type=type_hints["additional_login_parameters"])
            check_type(argname="argument allowed_external_redirect_urls", value=allowed_external_redirect_urls, expected_type=type_hints["allowed_external_redirect_urls"])
            check_type(argname="argument default_provider", value=default_provider, expected_type=type_hints["default_provider"])
            check_type(argname="argument facebook", value=facebook, expected_type=type_hints["facebook"])
            check_type(argname="argument github", value=github, expected_type=type_hints["github"])
            check_type(argname="argument google", value=google, expected_type=type_hints["google"])
            check_type(argname="argument issuer", value=issuer, expected_type=type_hints["issuer"])
            check_type(argname="argument microsoft", value=microsoft, expected_type=type_hints["microsoft"])
            check_type(argname="argument runtime_version", value=runtime_version, expected_type=type_hints["runtime_version"])
            check_type(argname="argument token_refresh_extension_hours", value=token_refresh_extension_hours, expected_type=type_hints["token_refresh_extension_hours"])
            check_type(argname="argument token_store_enabled", value=token_store_enabled, expected_type=type_hints["token_store_enabled"])
            check_type(argname="argument twitter", value=twitter, expected_type=type_hints["twitter"])
            check_type(argname="argument unauthenticated_client_action", value=unauthenticated_client_action, expected_type=type_hints["unauthenticated_client_action"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if active_directory is not None:
            self._values["active_directory"] = active_directory
        if additional_login_parameters is not None:
            self._values["additional_login_parameters"] = additional_login_parameters
        if allowed_external_redirect_urls is not None:
            self._values["allowed_external_redirect_urls"] = allowed_external_redirect_urls
        if default_provider is not None:
            self._values["default_provider"] = default_provider
        if facebook is not None:
            self._values["facebook"] = facebook
        if github is not None:
            self._values["github"] = github
        if google is not None:
            self._values["google"] = google
        if issuer is not None:
            self._values["issuer"] = issuer
        if microsoft is not None:
            self._values["microsoft"] = microsoft
        if runtime_version is not None:
            self._values["runtime_version"] = runtime_version
        if token_refresh_extension_hours is not None:
            self._values["token_refresh_extension_hours"] = token_refresh_extension_hours
        if token_store_enabled is not None:
            self._values["token_store_enabled"] = token_store_enabled
        if twitter is not None:
            self._values["twitter"] = twitter
        if unauthenticated_client_action is not None:
            self._values["unauthenticated_client_action"] = unauthenticated_client_action

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Should the Authentication / Authorization feature be enabled?

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#enabled LinuxFunctionAppSlot#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def active_directory(
        self,
    ) -> typing.Optional["LinuxFunctionAppSlotAuthSettingsActiveDirectory"]:
        '''active_directory block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#active_directory LinuxFunctionAppSlot#active_directory}
        '''
        result = self._values.get("active_directory")
        return typing.cast(typing.Optional["LinuxFunctionAppSlotAuthSettingsActiveDirectory"], result)

    @builtins.property
    def additional_login_parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Specifies a map of Login Parameters to send to the OpenID Connect authorization endpoint when a user logs in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#additional_login_parameters LinuxFunctionAppSlot#additional_login_parameters}
        '''
        result = self._values.get("additional_login_parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def allowed_external_redirect_urls(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of External URLs that can be redirected to as part of logging in or logging out of the Windows Web App.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#allowed_external_redirect_urls LinuxFunctionAppSlot#allowed_external_redirect_urls}
        '''
        result = self._values.get("allowed_external_redirect_urls")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def default_provider(self) -> typing.Optional[builtins.str]:
        '''The default authentication provider to use when multiple providers are configured.

        Possible values include: ``AzureActiveDirectory``, ``Facebook``, ``Google``, ``MicrosoftAccount``, ``Twitter``, ``Github``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#default_provider LinuxFunctionAppSlot#default_provider}
        '''
        result = self._values.get("default_provider")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def facebook(self) -> typing.Optional["LinuxFunctionAppSlotAuthSettingsFacebook"]:
        '''facebook block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#facebook LinuxFunctionAppSlot#facebook}
        '''
        result = self._values.get("facebook")
        return typing.cast(typing.Optional["LinuxFunctionAppSlotAuthSettingsFacebook"], result)

    @builtins.property
    def github(self) -> typing.Optional["LinuxFunctionAppSlotAuthSettingsGithub"]:
        '''github block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#github LinuxFunctionAppSlot#github}
        '''
        result = self._values.get("github")
        return typing.cast(typing.Optional["LinuxFunctionAppSlotAuthSettingsGithub"], result)

    @builtins.property
    def google(self) -> typing.Optional["LinuxFunctionAppSlotAuthSettingsGoogle"]:
        '''google block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#google LinuxFunctionAppSlot#google}
        '''
        result = self._values.get("google")
        return typing.cast(typing.Optional["LinuxFunctionAppSlotAuthSettingsGoogle"], result)

    @builtins.property
    def issuer(self) -> typing.Optional[builtins.str]:
        '''The OpenID Connect Issuer URI that represents the entity which issues access tokens.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#issuer LinuxFunctionAppSlot#issuer}
        '''
        result = self._values.get("issuer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def microsoft(self) -> typing.Optional["LinuxFunctionAppSlotAuthSettingsMicrosoft"]:
        '''microsoft block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#microsoft LinuxFunctionAppSlot#microsoft}
        '''
        result = self._values.get("microsoft")
        return typing.cast(typing.Optional["LinuxFunctionAppSlotAuthSettingsMicrosoft"], result)

    @builtins.property
    def runtime_version(self) -> typing.Optional[builtins.str]:
        '''The RuntimeVersion of the Authentication / Authorization feature in use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#runtime_version LinuxFunctionAppSlot#runtime_version}
        '''
        result = self._values.get("runtime_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_refresh_extension_hours(self) -> typing.Optional[jsii.Number]:
        '''The number of hours after session token expiration that a session token can be used to call the token refresh API.

        Defaults to ``72`` hours.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#token_refresh_extension_hours LinuxFunctionAppSlot#token_refresh_extension_hours}
        '''
        result = self._values.get("token_refresh_extension_hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def token_store_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the Windows Web App durably store platform-specific security tokens that are obtained during login flows? Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#token_store_enabled LinuxFunctionAppSlot#token_store_enabled}
        '''
        result = self._values.get("token_store_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def twitter(self) -> typing.Optional["LinuxFunctionAppSlotAuthSettingsTwitter"]:
        '''twitter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#twitter LinuxFunctionAppSlot#twitter}
        '''
        result = self._values.get("twitter")
        return typing.cast(typing.Optional["LinuxFunctionAppSlotAuthSettingsTwitter"], result)

    @builtins.property
    def unauthenticated_client_action(self) -> typing.Optional[builtins.str]:
        '''The action to take when an unauthenticated client attempts to access the app. Possible values include: ``RedirectToLoginPage``, ``AllowAnonymous``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#unauthenticated_client_action LinuxFunctionAppSlot#unauthenticated_client_action}
        '''
        result = self._values.get("unauthenticated_client_action")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotAuthSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsActiveDirectory",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "allowed_audiences": "allowedAudiences",
        "client_secret": "clientSecret",
        "client_secret_setting_name": "clientSecretSettingName",
    },
)
class LinuxFunctionAppSlotAuthSettingsActiveDirectory:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        allowed_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
        client_secret: typing.Optional[builtins.str] = None,
        client_secret_setting_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: The ID of the Client to use to authenticate with Azure Active Directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_id LinuxFunctionAppSlot#client_id}
        :param allowed_audiences: Specifies a list of Allowed audience values to consider when validating JWTs issued by Azure Active Directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#allowed_audiences LinuxFunctionAppSlot#allowed_audiences}
        :param client_secret: The Client Secret for the Client ID. Cannot be used with ``client_secret_setting_name``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret LinuxFunctionAppSlot#client_secret}
        :param client_secret_setting_name: The App Setting name that contains the client secret of the Client. Cannot be used with ``client_secret``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret_setting_name LinuxFunctionAppSlot#client_secret_setting_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__352d8cd74b2240944ed3004f6e4d3c13ff186b0fb1c95d938ee2cc9cb646dc83)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument allowed_audiences", value=allowed_audiences, expected_type=type_hints["allowed_audiences"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument client_secret_setting_name", value=client_secret_setting_name, expected_type=type_hints["client_secret_setting_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
        }
        if allowed_audiences is not None:
            self._values["allowed_audiences"] = allowed_audiences
        if client_secret is not None:
            self._values["client_secret"] = client_secret
        if client_secret_setting_name is not None:
            self._values["client_secret_setting_name"] = client_secret_setting_name

    @builtins.property
    def client_id(self) -> builtins.str:
        '''The ID of the Client to use to authenticate with Azure Active Directory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_id LinuxFunctionAppSlot#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_audiences(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of Allowed audience values to consider when validating JWTs issued by Azure Active Directory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#allowed_audiences LinuxFunctionAppSlot#allowed_audiences}
        '''
        result = self._values.get("allowed_audiences")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''The Client Secret for the Client ID. Cannot be used with ``client_secret_setting_name``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret LinuxFunctionAppSlot#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret_setting_name(self) -> typing.Optional[builtins.str]:
        '''The App Setting name that contains the client secret of the Client. Cannot be used with ``client_secret``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret_setting_name LinuxFunctionAppSlot#client_secret_setting_name}
        '''
        result = self._values.get("client_secret_setting_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotAuthSettingsActiveDirectory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LinuxFunctionAppSlotAuthSettingsActiveDirectoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsActiveDirectoryOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ff6e70fb544ace3d9f1e408b1db51cc3abb9330804f58cd5c4003f95cc677ad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedAudiences")
    def reset_allowed_audiences(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedAudiences", []))

    @jsii.member(jsii_name="resetClientSecret")
    def reset_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecret", []))

    @jsii.member(jsii_name="resetClientSecretSettingName")
    def reset_client_secret_setting_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecretSettingName", []))

    @builtins.property
    @jsii.member(jsii_name="allowedAudiencesInput")
    def allowed_audiences_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedAudiencesInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingNameInput")
    def client_secret_setting_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretSettingNameInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedAudiences")
    def allowed_audiences(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedAudiences"))

    @allowed_audiences.setter
    def allowed_audiences(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31235fe242310bfac756370b39af68e26e4fd7eb6320cbedd595f7d5a47328b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedAudiences", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e6a9dec3ca09ca5897eb9d826a31ce2e48ca15a1f73cdbc3c65168c9e62db61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81dad42dd5973675430851c16af09e80d76b9cf9fac85e272b82bab92a679dc9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingName")
    def client_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecretSettingName"))

    @client_secret_setting_name.setter
    def client_secret_setting_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8673149783fedd3285cbb70b9ae11878bb3cb70a132fd688439c45822f087d8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecretSettingName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LinuxFunctionAppSlotAuthSettingsActiveDirectory]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotAuthSettingsActiveDirectory], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LinuxFunctionAppSlotAuthSettingsActiveDirectory],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9d113893b02f558dabb46e3c587e3e97a79a786d8356e2af6e4e763be629a73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsFacebook",
    jsii_struct_bases=[],
    name_mapping={
        "app_id": "appId",
        "app_secret": "appSecret",
        "app_secret_setting_name": "appSecretSettingName",
        "oauth_scopes": "oauthScopes",
    },
)
class LinuxFunctionAppSlotAuthSettingsFacebook:
    def __init__(
        self,
        *,
        app_id: builtins.str,
        app_secret: typing.Optional[builtins.str] = None,
        app_secret_setting_name: typing.Optional[builtins.str] = None,
        oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param app_id: The App ID of the Facebook app used for login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#app_id LinuxFunctionAppSlot#app_id}
        :param app_secret: The App Secret of the Facebook app used for Facebook Login. Cannot be specified with ``app_secret_setting_name``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#app_secret LinuxFunctionAppSlot#app_secret}
        :param app_secret_setting_name: The app setting name that contains the ``app_secret`` value used for Facebook Login. Cannot be specified with ``app_secret``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#app_secret_setting_name LinuxFunctionAppSlot#app_secret_setting_name}
        :param oauth_scopes: Specifies a list of OAuth 2.0 scopes to be requested as part of Facebook Login authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#oauth_scopes LinuxFunctionAppSlot#oauth_scopes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa44718e5ed4256e6d36f5b5355d9771751744288285f1596a7f76d007973f3e)
            check_type(argname="argument app_id", value=app_id, expected_type=type_hints["app_id"])
            check_type(argname="argument app_secret", value=app_secret, expected_type=type_hints["app_secret"])
            check_type(argname="argument app_secret_setting_name", value=app_secret_setting_name, expected_type=type_hints["app_secret_setting_name"])
            check_type(argname="argument oauth_scopes", value=oauth_scopes, expected_type=type_hints["oauth_scopes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_id": app_id,
        }
        if app_secret is not None:
            self._values["app_secret"] = app_secret
        if app_secret_setting_name is not None:
            self._values["app_secret_setting_name"] = app_secret_setting_name
        if oauth_scopes is not None:
            self._values["oauth_scopes"] = oauth_scopes

    @builtins.property
    def app_id(self) -> builtins.str:
        '''The App ID of the Facebook app used for login.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#app_id LinuxFunctionAppSlot#app_id}
        '''
        result = self._values.get("app_id")
        assert result is not None, "Required property 'app_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_secret(self) -> typing.Optional[builtins.str]:
        '''The App Secret of the Facebook app used for Facebook Login. Cannot be specified with ``app_secret_setting_name``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#app_secret LinuxFunctionAppSlot#app_secret}
        '''
        result = self._values.get("app_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app_secret_setting_name(self) -> typing.Optional[builtins.str]:
        '''The app setting name that contains the ``app_secret`` value used for Facebook Login. Cannot be specified with ``app_secret``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#app_secret_setting_name LinuxFunctionAppSlot#app_secret_setting_name}
        '''
        result = self._values.get("app_secret_setting_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of OAuth 2.0 scopes to be requested as part of Facebook Login authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#oauth_scopes LinuxFunctionAppSlot#oauth_scopes}
        '''
        result = self._values.get("oauth_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotAuthSettingsFacebook(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LinuxFunctionAppSlotAuthSettingsFacebookOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsFacebookOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__583f00a8f247134ab910297e80d04ab63fdd005c3e28f744fc7454b7de7a09a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAppSecret")
    def reset_app_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppSecret", []))

    @jsii.member(jsii_name="resetAppSecretSettingName")
    def reset_app_secret_setting_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppSecretSettingName", []))

    @jsii.member(jsii_name="resetOauthScopes")
    def reset_oauth_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthScopes", []))

    @builtins.property
    @jsii.member(jsii_name="appIdInput")
    def app_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appIdInput"))

    @builtins.property
    @jsii.member(jsii_name="appSecretInput")
    def app_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="appSecretSettingNameInput")
    def app_secret_setting_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appSecretSettingNameInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthScopesInput")
    def oauth_scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "oauthScopesInput"))

    @builtins.property
    @jsii.member(jsii_name="appId")
    def app_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appId"))

    @app_id.setter
    def app_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8b43644535823a90236a5e4327b5cf24a1e590a1ff519b523dbe43e6a80fd51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appSecret")
    def app_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appSecret"))

    @app_secret.setter
    def app_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04e1369f0e47e239c9ee1f31fd302f67b2de8682fab8ee285760c76db3864059)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appSecretSettingName")
    def app_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appSecretSettingName"))

    @app_secret_setting_name.setter
    def app_secret_setting_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__659b546e53225d39af9d5af323fb910e0c8cbe130785a08c948f42507d43bdb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appSecretSettingName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthScopes")
    def oauth_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "oauthScopes"))

    @oauth_scopes.setter
    def oauth_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa9ea48fe03adec41925c4e2e9dc3efb5437c67a9ad084f599ba7962d1d93f2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthScopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LinuxFunctionAppSlotAuthSettingsFacebook]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotAuthSettingsFacebook], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LinuxFunctionAppSlotAuthSettingsFacebook],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8085f71925aa9b92f7b74ffaa7744edfa0198d2b940c158c4f9a24cdb68ba7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsGithub",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "client_secret_setting_name": "clientSecretSettingName",
        "oauth_scopes": "oauthScopes",
    },
)
class LinuxFunctionAppSlotAuthSettingsGithub:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        client_secret: typing.Optional[builtins.str] = None,
        client_secret_setting_name: typing.Optional[builtins.str] = None,
        oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param client_id: The ID of the GitHub app used for login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_id LinuxFunctionAppSlot#client_id}
        :param client_secret: The Client Secret of the GitHub app used for GitHub Login. Cannot be specified with ``client_secret_setting_name``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret LinuxFunctionAppSlot#client_secret}
        :param client_secret_setting_name: The app setting name that contains the ``client_secret`` value used for GitHub Login. Cannot be specified with ``client_secret``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret_setting_name LinuxFunctionAppSlot#client_secret_setting_name}
        :param oauth_scopes: Specifies a list of OAuth 2.0 scopes that will be requested as part of GitHub Login authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#oauth_scopes LinuxFunctionAppSlot#oauth_scopes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92da1b48820dd2f5297bc224c5c43edb74f40c29910580ccaeaeda324cc31758)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument client_secret_setting_name", value=client_secret_setting_name, expected_type=type_hints["client_secret_setting_name"])
            check_type(argname="argument oauth_scopes", value=oauth_scopes, expected_type=type_hints["oauth_scopes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
        }
        if client_secret is not None:
            self._values["client_secret"] = client_secret
        if client_secret_setting_name is not None:
            self._values["client_secret_setting_name"] = client_secret_setting_name
        if oauth_scopes is not None:
            self._values["oauth_scopes"] = oauth_scopes

    @builtins.property
    def client_id(self) -> builtins.str:
        '''The ID of the GitHub app used for login.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_id LinuxFunctionAppSlot#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''The Client Secret of the GitHub app used for GitHub Login. Cannot be specified with ``client_secret_setting_name``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret LinuxFunctionAppSlot#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret_setting_name(self) -> typing.Optional[builtins.str]:
        '''The app setting name that contains the ``client_secret`` value used for GitHub Login. Cannot be specified with ``client_secret``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret_setting_name LinuxFunctionAppSlot#client_secret_setting_name}
        '''
        result = self._values.get("client_secret_setting_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of OAuth 2.0 scopes that will be requested as part of GitHub Login authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#oauth_scopes LinuxFunctionAppSlot#oauth_scopes}
        '''
        result = self._values.get("oauth_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotAuthSettingsGithub(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LinuxFunctionAppSlotAuthSettingsGithubOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsGithubOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__528b99ab8961a0c6668e8ee8cf82fbe4408e9118addac646a2dbd36944160fdb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClientSecret")
    def reset_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecret", []))

    @jsii.member(jsii_name="resetClientSecretSettingName")
    def reset_client_secret_setting_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecretSettingName", []))

    @jsii.member(jsii_name="resetOauthScopes")
    def reset_oauth_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthScopes", []))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingNameInput")
    def client_secret_setting_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretSettingNameInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthScopesInput")
    def oauth_scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "oauthScopesInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cbcd86af02da8a205ff07502a82e8f5a9fa7b03adc314be38284f98213643d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c293dfc3574f6c58b4586e096ce6e97cb7849ff025ad9c9e8edcfecffbb68a06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingName")
    def client_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecretSettingName"))

    @client_secret_setting_name.setter
    def client_secret_setting_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af7709b5a4164bebbf81e82b7e1e43a99682ce13c3e515a2c1d0d91a8b3ef93e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecretSettingName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthScopes")
    def oauth_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "oauthScopes"))

    @oauth_scopes.setter
    def oauth_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0cd1d1773a17bc120d80378d6b0c83f91c863e755c6ad642d2010b73b2096a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthScopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LinuxFunctionAppSlotAuthSettingsGithub]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotAuthSettingsGithub], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LinuxFunctionAppSlotAuthSettingsGithub],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6088a41ed6752dce25adcc3126972ff044f5fb23d687194aad5d1904a58731b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsGoogle",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "client_secret_setting_name": "clientSecretSettingName",
        "oauth_scopes": "oauthScopes",
    },
)
class LinuxFunctionAppSlotAuthSettingsGoogle:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        client_secret: typing.Optional[builtins.str] = None,
        client_secret_setting_name: typing.Optional[builtins.str] = None,
        oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param client_id: The OpenID Connect Client ID for the Google web application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_id LinuxFunctionAppSlot#client_id}
        :param client_secret: The client secret associated with the Google web application. Cannot be specified with ``client_secret_setting_name``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret LinuxFunctionAppSlot#client_secret}
        :param client_secret_setting_name: The app setting name that contains the ``client_secret`` value used for Google Login. Cannot be specified with ``client_secret``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret_setting_name LinuxFunctionAppSlot#client_secret_setting_name}
        :param oauth_scopes: Specifies a list of OAuth 2.0 scopes that will be requested as part of Google Sign-In authentication. If not specified, "openid", "profile", and "email" are used as default scopes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#oauth_scopes LinuxFunctionAppSlot#oauth_scopes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e6759ceccebd4003bc8cd48f565ec9da1b4f53677030bb3c06f81e5ade6cf50)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument client_secret_setting_name", value=client_secret_setting_name, expected_type=type_hints["client_secret_setting_name"])
            check_type(argname="argument oauth_scopes", value=oauth_scopes, expected_type=type_hints["oauth_scopes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
        }
        if client_secret is not None:
            self._values["client_secret"] = client_secret
        if client_secret_setting_name is not None:
            self._values["client_secret_setting_name"] = client_secret_setting_name
        if oauth_scopes is not None:
            self._values["oauth_scopes"] = oauth_scopes

    @builtins.property
    def client_id(self) -> builtins.str:
        '''The OpenID Connect Client ID for the Google web application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_id LinuxFunctionAppSlot#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''The client secret associated with the Google web application.  Cannot be specified with ``client_secret_setting_name``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret LinuxFunctionAppSlot#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret_setting_name(self) -> typing.Optional[builtins.str]:
        '''The app setting name that contains the ``client_secret`` value used for Google Login. Cannot be specified with ``client_secret``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret_setting_name LinuxFunctionAppSlot#client_secret_setting_name}
        '''
        result = self._values.get("client_secret_setting_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of OAuth 2.0 scopes that will be requested as part of Google Sign-In authentication. If not specified, "openid", "profile", and "email" are used as default scopes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#oauth_scopes LinuxFunctionAppSlot#oauth_scopes}
        '''
        result = self._values.get("oauth_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotAuthSettingsGoogle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LinuxFunctionAppSlotAuthSettingsGoogleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsGoogleOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c085191d719b39b102936c421aa8b8333523b2e01818caff59ee027a04db1f34)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClientSecret")
    def reset_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecret", []))

    @jsii.member(jsii_name="resetClientSecretSettingName")
    def reset_client_secret_setting_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecretSettingName", []))

    @jsii.member(jsii_name="resetOauthScopes")
    def reset_oauth_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthScopes", []))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingNameInput")
    def client_secret_setting_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretSettingNameInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthScopesInput")
    def oauth_scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "oauthScopesInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4551b40ad750bf40203155dcaf13e40e2f37839bc18c0cddc947b4c31cac1b8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d4931a28987e5a9921b22937e90f227d84a1dc94f25863c77e234edda9141dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingName")
    def client_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecretSettingName"))

    @client_secret_setting_name.setter
    def client_secret_setting_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec2150f49d103e6da40bf3e2458418c05278913c159a566d47a3f4d871f80e63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecretSettingName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthScopes")
    def oauth_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "oauthScopes"))

    @oauth_scopes.setter
    def oauth_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59167e77e56018372047eea8ae3410ed8a92a4fb91b2f4d7b4928e77f4259ec5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthScopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LinuxFunctionAppSlotAuthSettingsGoogle]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotAuthSettingsGoogle], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LinuxFunctionAppSlotAuthSettingsGoogle],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__916ee439f412baecfe2bfd6ca234a3e56d8499e1a196bca76377342493a01461)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsMicrosoft",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "client_secret_setting_name": "clientSecretSettingName",
        "oauth_scopes": "oauthScopes",
    },
)
class LinuxFunctionAppSlotAuthSettingsMicrosoft:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        client_secret: typing.Optional[builtins.str] = None,
        client_secret_setting_name: typing.Optional[builtins.str] = None,
        oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param client_id: The OAuth 2.0 client ID that was created for the app used for authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_id LinuxFunctionAppSlot#client_id}
        :param client_secret: The OAuth 2.0 client secret that was created for the app used for authentication. Cannot be specified with ``client_secret_setting_name``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret LinuxFunctionAppSlot#client_secret}
        :param client_secret_setting_name: The app setting name containing the OAuth 2.0 client secret that was created for the app used for authentication. Cannot be specified with ``client_secret``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret_setting_name LinuxFunctionAppSlot#client_secret_setting_name}
        :param oauth_scopes: The list of OAuth 2.0 scopes that will be requested as part of Microsoft Account authentication. If not specified, ``wl.basic`` is used as the default scope. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#oauth_scopes LinuxFunctionAppSlot#oauth_scopes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0616760984d9ea5fe43e2f8db042da8e59eab3a45b787feda4efb68b3a7b9293)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument client_secret_setting_name", value=client_secret_setting_name, expected_type=type_hints["client_secret_setting_name"])
            check_type(argname="argument oauth_scopes", value=oauth_scopes, expected_type=type_hints["oauth_scopes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
        }
        if client_secret is not None:
            self._values["client_secret"] = client_secret
        if client_secret_setting_name is not None:
            self._values["client_secret_setting_name"] = client_secret_setting_name
        if oauth_scopes is not None:
            self._values["oauth_scopes"] = oauth_scopes

    @builtins.property
    def client_id(self) -> builtins.str:
        '''The OAuth 2.0 client ID that was created for the app used for authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_id LinuxFunctionAppSlot#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''The OAuth 2.0 client secret that was created for the app used for authentication. Cannot be specified with ``client_secret_setting_name``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret LinuxFunctionAppSlot#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret_setting_name(self) -> typing.Optional[builtins.str]:
        '''The app setting name containing the OAuth 2.0 client secret that was created for the app used for authentication. Cannot be specified with ``client_secret``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret_setting_name LinuxFunctionAppSlot#client_secret_setting_name}
        '''
        result = self._values.get("client_secret_setting_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of OAuth 2.0 scopes that will be requested as part of Microsoft Account authentication. If not specified, ``wl.basic`` is used as the default scope.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#oauth_scopes LinuxFunctionAppSlot#oauth_scopes}
        '''
        result = self._values.get("oauth_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotAuthSettingsMicrosoft(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LinuxFunctionAppSlotAuthSettingsMicrosoftOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsMicrosoftOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91b088aaa7d52cb7c9866959b035d57d0b3771e6d4a95f31c75c34b810f504e0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClientSecret")
    def reset_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecret", []))

    @jsii.member(jsii_name="resetClientSecretSettingName")
    def reset_client_secret_setting_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecretSettingName", []))

    @jsii.member(jsii_name="resetOauthScopes")
    def reset_oauth_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOauthScopes", []))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingNameInput")
    def client_secret_setting_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretSettingNameInput"))

    @builtins.property
    @jsii.member(jsii_name="oauthScopesInput")
    def oauth_scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "oauthScopesInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__978f4408addf7ae2bd3d10d3e6745d8781e3c270d61a7a175153ff450c52287b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25c849a5dd1a56380c13b0313e049d4c20bec74bafbb72b853bae5a03eba19cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingName")
    def client_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecretSettingName"))

    @client_secret_setting_name.setter
    def client_secret_setting_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3a9b10930336664c5d23a54c9fc13d0f36a5d35d838a589f04ec078aafa5f0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecretSettingName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthScopes")
    def oauth_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "oauthScopes"))

    @oauth_scopes.setter
    def oauth_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93c88363f9870e3b6d31705047e57c1765a4e0b876488be787af5cfb6517604c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthScopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LinuxFunctionAppSlotAuthSettingsMicrosoft]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotAuthSettingsMicrosoft], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LinuxFunctionAppSlotAuthSettingsMicrosoft],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77751aff532d4497f46204f9bb8191a273c1e12b2dc5ae478766d5396626fcc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LinuxFunctionAppSlotAuthSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5de5ab83079e1618f2eb8b0fc27adf744215ce0d10734e57ecef5d212eff922e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putActiveDirectory")
    def put_active_directory(
        self,
        *,
        client_id: builtins.str,
        allowed_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
        client_secret: typing.Optional[builtins.str] = None,
        client_secret_setting_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: The ID of the Client to use to authenticate with Azure Active Directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_id LinuxFunctionAppSlot#client_id}
        :param allowed_audiences: Specifies a list of Allowed audience values to consider when validating JWTs issued by Azure Active Directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#allowed_audiences LinuxFunctionAppSlot#allowed_audiences}
        :param client_secret: The Client Secret for the Client ID. Cannot be used with ``client_secret_setting_name``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret LinuxFunctionAppSlot#client_secret}
        :param client_secret_setting_name: The App Setting name that contains the client secret of the Client. Cannot be used with ``client_secret``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret_setting_name LinuxFunctionAppSlot#client_secret_setting_name}
        '''
        value = LinuxFunctionAppSlotAuthSettingsActiveDirectory(
            client_id=client_id,
            allowed_audiences=allowed_audiences,
            client_secret=client_secret,
            client_secret_setting_name=client_secret_setting_name,
        )

        return typing.cast(None, jsii.invoke(self, "putActiveDirectory", [value]))

    @jsii.member(jsii_name="putFacebook")
    def put_facebook(
        self,
        *,
        app_id: builtins.str,
        app_secret: typing.Optional[builtins.str] = None,
        app_secret_setting_name: typing.Optional[builtins.str] = None,
        oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param app_id: The App ID of the Facebook app used for login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#app_id LinuxFunctionAppSlot#app_id}
        :param app_secret: The App Secret of the Facebook app used for Facebook Login. Cannot be specified with ``app_secret_setting_name``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#app_secret LinuxFunctionAppSlot#app_secret}
        :param app_secret_setting_name: The app setting name that contains the ``app_secret`` value used for Facebook Login. Cannot be specified with ``app_secret``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#app_secret_setting_name LinuxFunctionAppSlot#app_secret_setting_name}
        :param oauth_scopes: Specifies a list of OAuth 2.0 scopes to be requested as part of Facebook Login authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#oauth_scopes LinuxFunctionAppSlot#oauth_scopes}
        '''
        value = LinuxFunctionAppSlotAuthSettingsFacebook(
            app_id=app_id,
            app_secret=app_secret,
            app_secret_setting_name=app_secret_setting_name,
            oauth_scopes=oauth_scopes,
        )

        return typing.cast(None, jsii.invoke(self, "putFacebook", [value]))

    @jsii.member(jsii_name="putGithub")
    def put_github(
        self,
        *,
        client_id: builtins.str,
        client_secret: typing.Optional[builtins.str] = None,
        client_secret_setting_name: typing.Optional[builtins.str] = None,
        oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param client_id: The ID of the GitHub app used for login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_id LinuxFunctionAppSlot#client_id}
        :param client_secret: The Client Secret of the GitHub app used for GitHub Login. Cannot be specified with ``client_secret_setting_name``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret LinuxFunctionAppSlot#client_secret}
        :param client_secret_setting_name: The app setting name that contains the ``client_secret`` value used for GitHub Login. Cannot be specified with ``client_secret``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret_setting_name LinuxFunctionAppSlot#client_secret_setting_name}
        :param oauth_scopes: Specifies a list of OAuth 2.0 scopes that will be requested as part of GitHub Login authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#oauth_scopes LinuxFunctionAppSlot#oauth_scopes}
        '''
        value = LinuxFunctionAppSlotAuthSettingsGithub(
            client_id=client_id,
            client_secret=client_secret,
            client_secret_setting_name=client_secret_setting_name,
            oauth_scopes=oauth_scopes,
        )

        return typing.cast(None, jsii.invoke(self, "putGithub", [value]))

    @jsii.member(jsii_name="putGoogle")
    def put_google(
        self,
        *,
        client_id: builtins.str,
        client_secret: typing.Optional[builtins.str] = None,
        client_secret_setting_name: typing.Optional[builtins.str] = None,
        oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param client_id: The OpenID Connect Client ID for the Google web application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_id LinuxFunctionAppSlot#client_id}
        :param client_secret: The client secret associated with the Google web application. Cannot be specified with ``client_secret_setting_name``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret LinuxFunctionAppSlot#client_secret}
        :param client_secret_setting_name: The app setting name that contains the ``client_secret`` value used for Google Login. Cannot be specified with ``client_secret``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret_setting_name LinuxFunctionAppSlot#client_secret_setting_name}
        :param oauth_scopes: Specifies a list of OAuth 2.0 scopes that will be requested as part of Google Sign-In authentication. If not specified, "openid", "profile", and "email" are used as default scopes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#oauth_scopes LinuxFunctionAppSlot#oauth_scopes}
        '''
        value = LinuxFunctionAppSlotAuthSettingsGoogle(
            client_id=client_id,
            client_secret=client_secret,
            client_secret_setting_name=client_secret_setting_name,
            oauth_scopes=oauth_scopes,
        )

        return typing.cast(None, jsii.invoke(self, "putGoogle", [value]))

    @jsii.member(jsii_name="putMicrosoft")
    def put_microsoft(
        self,
        *,
        client_id: builtins.str,
        client_secret: typing.Optional[builtins.str] = None,
        client_secret_setting_name: typing.Optional[builtins.str] = None,
        oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param client_id: The OAuth 2.0 client ID that was created for the app used for authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_id LinuxFunctionAppSlot#client_id}
        :param client_secret: The OAuth 2.0 client secret that was created for the app used for authentication. Cannot be specified with ``client_secret_setting_name``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret LinuxFunctionAppSlot#client_secret}
        :param client_secret_setting_name: The app setting name containing the OAuth 2.0 client secret that was created for the app used for authentication. Cannot be specified with ``client_secret``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret_setting_name LinuxFunctionAppSlot#client_secret_setting_name}
        :param oauth_scopes: The list of OAuth 2.0 scopes that will be requested as part of Microsoft Account authentication. If not specified, ``wl.basic`` is used as the default scope. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#oauth_scopes LinuxFunctionAppSlot#oauth_scopes}
        '''
        value = LinuxFunctionAppSlotAuthSettingsMicrosoft(
            client_id=client_id,
            client_secret=client_secret,
            client_secret_setting_name=client_secret_setting_name,
            oauth_scopes=oauth_scopes,
        )

        return typing.cast(None, jsii.invoke(self, "putMicrosoft", [value]))

    @jsii.member(jsii_name="putTwitter")
    def put_twitter(
        self,
        *,
        consumer_key: builtins.str,
        consumer_secret: typing.Optional[builtins.str] = None,
        consumer_secret_setting_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param consumer_key: The OAuth 1.0a consumer key of the Twitter application used for sign-in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#consumer_key LinuxFunctionAppSlot#consumer_key}
        :param consumer_secret: The OAuth 1.0a consumer secret of the Twitter application used for sign-in. Cannot be specified with ``consumer_secret_setting_name``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#consumer_secret LinuxFunctionAppSlot#consumer_secret}
        :param consumer_secret_setting_name: The app setting name that contains the OAuth 1.0a consumer secret of the Twitter application used for sign-in. Cannot be specified with ``consumer_secret``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#consumer_secret_setting_name LinuxFunctionAppSlot#consumer_secret_setting_name}
        '''
        value = LinuxFunctionAppSlotAuthSettingsTwitter(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            consumer_secret_setting_name=consumer_secret_setting_name,
        )

        return typing.cast(None, jsii.invoke(self, "putTwitter", [value]))

    @jsii.member(jsii_name="resetActiveDirectory")
    def reset_active_directory(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActiveDirectory", []))

    @jsii.member(jsii_name="resetAdditionalLoginParameters")
    def reset_additional_login_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalLoginParameters", []))

    @jsii.member(jsii_name="resetAllowedExternalRedirectUrls")
    def reset_allowed_external_redirect_urls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedExternalRedirectUrls", []))

    @jsii.member(jsii_name="resetDefaultProvider")
    def reset_default_provider(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultProvider", []))

    @jsii.member(jsii_name="resetFacebook")
    def reset_facebook(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFacebook", []))

    @jsii.member(jsii_name="resetGithub")
    def reset_github(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGithub", []))

    @jsii.member(jsii_name="resetGoogle")
    def reset_google(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGoogle", []))

    @jsii.member(jsii_name="resetIssuer")
    def reset_issuer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIssuer", []))

    @jsii.member(jsii_name="resetMicrosoft")
    def reset_microsoft(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMicrosoft", []))

    @jsii.member(jsii_name="resetRuntimeVersion")
    def reset_runtime_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntimeVersion", []))

    @jsii.member(jsii_name="resetTokenRefreshExtensionHours")
    def reset_token_refresh_extension_hours(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTokenRefreshExtensionHours", []))

    @jsii.member(jsii_name="resetTokenStoreEnabled")
    def reset_token_store_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTokenStoreEnabled", []))

    @jsii.member(jsii_name="resetTwitter")
    def reset_twitter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTwitter", []))

    @jsii.member(jsii_name="resetUnauthenticatedClientAction")
    def reset_unauthenticated_client_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnauthenticatedClientAction", []))

    @builtins.property
    @jsii.member(jsii_name="activeDirectory")
    def active_directory(
        self,
    ) -> LinuxFunctionAppSlotAuthSettingsActiveDirectoryOutputReference:
        return typing.cast(LinuxFunctionAppSlotAuthSettingsActiveDirectoryOutputReference, jsii.get(self, "activeDirectory"))

    @builtins.property
    @jsii.member(jsii_name="facebook")
    def facebook(self) -> LinuxFunctionAppSlotAuthSettingsFacebookOutputReference:
        return typing.cast(LinuxFunctionAppSlotAuthSettingsFacebookOutputReference, jsii.get(self, "facebook"))

    @builtins.property
    @jsii.member(jsii_name="github")
    def github(self) -> LinuxFunctionAppSlotAuthSettingsGithubOutputReference:
        return typing.cast(LinuxFunctionAppSlotAuthSettingsGithubOutputReference, jsii.get(self, "github"))

    @builtins.property
    @jsii.member(jsii_name="google")
    def google(self) -> LinuxFunctionAppSlotAuthSettingsGoogleOutputReference:
        return typing.cast(LinuxFunctionAppSlotAuthSettingsGoogleOutputReference, jsii.get(self, "google"))

    @builtins.property
    @jsii.member(jsii_name="microsoft")
    def microsoft(self) -> LinuxFunctionAppSlotAuthSettingsMicrosoftOutputReference:
        return typing.cast(LinuxFunctionAppSlotAuthSettingsMicrosoftOutputReference, jsii.get(self, "microsoft"))

    @builtins.property
    @jsii.member(jsii_name="twitter")
    def twitter(self) -> "LinuxFunctionAppSlotAuthSettingsTwitterOutputReference":
        return typing.cast("LinuxFunctionAppSlotAuthSettingsTwitterOutputReference", jsii.get(self, "twitter"))

    @builtins.property
    @jsii.member(jsii_name="activeDirectoryInput")
    def active_directory_input(
        self,
    ) -> typing.Optional[LinuxFunctionAppSlotAuthSettingsActiveDirectory]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotAuthSettingsActiveDirectory], jsii.get(self, "activeDirectoryInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalLoginParametersInput")
    def additional_login_parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "additionalLoginParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedExternalRedirectUrlsInput")
    def allowed_external_redirect_urls_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedExternalRedirectUrlsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultProviderInput")
    def default_provider_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="facebookInput")
    def facebook_input(
        self,
    ) -> typing.Optional[LinuxFunctionAppSlotAuthSettingsFacebook]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotAuthSettingsFacebook], jsii.get(self, "facebookInput"))

    @builtins.property
    @jsii.member(jsii_name="githubInput")
    def github_input(self) -> typing.Optional[LinuxFunctionAppSlotAuthSettingsGithub]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotAuthSettingsGithub], jsii.get(self, "githubInput"))

    @builtins.property
    @jsii.member(jsii_name="googleInput")
    def google_input(self) -> typing.Optional[LinuxFunctionAppSlotAuthSettingsGoogle]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotAuthSettingsGoogle], jsii.get(self, "googleInput"))

    @builtins.property
    @jsii.member(jsii_name="issuerInput")
    def issuer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerInput"))

    @builtins.property
    @jsii.member(jsii_name="microsoftInput")
    def microsoft_input(
        self,
    ) -> typing.Optional[LinuxFunctionAppSlotAuthSettingsMicrosoft]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotAuthSettingsMicrosoft], jsii.get(self, "microsoftInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeVersionInput")
    def runtime_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenRefreshExtensionHoursInput")
    def token_refresh_extension_hours_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tokenRefreshExtensionHoursInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenStoreEnabledInput")
    def token_store_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tokenStoreEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="twitterInput")
    def twitter_input(
        self,
    ) -> typing.Optional["LinuxFunctionAppSlotAuthSettingsTwitter"]:
        return typing.cast(typing.Optional["LinuxFunctionAppSlotAuthSettingsTwitter"], jsii.get(self, "twitterInput"))

    @builtins.property
    @jsii.member(jsii_name="unauthenticatedClientActionInput")
    def unauthenticated_client_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unauthenticatedClientActionInput"))

    @builtins.property
    @jsii.member(jsii_name="additionalLoginParameters")
    def additional_login_parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "additionalLoginParameters"))

    @additional_login_parameters.setter
    def additional_login_parameters(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fecce4709e8f10018c7c96049f7ced98e45e11e463e4cfd5b2787164bb1ef9cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalLoginParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedExternalRedirectUrls")
    def allowed_external_redirect_urls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedExternalRedirectUrls"))

    @allowed_external_redirect_urls.setter
    def allowed_external_redirect_urls(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b669cf79e46b338401b8b7f1f2926521ab39289b5b203be332421d9875f24b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedExternalRedirectUrls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultProvider")
    def default_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultProvider"))

    @default_provider.setter
    def default_provider(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abfddd83aa887d112a4898efdd4eed74c1ff82a937309cb47af7d7887e880870)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultProvider", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d95c98dce344db108dbea2a00ba539c09c529ee54161d2d02f8232b199619c30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issuer")
    def issuer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuer"))

    @issuer.setter
    def issuer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4668d702d405f80a1e3872ae7ce1d0e731dbc7bedb07202fe5484aae3c462088)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeVersion")
    def runtime_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeVersion"))

    @runtime_version.setter
    def runtime_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b21559a353643fd007bfe077fb63c737f5c2a54ccd035d5cb1c2b47ff95bde3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenRefreshExtensionHours")
    def token_refresh_extension_hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tokenRefreshExtensionHours"))

    @token_refresh_extension_hours.setter
    def token_refresh_extension_hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__720d83460b65b762445606979abc7cdea22af18912417e1f1397d3e9e05d998f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenRefreshExtensionHours", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenStoreEnabled")
    def token_store_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tokenStoreEnabled"))

    @token_store_enabled.setter
    def token_store_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b53c81ba7a15ec630429189ece6e935cd96c5d4ce506bd2de7b4ecc81388073)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenStoreEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unauthenticatedClientAction")
    def unauthenticated_client_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unauthenticatedClientAction"))

    @unauthenticated_client_action.setter
    def unauthenticated_client_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__499153c3cc46b162af385bafcf48a0a3c8aadbdbc2267b8c040acae7306dbf02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unauthenticatedClientAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LinuxFunctionAppSlotAuthSettings]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotAuthSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LinuxFunctionAppSlotAuthSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a92b226f11b8e88897930a58b714756ed2a6edbcf0798a51b3bfa2569cf79e04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsTwitter",
    jsii_struct_bases=[],
    name_mapping={
        "consumer_key": "consumerKey",
        "consumer_secret": "consumerSecret",
        "consumer_secret_setting_name": "consumerSecretSettingName",
    },
)
class LinuxFunctionAppSlotAuthSettingsTwitter:
    def __init__(
        self,
        *,
        consumer_key: builtins.str,
        consumer_secret: typing.Optional[builtins.str] = None,
        consumer_secret_setting_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param consumer_key: The OAuth 1.0a consumer key of the Twitter application used for sign-in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#consumer_key LinuxFunctionAppSlot#consumer_key}
        :param consumer_secret: The OAuth 1.0a consumer secret of the Twitter application used for sign-in. Cannot be specified with ``consumer_secret_setting_name``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#consumer_secret LinuxFunctionAppSlot#consumer_secret}
        :param consumer_secret_setting_name: The app setting name that contains the OAuth 1.0a consumer secret of the Twitter application used for sign-in. Cannot be specified with ``consumer_secret``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#consumer_secret_setting_name LinuxFunctionAppSlot#consumer_secret_setting_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__067f93dfb48d91364508d04f701128c7cc6d471272a59e4ed4859d16e0875259)
            check_type(argname="argument consumer_key", value=consumer_key, expected_type=type_hints["consumer_key"])
            check_type(argname="argument consumer_secret", value=consumer_secret, expected_type=type_hints["consumer_secret"])
            check_type(argname="argument consumer_secret_setting_name", value=consumer_secret_setting_name, expected_type=type_hints["consumer_secret_setting_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "consumer_key": consumer_key,
        }
        if consumer_secret is not None:
            self._values["consumer_secret"] = consumer_secret
        if consumer_secret_setting_name is not None:
            self._values["consumer_secret_setting_name"] = consumer_secret_setting_name

    @builtins.property
    def consumer_key(self) -> builtins.str:
        '''The OAuth 1.0a consumer key of the Twitter application used for sign-in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#consumer_key LinuxFunctionAppSlot#consumer_key}
        '''
        result = self._values.get("consumer_key")
        assert result is not None, "Required property 'consumer_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def consumer_secret(self) -> typing.Optional[builtins.str]:
        '''The OAuth 1.0a consumer secret of the Twitter application used for sign-in. Cannot be specified with ``consumer_secret_setting_name``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#consumer_secret LinuxFunctionAppSlot#consumer_secret}
        '''
        result = self._values.get("consumer_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def consumer_secret_setting_name(self) -> typing.Optional[builtins.str]:
        '''The app setting name that contains the OAuth 1.0a consumer secret of the Twitter application used for sign-in. Cannot be specified with ``consumer_secret``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#consumer_secret_setting_name LinuxFunctionAppSlot#consumer_secret_setting_name}
        '''
        result = self._values.get("consumer_secret_setting_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotAuthSettingsTwitter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LinuxFunctionAppSlotAuthSettingsTwitterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsTwitterOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f439f5104856bac8b3e5cb19c139b17cc264451fed3df19c73bcf4f243697b71)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetConsumerSecret")
    def reset_consumer_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsumerSecret", []))

    @jsii.member(jsii_name="resetConsumerSecretSettingName")
    def reset_consumer_secret_setting_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConsumerSecretSettingName", []))

    @builtins.property
    @jsii.member(jsii_name="consumerKeyInput")
    def consumer_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumerKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerSecretInput")
    def consumer_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumerSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerSecretSettingNameInput")
    def consumer_secret_setting_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumerSecretSettingNameInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerKey")
    def consumer_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerKey"))

    @consumer_key.setter
    def consumer_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__503fc36b3105008deead531e8b43459e845c71c5c877af7af833bd527087a3ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="consumerSecret")
    def consumer_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerSecret"))

    @consumer_secret.setter
    def consumer_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c33edb984b922090384d490df108277c3137952d45b7c4131dd37545d143d12b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="consumerSecretSettingName")
    def consumer_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerSecretSettingName"))

    @consumer_secret_setting_name.setter
    def consumer_secret_setting_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6d70aa109bc40dbb83e61b05bcc1c5f91739c5a85aba84aaa6494bb29644c48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerSecretSettingName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LinuxFunctionAppSlotAuthSettingsTwitter]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotAuthSettingsTwitter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LinuxFunctionAppSlotAuthSettingsTwitter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95cb95e1e5300ed71c94e89ee2b814949027039a60f930b120349fb04847b6aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsV2",
    jsii_struct_bases=[],
    name_mapping={
        "login": "login",
        "active_directory_v2": "activeDirectoryV2",
        "apple_v2": "appleV2",
        "auth_enabled": "authEnabled",
        "azure_static_web_app_v2": "azureStaticWebAppV2",
        "config_file_path": "configFilePath",
        "custom_oidc_v2": "customOidcV2",
        "default_provider": "defaultProvider",
        "excluded_paths": "excludedPaths",
        "facebook_v2": "facebookV2",
        "forward_proxy_convention": "forwardProxyConvention",
        "forward_proxy_custom_host_header_name": "forwardProxyCustomHostHeaderName",
        "forward_proxy_custom_scheme_header_name": "forwardProxyCustomSchemeHeaderName",
        "github_v2": "githubV2",
        "google_v2": "googleV2",
        "http_route_api_prefix": "httpRouteApiPrefix",
        "microsoft_v2": "microsoftV2",
        "require_authentication": "requireAuthentication",
        "require_https": "requireHttps",
        "runtime_version": "runtimeVersion",
        "twitter_v2": "twitterV2",
        "unauthenticated_action": "unauthenticatedAction",
    },
)
class LinuxFunctionAppSlotAuthSettingsV2:
    def __init__(
        self,
        *,
        login: typing.Union["LinuxFunctionAppSlotAuthSettingsV2Login", typing.Dict[builtins.str, typing.Any]],
        active_directory_v2: typing.Optional[typing.Union["LinuxFunctionAppSlotAuthSettingsV2ActiveDirectoryV2", typing.Dict[builtins.str, typing.Any]]] = None,
        apple_v2: typing.Optional[typing.Union["LinuxFunctionAppSlotAuthSettingsV2AppleV2", typing.Dict[builtins.str, typing.Any]]] = None,
        auth_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        azure_static_web_app_v2: typing.Optional[typing.Union["LinuxFunctionAppSlotAuthSettingsV2AzureStaticWebAppV2", typing.Dict[builtins.str, typing.Any]]] = None,
        config_file_path: typing.Optional[builtins.str] = None,
        custom_oidc_v2: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LinuxFunctionAppSlotAuthSettingsV2CustomOidcV2", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_provider: typing.Optional[builtins.str] = None,
        excluded_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        facebook_v2: typing.Optional[typing.Union["LinuxFunctionAppSlotAuthSettingsV2FacebookV2", typing.Dict[builtins.str, typing.Any]]] = None,
        forward_proxy_convention: typing.Optional[builtins.str] = None,
        forward_proxy_custom_host_header_name: typing.Optional[builtins.str] = None,
        forward_proxy_custom_scheme_header_name: typing.Optional[builtins.str] = None,
        github_v2: typing.Optional[typing.Union["LinuxFunctionAppSlotAuthSettingsV2GithubV2", typing.Dict[builtins.str, typing.Any]]] = None,
        google_v2: typing.Optional[typing.Union["LinuxFunctionAppSlotAuthSettingsV2GoogleV2", typing.Dict[builtins.str, typing.Any]]] = None,
        http_route_api_prefix: typing.Optional[builtins.str] = None,
        microsoft_v2: typing.Optional[typing.Union["LinuxFunctionAppSlotAuthSettingsV2MicrosoftV2", typing.Dict[builtins.str, typing.Any]]] = None,
        require_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_https: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        runtime_version: typing.Optional[builtins.str] = None,
        twitter_v2: typing.Optional[typing.Union["LinuxFunctionAppSlotAuthSettingsV2TwitterV2", typing.Dict[builtins.str, typing.Any]]] = None,
        unauthenticated_action: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param login: login block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#login LinuxFunctionAppSlot#login}
        :param active_directory_v2: active_directory_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#active_directory_v2 LinuxFunctionAppSlot#active_directory_v2}
        :param apple_v2: apple_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#apple_v2 LinuxFunctionAppSlot#apple_v2}
        :param auth_enabled: Should the AuthV2 Settings be enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#auth_enabled LinuxFunctionAppSlot#auth_enabled}
        :param azure_static_web_app_v2: azure_static_web_app_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#azure_static_web_app_v2 LinuxFunctionAppSlot#azure_static_web_app_v2}
        :param config_file_path: The path to the App Auth settings. **Note:** Relative Paths are evaluated from the Site Root directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#config_file_path LinuxFunctionAppSlot#config_file_path}
        :param custom_oidc_v2: custom_oidc_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#custom_oidc_v2 LinuxFunctionAppSlot#custom_oidc_v2}
        :param default_provider: The Default Authentication Provider to use when the ``unauthenticated_action`` is set to ``RedirectToLoginPage``. Possible values include: ``apple``, ``azureactivedirectory``, ``facebook``, ``github``, ``google``, ``twitter`` and the ``name`` of your ``custom_oidc_v2`` provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#default_provider LinuxFunctionAppSlot#default_provider}
        :param excluded_paths: The paths which should be excluded from the ``unauthenticated_action`` when it is set to ``RedirectToLoginPage``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#excluded_paths LinuxFunctionAppSlot#excluded_paths}
        :param facebook_v2: facebook_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#facebook_v2 LinuxFunctionAppSlot#facebook_v2}
        :param forward_proxy_convention: The convention used to determine the url of the request made. Possible values include ``ForwardProxyConventionNoProxy``, ``ForwardProxyConventionStandard``, ``ForwardProxyConventionCustom``. Defaults to ``ForwardProxyConventionNoProxy`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#forward_proxy_convention LinuxFunctionAppSlot#forward_proxy_convention}
        :param forward_proxy_custom_host_header_name: The name of the header containing the host of the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#forward_proxy_custom_host_header_name LinuxFunctionAppSlot#forward_proxy_custom_host_header_name}
        :param forward_proxy_custom_scheme_header_name: The name of the header containing the scheme of the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#forward_proxy_custom_scheme_header_name LinuxFunctionAppSlot#forward_proxy_custom_scheme_header_name}
        :param github_v2: github_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#github_v2 LinuxFunctionAppSlot#github_v2}
        :param google_v2: google_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#google_v2 LinuxFunctionAppSlot#google_v2}
        :param http_route_api_prefix: The prefix that should precede all the authentication and authorisation paths. Defaults to ``/.auth``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#http_route_api_prefix LinuxFunctionAppSlot#http_route_api_prefix}
        :param microsoft_v2: microsoft_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#microsoft_v2 LinuxFunctionAppSlot#microsoft_v2}
        :param require_authentication: Should the authentication flow be used for all requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#require_authentication LinuxFunctionAppSlot#require_authentication}
        :param require_https: Should HTTPS be required on connections? Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#require_https LinuxFunctionAppSlot#require_https}
        :param runtime_version: The Runtime Version of the Authentication and Authorisation feature of this App. Defaults to ``~1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#runtime_version LinuxFunctionAppSlot#runtime_version}
        :param twitter_v2: twitter_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#twitter_v2 LinuxFunctionAppSlot#twitter_v2}
        :param unauthenticated_action: The action to take for requests made without authentication. Possible values include ``RedirectToLoginPage``, ``AllowAnonymous``, ``Return401``, and ``Return403``. Defaults to ``RedirectToLoginPage``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#unauthenticated_action LinuxFunctionAppSlot#unauthenticated_action}
        '''
        if isinstance(login, dict):
            login = LinuxFunctionAppSlotAuthSettingsV2Login(**login)
        if isinstance(active_directory_v2, dict):
            active_directory_v2 = LinuxFunctionAppSlotAuthSettingsV2ActiveDirectoryV2(**active_directory_v2)
        if isinstance(apple_v2, dict):
            apple_v2 = LinuxFunctionAppSlotAuthSettingsV2AppleV2(**apple_v2)
        if isinstance(azure_static_web_app_v2, dict):
            azure_static_web_app_v2 = LinuxFunctionAppSlotAuthSettingsV2AzureStaticWebAppV2(**azure_static_web_app_v2)
        if isinstance(facebook_v2, dict):
            facebook_v2 = LinuxFunctionAppSlotAuthSettingsV2FacebookV2(**facebook_v2)
        if isinstance(github_v2, dict):
            github_v2 = LinuxFunctionAppSlotAuthSettingsV2GithubV2(**github_v2)
        if isinstance(google_v2, dict):
            google_v2 = LinuxFunctionAppSlotAuthSettingsV2GoogleV2(**google_v2)
        if isinstance(microsoft_v2, dict):
            microsoft_v2 = LinuxFunctionAppSlotAuthSettingsV2MicrosoftV2(**microsoft_v2)
        if isinstance(twitter_v2, dict):
            twitter_v2 = LinuxFunctionAppSlotAuthSettingsV2TwitterV2(**twitter_v2)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__450146a80d3fe33518a3cd30c442e10c1b0c483d11235ecef526fb1f169641bb)
            check_type(argname="argument login", value=login, expected_type=type_hints["login"])
            check_type(argname="argument active_directory_v2", value=active_directory_v2, expected_type=type_hints["active_directory_v2"])
            check_type(argname="argument apple_v2", value=apple_v2, expected_type=type_hints["apple_v2"])
            check_type(argname="argument auth_enabled", value=auth_enabled, expected_type=type_hints["auth_enabled"])
            check_type(argname="argument azure_static_web_app_v2", value=azure_static_web_app_v2, expected_type=type_hints["azure_static_web_app_v2"])
            check_type(argname="argument config_file_path", value=config_file_path, expected_type=type_hints["config_file_path"])
            check_type(argname="argument custom_oidc_v2", value=custom_oidc_v2, expected_type=type_hints["custom_oidc_v2"])
            check_type(argname="argument default_provider", value=default_provider, expected_type=type_hints["default_provider"])
            check_type(argname="argument excluded_paths", value=excluded_paths, expected_type=type_hints["excluded_paths"])
            check_type(argname="argument facebook_v2", value=facebook_v2, expected_type=type_hints["facebook_v2"])
            check_type(argname="argument forward_proxy_convention", value=forward_proxy_convention, expected_type=type_hints["forward_proxy_convention"])
            check_type(argname="argument forward_proxy_custom_host_header_name", value=forward_proxy_custom_host_header_name, expected_type=type_hints["forward_proxy_custom_host_header_name"])
            check_type(argname="argument forward_proxy_custom_scheme_header_name", value=forward_proxy_custom_scheme_header_name, expected_type=type_hints["forward_proxy_custom_scheme_header_name"])
            check_type(argname="argument github_v2", value=github_v2, expected_type=type_hints["github_v2"])
            check_type(argname="argument google_v2", value=google_v2, expected_type=type_hints["google_v2"])
            check_type(argname="argument http_route_api_prefix", value=http_route_api_prefix, expected_type=type_hints["http_route_api_prefix"])
            check_type(argname="argument microsoft_v2", value=microsoft_v2, expected_type=type_hints["microsoft_v2"])
            check_type(argname="argument require_authentication", value=require_authentication, expected_type=type_hints["require_authentication"])
            check_type(argname="argument require_https", value=require_https, expected_type=type_hints["require_https"])
            check_type(argname="argument runtime_version", value=runtime_version, expected_type=type_hints["runtime_version"])
            check_type(argname="argument twitter_v2", value=twitter_v2, expected_type=type_hints["twitter_v2"])
            check_type(argname="argument unauthenticated_action", value=unauthenticated_action, expected_type=type_hints["unauthenticated_action"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "login": login,
        }
        if active_directory_v2 is not None:
            self._values["active_directory_v2"] = active_directory_v2
        if apple_v2 is not None:
            self._values["apple_v2"] = apple_v2
        if auth_enabled is not None:
            self._values["auth_enabled"] = auth_enabled
        if azure_static_web_app_v2 is not None:
            self._values["azure_static_web_app_v2"] = azure_static_web_app_v2
        if config_file_path is not None:
            self._values["config_file_path"] = config_file_path
        if custom_oidc_v2 is not None:
            self._values["custom_oidc_v2"] = custom_oidc_v2
        if default_provider is not None:
            self._values["default_provider"] = default_provider
        if excluded_paths is not None:
            self._values["excluded_paths"] = excluded_paths
        if facebook_v2 is not None:
            self._values["facebook_v2"] = facebook_v2
        if forward_proxy_convention is not None:
            self._values["forward_proxy_convention"] = forward_proxy_convention
        if forward_proxy_custom_host_header_name is not None:
            self._values["forward_proxy_custom_host_header_name"] = forward_proxy_custom_host_header_name
        if forward_proxy_custom_scheme_header_name is not None:
            self._values["forward_proxy_custom_scheme_header_name"] = forward_proxy_custom_scheme_header_name
        if github_v2 is not None:
            self._values["github_v2"] = github_v2
        if google_v2 is not None:
            self._values["google_v2"] = google_v2
        if http_route_api_prefix is not None:
            self._values["http_route_api_prefix"] = http_route_api_prefix
        if microsoft_v2 is not None:
            self._values["microsoft_v2"] = microsoft_v2
        if require_authentication is not None:
            self._values["require_authentication"] = require_authentication
        if require_https is not None:
            self._values["require_https"] = require_https
        if runtime_version is not None:
            self._values["runtime_version"] = runtime_version
        if twitter_v2 is not None:
            self._values["twitter_v2"] = twitter_v2
        if unauthenticated_action is not None:
            self._values["unauthenticated_action"] = unauthenticated_action

    @builtins.property
    def login(self) -> "LinuxFunctionAppSlotAuthSettingsV2Login":
        '''login block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#login LinuxFunctionAppSlot#login}
        '''
        result = self._values.get("login")
        assert result is not None, "Required property 'login' is missing"
        return typing.cast("LinuxFunctionAppSlotAuthSettingsV2Login", result)

    @builtins.property
    def active_directory_v2(
        self,
    ) -> typing.Optional["LinuxFunctionAppSlotAuthSettingsV2ActiveDirectoryV2"]:
        '''active_directory_v2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#active_directory_v2 LinuxFunctionAppSlot#active_directory_v2}
        '''
        result = self._values.get("active_directory_v2")
        return typing.cast(typing.Optional["LinuxFunctionAppSlotAuthSettingsV2ActiveDirectoryV2"], result)

    @builtins.property
    def apple_v2(self) -> typing.Optional["LinuxFunctionAppSlotAuthSettingsV2AppleV2"]:
        '''apple_v2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#apple_v2 LinuxFunctionAppSlot#apple_v2}
        '''
        result = self._values.get("apple_v2")
        return typing.cast(typing.Optional["LinuxFunctionAppSlotAuthSettingsV2AppleV2"], result)

    @builtins.property
    def auth_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the AuthV2 Settings be enabled. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#auth_enabled LinuxFunctionAppSlot#auth_enabled}
        '''
        result = self._values.get("auth_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def azure_static_web_app_v2(
        self,
    ) -> typing.Optional["LinuxFunctionAppSlotAuthSettingsV2AzureStaticWebAppV2"]:
        '''azure_static_web_app_v2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#azure_static_web_app_v2 LinuxFunctionAppSlot#azure_static_web_app_v2}
        '''
        result = self._values.get("azure_static_web_app_v2")
        return typing.cast(typing.Optional["LinuxFunctionAppSlotAuthSettingsV2AzureStaticWebAppV2"], result)

    @builtins.property
    def config_file_path(self) -> typing.Optional[builtins.str]:
        '''The path to the App Auth settings. **Note:** Relative Paths are evaluated from the Site Root directory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#config_file_path LinuxFunctionAppSlot#config_file_path}
        '''
        result = self._values.get("config_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_oidc_v2(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LinuxFunctionAppSlotAuthSettingsV2CustomOidcV2"]]]:
        '''custom_oidc_v2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#custom_oidc_v2 LinuxFunctionAppSlot#custom_oidc_v2}
        '''
        result = self._values.get("custom_oidc_v2")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LinuxFunctionAppSlotAuthSettingsV2CustomOidcV2"]]], result)

    @builtins.property
    def default_provider(self) -> typing.Optional[builtins.str]:
        '''The Default Authentication Provider to use when the ``unauthenticated_action`` is set to ``RedirectToLoginPage``.

        Possible values include: ``apple``, ``azureactivedirectory``, ``facebook``, ``github``, ``google``, ``twitter`` and the ``name`` of your ``custom_oidc_v2`` provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#default_provider LinuxFunctionAppSlot#default_provider}
        '''
        result = self._values.get("default_provider")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def excluded_paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The paths which should be excluded from the ``unauthenticated_action`` when it is set to ``RedirectToLoginPage``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#excluded_paths LinuxFunctionAppSlot#excluded_paths}
        '''
        result = self._values.get("excluded_paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def facebook_v2(
        self,
    ) -> typing.Optional["LinuxFunctionAppSlotAuthSettingsV2FacebookV2"]:
        '''facebook_v2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#facebook_v2 LinuxFunctionAppSlot#facebook_v2}
        '''
        result = self._values.get("facebook_v2")
        return typing.cast(typing.Optional["LinuxFunctionAppSlotAuthSettingsV2FacebookV2"], result)

    @builtins.property
    def forward_proxy_convention(self) -> typing.Optional[builtins.str]:
        '''The convention used to determine the url of the request made.

        Possible values include ``ForwardProxyConventionNoProxy``, ``ForwardProxyConventionStandard``, ``ForwardProxyConventionCustom``. Defaults to ``ForwardProxyConventionNoProxy``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#forward_proxy_convention LinuxFunctionAppSlot#forward_proxy_convention}
        '''
        result = self._values.get("forward_proxy_convention")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def forward_proxy_custom_host_header_name(self) -> typing.Optional[builtins.str]:
        '''The name of the header containing the host of the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#forward_proxy_custom_host_header_name LinuxFunctionAppSlot#forward_proxy_custom_host_header_name}
        '''
        result = self._values.get("forward_proxy_custom_host_header_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def forward_proxy_custom_scheme_header_name(self) -> typing.Optional[builtins.str]:
        '''The name of the header containing the scheme of the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#forward_proxy_custom_scheme_header_name LinuxFunctionAppSlot#forward_proxy_custom_scheme_header_name}
        '''
        result = self._values.get("forward_proxy_custom_scheme_header_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def github_v2(
        self,
    ) -> typing.Optional["LinuxFunctionAppSlotAuthSettingsV2GithubV2"]:
        '''github_v2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#github_v2 LinuxFunctionAppSlot#github_v2}
        '''
        result = self._values.get("github_v2")
        return typing.cast(typing.Optional["LinuxFunctionAppSlotAuthSettingsV2GithubV2"], result)

    @builtins.property
    def google_v2(
        self,
    ) -> typing.Optional["LinuxFunctionAppSlotAuthSettingsV2GoogleV2"]:
        '''google_v2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#google_v2 LinuxFunctionAppSlot#google_v2}
        '''
        result = self._values.get("google_v2")
        return typing.cast(typing.Optional["LinuxFunctionAppSlotAuthSettingsV2GoogleV2"], result)

    @builtins.property
    def http_route_api_prefix(self) -> typing.Optional[builtins.str]:
        '''The prefix that should precede all the authentication and authorisation paths. Defaults to ``/.auth``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#http_route_api_prefix LinuxFunctionAppSlot#http_route_api_prefix}
        '''
        result = self._values.get("http_route_api_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def microsoft_v2(
        self,
    ) -> typing.Optional["LinuxFunctionAppSlotAuthSettingsV2MicrosoftV2"]:
        '''microsoft_v2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#microsoft_v2 LinuxFunctionAppSlot#microsoft_v2}
        '''
        result = self._values.get("microsoft_v2")
        return typing.cast(typing.Optional["LinuxFunctionAppSlotAuthSettingsV2MicrosoftV2"], result)

    @builtins.property
    def require_authentication(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the authentication flow be used for all requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#require_authentication LinuxFunctionAppSlot#require_authentication}
        '''
        result = self._values.get("require_authentication")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def require_https(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should HTTPS be required on connections? Defaults to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#require_https LinuxFunctionAppSlot#require_https}
        '''
        result = self._values.get("require_https")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def runtime_version(self) -> typing.Optional[builtins.str]:
        '''The Runtime Version of the Authentication and Authorisation feature of this App. Defaults to ``~1``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#runtime_version LinuxFunctionAppSlot#runtime_version}
        '''
        result = self._values.get("runtime_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def twitter_v2(
        self,
    ) -> typing.Optional["LinuxFunctionAppSlotAuthSettingsV2TwitterV2"]:
        '''twitter_v2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#twitter_v2 LinuxFunctionAppSlot#twitter_v2}
        '''
        result = self._values.get("twitter_v2")
        return typing.cast(typing.Optional["LinuxFunctionAppSlotAuthSettingsV2TwitterV2"], result)

    @builtins.property
    def unauthenticated_action(self) -> typing.Optional[builtins.str]:
        '''The action to take for requests made without authentication.

        Possible values include ``RedirectToLoginPage``, ``AllowAnonymous``, ``Return401``, and ``Return403``. Defaults to ``RedirectToLoginPage``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#unauthenticated_action LinuxFunctionAppSlot#unauthenticated_action}
        '''
        result = self._values.get("unauthenticated_action")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotAuthSettingsV2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsV2ActiveDirectoryV2",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "tenant_auth_endpoint": "tenantAuthEndpoint",
        "allowed_applications": "allowedApplications",
        "allowed_audiences": "allowedAudiences",
        "allowed_groups": "allowedGroups",
        "allowed_identities": "allowedIdentities",
        "client_secret_certificate_thumbprint": "clientSecretCertificateThumbprint",
        "client_secret_setting_name": "clientSecretSettingName",
        "jwt_allowed_client_applications": "jwtAllowedClientApplications",
        "jwt_allowed_groups": "jwtAllowedGroups",
        "login_parameters": "loginParameters",
        "www_authentication_disabled": "wwwAuthenticationDisabled",
    },
)
class LinuxFunctionAppSlotAuthSettingsV2ActiveDirectoryV2:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        tenant_auth_endpoint: builtins.str,
        allowed_applications: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_identities: typing.Optional[typing.Sequence[builtins.str]] = None,
        client_secret_certificate_thumbprint: typing.Optional[builtins.str] = None,
        client_secret_setting_name: typing.Optional[builtins.str] = None,
        jwt_allowed_client_applications: typing.Optional[typing.Sequence[builtins.str]] = None,
        jwt_allowed_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        login_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        www_authentication_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param client_id: The ID of the Client to use to authenticate with Azure Active Directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_id LinuxFunctionAppSlot#client_id}
        :param tenant_auth_endpoint: The Azure Tenant Endpoint for the Authenticating Tenant. e.g. ``https://login.microsoftonline.com/v2.0/{tenant-guid}/``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#tenant_auth_endpoint LinuxFunctionAppSlot#tenant_auth_endpoint}
        :param allowed_applications: The list of allowed Applications for the Default Authorisation Policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#allowed_applications LinuxFunctionAppSlot#allowed_applications}
        :param allowed_audiences: Specifies a list of Allowed audience values to consider when validating JWTs issued by Azure Active Directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#allowed_audiences LinuxFunctionAppSlot#allowed_audiences}
        :param allowed_groups: The list of allowed Group Names for the Default Authorisation Policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#allowed_groups LinuxFunctionAppSlot#allowed_groups}
        :param allowed_identities: The list of allowed Identities for the Default Authorisation Policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#allowed_identities LinuxFunctionAppSlot#allowed_identities}
        :param client_secret_certificate_thumbprint: The thumbprint of the certificate used for signing purposes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret_certificate_thumbprint LinuxFunctionAppSlot#client_secret_certificate_thumbprint}
        :param client_secret_setting_name: The App Setting name that contains the client secret of the Client. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret_setting_name LinuxFunctionAppSlot#client_secret_setting_name}
        :param jwt_allowed_client_applications: A list of Allowed Client Applications in the JWT Claim. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#jwt_allowed_client_applications LinuxFunctionAppSlot#jwt_allowed_client_applications}
        :param jwt_allowed_groups: A list of Allowed Groups in the JWT Claim. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#jwt_allowed_groups LinuxFunctionAppSlot#jwt_allowed_groups}
        :param login_parameters: A map of key-value pairs to send to the Authorisation Endpoint when a user logs in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#login_parameters LinuxFunctionAppSlot#login_parameters}
        :param www_authentication_disabled: Should the www-authenticate provider should be omitted from the request? Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#www_authentication_disabled LinuxFunctionAppSlot#www_authentication_disabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__720872c2e7f91103d4caa489d4966adfd8621efecf11d1f53117da1b9a2d430a)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument tenant_auth_endpoint", value=tenant_auth_endpoint, expected_type=type_hints["tenant_auth_endpoint"])
            check_type(argname="argument allowed_applications", value=allowed_applications, expected_type=type_hints["allowed_applications"])
            check_type(argname="argument allowed_audiences", value=allowed_audiences, expected_type=type_hints["allowed_audiences"])
            check_type(argname="argument allowed_groups", value=allowed_groups, expected_type=type_hints["allowed_groups"])
            check_type(argname="argument allowed_identities", value=allowed_identities, expected_type=type_hints["allowed_identities"])
            check_type(argname="argument client_secret_certificate_thumbprint", value=client_secret_certificate_thumbprint, expected_type=type_hints["client_secret_certificate_thumbprint"])
            check_type(argname="argument client_secret_setting_name", value=client_secret_setting_name, expected_type=type_hints["client_secret_setting_name"])
            check_type(argname="argument jwt_allowed_client_applications", value=jwt_allowed_client_applications, expected_type=type_hints["jwt_allowed_client_applications"])
            check_type(argname="argument jwt_allowed_groups", value=jwt_allowed_groups, expected_type=type_hints["jwt_allowed_groups"])
            check_type(argname="argument login_parameters", value=login_parameters, expected_type=type_hints["login_parameters"])
            check_type(argname="argument www_authentication_disabled", value=www_authentication_disabled, expected_type=type_hints["www_authentication_disabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "tenant_auth_endpoint": tenant_auth_endpoint,
        }
        if allowed_applications is not None:
            self._values["allowed_applications"] = allowed_applications
        if allowed_audiences is not None:
            self._values["allowed_audiences"] = allowed_audiences
        if allowed_groups is not None:
            self._values["allowed_groups"] = allowed_groups
        if allowed_identities is not None:
            self._values["allowed_identities"] = allowed_identities
        if client_secret_certificate_thumbprint is not None:
            self._values["client_secret_certificate_thumbprint"] = client_secret_certificate_thumbprint
        if client_secret_setting_name is not None:
            self._values["client_secret_setting_name"] = client_secret_setting_name
        if jwt_allowed_client_applications is not None:
            self._values["jwt_allowed_client_applications"] = jwt_allowed_client_applications
        if jwt_allowed_groups is not None:
            self._values["jwt_allowed_groups"] = jwt_allowed_groups
        if login_parameters is not None:
            self._values["login_parameters"] = login_parameters
        if www_authentication_disabled is not None:
            self._values["www_authentication_disabled"] = www_authentication_disabled

    @builtins.property
    def client_id(self) -> builtins.str:
        '''The ID of the Client to use to authenticate with Azure Active Directory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_id LinuxFunctionAppSlot#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tenant_auth_endpoint(self) -> builtins.str:
        '''The Azure Tenant Endpoint for the Authenticating Tenant. e.g. ``https://login.microsoftonline.com/v2.0/{tenant-guid}/``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#tenant_auth_endpoint LinuxFunctionAppSlot#tenant_auth_endpoint}
        '''
        result = self._values.get("tenant_auth_endpoint")
        assert result is not None, "Required property 'tenant_auth_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_applications(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of allowed Applications for the Default Authorisation Policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#allowed_applications LinuxFunctionAppSlot#allowed_applications}
        '''
        result = self._values.get("allowed_applications")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allowed_audiences(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of Allowed audience values to consider when validating JWTs issued by Azure Active Directory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#allowed_audiences LinuxFunctionAppSlot#allowed_audiences}
        '''
        result = self._values.get("allowed_audiences")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allowed_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of allowed Group Names for the Default Authorisation Policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#allowed_groups LinuxFunctionAppSlot#allowed_groups}
        '''
        result = self._values.get("allowed_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allowed_identities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of allowed Identities for the Default Authorisation Policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#allowed_identities LinuxFunctionAppSlot#allowed_identities}
        '''
        result = self._values.get("allowed_identities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def client_secret_certificate_thumbprint(self) -> typing.Optional[builtins.str]:
        '''The thumbprint of the certificate used for signing purposes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret_certificate_thumbprint LinuxFunctionAppSlot#client_secret_certificate_thumbprint}
        '''
        result = self._values.get("client_secret_certificate_thumbprint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret_setting_name(self) -> typing.Optional[builtins.str]:
        '''The App Setting name that contains the client secret of the Client.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret_setting_name LinuxFunctionAppSlot#client_secret_setting_name}
        '''
        result = self._values.get("client_secret_setting_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jwt_allowed_client_applications(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Allowed Client Applications in the JWT Claim.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#jwt_allowed_client_applications LinuxFunctionAppSlot#jwt_allowed_client_applications}
        '''
        result = self._values.get("jwt_allowed_client_applications")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def jwt_allowed_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Allowed Groups in the JWT Claim.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#jwt_allowed_groups LinuxFunctionAppSlot#jwt_allowed_groups}
        '''
        result = self._values.get("jwt_allowed_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def login_parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of key-value pairs to send to the Authorisation Endpoint when a user logs in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#login_parameters LinuxFunctionAppSlot#login_parameters}
        '''
        result = self._values.get("login_parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def www_authentication_disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the www-authenticate provider should be omitted from the request? Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#www_authentication_disabled LinuxFunctionAppSlot#www_authentication_disabled}
        '''
        result = self._values.get("www_authentication_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotAuthSettingsV2ActiveDirectoryV2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LinuxFunctionAppSlotAuthSettingsV2ActiveDirectoryV2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsV2ActiveDirectoryV2OutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f37170e1d99776caf2469fef37666e8e8a850e5fde8376026dbb2a1fd9c98dab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedApplications")
    def reset_allowed_applications(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedApplications", []))

    @jsii.member(jsii_name="resetAllowedAudiences")
    def reset_allowed_audiences(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedAudiences", []))

    @jsii.member(jsii_name="resetAllowedGroups")
    def reset_allowed_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedGroups", []))

    @jsii.member(jsii_name="resetAllowedIdentities")
    def reset_allowed_identities(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedIdentities", []))

    @jsii.member(jsii_name="resetClientSecretCertificateThumbprint")
    def reset_client_secret_certificate_thumbprint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecretCertificateThumbprint", []))

    @jsii.member(jsii_name="resetClientSecretSettingName")
    def reset_client_secret_setting_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecretSettingName", []))

    @jsii.member(jsii_name="resetJwtAllowedClientApplications")
    def reset_jwt_allowed_client_applications(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJwtAllowedClientApplications", []))

    @jsii.member(jsii_name="resetJwtAllowedGroups")
    def reset_jwt_allowed_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJwtAllowedGroups", []))

    @jsii.member(jsii_name="resetLoginParameters")
    def reset_login_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoginParameters", []))

    @jsii.member(jsii_name="resetWwwAuthenticationDisabled")
    def reset_www_authentication_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWwwAuthenticationDisabled", []))

    @builtins.property
    @jsii.member(jsii_name="allowedApplicationsInput")
    def allowed_applications_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedApplicationsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedAudiencesInput")
    def allowed_audiences_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedAudiencesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedGroupsInput")
    def allowed_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedIdentitiesInput")
    def allowed_identities_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedIdentitiesInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretCertificateThumbprintInput")
    def client_secret_certificate_thumbprint_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretCertificateThumbprintInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingNameInput")
    def client_secret_setting_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretSettingNameInput"))

    @builtins.property
    @jsii.member(jsii_name="jwtAllowedClientApplicationsInput")
    def jwt_allowed_client_applications_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "jwtAllowedClientApplicationsInput"))

    @builtins.property
    @jsii.member(jsii_name="jwtAllowedGroupsInput")
    def jwt_allowed_groups_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "jwtAllowedGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="loginParametersInput")
    def login_parameters_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "loginParametersInput"))

    @builtins.property
    @jsii.member(jsii_name="tenantAuthEndpointInput")
    def tenant_auth_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tenantAuthEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="wwwAuthenticationDisabledInput")
    def www_authentication_disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "wwwAuthenticationDisabledInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedApplications")
    def allowed_applications(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedApplications"))

    @allowed_applications.setter
    def allowed_applications(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71617b6b5eb7e64131b71aba060cd24f38ec3cdf5a5b3b57dda1fb66331e517e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedApplications", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedAudiences")
    def allowed_audiences(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedAudiences"))

    @allowed_audiences.setter
    def allowed_audiences(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1967e32c08d41fa7186a3b17d6c0af721ed8fed141c71ba117a3d2c709fbf485)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedAudiences", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedGroups")
    def allowed_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedGroups"))

    @allowed_groups.setter
    def allowed_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a265bbfdca324afde1d7e48831da8222620dc6754a7772abfedb95d7e2efd68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedIdentities")
    def allowed_identities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedIdentities"))

    @allowed_identities.setter
    def allowed_identities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbe70f22e588bbb28ed0cc9e47216b671c498b0951b62f38c4b8d08ef9a83629)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedIdentities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42eb83cd5d330f41e626a25ce1f071a1c37f816c56b8b76cd96e9f2915343410)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecretCertificateThumbprint")
    def client_secret_certificate_thumbprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecretCertificateThumbprint"))

    @client_secret_certificate_thumbprint.setter
    def client_secret_certificate_thumbprint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af539259e9867f275803066f2822e2c5d8961951d47fbecd08ae166bbb9ae8f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecretCertificateThumbprint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingName")
    def client_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecretSettingName"))

    @client_secret_setting_name.setter
    def client_secret_setting_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b811913bff54670334cfbd9c9edf8fd44ff16352b1b2e65a9d40a83d3d77a757)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecretSettingName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jwtAllowedClientApplications")
    def jwt_allowed_client_applications(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jwtAllowedClientApplications"))

    @jwt_allowed_client_applications.setter
    def jwt_allowed_client_applications(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25c6fb6d22913ea0844251a22037d9ae6c6a2e90a840c9dc1c9b9a06208c248f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jwtAllowedClientApplications", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jwtAllowedGroups")
    def jwt_allowed_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jwtAllowedGroups"))

    @jwt_allowed_groups.setter
    def jwt_allowed_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4a933800cf1f29c73ffc5dd730297232f40e76f1305fde12058c1c3c11ad139)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jwtAllowedGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loginParameters")
    def login_parameters(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "loginParameters"))

    @login_parameters.setter
    def login_parameters(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__420e6b0851e131b3ed555344ef284556a3359e114f506fafe56e6c0fdbc360e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantAuthEndpoint")
    def tenant_auth_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantAuthEndpoint"))

    @tenant_auth_endpoint.setter
    def tenant_auth_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f67805f728c67fe9823626a5fef9d22fe5d44fe3aa8efcfb91da25f14a423d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tenantAuthEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="wwwAuthenticationDisabled")
    def www_authentication_disabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "wwwAuthenticationDisabled"))

    @www_authentication_disabled.setter
    def www_authentication_disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06eefa95604c63fa2c4a6b10e430dd59d34d954d7ef3f976f8cec7cf7fc60346)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wwwAuthenticationDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LinuxFunctionAppSlotAuthSettingsV2ActiveDirectoryV2]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotAuthSettingsV2ActiveDirectoryV2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LinuxFunctionAppSlotAuthSettingsV2ActiveDirectoryV2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7058b38f1082c0489a3d15244006a80b49fc7732ff2e82637b89f6e279e18348)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsV2AppleV2",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "client_secret_setting_name": "clientSecretSettingName",
    },
)
class LinuxFunctionAppSlotAuthSettingsV2AppleV2:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        client_secret_setting_name: builtins.str,
    ) -> None:
        '''
        :param client_id: The OpenID Connect Client ID for the Apple web application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_id LinuxFunctionAppSlot#client_id}
        :param client_secret_setting_name: The app setting name that contains the ``client_secret`` value used for Apple Login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret_setting_name LinuxFunctionAppSlot#client_secret_setting_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e9c515e9399106b81a2a5138548027c175543254ffbd5d6b94b0a284d31814a)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret_setting_name", value=client_secret_setting_name, expected_type=type_hints["client_secret_setting_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "client_secret_setting_name": client_secret_setting_name,
        }

    @builtins.property
    def client_id(self) -> builtins.str:
        '''The OpenID Connect Client ID for the Apple web application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_id LinuxFunctionAppSlot#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret_setting_name(self) -> builtins.str:
        '''The app setting name that contains the ``client_secret`` value used for Apple Login.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret_setting_name LinuxFunctionAppSlot#client_secret_setting_name}
        '''
        result = self._values.get("client_secret_setting_name")
        assert result is not None, "Required property 'client_secret_setting_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotAuthSettingsV2AppleV2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LinuxFunctionAppSlotAuthSettingsV2AppleV2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsV2AppleV2OutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2e642c9d31ced2244df5c1e062ddee59b07198c0e502758d1396c797933d7f5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="loginScopes")
    def login_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "loginScopes"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingNameInput")
    def client_secret_setting_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretSettingNameInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f83cb1bb3f07fb622d6392ed7c14dc0a5338c2ee6d93d3edc94bc008ed97858)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingName")
    def client_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecretSettingName"))

    @client_secret_setting_name.setter
    def client_secret_setting_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e41b089780b2ba491b38902bce60256cad8904a7a64d79848a638fa7ad2be6e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecretSettingName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LinuxFunctionAppSlotAuthSettingsV2AppleV2]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotAuthSettingsV2AppleV2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LinuxFunctionAppSlotAuthSettingsV2AppleV2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffca5e17e05d295550093443ee0ff93d8eaafe07ae1fd53f4dd65cc8e0a88631)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsV2AzureStaticWebAppV2",
    jsii_struct_bases=[],
    name_mapping={"client_id": "clientId"},
)
class LinuxFunctionAppSlotAuthSettingsV2AzureStaticWebAppV2:
    def __init__(self, *, client_id: builtins.str) -> None:
        '''
        :param client_id: The ID of the Client to use to authenticate with Azure Static Web App Authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_id LinuxFunctionAppSlot#client_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99a4e6e413dbc4d2c20ba609619902c3e9d8d7e6430af63e0eaa09f6fdf0351c)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
        }

    @builtins.property
    def client_id(self) -> builtins.str:
        '''The ID of the Client to use to authenticate with Azure Static Web App Authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_id LinuxFunctionAppSlot#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotAuthSettingsV2AzureStaticWebAppV2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LinuxFunctionAppSlotAuthSettingsV2AzureStaticWebAppV2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsV2AzureStaticWebAppV2OutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a103c153c453f2a8663ddade02d0880f3c3fce989feda55772685fe38f045142)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64446197fd14537586b12611d4225f0983d27ceca85c99cdca5c93f588d0b112)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LinuxFunctionAppSlotAuthSettingsV2AzureStaticWebAppV2]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotAuthSettingsV2AzureStaticWebAppV2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LinuxFunctionAppSlotAuthSettingsV2AzureStaticWebAppV2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__654db6fafec10d1d1ee3e6c5beba2472f506afb56da943331f1075872f40c6c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsV2CustomOidcV2",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "name": "name",
        "openid_configuration_endpoint": "openidConfigurationEndpoint",
        "name_claim_type": "nameClaimType",
        "scopes": "scopes",
    },
)
class LinuxFunctionAppSlotAuthSettingsV2CustomOidcV2:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        name: builtins.str,
        openid_configuration_endpoint: builtins.str,
        name_claim_type: typing.Optional[builtins.str] = None,
        scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param client_id: The ID of the Client to use to authenticate with this Custom OIDC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_id LinuxFunctionAppSlot#client_id}
        :param name: The name of the Custom OIDC Authentication Provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#name LinuxFunctionAppSlot#name}
        :param openid_configuration_endpoint: The endpoint that contains all the configuration endpoints for this Custom OIDC provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#openid_configuration_endpoint LinuxFunctionAppSlot#openid_configuration_endpoint}
        :param name_claim_type: The name of the claim that contains the users name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#name_claim_type LinuxFunctionAppSlot#name_claim_type}
        :param scopes: The list of the scopes that should be requested while authenticating. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#scopes LinuxFunctionAppSlot#scopes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83d543532f436add229e3f7a7f7e0a76ab0cf9f709b54dfb23af294d2f053521)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument openid_configuration_endpoint", value=openid_configuration_endpoint, expected_type=type_hints["openid_configuration_endpoint"])
            check_type(argname="argument name_claim_type", value=name_claim_type, expected_type=type_hints["name_claim_type"])
            check_type(argname="argument scopes", value=scopes, expected_type=type_hints["scopes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "name": name,
            "openid_configuration_endpoint": openid_configuration_endpoint,
        }
        if name_claim_type is not None:
            self._values["name_claim_type"] = name_claim_type
        if scopes is not None:
            self._values["scopes"] = scopes

    @builtins.property
    def client_id(self) -> builtins.str:
        '''The ID of the Client to use to authenticate with this Custom OIDC.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_id LinuxFunctionAppSlot#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the Custom OIDC Authentication Provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#name LinuxFunctionAppSlot#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def openid_configuration_endpoint(self) -> builtins.str:
        '''The endpoint that contains all the configuration endpoints for this Custom OIDC provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#openid_configuration_endpoint LinuxFunctionAppSlot#openid_configuration_endpoint}
        '''
        result = self._values.get("openid_configuration_endpoint")
        assert result is not None, "Required property 'openid_configuration_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name_claim_type(self) -> typing.Optional[builtins.str]:
        '''The name of the claim that contains the users name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#name_claim_type LinuxFunctionAppSlot#name_claim_type}
        '''
        result = self._values.get("name_claim_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of the scopes that should be requested while authenticating.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#scopes LinuxFunctionAppSlot#scopes}
        '''
        result = self._values.get("scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotAuthSettingsV2CustomOidcV2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LinuxFunctionAppSlotAuthSettingsV2CustomOidcV2List(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsV2CustomOidcV2List",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c14d6682b6105021c92ce333153e2146fe7e68c628107a6721201cc4f4b49c6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LinuxFunctionAppSlotAuthSettingsV2CustomOidcV2OutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d80408fa765ac8b226b1567ecc9016bd685f065bad3397bb7bee04b3e98513dc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LinuxFunctionAppSlotAuthSettingsV2CustomOidcV2OutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f05509d98a30c80a3e6e1559f52af9d89dfc63692074f7a73584856e0e578d2d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9b565e4043418bef8b45c2b6d6a3c6e06a1cf8c78125635e4f0ebfc07640f45)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b160ebf81ef070f333fb13e71344cdb74f50748ba4104c3e528cd1103951ade)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotAuthSettingsV2CustomOidcV2]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotAuthSettingsV2CustomOidcV2]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotAuthSettingsV2CustomOidcV2]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de2bd1ad3918dc8045b3dbf2d8c562a3eb22eca0f4a46f12b9cac9386a3e6bcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LinuxFunctionAppSlotAuthSettingsV2CustomOidcV2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsV2CustomOidcV2OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0d908006ff25d473e2421f7e91eaeb05a119dd900ec7455fb01d863aa5886b9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetNameClaimType")
    def reset_name_claim_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNameClaimType", []))

    @jsii.member(jsii_name="resetScopes")
    def reset_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScopes", []))

    @builtins.property
    @jsii.member(jsii_name="authorisationEndpoint")
    def authorisation_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authorisationEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="certificationUri")
    def certification_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "certificationUri"))

    @builtins.property
    @jsii.member(jsii_name="clientCredentialMethod")
    def client_credential_method(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCredentialMethod"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingName")
    def client_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecretSettingName"))

    @builtins.property
    @jsii.member(jsii_name="issuerEndpoint")
    def issuer_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuerEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="tokenEndpoint")
    def token_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="nameClaimTypeInput")
    def name_claim_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameClaimTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="openidConfigurationEndpointInput")
    def openid_configuration_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "openidConfigurationEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="scopesInput")
    def scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scopesInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e3bf8b670aa073b994bf58654c66f1b96a59a446de64b38a74196cc42ddbeb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7c940a013f7abb193388e2cf2bc6d738cb464464295314d425aaa2ec2bd15f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nameClaimType")
    def name_claim_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nameClaimType"))

    @name_claim_type.setter
    def name_claim_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4ba29a371587739ebcf076c58525513a31465485843ec58b80c65f6365813a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nameClaimType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="openidConfigurationEndpoint")
    def openid_configuration_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "openidConfigurationEndpoint"))

    @openid_configuration_endpoint.setter
    def openid_configuration_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cf9b4d548ddf3142c6bf160a1746aa2f1cd84aad4f12de8a8dafe74fb9faca5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "openidConfigurationEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scopes"))

    @scopes.setter
    def scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55352c43927bf7306d8b724b84e5775ca49beb2fc9d32697eef56784d367b4d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotAuthSettingsV2CustomOidcV2]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotAuthSettingsV2CustomOidcV2]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotAuthSettingsV2CustomOidcV2]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45b1e4c3a8eefdf8e296f72e4b6ccaa3ac168c1a0238c73734db1035cb600166)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsV2FacebookV2",
    jsii_struct_bases=[],
    name_mapping={
        "app_id": "appId",
        "app_secret_setting_name": "appSecretSettingName",
        "graph_api_version": "graphApiVersion",
        "login_scopes": "loginScopes",
    },
)
class LinuxFunctionAppSlotAuthSettingsV2FacebookV2:
    def __init__(
        self,
        *,
        app_id: builtins.str,
        app_secret_setting_name: builtins.str,
        graph_api_version: typing.Optional[builtins.str] = None,
        login_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param app_id: The App ID of the Facebook app used for login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#app_id LinuxFunctionAppSlot#app_id}
        :param app_secret_setting_name: The app setting name that contains the ``app_secret`` value used for Facebook Login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#app_secret_setting_name LinuxFunctionAppSlot#app_secret_setting_name}
        :param graph_api_version: The version of the Facebook API to be used while logging in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#graph_api_version LinuxFunctionAppSlot#graph_api_version}
        :param login_scopes: Specifies a list of scopes to be requested as part of Facebook Login authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#login_scopes LinuxFunctionAppSlot#login_scopes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa9b5e0d890e79da35cea3cd6ee1926d259be41f3933e6eb0408b4bee095dc10)
            check_type(argname="argument app_id", value=app_id, expected_type=type_hints["app_id"])
            check_type(argname="argument app_secret_setting_name", value=app_secret_setting_name, expected_type=type_hints["app_secret_setting_name"])
            check_type(argname="argument graph_api_version", value=graph_api_version, expected_type=type_hints["graph_api_version"])
            check_type(argname="argument login_scopes", value=login_scopes, expected_type=type_hints["login_scopes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_id": app_id,
            "app_secret_setting_name": app_secret_setting_name,
        }
        if graph_api_version is not None:
            self._values["graph_api_version"] = graph_api_version
        if login_scopes is not None:
            self._values["login_scopes"] = login_scopes

    @builtins.property
    def app_id(self) -> builtins.str:
        '''The App ID of the Facebook app used for login.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#app_id LinuxFunctionAppSlot#app_id}
        '''
        result = self._values.get("app_id")
        assert result is not None, "Required property 'app_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_secret_setting_name(self) -> builtins.str:
        '''The app setting name that contains the ``app_secret`` value used for Facebook Login.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#app_secret_setting_name LinuxFunctionAppSlot#app_secret_setting_name}
        '''
        result = self._values.get("app_secret_setting_name")
        assert result is not None, "Required property 'app_secret_setting_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def graph_api_version(self) -> typing.Optional[builtins.str]:
        '''The version of the Facebook API to be used while logging in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#graph_api_version LinuxFunctionAppSlot#graph_api_version}
        '''
        result = self._values.get("graph_api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def login_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of scopes to be requested as part of Facebook Login authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#login_scopes LinuxFunctionAppSlot#login_scopes}
        '''
        result = self._values.get("login_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotAuthSettingsV2FacebookV2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LinuxFunctionAppSlotAuthSettingsV2FacebookV2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsV2FacebookV2OutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30a7de1dfe4d10f9027caa0e620baeca2faf2001ff136a385d83abe37db3e5da)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGraphApiVersion")
    def reset_graph_api_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGraphApiVersion", []))

    @jsii.member(jsii_name="resetLoginScopes")
    def reset_login_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoginScopes", []))

    @builtins.property
    @jsii.member(jsii_name="appIdInput")
    def app_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appIdInput"))

    @builtins.property
    @jsii.member(jsii_name="appSecretSettingNameInput")
    def app_secret_setting_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appSecretSettingNameInput"))

    @builtins.property
    @jsii.member(jsii_name="graphApiVersionInput")
    def graph_api_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "graphApiVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="loginScopesInput")
    def login_scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "loginScopesInput"))

    @builtins.property
    @jsii.member(jsii_name="appId")
    def app_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appId"))

    @app_id.setter
    def app_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__029b7824a8d5098f56546e60557ce4d7c60a2d395c47ea8e16ff67292114e972)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appSecretSettingName")
    def app_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appSecretSettingName"))

    @app_secret_setting_name.setter
    def app_secret_setting_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91f6a5369b23f52108801218138ca183de6bec2f37191bdfcecd364cc5fb1281)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appSecretSettingName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="graphApiVersion")
    def graph_api_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "graphApiVersion"))

    @graph_api_version.setter
    def graph_api_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a01818213d789ccd24de11fc14fff51cd6264961500be0271e160652b834f984)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "graphApiVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loginScopes")
    def login_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "loginScopes"))

    @login_scopes.setter
    def login_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c75fd2cea70ac0597afd8c33fd520f4d907c853a04e03651e52ef31bf3177bf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginScopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LinuxFunctionAppSlotAuthSettingsV2FacebookV2]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotAuthSettingsV2FacebookV2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LinuxFunctionAppSlotAuthSettingsV2FacebookV2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc317b370dfd43884733e826e22c0cbb34788cf6eb32e443ac5e68c64d07b0ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsV2GithubV2",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "client_secret_setting_name": "clientSecretSettingName",
        "login_scopes": "loginScopes",
    },
)
class LinuxFunctionAppSlotAuthSettingsV2GithubV2:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        client_secret_setting_name: builtins.str,
        login_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param client_id: The ID of the GitHub app used for login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_id LinuxFunctionAppSlot#client_id}
        :param client_secret_setting_name: The app setting name that contains the ``client_secret`` value used for GitHub Login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret_setting_name LinuxFunctionAppSlot#client_secret_setting_name}
        :param login_scopes: Specifies a list of OAuth 2.0 scopes that will be requested as part of GitHub Login authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#login_scopes LinuxFunctionAppSlot#login_scopes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4b84cb00f7aa81495aad263a27b13c4aaa144844e60de5b893a3c1cd6dbbd18)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret_setting_name", value=client_secret_setting_name, expected_type=type_hints["client_secret_setting_name"])
            check_type(argname="argument login_scopes", value=login_scopes, expected_type=type_hints["login_scopes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "client_secret_setting_name": client_secret_setting_name,
        }
        if login_scopes is not None:
            self._values["login_scopes"] = login_scopes

    @builtins.property
    def client_id(self) -> builtins.str:
        '''The ID of the GitHub app used for login.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_id LinuxFunctionAppSlot#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret_setting_name(self) -> builtins.str:
        '''The app setting name that contains the ``client_secret`` value used for GitHub Login.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret_setting_name LinuxFunctionAppSlot#client_secret_setting_name}
        '''
        result = self._values.get("client_secret_setting_name")
        assert result is not None, "Required property 'client_secret_setting_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def login_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of OAuth 2.0 scopes that will be requested as part of GitHub Login authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#login_scopes LinuxFunctionAppSlot#login_scopes}
        '''
        result = self._values.get("login_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotAuthSettingsV2GithubV2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LinuxFunctionAppSlotAuthSettingsV2GithubV2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsV2GithubV2OutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94658f2cf4229c3f63836f4c2fa288b59554e68253709e3db7c055db7b851f3e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetLoginScopes")
    def reset_login_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoginScopes", []))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingNameInput")
    def client_secret_setting_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretSettingNameInput"))

    @builtins.property
    @jsii.member(jsii_name="loginScopesInput")
    def login_scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "loginScopesInput"))

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fc1abfde06742120d25c7a289bfe71ed980256c4c03fec689860c71a6ba825d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingName")
    def client_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecretSettingName"))

    @client_secret_setting_name.setter
    def client_secret_setting_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0da9a8ed499183d062065e6f59a8ca7940ca7f795e5fbd0696ab956aa7db0ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecretSettingName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loginScopes")
    def login_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "loginScopes"))

    @login_scopes.setter
    def login_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f757e5b158403858d18cc01f1e78e75801017706efd6bbcf1b134fbed281a3cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginScopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LinuxFunctionAppSlotAuthSettingsV2GithubV2]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotAuthSettingsV2GithubV2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LinuxFunctionAppSlotAuthSettingsV2GithubV2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5d1711d343824facd359bfd7a4caf6a5e811cd372c8f091872c8488a616a922)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsV2GoogleV2",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "client_secret_setting_name": "clientSecretSettingName",
        "allowed_audiences": "allowedAudiences",
        "login_scopes": "loginScopes",
    },
)
class LinuxFunctionAppSlotAuthSettingsV2GoogleV2:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        client_secret_setting_name: builtins.str,
        allowed_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
        login_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param client_id: The OpenID Connect Client ID for the Google web application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_id LinuxFunctionAppSlot#client_id}
        :param client_secret_setting_name: The app setting name that contains the ``client_secret`` value used for Google Login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret_setting_name LinuxFunctionAppSlot#client_secret_setting_name}
        :param allowed_audiences: Specifies a list of Allowed Audiences that will be requested as part of Google Sign-In authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#allowed_audiences LinuxFunctionAppSlot#allowed_audiences}
        :param login_scopes: Specifies a list of Login scopes that will be requested as part of Google Sign-In authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#login_scopes LinuxFunctionAppSlot#login_scopes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70389e8b7646dd92e349bc021698ef2d4627154e692f84d6c899c6038a62e6de)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret_setting_name", value=client_secret_setting_name, expected_type=type_hints["client_secret_setting_name"])
            check_type(argname="argument allowed_audiences", value=allowed_audiences, expected_type=type_hints["allowed_audiences"])
            check_type(argname="argument login_scopes", value=login_scopes, expected_type=type_hints["login_scopes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "client_secret_setting_name": client_secret_setting_name,
        }
        if allowed_audiences is not None:
            self._values["allowed_audiences"] = allowed_audiences
        if login_scopes is not None:
            self._values["login_scopes"] = login_scopes

    @builtins.property
    def client_id(self) -> builtins.str:
        '''The OpenID Connect Client ID for the Google web application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_id LinuxFunctionAppSlot#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret_setting_name(self) -> builtins.str:
        '''The app setting name that contains the ``client_secret`` value used for Google Login.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret_setting_name LinuxFunctionAppSlot#client_secret_setting_name}
        '''
        result = self._values.get("client_secret_setting_name")
        assert result is not None, "Required property 'client_secret_setting_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_audiences(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of Allowed Audiences that will be requested as part of Google Sign-In authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#allowed_audiences LinuxFunctionAppSlot#allowed_audiences}
        '''
        result = self._values.get("allowed_audiences")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def login_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of Login scopes that will be requested as part of Google Sign-In authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#login_scopes LinuxFunctionAppSlot#login_scopes}
        '''
        result = self._values.get("login_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotAuthSettingsV2GoogleV2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LinuxFunctionAppSlotAuthSettingsV2GoogleV2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsV2GoogleV2OutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f4408c307e73eba8e0e94491fd37cb9bae2bbc90e58f3738366f27a6d375df8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedAudiences")
    def reset_allowed_audiences(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedAudiences", []))

    @jsii.member(jsii_name="resetLoginScopes")
    def reset_login_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoginScopes", []))

    @builtins.property
    @jsii.member(jsii_name="allowedAudiencesInput")
    def allowed_audiences_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedAudiencesInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingNameInput")
    def client_secret_setting_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretSettingNameInput"))

    @builtins.property
    @jsii.member(jsii_name="loginScopesInput")
    def login_scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "loginScopesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedAudiences")
    def allowed_audiences(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedAudiences"))

    @allowed_audiences.setter
    def allowed_audiences(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74ba8b101164eb6edeae1fcf1bfa3c80788ceabb8abe502236546545fee8aa44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedAudiences", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49869519f1a48a773f04d38053b8d92aa1bb4e233e66bfd8c316007c5ccb120c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingName")
    def client_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecretSettingName"))

    @client_secret_setting_name.setter
    def client_secret_setting_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2167a1c905727aefb98a47d303c6e588847c7d081283eab52bb0ccaa8f8caed0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecretSettingName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loginScopes")
    def login_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "loginScopes"))

    @login_scopes.setter
    def login_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99aeb3521a37a6cc29fa3771fcc6b0df2fe01235b46487f2c9eb079a43cbc0b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginScopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LinuxFunctionAppSlotAuthSettingsV2GoogleV2]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotAuthSettingsV2GoogleV2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LinuxFunctionAppSlotAuthSettingsV2GoogleV2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e4cc6a9b6e874ffc9fed89be20427a69cb206cd4f0e555e61466f383e8bcc26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsV2Login",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_external_redirect_urls": "allowedExternalRedirectUrls",
        "cookie_expiration_convention": "cookieExpirationConvention",
        "cookie_expiration_time": "cookieExpirationTime",
        "logout_endpoint": "logoutEndpoint",
        "nonce_expiration_time": "nonceExpirationTime",
        "preserve_url_fragments_for_logins": "preserveUrlFragmentsForLogins",
        "token_refresh_extension_time": "tokenRefreshExtensionTime",
        "token_store_enabled": "tokenStoreEnabled",
        "token_store_path": "tokenStorePath",
        "token_store_sas_setting_name": "tokenStoreSasSettingName",
        "validate_nonce": "validateNonce",
    },
)
class LinuxFunctionAppSlotAuthSettingsV2Login:
    def __init__(
        self,
        *,
        allowed_external_redirect_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
        cookie_expiration_convention: typing.Optional[builtins.str] = None,
        cookie_expiration_time: typing.Optional[builtins.str] = None,
        logout_endpoint: typing.Optional[builtins.str] = None,
        nonce_expiration_time: typing.Optional[builtins.str] = None,
        preserve_url_fragments_for_logins: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        token_refresh_extension_time: typing.Optional[jsii.Number] = None,
        token_store_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        token_store_path: typing.Optional[builtins.str] = None,
        token_store_sas_setting_name: typing.Optional[builtins.str] = None,
        validate_nonce: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allowed_external_redirect_urls: External URLs that can be redirected to as part of logging in or logging out of the app. This is an advanced setting typically only needed by Windows Store application backends. **Note:** URLs within the current domain are always implicitly allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#allowed_external_redirect_urls LinuxFunctionAppSlot#allowed_external_redirect_urls}
        :param cookie_expiration_convention: The method by which cookies expire. Possible values include: ``FixedTime``, and ``IdentityProviderDerived``. Defaults to ``FixedTime``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#cookie_expiration_convention LinuxFunctionAppSlot#cookie_expiration_convention}
        :param cookie_expiration_time: The time after the request is made when the session cookie should expire. Defaults to ``08:00:00``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#cookie_expiration_time LinuxFunctionAppSlot#cookie_expiration_time}
        :param logout_endpoint: The endpoint to which logout requests should be made. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#logout_endpoint LinuxFunctionAppSlot#logout_endpoint}
        :param nonce_expiration_time: The time after the request is made when the nonce should expire. Defaults to ``00:05:00``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#nonce_expiration_time LinuxFunctionAppSlot#nonce_expiration_time}
        :param preserve_url_fragments_for_logins: Should the fragments from the request be preserved after the login request is made. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#preserve_url_fragments_for_logins LinuxFunctionAppSlot#preserve_url_fragments_for_logins}
        :param token_refresh_extension_time: The number of hours after session token expiration that a session token can be used to call the token refresh API. Defaults to ``72`` hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#token_refresh_extension_time LinuxFunctionAppSlot#token_refresh_extension_time}
        :param token_store_enabled: Should the Token Store configuration Enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#token_store_enabled LinuxFunctionAppSlot#token_store_enabled}
        :param token_store_path: The directory path in the App Filesystem in which the tokens will be stored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#token_store_path LinuxFunctionAppSlot#token_store_path}
        :param token_store_sas_setting_name: The name of the app setting which contains the SAS URL of the blob storage containing the tokens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#token_store_sas_setting_name LinuxFunctionAppSlot#token_store_sas_setting_name}
        :param validate_nonce: Should the nonce be validated while completing the login flow. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#validate_nonce LinuxFunctionAppSlot#validate_nonce}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60d389bde4631920900d76f4f57730c81b6a7ce2c0250d6ce5e0da69d31610ba)
            check_type(argname="argument allowed_external_redirect_urls", value=allowed_external_redirect_urls, expected_type=type_hints["allowed_external_redirect_urls"])
            check_type(argname="argument cookie_expiration_convention", value=cookie_expiration_convention, expected_type=type_hints["cookie_expiration_convention"])
            check_type(argname="argument cookie_expiration_time", value=cookie_expiration_time, expected_type=type_hints["cookie_expiration_time"])
            check_type(argname="argument logout_endpoint", value=logout_endpoint, expected_type=type_hints["logout_endpoint"])
            check_type(argname="argument nonce_expiration_time", value=nonce_expiration_time, expected_type=type_hints["nonce_expiration_time"])
            check_type(argname="argument preserve_url_fragments_for_logins", value=preserve_url_fragments_for_logins, expected_type=type_hints["preserve_url_fragments_for_logins"])
            check_type(argname="argument token_refresh_extension_time", value=token_refresh_extension_time, expected_type=type_hints["token_refresh_extension_time"])
            check_type(argname="argument token_store_enabled", value=token_store_enabled, expected_type=type_hints["token_store_enabled"])
            check_type(argname="argument token_store_path", value=token_store_path, expected_type=type_hints["token_store_path"])
            check_type(argname="argument token_store_sas_setting_name", value=token_store_sas_setting_name, expected_type=type_hints["token_store_sas_setting_name"])
            check_type(argname="argument validate_nonce", value=validate_nonce, expected_type=type_hints["validate_nonce"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_external_redirect_urls is not None:
            self._values["allowed_external_redirect_urls"] = allowed_external_redirect_urls
        if cookie_expiration_convention is not None:
            self._values["cookie_expiration_convention"] = cookie_expiration_convention
        if cookie_expiration_time is not None:
            self._values["cookie_expiration_time"] = cookie_expiration_time
        if logout_endpoint is not None:
            self._values["logout_endpoint"] = logout_endpoint
        if nonce_expiration_time is not None:
            self._values["nonce_expiration_time"] = nonce_expiration_time
        if preserve_url_fragments_for_logins is not None:
            self._values["preserve_url_fragments_for_logins"] = preserve_url_fragments_for_logins
        if token_refresh_extension_time is not None:
            self._values["token_refresh_extension_time"] = token_refresh_extension_time
        if token_store_enabled is not None:
            self._values["token_store_enabled"] = token_store_enabled
        if token_store_path is not None:
            self._values["token_store_path"] = token_store_path
        if token_store_sas_setting_name is not None:
            self._values["token_store_sas_setting_name"] = token_store_sas_setting_name
        if validate_nonce is not None:
            self._values["validate_nonce"] = validate_nonce

    @builtins.property
    def allowed_external_redirect_urls(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''External URLs that can be redirected to as part of logging in or logging out of the app.

        This is an advanced setting typically only needed by Windows Store application backends. **Note:** URLs within the current domain are always implicitly allowed.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#allowed_external_redirect_urls LinuxFunctionAppSlot#allowed_external_redirect_urls}
        '''
        result = self._values.get("allowed_external_redirect_urls")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cookie_expiration_convention(self) -> typing.Optional[builtins.str]:
        '''The method by which cookies expire. Possible values include: ``FixedTime``, and ``IdentityProviderDerived``. Defaults to ``FixedTime``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#cookie_expiration_convention LinuxFunctionAppSlot#cookie_expiration_convention}
        '''
        result = self._values.get("cookie_expiration_convention")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cookie_expiration_time(self) -> typing.Optional[builtins.str]:
        '''The time after the request is made when the session cookie should expire. Defaults to ``08:00:00``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#cookie_expiration_time LinuxFunctionAppSlot#cookie_expiration_time}
        '''
        result = self._values.get("cookie_expiration_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logout_endpoint(self) -> typing.Optional[builtins.str]:
        '''The endpoint to which logout requests should be made.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#logout_endpoint LinuxFunctionAppSlot#logout_endpoint}
        '''
        result = self._values.get("logout_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nonce_expiration_time(self) -> typing.Optional[builtins.str]:
        '''The time after the request is made when the nonce should expire. Defaults to ``00:05:00``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#nonce_expiration_time LinuxFunctionAppSlot#nonce_expiration_time}
        '''
        result = self._values.get("nonce_expiration_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preserve_url_fragments_for_logins(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the fragments from the request be preserved after the login request is made. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#preserve_url_fragments_for_logins LinuxFunctionAppSlot#preserve_url_fragments_for_logins}
        '''
        result = self._values.get("preserve_url_fragments_for_logins")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def token_refresh_extension_time(self) -> typing.Optional[jsii.Number]:
        '''The number of hours after session token expiration that a session token can be used to call the token refresh API.

        Defaults to ``72`` hours.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#token_refresh_extension_time LinuxFunctionAppSlot#token_refresh_extension_time}
        '''
        result = self._values.get("token_refresh_extension_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def token_store_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the Token Store configuration Enabled. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#token_store_enabled LinuxFunctionAppSlot#token_store_enabled}
        '''
        result = self._values.get("token_store_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def token_store_path(self) -> typing.Optional[builtins.str]:
        '''The directory path in the App Filesystem in which the tokens will be stored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#token_store_path LinuxFunctionAppSlot#token_store_path}
        '''
        result = self._values.get("token_store_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_store_sas_setting_name(self) -> typing.Optional[builtins.str]:
        '''The name of the app setting which contains the SAS URL of the blob storage containing the tokens.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#token_store_sas_setting_name LinuxFunctionAppSlot#token_store_sas_setting_name}
        '''
        result = self._values.get("token_store_sas_setting_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def validate_nonce(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the nonce be validated while completing the login flow. Defaults to ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#validate_nonce LinuxFunctionAppSlot#validate_nonce}
        '''
        result = self._values.get("validate_nonce")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotAuthSettingsV2Login(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LinuxFunctionAppSlotAuthSettingsV2LoginOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsV2LoginOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad21f2010f4a11a33000cf23dc42d821803d1180c950ac9af08bd3212bac18d5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedExternalRedirectUrls")
    def reset_allowed_external_redirect_urls(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedExternalRedirectUrls", []))

    @jsii.member(jsii_name="resetCookieExpirationConvention")
    def reset_cookie_expiration_convention(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCookieExpirationConvention", []))

    @jsii.member(jsii_name="resetCookieExpirationTime")
    def reset_cookie_expiration_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCookieExpirationTime", []))

    @jsii.member(jsii_name="resetLogoutEndpoint")
    def reset_logout_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogoutEndpoint", []))

    @jsii.member(jsii_name="resetNonceExpirationTime")
    def reset_nonce_expiration_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNonceExpirationTime", []))

    @jsii.member(jsii_name="resetPreserveUrlFragmentsForLogins")
    def reset_preserve_url_fragments_for_logins(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreserveUrlFragmentsForLogins", []))

    @jsii.member(jsii_name="resetTokenRefreshExtensionTime")
    def reset_token_refresh_extension_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTokenRefreshExtensionTime", []))

    @jsii.member(jsii_name="resetTokenStoreEnabled")
    def reset_token_store_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTokenStoreEnabled", []))

    @jsii.member(jsii_name="resetTokenStorePath")
    def reset_token_store_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTokenStorePath", []))

    @jsii.member(jsii_name="resetTokenStoreSasSettingName")
    def reset_token_store_sas_setting_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTokenStoreSasSettingName", []))

    @jsii.member(jsii_name="resetValidateNonce")
    def reset_validate_nonce(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValidateNonce", []))

    @builtins.property
    @jsii.member(jsii_name="allowedExternalRedirectUrlsInput")
    def allowed_external_redirect_urls_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedExternalRedirectUrlsInput"))

    @builtins.property
    @jsii.member(jsii_name="cookieExpirationConventionInput")
    def cookie_expiration_convention_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cookieExpirationConventionInput"))

    @builtins.property
    @jsii.member(jsii_name="cookieExpirationTimeInput")
    def cookie_expiration_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cookieExpirationTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="logoutEndpointInput")
    def logout_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logoutEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="nonceExpirationTimeInput")
    def nonce_expiration_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nonceExpirationTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="preserveUrlFragmentsForLoginsInput")
    def preserve_url_fragments_for_logins_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "preserveUrlFragmentsForLoginsInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenRefreshExtensionTimeInput")
    def token_refresh_extension_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "tokenRefreshExtensionTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenStoreEnabledInput")
    def token_store_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "tokenStoreEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenStorePathInput")
    def token_store_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenStorePathInput"))

    @builtins.property
    @jsii.member(jsii_name="tokenStoreSasSettingNameInput")
    def token_store_sas_setting_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tokenStoreSasSettingNameInput"))

    @builtins.property
    @jsii.member(jsii_name="validateNonceInput")
    def validate_nonce_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "validateNonceInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedExternalRedirectUrls")
    def allowed_external_redirect_urls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedExternalRedirectUrls"))

    @allowed_external_redirect_urls.setter
    def allowed_external_redirect_urls(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d6756ea9b7a87e2f9973c3a841ff801625593fe59fd04099ca3a84132ccf9d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedExternalRedirectUrls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cookieExpirationConvention")
    def cookie_expiration_convention(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cookieExpirationConvention"))

    @cookie_expiration_convention.setter
    def cookie_expiration_convention(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5f893492a7df8eefa80d1d807ecaed29218315e0819bbd82356a3bc7945c6da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cookieExpirationConvention", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cookieExpirationTime")
    def cookie_expiration_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cookieExpirationTime"))

    @cookie_expiration_time.setter
    def cookie_expiration_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a48d6fa832720c1989b8fed5a663b3871b9984953e9c792115df728f742b80e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cookieExpirationTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logoutEndpoint")
    def logout_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logoutEndpoint"))

    @logout_endpoint.setter
    def logout_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf0daa0de11322437801606fdecfe54215e879151bcfb84750f410338bbee0d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logoutEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nonceExpirationTime")
    def nonce_expiration_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nonceExpirationTime"))

    @nonce_expiration_time.setter
    def nonce_expiration_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b75cd87503b9fa2a71969150842316712c1eb95b1c91d0708db691e6c898969)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nonceExpirationTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preserveUrlFragmentsForLogins")
    def preserve_url_fragments_for_logins(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "preserveUrlFragmentsForLogins"))

    @preserve_url_fragments_for_logins.setter
    def preserve_url_fragments_for_logins(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__829d9d70e7754e3abdfde8eddea5f28e900e0cecb5364cfa8179dfceafc49d53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preserveUrlFragmentsForLogins", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenRefreshExtensionTime")
    def token_refresh_extension_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tokenRefreshExtensionTime"))

    @token_refresh_extension_time.setter
    def token_refresh_extension_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39aee961db3ce4c09de4f9bfdffed2b89625e383196c6a4f6b3b79b3ba439810)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenRefreshExtensionTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenStoreEnabled")
    def token_store_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "tokenStoreEnabled"))

    @token_store_enabled.setter
    def token_store_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2afc390137e1c48f7acf116cc9e33e4f1e0fbf9bbd8ddb38fe9c077285ab4d86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenStoreEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenStorePath")
    def token_store_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenStorePath"))

    @token_store_path.setter
    def token_store_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4490761f5104809369564ea8320da1e9dd2fbafcdb87942bd9bc48c4f6224fc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenStorePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenStoreSasSettingName")
    def token_store_sas_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenStoreSasSettingName"))

    @token_store_sas_setting_name.setter
    def token_store_sas_setting_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbc383adc0e8f1d4aff6756f7414155414a269a8ffd12c9ee1043a2a58575334)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenStoreSasSettingName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="validateNonce")
    def validate_nonce(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "validateNonce"))

    @validate_nonce.setter
    def validate_nonce(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fee42e8c32019f29d395b5e6eb0c22c903edf5629a231e67bd54db50eb47b6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validateNonce", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LinuxFunctionAppSlotAuthSettingsV2Login]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotAuthSettingsV2Login], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LinuxFunctionAppSlotAuthSettingsV2Login],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ecb567c99373aea6409e37e1c21284e03ac962da238514bd67328547a3b05ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsV2MicrosoftV2",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "client_secret_setting_name": "clientSecretSettingName",
        "allowed_audiences": "allowedAudiences",
        "login_scopes": "loginScopes",
    },
)
class LinuxFunctionAppSlotAuthSettingsV2MicrosoftV2:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        client_secret_setting_name: builtins.str,
        allowed_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
        login_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param client_id: The OAuth 2.0 client ID that was created for the app used for authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_id LinuxFunctionAppSlot#client_id}
        :param client_secret_setting_name: The app setting name containing the OAuth 2.0 client secret that was created for the app used for authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret_setting_name LinuxFunctionAppSlot#client_secret_setting_name}
        :param allowed_audiences: Specifies a list of Allowed Audiences that will be requested as part of Microsoft Sign-In authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#allowed_audiences LinuxFunctionAppSlot#allowed_audiences}
        :param login_scopes: The list of Login scopes that will be requested as part of Microsoft Account authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#login_scopes LinuxFunctionAppSlot#login_scopes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f72a30f60e14ce3f66310a1470bf0688ae1f3eff0ece48426f47c0c5516257ba)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret_setting_name", value=client_secret_setting_name, expected_type=type_hints["client_secret_setting_name"])
            check_type(argname="argument allowed_audiences", value=allowed_audiences, expected_type=type_hints["allowed_audiences"])
            check_type(argname="argument login_scopes", value=login_scopes, expected_type=type_hints["login_scopes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "client_secret_setting_name": client_secret_setting_name,
        }
        if allowed_audiences is not None:
            self._values["allowed_audiences"] = allowed_audiences
        if login_scopes is not None:
            self._values["login_scopes"] = login_scopes

    @builtins.property
    def client_id(self) -> builtins.str:
        '''The OAuth 2.0 client ID that was created for the app used for authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_id LinuxFunctionAppSlot#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret_setting_name(self) -> builtins.str:
        '''The app setting name containing the OAuth 2.0 client secret that was created for the app used for authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret_setting_name LinuxFunctionAppSlot#client_secret_setting_name}
        '''
        result = self._values.get("client_secret_setting_name")
        assert result is not None, "Required property 'client_secret_setting_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_audiences(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of Allowed Audiences that will be requested as part of Microsoft Sign-In authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#allowed_audiences LinuxFunctionAppSlot#allowed_audiences}
        '''
        result = self._values.get("allowed_audiences")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def login_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of Login scopes that will be requested as part of Microsoft Account authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#login_scopes LinuxFunctionAppSlot#login_scopes}
        '''
        result = self._values.get("login_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotAuthSettingsV2MicrosoftV2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LinuxFunctionAppSlotAuthSettingsV2MicrosoftV2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsV2MicrosoftV2OutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0674ab71f34eb018f502dc64ea907c49beaf2f22906fc19309209facd9d3bb0f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedAudiences")
    def reset_allowed_audiences(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedAudiences", []))

    @jsii.member(jsii_name="resetLoginScopes")
    def reset_login_scopes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoginScopes", []))

    @builtins.property
    @jsii.member(jsii_name="allowedAudiencesInput")
    def allowed_audiences_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedAudiencesInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingNameInput")
    def client_secret_setting_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretSettingNameInput"))

    @builtins.property
    @jsii.member(jsii_name="loginScopesInput")
    def login_scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "loginScopesInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedAudiences")
    def allowed_audiences(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedAudiences"))

    @allowed_audiences.setter
    def allowed_audiences(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6949af6f6bc3a418476d1614dc5e3a1bc061ce82d4f4e3e2ba441f8640898c06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedAudiences", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e29933cbfbc1cc0558232cd1d1541e20b9d08e58fe0cb2bb9231b0a2b415bb0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingName")
    def client_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecretSettingName"))

    @client_secret_setting_name.setter
    def client_secret_setting_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5728a9af0ec1d25273842732f08ab8a565aa3a03f67d2799fa2be281df2e8552)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecretSettingName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loginScopes")
    def login_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "loginScopes"))

    @login_scopes.setter
    def login_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a593ea63c92aaf1032ee3528281168d36788a987189325e589689fc99fd13a8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginScopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LinuxFunctionAppSlotAuthSettingsV2MicrosoftV2]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotAuthSettingsV2MicrosoftV2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LinuxFunctionAppSlotAuthSettingsV2MicrosoftV2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81260382ca394b9405418f27c6f3ccaefa9eca0e49676a5157c659d9f0db6070)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LinuxFunctionAppSlotAuthSettingsV2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsV2OutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28faafe9b57d4e23ce04e42732569f1973178e4c01c752a387b214275a692e30)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putActiveDirectoryV2")
    def put_active_directory_v2(
        self,
        *,
        client_id: builtins.str,
        tenant_auth_endpoint: builtins.str,
        allowed_applications: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        allowed_identities: typing.Optional[typing.Sequence[builtins.str]] = None,
        client_secret_certificate_thumbprint: typing.Optional[builtins.str] = None,
        client_secret_setting_name: typing.Optional[builtins.str] = None,
        jwt_allowed_client_applications: typing.Optional[typing.Sequence[builtins.str]] = None,
        jwt_allowed_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        login_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        www_authentication_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param client_id: The ID of the Client to use to authenticate with Azure Active Directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_id LinuxFunctionAppSlot#client_id}
        :param tenant_auth_endpoint: The Azure Tenant Endpoint for the Authenticating Tenant. e.g. ``https://login.microsoftonline.com/v2.0/{tenant-guid}/``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#tenant_auth_endpoint LinuxFunctionAppSlot#tenant_auth_endpoint}
        :param allowed_applications: The list of allowed Applications for the Default Authorisation Policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#allowed_applications LinuxFunctionAppSlot#allowed_applications}
        :param allowed_audiences: Specifies a list of Allowed audience values to consider when validating JWTs issued by Azure Active Directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#allowed_audiences LinuxFunctionAppSlot#allowed_audiences}
        :param allowed_groups: The list of allowed Group Names for the Default Authorisation Policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#allowed_groups LinuxFunctionAppSlot#allowed_groups}
        :param allowed_identities: The list of allowed Identities for the Default Authorisation Policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#allowed_identities LinuxFunctionAppSlot#allowed_identities}
        :param client_secret_certificate_thumbprint: The thumbprint of the certificate used for signing purposes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret_certificate_thumbprint LinuxFunctionAppSlot#client_secret_certificate_thumbprint}
        :param client_secret_setting_name: The App Setting name that contains the client secret of the Client. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret_setting_name LinuxFunctionAppSlot#client_secret_setting_name}
        :param jwt_allowed_client_applications: A list of Allowed Client Applications in the JWT Claim. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#jwt_allowed_client_applications LinuxFunctionAppSlot#jwt_allowed_client_applications}
        :param jwt_allowed_groups: A list of Allowed Groups in the JWT Claim. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#jwt_allowed_groups LinuxFunctionAppSlot#jwt_allowed_groups}
        :param login_parameters: A map of key-value pairs to send to the Authorisation Endpoint when a user logs in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#login_parameters LinuxFunctionAppSlot#login_parameters}
        :param www_authentication_disabled: Should the www-authenticate provider should be omitted from the request? Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#www_authentication_disabled LinuxFunctionAppSlot#www_authentication_disabled}
        '''
        value = LinuxFunctionAppSlotAuthSettingsV2ActiveDirectoryV2(
            client_id=client_id,
            tenant_auth_endpoint=tenant_auth_endpoint,
            allowed_applications=allowed_applications,
            allowed_audiences=allowed_audiences,
            allowed_groups=allowed_groups,
            allowed_identities=allowed_identities,
            client_secret_certificate_thumbprint=client_secret_certificate_thumbprint,
            client_secret_setting_name=client_secret_setting_name,
            jwt_allowed_client_applications=jwt_allowed_client_applications,
            jwt_allowed_groups=jwt_allowed_groups,
            login_parameters=login_parameters,
            www_authentication_disabled=www_authentication_disabled,
        )

        return typing.cast(None, jsii.invoke(self, "putActiveDirectoryV2", [value]))

    @jsii.member(jsii_name="putAppleV2")
    def put_apple_v2(
        self,
        *,
        client_id: builtins.str,
        client_secret_setting_name: builtins.str,
    ) -> None:
        '''
        :param client_id: The OpenID Connect Client ID for the Apple web application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_id LinuxFunctionAppSlot#client_id}
        :param client_secret_setting_name: The app setting name that contains the ``client_secret`` value used for Apple Login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret_setting_name LinuxFunctionAppSlot#client_secret_setting_name}
        '''
        value = LinuxFunctionAppSlotAuthSettingsV2AppleV2(
            client_id=client_id, client_secret_setting_name=client_secret_setting_name
        )

        return typing.cast(None, jsii.invoke(self, "putAppleV2", [value]))

    @jsii.member(jsii_name="putAzureStaticWebAppV2")
    def put_azure_static_web_app_v2(self, *, client_id: builtins.str) -> None:
        '''
        :param client_id: The ID of the Client to use to authenticate with Azure Static Web App Authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_id LinuxFunctionAppSlot#client_id}
        '''
        value = LinuxFunctionAppSlotAuthSettingsV2AzureStaticWebAppV2(
            client_id=client_id
        )

        return typing.cast(None, jsii.invoke(self, "putAzureStaticWebAppV2", [value]))

    @jsii.member(jsii_name="putCustomOidcV2")
    def put_custom_oidc_v2(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LinuxFunctionAppSlotAuthSettingsV2CustomOidcV2, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0fe3b69f5bb068821abe77785ac6c074145a616b5cd5960b394b86fba1d20f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCustomOidcV2", [value]))

    @jsii.member(jsii_name="putFacebookV2")
    def put_facebook_v2(
        self,
        *,
        app_id: builtins.str,
        app_secret_setting_name: builtins.str,
        graph_api_version: typing.Optional[builtins.str] = None,
        login_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param app_id: The App ID of the Facebook app used for login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#app_id LinuxFunctionAppSlot#app_id}
        :param app_secret_setting_name: The app setting name that contains the ``app_secret`` value used for Facebook Login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#app_secret_setting_name LinuxFunctionAppSlot#app_secret_setting_name}
        :param graph_api_version: The version of the Facebook API to be used while logging in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#graph_api_version LinuxFunctionAppSlot#graph_api_version}
        :param login_scopes: Specifies a list of scopes to be requested as part of Facebook Login authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#login_scopes LinuxFunctionAppSlot#login_scopes}
        '''
        value = LinuxFunctionAppSlotAuthSettingsV2FacebookV2(
            app_id=app_id,
            app_secret_setting_name=app_secret_setting_name,
            graph_api_version=graph_api_version,
            login_scopes=login_scopes,
        )

        return typing.cast(None, jsii.invoke(self, "putFacebookV2", [value]))

    @jsii.member(jsii_name="putGithubV2")
    def put_github_v2(
        self,
        *,
        client_id: builtins.str,
        client_secret_setting_name: builtins.str,
        login_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param client_id: The ID of the GitHub app used for login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_id LinuxFunctionAppSlot#client_id}
        :param client_secret_setting_name: The app setting name that contains the ``client_secret`` value used for GitHub Login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret_setting_name LinuxFunctionAppSlot#client_secret_setting_name}
        :param login_scopes: Specifies a list of OAuth 2.0 scopes that will be requested as part of GitHub Login authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#login_scopes LinuxFunctionAppSlot#login_scopes}
        '''
        value = LinuxFunctionAppSlotAuthSettingsV2GithubV2(
            client_id=client_id,
            client_secret_setting_name=client_secret_setting_name,
            login_scopes=login_scopes,
        )

        return typing.cast(None, jsii.invoke(self, "putGithubV2", [value]))

    @jsii.member(jsii_name="putGoogleV2")
    def put_google_v2(
        self,
        *,
        client_id: builtins.str,
        client_secret_setting_name: builtins.str,
        allowed_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
        login_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param client_id: The OpenID Connect Client ID for the Google web application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_id LinuxFunctionAppSlot#client_id}
        :param client_secret_setting_name: The app setting name that contains the ``client_secret`` value used for Google Login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret_setting_name LinuxFunctionAppSlot#client_secret_setting_name}
        :param allowed_audiences: Specifies a list of Allowed Audiences that will be requested as part of Google Sign-In authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#allowed_audiences LinuxFunctionAppSlot#allowed_audiences}
        :param login_scopes: Specifies a list of Login scopes that will be requested as part of Google Sign-In authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#login_scopes LinuxFunctionAppSlot#login_scopes}
        '''
        value = LinuxFunctionAppSlotAuthSettingsV2GoogleV2(
            client_id=client_id,
            client_secret_setting_name=client_secret_setting_name,
            allowed_audiences=allowed_audiences,
            login_scopes=login_scopes,
        )

        return typing.cast(None, jsii.invoke(self, "putGoogleV2", [value]))

    @jsii.member(jsii_name="putLogin")
    def put_login(
        self,
        *,
        allowed_external_redirect_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
        cookie_expiration_convention: typing.Optional[builtins.str] = None,
        cookie_expiration_time: typing.Optional[builtins.str] = None,
        logout_endpoint: typing.Optional[builtins.str] = None,
        nonce_expiration_time: typing.Optional[builtins.str] = None,
        preserve_url_fragments_for_logins: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        token_refresh_extension_time: typing.Optional[jsii.Number] = None,
        token_store_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        token_store_path: typing.Optional[builtins.str] = None,
        token_store_sas_setting_name: typing.Optional[builtins.str] = None,
        validate_nonce: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allowed_external_redirect_urls: External URLs that can be redirected to as part of logging in or logging out of the app. This is an advanced setting typically only needed by Windows Store application backends. **Note:** URLs within the current domain are always implicitly allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#allowed_external_redirect_urls LinuxFunctionAppSlot#allowed_external_redirect_urls}
        :param cookie_expiration_convention: The method by which cookies expire. Possible values include: ``FixedTime``, and ``IdentityProviderDerived``. Defaults to ``FixedTime``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#cookie_expiration_convention LinuxFunctionAppSlot#cookie_expiration_convention}
        :param cookie_expiration_time: The time after the request is made when the session cookie should expire. Defaults to ``08:00:00``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#cookie_expiration_time LinuxFunctionAppSlot#cookie_expiration_time}
        :param logout_endpoint: The endpoint to which logout requests should be made. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#logout_endpoint LinuxFunctionAppSlot#logout_endpoint}
        :param nonce_expiration_time: The time after the request is made when the nonce should expire. Defaults to ``00:05:00``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#nonce_expiration_time LinuxFunctionAppSlot#nonce_expiration_time}
        :param preserve_url_fragments_for_logins: Should the fragments from the request be preserved after the login request is made. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#preserve_url_fragments_for_logins LinuxFunctionAppSlot#preserve_url_fragments_for_logins}
        :param token_refresh_extension_time: The number of hours after session token expiration that a session token can be used to call the token refresh API. Defaults to ``72`` hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#token_refresh_extension_time LinuxFunctionAppSlot#token_refresh_extension_time}
        :param token_store_enabled: Should the Token Store configuration Enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#token_store_enabled LinuxFunctionAppSlot#token_store_enabled}
        :param token_store_path: The directory path in the App Filesystem in which the tokens will be stored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#token_store_path LinuxFunctionAppSlot#token_store_path}
        :param token_store_sas_setting_name: The name of the app setting which contains the SAS URL of the blob storage containing the tokens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#token_store_sas_setting_name LinuxFunctionAppSlot#token_store_sas_setting_name}
        :param validate_nonce: Should the nonce be validated while completing the login flow. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#validate_nonce LinuxFunctionAppSlot#validate_nonce}
        '''
        value = LinuxFunctionAppSlotAuthSettingsV2Login(
            allowed_external_redirect_urls=allowed_external_redirect_urls,
            cookie_expiration_convention=cookie_expiration_convention,
            cookie_expiration_time=cookie_expiration_time,
            logout_endpoint=logout_endpoint,
            nonce_expiration_time=nonce_expiration_time,
            preserve_url_fragments_for_logins=preserve_url_fragments_for_logins,
            token_refresh_extension_time=token_refresh_extension_time,
            token_store_enabled=token_store_enabled,
            token_store_path=token_store_path,
            token_store_sas_setting_name=token_store_sas_setting_name,
            validate_nonce=validate_nonce,
        )

        return typing.cast(None, jsii.invoke(self, "putLogin", [value]))

    @jsii.member(jsii_name="putMicrosoftV2")
    def put_microsoft_v2(
        self,
        *,
        client_id: builtins.str,
        client_secret_setting_name: builtins.str,
        allowed_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
        login_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param client_id: The OAuth 2.0 client ID that was created for the app used for authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_id LinuxFunctionAppSlot#client_id}
        :param client_secret_setting_name: The app setting name containing the OAuth 2.0 client secret that was created for the app used for authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_secret_setting_name LinuxFunctionAppSlot#client_secret_setting_name}
        :param allowed_audiences: Specifies a list of Allowed Audiences that will be requested as part of Microsoft Sign-In authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#allowed_audiences LinuxFunctionAppSlot#allowed_audiences}
        :param login_scopes: The list of Login scopes that will be requested as part of Microsoft Account authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#login_scopes LinuxFunctionAppSlot#login_scopes}
        '''
        value = LinuxFunctionAppSlotAuthSettingsV2MicrosoftV2(
            client_id=client_id,
            client_secret_setting_name=client_secret_setting_name,
            allowed_audiences=allowed_audiences,
            login_scopes=login_scopes,
        )

        return typing.cast(None, jsii.invoke(self, "putMicrosoftV2", [value]))

    @jsii.member(jsii_name="putTwitterV2")
    def put_twitter_v2(
        self,
        *,
        consumer_key: builtins.str,
        consumer_secret_setting_name: builtins.str,
    ) -> None:
        '''
        :param consumer_key: The OAuth 1.0a consumer key of the Twitter application used for sign-in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#consumer_key LinuxFunctionAppSlot#consumer_key}
        :param consumer_secret_setting_name: The app setting name that contains the OAuth 1.0a consumer secret of the Twitter application used for sign-in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#consumer_secret_setting_name LinuxFunctionAppSlot#consumer_secret_setting_name}
        '''
        value = LinuxFunctionAppSlotAuthSettingsV2TwitterV2(
            consumer_key=consumer_key,
            consumer_secret_setting_name=consumer_secret_setting_name,
        )

        return typing.cast(None, jsii.invoke(self, "putTwitterV2", [value]))

    @jsii.member(jsii_name="resetActiveDirectoryV2")
    def reset_active_directory_v2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActiveDirectoryV2", []))

    @jsii.member(jsii_name="resetAppleV2")
    def reset_apple_v2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppleV2", []))

    @jsii.member(jsii_name="resetAuthEnabled")
    def reset_auth_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthEnabled", []))

    @jsii.member(jsii_name="resetAzureStaticWebAppV2")
    def reset_azure_static_web_app_v2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureStaticWebAppV2", []))

    @jsii.member(jsii_name="resetConfigFilePath")
    def reset_config_file_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigFilePath", []))

    @jsii.member(jsii_name="resetCustomOidcV2")
    def reset_custom_oidc_v2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomOidcV2", []))

    @jsii.member(jsii_name="resetDefaultProvider")
    def reset_default_provider(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultProvider", []))

    @jsii.member(jsii_name="resetExcludedPaths")
    def reset_excluded_paths(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExcludedPaths", []))

    @jsii.member(jsii_name="resetFacebookV2")
    def reset_facebook_v2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFacebookV2", []))

    @jsii.member(jsii_name="resetForwardProxyConvention")
    def reset_forward_proxy_convention(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardProxyConvention", []))

    @jsii.member(jsii_name="resetForwardProxyCustomHostHeaderName")
    def reset_forward_proxy_custom_host_header_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardProxyCustomHostHeaderName", []))

    @jsii.member(jsii_name="resetForwardProxyCustomSchemeHeaderName")
    def reset_forward_proxy_custom_scheme_header_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetForwardProxyCustomSchemeHeaderName", []))

    @jsii.member(jsii_name="resetGithubV2")
    def reset_github_v2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGithubV2", []))

    @jsii.member(jsii_name="resetGoogleV2")
    def reset_google_v2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGoogleV2", []))

    @jsii.member(jsii_name="resetHttpRouteApiPrefix")
    def reset_http_route_api_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpRouteApiPrefix", []))

    @jsii.member(jsii_name="resetMicrosoftV2")
    def reset_microsoft_v2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMicrosoftV2", []))

    @jsii.member(jsii_name="resetRequireAuthentication")
    def reset_require_authentication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireAuthentication", []))

    @jsii.member(jsii_name="resetRequireHttps")
    def reset_require_https(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRequireHttps", []))

    @jsii.member(jsii_name="resetRuntimeVersion")
    def reset_runtime_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntimeVersion", []))

    @jsii.member(jsii_name="resetTwitterV2")
    def reset_twitter_v2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTwitterV2", []))

    @jsii.member(jsii_name="resetUnauthenticatedAction")
    def reset_unauthenticated_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUnauthenticatedAction", []))

    @builtins.property
    @jsii.member(jsii_name="activeDirectoryV2")
    def active_directory_v2(
        self,
    ) -> LinuxFunctionAppSlotAuthSettingsV2ActiveDirectoryV2OutputReference:
        return typing.cast(LinuxFunctionAppSlotAuthSettingsV2ActiveDirectoryV2OutputReference, jsii.get(self, "activeDirectoryV2"))

    @builtins.property
    @jsii.member(jsii_name="appleV2")
    def apple_v2(self) -> LinuxFunctionAppSlotAuthSettingsV2AppleV2OutputReference:
        return typing.cast(LinuxFunctionAppSlotAuthSettingsV2AppleV2OutputReference, jsii.get(self, "appleV2"))

    @builtins.property
    @jsii.member(jsii_name="azureStaticWebAppV2")
    def azure_static_web_app_v2(
        self,
    ) -> LinuxFunctionAppSlotAuthSettingsV2AzureStaticWebAppV2OutputReference:
        return typing.cast(LinuxFunctionAppSlotAuthSettingsV2AzureStaticWebAppV2OutputReference, jsii.get(self, "azureStaticWebAppV2"))

    @builtins.property
    @jsii.member(jsii_name="customOidcV2")
    def custom_oidc_v2(self) -> LinuxFunctionAppSlotAuthSettingsV2CustomOidcV2List:
        return typing.cast(LinuxFunctionAppSlotAuthSettingsV2CustomOidcV2List, jsii.get(self, "customOidcV2"))

    @builtins.property
    @jsii.member(jsii_name="facebookV2")
    def facebook_v2(
        self,
    ) -> LinuxFunctionAppSlotAuthSettingsV2FacebookV2OutputReference:
        return typing.cast(LinuxFunctionAppSlotAuthSettingsV2FacebookV2OutputReference, jsii.get(self, "facebookV2"))

    @builtins.property
    @jsii.member(jsii_name="githubV2")
    def github_v2(self) -> LinuxFunctionAppSlotAuthSettingsV2GithubV2OutputReference:
        return typing.cast(LinuxFunctionAppSlotAuthSettingsV2GithubV2OutputReference, jsii.get(self, "githubV2"))

    @builtins.property
    @jsii.member(jsii_name="googleV2")
    def google_v2(self) -> LinuxFunctionAppSlotAuthSettingsV2GoogleV2OutputReference:
        return typing.cast(LinuxFunctionAppSlotAuthSettingsV2GoogleV2OutputReference, jsii.get(self, "googleV2"))

    @builtins.property
    @jsii.member(jsii_name="login")
    def login(self) -> LinuxFunctionAppSlotAuthSettingsV2LoginOutputReference:
        return typing.cast(LinuxFunctionAppSlotAuthSettingsV2LoginOutputReference, jsii.get(self, "login"))

    @builtins.property
    @jsii.member(jsii_name="microsoftV2")
    def microsoft_v2(
        self,
    ) -> LinuxFunctionAppSlotAuthSettingsV2MicrosoftV2OutputReference:
        return typing.cast(LinuxFunctionAppSlotAuthSettingsV2MicrosoftV2OutputReference, jsii.get(self, "microsoftV2"))

    @builtins.property
    @jsii.member(jsii_name="twitterV2")
    def twitter_v2(
        self,
    ) -> "LinuxFunctionAppSlotAuthSettingsV2TwitterV2OutputReference":
        return typing.cast("LinuxFunctionAppSlotAuthSettingsV2TwitterV2OutputReference", jsii.get(self, "twitterV2"))

    @builtins.property
    @jsii.member(jsii_name="activeDirectoryV2Input")
    def active_directory_v2_input(
        self,
    ) -> typing.Optional[LinuxFunctionAppSlotAuthSettingsV2ActiveDirectoryV2]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotAuthSettingsV2ActiveDirectoryV2], jsii.get(self, "activeDirectoryV2Input"))

    @builtins.property
    @jsii.member(jsii_name="appleV2Input")
    def apple_v2_input(
        self,
    ) -> typing.Optional[LinuxFunctionAppSlotAuthSettingsV2AppleV2]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotAuthSettingsV2AppleV2], jsii.get(self, "appleV2Input"))

    @builtins.property
    @jsii.member(jsii_name="authEnabledInput")
    def auth_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "authEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="azureStaticWebAppV2Input")
    def azure_static_web_app_v2_input(
        self,
    ) -> typing.Optional[LinuxFunctionAppSlotAuthSettingsV2AzureStaticWebAppV2]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotAuthSettingsV2AzureStaticWebAppV2], jsii.get(self, "azureStaticWebAppV2Input"))

    @builtins.property
    @jsii.member(jsii_name="configFilePathInput")
    def config_file_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configFilePathInput"))

    @builtins.property
    @jsii.member(jsii_name="customOidcV2Input")
    def custom_oidc_v2_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotAuthSettingsV2CustomOidcV2]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotAuthSettingsV2CustomOidcV2]]], jsii.get(self, "customOidcV2Input"))

    @builtins.property
    @jsii.member(jsii_name="defaultProviderInput")
    def default_provider_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="excludedPathsInput")
    def excluded_paths_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "excludedPathsInput"))

    @builtins.property
    @jsii.member(jsii_name="facebookV2Input")
    def facebook_v2_input(
        self,
    ) -> typing.Optional[LinuxFunctionAppSlotAuthSettingsV2FacebookV2]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotAuthSettingsV2FacebookV2], jsii.get(self, "facebookV2Input"))

    @builtins.property
    @jsii.member(jsii_name="forwardProxyConventionInput")
    def forward_proxy_convention_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "forwardProxyConventionInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardProxyCustomHostHeaderNameInput")
    def forward_proxy_custom_host_header_name_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "forwardProxyCustomHostHeaderNameInput"))

    @builtins.property
    @jsii.member(jsii_name="forwardProxyCustomSchemeHeaderNameInput")
    def forward_proxy_custom_scheme_header_name_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "forwardProxyCustomSchemeHeaderNameInput"))

    @builtins.property
    @jsii.member(jsii_name="githubV2Input")
    def github_v2_input(
        self,
    ) -> typing.Optional[LinuxFunctionAppSlotAuthSettingsV2GithubV2]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotAuthSettingsV2GithubV2], jsii.get(self, "githubV2Input"))

    @builtins.property
    @jsii.member(jsii_name="googleV2Input")
    def google_v2_input(
        self,
    ) -> typing.Optional[LinuxFunctionAppSlotAuthSettingsV2GoogleV2]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotAuthSettingsV2GoogleV2], jsii.get(self, "googleV2Input"))

    @builtins.property
    @jsii.member(jsii_name="httpRouteApiPrefixInput")
    def http_route_api_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpRouteApiPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="loginInput")
    def login_input(self) -> typing.Optional[LinuxFunctionAppSlotAuthSettingsV2Login]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotAuthSettingsV2Login], jsii.get(self, "loginInput"))

    @builtins.property
    @jsii.member(jsii_name="microsoftV2Input")
    def microsoft_v2_input(
        self,
    ) -> typing.Optional[LinuxFunctionAppSlotAuthSettingsV2MicrosoftV2]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotAuthSettingsV2MicrosoftV2], jsii.get(self, "microsoftV2Input"))

    @builtins.property
    @jsii.member(jsii_name="requireAuthenticationInput")
    def require_authentication_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireAuthenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="requireHttpsInput")
    def require_https_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "requireHttpsInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeVersionInput")
    def runtime_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="twitterV2Input")
    def twitter_v2_input(
        self,
    ) -> typing.Optional["LinuxFunctionAppSlotAuthSettingsV2TwitterV2"]:
        return typing.cast(typing.Optional["LinuxFunctionAppSlotAuthSettingsV2TwitterV2"], jsii.get(self, "twitterV2Input"))

    @builtins.property
    @jsii.member(jsii_name="unauthenticatedActionInput")
    def unauthenticated_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "unauthenticatedActionInput"))

    @builtins.property
    @jsii.member(jsii_name="authEnabled")
    def auth_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "authEnabled"))

    @auth_enabled.setter
    def auth_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76c0e1fdf62ee39a75ef969e06b644792aab058289e5f513a1040cfa072b18dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="configFilePath")
    def config_file_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "configFilePath"))

    @config_file_path.setter
    def config_file_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a68c025efa64ae1b79b611e8b5985116f6998011e0e55292af243be14475dc2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configFilePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultProvider")
    def default_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultProvider"))

    @default_provider.setter
    def default_provider(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f48e4b801c6a1274092d23b96607b7d52738d0beaf5c252cb519c50969b05232)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultProvider", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludedPaths")
    def excluded_paths(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedPaths"))

    @excluded_paths.setter
    def excluded_paths(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ec885632db3456eb87070014dab97712699d43ffc46dc9ab8872ff2173324dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedPaths", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forwardProxyConvention")
    def forward_proxy_convention(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forwardProxyConvention"))

    @forward_proxy_convention.setter
    def forward_proxy_convention(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91c6841172963c6787db0f6552229889f868e7ced6000e632d5465088e220e6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardProxyConvention", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forwardProxyCustomHostHeaderName")
    def forward_proxy_custom_host_header_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forwardProxyCustomHostHeaderName"))

    @forward_proxy_custom_host_header_name.setter
    def forward_proxy_custom_host_header_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af83dad42a15c7cf8ed458846421451a2a0b021c506a5f9b04f55ee664f1bcb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardProxyCustomHostHeaderName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forwardProxyCustomSchemeHeaderName")
    def forward_proxy_custom_scheme_header_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forwardProxyCustomSchemeHeaderName"))

    @forward_proxy_custom_scheme_header_name.setter
    def forward_proxy_custom_scheme_header_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d21a03f1b778d20b46f6c5e8c1bf72967e4b638e89298ba1259ba62138810df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardProxyCustomSchemeHeaderName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpRouteApiPrefix")
    def http_route_api_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpRouteApiPrefix"))

    @http_route_api_prefix.setter
    def http_route_api_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c7a574b1c4717b1837679011f9ac5e68dc620f57ad597566cf69026f4cc9973)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpRouteApiPrefix", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireAuthentication")
    def require_authentication(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireAuthentication"))

    @require_authentication.setter
    def require_authentication(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bf8720b00ba99f1113c9bade307679afb23646b089c20fb33110782ff8c90b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireAuthentication", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="requireHttps")
    def require_https(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "requireHttps"))

    @require_https.setter
    def require_https(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6adec2135f2b906f858de42996b962b6be8993dae0b106dda4cdc76f01ca3cc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireHttps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeVersion")
    def runtime_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeVersion"))

    @runtime_version.setter
    def runtime_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d61557b573bb2a8e18edea93e7af69403691e3ea2a9443af282a446b309bb92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unauthenticatedAction")
    def unauthenticated_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unauthenticatedAction"))

    @unauthenticated_action.setter
    def unauthenticated_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d67a8bbaed80c3c47f94577c5d8bb48a2f2585898a4a1a5d6e8b2701f2c5ecf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unauthenticatedAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LinuxFunctionAppSlotAuthSettingsV2]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotAuthSettingsV2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LinuxFunctionAppSlotAuthSettingsV2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cd42745f0fbabf321fefbc6f753c05d3138fbacb1d1eadfe3b60bb9b0dc411b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsV2TwitterV2",
    jsii_struct_bases=[],
    name_mapping={
        "consumer_key": "consumerKey",
        "consumer_secret_setting_name": "consumerSecretSettingName",
    },
)
class LinuxFunctionAppSlotAuthSettingsV2TwitterV2:
    def __init__(
        self,
        *,
        consumer_key: builtins.str,
        consumer_secret_setting_name: builtins.str,
    ) -> None:
        '''
        :param consumer_key: The OAuth 1.0a consumer key of the Twitter application used for sign-in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#consumer_key LinuxFunctionAppSlot#consumer_key}
        :param consumer_secret_setting_name: The app setting name that contains the OAuth 1.0a consumer secret of the Twitter application used for sign-in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#consumer_secret_setting_name LinuxFunctionAppSlot#consumer_secret_setting_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8795928db759ec5709c95b470ee839c718834a2f802b8c298aed259341d28351)
            check_type(argname="argument consumer_key", value=consumer_key, expected_type=type_hints["consumer_key"])
            check_type(argname="argument consumer_secret_setting_name", value=consumer_secret_setting_name, expected_type=type_hints["consumer_secret_setting_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "consumer_key": consumer_key,
            "consumer_secret_setting_name": consumer_secret_setting_name,
        }

    @builtins.property
    def consumer_key(self) -> builtins.str:
        '''The OAuth 1.0a consumer key of the Twitter application used for sign-in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#consumer_key LinuxFunctionAppSlot#consumer_key}
        '''
        result = self._values.get("consumer_key")
        assert result is not None, "Required property 'consumer_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def consumer_secret_setting_name(self) -> builtins.str:
        '''The app setting name that contains the OAuth 1.0a consumer secret of the Twitter application used for sign-in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#consumer_secret_setting_name LinuxFunctionAppSlot#consumer_secret_setting_name}
        '''
        result = self._values.get("consumer_secret_setting_name")
        assert result is not None, "Required property 'consumer_secret_setting_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotAuthSettingsV2TwitterV2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LinuxFunctionAppSlotAuthSettingsV2TwitterV2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotAuthSettingsV2TwitterV2OutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebdfe919a25fc14052dabe8aae97fdd66e7923b06cc8d00a956c29d0ca766609)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="consumerKeyInput")
    def consumer_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumerKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerSecretSettingNameInput")
    def consumer_secret_setting_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "consumerSecretSettingNameInput"))

    @builtins.property
    @jsii.member(jsii_name="consumerKey")
    def consumer_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerKey"))

    @consumer_key.setter
    def consumer_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc6f3d1985f808a0a8da3de196732a02ba32e857746c6f9c0425ac6f91d776e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="consumerSecretSettingName")
    def consumer_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerSecretSettingName"))

    @consumer_secret_setting_name.setter
    def consumer_secret_setting_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55a7b20552ec01b5facdea8cf560aa5777f180267e5ecbef5937e2df5ee7160f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerSecretSettingName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LinuxFunctionAppSlotAuthSettingsV2TwitterV2]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotAuthSettingsV2TwitterV2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LinuxFunctionAppSlotAuthSettingsV2TwitterV2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a686c3782f4a64b8212403c9f0b6ef51bdbc738429be726432e7054ea13a06f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotBackup",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "schedule": "schedule",
        "storage_account_url": "storageAccountUrl",
        "enabled": "enabled",
    },
)
class LinuxFunctionAppSlotBackup:
    def __init__(
        self,
        *,
        name: builtins.str,
        schedule: typing.Union["LinuxFunctionAppSlotBackupSchedule", typing.Dict[builtins.str, typing.Any]],
        storage_account_url: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param name: The name which should be used for this Backup. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#name LinuxFunctionAppSlot#name}
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#schedule LinuxFunctionAppSlot#schedule}
        :param storage_account_url: The SAS URL to the container. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#storage_account_url LinuxFunctionAppSlot#storage_account_url}
        :param enabled: Should this backup job be enabled? Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#enabled LinuxFunctionAppSlot#enabled}
        '''
        if isinstance(schedule, dict):
            schedule = LinuxFunctionAppSlotBackupSchedule(**schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c6f028be2e265796d2f785796ccd7138e23edcb666c1468eb47124542bd60d0)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument storage_account_url", value=storage_account_url, expected_type=type_hints["storage_account_url"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "schedule": schedule,
            "storage_account_url": storage_account_url,
        }
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def name(self) -> builtins.str:
        '''The name which should be used for this Backup.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#name LinuxFunctionAppSlot#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schedule(self) -> "LinuxFunctionAppSlotBackupSchedule":
        '''schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#schedule LinuxFunctionAppSlot#schedule}
        '''
        result = self._values.get("schedule")
        assert result is not None, "Required property 'schedule' is missing"
        return typing.cast("LinuxFunctionAppSlotBackupSchedule", result)

    @builtins.property
    def storage_account_url(self) -> builtins.str:
        '''The SAS URL to the container.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#storage_account_url LinuxFunctionAppSlot#storage_account_url}
        '''
        result = self._values.get("storage_account_url")
        assert result is not None, "Required property 'storage_account_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should this backup job be enabled?

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#enabled LinuxFunctionAppSlot#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotBackup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LinuxFunctionAppSlotBackupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotBackupOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f2cdc2d602148816f08e1455c424ade888fd4f243b99ad5b6599e3eb92ff733)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSchedule")
    def put_schedule(
        self,
        *,
        frequency_interval: jsii.Number,
        frequency_unit: builtins.str,
        keep_at_least_one_backup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retention_period_days: typing.Optional[jsii.Number] = None,
        start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param frequency_interval: How often the backup should be executed (e.g. for weekly backup, this should be set to ``7`` and ``frequency_unit`` should be set to ``Day``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#frequency_interval LinuxFunctionAppSlot#frequency_interval}
        :param frequency_unit: The unit of time for how often the backup should take place. Possible values include: ``Day`` and ``Hour``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#frequency_unit LinuxFunctionAppSlot#frequency_unit}
        :param keep_at_least_one_backup: Should the service keep at least one backup, regardless of age of backup. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#keep_at_least_one_backup LinuxFunctionAppSlot#keep_at_least_one_backup}
        :param retention_period_days: After how many days backups should be deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#retention_period_days LinuxFunctionAppSlot#retention_period_days}
        :param start_time: When the schedule should start working in RFC-3339 format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#start_time LinuxFunctionAppSlot#start_time}
        '''
        value = LinuxFunctionAppSlotBackupSchedule(
            frequency_interval=frequency_interval,
            frequency_unit=frequency_unit,
            keep_at_least_one_backup=keep_at_least_one_backup,
            retention_period_days=retention_period_days,
            start_time=start_time,
        )

        return typing.cast(None, jsii.invoke(self, "putSchedule", [value]))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> "LinuxFunctionAppSlotBackupScheduleOutputReference":
        return typing.cast("LinuxFunctionAppSlotBackupScheduleOutputReference", jsii.get(self, "schedule"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(self) -> typing.Optional["LinuxFunctionAppSlotBackupSchedule"]:
        return typing.cast(typing.Optional["LinuxFunctionAppSlotBackupSchedule"], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountUrlInput")
    def storage_account_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8714cbc08f665ae6a8975e6c6f2865af852cd61120813c6b47483809b4f5ce4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dd712ad40b0cb9776f76fc4352a7318d713c04559460f6fc9deed8ab9997d4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccountUrl")
    def storage_account_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountUrl"))

    @storage_account_url.setter
    def storage_account_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f615309a3fa5901dc155b1da48892378e8eaff3c2e03283b1e690b7d070a2ca8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LinuxFunctionAppSlotBackup]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotBackup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LinuxFunctionAppSlotBackup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3da41cb003e110e637cfdbeae082012df15250a76353dd91bfcb06a5de3be19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotBackupSchedule",
    jsii_struct_bases=[],
    name_mapping={
        "frequency_interval": "frequencyInterval",
        "frequency_unit": "frequencyUnit",
        "keep_at_least_one_backup": "keepAtLeastOneBackup",
        "retention_period_days": "retentionPeriodDays",
        "start_time": "startTime",
    },
)
class LinuxFunctionAppSlotBackupSchedule:
    def __init__(
        self,
        *,
        frequency_interval: jsii.Number,
        frequency_unit: builtins.str,
        keep_at_least_one_backup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        retention_period_days: typing.Optional[jsii.Number] = None,
        start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param frequency_interval: How often the backup should be executed (e.g. for weekly backup, this should be set to ``7`` and ``frequency_unit`` should be set to ``Day``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#frequency_interval LinuxFunctionAppSlot#frequency_interval}
        :param frequency_unit: The unit of time for how often the backup should take place. Possible values include: ``Day`` and ``Hour``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#frequency_unit LinuxFunctionAppSlot#frequency_unit}
        :param keep_at_least_one_backup: Should the service keep at least one backup, regardless of age of backup. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#keep_at_least_one_backup LinuxFunctionAppSlot#keep_at_least_one_backup}
        :param retention_period_days: After how many days backups should be deleted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#retention_period_days LinuxFunctionAppSlot#retention_period_days}
        :param start_time: When the schedule should start working in RFC-3339 format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#start_time LinuxFunctionAppSlot#start_time}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4813dbac238f6fb0ab27a49ec224ea22fcd28f7055e9ab4495fc41d8e926e85c)
            check_type(argname="argument frequency_interval", value=frequency_interval, expected_type=type_hints["frequency_interval"])
            check_type(argname="argument frequency_unit", value=frequency_unit, expected_type=type_hints["frequency_unit"])
            check_type(argname="argument keep_at_least_one_backup", value=keep_at_least_one_backup, expected_type=type_hints["keep_at_least_one_backup"])
            check_type(argname="argument retention_period_days", value=retention_period_days, expected_type=type_hints["retention_period_days"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "frequency_interval": frequency_interval,
            "frequency_unit": frequency_unit,
        }
        if keep_at_least_one_backup is not None:
            self._values["keep_at_least_one_backup"] = keep_at_least_one_backup
        if retention_period_days is not None:
            self._values["retention_period_days"] = retention_period_days
        if start_time is not None:
            self._values["start_time"] = start_time

    @builtins.property
    def frequency_interval(self) -> jsii.Number:
        '''How often the backup should be executed (e.g. for weekly backup, this should be set to ``7`` and ``frequency_unit`` should be set to ``Day``).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#frequency_interval LinuxFunctionAppSlot#frequency_interval}
        '''
        result = self._values.get("frequency_interval")
        assert result is not None, "Required property 'frequency_interval' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def frequency_unit(self) -> builtins.str:
        '''The unit of time for how often the backup should take place. Possible values include: ``Day`` and ``Hour``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#frequency_unit LinuxFunctionAppSlot#frequency_unit}
        '''
        result = self._values.get("frequency_unit")
        assert result is not None, "Required property 'frequency_unit' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def keep_at_least_one_backup(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the service keep at least one backup, regardless of age of backup. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#keep_at_least_one_backup LinuxFunctionAppSlot#keep_at_least_one_backup}
        '''
        result = self._values.get("keep_at_least_one_backup")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def retention_period_days(self) -> typing.Optional[jsii.Number]:
        '''After how many days backups should be deleted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#retention_period_days LinuxFunctionAppSlot#retention_period_days}
        '''
        result = self._values.get("retention_period_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''When the schedule should start working in RFC-3339 format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#start_time LinuxFunctionAppSlot#start_time}
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotBackupSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LinuxFunctionAppSlotBackupScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotBackupScheduleOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fefe40fabbe710cf7e10401e14e34bca485f34d252bd41d6ef3299bbc96a6c4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKeepAtLeastOneBackup")
    def reset_keep_at_least_one_backup(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeepAtLeastOneBackup", []))

    @jsii.member(jsii_name="resetRetentionPeriodDays")
    def reset_retention_period_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionPeriodDays", []))

    @jsii.member(jsii_name="resetStartTime")
    def reset_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTime", []))

    @builtins.property
    @jsii.member(jsii_name="lastExecutionTime")
    def last_execution_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lastExecutionTime"))

    @builtins.property
    @jsii.member(jsii_name="frequencyIntervalInput")
    def frequency_interval_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "frequencyIntervalInput"))

    @builtins.property
    @jsii.member(jsii_name="frequencyUnitInput")
    def frequency_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "frequencyUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="keepAtLeastOneBackupInput")
    def keep_at_least_one_backup_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "keepAtLeastOneBackupInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPeriodDaysInput")
    def retention_period_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionPeriodDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="frequencyInterval")
    def frequency_interval(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "frequencyInterval"))

    @frequency_interval.setter
    def frequency_interval(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63feaa1ed73183b185703b86f4aa02a1bd5c10d89f63fabd5610db6ec30a7dcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frequencyInterval", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="frequencyUnit")
    def frequency_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frequencyUnit"))

    @frequency_unit.setter
    def frequency_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8b6dab1d656d7e469ade3c5a455405e6edcb66f24ee55dabecbbd0c866c87b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frequencyUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keepAtLeastOneBackup")
    def keep_at_least_one_backup(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "keepAtLeastOneBackup"))

    @keep_at_least_one_backup.setter
    def keep_at_least_one_backup(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bece44d0692a6056c6976b4361cb9508dd2ae0b2a6b209c160809a2916e73cb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepAtLeastOneBackup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionPeriodDays")
    def retention_period_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionPeriodDays"))

    @retention_period_days.setter
    def retention_period_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bf889e65dfa171b1c5cad9fec4b60d7e79f594654042a40b3b9e57d20db918b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionPeriodDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a54f962c78ac5e679db8fad6a5376d7725d1f604eceec84bf1f9a412bd28c835)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LinuxFunctionAppSlotBackupSchedule]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotBackupSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LinuxFunctionAppSlotBackupSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0deac4dde135bb5c4f1d74b3258aa7bf7f638beb67e97fe6b12f697888b44109)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "function_app_id": "functionAppId",
        "name": "name",
        "site_config": "siteConfig",
        "app_settings": "appSettings",
        "auth_settings": "authSettings",
        "auth_settings_v2": "authSettingsV2",
        "backup": "backup",
        "builtin_logging_enabled": "builtinLoggingEnabled",
        "client_certificate_enabled": "clientCertificateEnabled",
        "client_certificate_exclusion_paths": "clientCertificateExclusionPaths",
        "client_certificate_mode": "clientCertificateMode",
        "connection_string": "connectionString",
        "content_share_force_disabled": "contentShareForceDisabled",
        "daily_memory_time_quota": "dailyMemoryTimeQuota",
        "enabled": "enabled",
        "ftp_publish_basic_authentication_enabled": "ftpPublishBasicAuthenticationEnabled",
        "functions_extension_version": "functionsExtensionVersion",
        "https_only": "httpsOnly",
        "id": "id",
        "identity": "identity",
        "key_vault_reference_identity_id": "keyVaultReferenceIdentityId",
        "public_network_access_enabled": "publicNetworkAccessEnabled",
        "service_plan_id": "servicePlanId",
        "storage_account": "storageAccount",
        "storage_account_access_key": "storageAccountAccessKey",
        "storage_account_name": "storageAccountName",
        "storage_key_vault_secret_id": "storageKeyVaultSecretId",
        "storage_uses_managed_identity": "storageUsesManagedIdentity",
        "tags": "tags",
        "timeouts": "timeouts",
        "virtual_network_backup_restore_enabled": "virtualNetworkBackupRestoreEnabled",
        "virtual_network_subnet_id": "virtualNetworkSubnetId",
        "vnet_image_pull_enabled": "vnetImagePullEnabled",
        "webdeploy_publish_basic_authentication_enabled": "webdeployPublishBasicAuthenticationEnabled",
    },
)
class LinuxFunctionAppSlotConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        function_app_id: builtins.str,
        name: builtins.str,
        site_config: typing.Union["LinuxFunctionAppSlotSiteConfig", typing.Dict[builtins.str, typing.Any]],
        app_settings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        auth_settings: typing.Optional[typing.Union[LinuxFunctionAppSlotAuthSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        auth_settings_v2: typing.Optional[typing.Union[LinuxFunctionAppSlotAuthSettingsV2, typing.Dict[builtins.str, typing.Any]]] = None,
        backup: typing.Optional[typing.Union[LinuxFunctionAppSlotBackup, typing.Dict[builtins.str, typing.Any]]] = None,
        builtin_logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_certificate_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_certificate_exclusion_paths: typing.Optional[builtins.str] = None,
        client_certificate_mode: typing.Optional[builtins.str] = None,
        connection_string: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LinuxFunctionAppSlotConnectionString", typing.Dict[builtins.str, typing.Any]]]]] = None,
        content_share_force_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        daily_memory_time_quota: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ftp_publish_basic_authentication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        functions_extension_version: typing.Optional[builtins.str] = None,
        https_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["LinuxFunctionAppSlotIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        key_vault_reference_identity_id: typing.Optional[builtins.str] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        service_plan_id: typing.Optional[builtins.str] = None,
        storage_account: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LinuxFunctionAppSlotStorageAccount", typing.Dict[builtins.str, typing.Any]]]]] = None,
        storage_account_access_key: typing.Optional[builtins.str] = None,
        storage_account_name: typing.Optional[builtins.str] = None,
        storage_key_vault_secret_id: typing.Optional[builtins.str] = None,
        storage_uses_managed_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["LinuxFunctionAppSlotTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_network_backup_restore_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        virtual_network_subnet_id: typing.Optional[builtins.str] = None,
        vnet_image_pull_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        webdeploy_publish_basic_authentication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param function_app_id: The ID of the Linux Function App this Slot is a member of. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#function_app_id LinuxFunctionAppSlot#function_app_id}
        :param name: Specifies the name of the Function App Slot. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#name LinuxFunctionAppSlot#name}
        :param site_config: site_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#site_config LinuxFunctionAppSlot#site_config}
        :param app_settings: A map of key-value pairs for `App Settings <https://docs.microsoft.com/en-us/azure/azure-functions/functions-app-settings>`_ and custom values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#app_settings LinuxFunctionAppSlot#app_settings}
        :param auth_settings: auth_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#auth_settings LinuxFunctionAppSlot#auth_settings}
        :param auth_settings_v2: auth_settings_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#auth_settings_v2 LinuxFunctionAppSlot#auth_settings_v2}
        :param backup: backup block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#backup LinuxFunctionAppSlot#backup}
        :param builtin_logging_enabled: Should built in logging be enabled. Configures ``AzureWebJobsDashboard`` app setting based on the configured storage setting. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#builtin_logging_enabled LinuxFunctionAppSlot#builtin_logging_enabled}
        :param client_certificate_enabled: Should the Function App Slot use Client Certificates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_certificate_enabled LinuxFunctionAppSlot#client_certificate_enabled}
        :param client_certificate_exclusion_paths: Paths to exclude when using client certificates, separated by ; Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_certificate_exclusion_paths LinuxFunctionAppSlot#client_certificate_exclusion_paths}
        :param client_certificate_mode: The mode of the Function App Slot's client certificates requirement for incoming requests. Possible values are ``Required``, ``Optional``, and ``OptionalInteractiveUser``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_certificate_mode LinuxFunctionAppSlot#client_certificate_mode}
        :param connection_string: connection_string block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#connection_string LinuxFunctionAppSlot#connection_string}
        :param content_share_force_disabled: Force disable the content share settings. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#content_share_force_disabled LinuxFunctionAppSlot#content_share_force_disabled}
        :param daily_memory_time_quota: The amount of memory in gigabyte-seconds that your application is allowed to consume per day. Setting this value only affects function apps in Consumption Plans. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#daily_memory_time_quota LinuxFunctionAppSlot#daily_memory_time_quota}
        :param enabled: Is the Linux Function App Slot enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#enabled LinuxFunctionAppSlot#enabled}
        :param ftp_publish_basic_authentication_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#ftp_publish_basic_authentication_enabled LinuxFunctionAppSlot#ftp_publish_basic_authentication_enabled}.
        :param functions_extension_version: The runtime version associated with the Function App Slot. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#functions_extension_version LinuxFunctionAppSlot#functions_extension_version}
        :param https_only: Can the Function App Slot only be accessed via HTTPS? Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#https_only LinuxFunctionAppSlot#https_only}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#id LinuxFunctionAppSlot#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#identity LinuxFunctionAppSlot#identity}
        :param key_vault_reference_identity_id: The User Assigned Identity to use for Key Vault access. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#key_vault_reference_identity_id LinuxFunctionAppSlot#key_vault_reference_identity_id}
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#public_network_access_enabled LinuxFunctionAppSlot#public_network_access_enabled}.
        :param service_plan_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#service_plan_id LinuxFunctionAppSlot#service_plan_id}.
        :param storage_account: storage_account block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#storage_account LinuxFunctionAppSlot#storage_account}
        :param storage_account_access_key: The access key which will be used to access the storage account for the Function App Slot. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#storage_account_access_key LinuxFunctionAppSlot#storage_account_access_key}
        :param storage_account_name: The backend storage account name which will be used by this Function App Slot. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#storage_account_name LinuxFunctionAppSlot#storage_account_name}
        :param storage_key_vault_secret_id: The Key Vault Secret ID, including version, that contains the Connection String to connect to the storage account for this Function App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#storage_key_vault_secret_id LinuxFunctionAppSlot#storage_key_vault_secret_id}
        :param storage_uses_managed_identity: Should the Function App Slot use its Managed Identity to access storage? Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#storage_uses_managed_identity LinuxFunctionAppSlot#storage_uses_managed_identity}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#tags LinuxFunctionAppSlot#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#timeouts LinuxFunctionAppSlot#timeouts}
        :param virtual_network_backup_restore_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#virtual_network_backup_restore_enabled LinuxFunctionAppSlot#virtual_network_backup_restore_enabled}.
        :param virtual_network_subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#virtual_network_subnet_id LinuxFunctionAppSlot#virtual_network_subnet_id}.
        :param vnet_image_pull_enabled: Is container image pull over virtual network enabled? Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#vnet_image_pull_enabled LinuxFunctionAppSlot#vnet_image_pull_enabled}
        :param webdeploy_publish_basic_authentication_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#webdeploy_publish_basic_authentication_enabled LinuxFunctionAppSlot#webdeploy_publish_basic_authentication_enabled}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(site_config, dict):
            site_config = LinuxFunctionAppSlotSiteConfig(**site_config)
        if isinstance(auth_settings, dict):
            auth_settings = LinuxFunctionAppSlotAuthSettings(**auth_settings)
        if isinstance(auth_settings_v2, dict):
            auth_settings_v2 = LinuxFunctionAppSlotAuthSettingsV2(**auth_settings_v2)
        if isinstance(backup, dict):
            backup = LinuxFunctionAppSlotBackup(**backup)
        if isinstance(identity, dict):
            identity = LinuxFunctionAppSlotIdentity(**identity)
        if isinstance(timeouts, dict):
            timeouts = LinuxFunctionAppSlotTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bda8efa9165dba8ca6259fec8dd31eda0f5026e0c02422ff85d9d2afbf35712a)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument function_app_id", value=function_app_id, expected_type=type_hints["function_app_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument site_config", value=site_config, expected_type=type_hints["site_config"])
            check_type(argname="argument app_settings", value=app_settings, expected_type=type_hints["app_settings"])
            check_type(argname="argument auth_settings", value=auth_settings, expected_type=type_hints["auth_settings"])
            check_type(argname="argument auth_settings_v2", value=auth_settings_v2, expected_type=type_hints["auth_settings_v2"])
            check_type(argname="argument backup", value=backup, expected_type=type_hints["backup"])
            check_type(argname="argument builtin_logging_enabled", value=builtin_logging_enabled, expected_type=type_hints["builtin_logging_enabled"])
            check_type(argname="argument client_certificate_enabled", value=client_certificate_enabled, expected_type=type_hints["client_certificate_enabled"])
            check_type(argname="argument client_certificate_exclusion_paths", value=client_certificate_exclusion_paths, expected_type=type_hints["client_certificate_exclusion_paths"])
            check_type(argname="argument client_certificate_mode", value=client_certificate_mode, expected_type=type_hints["client_certificate_mode"])
            check_type(argname="argument connection_string", value=connection_string, expected_type=type_hints["connection_string"])
            check_type(argname="argument content_share_force_disabled", value=content_share_force_disabled, expected_type=type_hints["content_share_force_disabled"])
            check_type(argname="argument daily_memory_time_quota", value=daily_memory_time_quota, expected_type=type_hints["daily_memory_time_quota"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument ftp_publish_basic_authentication_enabled", value=ftp_publish_basic_authentication_enabled, expected_type=type_hints["ftp_publish_basic_authentication_enabled"])
            check_type(argname="argument functions_extension_version", value=functions_extension_version, expected_type=type_hints["functions_extension_version"])
            check_type(argname="argument https_only", value=https_only, expected_type=type_hints["https_only"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument key_vault_reference_identity_id", value=key_vault_reference_identity_id, expected_type=type_hints["key_vault_reference_identity_id"])
            check_type(argname="argument public_network_access_enabled", value=public_network_access_enabled, expected_type=type_hints["public_network_access_enabled"])
            check_type(argname="argument service_plan_id", value=service_plan_id, expected_type=type_hints["service_plan_id"])
            check_type(argname="argument storage_account", value=storage_account, expected_type=type_hints["storage_account"])
            check_type(argname="argument storage_account_access_key", value=storage_account_access_key, expected_type=type_hints["storage_account_access_key"])
            check_type(argname="argument storage_account_name", value=storage_account_name, expected_type=type_hints["storage_account_name"])
            check_type(argname="argument storage_key_vault_secret_id", value=storage_key_vault_secret_id, expected_type=type_hints["storage_key_vault_secret_id"])
            check_type(argname="argument storage_uses_managed_identity", value=storage_uses_managed_identity, expected_type=type_hints["storage_uses_managed_identity"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument virtual_network_backup_restore_enabled", value=virtual_network_backup_restore_enabled, expected_type=type_hints["virtual_network_backup_restore_enabled"])
            check_type(argname="argument virtual_network_subnet_id", value=virtual_network_subnet_id, expected_type=type_hints["virtual_network_subnet_id"])
            check_type(argname="argument vnet_image_pull_enabled", value=vnet_image_pull_enabled, expected_type=type_hints["vnet_image_pull_enabled"])
            check_type(argname="argument webdeploy_publish_basic_authentication_enabled", value=webdeploy_publish_basic_authentication_enabled, expected_type=type_hints["webdeploy_publish_basic_authentication_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "function_app_id": function_app_id,
            "name": name,
            "site_config": site_config,
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
        if app_settings is not None:
            self._values["app_settings"] = app_settings
        if auth_settings is not None:
            self._values["auth_settings"] = auth_settings
        if auth_settings_v2 is not None:
            self._values["auth_settings_v2"] = auth_settings_v2
        if backup is not None:
            self._values["backup"] = backup
        if builtin_logging_enabled is not None:
            self._values["builtin_logging_enabled"] = builtin_logging_enabled
        if client_certificate_enabled is not None:
            self._values["client_certificate_enabled"] = client_certificate_enabled
        if client_certificate_exclusion_paths is not None:
            self._values["client_certificate_exclusion_paths"] = client_certificate_exclusion_paths
        if client_certificate_mode is not None:
            self._values["client_certificate_mode"] = client_certificate_mode
        if connection_string is not None:
            self._values["connection_string"] = connection_string
        if content_share_force_disabled is not None:
            self._values["content_share_force_disabled"] = content_share_force_disabled
        if daily_memory_time_quota is not None:
            self._values["daily_memory_time_quota"] = daily_memory_time_quota
        if enabled is not None:
            self._values["enabled"] = enabled
        if ftp_publish_basic_authentication_enabled is not None:
            self._values["ftp_publish_basic_authentication_enabled"] = ftp_publish_basic_authentication_enabled
        if functions_extension_version is not None:
            self._values["functions_extension_version"] = functions_extension_version
        if https_only is not None:
            self._values["https_only"] = https_only
        if id is not None:
            self._values["id"] = id
        if identity is not None:
            self._values["identity"] = identity
        if key_vault_reference_identity_id is not None:
            self._values["key_vault_reference_identity_id"] = key_vault_reference_identity_id
        if public_network_access_enabled is not None:
            self._values["public_network_access_enabled"] = public_network_access_enabled
        if service_plan_id is not None:
            self._values["service_plan_id"] = service_plan_id
        if storage_account is not None:
            self._values["storage_account"] = storage_account
        if storage_account_access_key is not None:
            self._values["storage_account_access_key"] = storage_account_access_key
        if storage_account_name is not None:
            self._values["storage_account_name"] = storage_account_name
        if storage_key_vault_secret_id is not None:
            self._values["storage_key_vault_secret_id"] = storage_key_vault_secret_id
        if storage_uses_managed_identity is not None:
            self._values["storage_uses_managed_identity"] = storage_uses_managed_identity
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if virtual_network_backup_restore_enabled is not None:
            self._values["virtual_network_backup_restore_enabled"] = virtual_network_backup_restore_enabled
        if virtual_network_subnet_id is not None:
            self._values["virtual_network_subnet_id"] = virtual_network_subnet_id
        if vnet_image_pull_enabled is not None:
            self._values["vnet_image_pull_enabled"] = vnet_image_pull_enabled
        if webdeploy_publish_basic_authentication_enabled is not None:
            self._values["webdeploy_publish_basic_authentication_enabled"] = webdeploy_publish_basic_authentication_enabled

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
    def function_app_id(self) -> builtins.str:
        '''The ID of the Linux Function App this Slot is a member of.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#function_app_id LinuxFunctionAppSlot#function_app_id}
        '''
        result = self._values.get("function_app_id")
        assert result is not None, "Required property 'function_app_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the name of the Function App Slot.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#name LinuxFunctionAppSlot#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def site_config(self) -> "LinuxFunctionAppSlotSiteConfig":
        '''site_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#site_config LinuxFunctionAppSlot#site_config}
        '''
        result = self._values.get("site_config")
        assert result is not None, "Required property 'site_config' is missing"
        return typing.cast("LinuxFunctionAppSlotSiteConfig", result)

    @builtins.property
    def app_settings(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of key-value pairs for `App Settings <https://docs.microsoft.com/en-us/azure/azure-functions/functions-app-settings>`_ and custom values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#app_settings LinuxFunctionAppSlot#app_settings}
        '''
        result = self._values.get("app_settings")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def auth_settings(self) -> typing.Optional[LinuxFunctionAppSlotAuthSettings]:
        '''auth_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#auth_settings LinuxFunctionAppSlot#auth_settings}
        '''
        result = self._values.get("auth_settings")
        return typing.cast(typing.Optional[LinuxFunctionAppSlotAuthSettings], result)

    @builtins.property
    def auth_settings_v2(self) -> typing.Optional[LinuxFunctionAppSlotAuthSettingsV2]:
        '''auth_settings_v2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#auth_settings_v2 LinuxFunctionAppSlot#auth_settings_v2}
        '''
        result = self._values.get("auth_settings_v2")
        return typing.cast(typing.Optional[LinuxFunctionAppSlotAuthSettingsV2], result)

    @builtins.property
    def backup(self) -> typing.Optional[LinuxFunctionAppSlotBackup]:
        '''backup block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#backup LinuxFunctionAppSlot#backup}
        '''
        result = self._values.get("backup")
        return typing.cast(typing.Optional[LinuxFunctionAppSlotBackup], result)

    @builtins.property
    def builtin_logging_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should built in logging be enabled. Configures ``AzureWebJobsDashboard`` app setting based on the configured storage setting.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#builtin_logging_enabled LinuxFunctionAppSlot#builtin_logging_enabled}
        '''
        result = self._values.get("builtin_logging_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def client_certificate_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the Function App Slot use Client Certificates.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_certificate_enabled LinuxFunctionAppSlot#client_certificate_enabled}
        '''
        result = self._values.get("client_certificate_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def client_certificate_exclusion_paths(self) -> typing.Optional[builtins.str]:
        '''Paths to exclude when using client certificates, separated by ;

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_certificate_exclusion_paths LinuxFunctionAppSlot#client_certificate_exclusion_paths}
        '''
        result = self._values.get("client_certificate_exclusion_paths")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_certificate_mode(self) -> typing.Optional[builtins.str]:
        '''The mode of the Function App Slot's client certificates requirement for incoming requests.

        Possible values are ``Required``, ``Optional``, and ``OptionalInteractiveUser``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#client_certificate_mode LinuxFunctionAppSlot#client_certificate_mode}
        '''
        result = self._values.get("client_certificate_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connection_string(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LinuxFunctionAppSlotConnectionString"]]]:
        '''connection_string block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#connection_string LinuxFunctionAppSlot#connection_string}
        '''
        result = self._values.get("connection_string")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LinuxFunctionAppSlotConnectionString"]]], result)

    @builtins.property
    def content_share_force_disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Force disable the content share settings.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#content_share_force_disabled LinuxFunctionAppSlot#content_share_force_disabled}
        '''
        result = self._values.get("content_share_force_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def daily_memory_time_quota(self) -> typing.Optional[jsii.Number]:
        '''The amount of memory in gigabyte-seconds that your application is allowed to consume per day.

        Setting this value only affects function apps in Consumption Plans.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#daily_memory_time_quota LinuxFunctionAppSlot#daily_memory_time_quota}
        '''
        result = self._values.get("daily_memory_time_quota")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Is the Linux Function App Slot enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#enabled LinuxFunctionAppSlot#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ftp_publish_basic_authentication_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#ftp_publish_basic_authentication_enabled LinuxFunctionAppSlot#ftp_publish_basic_authentication_enabled}.'''
        result = self._values.get("ftp_publish_basic_authentication_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def functions_extension_version(self) -> typing.Optional[builtins.str]:
        '''The runtime version associated with the Function App Slot.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#functions_extension_version LinuxFunctionAppSlot#functions_extension_version}
        '''
        result = self._values.get("functions_extension_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def https_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Can the Function App Slot only be accessed via HTTPS?

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#https_only LinuxFunctionAppSlot#https_only}
        '''
        result = self._values.get("https_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#id LinuxFunctionAppSlot#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(self) -> typing.Optional["LinuxFunctionAppSlotIdentity"]:
        '''identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#identity LinuxFunctionAppSlot#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional["LinuxFunctionAppSlotIdentity"], result)

    @builtins.property
    def key_vault_reference_identity_id(self) -> typing.Optional[builtins.str]:
        '''The User Assigned Identity to use for Key Vault access.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#key_vault_reference_identity_id LinuxFunctionAppSlot#key_vault_reference_identity_id}
        '''
        result = self._values.get("key_vault_reference_identity_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_network_access_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#public_network_access_enabled LinuxFunctionAppSlot#public_network_access_enabled}.'''
        result = self._values.get("public_network_access_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def service_plan_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#service_plan_id LinuxFunctionAppSlot#service_plan_id}.'''
        result = self._values.get("service_plan_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_account(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LinuxFunctionAppSlotStorageAccount"]]]:
        '''storage_account block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#storage_account LinuxFunctionAppSlot#storage_account}
        '''
        result = self._values.get("storage_account")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LinuxFunctionAppSlotStorageAccount"]]], result)

    @builtins.property
    def storage_account_access_key(self) -> typing.Optional[builtins.str]:
        '''The access key which will be used to access the storage account for the Function App Slot.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#storage_account_access_key LinuxFunctionAppSlot#storage_account_access_key}
        '''
        result = self._values.get("storage_account_access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_account_name(self) -> typing.Optional[builtins.str]:
        '''The backend storage account name which will be used by this Function App Slot.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#storage_account_name LinuxFunctionAppSlot#storage_account_name}
        '''
        result = self._values.get("storage_account_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_key_vault_secret_id(self) -> typing.Optional[builtins.str]:
        '''The Key Vault Secret ID, including version, that contains the Connection String to connect to the storage account for this Function App.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#storage_key_vault_secret_id LinuxFunctionAppSlot#storage_key_vault_secret_id}
        '''
        result = self._values.get("storage_key_vault_secret_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_uses_managed_identity(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the Function App Slot use its Managed Identity to access storage?

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#storage_uses_managed_identity LinuxFunctionAppSlot#storage_uses_managed_identity}
        '''
        result = self._values.get("storage_uses_managed_identity")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#tags LinuxFunctionAppSlot#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["LinuxFunctionAppSlotTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#timeouts LinuxFunctionAppSlot#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["LinuxFunctionAppSlotTimeouts"], result)

    @builtins.property
    def virtual_network_backup_restore_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#virtual_network_backup_restore_enabled LinuxFunctionAppSlot#virtual_network_backup_restore_enabled}.'''
        result = self._values.get("virtual_network_backup_restore_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def virtual_network_subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#virtual_network_subnet_id LinuxFunctionAppSlot#virtual_network_subnet_id}.'''
        result = self._values.get("virtual_network_subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vnet_image_pull_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Is container image pull over virtual network enabled? Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#vnet_image_pull_enabled LinuxFunctionAppSlot#vnet_image_pull_enabled}
        '''
        result = self._values.get("vnet_image_pull_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def webdeploy_publish_basic_authentication_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#webdeploy_publish_basic_authentication_enabled LinuxFunctionAppSlot#webdeploy_publish_basic_authentication_enabled}.'''
        result = self._values.get("webdeploy_publish_basic_authentication_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotConnectionString",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type", "value": "value"},
)
class LinuxFunctionAppSlotConnectionString:
    def __init__(
        self,
        *,
        name: builtins.str,
        type: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param name: The name which should be used for this Connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#name LinuxFunctionAppSlot#name}
        :param type: Type of database. Possible values include: ``MySQL``, ``SQLServer``, ``SQLAzure``, ``Custom``, ``NotificationHub``, ``ServiceBus``, ``EventHub``, ``APIHub``, ``DocDb``, ``RedisCache``, and ``PostgreSQL``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#type LinuxFunctionAppSlot#type}
        :param value: The connection string value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#value LinuxFunctionAppSlot#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6f1da3fc01434d0be952b1f3905cc271e3e25491041f2bb31b33c1b86a747e9)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "type": type,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''The name which should be used for this Connection.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#name LinuxFunctionAppSlot#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Type of database. Possible values include: ``MySQL``, ``SQLServer``, ``SQLAzure``, ``Custom``, ``NotificationHub``, ``ServiceBus``, ``EventHub``, ``APIHub``, ``DocDb``, ``RedisCache``, and ``PostgreSQL``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#type LinuxFunctionAppSlot#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The connection string value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#value LinuxFunctionAppSlot#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotConnectionString(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LinuxFunctionAppSlotConnectionStringList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotConnectionStringList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__975cf779431599e2e4d99ef98c058b6fa82d43441c5c570fca23d6c7b182a8c6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LinuxFunctionAppSlotConnectionStringOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bdfa15a851d9a8d01037e60326c5595b67579026ca71d301da9c4403fbd43c6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LinuxFunctionAppSlotConnectionStringOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09f4742f521cebaad6848411e20b4c60e4412613ccb53f54b17593e6ecee3a49)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a19602174cc96aa33e1093e59176718c4a60bf1fc550e34df9faa985715f81ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cce6ef9f91e931442ac64e28ea874fff1ba209cc04831c5934958168979d3c05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotConnectionString]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotConnectionString]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotConnectionString]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e190d1cb8cd5d72eabe4d95afd1f6257fea97487b7a7c1ed87418767623e4436)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LinuxFunctionAppSlotConnectionStringOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotConnectionStringOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bef64d05d7ac661019a872b5e53ab56f6f1e377f1c9815743598acdd38f0e8c6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d990b1657d1d29489152f1429288b85e1406fc0618dae3235710058f384ef4f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d734b788a6eada651762757dd43747c5ec0fd051abf082a885ca0e352fa11b22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93869a59debbb6c835cdae16ce7f1d9bf209b7b65e8c91526b4c949fb5cd847f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotConnectionString]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotConnectionString]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotConnectionString]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bd5870f4a927944a6c7726232f835b028db0ff10647017a44e1a84bbfbb3c50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotIdentity",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "identity_ids": "identityIds"},
)
class LinuxFunctionAppSlotIdentity:
    def __init__(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#type LinuxFunctionAppSlot#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#identity_ids LinuxFunctionAppSlot#identity_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__850409c848d4c04ee123f5385c756c3e97aeb95c0ee5cd8bafe0d2af9ca2fd8f)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if identity_ids is not None:
            self._values["identity_ids"] = identity_ids

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#type LinuxFunctionAppSlot#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#identity_ids LinuxFunctionAppSlot#identity_ids}.'''
        result = self._values.get("identity_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LinuxFunctionAppSlotIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotIdentityOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aba9ff3b33d9bb1ae7b1aba9a645056ac54dca8bd65051a3a86331494baab1e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetIdentityIds")
    def reset_identity_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentityIds", []))

    @builtins.property
    @jsii.member(jsii_name="principalId")
    def principal_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "principalId"))

    @builtins.property
    @jsii.member(jsii_name="tenantId")
    def tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantId"))

    @builtins.property
    @jsii.member(jsii_name="identityIdsInput")
    def identity_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "identityIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="identityIds")
    def identity_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "identityIds"))

    @identity_ids.setter
    def identity_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9d62145ca2249ce04acdcd43aead3e5edc9f45cb04441dbbc2413978cfa283b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__326dd24997085ef2ee1ed791c816d5328feef53b3ef15748ee9e2662f81c9cd2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LinuxFunctionAppSlotIdentity]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LinuxFunctionAppSlotIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43bad7647155ed0e396d21f84100218c9a73c48647303393762576375057c2da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotSiteConfig",
    jsii_struct_bases=[],
    name_mapping={
        "always_on": "alwaysOn",
        "api_definition_url": "apiDefinitionUrl",
        "api_management_api_id": "apiManagementApiId",
        "app_command_line": "appCommandLine",
        "application_insights_connection_string": "applicationInsightsConnectionString",
        "application_insights_key": "applicationInsightsKey",
        "application_stack": "applicationStack",
        "app_scale_limit": "appScaleLimit",
        "app_service_logs": "appServiceLogs",
        "auto_swap_slot_name": "autoSwapSlotName",
        "container_registry_managed_identity_client_id": "containerRegistryManagedIdentityClientId",
        "container_registry_use_managed_identity": "containerRegistryUseManagedIdentity",
        "cors": "cors",
        "default_documents": "defaultDocuments",
        "elastic_instance_minimum": "elasticInstanceMinimum",
        "ftps_state": "ftpsState",
        "health_check_eviction_time_in_min": "healthCheckEvictionTimeInMin",
        "health_check_path": "healthCheckPath",
        "http2_enabled": "http2Enabled",
        "ip_restriction": "ipRestriction",
        "ip_restriction_default_action": "ipRestrictionDefaultAction",
        "load_balancing_mode": "loadBalancingMode",
        "managed_pipeline_mode": "managedPipelineMode",
        "minimum_tls_version": "minimumTlsVersion",
        "pre_warmed_instance_count": "preWarmedInstanceCount",
        "remote_debugging_enabled": "remoteDebuggingEnabled",
        "remote_debugging_version": "remoteDebuggingVersion",
        "runtime_scale_monitoring_enabled": "runtimeScaleMonitoringEnabled",
        "scm_ip_restriction": "scmIpRestriction",
        "scm_ip_restriction_default_action": "scmIpRestrictionDefaultAction",
        "scm_minimum_tls_version": "scmMinimumTlsVersion",
        "scm_use_main_ip_restriction": "scmUseMainIpRestriction",
        "use32_bit_worker": "use32BitWorker",
        "vnet_route_all_enabled": "vnetRouteAllEnabled",
        "websockets_enabled": "websocketsEnabled",
        "worker_count": "workerCount",
    },
)
class LinuxFunctionAppSlotSiteConfig:
    def __init__(
        self,
        *,
        always_on: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        api_definition_url: typing.Optional[builtins.str] = None,
        api_management_api_id: typing.Optional[builtins.str] = None,
        app_command_line: typing.Optional[builtins.str] = None,
        application_insights_connection_string: typing.Optional[builtins.str] = None,
        application_insights_key: typing.Optional[builtins.str] = None,
        application_stack: typing.Optional[typing.Union["LinuxFunctionAppSlotSiteConfigApplicationStack", typing.Dict[builtins.str, typing.Any]]] = None,
        app_scale_limit: typing.Optional[jsii.Number] = None,
        app_service_logs: typing.Optional[typing.Union["LinuxFunctionAppSlotSiteConfigAppServiceLogs", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_swap_slot_name: typing.Optional[builtins.str] = None,
        container_registry_managed_identity_client_id: typing.Optional[builtins.str] = None,
        container_registry_use_managed_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cors: typing.Optional[typing.Union["LinuxFunctionAppSlotSiteConfigCors", typing.Dict[builtins.str, typing.Any]]] = None,
        default_documents: typing.Optional[typing.Sequence[builtins.str]] = None,
        elastic_instance_minimum: typing.Optional[jsii.Number] = None,
        ftps_state: typing.Optional[builtins.str] = None,
        health_check_eviction_time_in_min: typing.Optional[jsii.Number] = None,
        health_check_path: typing.Optional[builtins.str] = None,
        http2_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ip_restriction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LinuxFunctionAppSlotSiteConfigIpRestriction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ip_restriction_default_action: typing.Optional[builtins.str] = None,
        load_balancing_mode: typing.Optional[builtins.str] = None,
        managed_pipeline_mode: typing.Optional[builtins.str] = None,
        minimum_tls_version: typing.Optional[builtins.str] = None,
        pre_warmed_instance_count: typing.Optional[jsii.Number] = None,
        remote_debugging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        remote_debugging_version: typing.Optional[builtins.str] = None,
        runtime_scale_monitoring_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        scm_ip_restriction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LinuxFunctionAppSlotSiteConfigScmIpRestriction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        scm_ip_restriction_default_action: typing.Optional[builtins.str] = None,
        scm_minimum_tls_version: typing.Optional[builtins.str] = None,
        scm_use_main_ip_restriction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use32_bit_worker: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vnet_route_all_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        websockets_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        worker_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param always_on: If this Linux Web App is Always On enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#always_on LinuxFunctionAppSlot#always_on}
        :param api_definition_url: The URL of the API definition that describes this Linux Function App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#api_definition_url LinuxFunctionAppSlot#api_definition_url}
        :param api_management_api_id: The ID of the API Management API for this Linux Function App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#api_management_api_id LinuxFunctionAppSlot#api_management_api_id}
        :param app_command_line: The program and any arguments used to launch this app via the command line. (Example ``node myapp.js``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#app_command_line LinuxFunctionAppSlot#app_command_line}
        :param application_insights_connection_string: The Connection String for linking the Linux Function App to Application Insights. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#application_insights_connection_string LinuxFunctionAppSlot#application_insights_connection_string}
        :param application_insights_key: The Instrumentation Key for connecting the Linux Function App to Application Insights. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#application_insights_key LinuxFunctionAppSlot#application_insights_key}
        :param application_stack: application_stack block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#application_stack LinuxFunctionAppSlot#application_stack}
        :param app_scale_limit: The number of workers this function app can scale out to. Only applicable to apps on the Consumption and Premium plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#app_scale_limit LinuxFunctionAppSlot#app_scale_limit}
        :param app_service_logs: app_service_logs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#app_service_logs LinuxFunctionAppSlot#app_service_logs}
        :param auto_swap_slot_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#auto_swap_slot_name LinuxFunctionAppSlot#auto_swap_slot_name}.
        :param container_registry_managed_identity_client_id: The Client ID of the Managed Service Identity to use for connections to the Azure Container Registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#container_registry_managed_identity_client_id LinuxFunctionAppSlot#container_registry_managed_identity_client_id}
        :param container_registry_use_managed_identity: Should connections for Azure Container Registry use Managed Identity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#container_registry_use_managed_identity LinuxFunctionAppSlot#container_registry_use_managed_identity}
        :param cors: cors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#cors LinuxFunctionAppSlot#cors}
        :param default_documents: Specifies a list of Default Documents for the Linux Web App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#default_documents LinuxFunctionAppSlot#default_documents}
        :param elastic_instance_minimum: The number of minimum instances for this Linux Function App. Only affects apps on Elastic Premium plans. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#elastic_instance_minimum LinuxFunctionAppSlot#elastic_instance_minimum}
        :param ftps_state: State of FTP / FTPS service for this function app. Possible values include: ``AllAllowed``, ``FtpsOnly`` and ``Disabled``. Defaults to ``Disabled``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#ftps_state LinuxFunctionAppSlot#ftps_state}
        :param health_check_eviction_time_in_min: The amount of time in minutes that a node is unhealthy before being removed from the load balancer. Possible values are between ``2`` and ``10``. Defaults to ``10``. Only valid in conjunction with ``health_check_path`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#health_check_eviction_time_in_min LinuxFunctionAppSlot#health_check_eviction_time_in_min}
        :param health_check_path: The path to be checked for this function app health. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#health_check_path LinuxFunctionAppSlot#health_check_path}
        :param http2_enabled: Specifies if the http2 protocol should be enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#http2_enabled LinuxFunctionAppSlot#http2_enabled}
        :param ip_restriction: ip_restriction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#ip_restriction LinuxFunctionAppSlot#ip_restriction}
        :param ip_restriction_default_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#ip_restriction_default_action LinuxFunctionAppSlot#ip_restriction_default_action}.
        :param load_balancing_mode: The Site load balancing mode. Possible values include: ``WeightedRoundRobin``, ``LeastRequests``, ``LeastResponseTime``, ``WeightedTotalTraffic``, ``RequestHash``, ``PerSiteRoundRobin``. Defaults to ``LeastRequests`` if omitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#load_balancing_mode LinuxFunctionAppSlot#load_balancing_mode}
        :param managed_pipeline_mode: The Managed Pipeline mode. Possible values include: ``Integrated``, ``Classic``. Defaults to ``Integrated``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#managed_pipeline_mode LinuxFunctionAppSlot#managed_pipeline_mode}
        :param minimum_tls_version: The configures the minimum version of TLS required for SSL requests. Possible values include: ``1.0``, ``1.1``, ``1.2`` and ``1.3``. Defaults to ``1.2``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#minimum_tls_version LinuxFunctionAppSlot#minimum_tls_version}
        :param pre_warmed_instance_count: The number of pre-warmed instances for this function app. Only affects apps on an Elastic Premium plan. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#pre_warmed_instance_count LinuxFunctionAppSlot#pre_warmed_instance_count}
        :param remote_debugging_enabled: Should Remote Debugging be enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#remote_debugging_enabled LinuxFunctionAppSlot#remote_debugging_enabled}
        :param remote_debugging_version: The Remote Debugging Version. Currently only ``VS2022`` is supported. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#remote_debugging_version LinuxFunctionAppSlot#remote_debugging_version}
        :param runtime_scale_monitoring_enabled: Should Functions Runtime Scale Monitoring be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#runtime_scale_monitoring_enabled LinuxFunctionAppSlot#runtime_scale_monitoring_enabled}
        :param scm_ip_restriction: scm_ip_restriction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#scm_ip_restriction LinuxFunctionAppSlot#scm_ip_restriction}
        :param scm_ip_restriction_default_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#scm_ip_restriction_default_action LinuxFunctionAppSlot#scm_ip_restriction_default_action}.
        :param scm_minimum_tls_version: Configures the minimum version of TLS required for SSL requests to the SCM site Possible values include: ``1.0``, ``1.1``, ``1.2`` and ``1.3``. Defaults to ``1.2``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#scm_minimum_tls_version LinuxFunctionAppSlot#scm_minimum_tls_version}
        :param scm_use_main_ip_restriction: Should the Linux Function App ``ip_restriction`` configuration be used for the SCM also. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#scm_use_main_ip_restriction LinuxFunctionAppSlot#scm_use_main_ip_restriction}
        :param use32_bit_worker: Should the Linux Web App use a 32-bit worker. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#use_32_bit_worker LinuxFunctionAppSlot#use_32_bit_worker}
        :param vnet_route_all_enabled: Should all outbound traffic to have Virtual Network Security Groups and User Defined Routes applied? Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#vnet_route_all_enabled LinuxFunctionAppSlot#vnet_route_all_enabled}
        :param websockets_enabled: Should Web Sockets be enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#websockets_enabled LinuxFunctionAppSlot#websockets_enabled}
        :param worker_count: The number of Workers for this Linux Function App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#worker_count LinuxFunctionAppSlot#worker_count}
        '''
        if isinstance(application_stack, dict):
            application_stack = LinuxFunctionAppSlotSiteConfigApplicationStack(**application_stack)
        if isinstance(app_service_logs, dict):
            app_service_logs = LinuxFunctionAppSlotSiteConfigAppServiceLogs(**app_service_logs)
        if isinstance(cors, dict):
            cors = LinuxFunctionAppSlotSiteConfigCors(**cors)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__545635225a559a7a251e23829957a53cab882bdbbf83092dad2401a4eb3f094a)
            check_type(argname="argument always_on", value=always_on, expected_type=type_hints["always_on"])
            check_type(argname="argument api_definition_url", value=api_definition_url, expected_type=type_hints["api_definition_url"])
            check_type(argname="argument api_management_api_id", value=api_management_api_id, expected_type=type_hints["api_management_api_id"])
            check_type(argname="argument app_command_line", value=app_command_line, expected_type=type_hints["app_command_line"])
            check_type(argname="argument application_insights_connection_string", value=application_insights_connection_string, expected_type=type_hints["application_insights_connection_string"])
            check_type(argname="argument application_insights_key", value=application_insights_key, expected_type=type_hints["application_insights_key"])
            check_type(argname="argument application_stack", value=application_stack, expected_type=type_hints["application_stack"])
            check_type(argname="argument app_scale_limit", value=app_scale_limit, expected_type=type_hints["app_scale_limit"])
            check_type(argname="argument app_service_logs", value=app_service_logs, expected_type=type_hints["app_service_logs"])
            check_type(argname="argument auto_swap_slot_name", value=auto_swap_slot_name, expected_type=type_hints["auto_swap_slot_name"])
            check_type(argname="argument container_registry_managed_identity_client_id", value=container_registry_managed_identity_client_id, expected_type=type_hints["container_registry_managed_identity_client_id"])
            check_type(argname="argument container_registry_use_managed_identity", value=container_registry_use_managed_identity, expected_type=type_hints["container_registry_use_managed_identity"])
            check_type(argname="argument cors", value=cors, expected_type=type_hints["cors"])
            check_type(argname="argument default_documents", value=default_documents, expected_type=type_hints["default_documents"])
            check_type(argname="argument elastic_instance_minimum", value=elastic_instance_minimum, expected_type=type_hints["elastic_instance_minimum"])
            check_type(argname="argument ftps_state", value=ftps_state, expected_type=type_hints["ftps_state"])
            check_type(argname="argument health_check_eviction_time_in_min", value=health_check_eviction_time_in_min, expected_type=type_hints["health_check_eviction_time_in_min"])
            check_type(argname="argument health_check_path", value=health_check_path, expected_type=type_hints["health_check_path"])
            check_type(argname="argument http2_enabled", value=http2_enabled, expected_type=type_hints["http2_enabled"])
            check_type(argname="argument ip_restriction", value=ip_restriction, expected_type=type_hints["ip_restriction"])
            check_type(argname="argument ip_restriction_default_action", value=ip_restriction_default_action, expected_type=type_hints["ip_restriction_default_action"])
            check_type(argname="argument load_balancing_mode", value=load_balancing_mode, expected_type=type_hints["load_balancing_mode"])
            check_type(argname="argument managed_pipeline_mode", value=managed_pipeline_mode, expected_type=type_hints["managed_pipeline_mode"])
            check_type(argname="argument minimum_tls_version", value=minimum_tls_version, expected_type=type_hints["minimum_tls_version"])
            check_type(argname="argument pre_warmed_instance_count", value=pre_warmed_instance_count, expected_type=type_hints["pre_warmed_instance_count"])
            check_type(argname="argument remote_debugging_enabled", value=remote_debugging_enabled, expected_type=type_hints["remote_debugging_enabled"])
            check_type(argname="argument remote_debugging_version", value=remote_debugging_version, expected_type=type_hints["remote_debugging_version"])
            check_type(argname="argument runtime_scale_monitoring_enabled", value=runtime_scale_monitoring_enabled, expected_type=type_hints["runtime_scale_monitoring_enabled"])
            check_type(argname="argument scm_ip_restriction", value=scm_ip_restriction, expected_type=type_hints["scm_ip_restriction"])
            check_type(argname="argument scm_ip_restriction_default_action", value=scm_ip_restriction_default_action, expected_type=type_hints["scm_ip_restriction_default_action"])
            check_type(argname="argument scm_minimum_tls_version", value=scm_minimum_tls_version, expected_type=type_hints["scm_minimum_tls_version"])
            check_type(argname="argument scm_use_main_ip_restriction", value=scm_use_main_ip_restriction, expected_type=type_hints["scm_use_main_ip_restriction"])
            check_type(argname="argument use32_bit_worker", value=use32_bit_worker, expected_type=type_hints["use32_bit_worker"])
            check_type(argname="argument vnet_route_all_enabled", value=vnet_route_all_enabled, expected_type=type_hints["vnet_route_all_enabled"])
            check_type(argname="argument websockets_enabled", value=websockets_enabled, expected_type=type_hints["websockets_enabled"])
            check_type(argname="argument worker_count", value=worker_count, expected_type=type_hints["worker_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if always_on is not None:
            self._values["always_on"] = always_on
        if api_definition_url is not None:
            self._values["api_definition_url"] = api_definition_url
        if api_management_api_id is not None:
            self._values["api_management_api_id"] = api_management_api_id
        if app_command_line is not None:
            self._values["app_command_line"] = app_command_line
        if application_insights_connection_string is not None:
            self._values["application_insights_connection_string"] = application_insights_connection_string
        if application_insights_key is not None:
            self._values["application_insights_key"] = application_insights_key
        if application_stack is not None:
            self._values["application_stack"] = application_stack
        if app_scale_limit is not None:
            self._values["app_scale_limit"] = app_scale_limit
        if app_service_logs is not None:
            self._values["app_service_logs"] = app_service_logs
        if auto_swap_slot_name is not None:
            self._values["auto_swap_slot_name"] = auto_swap_slot_name
        if container_registry_managed_identity_client_id is not None:
            self._values["container_registry_managed_identity_client_id"] = container_registry_managed_identity_client_id
        if container_registry_use_managed_identity is not None:
            self._values["container_registry_use_managed_identity"] = container_registry_use_managed_identity
        if cors is not None:
            self._values["cors"] = cors
        if default_documents is not None:
            self._values["default_documents"] = default_documents
        if elastic_instance_minimum is not None:
            self._values["elastic_instance_minimum"] = elastic_instance_minimum
        if ftps_state is not None:
            self._values["ftps_state"] = ftps_state
        if health_check_eviction_time_in_min is not None:
            self._values["health_check_eviction_time_in_min"] = health_check_eviction_time_in_min
        if health_check_path is not None:
            self._values["health_check_path"] = health_check_path
        if http2_enabled is not None:
            self._values["http2_enabled"] = http2_enabled
        if ip_restriction is not None:
            self._values["ip_restriction"] = ip_restriction
        if ip_restriction_default_action is not None:
            self._values["ip_restriction_default_action"] = ip_restriction_default_action
        if load_balancing_mode is not None:
            self._values["load_balancing_mode"] = load_balancing_mode
        if managed_pipeline_mode is not None:
            self._values["managed_pipeline_mode"] = managed_pipeline_mode
        if minimum_tls_version is not None:
            self._values["minimum_tls_version"] = minimum_tls_version
        if pre_warmed_instance_count is not None:
            self._values["pre_warmed_instance_count"] = pre_warmed_instance_count
        if remote_debugging_enabled is not None:
            self._values["remote_debugging_enabled"] = remote_debugging_enabled
        if remote_debugging_version is not None:
            self._values["remote_debugging_version"] = remote_debugging_version
        if runtime_scale_monitoring_enabled is not None:
            self._values["runtime_scale_monitoring_enabled"] = runtime_scale_monitoring_enabled
        if scm_ip_restriction is not None:
            self._values["scm_ip_restriction"] = scm_ip_restriction
        if scm_ip_restriction_default_action is not None:
            self._values["scm_ip_restriction_default_action"] = scm_ip_restriction_default_action
        if scm_minimum_tls_version is not None:
            self._values["scm_minimum_tls_version"] = scm_minimum_tls_version
        if scm_use_main_ip_restriction is not None:
            self._values["scm_use_main_ip_restriction"] = scm_use_main_ip_restriction
        if use32_bit_worker is not None:
            self._values["use32_bit_worker"] = use32_bit_worker
        if vnet_route_all_enabled is not None:
            self._values["vnet_route_all_enabled"] = vnet_route_all_enabled
        if websockets_enabled is not None:
            self._values["websockets_enabled"] = websockets_enabled
        if worker_count is not None:
            self._values["worker_count"] = worker_count

    @builtins.property
    def always_on(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If this Linux Web App is Always On enabled. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#always_on LinuxFunctionAppSlot#always_on}
        '''
        result = self._values.get("always_on")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def api_definition_url(self) -> typing.Optional[builtins.str]:
        '''The URL of the API definition that describes this Linux Function App.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#api_definition_url LinuxFunctionAppSlot#api_definition_url}
        '''
        result = self._values.get("api_definition_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def api_management_api_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the API Management API for this Linux Function App.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#api_management_api_id LinuxFunctionAppSlot#api_management_api_id}
        '''
        result = self._values.get("api_management_api_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app_command_line(self) -> typing.Optional[builtins.str]:
        '''The program and any arguments used to launch this app via the command line. (Example ``node myapp.js``).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#app_command_line LinuxFunctionAppSlot#app_command_line}
        '''
        result = self._values.get("app_command_line")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_insights_connection_string(self) -> typing.Optional[builtins.str]:
        '''The Connection String for linking the Linux Function App to Application Insights.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#application_insights_connection_string LinuxFunctionAppSlot#application_insights_connection_string}
        '''
        result = self._values.get("application_insights_connection_string")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_insights_key(self) -> typing.Optional[builtins.str]:
        '''The Instrumentation Key for connecting the Linux Function App to Application Insights.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#application_insights_key LinuxFunctionAppSlot#application_insights_key}
        '''
        result = self._values.get("application_insights_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_stack(
        self,
    ) -> typing.Optional["LinuxFunctionAppSlotSiteConfigApplicationStack"]:
        '''application_stack block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#application_stack LinuxFunctionAppSlot#application_stack}
        '''
        result = self._values.get("application_stack")
        return typing.cast(typing.Optional["LinuxFunctionAppSlotSiteConfigApplicationStack"], result)

    @builtins.property
    def app_scale_limit(self) -> typing.Optional[jsii.Number]:
        '''The number of workers this function app can scale out to.

        Only applicable to apps on the Consumption and Premium plan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#app_scale_limit LinuxFunctionAppSlot#app_scale_limit}
        '''
        result = self._values.get("app_scale_limit")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def app_service_logs(
        self,
    ) -> typing.Optional["LinuxFunctionAppSlotSiteConfigAppServiceLogs"]:
        '''app_service_logs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#app_service_logs LinuxFunctionAppSlot#app_service_logs}
        '''
        result = self._values.get("app_service_logs")
        return typing.cast(typing.Optional["LinuxFunctionAppSlotSiteConfigAppServiceLogs"], result)

    @builtins.property
    def auto_swap_slot_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#auto_swap_slot_name LinuxFunctionAppSlot#auto_swap_slot_name}.'''
        result = self._values.get("auto_swap_slot_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_registry_managed_identity_client_id(
        self,
    ) -> typing.Optional[builtins.str]:
        '''The Client ID of the Managed Service Identity to use for connections to the Azure Container Registry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#container_registry_managed_identity_client_id LinuxFunctionAppSlot#container_registry_managed_identity_client_id}
        '''
        result = self._values.get("container_registry_managed_identity_client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_registry_use_managed_identity(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should connections for Azure Container Registry use Managed Identity.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#container_registry_use_managed_identity LinuxFunctionAppSlot#container_registry_use_managed_identity}
        '''
        result = self._values.get("container_registry_use_managed_identity")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cors(self) -> typing.Optional["LinuxFunctionAppSlotSiteConfigCors"]:
        '''cors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#cors LinuxFunctionAppSlot#cors}
        '''
        result = self._values.get("cors")
        return typing.cast(typing.Optional["LinuxFunctionAppSlotSiteConfigCors"], result)

    @builtins.property
    def default_documents(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of Default Documents for the Linux Web App.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#default_documents LinuxFunctionAppSlot#default_documents}
        '''
        result = self._values.get("default_documents")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def elastic_instance_minimum(self) -> typing.Optional[jsii.Number]:
        '''The number of minimum instances for this Linux Function App. Only affects apps on Elastic Premium plans.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#elastic_instance_minimum LinuxFunctionAppSlot#elastic_instance_minimum}
        '''
        result = self._values.get("elastic_instance_minimum")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ftps_state(self) -> typing.Optional[builtins.str]:
        '''State of FTP / FTPS service for this function app.

        Possible values include: ``AllAllowed``, ``FtpsOnly`` and ``Disabled``. Defaults to ``Disabled``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#ftps_state LinuxFunctionAppSlot#ftps_state}
        '''
        result = self._values.get("ftps_state")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_check_eviction_time_in_min(self) -> typing.Optional[jsii.Number]:
        '''The amount of time in minutes that a node is unhealthy before being removed from the load balancer.

        Possible values are between ``2`` and ``10``. Defaults to ``10``. Only valid in conjunction with ``health_check_path``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#health_check_eviction_time_in_min LinuxFunctionAppSlot#health_check_eviction_time_in_min}
        '''
        result = self._values.get("health_check_eviction_time_in_min")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def health_check_path(self) -> typing.Optional[builtins.str]:
        '''The path to be checked for this function app health.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#health_check_path LinuxFunctionAppSlot#health_check_path}
        '''
        result = self._values.get("health_check_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http2_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if the http2 protocol should be enabled. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#http2_enabled LinuxFunctionAppSlot#http2_enabled}
        '''
        result = self._values.get("http2_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ip_restriction(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LinuxFunctionAppSlotSiteConfigIpRestriction"]]]:
        '''ip_restriction block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#ip_restriction LinuxFunctionAppSlot#ip_restriction}
        '''
        result = self._values.get("ip_restriction")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LinuxFunctionAppSlotSiteConfigIpRestriction"]]], result)

    @builtins.property
    def ip_restriction_default_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#ip_restriction_default_action LinuxFunctionAppSlot#ip_restriction_default_action}.'''
        result = self._values.get("ip_restriction_default_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancing_mode(self) -> typing.Optional[builtins.str]:
        '''The Site load balancing mode. Possible values include: ``WeightedRoundRobin``, ``LeastRequests``, ``LeastResponseTime``, ``WeightedTotalTraffic``, ``RequestHash``, ``PerSiteRoundRobin``. Defaults to ``LeastRequests`` if omitted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#load_balancing_mode LinuxFunctionAppSlot#load_balancing_mode}
        '''
        result = self._values.get("load_balancing_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_pipeline_mode(self) -> typing.Optional[builtins.str]:
        '''The Managed Pipeline mode. Possible values include: ``Integrated``, ``Classic``. Defaults to ``Integrated``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#managed_pipeline_mode LinuxFunctionAppSlot#managed_pipeline_mode}
        '''
        result = self._values.get("managed_pipeline_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minimum_tls_version(self) -> typing.Optional[builtins.str]:
        '''The configures the minimum version of TLS required for SSL requests.

        Possible values include: ``1.0``, ``1.1``, ``1.2`` and ``1.3``. Defaults to ``1.2``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#minimum_tls_version LinuxFunctionAppSlot#minimum_tls_version}
        '''
        result = self._values.get("minimum_tls_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pre_warmed_instance_count(self) -> typing.Optional[jsii.Number]:
        '''The number of pre-warmed instances for this function app. Only affects apps on an Elastic Premium plan.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#pre_warmed_instance_count LinuxFunctionAppSlot#pre_warmed_instance_count}
        '''
        result = self._values.get("pre_warmed_instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def remote_debugging_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should Remote Debugging be enabled. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#remote_debugging_enabled LinuxFunctionAppSlot#remote_debugging_enabled}
        '''
        result = self._values.get("remote_debugging_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def remote_debugging_version(self) -> typing.Optional[builtins.str]:
        '''The Remote Debugging Version. Currently only ``VS2022`` is supported.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#remote_debugging_version LinuxFunctionAppSlot#remote_debugging_version}
        '''
        result = self._values.get("remote_debugging_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_scale_monitoring_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should Functions Runtime Scale Monitoring be enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#runtime_scale_monitoring_enabled LinuxFunctionAppSlot#runtime_scale_monitoring_enabled}
        '''
        result = self._values.get("runtime_scale_monitoring_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def scm_ip_restriction(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LinuxFunctionAppSlotSiteConfigScmIpRestriction"]]]:
        '''scm_ip_restriction block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#scm_ip_restriction LinuxFunctionAppSlot#scm_ip_restriction}
        '''
        result = self._values.get("scm_ip_restriction")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LinuxFunctionAppSlotSiteConfigScmIpRestriction"]]], result)

    @builtins.property
    def scm_ip_restriction_default_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#scm_ip_restriction_default_action LinuxFunctionAppSlot#scm_ip_restriction_default_action}.'''
        result = self._values.get("scm_ip_restriction_default_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scm_minimum_tls_version(self) -> typing.Optional[builtins.str]:
        '''Configures the minimum version of TLS required for SSL requests to the SCM site Possible values include: ``1.0``, ``1.1``, ``1.2`` and ``1.3``. Defaults to ``1.2``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#scm_minimum_tls_version LinuxFunctionAppSlot#scm_minimum_tls_version}
        '''
        result = self._values.get("scm_minimum_tls_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scm_use_main_ip_restriction(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the Linux Function App ``ip_restriction`` configuration be used for the SCM also.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#scm_use_main_ip_restriction LinuxFunctionAppSlot#scm_use_main_ip_restriction}
        '''
        result = self._values.get("scm_use_main_ip_restriction")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def use32_bit_worker(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the Linux Web App use a 32-bit worker.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#use_32_bit_worker LinuxFunctionAppSlot#use_32_bit_worker}
        '''
        result = self._values.get("use32_bit_worker")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def vnet_route_all_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should all outbound traffic to have Virtual Network Security Groups and User Defined Routes applied? Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#vnet_route_all_enabled LinuxFunctionAppSlot#vnet_route_all_enabled}
        '''
        result = self._values.get("vnet_route_all_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def websockets_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should Web Sockets be enabled. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#websockets_enabled LinuxFunctionAppSlot#websockets_enabled}
        '''
        result = self._values.get("websockets_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def worker_count(self) -> typing.Optional[jsii.Number]:
        '''The number of Workers for this Linux Function App.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#worker_count LinuxFunctionAppSlot#worker_count}
        '''
        result = self._values.get("worker_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotSiteConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotSiteConfigAppServiceLogs",
    jsii_struct_bases=[],
    name_mapping={
        "disk_quota_mb": "diskQuotaMb",
        "retention_period_days": "retentionPeriodDays",
    },
)
class LinuxFunctionAppSlotSiteConfigAppServiceLogs:
    def __init__(
        self,
        *,
        disk_quota_mb: typing.Optional[jsii.Number] = None,
        retention_period_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param disk_quota_mb: The amount of disk space to use for logs. Valid values are between ``25`` and ``100``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#disk_quota_mb LinuxFunctionAppSlot#disk_quota_mb}
        :param retention_period_days: The retention period for logs in days. Valid values are between ``0`` and ``99999``. Defaults to ``0`` (never delete). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#retention_period_days LinuxFunctionAppSlot#retention_period_days}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0c526c5409b5290d68e2259ca0a8cf7ab29d291bfa09cbb1ff388f1d805f457)
            check_type(argname="argument disk_quota_mb", value=disk_quota_mb, expected_type=type_hints["disk_quota_mb"])
            check_type(argname="argument retention_period_days", value=retention_period_days, expected_type=type_hints["retention_period_days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if disk_quota_mb is not None:
            self._values["disk_quota_mb"] = disk_quota_mb
        if retention_period_days is not None:
            self._values["retention_period_days"] = retention_period_days

    @builtins.property
    def disk_quota_mb(self) -> typing.Optional[jsii.Number]:
        '''The amount of disk space to use for logs. Valid values are between ``25`` and ``100``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#disk_quota_mb LinuxFunctionAppSlot#disk_quota_mb}
        '''
        result = self._values.get("disk_quota_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retention_period_days(self) -> typing.Optional[jsii.Number]:
        '''The retention period for logs in days. Valid values are between ``0`` and ``99999``. Defaults to ``0`` (never delete).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#retention_period_days LinuxFunctionAppSlot#retention_period_days}
        '''
        result = self._values.get("retention_period_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotSiteConfigAppServiceLogs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LinuxFunctionAppSlotSiteConfigAppServiceLogsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotSiteConfigAppServiceLogsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cbb1c3ca796b0239c9d08f888d679d9f1b1ab92a38d79246aedba7e2d166935)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDiskQuotaMb")
    def reset_disk_quota_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDiskQuotaMb", []))

    @jsii.member(jsii_name="resetRetentionPeriodDays")
    def reset_retention_period_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRetentionPeriodDays", []))

    @builtins.property
    @jsii.member(jsii_name="diskQuotaMbInput")
    def disk_quota_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "diskQuotaMbInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPeriodDaysInput")
    def retention_period_days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "retentionPeriodDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="diskQuotaMb")
    def disk_quota_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "diskQuotaMb"))

    @disk_quota_mb.setter
    def disk_quota_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82b4282fc5e54fcdff494f0ac99439634d151cd9638b5d4ed5956873ddbb4d96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskQuotaMb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionPeriodDays")
    def retention_period_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionPeriodDays"))

    @retention_period_days.setter
    def retention_period_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cdbe6a0515e6e3b8762478352a5c4e274e88a697a9bbf4bb7a44794f187c313)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionPeriodDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LinuxFunctionAppSlotSiteConfigAppServiceLogs]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotSiteConfigAppServiceLogs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LinuxFunctionAppSlotSiteConfigAppServiceLogs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee188e20fbcb3f570dcf8d80533d66015a798722a1254f0f58b9e107a15cb49c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotSiteConfigApplicationStack",
    jsii_struct_bases=[],
    name_mapping={
        "docker": "docker",
        "dotnet_version": "dotnetVersion",
        "java_version": "javaVersion",
        "node_version": "nodeVersion",
        "powershell_core_version": "powershellCoreVersion",
        "python_version": "pythonVersion",
        "use_custom_runtime": "useCustomRuntime",
        "use_dotnet_isolated_runtime": "useDotnetIsolatedRuntime",
    },
)
class LinuxFunctionAppSlotSiteConfigApplicationStack:
    def __init__(
        self,
        *,
        docker: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LinuxFunctionAppSlotSiteConfigApplicationStackDocker", typing.Dict[builtins.str, typing.Any]]]]] = None,
        dotnet_version: typing.Optional[builtins.str] = None,
        java_version: typing.Optional[builtins.str] = None,
        node_version: typing.Optional[builtins.str] = None,
        powershell_core_version: typing.Optional[builtins.str] = None,
        python_version: typing.Optional[builtins.str] = None,
        use_custom_runtime: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_dotnet_isolated_runtime: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param docker: docker block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#docker LinuxFunctionAppSlot#docker}
        :param dotnet_version: The version of .Net. Possible values are ``3.1``, ``6.0``, ``7.0``, ``8.0`` and ``9.0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#dotnet_version LinuxFunctionAppSlot#dotnet_version}
        :param java_version: The version of Java to use. Possible values are ``8``, ``11``, ``17``, and ``21``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#java_version LinuxFunctionAppSlot#java_version}
        :param node_version: The version of Node to use. Possible values include ``12``, ``14``, ``16``, ``18``, ``20`` and ``22``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#node_version LinuxFunctionAppSlot#node_version}
        :param powershell_core_version: The version of PowerShell Core to use. Possibles values are ``7``, ``7.2``, and ``7.4``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#powershell_core_version LinuxFunctionAppSlot#powershell_core_version}
        :param python_version: The version of Python to use. Possible values include ``3.13``, ``3.12``, ``3.11``, ``3.10``, ``3.9``, ``3.8``, and ``3.7``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#python_version LinuxFunctionAppSlot#python_version}
        :param use_custom_runtime: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#use_custom_runtime LinuxFunctionAppSlot#use_custom_runtime}.
        :param use_dotnet_isolated_runtime: Should the DotNet process use an isolated runtime. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#use_dotnet_isolated_runtime LinuxFunctionAppSlot#use_dotnet_isolated_runtime}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abecaab36337c7aef22da00918872ffc6cc9ff7b632dc7995c6a2b602bcc6d6d)
            check_type(argname="argument docker", value=docker, expected_type=type_hints["docker"])
            check_type(argname="argument dotnet_version", value=dotnet_version, expected_type=type_hints["dotnet_version"])
            check_type(argname="argument java_version", value=java_version, expected_type=type_hints["java_version"])
            check_type(argname="argument node_version", value=node_version, expected_type=type_hints["node_version"])
            check_type(argname="argument powershell_core_version", value=powershell_core_version, expected_type=type_hints["powershell_core_version"])
            check_type(argname="argument python_version", value=python_version, expected_type=type_hints["python_version"])
            check_type(argname="argument use_custom_runtime", value=use_custom_runtime, expected_type=type_hints["use_custom_runtime"])
            check_type(argname="argument use_dotnet_isolated_runtime", value=use_dotnet_isolated_runtime, expected_type=type_hints["use_dotnet_isolated_runtime"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if docker is not None:
            self._values["docker"] = docker
        if dotnet_version is not None:
            self._values["dotnet_version"] = dotnet_version
        if java_version is not None:
            self._values["java_version"] = java_version
        if node_version is not None:
            self._values["node_version"] = node_version
        if powershell_core_version is not None:
            self._values["powershell_core_version"] = powershell_core_version
        if python_version is not None:
            self._values["python_version"] = python_version
        if use_custom_runtime is not None:
            self._values["use_custom_runtime"] = use_custom_runtime
        if use_dotnet_isolated_runtime is not None:
            self._values["use_dotnet_isolated_runtime"] = use_dotnet_isolated_runtime

    @builtins.property
    def docker(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LinuxFunctionAppSlotSiteConfigApplicationStackDocker"]]]:
        '''docker block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#docker LinuxFunctionAppSlot#docker}
        '''
        result = self._values.get("docker")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LinuxFunctionAppSlotSiteConfigApplicationStackDocker"]]], result)

    @builtins.property
    def dotnet_version(self) -> typing.Optional[builtins.str]:
        '''The version of .Net. Possible values are ``3.1``, ``6.0``, ``7.0``, ``8.0`` and ``9.0``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#dotnet_version LinuxFunctionAppSlot#dotnet_version}
        '''
        result = self._values.get("dotnet_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def java_version(self) -> typing.Optional[builtins.str]:
        '''The version of Java to use. Possible values are ``8``, ``11``, ``17``, and ``21``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#java_version LinuxFunctionAppSlot#java_version}
        '''
        result = self._values.get("java_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def node_version(self) -> typing.Optional[builtins.str]:
        '''The version of Node to use. Possible values include ``12``, ``14``, ``16``, ``18``, ``20`` and ``22``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#node_version LinuxFunctionAppSlot#node_version}
        '''
        result = self._values.get("node_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def powershell_core_version(self) -> typing.Optional[builtins.str]:
        '''The version of PowerShell Core to use. Possibles values are ``7``, ``7.2``, and ``7.4``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#powershell_core_version LinuxFunctionAppSlot#powershell_core_version}
        '''
        result = self._values.get("powershell_core_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def python_version(self) -> typing.Optional[builtins.str]:
        '''The version of Python to use. Possible values include ``3.13``, ``3.12``, ``3.11``, ``3.10``, ``3.9``, ``3.8``, and ``3.7``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#python_version LinuxFunctionAppSlot#python_version}
        '''
        result = self._values.get("python_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_custom_runtime(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#use_custom_runtime LinuxFunctionAppSlot#use_custom_runtime}.'''
        result = self._values.get("use_custom_runtime")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def use_dotnet_isolated_runtime(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the DotNet process use an isolated runtime. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#use_dotnet_isolated_runtime LinuxFunctionAppSlot#use_dotnet_isolated_runtime}
        '''
        result = self._values.get("use_dotnet_isolated_runtime")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotSiteConfigApplicationStack(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotSiteConfigApplicationStackDocker",
    jsii_struct_bases=[],
    name_mapping={
        "image_name": "imageName",
        "image_tag": "imageTag",
        "registry_url": "registryUrl",
        "registry_password": "registryPassword",
        "registry_username": "registryUsername",
    },
)
class LinuxFunctionAppSlotSiteConfigApplicationStackDocker:
    def __init__(
        self,
        *,
        image_name: builtins.str,
        image_tag: builtins.str,
        registry_url: builtins.str,
        registry_password: typing.Optional[builtins.str] = None,
        registry_username: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param image_name: The name of the Docker image to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#image_name LinuxFunctionAppSlot#image_name}
        :param image_tag: The image tag of the image to use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#image_tag LinuxFunctionAppSlot#image_tag}
        :param registry_url: The URL of the docker registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#registry_url LinuxFunctionAppSlot#registry_url}
        :param registry_password: The password for the account to use to connect to the registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#registry_password LinuxFunctionAppSlot#registry_password}
        :param registry_username: The username to use for connections to the registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#registry_username LinuxFunctionAppSlot#registry_username}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6d0082ef34d3c886c674b3af28480907f7cf0ec18580c650438757f99b0aa90)
            check_type(argname="argument image_name", value=image_name, expected_type=type_hints["image_name"])
            check_type(argname="argument image_tag", value=image_tag, expected_type=type_hints["image_tag"])
            check_type(argname="argument registry_url", value=registry_url, expected_type=type_hints["registry_url"])
            check_type(argname="argument registry_password", value=registry_password, expected_type=type_hints["registry_password"])
            check_type(argname="argument registry_username", value=registry_username, expected_type=type_hints["registry_username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image_name": image_name,
            "image_tag": image_tag,
            "registry_url": registry_url,
        }
        if registry_password is not None:
            self._values["registry_password"] = registry_password
        if registry_username is not None:
            self._values["registry_username"] = registry_username

    @builtins.property
    def image_name(self) -> builtins.str:
        '''The name of the Docker image to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#image_name LinuxFunctionAppSlot#image_name}
        '''
        result = self._values.get("image_name")
        assert result is not None, "Required property 'image_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def image_tag(self) -> builtins.str:
        '''The image tag of the image to use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#image_tag LinuxFunctionAppSlot#image_tag}
        '''
        result = self._values.get("image_tag")
        assert result is not None, "Required property 'image_tag' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def registry_url(self) -> builtins.str:
        '''The URL of the docker registry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#registry_url LinuxFunctionAppSlot#registry_url}
        '''
        result = self._values.get("registry_url")
        assert result is not None, "Required property 'registry_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def registry_password(self) -> typing.Optional[builtins.str]:
        '''The password for the account to use to connect to the registry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#registry_password LinuxFunctionAppSlot#registry_password}
        '''
        result = self._values.get("registry_password")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def registry_username(self) -> typing.Optional[builtins.str]:
        '''The username to use for connections to the registry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#registry_username LinuxFunctionAppSlot#registry_username}
        '''
        result = self._values.get("registry_username")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotSiteConfigApplicationStackDocker(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LinuxFunctionAppSlotSiteConfigApplicationStackDockerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotSiteConfigApplicationStackDockerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d307abece9eb60e38a811f973f5d97d8ddc1f3393bda0436137ab94af603904f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LinuxFunctionAppSlotSiteConfigApplicationStackDockerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9aed5c757afe02f30b12998bcc9e46463a95c65506a9eaed22d77d834e96ce61)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LinuxFunctionAppSlotSiteConfigApplicationStackDockerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb10987a5d015b557657109bbd64560ed6069ede7e895e68119afe57972a8235)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8efed2a202cb55c45456bf0cdfa49cdb9e444e3e62351a3217900cf8790acc7c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62b18f5d96eb85597284cdb24bcecbbb8e80d4fe4285ec13e77b927dd92a185f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotSiteConfigApplicationStackDocker]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotSiteConfigApplicationStackDocker]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotSiteConfigApplicationStackDocker]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f19d5c7775dc4c4b37fd7e1ef5b3be28bab44e10a4825293fcd600c67da2fc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LinuxFunctionAppSlotSiteConfigApplicationStackDockerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotSiteConfigApplicationStackDockerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de0b7812b0adff55cee768a1a7b3863fa983cd21703e163b96b77e499c8ecc62)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetRegistryPassword")
    def reset_registry_password(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegistryPassword", []))

    @jsii.member(jsii_name="resetRegistryUsername")
    def reset_registry_username(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegistryUsername", []))

    @builtins.property
    @jsii.member(jsii_name="imageNameInput")
    def image_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageNameInput"))

    @builtins.property
    @jsii.member(jsii_name="imageTagInput")
    def image_tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "imageTagInput"))

    @builtins.property
    @jsii.member(jsii_name="registryPasswordInput")
    def registry_password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "registryPasswordInput"))

    @builtins.property
    @jsii.member(jsii_name="registryUrlInput")
    def registry_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "registryUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="registryUsernameInput")
    def registry_username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "registryUsernameInput"))

    @builtins.property
    @jsii.member(jsii_name="imageName")
    def image_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageName"))

    @image_name.setter
    def image_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__377fac66f8c6f2c19bb78e6655770e6d741c7c101a633a5868e586951de1704e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="imageTag")
    def image_tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "imageTag"))

    @image_tag.setter
    def image_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5790fae2c9687f24bce2775a794cbd1ede67d4d5f88ac26a06c24a096066084f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "imageTag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="registryPassword")
    def registry_password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "registryPassword"))

    @registry_password.setter
    def registry_password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15e7691104f43208550df0fc3e2f587f2051f42f786a7c4f05a73ecb6030c241)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registryPassword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="registryUrl")
    def registry_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "registryUrl"))

    @registry_url.setter
    def registry_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dee6a61cd8735e4ea510331c35207bd61f2755efe95748eb48fac811782fe58f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registryUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="registryUsername")
    def registry_username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "registryUsername"))

    @registry_username.setter
    def registry_username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d823ec0cd848841daef71658afd5e1c8b79630c7905b66d752bdddee19fe4e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "registryUsername", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotSiteConfigApplicationStackDocker]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotSiteConfigApplicationStackDocker]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotSiteConfigApplicationStackDocker]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aadee031d2df7d0d4c4e3a6769532376ebc1a295d2483625ac585ce38d11dda9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LinuxFunctionAppSlotSiteConfigApplicationStackOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotSiteConfigApplicationStackOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__416f50005754c51c531583a44cb9fcdeae99bf68b17c2f9a04783a96ed2ea49f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDocker")
    def put_docker(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LinuxFunctionAppSlotSiteConfigApplicationStackDocker, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__788ab54854123beb96f3aa80ae66da2615b16d140b7036bd20ee4cdafd14713f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDocker", [value]))

    @jsii.member(jsii_name="resetDocker")
    def reset_docker(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDocker", []))

    @jsii.member(jsii_name="resetDotnetVersion")
    def reset_dotnet_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDotnetVersion", []))

    @jsii.member(jsii_name="resetJavaVersion")
    def reset_java_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetJavaVersion", []))

    @jsii.member(jsii_name="resetNodeVersion")
    def reset_node_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNodeVersion", []))

    @jsii.member(jsii_name="resetPowershellCoreVersion")
    def reset_powershell_core_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPowershellCoreVersion", []))

    @jsii.member(jsii_name="resetPythonVersion")
    def reset_python_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPythonVersion", []))

    @jsii.member(jsii_name="resetUseCustomRuntime")
    def reset_use_custom_runtime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseCustomRuntime", []))

    @jsii.member(jsii_name="resetUseDotnetIsolatedRuntime")
    def reset_use_dotnet_isolated_runtime(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseDotnetIsolatedRuntime", []))

    @builtins.property
    @jsii.member(jsii_name="docker")
    def docker(self) -> LinuxFunctionAppSlotSiteConfigApplicationStackDockerList:
        return typing.cast(LinuxFunctionAppSlotSiteConfigApplicationStackDockerList, jsii.get(self, "docker"))

    @builtins.property
    @jsii.member(jsii_name="dockerInput")
    def docker_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotSiteConfigApplicationStackDocker]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotSiteConfigApplicationStackDocker]]], jsii.get(self, "dockerInput"))

    @builtins.property
    @jsii.member(jsii_name="dotnetVersionInput")
    def dotnet_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "dotnetVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="javaVersionInput")
    def java_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "javaVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="nodeVersionInput")
    def node_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nodeVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="powershellCoreVersionInput")
    def powershell_core_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "powershellCoreVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="pythonVersionInput")
    def python_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pythonVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="useCustomRuntimeInput")
    def use_custom_runtime_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useCustomRuntimeInput"))

    @builtins.property
    @jsii.member(jsii_name="useDotnetIsolatedRuntimeInput")
    def use_dotnet_isolated_runtime_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useDotnetIsolatedRuntimeInput"))

    @builtins.property
    @jsii.member(jsii_name="dotnetVersion")
    def dotnet_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dotnetVersion"))

    @dotnet_version.setter
    def dotnet_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a5f0c609180b6c1087a8a702f17424e5f489bafd6d441f596906d8c18bebf18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dotnetVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="javaVersion")
    def java_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "javaVersion"))

    @java_version.setter
    def java_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__865e2d9c75504a46f22bbd9d3ccff3edae8e9a112917ddcf92d3de8ba6993e24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "javaVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nodeVersion")
    def node_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nodeVersion"))

    @node_version.setter
    def node_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb109ab2a93e79c877621da168fa5e4f1203efe1a7d85a52a9ed8eda11f48a7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="powershellCoreVersion")
    def powershell_core_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "powershellCoreVersion"))

    @powershell_core_version.setter
    def powershell_core_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__990cf712ff152bc23ad726af1e41739f5c8a929624d95ed9afd15edefa18e6f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "powershellCoreVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pythonVersion")
    def python_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "pythonVersion"))

    @python_version.setter
    def python_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__440e86b55b734ce7640a6b42768e22a2200a8a5c6a5a8556381c2fa3f26d7209)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pythonVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useCustomRuntime")
    def use_custom_runtime(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useCustomRuntime"))

    @use_custom_runtime.setter
    def use_custom_runtime(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d52ab39aa896b1d74bfdcad314f4182a0317f851cf58ec213b021f80a206aa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useCustomRuntime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useDotnetIsolatedRuntime")
    def use_dotnet_isolated_runtime(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useDotnetIsolatedRuntime"))

    @use_dotnet_isolated_runtime.setter
    def use_dotnet_isolated_runtime(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f7ad4a9fb2a3defb97c7d4d4b8422415cece8bfb6e9fb7bce2be1a77213b37d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useDotnetIsolatedRuntime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[LinuxFunctionAppSlotSiteConfigApplicationStack]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotSiteConfigApplicationStack], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LinuxFunctionAppSlotSiteConfigApplicationStack],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__237b1bfd39264362437b4c28b1aa7c1cd44aad5719e2461a278244836d197273)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotSiteConfigCors",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_origins": "allowedOrigins",
        "support_credentials": "supportCredentials",
    },
)
class LinuxFunctionAppSlotSiteConfigCors:
    def __init__(
        self,
        *,
        allowed_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
        support_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allowed_origins: Specifies a list of origins that should be allowed to make cross-origin calls. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#allowed_origins LinuxFunctionAppSlot#allowed_origins}
        :param support_credentials: Are credentials allowed in CORS requests? Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#support_credentials LinuxFunctionAppSlot#support_credentials}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6cd6c98b0b4fc0d8c9d7dfc06b3154ae3db58f065e80a40078e6c388c2beeb4)
            check_type(argname="argument allowed_origins", value=allowed_origins, expected_type=type_hints["allowed_origins"])
            check_type(argname="argument support_credentials", value=support_credentials, expected_type=type_hints["support_credentials"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allowed_origins is not None:
            self._values["allowed_origins"] = allowed_origins
        if support_credentials is not None:
            self._values["support_credentials"] = support_credentials

    @builtins.property
    def allowed_origins(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of origins that should be allowed to make cross-origin calls.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#allowed_origins LinuxFunctionAppSlot#allowed_origins}
        '''
        result = self._values.get("allowed_origins")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def support_credentials(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Are credentials allowed in CORS requests? Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#support_credentials LinuxFunctionAppSlot#support_credentials}
        '''
        result = self._values.get("support_credentials")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotSiteConfigCors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LinuxFunctionAppSlotSiteConfigCorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotSiteConfigCorsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffd34e471ada35ba765efe6950e1af23cf0579920043118f6a684585f72daee4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAllowedOrigins")
    def reset_allowed_origins(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllowedOrigins", []))

    @jsii.member(jsii_name="resetSupportCredentials")
    def reset_support_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSupportCredentials", []))

    @builtins.property
    @jsii.member(jsii_name="allowedOriginsInput")
    def allowed_origins_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "allowedOriginsInput"))

    @builtins.property
    @jsii.member(jsii_name="supportCredentialsInput")
    def support_credentials_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "supportCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="allowedOrigins")
    def allowed_origins(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedOrigins"))

    @allowed_origins.setter
    def allowed_origins(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b85eb2d79cba67f4c3c6a8c3dfd38b6cf88fda919eb5b38b4c24cedce9f3fe0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedOrigins", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="supportCredentials")
    def support_credentials(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "supportCredentials"))

    @support_credentials.setter
    def support_credentials(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e0f60bfaaf3d7b0ff267cf4ebe06682ba17461c625a1595c9b4f720ab9fe4f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportCredentials", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LinuxFunctionAppSlotSiteConfigCors]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotSiteConfigCors], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LinuxFunctionAppSlotSiteConfigCors],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b205752b9a6291d525017f7689fe8a8f529eb89286d45d0c8a488bd17c5f22a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotSiteConfigIpRestriction",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "description": "description",
        "headers": "headers",
        "ip_address": "ipAddress",
        "name": "name",
        "priority": "priority",
        "service_tag": "serviceTag",
        "virtual_network_subnet_id": "virtualNetworkSubnetId",
    },
)
class LinuxFunctionAppSlotSiteConfigIpRestriction:
    def __init__(
        self,
        *,
        action: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LinuxFunctionAppSlotSiteConfigIpRestrictionHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ip_address: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        service_tag: typing.Optional[builtins.str] = None,
        virtual_network_subnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action: The action to take. Possible values are ``Allow`` or ``Deny``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#action LinuxFunctionAppSlot#action}
        :param description: The description of the IP restriction rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#description LinuxFunctionAppSlot#description}
        :param headers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#headers LinuxFunctionAppSlot#headers}.
        :param ip_address: The CIDR notation of the IP or IP Range to match. For example: ``10.0.0.0/24`` or ``192.168.10.1/32`` or ``fe80::/64`` or ``13.107.6.152/31,13.107.128.0/22`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#ip_address LinuxFunctionAppSlot#ip_address}
        :param name: The name which should be used for this ``ip_restriction``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#name LinuxFunctionAppSlot#name}
        :param priority: The priority value of this ``ip_restriction``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#priority LinuxFunctionAppSlot#priority}
        :param service_tag: The Service Tag used for this IP Restriction. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#service_tag LinuxFunctionAppSlot#service_tag}
        :param virtual_network_subnet_id: The Virtual Network Subnet ID used for this IP Restriction. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#virtual_network_subnet_id LinuxFunctionAppSlot#virtual_network_subnet_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2181d25c5700b45f8316e979148e3e18271066d7eba8ac19bf4940eee4967f73)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument service_tag", value=service_tag, expected_type=type_hints["service_tag"])
            check_type(argname="argument virtual_network_subnet_id", value=virtual_network_subnet_id, expected_type=type_hints["virtual_network_subnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action is not None:
            self._values["action"] = action
        if description is not None:
            self._values["description"] = description
        if headers is not None:
            self._values["headers"] = headers
        if ip_address is not None:
            self._values["ip_address"] = ip_address
        if name is not None:
            self._values["name"] = name
        if priority is not None:
            self._values["priority"] = priority
        if service_tag is not None:
            self._values["service_tag"] = service_tag
        if virtual_network_subnet_id is not None:
            self._values["virtual_network_subnet_id"] = virtual_network_subnet_id

    @builtins.property
    def action(self) -> typing.Optional[builtins.str]:
        '''The action to take. Possible values are ``Allow`` or ``Deny``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#action LinuxFunctionAppSlot#action}
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the IP restriction rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#description LinuxFunctionAppSlot#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LinuxFunctionAppSlotSiteConfigIpRestrictionHeaders"]]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#headers LinuxFunctionAppSlot#headers}.'''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LinuxFunctionAppSlotSiteConfigIpRestrictionHeaders"]]], result)

    @builtins.property
    def ip_address(self) -> typing.Optional[builtins.str]:
        '''The CIDR notation of the IP or IP Range to match.

        For example: ``10.0.0.0/24`` or ``192.168.10.1/32`` or ``fe80::/64`` or ``13.107.6.152/31,13.107.128.0/22``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#ip_address LinuxFunctionAppSlot#ip_address}
        '''
        result = self._values.get("ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name which should be used for this ``ip_restriction``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#name LinuxFunctionAppSlot#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''The priority value of this ``ip_restriction``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#priority LinuxFunctionAppSlot#priority}
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service_tag(self) -> typing.Optional[builtins.str]:
        '''The Service Tag used for this IP Restriction.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#service_tag LinuxFunctionAppSlot#service_tag}
        '''
        result = self._values.get("service_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def virtual_network_subnet_id(self) -> typing.Optional[builtins.str]:
        '''The Virtual Network Subnet ID used for this IP Restriction.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#virtual_network_subnet_id LinuxFunctionAppSlot#virtual_network_subnet_id}
        '''
        result = self._values.get("virtual_network_subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotSiteConfigIpRestriction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotSiteConfigIpRestrictionHeaders",
    jsii_struct_bases=[],
    name_mapping={
        "x_azure_fdid": "xAzureFdid",
        "x_fd_health_probe": "xFdHealthProbe",
        "x_forwarded_for": "xForwardedFor",
        "x_forwarded_host": "xForwardedHost",
    },
)
class LinuxFunctionAppSlotSiteConfigIpRestrictionHeaders:
    def __init__(
        self,
        *,
        x_azure_fdid: typing.Optional[typing.Sequence[builtins.str]] = None,
        x_fd_health_probe: typing.Optional[typing.Sequence[builtins.str]] = None,
        x_forwarded_for: typing.Optional[typing.Sequence[builtins.str]] = None,
        x_forwarded_host: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param x_azure_fdid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#x_azure_fdid LinuxFunctionAppSlot#x_azure_fdid}.
        :param x_fd_health_probe: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#x_fd_health_probe LinuxFunctionAppSlot#x_fd_health_probe}.
        :param x_forwarded_for: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#x_forwarded_for LinuxFunctionAppSlot#x_forwarded_for}.
        :param x_forwarded_host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#x_forwarded_host LinuxFunctionAppSlot#x_forwarded_host}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50d5256d44a930fb2a8059c70d838c9de005f4581e36a76400095e65f7b92455)
            check_type(argname="argument x_azure_fdid", value=x_azure_fdid, expected_type=type_hints["x_azure_fdid"])
            check_type(argname="argument x_fd_health_probe", value=x_fd_health_probe, expected_type=type_hints["x_fd_health_probe"])
            check_type(argname="argument x_forwarded_for", value=x_forwarded_for, expected_type=type_hints["x_forwarded_for"])
            check_type(argname="argument x_forwarded_host", value=x_forwarded_host, expected_type=type_hints["x_forwarded_host"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if x_azure_fdid is not None:
            self._values["x_azure_fdid"] = x_azure_fdid
        if x_fd_health_probe is not None:
            self._values["x_fd_health_probe"] = x_fd_health_probe
        if x_forwarded_for is not None:
            self._values["x_forwarded_for"] = x_forwarded_for
        if x_forwarded_host is not None:
            self._values["x_forwarded_host"] = x_forwarded_host

    @builtins.property
    def x_azure_fdid(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#x_azure_fdid LinuxFunctionAppSlot#x_azure_fdid}.'''
        result = self._values.get("x_azure_fdid")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def x_fd_health_probe(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#x_fd_health_probe LinuxFunctionAppSlot#x_fd_health_probe}.'''
        result = self._values.get("x_fd_health_probe")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def x_forwarded_for(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#x_forwarded_for LinuxFunctionAppSlot#x_forwarded_for}.'''
        result = self._values.get("x_forwarded_for")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def x_forwarded_host(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#x_forwarded_host LinuxFunctionAppSlot#x_forwarded_host}.'''
        result = self._values.get("x_forwarded_host")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotSiteConfigIpRestrictionHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LinuxFunctionAppSlotSiteConfigIpRestrictionHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotSiteConfigIpRestrictionHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e170f73a1a027dc804e96a211b0bb73d02a5aeca206d470d4fb922101e6d357)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LinuxFunctionAppSlotSiteConfigIpRestrictionHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91576af329c18629b095f2adb25232eab2b8ee1e889d8c15722e72af8fb33ac8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LinuxFunctionAppSlotSiteConfigIpRestrictionHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfe6bc8d8b8ca61c0f64aff33e4ebcd7981b17c743bdf25a99671e6e8049ac54)
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
            type_hints = typing.get_type_hints(_typecheckingstub__964c99717c4ba93e2be5485ce8a124bd790bfc7508f398cb51fc21a0a24eadb2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0757a7d85970c558d055a85e492f59672d984437ae410f986f661422381ed19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotSiteConfigIpRestrictionHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotSiteConfigIpRestrictionHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotSiteConfigIpRestrictionHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__564d69487555c97f71d0d6a4326d4cee20423e9cb8f5dadee6b3d09903f2a572)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LinuxFunctionAppSlotSiteConfigIpRestrictionHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotSiteConfigIpRestrictionHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebb688944243042dbe00c9954d98b17945880f3e3cd2ba3917971c07925abafd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetXAzureFdid")
    def reset_x_azure_fdid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetXAzureFdid", []))

    @jsii.member(jsii_name="resetXFdHealthProbe")
    def reset_x_fd_health_probe(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetXFdHealthProbe", []))

    @jsii.member(jsii_name="resetXForwardedFor")
    def reset_x_forwarded_for(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetXForwardedFor", []))

    @jsii.member(jsii_name="resetXForwardedHost")
    def reset_x_forwarded_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetXForwardedHost", []))

    @builtins.property
    @jsii.member(jsii_name="xAzureFdidInput")
    def x_azure_fdid_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "xAzureFdidInput"))

    @builtins.property
    @jsii.member(jsii_name="xFdHealthProbeInput")
    def x_fd_health_probe_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "xFdHealthProbeInput"))

    @builtins.property
    @jsii.member(jsii_name="xForwardedForInput")
    def x_forwarded_for_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "xForwardedForInput"))

    @builtins.property
    @jsii.member(jsii_name="xForwardedHostInput")
    def x_forwarded_host_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "xForwardedHostInput"))

    @builtins.property
    @jsii.member(jsii_name="xAzureFdid")
    def x_azure_fdid(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "xAzureFdid"))

    @x_azure_fdid.setter
    def x_azure_fdid(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b175cab431bb0a66d369d1b5147245d03c021d1c4afec20c2d44b5b0ba6e4ca4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "xAzureFdid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="xFdHealthProbe")
    def x_fd_health_probe(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "xFdHealthProbe"))

    @x_fd_health_probe.setter
    def x_fd_health_probe(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8260ad1fb7740237aa412f46bddcd9788f77c09ff0ab4edad3d3c09b407acf4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "xFdHealthProbe", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="xForwardedFor")
    def x_forwarded_for(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "xForwardedFor"))

    @x_forwarded_for.setter
    def x_forwarded_for(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b6bf0179fb3a58b1324f9ad03432d20f36bd8be64dd12fb77b10909b2fbc978)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "xForwardedFor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="xForwardedHost")
    def x_forwarded_host(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "xForwardedHost"))

    @x_forwarded_host.setter
    def x_forwarded_host(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__746ee6f9d32fb84782938db41768ba54e9c6d2b2c623e81a7d290895360fd80b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "xForwardedHost", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotSiteConfigIpRestrictionHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotSiteConfigIpRestrictionHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotSiteConfigIpRestrictionHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b77062612584b268a742741a28f1265fd70b59a24c8122aa328b010fcaae122)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LinuxFunctionAppSlotSiteConfigIpRestrictionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotSiteConfigIpRestrictionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73cba6347ed17055cbc7abed9e774ba53a022c5e4fd81ab2c490627d87c97786)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LinuxFunctionAppSlotSiteConfigIpRestrictionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b488ef2fe1df97afccf9373c8a00797263248c992026260152cd2f33bf8174a6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LinuxFunctionAppSlotSiteConfigIpRestrictionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9d345c3f2e8bc1ab447a3d6b692fd04f8981fefbea0e190c7cadaf163dfc024)
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
            type_hints = typing.get_type_hints(_typecheckingstub__80d768b9c95be4bfceff88c408605f7dfc41a671a9ec38480c30513a494798bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__476f93f2e52f4d9e05e0f518696d48b91111af863a7c277331402d63a5881deb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotSiteConfigIpRestriction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotSiteConfigIpRestriction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotSiteConfigIpRestriction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0adab1c3bd6bcb899f2a0fc1d1ad9a816248842fed4c496d5160275e19f439d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LinuxFunctionAppSlotSiteConfigIpRestrictionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotSiteConfigIpRestrictionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b790a27a1051bd06a7328b1a2ca7c16144ad7cf430e70d73e024032e92fd24b8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHeaders")
    def put_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LinuxFunctionAppSlotSiteConfigIpRestrictionHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48de0acd9a8a31921840a9cae00b754296b9bb8af9edb89ac57de486d1fd51bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeaders", [value]))

    @jsii.member(jsii_name="resetAction")
    def reset_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAction", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetHeaders")
    def reset_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaders", []))

    @jsii.member(jsii_name="resetIpAddress")
    def reset_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddress", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetServiceTag")
    def reset_service_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceTag", []))

    @jsii.member(jsii_name="resetVirtualNetworkSubnetId")
    def reset_virtual_network_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualNetworkSubnetId", []))

    @builtins.property
    @jsii.member(jsii_name="headers")
    def headers(self) -> LinuxFunctionAppSlotSiteConfigIpRestrictionHeadersList:
        return typing.cast(LinuxFunctionAppSlotSiteConfigIpRestrictionHeadersList, jsii.get(self, "headers"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="headersInput")
    def headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotSiteConfigIpRestrictionHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotSiteConfigIpRestrictionHeaders]]], jsii.get(self, "headersInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceTagInput")
    def service_tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceTagInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkSubnetIdInput")
    def virtual_network_subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualNetworkSubnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__691d38a74c0c927a712ac9ef43d57a9fa19a3654c6438accda9b3cd9d2fb0192)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c749f3a45a2d5e550886ccd96ade41e18fa9ca02b440b0313613de9f034e2bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe153b1c901bfde0c86db8ebc298684b2cd8adb47d2853cd16a03d6121f91a68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c9cd5fe034bc18bffc479a5d845685f3124f89ad3d2c8a032134cf24382d88f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51a22cc7068c628f423d8a30fab25dc1a7280c0d674925650b42e80c8f505675)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceTag")
    def service_tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceTag"))

    @service_tag.setter
    def service_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1386979a4d64d0c85dd24d7237553a47c83e1d9385ccd249d645e81d34e8f16f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceTag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkSubnetId")
    def virtual_network_subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkSubnetId"))

    @virtual_network_subnet_id.setter
    def virtual_network_subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed74ddc11f0b93464b94a2a4707d2ca2480d9e7a6174db7ed4fa964a45e44f7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkSubnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotSiteConfigIpRestriction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotSiteConfigIpRestriction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotSiteConfigIpRestriction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2a7ca7b656b32d335eff58a55da4cf44e5fb57412e76e1c3af91bac2aefb482)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LinuxFunctionAppSlotSiteConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotSiteConfigOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c9c784634f92258245bbd5865f0358ef44f9fce0735bd13630cc36bf756dce8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putApplicationStack")
    def put_application_stack(
        self,
        *,
        docker: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LinuxFunctionAppSlotSiteConfigApplicationStackDocker, typing.Dict[builtins.str, typing.Any]]]]] = None,
        dotnet_version: typing.Optional[builtins.str] = None,
        java_version: typing.Optional[builtins.str] = None,
        node_version: typing.Optional[builtins.str] = None,
        powershell_core_version: typing.Optional[builtins.str] = None,
        python_version: typing.Optional[builtins.str] = None,
        use_custom_runtime: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use_dotnet_isolated_runtime: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param docker: docker block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#docker LinuxFunctionAppSlot#docker}
        :param dotnet_version: The version of .Net. Possible values are ``3.1``, ``6.0``, ``7.0``, ``8.0`` and ``9.0``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#dotnet_version LinuxFunctionAppSlot#dotnet_version}
        :param java_version: The version of Java to use. Possible values are ``8``, ``11``, ``17``, and ``21``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#java_version LinuxFunctionAppSlot#java_version}
        :param node_version: The version of Node to use. Possible values include ``12``, ``14``, ``16``, ``18``, ``20`` and ``22``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#node_version LinuxFunctionAppSlot#node_version}
        :param powershell_core_version: The version of PowerShell Core to use. Possibles values are ``7``, ``7.2``, and ``7.4``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#powershell_core_version LinuxFunctionAppSlot#powershell_core_version}
        :param python_version: The version of Python to use. Possible values include ``3.13``, ``3.12``, ``3.11``, ``3.10``, ``3.9``, ``3.8``, and ``3.7``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#python_version LinuxFunctionAppSlot#python_version}
        :param use_custom_runtime: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#use_custom_runtime LinuxFunctionAppSlot#use_custom_runtime}.
        :param use_dotnet_isolated_runtime: Should the DotNet process use an isolated runtime. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#use_dotnet_isolated_runtime LinuxFunctionAppSlot#use_dotnet_isolated_runtime}
        '''
        value = LinuxFunctionAppSlotSiteConfigApplicationStack(
            docker=docker,
            dotnet_version=dotnet_version,
            java_version=java_version,
            node_version=node_version,
            powershell_core_version=powershell_core_version,
            python_version=python_version,
            use_custom_runtime=use_custom_runtime,
            use_dotnet_isolated_runtime=use_dotnet_isolated_runtime,
        )

        return typing.cast(None, jsii.invoke(self, "putApplicationStack", [value]))

    @jsii.member(jsii_name="putAppServiceLogs")
    def put_app_service_logs(
        self,
        *,
        disk_quota_mb: typing.Optional[jsii.Number] = None,
        retention_period_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param disk_quota_mb: The amount of disk space to use for logs. Valid values are between ``25`` and ``100``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#disk_quota_mb LinuxFunctionAppSlot#disk_quota_mb}
        :param retention_period_days: The retention period for logs in days. Valid values are between ``0`` and ``99999``. Defaults to ``0`` (never delete). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#retention_period_days LinuxFunctionAppSlot#retention_period_days}
        '''
        value = LinuxFunctionAppSlotSiteConfigAppServiceLogs(
            disk_quota_mb=disk_quota_mb, retention_period_days=retention_period_days
        )

        return typing.cast(None, jsii.invoke(self, "putAppServiceLogs", [value]))

    @jsii.member(jsii_name="putCors")
    def put_cors(
        self,
        *,
        allowed_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
        support_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allowed_origins: Specifies a list of origins that should be allowed to make cross-origin calls. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#allowed_origins LinuxFunctionAppSlot#allowed_origins}
        :param support_credentials: Are credentials allowed in CORS requests? Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#support_credentials LinuxFunctionAppSlot#support_credentials}
        '''
        value = LinuxFunctionAppSlotSiteConfigCors(
            allowed_origins=allowed_origins, support_credentials=support_credentials
        )

        return typing.cast(None, jsii.invoke(self, "putCors", [value]))

    @jsii.member(jsii_name="putIpRestriction")
    def put_ip_restriction(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LinuxFunctionAppSlotSiteConfigIpRestriction, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6126f4ce91a78eda649d7881057283f1a3c357f8b09e18692de910a81ce57971)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIpRestriction", [value]))

    @jsii.member(jsii_name="putScmIpRestriction")
    def put_scm_ip_restriction(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LinuxFunctionAppSlotSiteConfigScmIpRestriction", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e92d9180c1cbff3234d7497041a518bd81bd7922cb290beac32c9edfd1c8239e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putScmIpRestriction", [value]))

    @jsii.member(jsii_name="resetAlwaysOn")
    def reset_always_on(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlwaysOn", []))

    @jsii.member(jsii_name="resetApiDefinitionUrl")
    def reset_api_definition_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiDefinitionUrl", []))

    @jsii.member(jsii_name="resetApiManagementApiId")
    def reset_api_management_api_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiManagementApiId", []))

    @jsii.member(jsii_name="resetAppCommandLine")
    def reset_app_command_line(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppCommandLine", []))

    @jsii.member(jsii_name="resetApplicationInsightsConnectionString")
    def reset_application_insights_connection_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplicationInsightsConnectionString", []))

    @jsii.member(jsii_name="resetApplicationInsightsKey")
    def reset_application_insights_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplicationInsightsKey", []))

    @jsii.member(jsii_name="resetApplicationStack")
    def reset_application_stack(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplicationStack", []))

    @jsii.member(jsii_name="resetAppScaleLimit")
    def reset_app_scale_limit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppScaleLimit", []))

    @jsii.member(jsii_name="resetAppServiceLogs")
    def reset_app_service_logs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppServiceLogs", []))

    @jsii.member(jsii_name="resetAutoSwapSlotName")
    def reset_auto_swap_slot_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoSwapSlotName", []))

    @jsii.member(jsii_name="resetContainerRegistryManagedIdentityClientId")
    def reset_container_registry_managed_identity_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerRegistryManagedIdentityClientId", []))

    @jsii.member(jsii_name="resetContainerRegistryUseManagedIdentity")
    def reset_container_registry_use_managed_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerRegistryUseManagedIdentity", []))

    @jsii.member(jsii_name="resetCors")
    def reset_cors(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCors", []))

    @jsii.member(jsii_name="resetDefaultDocuments")
    def reset_default_documents(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultDocuments", []))

    @jsii.member(jsii_name="resetElasticInstanceMinimum")
    def reset_elastic_instance_minimum(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetElasticInstanceMinimum", []))

    @jsii.member(jsii_name="resetFtpsState")
    def reset_ftps_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFtpsState", []))

    @jsii.member(jsii_name="resetHealthCheckEvictionTimeInMin")
    def reset_health_check_eviction_time_in_min(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthCheckEvictionTimeInMin", []))

    @jsii.member(jsii_name="resetHealthCheckPath")
    def reset_health_check_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthCheckPath", []))

    @jsii.member(jsii_name="resetHttp2Enabled")
    def reset_http2_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttp2Enabled", []))

    @jsii.member(jsii_name="resetIpRestriction")
    def reset_ip_restriction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpRestriction", []))

    @jsii.member(jsii_name="resetIpRestrictionDefaultAction")
    def reset_ip_restriction_default_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpRestrictionDefaultAction", []))

    @jsii.member(jsii_name="resetLoadBalancingMode")
    def reset_load_balancing_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoadBalancingMode", []))

    @jsii.member(jsii_name="resetManagedPipelineMode")
    def reset_managed_pipeline_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedPipelineMode", []))

    @jsii.member(jsii_name="resetMinimumTlsVersion")
    def reset_minimum_tls_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumTlsVersion", []))

    @jsii.member(jsii_name="resetPreWarmedInstanceCount")
    def reset_pre_warmed_instance_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPreWarmedInstanceCount", []))

    @jsii.member(jsii_name="resetRemoteDebuggingEnabled")
    def reset_remote_debugging_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoteDebuggingEnabled", []))

    @jsii.member(jsii_name="resetRemoteDebuggingVersion")
    def reset_remote_debugging_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRemoteDebuggingVersion", []))

    @jsii.member(jsii_name="resetRuntimeScaleMonitoringEnabled")
    def reset_runtime_scale_monitoring_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRuntimeScaleMonitoringEnabled", []))

    @jsii.member(jsii_name="resetScmIpRestriction")
    def reset_scm_ip_restriction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScmIpRestriction", []))

    @jsii.member(jsii_name="resetScmIpRestrictionDefaultAction")
    def reset_scm_ip_restriction_default_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScmIpRestrictionDefaultAction", []))

    @jsii.member(jsii_name="resetScmMinimumTlsVersion")
    def reset_scm_minimum_tls_version(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScmMinimumTlsVersion", []))

    @jsii.member(jsii_name="resetScmUseMainIpRestriction")
    def reset_scm_use_main_ip_restriction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScmUseMainIpRestriction", []))

    @jsii.member(jsii_name="resetUse32BitWorker")
    def reset_use32_bit_worker(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUse32BitWorker", []))

    @jsii.member(jsii_name="resetVnetRouteAllEnabled")
    def reset_vnet_route_all_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVnetRouteAllEnabled", []))

    @jsii.member(jsii_name="resetWebsocketsEnabled")
    def reset_websockets_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebsocketsEnabled", []))

    @jsii.member(jsii_name="resetWorkerCount")
    def reset_worker_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkerCount", []))

    @builtins.property
    @jsii.member(jsii_name="applicationStack")
    def application_stack(
        self,
    ) -> LinuxFunctionAppSlotSiteConfigApplicationStackOutputReference:
        return typing.cast(LinuxFunctionAppSlotSiteConfigApplicationStackOutputReference, jsii.get(self, "applicationStack"))

    @builtins.property
    @jsii.member(jsii_name="appServiceLogs")
    def app_service_logs(
        self,
    ) -> LinuxFunctionAppSlotSiteConfigAppServiceLogsOutputReference:
        return typing.cast(LinuxFunctionAppSlotSiteConfigAppServiceLogsOutputReference, jsii.get(self, "appServiceLogs"))

    @builtins.property
    @jsii.member(jsii_name="cors")
    def cors(self) -> LinuxFunctionAppSlotSiteConfigCorsOutputReference:
        return typing.cast(LinuxFunctionAppSlotSiteConfigCorsOutputReference, jsii.get(self, "cors"))

    @builtins.property
    @jsii.member(jsii_name="detailedErrorLoggingEnabled")
    def detailed_error_logging_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "detailedErrorLoggingEnabled"))

    @builtins.property
    @jsii.member(jsii_name="ipRestriction")
    def ip_restriction(self) -> LinuxFunctionAppSlotSiteConfigIpRestrictionList:
        return typing.cast(LinuxFunctionAppSlotSiteConfigIpRestrictionList, jsii.get(self, "ipRestriction"))

    @builtins.property
    @jsii.member(jsii_name="linuxFxVersion")
    def linux_fx_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "linuxFxVersion"))

    @builtins.property
    @jsii.member(jsii_name="scmIpRestriction")
    def scm_ip_restriction(
        self,
    ) -> "LinuxFunctionAppSlotSiteConfigScmIpRestrictionList":
        return typing.cast("LinuxFunctionAppSlotSiteConfigScmIpRestrictionList", jsii.get(self, "scmIpRestriction"))

    @builtins.property
    @jsii.member(jsii_name="scmType")
    def scm_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scmType"))

    @builtins.property
    @jsii.member(jsii_name="alwaysOnInput")
    def always_on_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "alwaysOnInput"))

    @builtins.property
    @jsii.member(jsii_name="apiDefinitionUrlInput")
    def api_definition_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiDefinitionUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="apiManagementApiIdInput")
    def api_management_api_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiManagementApiIdInput"))

    @builtins.property
    @jsii.member(jsii_name="appCommandLineInput")
    def app_command_line_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appCommandLineInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationInsightsConnectionStringInput")
    def application_insights_connection_string_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationInsightsConnectionStringInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationInsightsKeyInput")
    def application_insights_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationInsightsKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationStackInput")
    def application_stack_input(
        self,
    ) -> typing.Optional[LinuxFunctionAppSlotSiteConfigApplicationStack]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotSiteConfigApplicationStack], jsii.get(self, "applicationStackInput"))

    @builtins.property
    @jsii.member(jsii_name="appScaleLimitInput")
    def app_scale_limit_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "appScaleLimitInput"))

    @builtins.property
    @jsii.member(jsii_name="appServiceLogsInput")
    def app_service_logs_input(
        self,
    ) -> typing.Optional[LinuxFunctionAppSlotSiteConfigAppServiceLogs]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotSiteConfigAppServiceLogs], jsii.get(self, "appServiceLogsInput"))

    @builtins.property
    @jsii.member(jsii_name="autoSwapSlotNameInput")
    def auto_swap_slot_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoSwapSlotNameInput"))

    @builtins.property
    @jsii.member(jsii_name="containerRegistryManagedIdentityClientIdInput")
    def container_registry_managed_identity_client_id_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerRegistryManagedIdentityClientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="containerRegistryUseManagedIdentityInput")
    def container_registry_use_managed_identity_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "containerRegistryUseManagedIdentityInput"))

    @builtins.property
    @jsii.member(jsii_name="corsInput")
    def cors_input(self) -> typing.Optional[LinuxFunctionAppSlotSiteConfigCors]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotSiteConfigCors], jsii.get(self, "corsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultDocumentsInput")
    def default_documents_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "defaultDocumentsInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticInstanceMinimumInput")
    def elastic_instance_minimum_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "elasticInstanceMinimumInput"))

    @builtins.property
    @jsii.member(jsii_name="ftpsStateInput")
    def ftps_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ftpsStateInput"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckEvictionTimeInMinInput")
    def health_check_eviction_time_in_min_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "healthCheckEvictionTimeInMinInput"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckPathInput")
    def health_check_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "healthCheckPathInput"))

    @builtins.property
    @jsii.member(jsii_name="http2EnabledInput")
    def http2_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "http2EnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="ipRestrictionDefaultActionInput")
    def ip_restriction_default_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipRestrictionDefaultActionInput"))

    @builtins.property
    @jsii.member(jsii_name="ipRestrictionInput")
    def ip_restriction_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotSiteConfigIpRestriction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotSiteConfigIpRestriction]]], jsii.get(self, "ipRestrictionInput"))

    @builtins.property
    @jsii.member(jsii_name="loadBalancingModeInput")
    def load_balancing_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loadBalancingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="managedPipelineModeInput")
    def managed_pipeline_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managedPipelineModeInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumTlsVersionInput")
    def minimum_tls_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "minimumTlsVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="preWarmedInstanceCountInput")
    def pre_warmed_instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "preWarmedInstanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteDebuggingEnabledInput")
    def remote_debugging_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "remoteDebuggingEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteDebuggingVersionInput")
    def remote_debugging_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "remoteDebuggingVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeScaleMonitoringEnabledInput")
    def runtime_scale_monitoring_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "runtimeScaleMonitoringEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="scmIpRestrictionDefaultActionInput")
    def scm_ip_restriction_default_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scmIpRestrictionDefaultActionInput"))

    @builtins.property
    @jsii.member(jsii_name="scmIpRestrictionInput")
    def scm_ip_restriction_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LinuxFunctionAppSlotSiteConfigScmIpRestriction"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LinuxFunctionAppSlotSiteConfigScmIpRestriction"]]], jsii.get(self, "scmIpRestrictionInput"))

    @builtins.property
    @jsii.member(jsii_name="scmMinimumTlsVersionInput")
    def scm_minimum_tls_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scmMinimumTlsVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="scmUseMainIpRestrictionInput")
    def scm_use_main_ip_restriction_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "scmUseMainIpRestrictionInput"))

    @builtins.property
    @jsii.member(jsii_name="use32BitWorkerInput")
    def use32_bit_worker_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "use32BitWorkerInput"))

    @builtins.property
    @jsii.member(jsii_name="vnetRouteAllEnabledInput")
    def vnet_route_all_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "vnetRouteAllEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="websocketsEnabledInput")
    def websockets_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "websocketsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="workerCountInput")
    def worker_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "workerCountInput"))

    @builtins.property
    @jsii.member(jsii_name="alwaysOn")
    def always_on(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "alwaysOn"))

    @always_on.setter
    def always_on(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5d3f7d71d944080d100644a2483cd4c74c28a0648d56ae90156c5c703e558bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alwaysOn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiDefinitionUrl")
    def api_definition_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiDefinitionUrl"))

    @api_definition_url.setter
    def api_definition_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b58de00b8121d3fc793ea5cb973932e3b4c1d7f37140f9098e906cc829a83e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiDefinitionUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiManagementApiId")
    def api_management_api_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiManagementApiId"))

    @api_management_api_id.setter
    def api_management_api_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f14a98c07510de1c0d2f3b26413bef91fdfeebe093955fc60b67195819f1760)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiManagementApiId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appCommandLine")
    def app_command_line(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appCommandLine"))

    @app_command_line.setter
    def app_command_line(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfb8c9893ee225174b747417e8a15bc643c36ea9db66f37a27220ee53c95ea52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appCommandLine", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="applicationInsightsConnectionString")
    def application_insights_connection_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationInsightsConnectionString"))

    @application_insights_connection_string.setter
    def application_insights_connection_string(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b70566296b1f4075247cb1428b144fa53f66efde640697d8483c6e9114e9b40f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationInsightsConnectionString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="applicationInsightsKey")
    def application_insights_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationInsightsKey"))

    @application_insights_key.setter
    def application_insights_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e32ca8802f9de893dcc7f9e3fb97283667439613433aca1fc738919155222aae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationInsightsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appScaleLimit")
    def app_scale_limit(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "appScaleLimit"))

    @app_scale_limit.setter
    def app_scale_limit(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6578c88e833928ffda197a9cf6423ad5f3490d1367de3f57b8a2f2c09594ae5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appScaleLimit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoSwapSlotName")
    def auto_swap_slot_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoSwapSlotName"))

    @auto_swap_slot_name.setter
    def auto_swap_slot_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74a599adced3d2d1ad564718449480bc4b051f56d5ea8d7a7348e34af8772efc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoSwapSlotName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containerRegistryManagedIdentityClientId")
    def container_registry_managed_identity_client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerRegistryManagedIdentityClientId"))

    @container_registry_managed_identity_client_id.setter
    def container_registry_managed_identity_client_id(
        self,
        value: builtins.str,
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b8602c2eb0aa2acdf0c788407cb60e6690ccf64b583cafc17391b813e8f5192)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerRegistryManagedIdentityClientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="containerRegistryUseManagedIdentity")
    def container_registry_use_managed_identity(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "containerRegistryUseManagedIdentity"))

    @container_registry_use_managed_identity.setter
    def container_registry_use_managed_identity(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e55bfd227ef68ac403f50517d9fbb6fb1550cf8c5792109df06251733c495e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerRegistryUseManagedIdentity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultDocuments")
    def default_documents(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "defaultDocuments"))

    @default_documents.setter
    def default_documents(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b1fd312592fed2d98585f56767caba807ba46fc36ec73565b81ec355263de00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultDocuments", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="elasticInstanceMinimum")
    def elastic_instance_minimum(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "elasticInstanceMinimum"))

    @elastic_instance_minimum.setter
    def elastic_instance_minimum(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8847a649f251f81329df7d12009d9d7e932396ed3cba538a5fe015e380e5325)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elasticInstanceMinimum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ftpsState")
    def ftps_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ftpsState"))

    @ftps_state.setter
    def ftps_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a89260944f71302e836748964f17bf85d991be177dbe03702f95843c1dca883)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ftpsState", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="healthCheckEvictionTimeInMin")
    def health_check_eviction_time_in_min(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "healthCheckEvictionTimeInMin"))

    @health_check_eviction_time_in_min.setter
    def health_check_eviction_time_in_min(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3b00ecf053b684924c9debbfc3c77b9cb7ff5ea60be5c084e4d93b4266339e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthCheckEvictionTimeInMin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="healthCheckPath")
    def health_check_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "healthCheckPath"))

    @health_check_path.setter
    def health_check_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62f0f9582ed52c2c42136ca62dd0238070e068dd934cc71178c482ff1f6ed5e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthCheckPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="http2Enabled")
    def http2_enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "http2Enabled"))

    @http2_enabled.setter
    def http2_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__267ce8f413baacfa7788657aebfdf7d9306f0ca717ed547e9a36bf3fa292b09d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "http2Enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipRestrictionDefaultAction")
    def ip_restriction_default_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipRestrictionDefaultAction"))

    @ip_restriction_default_action.setter
    def ip_restriction_default_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5f18d510a8215f580f8ea98e83008aabb15ed0717bdf0416da430151e11f766)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipRestrictionDefaultAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancingMode")
    def load_balancing_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancingMode"))

    @load_balancing_mode.setter
    def load_balancing_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39450caf2bce0b203a3a406be564b6c14cd482aafb20c22df23ba8629c124235)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managedPipelineMode")
    def managed_pipeline_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managedPipelineMode"))

    @managed_pipeline_mode.setter
    def managed_pipeline_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fc508a989b99d1d2bddcd36b3c5aa059cbd81ebadf2246f784cea6241960abb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedPipelineMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimumTlsVersion")
    def minimum_tls_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minimumTlsVersion"))

    @minimum_tls_version.setter
    def minimum_tls_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9b2c4cb2e9acc5395c0a3e1afef0f33dbd786a32ca979463eaca0562f266253)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumTlsVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="preWarmedInstanceCount")
    def pre_warmed_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "preWarmedInstanceCount"))

    @pre_warmed_instance_count.setter
    def pre_warmed_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a4680dc65e5e40529cb97b77af53fed60cb0e005c9580c64987203361ee5315)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preWarmedInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remoteDebuggingEnabled")
    def remote_debugging_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "remoteDebuggingEnabled"))

    @remote_debugging_enabled.setter
    def remote_debugging_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44411c374399a05d3b19901064927051d235ef48d00c102463c21496b1a0c123)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteDebuggingEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remoteDebuggingVersion")
    def remote_debugging_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteDebuggingVersion"))

    @remote_debugging_version.setter
    def remote_debugging_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f70c2c5b7f6cab1df44ac15d49c757bed15ee5ef83b1cd9e92cc1f106f87201)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteDebuggingVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeScaleMonitoringEnabled")
    def runtime_scale_monitoring_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "runtimeScaleMonitoringEnabled"))

    @runtime_scale_monitoring_enabled.setter
    def runtime_scale_monitoring_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63534a787f782a35ab7fb2e46283600a1662e299467e7bdc53eb65e50ae2bb6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeScaleMonitoringEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scmIpRestrictionDefaultAction")
    def scm_ip_restriction_default_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scmIpRestrictionDefaultAction"))

    @scm_ip_restriction_default_action.setter
    def scm_ip_restriction_default_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89a03188383bc06eb697eaf4a4308a5a3149ca3c371e25676dd4c9b6a4f52397)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scmIpRestrictionDefaultAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scmMinimumTlsVersion")
    def scm_minimum_tls_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scmMinimumTlsVersion"))

    @scm_minimum_tls_version.setter
    def scm_minimum_tls_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28a7e1072572fac92f0f7687ca524a3a8febdfde4f7dd2c9fd95b65a87917842)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scmMinimumTlsVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scmUseMainIpRestriction")
    def scm_use_main_ip_restriction(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "scmUseMainIpRestriction"))

    @scm_use_main_ip_restriction.setter
    def scm_use_main_ip_restriction(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f573a72b26d542684ee851d64e442d067f99c9692bf13a1ad5601a8b91300e86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scmUseMainIpRestriction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="use32BitWorker")
    def use32_bit_worker(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "use32BitWorker"))

    @use32_bit_worker.setter
    def use32_bit_worker(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b27d048215f3e84092819b20ba1048ef8ec76fd632d64fa3071b23434dfca29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "use32BitWorker", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vnetRouteAllEnabled")
    def vnet_route_all_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "vnetRouteAllEnabled"))

    @vnet_route_all_enabled.setter
    def vnet_route_all_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a6354706637e88ca8af4d7fb90cd27080a28577be589349a9dd3c0a1e783cab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vnetRouteAllEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="websocketsEnabled")
    def websockets_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "websocketsEnabled"))

    @websockets_enabled.setter
    def websockets_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2212bd8de7e82029321adf2b48160235520690a4653d78c63c4be89229ea8308)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "websocketsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workerCount")
    def worker_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "workerCount"))

    @worker_count.setter
    def worker_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__177e17b3fc5aa99ae0d1304f263ce23b34ee4c06255b3930092c671a2b69844e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workerCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LinuxFunctionAppSlotSiteConfig]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotSiteConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LinuxFunctionAppSlotSiteConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4d02f6c531fee6bb538f2dab91ee815ffe2d953a6c54601cd2d276690a80621)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotSiteConfigScmIpRestriction",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "description": "description",
        "headers": "headers",
        "ip_address": "ipAddress",
        "name": "name",
        "priority": "priority",
        "service_tag": "serviceTag",
        "virtual_network_subnet_id": "virtualNetworkSubnetId",
    },
)
class LinuxFunctionAppSlotSiteConfigScmIpRestriction:
    def __init__(
        self,
        *,
        action: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LinuxFunctionAppSlotSiteConfigScmIpRestrictionHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ip_address: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        service_tag: typing.Optional[builtins.str] = None,
        virtual_network_subnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action: The action to take. Possible values are ``Allow`` or ``Deny``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#action LinuxFunctionAppSlot#action}
        :param description: The description of the IP restriction rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#description LinuxFunctionAppSlot#description}
        :param headers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#headers LinuxFunctionAppSlot#headers}.
        :param ip_address: The CIDR notation of the IP or IP Range to match. For example: ``10.0.0.0/24`` or ``192.168.10.1/32`` or ``fe80::/64`` or ``13.107.6.152/31,13.107.128.0/22`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#ip_address LinuxFunctionAppSlot#ip_address}
        :param name: The name which should be used for this ``ip_restriction``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#name LinuxFunctionAppSlot#name}
        :param priority: The priority value of this ``ip_restriction``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#priority LinuxFunctionAppSlot#priority}
        :param service_tag: The Service Tag used for this IP Restriction. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#service_tag LinuxFunctionAppSlot#service_tag}
        :param virtual_network_subnet_id: The Virtual Network Subnet ID used for this IP Restriction. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#virtual_network_subnet_id LinuxFunctionAppSlot#virtual_network_subnet_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24a3a5f6181c88a36b713b81816ee4d56bfcc2c37c4131adf5264b3ba8f6b05b)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
            check_type(argname="argument ip_address", value=ip_address, expected_type=type_hints["ip_address"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument service_tag", value=service_tag, expected_type=type_hints["service_tag"])
            check_type(argname="argument virtual_network_subnet_id", value=virtual_network_subnet_id, expected_type=type_hints["virtual_network_subnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action is not None:
            self._values["action"] = action
        if description is not None:
            self._values["description"] = description
        if headers is not None:
            self._values["headers"] = headers
        if ip_address is not None:
            self._values["ip_address"] = ip_address
        if name is not None:
            self._values["name"] = name
        if priority is not None:
            self._values["priority"] = priority
        if service_tag is not None:
            self._values["service_tag"] = service_tag
        if virtual_network_subnet_id is not None:
            self._values["virtual_network_subnet_id"] = virtual_network_subnet_id

    @builtins.property
    def action(self) -> typing.Optional[builtins.str]:
        '''The action to take. Possible values are ``Allow`` or ``Deny``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#action LinuxFunctionAppSlot#action}
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the IP restriction rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#description LinuxFunctionAppSlot#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LinuxFunctionAppSlotSiteConfigScmIpRestrictionHeaders"]]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#headers LinuxFunctionAppSlot#headers}.'''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LinuxFunctionAppSlotSiteConfigScmIpRestrictionHeaders"]]], result)

    @builtins.property
    def ip_address(self) -> typing.Optional[builtins.str]:
        '''The CIDR notation of the IP or IP Range to match.

        For example: ``10.0.0.0/24`` or ``192.168.10.1/32`` or ``fe80::/64`` or ``13.107.6.152/31,13.107.128.0/22``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#ip_address LinuxFunctionAppSlot#ip_address}
        '''
        result = self._values.get("ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name which should be used for this ``ip_restriction``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#name LinuxFunctionAppSlot#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''The priority value of this ``ip_restriction``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#priority LinuxFunctionAppSlot#priority}
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service_tag(self) -> typing.Optional[builtins.str]:
        '''The Service Tag used for this IP Restriction.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#service_tag LinuxFunctionAppSlot#service_tag}
        '''
        result = self._values.get("service_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def virtual_network_subnet_id(self) -> typing.Optional[builtins.str]:
        '''The Virtual Network Subnet ID used for this IP Restriction.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#virtual_network_subnet_id LinuxFunctionAppSlot#virtual_network_subnet_id}
        '''
        result = self._values.get("virtual_network_subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotSiteConfigScmIpRestriction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotSiteConfigScmIpRestrictionHeaders",
    jsii_struct_bases=[],
    name_mapping={
        "x_azure_fdid": "xAzureFdid",
        "x_fd_health_probe": "xFdHealthProbe",
        "x_forwarded_for": "xForwardedFor",
        "x_forwarded_host": "xForwardedHost",
    },
)
class LinuxFunctionAppSlotSiteConfigScmIpRestrictionHeaders:
    def __init__(
        self,
        *,
        x_azure_fdid: typing.Optional[typing.Sequence[builtins.str]] = None,
        x_fd_health_probe: typing.Optional[typing.Sequence[builtins.str]] = None,
        x_forwarded_for: typing.Optional[typing.Sequence[builtins.str]] = None,
        x_forwarded_host: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param x_azure_fdid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#x_azure_fdid LinuxFunctionAppSlot#x_azure_fdid}.
        :param x_fd_health_probe: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#x_fd_health_probe LinuxFunctionAppSlot#x_fd_health_probe}.
        :param x_forwarded_for: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#x_forwarded_for LinuxFunctionAppSlot#x_forwarded_for}.
        :param x_forwarded_host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#x_forwarded_host LinuxFunctionAppSlot#x_forwarded_host}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5217b9a98433bba6c41fcf3fc0bf2d63d8fe291322dc344655336aae01951e6)
            check_type(argname="argument x_azure_fdid", value=x_azure_fdid, expected_type=type_hints["x_azure_fdid"])
            check_type(argname="argument x_fd_health_probe", value=x_fd_health_probe, expected_type=type_hints["x_fd_health_probe"])
            check_type(argname="argument x_forwarded_for", value=x_forwarded_for, expected_type=type_hints["x_forwarded_for"])
            check_type(argname="argument x_forwarded_host", value=x_forwarded_host, expected_type=type_hints["x_forwarded_host"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if x_azure_fdid is not None:
            self._values["x_azure_fdid"] = x_azure_fdid
        if x_fd_health_probe is not None:
            self._values["x_fd_health_probe"] = x_fd_health_probe
        if x_forwarded_for is not None:
            self._values["x_forwarded_for"] = x_forwarded_for
        if x_forwarded_host is not None:
            self._values["x_forwarded_host"] = x_forwarded_host

    @builtins.property
    def x_azure_fdid(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#x_azure_fdid LinuxFunctionAppSlot#x_azure_fdid}.'''
        result = self._values.get("x_azure_fdid")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def x_fd_health_probe(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#x_fd_health_probe LinuxFunctionAppSlot#x_fd_health_probe}.'''
        result = self._values.get("x_fd_health_probe")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def x_forwarded_for(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#x_forwarded_for LinuxFunctionAppSlot#x_forwarded_for}.'''
        result = self._values.get("x_forwarded_for")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def x_forwarded_host(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#x_forwarded_host LinuxFunctionAppSlot#x_forwarded_host}.'''
        result = self._values.get("x_forwarded_host")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotSiteConfigScmIpRestrictionHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LinuxFunctionAppSlotSiteConfigScmIpRestrictionHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotSiteConfigScmIpRestrictionHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__86680d7cd71c9ae5400d573401629695d56bbc00adb88e0218716b5ce3ddeeaf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LinuxFunctionAppSlotSiteConfigScmIpRestrictionHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61ec907a40d8674b913a90581aeee914699e1ee97c1fd8bffe2b9c9f4c779cc2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LinuxFunctionAppSlotSiteConfigScmIpRestrictionHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51bb60f8a757491386d80fcc77dbaf9956881edb57a58de11453d9ecefbb24fe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62176d54f8458b20c8b41d20da4111b64a0f05e461f06e0bff0d4d9695a7d11b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__678bbc0a431ce4c063f92a4deda69e88afdfbb438bc06d195455d56f54776440)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotSiteConfigScmIpRestrictionHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotSiteConfigScmIpRestrictionHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotSiteConfigScmIpRestrictionHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d79d388fa67e9a388e1493495d363512e691dfb24d58c6fa64428e8f7c3b839)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LinuxFunctionAppSlotSiteConfigScmIpRestrictionHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotSiteConfigScmIpRestrictionHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73c96adda532eb5eadab8c99f39ebc6c7e2649d0285972fa72bb27161bcfb10a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetXAzureFdid")
    def reset_x_azure_fdid(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetXAzureFdid", []))

    @jsii.member(jsii_name="resetXFdHealthProbe")
    def reset_x_fd_health_probe(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetXFdHealthProbe", []))

    @jsii.member(jsii_name="resetXForwardedFor")
    def reset_x_forwarded_for(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetXForwardedFor", []))

    @jsii.member(jsii_name="resetXForwardedHost")
    def reset_x_forwarded_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetXForwardedHost", []))

    @builtins.property
    @jsii.member(jsii_name="xAzureFdidInput")
    def x_azure_fdid_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "xAzureFdidInput"))

    @builtins.property
    @jsii.member(jsii_name="xFdHealthProbeInput")
    def x_fd_health_probe_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "xFdHealthProbeInput"))

    @builtins.property
    @jsii.member(jsii_name="xForwardedForInput")
    def x_forwarded_for_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "xForwardedForInput"))

    @builtins.property
    @jsii.member(jsii_name="xForwardedHostInput")
    def x_forwarded_host_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "xForwardedHostInput"))

    @builtins.property
    @jsii.member(jsii_name="xAzureFdid")
    def x_azure_fdid(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "xAzureFdid"))

    @x_azure_fdid.setter
    def x_azure_fdid(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6791c3485ca2d62d16aa60ca2c93b7c9acfbfe7a984dda3b94cba05f379b8e13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "xAzureFdid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="xFdHealthProbe")
    def x_fd_health_probe(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "xFdHealthProbe"))

    @x_fd_health_probe.setter
    def x_fd_health_probe(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26b93132d15d29adc03cb139768b34fb432701010b115be9047c5dfb43d39be7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "xFdHealthProbe", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="xForwardedFor")
    def x_forwarded_for(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "xForwardedFor"))

    @x_forwarded_for.setter
    def x_forwarded_for(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04a295a236226b4b45abb5a2e3654019caca7d5294f3ccff4b08c6331b8db3e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "xForwardedFor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="xForwardedHost")
    def x_forwarded_host(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "xForwardedHost"))

    @x_forwarded_host.setter
    def x_forwarded_host(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4010a5ef5c99012ace28bd55e599bfdf459a071d90cb2d71d7971275a6292488)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "xForwardedHost", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotSiteConfigScmIpRestrictionHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotSiteConfigScmIpRestrictionHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotSiteConfigScmIpRestrictionHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c8779dd731eb8f329afe4bb62d99b998d259414a570682ff97d578bbe8298be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LinuxFunctionAppSlotSiteConfigScmIpRestrictionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotSiteConfigScmIpRestrictionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bee19a6c463b0a0c76d0ad2039cb0434b6ab4d823719a323d918e72d91ec92bc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LinuxFunctionAppSlotSiteConfigScmIpRestrictionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47db1868e90d328889f66c6168b5b90d3c5fca042b7136b41d163c0874b72b79)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LinuxFunctionAppSlotSiteConfigScmIpRestrictionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97be545db9e5831fa6bfc00fa1b50718de2c8d4057d9f1a3973937626477b0a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0499db163bb5abe428af1f753e9e4ff3aafa25405cf37d9a84985adf76c5f8a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f4a544f29ae182b84a2ef3331eba48220378d05820f456391c56e35b8ca2ba6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotSiteConfigScmIpRestriction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotSiteConfigScmIpRestriction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotSiteConfigScmIpRestriction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bb2bca8a946e18640620f7120dd2092f7dab7d2eac632199bd2e362265c3084)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LinuxFunctionAppSlotSiteConfigScmIpRestrictionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotSiteConfigScmIpRestrictionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8f8f278448c47d99647b07af350627d8b32c885642b318e4889aeb76b10ebeb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHeaders")
    def put_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LinuxFunctionAppSlotSiteConfigScmIpRestrictionHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78c7b8317f515a3bf56bc4cbe5fb8068f6d31c17b1149bba16eaa4c3be6e9f4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeaders", [value]))

    @jsii.member(jsii_name="resetAction")
    def reset_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAction", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetHeaders")
    def reset_headers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeaders", []))

    @jsii.member(jsii_name="resetIpAddress")
    def reset_ip_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpAddress", []))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetServiceTag")
    def reset_service_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceTag", []))

    @jsii.member(jsii_name="resetVirtualNetworkSubnetId")
    def reset_virtual_network_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualNetworkSubnetId", []))

    @builtins.property
    @jsii.member(jsii_name="headers")
    def headers(self) -> LinuxFunctionAppSlotSiteConfigScmIpRestrictionHeadersList:
        return typing.cast(LinuxFunctionAppSlotSiteConfigScmIpRestrictionHeadersList, jsii.get(self, "headers"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="headersInput")
    def headers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotSiteConfigScmIpRestrictionHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotSiteConfigScmIpRestrictionHeaders]]], jsii.get(self, "headersInput"))

    @builtins.property
    @jsii.member(jsii_name="ipAddressInput")
    def ip_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ipAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceTagInput")
    def service_tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceTagInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkSubnetIdInput")
    def virtual_network_subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualNetworkSubnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e29b9e837a5e624a0071075b4592d1c2ef35133467cb43d762ca2f8034b0e47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d035ee76d5022da13396b0f8eb7f1f1a2c44cf1e3470d1057a0fe6b38c38ec4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fe44c25b2c4b90814a7d97d182b4b26c3c6d3a43bc8d6ec4c3415efd206b85a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcdccac011ae4e2ba2faff10c37187c0158c6a2e40f97a1aaabb6f2dd5ad1310)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81f52344b8cf11a5bb75c8d5568a0cce86001c149854009296c184531abfcc3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceTag")
    def service_tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceTag"))

    @service_tag.setter
    def service_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8c8f7c16e83f01dc4ce06c9283199420d93b4b3b0e0718d04b5fc49c85c7e6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceTag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkSubnetId")
    def virtual_network_subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkSubnetId"))

    @virtual_network_subnet_id.setter
    def virtual_network_subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5740f4983c783c7471419e76dafb3f2e41c78ef31ad6a94282bd3f5ff02f1c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkSubnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotSiteConfigScmIpRestriction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotSiteConfigScmIpRestriction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotSiteConfigScmIpRestriction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48c24aa4fbe4a5f0b21b6c4cae016fd205417675ff1b573630f2d3cc3504ff68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotSiteCredential",
    jsii_struct_bases=[],
    name_mapping={},
)
class LinuxFunctionAppSlotSiteCredential:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotSiteCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LinuxFunctionAppSlotSiteCredentialList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotSiteCredentialList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea665609d66872069bd414f11891e63b65ed8fa4b5265ae54ac37e031bc1c6ef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LinuxFunctionAppSlotSiteCredentialOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8358b4f76a0398bf9bdb17c811610ba7998274adb66a6dc5e137acc092459716)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LinuxFunctionAppSlotSiteCredentialOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6677e171f6c522738ae3858b86ab883d58e9a86676e3f0fa7a4e1f8785f42fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aaf65d5e1d196707c447b0ff7783a819aefb329d87af551a0ea811d3c7cb0dd2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__391ea2bee5dfacd2fe4c0bca275e98902c4dbb3c0a83d420a3dd96df2c98bb9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class LinuxFunctionAppSlotSiteCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotSiteCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__753c0e849c7f11b3ff0f6cefe744de05295818f5df1bf1ff4850b187fb34edef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LinuxFunctionAppSlotSiteCredential]:
        return typing.cast(typing.Optional[LinuxFunctionAppSlotSiteCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LinuxFunctionAppSlotSiteCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4296b5e5e9c388e1151d7f99bee07ec593c3d282cb61be8096b0673f0f4eb86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotStorageAccount",
    jsii_struct_bases=[],
    name_mapping={
        "access_key": "accessKey",
        "account_name": "accountName",
        "name": "name",
        "share_name": "shareName",
        "type": "type",
        "mount_path": "mountPath",
    },
)
class LinuxFunctionAppSlotStorageAccount:
    def __init__(
        self,
        *,
        access_key: builtins.str,
        account_name: builtins.str,
        name: builtins.str,
        share_name: builtins.str,
        type: builtins.str,
        mount_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param access_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#access_key LinuxFunctionAppSlot#access_key}.
        :param account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#account_name LinuxFunctionAppSlot#account_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#name LinuxFunctionAppSlot#name}.
        :param share_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#share_name LinuxFunctionAppSlot#share_name}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#type LinuxFunctionAppSlot#type}.
        :param mount_path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#mount_path LinuxFunctionAppSlot#mount_path}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66e2738789ab96656c42fe63a287a95cf4d66b6ea3b1961abcd5361699384a56)
            check_type(argname="argument access_key", value=access_key, expected_type=type_hints["access_key"])
            check_type(argname="argument account_name", value=account_name, expected_type=type_hints["account_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument share_name", value=share_name, expected_type=type_hints["share_name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument mount_path", value=mount_path, expected_type=type_hints["mount_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "access_key": access_key,
            "account_name": account_name,
            "name": name,
            "share_name": share_name,
            "type": type,
        }
        if mount_path is not None:
            self._values["mount_path"] = mount_path

    @builtins.property
    def access_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#access_key LinuxFunctionAppSlot#access_key}.'''
        result = self._values.get("access_key")
        assert result is not None, "Required property 'access_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#account_name LinuxFunctionAppSlot#account_name}.'''
        result = self._values.get("account_name")
        assert result is not None, "Required property 'account_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#name LinuxFunctionAppSlot#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def share_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#share_name LinuxFunctionAppSlot#share_name}.'''
        result = self._values.get("share_name")
        assert result is not None, "Required property 'share_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#type LinuxFunctionAppSlot#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mount_path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#mount_path LinuxFunctionAppSlot#mount_path}.'''
        result = self._values.get("mount_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotStorageAccount(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LinuxFunctionAppSlotStorageAccountList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotStorageAccountList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b910c59a4bea6c8f8fc47a54dccdcfaba9d5c446030d6ccc343977297da606ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LinuxFunctionAppSlotStorageAccountOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94661b3d842ac51772ed6bfc35cd93576f68357c66c464a893d5351d02a7a14a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LinuxFunctionAppSlotStorageAccountOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32554e8513276ee64faeaf7e8210ecaa3a0c6f05d2268a2b751cef14dc0b5fc9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__791896a42bbdc1a79f0968d3883b5de4322aaa6ee8600133ca704b138aaba8e3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__914e9aef43b76a5de261ab93a4f08c84240e39775343485588438edbbf244faf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotStorageAccount]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotStorageAccount]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotStorageAccount]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1273f642ced8cc803fe7576741b9c00f13cb9a2ad7c268dc72d26701e64a6a2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LinuxFunctionAppSlotStorageAccountOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotStorageAccountOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__868a025df05f98f7e41bea307804ba39638c458fe75ea09af0f1af6a678d6e35)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMountPath")
    def reset_mount_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMountPath", []))

    @builtins.property
    @jsii.member(jsii_name="accessKeyInput")
    def access_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="accountNameInput")
    def account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="mountPathInput")
    def mount_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mountPathInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="shareNameInput")
    def share_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "shareNameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="accessKey")
    def access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accessKey"))

    @access_key.setter
    def access_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25d9f3d98b0d068f39ae25ebd0a32064a5b763814327fe25ed2173b61498953e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="accountName")
    def account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountName"))

    @account_name.setter
    def account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6677a7093a9786fd0c617b713b003308767d2faf80d8bcd09f523aa444662306)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mountPath")
    def mount_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mountPath"))

    @mount_path.setter
    def mount_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5708f7c457648718f034c67082e45b3dce585e2fde79b52a4b115b8d7ccf236)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mountPath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a77d06deeaf14907a64aa69a26de51f880768eb9ce4639552d73f5fbbe4bb716)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="shareName")
    def share_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "shareName"))

    @share_name.setter
    def share_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bab8d20e5727e7a1e11df821cb8e514be09d41f77f63e9e98dbe90ee22f10a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "shareName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__839f7b0f06abd14d1defcb82ca6a8172611e8a4fd46c9b4cecc8ec785313f1f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotStorageAccount]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotStorageAccount]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotStorageAccount]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da3e6118f1df9de6cf3529ac07326dfb921e0e8c0c9e71e0bad0f34a4f20a771)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class LinuxFunctionAppSlotTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#create LinuxFunctionAppSlot#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#delete LinuxFunctionAppSlot#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#read LinuxFunctionAppSlot#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#update LinuxFunctionAppSlot#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30402b4c8cbe125cea62ac89e50a912641916e4a16a7ebb4d7af78dfd2cdc42f)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#create LinuxFunctionAppSlot#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#delete LinuxFunctionAppSlot#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#read LinuxFunctionAppSlot#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/linux_function_app_slot#update LinuxFunctionAppSlot#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinuxFunctionAppSlotTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LinuxFunctionAppSlotTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.linuxFunctionAppSlot.LinuxFunctionAppSlotTimeoutsOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9d166d4550efdb17462790ba02c21890e849787866edcd0ddf287905dd2abbd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5364dff727f7d8e7340861257a4b082c9394858532480c54f6caa7f68c9a195)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2ceb0422f9a2d93f2d9ea08f1ce4f072257802b7bae8146722fd808041f5817)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9e700a0872d7307b59a694348447f37d0e3ca73bac42238ac0ffcc8f5d327f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a00811a0df305d5e1ed87a3fa378f01f45dac504a3e7282acde3813b5fe3d6ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe01daf3c8dc33e555afbf2d2fde2f81fbc4f493d6187aefb0ea68c16571e7bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "LinuxFunctionAppSlot",
    "LinuxFunctionAppSlotAuthSettings",
    "LinuxFunctionAppSlotAuthSettingsActiveDirectory",
    "LinuxFunctionAppSlotAuthSettingsActiveDirectoryOutputReference",
    "LinuxFunctionAppSlotAuthSettingsFacebook",
    "LinuxFunctionAppSlotAuthSettingsFacebookOutputReference",
    "LinuxFunctionAppSlotAuthSettingsGithub",
    "LinuxFunctionAppSlotAuthSettingsGithubOutputReference",
    "LinuxFunctionAppSlotAuthSettingsGoogle",
    "LinuxFunctionAppSlotAuthSettingsGoogleOutputReference",
    "LinuxFunctionAppSlotAuthSettingsMicrosoft",
    "LinuxFunctionAppSlotAuthSettingsMicrosoftOutputReference",
    "LinuxFunctionAppSlotAuthSettingsOutputReference",
    "LinuxFunctionAppSlotAuthSettingsTwitter",
    "LinuxFunctionAppSlotAuthSettingsTwitterOutputReference",
    "LinuxFunctionAppSlotAuthSettingsV2",
    "LinuxFunctionAppSlotAuthSettingsV2ActiveDirectoryV2",
    "LinuxFunctionAppSlotAuthSettingsV2ActiveDirectoryV2OutputReference",
    "LinuxFunctionAppSlotAuthSettingsV2AppleV2",
    "LinuxFunctionAppSlotAuthSettingsV2AppleV2OutputReference",
    "LinuxFunctionAppSlotAuthSettingsV2AzureStaticWebAppV2",
    "LinuxFunctionAppSlotAuthSettingsV2AzureStaticWebAppV2OutputReference",
    "LinuxFunctionAppSlotAuthSettingsV2CustomOidcV2",
    "LinuxFunctionAppSlotAuthSettingsV2CustomOidcV2List",
    "LinuxFunctionAppSlotAuthSettingsV2CustomOidcV2OutputReference",
    "LinuxFunctionAppSlotAuthSettingsV2FacebookV2",
    "LinuxFunctionAppSlotAuthSettingsV2FacebookV2OutputReference",
    "LinuxFunctionAppSlotAuthSettingsV2GithubV2",
    "LinuxFunctionAppSlotAuthSettingsV2GithubV2OutputReference",
    "LinuxFunctionAppSlotAuthSettingsV2GoogleV2",
    "LinuxFunctionAppSlotAuthSettingsV2GoogleV2OutputReference",
    "LinuxFunctionAppSlotAuthSettingsV2Login",
    "LinuxFunctionAppSlotAuthSettingsV2LoginOutputReference",
    "LinuxFunctionAppSlotAuthSettingsV2MicrosoftV2",
    "LinuxFunctionAppSlotAuthSettingsV2MicrosoftV2OutputReference",
    "LinuxFunctionAppSlotAuthSettingsV2OutputReference",
    "LinuxFunctionAppSlotAuthSettingsV2TwitterV2",
    "LinuxFunctionAppSlotAuthSettingsV2TwitterV2OutputReference",
    "LinuxFunctionAppSlotBackup",
    "LinuxFunctionAppSlotBackupOutputReference",
    "LinuxFunctionAppSlotBackupSchedule",
    "LinuxFunctionAppSlotBackupScheduleOutputReference",
    "LinuxFunctionAppSlotConfig",
    "LinuxFunctionAppSlotConnectionString",
    "LinuxFunctionAppSlotConnectionStringList",
    "LinuxFunctionAppSlotConnectionStringOutputReference",
    "LinuxFunctionAppSlotIdentity",
    "LinuxFunctionAppSlotIdentityOutputReference",
    "LinuxFunctionAppSlotSiteConfig",
    "LinuxFunctionAppSlotSiteConfigAppServiceLogs",
    "LinuxFunctionAppSlotSiteConfigAppServiceLogsOutputReference",
    "LinuxFunctionAppSlotSiteConfigApplicationStack",
    "LinuxFunctionAppSlotSiteConfigApplicationStackDocker",
    "LinuxFunctionAppSlotSiteConfigApplicationStackDockerList",
    "LinuxFunctionAppSlotSiteConfigApplicationStackDockerOutputReference",
    "LinuxFunctionAppSlotSiteConfigApplicationStackOutputReference",
    "LinuxFunctionAppSlotSiteConfigCors",
    "LinuxFunctionAppSlotSiteConfigCorsOutputReference",
    "LinuxFunctionAppSlotSiteConfigIpRestriction",
    "LinuxFunctionAppSlotSiteConfigIpRestrictionHeaders",
    "LinuxFunctionAppSlotSiteConfigIpRestrictionHeadersList",
    "LinuxFunctionAppSlotSiteConfigIpRestrictionHeadersOutputReference",
    "LinuxFunctionAppSlotSiteConfigIpRestrictionList",
    "LinuxFunctionAppSlotSiteConfigIpRestrictionOutputReference",
    "LinuxFunctionAppSlotSiteConfigOutputReference",
    "LinuxFunctionAppSlotSiteConfigScmIpRestriction",
    "LinuxFunctionAppSlotSiteConfigScmIpRestrictionHeaders",
    "LinuxFunctionAppSlotSiteConfigScmIpRestrictionHeadersList",
    "LinuxFunctionAppSlotSiteConfigScmIpRestrictionHeadersOutputReference",
    "LinuxFunctionAppSlotSiteConfigScmIpRestrictionList",
    "LinuxFunctionAppSlotSiteConfigScmIpRestrictionOutputReference",
    "LinuxFunctionAppSlotSiteCredential",
    "LinuxFunctionAppSlotSiteCredentialList",
    "LinuxFunctionAppSlotSiteCredentialOutputReference",
    "LinuxFunctionAppSlotStorageAccount",
    "LinuxFunctionAppSlotStorageAccountList",
    "LinuxFunctionAppSlotStorageAccountOutputReference",
    "LinuxFunctionAppSlotTimeouts",
    "LinuxFunctionAppSlotTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__78df0419662a3e06e4f514a5d781b72538709f9932eaae4a4f6c5940d9fbecc0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    function_app_id: builtins.str,
    name: builtins.str,
    site_config: typing.Union[LinuxFunctionAppSlotSiteConfig, typing.Dict[builtins.str, typing.Any]],
    app_settings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    auth_settings: typing.Optional[typing.Union[LinuxFunctionAppSlotAuthSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    auth_settings_v2: typing.Optional[typing.Union[LinuxFunctionAppSlotAuthSettingsV2, typing.Dict[builtins.str, typing.Any]]] = None,
    backup: typing.Optional[typing.Union[LinuxFunctionAppSlotBackup, typing.Dict[builtins.str, typing.Any]]] = None,
    builtin_logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_certificate_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_certificate_exclusion_paths: typing.Optional[builtins.str] = None,
    client_certificate_mode: typing.Optional[builtins.str] = None,
    connection_string: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LinuxFunctionAppSlotConnectionString, typing.Dict[builtins.str, typing.Any]]]]] = None,
    content_share_force_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    daily_memory_time_quota: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ftp_publish_basic_authentication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    functions_extension_version: typing.Optional[builtins.str] = None,
    https_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[LinuxFunctionAppSlotIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    key_vault_reference_identity_id: typing.Optional[builtins.str] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    service_plan_id: typing.Optional[builtins.str] = None,
    storage_account: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LinuxFunctionAppSlotStorageAccount, typing.Dict[builtins.str, typing.Any]]]]] = None,
    storage_account_access_key: typing.Optional[builtins.str] = None,
    storage_account_name: typing.Optional[builtins.str] = None,
    storage_key_vault_secret_id: typing.Optional[builtins.str] = None,
    storage_uses_managed_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[LinuxFunctionAppSlotTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_network_backup_restore_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    virtual_network_subnet_id: typing.Optional[builtins.str] = None,
    vnet_image_pull_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    webdeploy_publish_basic_authentication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__1ab1e0843eb08debf9e943c8639d6c59440e40f1e9ed376ebcc43567b7abecc6(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7990af5003871d0e8a0a991327e4104d3161383ad27c45e47af5e6042eec787f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LinuxFunctionAppSlotConnectionString, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d5f3fde315b4bc3d9aa5bb90eb97f4718be8c7ff7f6bd5e3d35c142bc4eb19a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LinuxFunctionAppSlotStorageAccount, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa604fa0b3da185a6c3585ce559531c5aa994c66e0a3554b8e219b372c22b44d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f029c15f87483faeff23949ed3e1e488ace2529fb2c9f2c4b019fbc4ee1c333(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ac4d056771532a4a4cebbe26558de52c3358f121edb6d2cc374697c29703463(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b59fe8b3c06e46ec0357ef37fc5db3ba98eca21e1f95e3689d49c2c4168d3e79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f85b35dce986505903dc5dfaf2821df1c1419c88351770ee87ea88ba62a007e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__225d802254c0a0f5d3c1b7a8bb94e3f07f7640a2bc1dc1b3aa468d7754796f05(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72563994f81a07e9472b1e7a66078fbaa9513b0008db6cfc6a2824c73e5bbe24(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d91cabea7bbd9434eaadc2469d5cfb679c4e37d06483498370bed867690bc60(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__838bf1886db7a66af93c96892dea18d1e8d15a3752aa4962af20277860c2fff9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5cb7bfb5260e2ae57a538a44c50c4c8534d7b1e8e6d88da53e31898782849e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a13e732252f18ec7810da0aca8ad793f5b53c8978d6d51a076b8378f563abd00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11aa8338f3c3937bbdc5bebb8462fbc39a6e9f641a9ba3254b5c774d8a41a6a9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86ba1724106db3333d9cd00875872f9e81ac2d5743e357be79569eafdc91f37c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__728a26fa49201905f106f0a4cbbffacba36b7a4e4cb4eda3d6aa20d4a71cad45(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea798b3118a5c5ef774db0addf8e3ace14e55a22dd3f1d5fb43d2ebadc256e38(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf428b6ccbc0486462a14c2acf6e535cd8f9ace6ea58e254a69035827a933843(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51d882abee194b112fe9bf241fbb14bd70166ceb82710a1dfb22c5713237ec27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cadbdfa274bddf868efa2c8e78d9bad7f62aaed4ef3050f01dbab2cbf3a34788(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a19aafa7deae0233ee064d64aba7636eef7c4a99325534762074200fa7dfd2c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f57aadfd8056829d12978d6e3c0deaff46d9db31794ded5f22f5f6e9b0515c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f61511be1ed233d174620fbc622a6fe8620215e74b36de921265b03246cf6923(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__834ead9eb54c179b92c6af6a50427e0e4d463dcd5fe3e77cd59f2b3402d55faa(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e0921a9e1b51e14e8c77ca4e5ef6cd3068722c5c85163087b5209b2654bc414(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb430714bfaa0f6fd9e4c9e4d20990c1c840c36fbbf93073557aea70c5cae4ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__001bd18f55fac43c5ec603afc17161d630fdc3c94db85141be6b105ad1279090(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2efab8c919e07809e3889d7c8b0bf0ea2442041a28ddcd6c092af63f7c356aa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9f434d3380681049777a602ae400de79c9711afec806ec4b54cc70f7028219e(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    active_directory: typing.Optional[typing.Union[LinuxFunctionAppSlotAuthSettingsActiveDirectory, typing.Dict[builtins.str, typing.Any]]] = None,
    additional_login_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    allowed_external_redirect_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
    default_provider: typing.Optional[builtins.str] = None,
    facebook: typing.Optional[typing.Union[LinuxFunctionAppSlotAuthSettingsFacebook, typing.Dict[builtins.str, typing.Any]]] = None,
    github: typing.Optional[typing.Union[LinuxFunctionAppSlotAuthSettingsGithub, typing.Dict[builtins.str, typing.Any]]] = None,
    google: typing.Optional[typing.Union[LinuxFunctionAppSlotAuthSettingsGoogle, typing.Dict[builtins.str, typing.Any]]] = None,
    issuer: typing.Optional[builtins.str] = None,
    microsoft: typing.Optional[typing.Union[LinuxFunctionAppSlotAuthSettingsMicrosoft, typing.Dict[builtins.str, typing.Any]]] = None,
    runtime_version: typing.Optional[builtins.str] = None,
    token_refresh_extension_hours: typing.Optional[jsii.Number] = None,
    token_store_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    twitter: typing.Optional[typing.Union[LinuxFunctionAppSlotAuthSettingsTwitter, typing.Dict[builtins.str, typing.Any]]] = None,
    unauthenticated_client_action: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__352d8cd74b2240944ed3004f6e4d3c13ff186b0fb1c95d938ee2cc9cb646dc83(
    *,
    client_id: builtins.str,
    allowed_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
    client_secret: typing.Optional[builtins.str] = None,
    client_secret_setting_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ff6e70fb544ace3d9f1e408b1db51cc3abb9330804f58cd5c4003f95cc677ad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31235fe242310bfac756370b39af68e26e4fd7eb6320cbedd595f7d5a47328b8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e6a9dec3ca09ca5897eb9d826a31ce2e48ca15a1f73cdbc3c65168c9e62db61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81dad42dd5973675430851c16af09e80d76b9cf9fac85e272b82bab92a679dc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8673149783fedd3285cbb70b9ae11878bb3cb70a132fd688439c45822f087d8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9d113893b02f558dabb46e3c587e3e97a79a786d8356e2af6e4e763be629a73(
    value: typing.Optional[LinuxFunctionAppSlotAuthSettingsActiveDirectory],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa44718e5ed4256e6d36f5b5355d9771751744288285f1596a7f76d007973f3e(
    *,
    app_id: builtins.str,
    app_secret: typing.Optional[builtins.str] = None,
    app_secret_setting_name: typing.Optional[builtins.str] = None,
    oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__583f00a8f247134ab910297e80d04ab63fdd005c3e28f744fc7454b7de7a09a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8b43644535823a90236a5e4327b5cf24a1e590a1ff519b523dbe43e6a80fd51(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04e1369f0e47e239c9ee1f31fd302f67b2de8682fab8ee285760c76db3864059(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__659b546e53225d39af9d5af323fb910e0c8cbe130785a08c948f42507d43bdb1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa9ea48fe03adec41925c4e2e9dc3efb5437c67a9ad084f599ba7962d1d93f2a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8085f71925aa9b92f7b74ffaa7744edfa0198d2b940c158c4f9a24cdb68ba7f(
    value: typing.Optional[LinuxFunctionAppSlotAuthSettingsFacebook],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92da1b48820dd2f5297bc224c5c43edb74f40c29910580ccaeaeda324cc31758(
    *,
    client_id: builtins.str,
    client_secret: typing.Optional[builtins.str] = None,
    client_secret_setting_name: typing.Optional[builtins.str] = None,
    oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__528b99ab8961a0c6668e8ee8cf82fbe4408e9118addac646a2dbd36944160fdb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cbcd86af02da8a205ff07502a82e8f5a9fa7b03adc314be38284f98213643d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c293dfc3574f6c58b4586e096ce6e97cb7849ff025ad9c9e8edcfecffbb68a06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af7709b5a4164bebbf81e82b7e1e43a99682ce13c3e515a2c1d0d91a8b3ef93e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0cd1d1773a17bc120d80378d6b0c83f91c863e755c6ad642d2010b73b2096a5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6088a41ed6752dce25adcc3126972ff044f5fb23d687194aad5d1904a58731b8(
    value: typing.Optional[LinuxFunctionAppSlotAuthSettingsGithub],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e6759ceccebd4003bc8cd48f565ec9da1b4f53677030bb3c06f81e5ade6cf50(
    *,
    client_id: builtins.str,
    client_secret: typing.Optional[builtins.str] = None,
    client_secret_setting_name: typing.Optional[builtins.str] = None,
    oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c085191d719b39b102936c421aa8b8333523b2e01818caff59ee027a04db1f34(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4551b40ad750bf40203155dcaf13e40e2f37839bc18c0cddc947b4c31cac1b8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d4931a28987e5a9921b22937e90f227d84a1dc94f25863c77e234edda9141dc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec2150f49d103e6da40bf3e2458418c05278913c159a566d47a3f4d871f80e63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59167e77e56018372047eea8ae3410ed8a92a4fb91b2f4d7b4928e77f4259ec5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__916ee439f412baecfe2bfd6ca234a3e56d8499e1a196bca76377342493a01461(
    value: typing.Optional[LinuxFunctionAppSlotAuthSettingsGoogle],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0616760984d9ea5fe43e2f8db042da8e59eab3a45b787feda4efb68b3a7b9293(
    *,
    client_id: builtins.str,
    client_secret: typing.Optional[builtins.str] = None,
    client_secret_setting_name: typing.Optional[builtins.str] = None,
    oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91b088aaa7d52cb7c9866959b035d57d0b3771e6d4a95f31c75c34b810f504e0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__978f4408addf7ae2bd3d10d3e6745d8781e3c270d61a7a175153ff450c52287b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25c849a5dd1a56380c13b0313e049d4c20bec74bafbb72b853bae5a03eba19cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3a9b10930336664c5d23a54c9fc13d0f36a5d35d838a589f04ec078aafa5f0e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93c88363f9870e3b6d31705047e57c1765a4e0b876488be787af5cfb6517604c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77751aff532d4497f46204f9bb8191a273c1e12b2dc5ae478766d5396626fcc1(
    value: typing.Optional[LinuxFunctionAppSlotAuthSettingsMicrosoft],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5de5ab83079e1618f2eb8b0fc27adf744215ce0d10734e57ecef5d212eff922e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fecce4709e8f10018c7c96049f7ced98e45e11e463e4cfd5b2787164bb1ef9cf(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b669cf79e46b338401b8b7f1f2926521ab39289b5b203be332421d9875f24b2(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abfddd83aa887d112a4898efdd4eed74c1ff82a937309cb47af7d7887e880870(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d95c98dce344db108dbea2a00ba539c09c529ee54161d2d02f8232b199619c30(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4668d702d405f80a1e3872ae7ce1d0e731dbc7bedb07202fe5484aae3c462088(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b21559a353643fd007bfe077fb63c737f5c2a54ccd035d5cb1c2b47ff95bde3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__720d83460b65b762445606979abc7cdea22af18912417e1f1397d3e9e05d998f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b53c81ba7a15ec630429189ece6e935cd96c5d4ce506bd2de7b4ecc81388073(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__499153c3cc46b162af385bafcf48a0a3c8aadbdbc2267b8c040acae7306dbf02(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a92b226f11b8e88897930a58b714756ed2a6edbcf0798a51b3bfa2569cf79e04(
    value: typing.Optional[LinuxFunctionAppSlotAuthSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__067f93dfb48d91364508d04f701128c7cc6d471272a59e4ed4859d16e0875259(
    *,
    consumer_key: builtins.str,
    consumer_secret: typing.Optional[builtins.str] = None,
    consumer_secret_setting_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f439f5104856bac8b3e5cb19c139b17cc264451fed3df19c73bcf4f243697b71(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__503fc36b3105008deead531e8b43459e845c71c5c877af7af833bd527087a3ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c33edb984b922090384d490df108277c3137952d45b7c4131dd37545d143d12b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6d70aa109bc40dbb83e61b05bcc1c5f91739c5a85aba84aaa6494bb29644c48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95cb95e1e5300ed71c94e89ee2b814949027039a60f930b120349fb04847b6aa(
    value: typing.Optional[LinuxFunctionAppSlotAuthSettingsTwitter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__450146a80d3fe33518a3cd30c442e10c1b0c483d11235ecef526fb1f169641bb(
    *,
    login: typing.Union[LinuxFunctionAppSlotAuthSettingsV2Login, typing.Dict[builtins.str, typing.Any]],
    active_directory_v2: typing.Optional[typing.Union[LinuxFunctionAppSlotAuthSettingsV2ActiveDirectoryV2, typing.Dict[builtins.str, typing.Any]]] = None,
    apple_v2: typing.Optional[typing.Union[LinuxFunctionAppSlotAuthSettingsV2AppleV2, typing.Dict[builtins.str, typing.Any]]] = None,
    auth_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    azure_static_web_app_v2: typing.Optional[typing.Union[LinuxFunctionAppSlotAuthSettingsV2AzureStaticWebAppV2, typing.Dict[builtins.str, typing.Any]]] = None,
    config_file_path: typing.Optional[builtins.str] = None,
    custom_oidc_v2: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LinuxFunctionAppSlotAuthSettingsV2CustomOidcV2, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_provider: typing.Optional[builtins.str] = None,
    excluded_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    facebook_v2: typing.Optional[typing.Union[LinuxFunctionAppSlotAuthSettingsV2FacebookV2, typing.Dict[builtins.str, typing.Any]]] = None,
    forward_proxy_convention: typing.Optional[builtins.str] = None,
    forward_proxy_custom_host_header_name: typing.Optional[builtins.str] = None,
    forward_proxy_custom_scheme_header_name: typing.Optional[builtins.str] = None,
    github_v2: typing.Optional[typing.Union[LinuxFunctionAppSlotAuthSettingsV2GithubV2, typing.Dict[builtins.str, typing.Any]]] = None,
    google_v2: typing.Optional[typing.Union[LinuxFunctionAppSlotAuthSettingsV2GoogleV2, typing.Dict[builtins.str, typing.Any]]] = None,
    http_route_api_prefix: typing.Optional[builtins.str] = None,
    microsoft_v2: typing.Optional[typing.Union[LinuxFunctionAppSlotAuthSettingsV2MicrosoftV2, typing.Dict[builtins.str, typing.Any]]] = None,
    require_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_https: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    runtime_version: typing.Optional[builtins.str] = None,
    twitter_v2: typing.Optional[typing.Union[LinuxFunctionAppSlotAuthSettingsV2TwitterV2, typing.Dict[builtins.str, typing.Any]]] = None,
    unauthenticated_action: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__720872c2e7f91103d4caa489d4966adfd8621efecf11d1f53117da1b9a2d430a(
    *,
    client_id: builtins.str,
    tenant_auth_endpoint: builtins.str,
    allowed_applications: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    allowed_identities: typing.Optional[typing.Sequence[builtins.str]] = None,
    client_secret_certificate_thumbprint: typing.Optional[builtins.str] = None,
    client_secret_setting_name: typing.Optional[builtins.str] = None,
    jwt_allowed_client_applications: typing.Optional[typing.Sequence[builtins.str]] = None,
    jwt_allowed_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    login_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    www_authentication_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f37170e1d99776caf2469fef37666e8e8a850e5fde8376026dbb2a1fd9c98dab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71617b6b5eb7e64131b71aba060cd24f38ec3cdf5a5b3b57dda1fb66331e517e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1967e32c08d41fa7186a3b17d6c0af721ed8fed141c71ba117a3d2c709fbf485(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a265bbfdca324afde1d7e48831da8222620dc6754a7772abfedb95d7e2efd68(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbe70f22e588bbb28ed0cc9e47216b671c498b0951b62f38c4b8d08ef9a83629(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42eb83cd5d330f41e626a25ce1f071a1c37f816c56b8b76cd96e9f2915343410(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af539259e9867f275803066f2822e2c5d8961951d47fbecd08ae166bbb9ae8f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b811913bff54670334cfbd9c9edf8fd44ff16352b1b2e65a9d40a83d3d77a757(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25c6fb6d22913ea0844251a22037d9ae6c6a2e90a840c9dc1c9b9a06208c248f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4a933800cf1f29c73ffc5dd730297232f40e76f1305fde12058c1c3c11ad139(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__420e6b0851e131b3ed555344ef284556a3359e114f506fafe56e6c0fdbc360e4(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f67805f728c67fe9823626a5fef9d22fe5d44fe3aa8efcfb91da25f14a423d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06eefa95604c63fa2c4a6b10e430dd59d34d954d7ef3f976f8cec7cf7fc60346(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7058b38f1082c0489a3d15244006a80b49fc7732ff2e82637b89f6e279e18348(
    value: typing.Optional[LinuxFunctionAppSlotAuthSettingsV2ActiveDirectoryV2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e9c515e9399106b81a2a5138548027c175543254ffbd5d6b94b0a284d31814a(
    *,
    client_id: builtins.str,
    client_secret_setting_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2e642c9d31ced2244df5c1e062ddee59b07198c0e502758d1396c797933d7f5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f83cb1bb3f07fb622d6392ed7c14dc0a5338c2ee6d93d3edc94bc008ed97858(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e41b089780b2ba491b38902bce60256cad8904a7a64d79848a638fa7ad2be6e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffca5e17e05d295550093443ee0ff93d8eaafe07ae1fd53f4dd65cc8e0a88631(
    value: typing.Optional[LinuxFunctionAppSlotAuthSettingsV2AppleV2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99a4e6e413dbc4d2c20ba609619902c3e9d8d7e6430af63e0eaa09f6fdf0351c(
    *,
    client_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a103c153c453f2a8663ddade02d0880f3c3fce989feda55772685fe38f045142(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64446197fd14537586b12611d4225f0983d27ceca85c99cdca5c93f588d0b112(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__654db6fafec10d1d1ee3e6c5beba2472f506afb56da943331f1075872f40c6c7(
    value: typing.Optional[LinuxFunctionAppSlotAuthSettingsV2AzureStaticWebAppV2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83d543532f436add229e3f7a7f7e0a76ab0cf9f709b54dfb23af294d2f053521(
    *,
    client_id: builtins.str,
    name: builtins.str,
    openid_configuration_endpoint: builtins.str,
    name_claim_type: typing.Optional[builtins.str] = None,
    scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c14d6682b6105021c92ce333153e2146fe7e68c628107a6721201cc4f4b49c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d80408fa765ac8b226b1567ecc9016bd685f065bad3397bb7bee04b3e98513dc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f05509d98a30c80a3e6e1559f52af9d89dfc63692074f7a73584856e0e578d2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9b565e4043418bef8b45c2b6d6a3c6e06a1cf8c78125635e4f0ebfc07640f45(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b160ebf81ef070f333fb13e71344cdb74f50748ba4104c3e528cd1103951ade(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de2bd1ad3918dc8045b3dbf2d8c562a3eb22eca0f4a46f12b9cac9386a3e6bcc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotAuthSettingsV2CustomOidcV2]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0d908006ff25d473e2421f7e91eaeb05a119dd900ec7455fb01d863aa5886b9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e3bf8b670aa073b994bf58654c66f1b96a59a446de64b38a74196cc42ddbeb8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7c940a013f7abb193388e2cf2bc6d738cb464464295314d425aaa2ec2bd15f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4ba29a371587739ebcf076c58525513a31465485843ec58b80c65f6365813a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cf9b4d548ddf3142c6bf160a1746aa2f1cd84aad4f12de8a8dafe74fb9faca5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55352c43927bf7306d8b724b84e5775ca49beb2fc9d32697eef56784d367b4d0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45b1e4c3a8eefdf8e296f72e4b6ccaa3ac168c1a0238c73734db1035cb600166(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotAuthSettingsV2CustomOidcV2]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa9b5e0d890e79da35cea3cd6ee1926d259be41f3933e6eb0408b4bee095dc10(
    *,
    app_id: builtins.str,
    app_secret_setting_name: builtins.str,
    graph_api_version: typing.Optional[builtins.str] = None,
    login_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30a7de1dfe4d10f9027caa0e620baeca2faf2001ff136a385d83abe37db3e5da(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__029b7824a8d5098f56546e60557ce4d7c60a2d395c47ea8e16ff67292114e972(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91f6a5369b23f52108801218138ca183de6bec2f37191bdfcecd364cc5fb1281(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a01818213d789ccd24de11fc14fff51cd6264961500be0271e160652b834f984(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c75fd2cea70ac0597afd8c33fd520f4d907c853a04e03651e52ef31bf3177bf0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc317b370dfd43884733e826e22c0cbb34788cf6eb32e443ac5e68c64d07b0ac(
    value: typing.Optional[LinuxFunctionAppSlotAuthSettingsV2FacebookV2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4b84cb00f7aa81495aad263a27b13c4aaa144844e60de5b893a3c1cd6dbbd18(
    *,
    client_id: builtins.str,
    client_secret_setting_name: builtins.str,
    login_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94658f2cf4229c3f63836f4c2fa288b59554e68253709e3db7c055db7b851f3e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fc1abfde06742120d25c7a289bfe71ed980256c4c03fec689860c71a6ba825d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0da9a8ed499183d062065e6f59a8ca7940ca7f795e5fbd0696ab956aa7db0ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f757e5b158403858d18cc01f1e78e75801017706efd6bbcf1b134fbed281a3cc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5d1711d343824facd359bfd7a4caf6a5e811cd372c8f091872c8488a616a922(
    value: typing.Optional[LinuxFunctionAppSlotAuthSettingsV2GithubV2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70389e8b7646dd92e349bc021698ef2d4627154e692f84d6c899c6038a62e6de(
    *,
    client_id: builtins.str,
    client_secret_setting_name: builtins.str,
    allowed_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
    login_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f4408c307e73eba8e0e94491fd37cb9bae2bbc90e58f3738366f27a6d375df8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74ba8b101164eb6edeae1fcf1bfa3c80788ceabb8abe502236546545fee8aa44(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49869519f1a48a773f04d38053b8d92aa1bb4e233e66bfd8c316007c5ccb120c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2167a1c905727aefb98a47d303c6e588847c7d081283eab52bb0ccaa8f8caed0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99aeb3521a37a6cc29fa3771fcc6b0df2fe01235b46487f2c9eb079a43cbc0b3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e4cc6a9b6e874ffc9fed89be20427a69cb206cd4f0e555e61466f383e8bcc26(
    value: typing.Optional[LinuxFunctionAppSlotAuthSettingsV2GoogleV2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60d389bde4631920900d76f4f57730c81b6a7ce2c0250d6ce5e0da69d31610ba(
    *,
    allowed_external_redirect_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
    cookie_expiration_convention: typing.Optional[builtins.str] = None,
    cookie_expiration_time: typing.Optional[builtins.str] = None,
    logout_endpoint: typing.Optional[builtins.str] = None,
    nonce_expiration_time: typing.Optional[builtins.str] = None,
    preserve_url_fragments_for_logins: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    token_refresh_extension_time: typing.Optional[jsii.Number] = None,
    token_store_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    token_store_path: typing.Optional[builtins.str] = None,
    token_store_sas_setting_name: typing.Optional[builtins.str] = None,
    validate_nonce: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad21f2010f4a11a33000cf23dc42d821803d1180c950ac9af08bd3212bac18d5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d6756ea9b7a87e2f9973c3a841ff801625593fe59fd04099ca3a84132ccf9d5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5f893492a7df8eefa80d1d807ecaed29218315e0819bbd82356a3bc7945c6da(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a48d6fa832720c1989b8fed5a663b3871b9984953e9c792115df728f742b80e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf0daa0de11322437801606fdecfe54215e879151bcfb84750f410338bbee0d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b75cd87503b9fa2a71969150842316712c1eb95b1c91d0708db691e6c898969(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__829d9d70e7754e3abdfde8eddea5f28e900e0cecb5364cfa8179dfceafc49d53(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39aee961db3ce4c09de4f9bfdffed2b89625e383196c6a4f6b3b79b3ba439810(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2afc390137e1c48f7acf116cc9e33e4f1e0fbf9bbd8ddb38fe9c077285ab4d86(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4490761f5104809369564ea8320da1e9dd2fbafcdb87942bd9bc48c4f6224fc4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbc383adc0e8f1d4aff6756f7414155414a269a8ffd12c9ee1043a2a58575334(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fee42e8c32019f29d395b5e6eb0c22c903edf5629a231e67bd54db50eb47b6d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ecb567c99373aea6409e37e1c21284e03ac962da238514bd67328547a3b05ab(
    value: typing.Optional[LinuxFunctionAppSlotAuthSettingsV2Login],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f72a30f60e14ce3f66310a1470bf0688ae1f3eff0ece48426f47c0c5516257ba(
    *,
    client_id: builtins.str,
    client_secret_setting_name: builtins.str,
    allowed_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
    login_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0674ab71f34eb018f502dc64ea907c49beaf2f22906fc19309209facd9d3bb0f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6949af6f6bc3a418476d1614dc5e3a1bc061ce82d4f4e3e2ba441f8640898c06(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e29933cbfbc1cc0558232cd1d1541e20b9d08e58fe0cb2bb9231b0a2b415bb0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5728a9af0ec1d25273842732f08ab8a565aa3a03f67d2799fa2be281df2e8552(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a593ea63c92aaf1032ee3528281168d36788a987189325e589689fc99fd13a8c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81260382ca394b9405418f27c6f3ccaefa9eca0e49676a5157c659d9f0db6070(
    value: typing.Optional[LinuxFunctionAppSlotAuthSettingsV2MicrosoftV2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28faafe9b57d4e23ce04e42732569f1973178e4c01c752a387b214275a692e30(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0fe3b69f5bb068821abe77785ac6c074145a616b5cd5960b394b86fba1d20f8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LinuxFunctionAppSlotAuthSettingsV2CustomOidcV2, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76c0e1fdf62ee39a75ef969e06b644792aab058289e5f513a1040cfa072b18dd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a68c025efa64ae1b79b611e8b5985116f6998011e0e55292af243be14475dc2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f48e4b801c6a1274092d23b96607b7d52738d0beaf5c252cb519c50969b05232(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ec885632db3456eb87070014dab97712699d43ffc46dc9ab8872ff2173324dc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91c6841172963c6787db0f6552229889f868e7ced6000e632d5465088e220e6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af83dad42a15c7cf8ed458846421451a2a0b021c506a5f9b04f55ee664f1bcb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d21a03f1b778d20b46f6c5e8c1bf72967e4b638e89298ba1259ba62138810df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c7a574b1c4717b1837679011f9ac5e68dc620f57ad597566cf69026f4cc9973(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bf8720b00ba99f1113c9bade307679afb23646b089c20fb33110782ff8c90b2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6adec2135f2b906f858de42996b962b6be8993dae0b106dda4cdc76f01ca3cc6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d61557b573bb2a8e18edea93e7af69403691e3ea2a9443af282a446b309bb92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d67a8bbaed80c3c47f94577c5d8bb48a2f2585898a4a1a5d6e8b2701f2c5ecf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cd42745f0fbabf321fefbc6f753c05d3138fbacb1d1eadfe3b60bb9b0dc411b(
    value: typing.Optional[LinuxFunctionAppSlotAuthSettingsV2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8795928db759ec5709c95b470ee839c718834a2f802b8c298aed259341d28351(
    *,
    consumer_key: builtins.str,
    consumer_secret_setting_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebdfe919a25fc14052dabe8aae97fdd66e7923b06cc8d00a956c29d0ca766609(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc6f3d1985f808a0a8da3de196732a02ba32e857746c6f9c0425ac6f91d776e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55a7b20552ec01b5facdea8cf560aa5777f180267e5ecbef5937e2df5ee7160f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a686c3782f4a64b8212403c9f0b6ef51bdbc738429be726432e7054ea13a06f6(
    value: typing.Optional[LinuxFunctionAppSlotAuthSettingsV2TwitterV2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c6f028be2e265796d2f785796ccd7138e23edcb666c1468eb47124542bd60d0(
    *,
    name: builtins.str,
    schedule: typing.Union[LinuxFunctionAppSlotBackupSchedule, typing.Dict[builtins.str, typing.Any]],
    storage_account_url: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f2cdc2d602148816f08e1455c424ade888fd4f243b99ad5b6599e3eb92ff733(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8714cbc08f665ae6a8975e6c6f2865af852cd61120813c6b47483809b4f5ce4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dd712ad40b0cb9776f76fc4352a7318d713c04559460f6fc9deed8ab9997d4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f615309a3fa5901dc155b1da48892378e8eaff3c2e03283b1e690b7d070a2ca8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3da41cb003e110e637cfdbeae082012df15250a76353dd91bfcb06a5de3be19(
    value: typing.Optional[LinuxFunctionAppSlotBackup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4813dbac238f6fb0ab27a49ec224ea22fcd28f7055e9ab4495fc41d8e926e85c(
    *,
    frequency_interval: jsii.Number,
    frequency_unit: builtins.str,
    keep_at_least_one_backup: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    retention_period_days: typing.Optional[jsii.Number] = None,
    start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fefe40fabbe710cf7e10401e14e34bca485f34d252bd41d6ef3299bbc96a6c4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63feaa1ed73183b185703b86f4aa02a1bd5c10d89f63fabd5610db6ec30a7dcf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8b6dab1d656d7e469ade3c5a455405e6edcb66f24ee55dabecbbd0c866c87b8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bece44d0692a6056c6976b4361cb9508dd2ae0b2a6b209c160809a2916e73cb8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bf889e65dfa171b1c5cad9fec4b60d7e79f594654042a40b3b9e57d20db918b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a54f962c78ac5e679db8fad6a5376d7725d1f604eceec84bf1f9a412bd28c835(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0deac4dde135bb5c4f1d74b3258aa7bf7f638beb67e97fe6b12f697888b44109(
    value: typing.Optional[LinuxFunctionAppSlotBackupSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bda8efa9165dba8ca6259fec8dd31eda0f5026e0c02422ff85d9d2afbf35712a(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    function_app_id: builtins.str,
    name: builtins.str,
    site_config: typing.Union[LinuxFunctionAppSlotSiteConfig, typing.Dict[builtins.str, typing.Any]],
    app_settings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    auth_settings: typing.Optional[typing.Union[LinuxFunctionAppSlotAuthSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    auth_settings_v2: typing.Optional[typing.Union[LinuxFunctionAppSlotAuthSettingsV2, typing.Dict[builtins.str, typing.Any]]] = None,
    backup: typing.Optional[typing.Union[LinuxFunctionAppSlotBackup, typing.Dict[builtins.str, typing.Any]]] = None,
    builtin_logging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_certificate_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_certificate_exclusion_paths: typing.Optional[builtins.str] = None,
    client_certificate_mode: typing.Optional[builtins.str] = None,
    connection_string: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LinuxFunctionAppSlotConnectionString, typing.Dict[builtins.str, typing.Any]]]]] = None,
    content_share_force_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    daily_memory_time_quota: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ftp_publish_basic_authentication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    functions_extension_version: typing.Optional[builtins.str] = None,
    https_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[LinuxFunctionAppSlotIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    key_vault_reference_identity_id: typing.Optional[builtins.str] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    service_plan_id: typing.Optional[builtins.str] = None,
    storage_account: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LinuxFunctionAppSlotStorageAccount, typing.Dict[builtins.str, typing.Any]]]]] = None,
    storage_account_access_key: typing.Optional[builtins.str] = None,
    storage_account_name: typing.Optional[builtins.str] = None,
    storage_key_vault_secret_id: typing.Optional[builtins.str] = None,
    storage_uses_managed_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[LinuxFunctionAppSlotTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_network_backup_restore_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    virtual_network_subnet_id: typing.Optional[builtins.str] = None,
    vnet_image_pull_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    webdeploy_publish_basic_authentication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6f1da3fc01434d0be952b1f3905cc271e3e25491041f2bb31b33c1b86a747e9(
    *,
    name: builtins.str,
    type: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__975cf779431599e2e4d99ef98c058b6fa82d43441c5c570fca23d6c7b182a8c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bdfa15a851d9a8d01037e60326c5595b67579026ca71d301da9c4403fbd43c6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09f4742f521cebaad6848411e20b4c60e4412613ccb53f54b17593e6ecee3a49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a19602174cc96aa33e1093e59176718c4a60bf1fc550e34df9faa985715f81ca(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cce6ef9f91e931442ac64e28ea874fff1ba209cc04831c5934958168979d3c05(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e190d1cb8cd5d72eabe4d95afd1f6257fea97487b7a7c1ed87418767623e4436(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotConnectionString]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bef64d05d7ac661019a872b5e53ab56f6f1e377f1c9815743598acdd38f0e8c6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d990b1657d1d29489152f1429288b85e1406fc0618dae3235710058f384ef4f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d734b788a6eada651762757dd43747c5ec0fd051abf082a885ca0e352fa11b22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93869a59debbb6c835cdae16ce7f1d9bf209b7b65e8c91526b4c949fb5cd847f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bd5870f4a927944a6c7726232f835b028db0ff10647017a44e1a84bbfbb3c50(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotConnectionString]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__850409c848d4c04ee123f5385c756c3e97aeb95c0ee5cd8bafe0d2af9ca2fd8f(
    *,
    type: builtins.str,
    identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aba9ff3b33d9bb1ae7b1aba9a645056ac54dca8bd65051a3a86331494baab1e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9d62145ca2249ce04acdcd43aead3e5edc9f45cb04441dbbc2413978cfa283b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__326dd24997085ef2ee1ed791c816d5328feef53b3ef15748ee9e2662f81c9cd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43bad7647155ed0e396d21f84100218c9a73c48647303393762576375057c2da(
    value: typing.Optional[LinuxFunctionAppSlotIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__545635225a559a7a251e23829957a53cab882bdbbf83092dad2401a4eb3f094a(
    *,
    always_on: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    api_definition_url: typing.Optional[builtins.str] = None,
    api_management_api_id: typing.Optional[builtins.str] = None,
    app_command_line: typing.Optional[builtins.str] = None,
    application_insights_connection_string: typing.Optional[builtins.str] = None,
    application_insights_key: typing.Optional[builtins.str] = None,
    application_stack: typing.Optional[typing.Union[LinuxFunctionAppSlotSiteConfigApplicationStack, typing.Dict[builtins.str, typing.Any]]] = None,
    app_scale_limit: typing.Optional[jsii.Number] = None,
    app_service_logs: typing.Optional[typing.Union[LinuxFunctionAppSlotSiteConfigAppServiceLogs, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_swap_slot_name: typing.Optional[builtins.str] = None,
    container_registry_managed_identity_client_id: typing.Optional[builtins.str] = None,
    container_registry_use_managed_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cors: typing.Optional[typing.Union[LinuxFunctionAppSlotSiteConfigCors, typing.Dict[builtins.str, typing.Any]]] = None,
    default_documents: typing.Optional[typing.Sequence[builtins.str]] = None,
    elastic_instance_minimum: typing.Optional[jsii.Number] = None,
    ftps_state: typing.Optional[builtins.str] = None,
    health_check_eviction_time_in_min: typing.Optional[jsii.Number] = None,
    health_check_path: typing.Optional[builtins.str] = None,
    http2_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ip_restriction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LinuxFunctionAppSlotSiteConfigIpRestriction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ip_restriction_default_action: typing.Optional[builtins.str] = None,
    load_balancing_mode: typing.Optional[builtins.str] = None,
    managed_pipeline_mode: typing.Optional[builtins.str] = None,
    minimum_tls_version: typing.Optional[builtins.str] = None,
    pre_warmed_instance_count: typing.Optional[jsii.Number] = None,
    remote_debugging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    remote_debugging_version: typing.Optional[builtins.str] = None,
    runtime_scale_monitoring_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    scm_ip_restriction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LinuxFunctionAppSlotSiteConfigScmIpRestriction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    scm_ip_restriction_default_action: typing.Optional[builtins.str] = None,
    scm_minimum_tls_version: typing.Optional[builtins.str] = None,
    scm_use_main_ip_restriction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use32_bit_worker: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vnet_route_all_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    websockets_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    worker_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0c526c5409b5290d68e2259ca0a8cf7ab29d291bfa09cbb1ff388f1d805f457(
    *,
    disk_quota_mb: typing.Optional[jsii.Number] = None,
    retention_period_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cbb1c3ca796b0239c9d08f888d679d9f1b1ab92a38d79246aedba7e2d166935(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82b4282fc5e54fcdff494f0ac99439634d151cd9638b5d4ed5956873ddbb4d96(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cdbe6a0515e6e3b8762478352a5c4e274e88a697a9bbf4bb7a44794f187c313(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee188e20fbcb3f570dcf8d80533d66015a798722a1254f0f58b9e107a15cb49c(
    value: typing.Optional[LinuxFunctionAppSlotSiteConfigAppServiceLogs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abecaab36337c7aef22da00918872ffc6cc9ff7b632dc7995c6a2b602bcc6d6d(
    *,
    docker: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LinuxFunctionAppSlotSiteConfigApplicationStackDocker, typing.Dict[builtins.str, typing.Any]]]]] = None,
    dotnet_version: typing.Optional[builtins.str] = None,
    java_version: typing.Optional[builtins.str] = None,
    node_version: typing.Optional[builtins.str] = None,
    powershell_core_version: typing.Optional[builtins.str] = None,
    python_version: typing.Optional[builtins.str] = None,
    use_custom_runtime: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    use_dotnet_isolated_runtime: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6d0082ef34d3c886c674b3af28480907f7cf0ec18580c650438757f99b0aa90(
    *,
    image_name: builtins.str,
    image_tag: builtins.str,
    registry_url: builtins.str,
    registry_password: typing.Optional[builtins.str] = None,
    registry_username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d307abece9eb60e38a811f973f5d97d8ddc1f3393bda0436137ab94af603904f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9aed5c757afe02f30b12998bcc9e46463a95c65506a9eaed22d77d834e96ce61(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb10987a5d015b557657109bbd64560ed6069ede7e895e68119afe57972a8235(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8efed2a202cb55c45456bf0cdfa49cdb9e444e3e62351a3217900cf8790acc7c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62b18f5d96eb85597284cdb24bcecbbb8e80d4fe4285ec13e77b927dd92a185f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f19d5c7775dc4c4b37fd7e1ef5b3be28bab44e10a4825293fcd600c67da2fc3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotSiteConfigApplicationStackDocker]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de0b7812b0adff55cee768a1a7b3863fa983cd21703e163b96b77e499c8ecc62(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__377fac66f8c6f2c19bb78e6655770e6d741c7c101a633a5868e586951de1704e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5790fae2c9687f24bce2775a794cbd1ede67d4d5f88ac26a06c24a096066084f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15e7691104f43208550df0fc3e2f587f2051f42f786a7c4f05a73ecb6030c241(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dee6a61cd8735e4ea510331c35207bd61f2755efe95748eb48fac811782fe58f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d823ec0cd848841daef71658afd5e1c8b79630c7905b66d752bdddee19fe4e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aadee031d2df7d0d4c4e3a6769532376ebc1a295d2483625ac585ce38d11dda9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotSiteConfigApplicationStackDocker]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__416f50005754c51c531583a44cb9fcdeae99bf68b17c2f9a04783a96ed2ea49f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__788ab54854123beb96f3aa80ae66da2615b16d140b7036bd20ee4cdafd14713f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LinuxFunctionAppSlotSiteConfigApplicationStackDocker, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a5f0c609180b6c1087a8a702f17424e5f489bafd6d441f596906d8c18bebf18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__865e2d9c75504a46f22bbd9d3ccff3edae8e9a112917ddcf92d3de8ba6993e24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb109ab2a93e79c877621da168fa5e4f1203efe1a7d85a52a9ed8eda11f48a7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__990cf712ff152bc23ad726af1e41739f5c8a929624d95ed9afd15edefa18e6f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__440e86b55b734ce7640a6b42768e22a2200a8a5c6a5a8556381c2fa3f26d7209(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d52ab39aa896b1d74bfdcad314f4182a0317f851cf58ec213b021f80a206aa6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f7ad4a9fb2a3defb97c7d4d4b8422415cece8bfb6e9fb7bce2be1a77213b37d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__237b1bfd39264362437b4c28b1aa7c1cd44aad5719e2461a278244836d197273(
    value: typing.Optional[LinuxFunctionAppSlotSiteConfigApplicationStack],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6cd6c98b0b4fc0d8c9d7dfc06b3154ae3db58f065e80a40078e6c388c2beeb4(
    *,
    allowed_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
    support_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffd34e471ada35ba765efe6950e1af23cf0579920043118f6a684585f72daee4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b85eb2d79cba67f4c3c6a8c3dfd38b6cf88fda919eb5b38b4c24cedce9f3fe0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e0f60bfaaf3d7b0ff267cf4ebe06682ba17461c625a1595c9b4f720ab9fe4f1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b205752b9a6291d525017f7689fe8a8f529eb89286d45d0c8a488bd17c5f22a(
    value: typing.Optional[LinuxFunctionAppSlotSiteConfigCors],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2181d25c5700b45f8316e979148e3e18271066d7eba8ac19bf4940eee4967f73(
    *,
    action: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LinuxFunctionAppSlotSiteConfigIpRestrictionHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ip_address: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    service_tag: typing.Optional[builtins.str] = None,
    virtual_network_subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50d5256d44a930fb2a8059c70d838c9de005f4581e36a76400095e65f7b92455(
    *,
    x_azure_fdid: typing.Optional[typing.Sequence[builtins.str]] = None,
    x_fd_health_probe: typing.Optional[typing.Sequence[builtins.str]] = None,
    x_forwarded_for: typing.Optional[typing.Sequence[builtins.str]] = None,
    x_forwarded_host: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e170f73a1a027dc804e96a211b0bb73d02a5aeca206d470d4fb922101e6d357(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91576af329c18629b095f2adb25232eab2b8ee1e889d8c15722e72af8fb33ac8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfe6bc8d8b8ca61c0f64aff33e4ebcd7981b17c743bdf25a99671e6e8049ac54(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__964c99717c4ba93e2be5485ce8a124bd790bfc7508f398cb51fc21a0a24eadb2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0757a7d85970c558d055a85e492f59672d984437ae410f986f661422381ed19(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__564d69487555c97f71d0d6a4326d4cee20423e9cb8f5dadee6b3d09903f2a572(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotSiteConfigIpRestrictionHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebb688944243042dbe00c9954d98b17945880f3e3cd2ba3917971c07925abafd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b175cab431bb0a66d369d1b5147245d03c021d1c4afec20c2d44b5b0ba6e4ca4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8260ad1fb7740237aa412f46bddcd9788f77c09ff0ab4edad3d3c09b407acf4c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b6bf0179fb3a58b1324f9ad03432d20f36bd8be64dd12fb77b10909b2fbc978(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__746ee6f9d32fb84782938db41768ba54e9c6d2b2c623e81a7d290895360fd80b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b77062612584b268a742741a28f1265fd70b59a24c8122aa328b010fcaae122(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotSiteConfigIpRestrictionHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73cba6347ed17055cbc7abed9e774ba53a022c5e4fd81ab2c490627d87c97786(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b488ef2fe1df97afccf9373c8a00797263248c992026260152cd2f33bf8174a6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9d345c3f2e8bc1ab447a3d6b692fd04f8981fefbea0e190c7cadaf163dfc024(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80d768b9c95be4bfceff88c408605f7dfc41a671a9ec38480c30513a494798bd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__476f93f2e52f4d9e05e0f518696d48b91111af863a7c277331402d63a5881deb(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0adab1c3bd6bcb899f2a0fc1d1ad9a816248842fed4c496d5160275e19f439d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotSiteConfigIpRestriction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b790a27a1051bd06a7328b1a2ca7c16144ad7cf430e70d73e024032e92fd24b8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48de0acd9a8a31921840a9cae00b754296b9bb8af9edb89ac57de486d1fd51bd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LinuxFunctionAppSlotSiteConfigIpRestrictionHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__691d38a74c0c927a712ac9ef43d57a9fa19a3654c6438accda9b3cd9d2fb0192(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c749f3a45a2d5e550886ccd96ade41e18fa9ca02b440b0313613de9f034e2bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe153b1c901bfde0c86db8ebc298684b2cd8adb47d2853cd16a03d6121f91a68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c9cd5fe034bc18bffc479a5d845685f3124f89ad3d2c8a032134cf24382d88f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51a22cc7068c628f423d8a30fab25dc1a7280c0d674925650b42e80c8f505675(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1386979a4d64d0c85dd24d7237553a47c83e1d9385ccd249d645e81d34e8f16f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed74ddc11f0b93464b94a2a4707d2ca2480d9e7a6174db7ed4fa964a45e44f7d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2a7ca7b656b32d335eff58a55da4cf44e5fb57412e76e1c3af91bac2aefb482(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotSiteConfigIpRestriction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c9c784634f92258245bbd5865f0358ef44f9fce0735bd13630cc36bf756dce8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6126f4ce91a78eda649d7881057283f1a3c357f8b09e18692de910a81ce57971(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LinuxFunctionAppSlotSiteConfigIpRestriction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e92d9180c1cbff3234d7497041a518bd81bd7922cb290beac32c9edfd1c8239e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LinuxFunctionAppSlotSiteConfigScmIpRestriction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5d3f7d71d944080d100644a2483cd4c74c28a0648d56ae90156c5c703e558bc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b58de00b8121d3fc793ea5cb973932e3b4c1d7f37140f9098e906cc829a83e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f14a98c07510de1c0d2f3b26413bef91fdfeebe093955fc60b67195819f1760(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfb8c9893ee225174b747417e8a15bc643c36ea9db66f37a27220ee53c95ea52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b70566296b1f4075247cb1428b144fa53f66efde640697d8483c6e9114e9b40f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e32ca8802f9de893dcc7f9e3fb97283667439613433aca1fc738919155222aae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6578c88e833928ffda197a9cf6423ad5f3490d1367de3f57b8a2f2c09594ae5c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74a599adced3d2d1ad564718449480bc4b051f56d5ea8d7a7348e34af8772efc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b8602c2eb0aa2acdf0c788407cb60e6690ccf64b583cafc17391b813e8f5192(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e55bfd227ef68ac403f50517d9fbb6fb1550cf8c5792109df06251733c495e1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b1fd312592fed2d98585f56767caba807ba46fc36ec73565b81ec355263de00(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8847a649f251f81329df7d12009d9d7e932396ed3cba538a5fe015e380e5325(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a89260944f71302e836748964f17bf85d991be177dbe03702f95843c1dca883(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3b00ecf053b684924c9debbfc3c77b9cb7ff5ea60be5c084e4d93b4266339e0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62f0f9582ed52c2c42136ca62dd0238070e068dd934cc71178c482ff1f6ed5e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__267ce8f413baacfa7788657aebfdf7d9306f0ca717ed547e9a36bf3fa292b09d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5f18d510a8215f580f8ea98e83008aabb15ed0717bdf0416da430151e11f766(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39450caf2bce0b203a3a406be564b6c14cd482aafb20c22df23ba8629c124235(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fc508a989b99d1d2bddcd36b3c5aa059cbd81ebadf2246f784cea6241960abb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9b2c4cb2e9acc5395c0a3e1afef0f33dbd786a32ca979463eaca0562f266253(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a4680dc65e5e40529cb97b77af53fed60cb0e005c9580c64987203361ee5315(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44411c374399a05d3b19901064927051d235ef48d00c102463c21496b1a0c123(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f70c2c5b7f6cab1df44ac15d49c757bed15ee5ef83b1cd9e92cc1f106f87201(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63534a787f782a35ab7fb2e46283600a1662e299467e7bdc53eb65e50ae2bb6d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89a03188383bc06eb697eaf4a4308a5a3149ca3c371e25676dd4c9b6a4f52397(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28a7e1072572fac92f0f7687ca524a3a8febdfde4f7dd2c9fd95b65a87917842(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f573a72b26d542684ee851d64e442d067f99c9692bf13a1ad5601a8b91300e86(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b27d048215f3e84092819b20ba1048ef8ec76fd632d64fa3071b23434dfca29(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a6354706637e88ca8af4d7fb90cd27080a28577be589349a9dd3c0a1e783cab(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2212bd8de7e82029321adf2b48160235520690a4653d78c63c4be89229ea8308(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__177e17b3fc5aa99ae0d1304f263ce23b34ee4c06255b3930092c671a2b69844e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4d02f6c531fee6bb538f2dab91ee815ffe2d953a6c54601cd2d276690a80621(
    value: typing.Optional[LinuxFunctionAppSlotSiteConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24a3a5f6181c88a36b713b81816ee4d56bfcc2c37c4131adf5264b3ba8f6b05b(
    *,
    action: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LinuxFunctionAppSlotSiteConfigScmIpRestrictionHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ip_address: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    service_tag: typing.Optional[builtins.str] = None,
    virtual_network_subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5217b9a98433bba6c41fcf3fc0bf2d63d8fe291322dc344655336aae01951e6(
    *,
    x_azure_fdid: typing.Optional[typing.Sequence[builtins.str]] = None,
    x_fd_health_probe: typing.Optional[typing.Sequence[builtins.str]] = None,
    x_forwarded_for: typing.Optional[typing.Sequence[builtins.str]] = None,
    x_forwarded_host: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86680d7cd71c9ae5400d573401629695d56bbc00adb88e0218716b5ce3ddeeaf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61ec907a40d8674b913a90581aeee914699e1ee97c1fd8bffe2b9c9f4c779cc2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51bb60f8a757491386d80fcc77dbaf9956881edb57a58de11453d9ecefbb24fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62176d54f8458b20c8b41d20da4111b64a0f05e461f06e0bff0d4d9695a7d11b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__678bbc0a431ce4c063f92a4deda69e88afdfbb438bc06d195455d56f54776440(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d79d388fa67e9a388e1493495d363512e691dfb24d58c6fa64428e8f7c3b839(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotSiteConfigScmIpRestrictionHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73c96adda532eb5eadab8c99f39ebc6c7e2649d0285972fa72bb27161bcfb10a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6791c3485ca2d62d16aa60ca2c93b7c9acfbfe7a984dda3b94cba05f379b8e13(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26b93132d15d29adc03cb139768b34fb432701010b115be9047c5dfb43d39be7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04a295a236226b4b45abb5a2e3654019caca7d5294f3ccff4b08c6331b8db3e8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4010a5ef5c99012ace28bd55e599bfdf459a071d90cb2d71d7971275a6292488(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c8779dd731eb8f329afe4bb62d99b998d259414a570682ff97d578bbe8298be(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotSiteConfigScmIpRestrictionHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee19a6c463b0a0c76d0ad2039cb0434b6ab4d823719a323d918e72d91ec92bc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47db1868e90d328889f66c6168b5b90d3c5fca042b7136b41d163c0874b72b79(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97be545db9e5831fa6bfc00fa1b50718de2c8d4057d9f1a3973937626477b0a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0499db163bb5abe428af1f753e9e4ff3aafa25405cf37d9a84985adf76c5f8a5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f4a544f29ae182b84a2ef3331eba48220378d05820f456391c56e35b8ca2ba6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bb2bca8a946e18640620f7120dd2092f7dab7d2eac632199bd2e362265c3084(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotSiteConfigScmIpRestriction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8f8f278448c47d99647b07af350627d8b32c885642b318e4889aeb76b10ebeb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78c7b8317f515a3bf56bc4cbe5fb8068f6d31c17b1149bba16eaa4c3be6e9f4e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LinuxFunctionAppSlotSiteConfigScmIpRestrictionHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e29b9e837a5e624a0071075b4592d1c2ef35133467cb43d762ca2f8034b0e47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d035ee76d5022da13396b0f8eb7f1f1a2c44cf1e3470d1057a0fe6b38c38ec4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fe44c25b2c4b90814a7d97d182b4b26c3c6d3a43bc8d6ec4c3415efd206b85a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcdccac011ae4e2ba2faff10c37187c0158c6a2e40f97a1aaabb6f2dd5ad1310(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81f52344b8cf11a5bb75c8d5568a0cce86001c149854009296c184531abfcc3e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8c8f7c16e83f01dc4ce06c9283199420d93b4b3b0e0718d04b5fc49c85c7e6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5740f4983c783c7471419e76dafb3f2e41c78ef31ad6a94282bd3f5ff02f1c3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48c24aa4fbe4a5f0b21b6c4cae016fd205417675ff1b573630f2d3cc3504ff68(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotSiteConfigScmIpRestriction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea665609d66872069bd414f11891e63b65ed8fa4b5265ae54ac37e031bc1c6ef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8358b4f76a0398bf9bdb17c811610ba7998274adb66a6dc5e137acc092459716(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6677e171f6c522738ae3858b86ab883d58e9a86676e3f0fa7a4e1f8785f42fa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaf65d5e1d196707c447b0ff7783a819aefb329d87af551a0ea811d3c7cb0dd2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__391ea2bee5dfacd2fe4c0bca275e98902c4dbb3c0a83d420a3dd96df2c98bb9f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__753c0e849c7f11b3ff0f6cefe744de05295818f5df1bf1ff4850b187fb34edef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4296b5e5e9c388e1151d7f99bee07ec593c3d282cb61be8096b0673f0f4eb86(
    value: typing.Optional[LinuxFunctionAppSlotSiteCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66e2738789ab96656c42fe63a287a95cf4d66b6ea3b1961abcd5361699384a56(
    *,
    access_key: builtins.str,
    account_name: builtins.str,
    name: builtins.str,
    share_name: builtins.str,
    type: builtins.str,
    mount_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b910c59a4bea6c8f8fc47a54dccdcfaba9d5c446030d6ccc343977297da606ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94661b3d842ac51772ed6bfc35cd93576f68357c66c464a893d5351d02a7a14a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32554e8513276ee64faeaf7e8210ecaa3a0c6f05d2268a2b751cef14dc0b5fc9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__791896a42bbdc1a79f0968d3883b5de4322aaa6ee8600133ca704b138aaba8e3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__914e9aef43b76a5de261ab93a4f08c84240e39775343485588438edbbf244faf(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1273f642ced8cc803fe7576741b9c00f13cb9a2ad7c268dc72d26701e64a6a2e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LinuxFunctionAppSlotStorageAccount]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__868a025df05f98f7e41bea307804ba39638c458fe75ea09af0f1af6a678d6e35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25d9f3d98b0d068f39ae25ebd0a32064a5b763814327fe25ed2173b61498953e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6677a7093a9786fd0c617b713b003308767d2faf80d8bcd09f523aa444662306(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5708f7c457648718f034c67082e45b3dce585e2fde79b52a4b115b8d7ccf236(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a77d06deeaf14907a64aa69a26de51f880768eb9ce4639552d73f5fbbe4bb716(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bab8d20e5727e7a1e11df821cb8e514be09d41f77f63e9e98dbe90ee22f10a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__839f7b0f06abd14d1defcb82ca6a8172611e8a4fd46c9b4cecc8ec785313f1f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da3e6118f1df9de6cf3529ac07326dfb921e0e8c0c9e71e0bad0f34a4f20a771(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotStorageAccount]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30402b4c8cbe125cea62ac89e50a912641916e4a16a7ebb4d7af78dfd2cdc42f(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9d166d4550efdb17462790ba02c21890e849787866edcd0ddf287905dd2abbd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5364dff727f7d8e7340861257a4b082c9394858532480c54f6caa7f68c9a195(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2ceb0422f9a2d93f2d9ea08f1ce4f072257802b7bae8146722fd808041f5817(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9e700a0872d7307b59a694348447f37d0e3ca73bac42238ac0ffcc8f5d327f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a00811a0df305d5e1ed87a3fa378f01f45dac504a3e7282acde3813b5fe3d6ed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe01daf3c8dc33e555afbf2d2fde2f81fbc4f493d6187aefb0ea68c16571e7bf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LinuxFunctionAppSlotTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
