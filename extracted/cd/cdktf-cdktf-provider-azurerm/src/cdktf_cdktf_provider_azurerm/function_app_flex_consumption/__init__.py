r'''
# `azurerm_function_app_flex_consumption`

Refer to the Terraform Registry for docs: [`azurerm_function_app_flex_consumption`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption).
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


class FunctionAppFlexConsumption(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumption",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption azurerm_function_app_flex_consumption}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        runtime_name: builtins.str,
        runtime_version: builtins.str,
        service_plan_id: builtins.str,
        site_config: typing.Union["FunctionAppFlexConsumptionSiteConfig", typing.Dict[builtins.str, typing.Any]],
        storage_authentication_type: builtins.str,
        storage_container_endpoint: builtins.str,
        storage_container_type: builtins.str,
        always_ready: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FunctionAppFlexConsumptionAlwaysReady", typing.Dict[builtins.str, typing.Any]]]]] = None,
        app_settings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        auth_settings: typing.Optional[typing.Union["FunctionAppFlexConsumptionAuthSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        auth_settings_v2: typing.Optional[typing.Union["FunctionAppFlexConsumptionAuthSettingsV2", typing.Dict[builtins.str, typing.Any]]] = None,
        client_certificate_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_certificate_exclusion_paths: typing.Optional[builtins.str] = None,
        client_certificate_mode: typing.Optional[builtins.str] = None,
        connection_string: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FunctionAppFlexConsumptionConnectionString", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        https_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["FunctionAppFlexConsumptionIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        instance_memory_in_mb: typing.Optional[jsii.Number] = None,
        maximum_instance_count: typing.Optional[jsii.Number] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sticky_settings: typing.Optional[typing.Union["FunctionAppFlexConsumptionStickySettings", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_access_key: typing.Optional[builtins.str] = None,
        storage_user_assigned_identity_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["FunctionAppFlexConsumptionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_network_subnet_id: typing.Optional[builtins.str] = None,
        webdeploy_publish_basic_authentication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        zip_deploy_file: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption azurerm_function_app_flex_consumption} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#location FunctionAppFlexConsumption#location}.
        :param name: Specifies the name of the Function App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#name FunctionAppFlexConsumption#name}
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#resource_group_name FunctionAppFlexConsumption#resource_group_name}.
        :param runtime_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#runtime_name FunctionAppFlexConsumption#runtime_name}.
        :param runtime_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#runtime_version FunctionAppFlexConsumption#runtime_version}.
        :param service_plan_id: The ID of the App Service Plan within which to create this Function App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#service_plan_id FunctionAppFlexConsumption#service_plan_id}
        :param site_config: site_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#site_config FunctionAppFlexConsumption#site_config}
        :param storage_authentication_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#storage_authentication_type FunctionAppFlexConsumption#storage_authentication_type}.
        :param storage_container_endpoint: The endpoint of the storage container where the function app's code is hosted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#storage_container_endpoint FunctionAppFlexConsumption#storage_container_endpoint}
        :param storage_container_type: The type of the storage container where the function app's code is hosted. Only ``blobContainer`` is supported currently. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#storage_container_type FunctionAppFlexConsumption#storage_container_type}
        :param always_ready: always_ready block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#always_ready FunctionAppFlexConsumption#always_ready}
        :param app_settings: A map of key-value pairs for `App Settings <https://docs.microsoft.com/en-us/azure/azure-functions/functions-app-settings>`_ and custom values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#app_settings FunctionAppFlexConsumption#app_settings}
        :param auth_settings: auth_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#auth_settings FunctionAppFlexConsumption#auth_settings}
        :param auth_settings_v2: auth_settings_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#auth_settings_v2 FunctionAppFlexConsumption#auth_settings_v2}
        :param client_certificate_enabled: Should the function app use Client Certificates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_certificate_enabled FunctionAppFlexConsumption#client_certificate_enabled}
        :param client_certificate_exclusion_paths: Paths to exclude when using client certificates, separated by ; Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_certificate_exclusion_paths FunctionAppFlexConsumption#client_certificate_exclusion_paths}
        :param client_certificate_mode: The mode of the Function App's client certificates requirement for incoming requests. Possible values are ``Required``, ``Optional``, and ``OptionalInteractiveUser`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_certificate_mode FunctionAppFlexConsumption#client_certificate_mode}
        :param connection_string: connection_string block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#connection_string FunctionAppFlexConsumption#connection_string}
        :param enabled: Is the Function App enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#enabled FunctionAppFlexConsumption#enabled}
        :param https_only: Can the Function App only be accessed via HTTPS? Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#https_only FunctionAppFlexConsumption#https_only}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#id FunctionAppFlexConsumption#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#identity FunctionAppFlexConsumption#identity}
        :param instance_memory_in_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#instance_memory_in_mb FunctionAppFlexConsumption#instance_memory_in_mb}.
        :param maximum_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#maximum_instance_count FunctionAppFlexConsumption#maximum_instance_count}.
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#public_network_access_enabled FunctionAppFlexConsumption#public_network_access_enabled}.
        :param sticky_settings: sticky_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#sticky_settings FunctionAppFlexConsumption#sticky_settings}
        :param storage_access_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#storage_access_key FunctionAppFlexConsumption#storage_access_key}.
        :param storage_user_assigned_identity_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#storage_user_assigned_identity_id FunctionAppFlexConsumption#storage_user_assigned_identity_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#tags FunctionAppFlexConsumption#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#timeouts FunctionAppFlexConsumption#timeouts}
        :param virtual_network_subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#virtual_network_subnet_id FunctionAppFlexConsumption#virtual_network_subnet_id}.
        :param webdeploy_publish_basic_authentication_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#webdeploy_publish_basic_authentication_enabled FunctionAppFlexConsumption#webdeploy_publish_basic_authentication_enabled}.
        :param zip_deploy_file: The local path and filename of the Zip packaged application to deploy to this Function App. **Note:** Using this value requires either ``WEBSITE_RUN_FROM_PACKAGE=1`` or ``SCM_DO_BUILD_DURING_DEPLOYMENT=true`` to be set on the App in ``app_settings``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#zip_deploy_file FunctionAppFlexConsumption#zip_deploy_file}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__126b9577b10a7316d290734ff529d809fb5c8dc24deb3c5120963aef8c80f571)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = FunctionAppFlexConsumptionConfig(
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            runtime_name=runtime_name,
            runtime_version=runtime_version,
            service_plan_id=service_plan_id,
            site_config=site_config,
            storage_authentication_type=storage_authentication_type,
            storage_container_endpoint=storage_container_endpoint,
            storage_container_type=storage_container_type,
            always_ready=always_ready,
            app_settings=app_settings,
            auth_settings=auth_settings,
            auth_settings_v2=auth_settings_v2,
            client_certificate_enabled=client_certificate_enabled,
            client_certificate_exclusion_paths=client_certificate_exclusion_paths,
            client_certificate_mode=client_certificate_mode,
            connection_string=connection_string,
            enabled=enabled,
            https_only=https_only,
            id=id,
            identity=identity,
            instance_memory_in_mb=instance_memory_in_mb,
            maximum_instance_count=maximum_instance_count,
            public_network_access_enabled=public_network_access_enabled,
            sticky_settings=sticky_settings,
            storage_access_key=storage_access_key,
            storage_user_assigned_identity_id=storage_user_assigned_identity_id,
            tags=tags,
            timeouts=timeouts,
            virtual_network_subnet_id=virtual_network_subnet_id,
            webdeploy_publish_basic_authentication_enabled=webdeploy_publish_basic_authentication_enabled,
            zip_deploy_file=zip_deploy_file,
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
        '''Generates CDKTF code for importing a FunctionAppFlexConsumption resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the FunctionAppFlexConsumption to import.
        :param import_from_id: The id of the existing FunctionAppFlexConsumption that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the FunctionAppFlexConsumption to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b7fbacc1be6422c2bc003c26840fbb1c6ea4fd129ee84112f1f70e935898926)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAlwaysReady")
    def put_always_ready(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FunctionAppFlexConsumptionAlwaysReady", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40ce25227edf520677e2d55c45479ce5c68d11de711c6542880cdef81751679f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAlwaysReady", [value]))

    @jsii.member(jsii_name="putAuthSettings")
    def put_auth_settings(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        active_directory: typing.Optional[typing.Union["FunctionAppFlexConsumptionAuthSettingsActiveDirectory", typing.Dict[builtins.str, typing.Any]]] = None,
        additional_login_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        allowed_external_redirect_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_provider: typing.Optional[builtins.str] = None,
        facebook: typing.Optional[typing.Union["FunctionAppFlexConsumptionAuthSettingsFacebook", typing.Dict[builtins.str, typing.Any]]] = None,
        github: typing.Optional[typing.Union["FunctionAppFlexConsumptionAuthSettingsGithub", typing.Dict[builtins.str, typing.Any]]] = None,
        google: typing.Optional[typing.Union["FunctionAppFlexConsumptionAuthSettingsGoogle", typing.Dict[builtins.str, typing.Any]]] = None,
        issuer: typing.Optional[builtins.str] = None,
        microsoft: typing.Optional[typing.Union["FunctionAppFlexConsumptionAuthSettingsMicrosoft", typing.Dict[builtins.str, typing.Any]]] = None,
        runtime_version: typing.Optional[builtins.str] = None,
        token_refresh_extension_hours: typing.Optional[jsii.Number] = None,
        token_store_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        twitter: typing.Optional[typing.Union["FunctionAppFlexConsumptionAuthSettingsTwitter", typing.Dict[builtins.str, typing.Any]]] = None,
        unauthenticated_client_action: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Should the Authentication / Authorization feature be enabled? Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#enabled FunctionAppFlexConsumption#enabled}
        :param active_directory: active_directory block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#active_directory FunctionAppFlexConsumption#active_directory}
        :param additional_login_parameters: Specifies a map of Login Parameters to send to the OpenID Connect authorization endpoint when a user logs in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#additional_login_parameters FunctionAppFlexConsumption#additional_login_parameters}
        :param allowed_external_redirect_urls: Specifies a list of External URLs that can be redirected to as part of logging in or logging out of the Windows Web App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#allowed_external_redirect_urls FunctionAppFlexConsumption#allowed_external_redirect_urls}
        :param default_provider: The default authentication provider to use when multiple providers are configured. Possible values include: ``AzureActiveDirectory``, ``Facebook``, ``Google``, ``MicrosoftAccount``, ``Twitter``, ``Github``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#default_provider FunctionAppFlexConsumption#default_provider}
        :param facebook: facebook block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#facebook FunctionAppFlexConsumption#facebook}
        :param github: github block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#github FunctionAppFlexConsumption#github}
        :param google: google block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#google FunctionAppFlexConsumption#google}
        :param issuer: The OpenID Connect Issuer URI that represents the entity which issues access tokens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#issuer FunctionAppFlexConsumption#issuer}
        :param microsoft: microsoft block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#microsoft FunctionAppFlexConsumption#microsoft}
        :param runtime_version: The RuntimeVersion of the Authentication / Authorization feature in use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#runtime_version FunctionAppFlexConsumption#runtime_version}
        :param token_refresh_extension_hours: The number of hours after session token expiration that a session token can be used to call the token refresh API. Defaults to ``72`` hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#token_refresh_extension_hours FunctionAppFlexConsumption#token_refresh_extension_hours}
        :param token_store_enabled: Should the Windows Web App durably store platform-specific security tokens that are obtained during login flows? Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#token_store_enabled FunctionAppFlexConsumption#token_store_enabled}
        :param twitter: twitter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#twitter FunctionAppFlexConsumption#twitter}
        :param unauthenticated_client_action: The action to take when an unauthenticated client attempts to access the app. Possible values include: ``RedirectToLoginPage``, ``AllowAnonymous``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#unauthenticated_client_action FunctionAppFlexConsumption#unauthenticated_client_action}
        '''
        value = FunctionAppFlexConsumptionAuthSettings(
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
        login: typing.Union["FunctionAppFlexConsumptionAuthSettingsV2Login", typing.Dict[builtins.str, typing.Any]],
        active_directory_v2: typing.Optional[typing.Union["FunctionAppFlexConsumptionAuthSettingsV2ActiveDirectoryV2", typing.Dict[builtins.str, typing.Any]]] = None,
        apple_v2: typing.Optional[typing.Union["FunctionAppFlexConsumptionAuthSettingsV2AppleV2", typing.Dict[builtins.str, typing.Any]]] = None,
        auth_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        azure_static_web_app_v2: typing.Optional[typing.Union["FunctionAppFlexConsumptionAuthSettingsV2AzureStaticWebAppV2", typing.Dict[builtins.str, typing.Any]]] = None,
        config_file_path: typing.Optional[builtins.str] = None,
        custom_oidc_v2: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FunctionAppFlexConsumptionAuthSettingsV2CustomOidcV2", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_provider: typing.Optional[builtins.str] = None,
        excluded_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        facebook_v2: typing.Optional[typing.Union["FunctionAppFlexConsumptionAuthSettingsV2FacebookV2", typing.Dict[builtins.str, typing.Any]]] = None,
        forward_proxy_convention: typing.Optional[builtins.str] = None,
        forward_proxy_custom_host_header_name: typing.Optional[builtins.str] = None,
        forward_proxy_custom_scheme_header_name: typing.Optional[builtins.str] = None,
        github_v2: typing.Optional[typing.Union["FunctionAppFlexConsumptionAuthSettingsV2GithubV2", typing.Dict[builtins.str, typing.Any]]] = None,
        google_v2: typing.Optional[typing.Union["FunctionAppFlexConsumptionAuthSettingsV2GoogleV2", typing.Dict[builtins.str, typing.Any]]] = None,
        http_route_api_prefix: typing.Optional[builtins.str] = None,
        microsoft_v2: typing.Optional[typing.Union["FunctionAppFlexConsumptionAuthSettingsV2MicrosoftV2", typing.Dict[builtins.str, typing.Any]]] = None,
        require_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_https: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        runtime_version: typing.Optional[builtins.str] = None,
        twitter_v2: typing.Optional[typing.Union["FunctionAppFlexConsumptionAuthSettingsV2TwitterV2", typing.Dict[builtins.str, typing.Any]]] = None,
        unauthenticated_action: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param login: login block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#login FunctionAppFlexConsumption#login}
        :param active_directory_v2: active_directory_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#active_directory_v2 FunctionAppFlexConsumption#active_directory_v2}
        :param apple_v2: apple_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#apple_v2 FunctionAppFlexConsumption#apple_v2}
        :param auth_enabled: Should the AuthV2 Settings be enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#auth_enabled FunctionAppFlexConsumption#auth_enabled}
        :param azure_static_web_app_v2: azure_static_web_app_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#azure_static_web_app_v2 FunctionAppFlexConsumption#azure_static_web_app_v2}
        :param config_file_path: The path to the App Auth settings. **Note:** Relative Paths are evaluated from the Site Root directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#config_file_path FunctionAppFlexConsumption#config_file_path}
        :param custom_oidc_v2: custom_oidc_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#custom_oidc_v2 FunctionAppFlexConsumption#custom_oidc_v2}
        :param default_provider: The Default Authentication Provider to use when the ``unauthenticated_action`` is set to ``RedirectToLoginPage``. Possible values include: ``apple``, ``azureactivedirectory``, ``facebook``, ``github``, ``google``, ``twitter`` and the ``name`` of your ``custom_oidc_v2`` provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#default_provider FunctionAppFlexConsumption#default_provider}
        :param excluded_paths: The paths which should be excluded from the ``unauthenticated_action`` when it is set to ``RedirectToLoginPage``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#excluded_paths FunctionAppFlexConsumption#excluded_paths}
        :param facebook_v2: facebook_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#facebook_v2 FunctionAppFlexConsumption#facebook_v2}
        :param forward_proxy_convention: The convention used to determine the url of the request made. Possible values include ``ForwardProxyConventionNoProxy``, ``ForwardProxyConventionStandard``, ``ForwardProxyConventionCustom``. Defaults to ``ForwardProxyConventionNoProxy`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#forward_proxy_convention FunctionAppFlexConsumption#forward_proxy_convention}
        :param forward_proxy_custom_host_header_name: The name of the header containing the host of the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#forward_proxy_custom_host_header_name FunctionAppFlexConsumption#forward_proxy_custom_host_header_name}
        :param forward_proxy_custom_scheme_header_name: The name of the header containing the scheme of the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#forward_proxy_custom_scheme_header_name FunctionAppFlexConsumption#forward_proxy_custom_scheme_header_name}
        :param github_v2: github_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#github_v2 FunctionAppFlexConsumption#github_v2}
        :param google_v2: google_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#google_v2 FunctionAppFlexConsumption#google_v2}
        :param http_route_api_prefix: The prefix that should precede all the authentication and authorisation paths. Defaults to ``/.auth``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#http_route_api_prefix FunctionAppFlexConsumption#http_route_api_prefix}
        :param microsoft_v2: microsoft_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#microsoft_v2 FunctionAppFlexConsumption#microsoft_v2}
        :param require_authentication: Should the authentication flow be used for all requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#require_authentication FunctionAppFlexConsumption#require_authentication}
        :param require_https: Should HTTPS be required on connections? Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#require_https FunctionAppFlexConsumption#require_https}
        :param runtime_version: The Runtime Version of the Authentication and Authorisation feature of this App. Defaults to ``~1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#runtime_version FunctionAppFlexConsumption#runtime_version}
        :param twitter_v2: twitter_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#twitter_v2 FunctionAppFlexConsumption#twitter_v2}
        :param unauthenticated_action: The action to take for requests made without authentication. Possible values include ``RedirectToLoginPage``, ``AllowAnonymous``, ``Return401``, and ``Return403``. Defaults to ``RedirectToLoginPage``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#unauthenticated_action FunctionAppFlexConsumption#unauthenticated_action}
        '''
        value = FunctionAppFlexConsumptionAuthSettingsV2(
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

    @jsii.member(jsii_name="putConnectionString")
    def put_connection_string(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FunctionAppFlexConsumptionConnectionString", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dde6579271f293d0e04989a80087daac9feab94328203426db6bdddcd8ae788f)
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
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#type FunctionAppFlexConsumption#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#identity_ids FunctionAppFlexConsumption#identity_ids}.
        '''
        value = FunctionAppFlexConsumptionIdentity(
            type=type, identity_ids=identity_ids
        )

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

    @jsii.member(jsii_name="putSiteConfig")
    def put_site_config(
        self,
        *,
        api_definition_url: typing.Optional[builtins.str] = None,
        api_management_api_id: typing.Optional[builtins.str] = None,
        app_command_line: typing.Optional[builtins.str] = None,
        application_insights_connection_string: typing.Optional[builtins.str] = None,
        application_insights_key: typing.Optional[builtins.str] = None,
        app_service_logs: typing.Optional[typing.Union["FunctionAppFlexConsumptionSiteConfigAppServiceLogs", typing.Dict[builtins.str, typing.Any]]] = None,
        container_registry_managed_identity_client_id: typing.Optional[builtins.str] = None,
        container_registry_use_managed_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cors: typing.Optional[typing.Union["FunctionAppFlexConsumptionSiteConfigCors", typing.Dict[builtins.str, typing.Any]]] = None,
        default_documents: typing.Optional[typing.Sequence[builtins.str]] = None,
        elastic_instance_minimum: typing.Optional[jsii.Number] = None,
        health_check_eviction_time_in_min: typing.Optional[jsii.Number] = None,
        health_check_path: typing.Optional[builtins.str] = None,
        http2_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ip_restriction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FunctionAppFlexConsumptionSiteConfigIpRestriction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ip_restriction_default_action: typing.Optional[builtins.str] = None,
        load_balancing_mode: typing.Optional[builtins.str] = None,
        managed_pipeline_mode: typing.Optional[builtins.str] = None,
        minimum_tls_version: typing.Optional[builtins.str] = None,
        remote_debugging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        remote_debugging_version: typing.Optional[builtins.str] = None,
        runtime_scale_monitoring_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        scm_ip_restriction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FunctionAppFlexConsumptionSiteConfigScmIpRestriction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        scm_ip_restriction_default_action: typing.Optional[builtins.str] = None,
        scm_minimum_tls_version: typing.Optional[builtins.str] = None,
        scm_use_main_ip_restriction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use32_bit_worker: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vnet_route_all_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        websockets_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        worker_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param api_definition_url: The URL of the API definition that describes this Linux Function App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#api_definition_url FunctionAppFlexConsumption#api_definition_url}
        :param api_management_api_id: The ID of the API Management API for this Linux Function App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#api_management_api_id FunctionAppFlexConsumption#api_management_api_id}
        :param app_command_line: The program and any arguments used to launch this app via the command line. (Example ``node myapp.js``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#app_command_line FunctionAppFlexConsumption#app_command_line}
        :param application_insights_connection_string: The Connection String for linking the Linux Function App to Application Insights. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#application_insights_connection_string FunctionAppFlexConsumption#application_insights_connection_string}
        :param application_insights_key: The Instrumentation Key for connecting the Linux Function App to Application Insights. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#application_insights_key FunctionAppFlexConsumption#application_insights_key}
        :param app_service_logs: app_service_logs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#app_service_logs FunctionAppFlexConsumption#app_service_logs}
        :param container_registry_managed_identity_client_id: The Client ID of the Managed Service Identity to use for connections to the Azure Container Registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#container_registry_managed_identity_client_id FunctionAppFlexConsumption#container_registry_managed_identity_client_id}
        :param container_registry_use_managed_identity: Should connections for Azure Container Registry use Managed Identity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#container_registry_use_managed_identity FunctionAppFlexConsumption#container_registry_use_managed_identity}
        :param cors: cors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#cors FunctionAppFlexConsumption#cors}
        :param default_documents: Specifies a list of Default Documents for the Linux Web App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#default_documents FunctionAppFlexConsumption#default_documents}
        :param elastic_instance_minimum: The number of minimum instances for this Linux Function App. Only affects apps on Elastic Premium plans. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#elastic_instance_minimum FunctionAppFlexConsumption#elastic_instance_minimum}
        :param health_check_eviction_time_in_min: The amount of time in minutes that a node is unhealthy before being removed from the load balancer. Possible values are between ``2`` and ``10``. Only valid in conjunction with ``health_check_path`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#health_check_eviction_time_in_min FunctionAppFlexConsumption#health_check_eviction_time_in_min}
        :param health_check_path: The path to be checked for this function app health. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#health_check_path FunctionAppFlexConsumption#health_check_path}
        :param http2_enabled: Specifies if the http2 protocol should be enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#http2_enabled FunctionAppFlexConsumption#http2_enabled}
        :param ip_restriction: ip_restriction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#ip_restriction FunctionAppFlexConsumption#ip_restriction}
        :param ip_restriction_default_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#ip_restriction_default_action FunctionAppFlexConsumption#ip_restriction_default_action}.
        :param load_balancing_mode: The Site load balancing mode. Possible values include: ``WeightedRoundRobin``, ``LeastRequests``, ``LeastResponseTime``, ``WeightedTotalTraffic``, ``RequestHash``, ``PerSiteRoundRobin``. Defaults to ``LeastRequests`` if omitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#load_balancing_mode FunctionAppFlexConsumption#load_balancing_mode}
        :param managed_pipeline_mode: The Managed Pipeline mode. Possible values include: ``Integrated``, ``Classic``. Defaults to ``Integrated``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#managed_pipeline_mode FunctionAppFlexConsumption#managed_pipeline_mode}
        :param minimum_tls_version: The configures the minimum version of TLS required for SSL requests. Possible values include: ``1.0``, ``1.1``, and ``1.2``. Defaults to ``1.2``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#minimum_tls_version FunctionAppFlexConsumption#minimum_tls_version}
        :param remote_debugging_enabled: Should Remote Debugging be enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#remote_debugging_enabled FunctionAppFlexConsumption#remote_debugging_enabled}
        :param remote_debugging_version: The Remote Debugging Version. Possible values include ``VS2017``, ``VS2019``, and `VS2022``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#remote_debugging_version FunctionAppFlexConsumption#remote_debugging_version}
        :param runtime_scale_monitoring_enabled: Should Functions Runtime Scale Monitoring be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#runtime_scale_monitoring_enabled FunctionAppFlexConsumption#runtime_scale_monitoring_enabled}
        :param scm_ip_restriction: scm_ip_restriction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#scm_ip_restriction FunctionAppFlexConsumption#scm_ip_restriction}
        :param scm_ip_restriction_default_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#scm_ip_restriction_default_action FunctionAppFlexConsumption#scm_ip_restriction_default_action}.
        :param scm_minimum_tls_version: Configures the minimum version of TLS required for SSL requests to the SCM site Possible values include: ``1.0``, ``1.1``, and ``1.2``. Defaults to ``1.2``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#scm_minimum_tls_version FunctionAppFlexConsumption#scm_minimum_tls_version}
        :param scm_use_main_ip_restriction: Should the Linux Function App ``ip_restriction`` configuration be used for the SCM also. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#scm_use_main_ip_restriction FunctionAppFlexConsumption#scm_use_main_ip_restriction}
        :param use32_bit_worker: Should the Linux Function App use a 32-bit worker. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#use_32_bit_worker FunctionAppFlexConsumption#use_32_bit_worker}
        :param vnet_route_all_enabled: Should the Linux Function App route all traffic through the virtual network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#vnet_route_all_enabled FunctionAppFlexConsumption#vnet_route_all_enabled}
        :param websockets_enabled: Should Web Sockets be enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#websockets_enabled FunctionAppFlexConsumption#websockets_enabled}
        :param worker_count: The number of Workers for this Linux Function App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#worker_count FunctionAppFlexConsumption#worker_count}
        '''
        value = FunctionAppFlexConsumptionSiteConfig(
            api_definition_url=api_definition_url,
            api_management_api_id=api_management_api_id,
            app_command_line=app_command_line,
            application_insights_connection_string=application_insights_connection_string,
            application_insights_key=application_insights_key,
            app_service_logs=app_service_logs,
            container_registry_managed_identity_client_id=container_registry_managed_identity_client_id,
            container_registry_use_managed_identity=container_registry_use_managed_identity,
            cors=cors,
            default_documents=default_documents,
            elastic_instance_minimum=elastic_instance_minimum,
            health_check_eviction_time_in_min=health_check_eviction_time_in_min,
            health_check_path=health_check_path,
            http2_enabled=http2_enabled,
            ip_restriction=ip_restriction,
            ip_restriction_default_action=ip_restriction_default_action,
            load_balancing_mode=load_balancing_mode,
            managed_pipeline_mode=managed_pipeline_mode,
            minimum_tls_version=minimum_tls_version,
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

    @jsii.member(jsii_name="putStickySettings")
    def put_sticky_settings(
        self,
        *,
        app_setting_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection_string_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param app_setting_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#app_setting_names FunctionAppFlexConsumption#app_setting_names}.
        :param connection_string_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#connection_string_names FunctionAppFlexConsumption#connection_string_names}.
        '''
        value = FunctionAppFlexConsumptionStickySettings(
            app_setting_names=app_setting_names,
            connection_string_names=connection_string_names,
        )

        return typing.cast(None, jsii.invoke(self, "putStickySettings", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#create FunctionAppFlexConsumption#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#delete FunctionAppFlexConsumption#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#read FunctionAppFlexConsumption#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#update FunctionAppFlexConsumption#update}.
        '''
        value = FunctionAppFlexConsumptionTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAlwaysReady")
    def reset_always_ready(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlwaysReady", []))

    @jsii.member(jsii_name="resetAppSettings")
    def reset_app_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppSettings", []))

    @jsii.member(jsii_name="resetAuthSettings")
    def reset_auth_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthSettings", []))

    @jsii.member(jsii_name="resetAuthSettingsV2")
    def reset_auth_settings_v2(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthSettingsV2", []))

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

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetHttpsOnly")
    def reset_https_only(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpsOnly", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetInstanceMemoryInMb")
    def reset_instance_memory_in_mb(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceMemoryInMb", []))

    @jsii.member(jsii_name="resetMaximumInstanceCount")
    def reset_maximum_instance_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumInstanceCount", []))

    @jsii.member(jsii_name="resetPublicNetworkAccessEnabled")
    def reset_public_network_access_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicNetworkAccessEnabled", []))

    @jsii.member(jsii_name="resetStickySettings")
    def reset_sticky_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStickySettings", []))

    @jsii.member(jsii_name="resetStorageAccessKey")
    def reset_storage_access_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageAccessKey", []))

    @jsii.member(jsii_name="resetStorageUserAssignedIdentityId")
    def reset_storage_user_assigned_identity_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageUserAssignedIdentityId", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetVirtualNetworkSubnetId")
    def reset_virtual_network_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVirtualNetworkSubnetId", []))

    @jsii.member(jsii_name="resetWebdeployPublishBasicAuthenticationEnabled")
    def reset_webdeploy_publish_basic_authentication_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebdeployPublishBasicAuthenticationEnabled", []))

    @jsii.member(jsii_name="resetZipDeployFile")
    def reset_zip_deploy_file(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZipDeployFile", []))

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
    @jsii.member(jsii_name="alwaysReady")
    def always_ready(self) -> "FunctionAppFlexConsumptionAlwaysReadyList":
        return typing.cast("FunctionAppFlexConsumptionAlwaysReadyList", jsii.get(self, "alwaysReady"))

    @builtins.property
    @jsii.member(jsii_name="authSettings")
    def auth_settings(self) -> "FunctionAppFlexConsumptionAuthSettingsOutputReference":
        return typing.cast("FunctionAppFlexConsumptionAuthSettingsOutputReference", jsii.get(self, "authSettings"))

    @builtins.property
    @jsii.member(jsii_name="authSettingsV2")
    def auth_settings_v2(
        self,
    ) -> "FunctionAppFlexConsumptionAuthSettingsV2OutputReference":
        return typing.cast("FunctionAppFlexConsumptionAuthSettingsV2OutputReference", jsii.get(self, "authSettingsV2"))

    @builtins.property
    @jsii.member(jsii_name="connectionString")
    def connection_string(self) -> "FunctionAppFlexConsumptionConnectionStringList":
        return typing.cast("FunctionAppFlexConsumptionConnectionStringList", jsii.get(self, "connectionString"))

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
    def identity(self) -> "FunctionAppFlexConsumptionIdentityOutputReference":
        return typing.cast("FunctionAppFlexConsumptionIdentityOutputReference", jsii.get(self, "identity"))

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
    def site_config(self) -> "FunctionAppFlexConsumptionSiteConfigOutputReference":
        return typing.cast("FunctionAppFlexConsumptionSiteConfigOutputReference", jsii.get(self, "siteConfig"))

    @builtins.property
    @jsii.member(jsii_name="siteCredential")
    def site_credential(self) -> "FunctionAppFlexConsumptionSiteCredentialList":
        return typing.cast("FunctionAppFlexConsumptionSiteCredentialList", jsii.get(self, "siteCredential"))

    @builtins.property
    @jsii.member(jsii_name="stickySettings")
    def sticky_settings(
        self,
    ) -> "FunctionAppFlexConsumptionStickySettingsOutputReference":
        return typing.cast("FunctionAppFlexConsumptionStickySettingsOutputReference", jsii.get(self, "stickySettings"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "FunctionAppFlexConsumptionTimeoutsOutputReference":
        return typing.cast("FunctionAppFlexConsumptionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="alwaysReadyInput")
    def always_ready_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionAppFlexConsumptionAlwaysReady"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionAppFlexConsumptionAlwaysReady"]]], jsii.get(self, "alwaysReadyInput"))

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
    ) -> typing.Optional["FunctionAppFlexConsumptionAuthSettings"]:
        return typing.cast(typing.Optional["FunctionAppFlexConsumptionAuthSettings"], jsii.get(self, "authSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="authSettingsV2Input")
    def auth_settings_v2_input(
        self,
    ) -> typing.Optional["FunctionAppFlexConsumptionAuthSettingsV2"]:
        return typing.cast(typing.Optional["FunctionAppFlexConsumptionAuthSettingsV2"], jsii.get(self, "authSettingsV2Input"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionAppFlexConsumptionConnectionString"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionAppFlexConsumptionConnectionString"]]], jsii.get(self, "connectionStringInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="httpsOnlyInput")
    def https_only_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "httpsOnlyInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional["FunctionAppFlexConsumptionIdentity"]:
        return typing.cast(typing.Optional["FunctionAppFlexConsumptionIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceMemoryInMbInput")
    def instance_memory_in_mb_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "instanceMemoryInMbInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumInstanceCountInput")
    def maximum_instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumInstanceCountInput"))

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
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeNameInput")
    def runtime_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="runtimeVersionInput")
    def runtime_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runtimeVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="servicePlanIdInput")
    def service_plan_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "servicePlanIdInput"))

    @builtins.property
    @jsii.member(jsii_name="siteConfigInput")
    def site_config_input(
        self,
    ) -> typing.Optional["FunctionAppFlexConsumptionSiteConfig"]:
        return typing.cast(typing.Optional["FunctionAppFlexConsumptionSiteConfig"], jsii.get(self, "siteConfigInput"))

    @builtins.property
    @jsii.member(jsii_name="stickySettingsInput")
    def sticky_settings_input(
        self,
    ) -> typing.Optional["FunctionAppFlexConsumptionStickySettings"]:
        return typing.cast(typing.Optional["FunctionAppFlexConsumptionStickySettings"], jsii.get(self, "stickySettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccessKeyInput")
    def storage_access_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAuthenticationTypeInput")
    def storage_authentication_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAuthenticationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="storageContainerEndpointInput")
    def storage_container_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageContainerEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="storageContainerTypeInput")
    def storage_container_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageContainerTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="storageUserAssignedIdentityIdInput")
    def storage_user_assigned_identity_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageUserAssignedIdentityIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "FunctionAppFlexConsumptionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "FunctionAppFlexConsumptionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkSubnetIdInput")
    def virtual_network_subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualNetworkSubnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="webdeployPublishBasicAuthenticationEnabledInput")
    def webdeploy_publish_basic_authentication_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "webdeployPublishBasicAuthenticationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="zipDeployFileInput")
    def zip_deploy_file_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "zipDeployFileInput"))

    @builtins.property
    @jsii.member(jsii_name="appSettings")
    def app_settings(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "appSettings"))

    @app_settings.setter
    def app_settings(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2feffe7e0c8fd657514c0217544cc4f23aec888f806bb4daede80fed151082a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appSettings", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__ba7e1674fee7b12b4948bf90a2f4c88b99d836db0684c887f47d9c296ab9618a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificateEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCertificateExclusionPaths")
    def client_certificate_exclusion_paths(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificateExclusionPaths"))

    @client_certificate_exclusion_paths.setter
    def client_certificate_exclusion_paths(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__338f64c22a046986a86d031df1039f2c5060a765bcc3cf24d9270276d89b5233)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificateExclusionPaths", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientCertificateMode")
    def client_certificate_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientCertificateMode"))

    @client_certificate_mode.setter
    def client_certificate_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0607c0220302892b64cbade88db326ae339c483aca1f532178dddabf988613ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientCertificateMode", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__b3365ab7303831e9a6f700eed7a3799ed66203c99cbd2d74820345e79d41fe3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__0b29511d734477ea729d4ffe81fec481ecfb24a43334c3e5b7706e170f8bace1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpsOnly", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51f1d08463b971cd1939807c870770d3b17641a6beb0c82f5dbcc22c434ba8be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="instanceMemoryInMb")
    def instance_memory_in_mb(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "instanceMemoryInMb"))

    @instance_memory_in_mb.setter
    def instance_memory_in_mb(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae4ac2f2b8e826c0416eabcc2c8c8b3dff04818e6d80e5a8071a91c972eb06f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceMemoryInMb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad347117faa54590d0661668f502301fd09c7155cdf13dcbda742ed478cb7766)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maximumInstanceCount")
    def maximum_instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumInstanceCount"))

    @maximum_instance_count.setter
    def maximum_instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__195fb5f066fd72f5e533199e9976369c64f607fe9880d078663af15e943cc94a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumInstanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b1470c16d75211ed1892dc753409ad0f789c6a8f2c76d99227a1b00667908a7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2463793ec9606242c88a572e248a680c26cf61fa7665f2377e1765fcb82d0212)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicNetworkAccessEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06a58b1961b33915d3d5fe41fa0dff62cfe6fd9fda1f87e1d2e971331aab5040)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeName")
    def runtime_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeName"))

    @runtime_name.setter
    def runtime_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72aef464f999321612e8c33c76e97b8d7ee60e6b3017e07a37fdd207d73fc4d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeVersion")
    def runtime_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeVersion"))

    @runtime_version.setter
    def runtime_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea6f2e9e91e0bd5500fe8b7ce51d4e017e56848137f754cf3333f83738ca532e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="servicePlanId")
    def service_plan_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "servicePlanId"))

    @service_plan_id.setter
    def service_plan_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f9ca24a10fc09e798a4a2ecfff33f4099aab1de89dbee9a26b7c5aea2053a66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "servicePlanId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAccessKey")
    def storage_access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccessKey"))

    @storage_access_key.setter
    def storage_access_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b3307af676806f38ed1654f0989109e4e6cedd9384cf7cbce7237e55b9d6215)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccessKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageAuthenticationType")
    def storage_authentication_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAuthenticationType"))

    @storage_authentication_type.setter
    def storage_authentication_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e63bc31b91af5018234c3f70da7bcf64f3e65fb9d795998ae68e86074a8f108)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAuthenticationType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageContainerEndpoint")
    def storage_container_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageContainerEndpoint"))

    @storage_container_endpoint.setter
    def storage_container_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06f52a3ac7562f81625802c791490faaa5494f1440e8e434c507f6666f83e557)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageContainerEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageContainerType")
    def storage_container_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageContainerType"))

    @storage_container_type.setter
    def storage_container_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88855aace53efc4934e3ba1cbbc6c84a004a9a57281c832bd66d057dbbde9b44)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageContainerType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="storageUserAssignedIdentityId")
    def storage_user_assigned_identity_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageUserAssignedIdentityId"))

    @storage_user_assigned_identity_id.setter
    def storage_user_assigned_identity_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__760fb3bf0d72bf9596367946fe13c8a010726297c4134b7b2378c7373b15cf31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageUserAssignedIdentityId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90e1c37b5ea9b3b7accd8b6ed27471a9b9c6c7302baaffd79389532328abb6f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkSubnetId")
    def virtual_network_subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkSubnetId"))

    @virtual_network_subnet_id.setter
    def virtual_network_subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9cb623e8c7a4e54dd592258a032d24323dd5a468c7c086b6d3b4465c3ab0956)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkSubnetId", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__c789f5c81b67a781bec1b961e7a1f6ea7b0f3cdf13c2c03ed6b819db4399d54b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webdeployPublishBasicAuthenticationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zipDeployFile")
    def zip_deploy_file(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "zipDeployFile"))

    @zip_deploy_file.setter
    def zip_deploy_file(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65550156545b88b41265d7f8f91fb89c366212463206b9b61a268893c323e188)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zipDeployFile", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAlwaysReady",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "instance_count": "instanceCount"},
)
class FunctionAppFlexConsumptionAlwaysReady:
    def __init__(
        self,
        *,
        name: builtins.str,
        instance_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#name FunctionAppFlexConsumption#name}.
        :param instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#instance_count FunctionAppFlexConsumption#instance_count}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8463a737a873ef7e79fda7a9794ba048e43b699cb216eb5ee2a17f57414696dc)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument instance_count", value=instance_count, expected_type=type_hints["instance_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if instance_count is not None:
            self._values["instance_count"] = instance_count

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#name FunctionAppFlexConsumption#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#instance_count FunctionAppFlexConsumption#instance_count}.'''
        result = self._values.get("instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionAppFlexConsumptionAlwaysReady(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionAppFlexConsumptionAlwaysReadyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAlwaysReadyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__601d27bfb3937ba5b7b76f0584163d5cbc72fe11b5cf60fcc3317ef2db676475)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FunctionAppFlexConsumptionAlwaysReadyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc043e2172cc1e0d72d2874882ab2f315d1d949a8c67223b26fa1c22bf0d4e15)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FunctionAppFlexConsumptionAlwaysReadyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b05646d97375cac84e7182ba145f3723d88d7a872ffdaf7edd2df5f089d5e5e2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b328212f440582ca6b75468ac0864b61e030f43aa46a9804ac8f96c73275035)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2594e6aca29f0cdb572fc4fa6d63af749c8129b6fda471e5646870e45400743e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionAlwaysReady]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionAlwaysReady]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionAlwaysReady]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58c188d29062303309e745b567546760d123f5235054c7bfb3b0de28f70dd921)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FunctionAppFlexConsumptionAlwaysReadyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAlwaysReadyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c27c7ce6c3ed96a59d85bdaec62bb1cf28563f81c9227030322e890a0e3a506)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetInstanceCount")
    def reset_instance_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstanceCount", []))

    @builtins.property
    @jsii.member(jsii_name="instanceCountInput")
    def instance_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "instanceCountInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="instanceCount")
    def instance_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "instanceCount"))

    @instance_count.setter
    def instance_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__644b7b7bf463e785eb90942265dedce4fb68833e07af18233e66ee03fb4dc20f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45de20ebc141bea7de9f3c14b61cc7a28a5fee9074bd7a168c0688bdbcf30cbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionAppFlexConsumptionAlwaysReady]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionAppFlexConsumptionAlwaysReady]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionAppFlexConsumptionAlwaysReady]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f7c905decdf813697fd6665266492cd489ce4a8bb7bb86f2d228c3dc55a40f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettings",
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
class FunctionAppFlexConsumptionAuthSettings:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        active_directory: typing.Optional[typing.Union["FunctionAppFlexConsumptionAuthSettingsActiveDirectory", typing.Dict[builtins.str, typing.Any]]] = None,
        additional_login_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        allowed_external_redirect_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
        default_provider: typing.Optional[builtins.str] = None,
        facebook: typing.Optional[typing.Union["FunctionAppFlexConsumptionAuthSettingsFacebook", typing.Dict[builtins.str, typing.Any]]] = None,
        github: typing.Optional[typing.Union["FunctionAppFlexConsumptionAuthSettingsGithub", typing.Dict[builtins.str, typing.Any]]] = None,
        google: typing.Optional[typing.Union["FunctionAppFlexConsumptionAuthSettingsGoogle", typing.Dict[builtins.str, typing.Any]]] = None,
        issuer: typing.Optional[builtins.str] = None,
        microsoft: typing.Optional[typing.Union["FunctionAppFlexConsumptionAuthSettingsMicrosoft", typing.Dict[builtins.str, typing.Any]]] = None,
        runtime_version: typing.Optional[builtins.str] = None,
        token_refresh_extension_hours: typing.Optional[jsii.Number] = None,
        token_store_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        twitter: typing.Optional[typing.Union["FunctionAppFlexConsumptionAuthSettingsTwitter", typing.Dict[builtins.str, typing.Any]]] = None,
        unauthenticated_client_action: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param enabled: Should the Authentication / Authorization feature be enabled? Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#enabled FunctionAppFlexConsumption#enabled}
        :param active_directory: active_directory block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#active_directory FunctionAppFlexConsumption#active_directory}
        :param additional_login_parameters: Specifies a map of Login Parameters to send to the OpenID Connect authorization endpoint when a user logs in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#additional_login_parameters FunctionAppFlexConsumption#additional_login_parameters}
        :param allowed_external_redirect_urls: Specifies a list of External URLs that can be redirected to as part of logging in or logging out of the Windows Web App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#allowed_external_redirect_urls FunctionAppFlexConsumption#allowed_external_redirect_urls}
        :param default_provider: The default authentication provider to use when multiple providers are configured. Possible values include: ``AzureActiveDirectory``, ``Facebook``, ``Google``, ``MicrosoftAccount``, ``Twitter``, ``Github``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#default_provider FunctionAppFlexConsumption#default_provider}
        :param facebook: facebook block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#facebook FunctionAppFlexConsumption#facebook}
        :param github: github block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#github FunctionAppFlexConsumption#github}
        :param google: google block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#google FunctionAppFlexConsumption#google}
        :param issuer: The OpenID Connect Issuer URI that represents the entity which issues access tokens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#issuer FunctionAppFlexConsumption#issuer}
        :param microsoft: microsoft block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#microsoft FunctionAppFlexConsumption#microsoft}
        :param runtime_version: The RuntimeVersion of the Authentication / Authorization feature in use. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#runtime_version FunctionAppFlexConsumption#runtime_version}
        :param token_refresh_extension_hours: The number of hours after session token expiration that a session token can be used to call the token refresh API. Defaults to ``72`` hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#token_refresh_extension_hours FunctionAppFlexConsumption#token_refresh_extension_hours}
        :param token_store_enabled: Should the Windows Web App durably store platform-specific security tokens that are obtained during login flows? Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#token_store_enabled FunctionAppFlexConsumption#token_store_enabled}
        :param twitter: twitter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#twitter FunctionAppFlexConsumption#twitter}
        :param unauthenticated_client_action: The action to take when an unauthenticated client attempts to access the app. Possible values include: ``RedirectToLoginPage``, ``AllowAnonymous``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#unauthenticated_client_action FunctionAppFlexConsumption#unauthenticated_client_action}
        '''
        if isinstance(active_directory, dict):
            active_directory = FunctionAppFlexConsumptionAuthSettingsActiveDirectory(**active_directory)
        if isinstance(facebook, dict):
            facebook = FunctionAppFlexConsumptionAuthSettingsFacebook(**facebook)
        if isinstance(github, dict):
            github = FunctionAppFlexConsumptionAuthSettingsGithub(**github)
        if isinstance(google, dict):
            google = FunctionAppFlexConsumptionAuthSettingsGoogle(**google)
        if isinstance(microsoft, dict):
            microsoft = FunctionAppFlexConsumptionAuthSettingsMicrosoft(**microsoft)
        if isinstance(twitter, dict):
            twitter = FunctionAppFlexConsumptionAuthSettingsTwitter(**twitter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33a5c2f61785385d03e582398da51411a6061765eaee2b3273c261f58c70a509)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#enabled FunctionAppFlexConsumption#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def active_directory(
        self,
    ) -> typing.Optional["FunctionAppFlexConsumptionAuthSettingsActiveDirectory"]:
        '''active_directory block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#active_directory FunctionAppFlexConsumption#active_directory}
        '''
        result = self._values.get("active_directory")
        return typing.cast(typing.Optional["FunctionAppFlexConsumptionAuthSettingsActiveDirectory"], result)

    @builtins.property
    def additional_login_parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Specifies a map of Login Parameters to send to the OpenID Connect authorization endpoint when a user logs in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#additional_login_parameters FunctionAppFlexConsumption#additional_login_parameters}
        '''
        result = self._values.get("additional_login_parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def allowed_external_redirect_urls(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of External URLs that can be redirected to as part of logging in or logging out of the Windows Web App.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#allowed_external_redirect_urls FunctionAppFlexConsumption#allowed_external_redirect_urls}
        '''
        result = self._values.get("allowed_external_redirect_urls")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def default_provider(self) -> typing.Optional[builtins.str]:
        '''The default authentication provider to use when multiple providers are configured.

        Possible values include: ``AzureActiveDirectory``, ``Facebook``, ``Google``, ``MicrosoftAccount``, ``Twitter``, ``Github``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#default_provider FunctionAppFlexConsumption#default_provider}
        '''
        result = self._values.get("default_provider")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def facebook(
        self,
    ) -> typing.Optional["FunctionAppFlexConsumptionAuthSettingsFacebook"]:
        '''facebook block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#facebook FunctionAppFlexConsumption#facebook}
        '''
        result = self._values.get("facebook")
        return typing.cast(typing.Optional["FunctionAppFlexConsumptionAuthSettingsFacebook"], result)

    @builtins.property
    def github(self) -> typing.Optional["FunctionAppFlexConsumptionAuthSettingsGithub"]:
        '''github block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#github FunctionAppFlexConsumption#github}
        '''
        result = self._values.get("github")
        return typing.cast(typing.Optional["FunctionAppFlexConsumptionAuthSettingsGithub"], result)

    @builtins.property
    def google(self) -> typing.Optional["FunctionAppFlexConsumptionAuthSettingsGoogle"]:
        '''google block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#google FunctionAppFlexConsumption#google}
        '''
        result = self._values.get("google")
        return typing.cast(typing.Optional["FunctionAppFlexConsumptionAuthSettingsGoogle"], result)

    @builtins.property
    def issuer(self) -> typing.Optional[builtins.str]:
        '''The OpenID Connect Issuer URI that represents the entity which issues access tokens.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#issuer FunctionAppFlexConsumption#issuer}
        '''
        result = self._values.get("issuer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def microsoft(
        self,
    ) -> typing.Optional["FunctionAppFlexConsumptionAuthSettingsMicrosoft"]:
        '''microsoft block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#microsoft FunctionAppFlexConsumption#microsoft}
        '''
        result = self._values.get("microsoft")
        return typing.cast(typing.Optional["FunctionAppFlexConsumptionAuthSettingsMicrosoft"], result)

    @builtins.property
    def runtime_version(self) -> typing.Optional[builtins.str]:
        '''The RuntimeVersion of the Authentication / Authorization feature in use.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#runtime_version FunctionAppFlexConsumption#runtime_version}
        '''
        result = self._values.get("runtime_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_refresh_extension_hours(self) -> typing.Optional[jsii.Number]:
        '''The number of hours after session token expiration that a session token can be used to call the token refresh API.

        Defaults to ``72`` hours.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#token_refresh_extension_hours FunctionAppFlexConsumption#token_refresh_extension_hours}
        '''
        result = self._values.get("token_refresh_extension_hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def token_store_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the Windows Web App durably store platform-specific security tokens that are obtained during login flows? Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#token_store_enabled FunctionAppFlexConsumption#token_store_enabled}
        '''
        result = self._values.get("token_store_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def twitter(
        self,
    ) -> typing.Optional["FunctionAppFlexConsumptionAuthSettingsTwitter"]:
        '''twitter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#twitter FunctionAppFlexConsumption#twitter}
        '''
        result = self._values.get("twitter")
        return typing.cast(typing.Optional["FunctionAppFlexConsumptionAuthSettingsTwitter"], result)

    @builtins.property
    def unauthenticated_client_action(self) -> typing.Optional[builtins.str]:
        '''The action to take when an unauthenticated client attempts to access the app. Possible values include: ``RedirectToLoginPage``, ``AllowAnonymous``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#unauthenticated_client_action FunctionAppFlexConsumption#unauthenticated_client_action}
        '''
        result = self._values.get("unauthenticated_client_action")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionAppFlexConsumptionAuthSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsActiveDirectory",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "allowed_audiences": "allowedAudiences",
        "client_secret": "clientSecret",
        "client_secret_setting_name": "clientSecretSettingName",
    },
)
class FunctionAppFlexConsumptionAuthSettingsActiveDirectory:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        allowed_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
        client_secret: typing.Optional[builtins.str] = None,
        client_secret_setting_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param client_id: The ID of the Client to use to authenticate with Azure Active Directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_id FunctionAppFlexConsumption#client_id}
        :param allowed_audiences: Specifies a list of Allowed audience values to consider when validating JWTs issued by Azure Active Directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#allowed_audiences FunctionAppFlexConsumption#allowed_audiences}
        :param client_secret: The Client Secret for the Client ID. Cannot be used with ``client_secret_setting_name``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret FunctionAppFlexConsumption#client_secret}
        :param client_secret_setting_name: The App Setting name that contains the client secret of the Client. Cannot be used with ``client_secret``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret_setting_name FunctionAppFlexConsumption#client_secret_setting_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5e6055c5e1def326ef64c02117c39a68690d59a1ab27e5c099bcbfe176028d8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_id FunctionAppFlexConsumption#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_audiences(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of Allowed audience values to consider when validating JWTs issued by Azure Active Directory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#allowed_audiences FunctionAppFlexConsumption#allowed_audiences}
        '''
        result = self._values.get("allowed_audiences")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''The Client Secret for the Client ID. Cannot be used with ``client_secret_setting_name``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret FunctionAppFlexConsumption#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret_setting_name(self) -> typing.Optional[builtins.str]:
        '''The App Setting name that contains the client secret of the Client. Cannot be used with ``client_secret``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret_setting_name FunctionAppFlexConsumption#client_secret_setting_name}
        '''
        result = self._values.get("client_secret_setting_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionAppFlexConsumptionAuthSettingsActiveDirectory(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionAppFlexConsumptionAuthSettingsActiveDirectoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsActiveDirectoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__41fdf5da4f6ce4657aa2c2dae68e2415c04ec83ec05cafd0ef4e23dacd45fc2b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ad38faa354a0fd31af190866d01d8878b47ea8b682c79da43a01cbd4675306b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedAudiences", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf79324d2a5cdec7cb3ee11b201477985f673f67558bbcf80a124a8447137a52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a475a5ee81b9e118670a0552330b22066a663b84c00b3a779555e7185812b7bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingName")
    def client_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecretSettingName"))

    @client_secret_setting_name.setter
    def client_secret_setting_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__984b8016a1515f22b826acb32a9b8315f9dcd3201f4d1d61678f7049fdf50f57)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecretSettingName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FunctionAppFlexConsumptionAuthSettingsActiveDirectory]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionAuthSettingsActiveDirectory], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionAppFlexConsumptionAuthSettingsActiveDirectory],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__631b5338e9a11f26ede5b83b78b6dcc912a4ddb2385f10d5bd31f1e29fcadd7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsFacebook",
    jsii_struct_bases=[],
    name_mapping={
        "app_id": "appId",
        "app_secret": "appSecret",
        "app_secret_setting_name": "appSecretSettingName",
        "oauth_scopes": "oauthScopes",
    },
)
class FunctionAppFlexConsumptionAuthSettingsFacebook:
    def __init__(
        self,
        *,
        app_id: builtins.str,
        app_secret: typing.Optional[builtins.str] = None,
        app_secret_setting_name: typing.Optional[builtins.str] = None,
        oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param app_id: The App ID of the Facebook app used for login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#app_id FunctionAppFlexConsumption#app_id}
        :param app_secret: The App Secret of the Facebook app used for Facebook Login. Cannot be specified with ``app_secret_setting_name``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#app_secret FunctionAppFlexConsumption#app_secret}
        :param app_secret_setting_name: The app setting name that contains the ``app_secret`` value used for Facebook Login. Cannot be specified with ``app_secret``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#app_secret_setting_name FunctionAppFlexConsumption#app_secret_setting_name}
        :param oauth_scopes: Specifies a list of OAuth 2.0 scopes to be requested as part of Facebook Login authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#oauth_scopes FunctionAppFlexConsumption#oauth_scopes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c9bc3da4ed6fe0bdd2a055f42cc1fe9d8a4bc7a8557519e8ce34a31441601a4)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#app_id FunctionAppFlexConsumption#app_id}
        '''
        result = self._values.get("app_id")
        assert result is not None, "Required property 'app_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_secret(self) -> typing.Optional[builtins.str]:
        '''The App Secret of the Facebook app used for Facebook Login. Cannot be specified with ``app_secret_setting_name``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#app_secret FunctionAppFlexConsumption#app_secret}
        '''
        result = self._values.get("app_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app_secret_setting_name(self) -> typing.Optional[builtins.str]:
        '''The app setting name that contains the ``app_secret`` value used for Facebook Login. Cannot be specified with ``app_secret``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#app_secret_setting_name FunctionAppFlexConsumption#app_secret_setting_name}
        '''
        result = self._values.get("app_secret_setting_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of OAuth 2.0 scopes to be requested as part of Facebook Login authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#oauth_scopes FunctionAppFlexConsumption#oauth_scopes}
        '''
        result = self._values.get("oauth_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionAppFlexConsumptionAuthSettingsFacebook(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionAppFlexConsumptionAuthSettingsFacebookOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsFacebookOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c9461a898efcf67b81bcbfc874aa50edd07b9247a53058d39f31d935155f34e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3af25de99670b0fbfe0a8ae003ed06ec11408c8690b6dceaa24b5f4b87d6a9be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appSecret")
    def app_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appSecret"))

    @app_secret.setter
    def app_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dca3ff37da32528c30ddb9ae3b13924e1fef5a3edaca6adf409205d76aedb9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appSecretSettingName")
    def app_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appSecretSettingName"))

    @app_secret_setting_name.setter
    def app_secret_setting_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__297b19eb3e8039fd170a75910a4c6aa8e74af2f936f4153209bd1801ced75ad2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appSecretSettingName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthScopes")
    def oauth_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "oauthScopes"))

    @oauth_scopes.setter
    def oauth_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1eaf85798af5370eafa1f1a69a0fd5c189449c752a27c99673b8e252d6f6cf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthScopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FunctionAppFlexConsumptionAuthSettingsFacebook]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionAuthSettingsFacebook], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionAppFlexConsumptionAuthSettingsFacebook],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b66aa716fb035544d9d9b943a5e0379056fcef364e8b407c8a65bcf6f8137a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsGithub",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "client_secret_setting_name": "clientSecretSettingName",
        "oauth_scopes": "oauthScopes",
    },
)
class FunctionAppFlexConsumptionAuthSettingsGithub:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        client_secret: typing.Optional[builtins.str] = None,
        client_secret_setting_name: typing.Optional[builtins.str] = None,
        oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param client_id: The ID of the GitHub app used for login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_id FunctionAppFlexConsumption#client_id}
        :param client_secret: The Client Secret of the GitHub app used for GitHub Login. Cannot be specified with ``client_secret_setting_name``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret FunctionAppFlexConsumption#client_secret}
        :param client_secret_setting_name: The app setting name that contains the ``client_secret`` value used for GitHub Login. Cannot be specified with ``client_secret``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret_setting_name FunctionAppFlexConsumption#client_secret_setting_name}
        :param oauth_scopes: Specifies a list of OAuth 2.0 scopes that will be requested as part of GitHub Login authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#oauth_scopes FunctionAppFlexConsumption#oauth_scopes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c79c91699c982418e73af8c56c29efd7dda593ceec4a2da48b2f15c7b51035c8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_id FunctionAppFlexConsumption#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''The Client Secret of the GitHub app used for GitHub Login. Cannot be specified with ``client_secret_setting_name``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret FunctionAppFlexConsumption#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret_setting_name(self) -> typing.Optional[builtins.str]:
        '''The app setting name that contains the ``client_secret`` value used for GitHub Login. Cannot be specified with ``client_secret``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret_setting_name FunctionAppFlexConsumption#client_secret_setting_name}
        '''
        result = self._values.get("client_secret_setting_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of OAuth 2.0 scopes that will be requested as part of GitHub Login authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#oauth_scopes FunctionAppFlexConsumption#oauth_scopes}
        '''
        result = self._values.get("oauth_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionAppFlexConsumptionAuthSettingsGithub(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionAppFlexConsumptionAuthSettingsGithubOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsGithubOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7b7dde99db6a75920cfa2b939d43c56d7780e88dfcd40a11b3652abdb3f6a1ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a2ebca37913e5c75d6f9aadc8ec0ca0fc0009486621a8eba881529a583ac1af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0319bc9f8cd8401cae1f08414544d20e642f63ed08b6bf468aecc63059973d62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingName")
    def client_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecretSettingName"))

    @client_secret_setting_name.setter
    def client_secret_setting_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__624b36a374b5fffeaac90016f4b1550e7b4310e7a0037914911c6ea3c9ffb7a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecretSettingName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthScopes")
    def oauth_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "oauthScopes"))

    @oauth_scopes.setter
    def oauth_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d23a55441f403a2e772889dd8a6fb50fedbb9dda1e2a0135439ebe70e890e14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthScopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FunctionAppFlexConsumptionAuthSettingsGithub]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionAuthSettingsGithub], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionAppFlexConsumptionAuthSettingsGithub],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53c7f51cefb6d0e53a21caf54d45e63444093541b317d78c2290176b78ffb89b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsGoogle",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "client_secret_setting_name": "clientSecretSettingName",
        "oauth_scopes": "oauthScopes",
    },
)
class FunctionAppFlexConsumptionAuthSettingsGoogle:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        client_secret: typing.Optional[builtins.str] = None,
        client_secret_setting_name: typing.Optional[builtins.str] = None,
        oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param client_id: The OpenID Connect Client ID for the Google web application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_id FunctionAppFlexConsumption#client_id}
        :param client_secret: The client secret associated with the Google web application. Cannot be specified with ``client_secret_setting_name``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret FunctionAppFlexConsumption#client_secret}
        :param client_secret_setting_name: The app setting name that contains the ``client_secret`` value used for Google Login. Cannot be specified with ``client_secret``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret_setting_name FunctionAppFlexConsumption#client_secret_setting_name}
        :param oauth_scopes: Specifies a list of OAuth 2.0 scopes that will be requested as part of Google Sign-In authentication. If not specified, "openid", "profile", and "email" are used as default scopes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#oauth_scopes FunctionAppFlexConsumption#oauth_scopes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__794063635fa89eb2055cc87f151fce401807ab61f387b80b74b30cd208819687)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_id FunctionAppFlexConsumption#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''The client secret associated with the Google web application.  Cannot be specified with ``client_secret_setting_name``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret FunctionAppFlexConsumption#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret_setting_name(self) -> typing.Optional[builtins.str]:
        '''The app setting name that contains the ``client_secret`` value used for Google Login. Cannot be specified with ``client_secret``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret_setting_name FunctionAppFlexConsumption#client_secret_setting_name}
        '''
        result = self._values.get("client_secret_setting_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of OAuth 2.0 scopes that will be requested as part of Google Sign-In authentication. If not specified, "openid", "profile", and "email" are used as default scopes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#oauth_scopes FunctionAppFlexConsumption#oauth_scopes}
        '''
        result = self._values.get("oauth_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionAppFlexConsumptionAuthSettingsGoogle(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionAppFlexConsumptionAuthSettingsGoogleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsGoogleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3672946e00797a6c9cd0e2b2fac1d1d7b53c62dd39b3f17ff1ae14026954aa27)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b4a82fdee529d662e7ee852c5ccb750a596b918d25f1cc060021a128b04df77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0c940b69a9669c004326680cb3b3cb00834804940bd3ef844a8356997e2c0a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingName")
    def client_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecretSettingName"))

    @client_secret_setting_name.setter
    def client_secret_setting_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__075283454b4bd3d677f886e38fc5ec801e2949d59fb9ea379b50bc6309f4c2ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecretSettingName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthScopes")
    def oauth_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "oauthScopes"))

    @oauth_scopes.setter
    def oauth_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__453eef960d6646fabda0de26105466f31fa207043c77410a87bd48e2b2518677)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthScopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FunctionAppFlexConsumptionAuthSettingsGoogle]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionAuthSettingsGoogle], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionAppFlexConsumptionAuthSettingsGoogle],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4ff8d7ea9bb4fc358c7bd64e17b6f51014840357cf6e324f5e74c7753e77d6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsMicrosoft",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "client_secret": "clientSecret",
        "client_secret_setting_name": "clientSecretSettingName",
        "oauth_scopes": "oauthScopes",
    },
)
class FunctionAppFlexConsumptionAuthSettingsMicrosoft:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        client_secret: typing.Optional[builtins.str] = None,
        client_secret_setting_name: typing.Optional[builtins.str] = None,
        oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param client_id: The OAuth 2.0 client ID that was created for the app used for authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_id FunctionAppFlexConsumption#client_id}
        :param client_secret: The OAuth 2.0 client secret that was created for the app used for authentication. Cannot be specified with ``client_secret_setting_name``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret FunctionAppFlexConsumption#client_secret}
        :param client_secret_setting_name: The app setting name containing the OAuth 2.0 client secret that was created for the app used for authentication. Cannot be specified with ``client_secret``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret_setting_name FunctionAppFlexConsumption#client_secret_setting_name}
        :param oauth_scopes: The list of OAuth 2.0 scopes that will be requested as part of Microsoft Account authentication. If not specified, ``wl.basic`` is used as the default scope. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#oauth_scopes FunctionAppFlexConsumption#oauth_scopes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98f2797aa67df612d5288813ab95d1c15223b7b4dbe09d4f8a09b0c5586f2c41)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_id FunctionAppFlexConsumption#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''The OAuth 2.0 client secret that was created for the app used for authentication. Cannot be specified with ``client_secret_setting_name``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret FunctionAppFlexConsumption#client_secret}
        '''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret_setting_name(self) -> typing.Optional[builtins.str]:
        '''The app setting name containing the OAuth 2.0 client secret that was created for the app used for authentication. Cannot be specified with ``client_secret``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret_setting_name FunctionAppFlexConsumption#client_secret_setting_name}
        '''
        result = self._values.get("client_secret_setting_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of OAuth 2.0 scopes that will be requested as part of Microsoft Account authentication. If not specified, ``wl.basic`` is used as the default scope.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#oauth_scopes FunctionAppFlexConsumption#oauth_scopes}
        '''
        result = self._values.get("oauth_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionAppFlexConsumptionAuthSettingsMicrosoft(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionAppFlexConsumptionAuthSettingsMicrosoftOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsMicrosoftOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2e63e8b841c7a34e76329ca7c49f2a77b54d7ad838b5586a618340d43c7ce10c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__135bd3c4e55942e8ab53c4b7e36de25ebb54c4f1e16702cb922d430242acbd26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c22080a72461f9a1f210842409de8d455b2e572412e976a172ca65006c74de59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingName")
    def client_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecretSettingName"))

    @client_secret_setting_name.setter
    def client_secret_setting_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe758c92fc41bd1de24bf364c6faeefb506f958b2bcdce5f8ea5f25e65e69c75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecretSettingName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="oauthScopes")
    def oauth_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "oauthScopes"))

    @oauth_scopes.setter
    def oauth_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f46453a7bf6d2f3ac36f461612134db053354874205432b31cf597a40941178)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthScopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FunctionAppFlexConsumptionAuthSettingsMicrosoft]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionAuthSettingsMicrosoft], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionAppFlexConsumptionAuthSettingsMicrosoft],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44f4dcd4892432840e6099387ee26acdd1a5d3be92180481224b2bd663ab7d15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FunctionAppFlexConsumptionAuthSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e995ceb8548a695e0b4c0d2d1c5ac09614d61a6305135e54f695f65a1f85e5e)
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
        :param client_id: The ID of the Client to use to authenticate with Azure Active Directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_id FunctionAppFlexConsumption#client_id}
        :param allowed_audiences: Specifies a list of Allowed audience values to consider when validating JWTs issued by Azure Active Directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#allowed_audiences FunctionAppFlexConsumption#allowed_audiences}
        :param client_secret: The Client Secret for the Client ID. Cannot be used with ``client_secret_setting_name``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret FunctionAppFlexConsumption#client_secret}
        :param client_secret_setting_name: The App Setting name that contains the client secret of the Client. Cannot be used with ``client_secret``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret_setting_name FunctionAppFlexConsumption#client_secret_setting_name}
        '''
        value = FunctionAppFlexConsumptionAuthSettingsActiveDirectory(
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
        :param app_id: The App ID of the Facebook app used for login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#app_id FunctionAppFlexConsumption#app_id}
        :param app_secret: The App Secret of the Facebook app used for Facebook Login. Cannot be specified with ``app_secret_setting_name``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#app_secret FunctionAppFlexConsumption#app_secret}
        :param app_secret_setting_name: The app setting name that contains the ``app_secret`` value used for Facebook Login. Cannot be specified with ``app_secret``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#app_secret_setting_name FunctionAppFlexConsumption#app_secret_setting_name}
        :param oauth_scopes: Specifies a list of OAuth 2.0 scopes to be requested as part of Facebook Login authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#oauth_scopes FunctionAppFlexConsumption#oauth_scopes}
        '''
        value = FunctionAppFlexConsumptionAuthSettingsFacebook(
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
        :param client_id: The ID of the GitHub app used for login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_id FunctionAppFlexConsumption#client_id}
        :param client_secret: The Client Secret of the GitHub app used for GitHub Login. Cannot be specified with ``client_secret_setting_name``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret FunctionAppFlexConsumption#client_secret}
        :param client_secret_setting_name: The app setting name that contains the ``client_secret`` value used for GitHub Login. Cannot be specified with ``client_secret``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret_setting_name FunctionAppFlexConsumption#client_secret_setting_name}
        :param oauth_scopes: Specifies a list of OAuth 2.0 scopes that will be requested as part of GitHub Login authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#oauth_scopes FunctionAppFlexConsumption#oauth_scopes}
        '''
        value = FunctionAppFlexConsumptionAuthSettingsGithub(
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
        :param client_id: The OpenID Connect Client ID for the Google web application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_id FunctionAppFlexConsumption#client_id}
        :param client_secret: The client secret associated with the Google web application. Cannot be specified with ``client_secret_setting_name``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret FunctionAppFlexConsumption#client_secret}
        :param client_secret_setting_name: The app setting name that contains the ``client_secret`` value used for Google Login. Cannot be specified with ``client_secret``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret_setting_name FunctionAppFlexConsumption#client_secret_setting_name}
        :param oauth_scopes: Specifies a list of OAuth 2.0 scopes that will be requested as part of Google Sign-In authentication. If not specified, "openid", "profile", and "email" are used as default scopes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#oauth_scopes FunctionAppFlexConsumption#oauth_scopes}
        '''
        value = FunctionAppFlexConsumptionAuthSettingsGoogle(
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
        :param client_id: The OAuth 2.0 client ID that was created for the app used for authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_id FunctionAppFlexConsumption#client_id}
        :param client_secret: The OAuth 2.0 client secret that was created for the app used for authentication. Cannot be specified with ``client_secret_setting_name``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret FunctionAppFlexConsumption#client_secret}
        :param client_secret_setting_name: The app setting name containing the OAuth 2.0 client secret that was created for the app used for authentication. Cannot be specified with ``client_secret``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret_setting_name FunctionAppFlexConsumption#client_secret_setting_name}
        :param oauth_scopes: The list of OAuth 2.0 scopes that will be requested as part of Microsoft Account authentication. If not specified, ``wl.basic`` is used as the default scope. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#oauth_scopes FunctionAppFlexConsumption#oauth_scopes}
        '''
        value = FunctionAppFlexConsumptionAuthSettingsMicrosoft(
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
        :param consumer_key: The OAuth 1.0a consumer key of the Twitter application used for sign-in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#consumer_key FunctionAppFlexConsumption#consumer_key}
        :param consumer_secret: The OAuth 1.0a consumer secret of the Twitter application used for sign-in. Cannot be specified with ``consumer_secret_setting_name``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#consumer_secret FunctionAppFlexConsumption#consumer_secret}
        :param consumer_secret_setting_name: The app setting name that contains the OAuth 1.0a consumer secret of the Twitter application used for sign-in. Cannot be specified with ``consumer_secret``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#consumer_secret_setting_name FunctionAppFlexConsumption#consumer_secret_setting_name}
        '''
        value = FunctionAppFlexConsumptionAuthSettingsTwitter(
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
    ) -> FunctionAppFlexConsumptionAuthSettingsActiveDirectoryOutputReference:
        return typing.cast(FunctionAppFlexConsumptionAuthSettingsActiveDirectoryOutputReference, jsii.get(self, "activeDirectory"))

    @builtins.property
    @jsii.member(jsii_name="facebook")
    def facebook(self) -> FunctionAppFlexConsumptionAuthSettingsFacebookOutputReference:
        return typing.cast(FunctionAppFlexConsumptionAuthSettingsFacebookOutputReference, jsii.get(self, "facebook"))

    @builtins.property
    @jsii.member(jsii_name="github")
    def github(self) -> FunctionAppFlexConsumptionAuthSettingsGithubOutputReference:
        return typing.cast(FunctionAppFlexConsumptionAuthSettingsGithubOutputReference, jsii.get(self, "github"))

    @builtins.property
    @jsii.member(jsii_name="google")
    def google(self) -> FunctionAppFlexConsumptionAuthSettingsGoogleOutputReference:
        return typing.cast(FunctionAppFlexConsumptionAuthSettingsGoogleOutputReference, jsii.get(self, "google"))

    @builtins.property
    @jsii.member(jsii_name="microsoft")
    def microsoft(
        self,
    ) -> FunctionAppFlexConsumptionAuthSettingsMicrosoftOutputReference:
        return typing.cast(FunctionAppFlexConsumptionAuthSettingsMicrosoftOutputReference, jsii.get(self, "microsoft"))

    @builtins.property
    @jsii.member(jsii_name="twitter")
    def twitter(self) -> "FunctionAppFlexConsumptionAuthSettingsTwitterOutputReference":
        return typing.cast("FunctionAppFlexConsumptionAuthSettingsTwitterOutputReference", jsii.get(self, "twitter"))

    @builtins.property
    @jsii.member(jsii_name="activeDirectoryInput")
    def active_directory_input(
        self,
    ) -> typing.Optional[FunctionAppFlexConsumptionAuthSettingsActiveDirectory]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionAuthSettingsActiveDirectory], jsii.get(self, "activeDirectoryInput"))

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
    ) -> typing.Optional[FunctionAppFlexConsumptionAuthSettingsFacebook]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionAuthSettingsFacebook], jsii.get(self, "facebookInput"))

    @builtins.property
    @jsii.member(jsii_name="githubInput")
    def github_input(
        self,
    ) -> typing.Optional[FunctionAppFlexConsumptionAuthSettingsGithub]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionAuthSettingsGithub], jsii.get(self, "githubInput"))

    @builtins.property
    @jsii.member(jsii_name="googleInput")
    def google_input(
        self,
    ) -> typing.Optional[FunctionAppFlexConsumptionAuthSettingsGoogle]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionAuthSettingsGoogle], jsii.get(self, "googleInput"))

    @builtins.property
    @jsii.member(jsii_name="issuerInput")
    def issuer_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "issuerInput"))

    @builtins.property
    @jsii.member(jsii_name="microsoftInput")
    def microsoft_input(
        self,
    ) -> typing.Optional[FunctionAppFlexConsumptionAuthSettingsMicrosoft]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionAuthSettingsMicrosoft], jsii.get(self, "microsoftInput"))

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
    ) -> typing.Optional["FunctionAppFlexConsumptionAuthSettingsTwitter"]:
        return typing.cast(typing.Optional["FunctionAppFlexConsumptionAuthSettingsTwitter"], jsii.get(self, "twitterInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e5c92207bc8a3bd7c44199d18b97f28f51e1c6068313a03502b1d93b4c325919)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "additionalLoginParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedExternalRedirectUrls")
    def allowed_external_redirect_urls(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedExternalRedirectUrls"))

    @allowed_external_redirect_urls.setter
    def allowed_external_redirect_urls(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1626c69318c117f27424bd324df5f1470ec98e26fa2fbd09ffc4892933920c4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedExternalRedirectUrls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultProvider")
    def default_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultProvider"))

    @default_provider.setter
    def default_provider(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77752df7f71ee219849439584d5cb00d4290916db3af84415cbedafee297967d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5de1e4f08043f02b83115093b5499adce62e8e5da3f9c4f6b0291fd1ea10abcc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="issuer")
    def issuer(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "issuer"))

    @issuer.setter
    def issuer(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b25df2e1dc45b15a8c5cb15da1997cb4ad963ed9f5112f42146e7358464ffa29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "issuer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeVersion")
    def runtime_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeVersion"))

    @runtime_version.setter
    def runtime_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9669d52682b32a7135fc4efb57bc61b4a5118b1de04562a2eccc97918d0d7fe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenRefreshExtensionHours")
    def token_refresh_extension_hours(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tokenRefreshExtensionHours"))

    @token_refresh_extension_hours.setter
    def token_refresh_extension_hours(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aa01dee91374af0aca56b60b07f4200720c33922e6bbe491e1420f5147c2e06)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ffd9ae4971930028526b4419e825250a749a31e6572cef7127776b39527209e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenStoreEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unauthenticatedClientAction")
    def unauthenticated_client_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unauthenticatedClientAction"))

    @unauthenticated_client_action.setter
    def unauthenticated_client_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fe34949bcc9e793d2537ea101c89dd79a204f98013722adc65270a08685343e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unauthenticatedClientAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FunctionAppFlexConsumptionAuthSettings]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionAuthSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionAppFlexConsumptionAuthSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73bce6704887edc788c2317c30c696ce523e905379510ffafea1f6d7179c2c88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsTwitter",
    jsii_struct_bases=[],
    name_mapping={
        "consumer_key": "consumerKey",
        "consumer_secret": "consumerSecret",
        "consumer_secret_setting_name": "consumerSecretSettingName",
    },
)
class FunctionAppFlexConsumptionAuthSettingsTwitter:
    def __init__(
        self,
        *,
        consumer_key: builtins.str,
        consumer_secret: typing.Optional[builtins.str] = None,
        consumer_secret_setting_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param consumer_key: The OAuth 1.0a consumer key of the Twitter application used for sign-in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#consumer_key FunctionAppFlexConsumption#consumer_key}
        :param consumer_secret: The OAuth 1.0a consumer secret of the Twitter application used for sign-in. Cannot be specified with ``consumer_secret_setting_name``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#consumer_secret FunctionAppFlexConsumption#consumer_secret}
        :param consumer_secret_setting_name: The app setting name that contains the OAuth 1.0a consumer secret of the Twitter application used for sign-in. Cannot be specified with ``consumer_secret``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#consumer_secret_setting_name FunctionAppFlexConsumption#consumer_secret_setting_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dacb4f234063a53547ec53cf68ff7e3971654da48aa2bd924fa83df696c3ce7)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#consumer_key FunctionAppFlexConsumption#consumer_key}
        '''
        result = self._values.get("consumer_key")
        assert result is not None, "Required property 'consumer_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def consumer_secret(self) -> typing.Optional[builtins.str]:
        '''The OAuth 1.0a consumer secret of the Twitter application used for sign-in. Cannot be specified with ``consumer_secret_setting_name``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#consumer_secret FunctionAppFlexConsumption#consumer_secret}
        '''
        result = self._values.get("consumer_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def consumer_secret_setting_name(self) -> typing.Optional[builtins.str]:
        '''The app setting name that contains the OAuth 1.0a consumer secret of the Twitter application used for sign-in. Cannot be specified with ``consumer_secret``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#consumer_secret_setting_name FunctionAppFlexConsumption#consumer_secret_setting_name}
        '''
        result = self._values.get("consumer_secret_setting_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionAppFlexConsumptionAuthSettingsTwitter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionAppFlexConsumptionAuthSettingsTwitterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsTwitterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1dae5c770be4f0d8794fe11f76066fcc4108cf2adbdb350f2e7cdd7178e9b4bd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8687c9577386820c4da2cd5f55637458b87718975b4b592b7ab3b1bfd42d6f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="consumerSecret")
    def consumer_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerSecret"))

    @consumer_secret.setter
    def consumer_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f5c27fc84a41e5053fa40cd5faa61a9651f1c1cbbac03e86dedc2148cfd2d64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerSecret", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="consumerSecretSettingName")
    def consumer_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerSecretSettingName"))

    @consumer_secret_setting_name.setter
    def consumer_secret_setting_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__712974a263b67e04ff13091a035aee3bdf10fed0a456cba2bbbda656a9912d70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerSecretSettingName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FunctionAppFlexConsumptionAuthSettingsTwitter]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionAuthSettingsTwitter], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionAppFlexConsumptionAuthSettingsTwitter],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__736d6c13225d1e8325aa49acee9fe70c11156b426d856884c733d019e854692d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsV2",
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
class FunctionAppFlexConsumptionAuthSettingsV2:
    def __init__(
        self,
        *,
        login: typing.Union["FunctionAppFlexConsumptionAuthSettingsV2Login", typing.Dict[builtins.str, typing.Any]],
        active_directory_v2: typing.Optional[typing.Union["FunctionAppFlexConsumptionAuthSettingsV2ActiveDirectoryV2", typing.Dict[builtins.str, typing.Any]]] = None,
        apple_v2: typing.Optional[typing.Union["FunctionAppFlexConsumptionAuthSettingsV2AppleV2", typing.Dict[builtins.str, typing.Any]]] = None,
        auth_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        azure_static_web_app_v2: typing.Optional[typing.Union["FunctionAppFlexConsumptionAuthSettingsV2AzureStaticWebAppV2", typing.Dict[builtins.str, typing.Any]]] = None,
        config_file_path: typing.Optional[builtins.str] = None,
        custom_oidc_v2: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FunctionAppFlexConsumptionAuthSettingsV2CustomOidcV2", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_provider: typing.Optional[builtins.str] = None,
        excluded_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        facebook_v2: typing.Optional[typing.Union["FunctionAppFlexConsumptionAuthSettingsV2FacebookV2", typing.Dict[builtins.str, typing.Any]]] = None,
        forward_proxy_convention: typing.Optional[builtins.str] = None,
        forward_proxy_custom_host_header_name: typing.Optional[builtins.str] = None,
        forward_proxy_custom_scheme_header_name: typing.Optional[builtins.str] = None,
        github_v2: typing.Optional[typing.Union["FunctionAppFlexConsumptionAuthSettingsV2GithubV2", typing.Dict[builtins.str, typing.Any]]] = None,
        google_v2: typing.Optional[typing.Union["FunctionAppFlexConsumptionAuthSettingsV2GoogleV2", typing.Dict[builtins.str, typing.Any]]] = None,
        http_route_api_prefix: typing.Optional[builtins.str] = None,
        microsoft_v2: typing.Optional[typing.Union["FunctionAppFlexConsumptionAuthSettingsV2MicrosoftV2", typing.Dict[builtins.str, typing.Any]]] = None,
        require_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        require_https: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        runtime_version: typing.Optional[builtins.str] = None,
        twitter_v2: typing.Optional[typing.Union["FunctionAppFlexConsumptionAuthSettingsV2TwitterV2", typing.Dict[builtins.str, typing.Any]]] = None,
        unauthenticated_action: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param login: login block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#login FunctionAppFlexConsumption#login}
        :param active_directory_v2: active_directory_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#active_directory_v2 FunctionAppFlexConsumption#active_directory_v2}
        :param apple_v2: apple_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#apple_v2 FunctionAppFlexConsumption#apple_v2}
        :param auth_enabled: Should the AuthV2 Settings be enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#auth_enabled FunctionAppFlexConsumption#auth_enabled}
        :param azure_static_web_app_v2: azure_static_web_app_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#azure_static_web_app_v2 FunctionAppFlexConsumption#azure_static_web_app_v2}
        :param config_file_path: The path to the App Auth settings. **Note:** Relative Paths are evaluated from the Site Root directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#config_file_path FunctionAppFlexConsumption#config_file_path}
        :param custom_oidc_v2: custom_oidc_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#custom_oidc_v2 FunctionAppFlexConsumption#custom_oidc_v2}
        :param default_provider: The Default Authentication Provider to use when the ``unauthenticated_action`` is set to ``RedirectToLoginPage``. Possible values include: ``apple``, ``azureactivedirectory``, ``facebook``, ``github``, ``google``, ``twitter`` and the ``name`` of your ``custom_oidc_v2`` provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#default_provider FunctionAppFlexConsumption#default_provider}
        :param excluded_paths: The paths which should be excluded from the ``unauthenticated_action`` when it is set to ``RedirectToLoginPage``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#excluded_paths FunctionAppFlexConsumption#excluded_paths}
        :param facebook_v2: facebook_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#facebook_v2 FunctionAppFlexConsumption#facebook_v2}
        :param forward_proxy_convention: The convention used to determine the url of the request made. Possible values include ``ForwardProxyConventionNoProxy``, ``ForwardProxyConventionStandard``, ``ForwardProxyConventionCustom``. Defaults to ``ForwardProxyConventionNoProxy`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#forward_proxy_convention FunctionAppFlexConsumption#forward_proxy_convention}
        :param forward_proxy_custom_host_header_name: The name of the header containing the host of the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#forward_proxy_custom_host_header_name FunctionAppFlexConsumption#forward_proxy_custom_host_header_name}
        :param forward_proxy_custom_scheme_header_name: The name of the header containing the scheme of the request. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#forward_proxy_custom_scheme_header_name FunctionAppFlexConsumption#forward_proxy_custom_scheme_header_name}
        :param github_v2: github_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#github_v2 FunctionAppFlexConsumption#github_v2}
        :param google_v2: google_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#google_v2 FunctionAppFlexConsumption#google_v2}
        :param http_route_api_prefix: The prefix that should precede all the authentication and authorisation paths. Defaults to ``/.auth``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#http_route_api_prefix FunctionAppFlexConsumption#http_route_api_prefix}
        :param microsoft_v2: microsoft_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#microsoft_v2 FunctionAppFlexConsumption#microsoft_v2}
        :param require_authentication: Should the authentication flow be used for all requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#require_authentication FunctionAppFlexConsumption#require_authentication}
        :param require_https: Should HTTPS be required on connections? Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#require_https FunctionAppFlexConsumption#require_https}
        :param runtime_version: The Runtime Version of the Authentication and Authorisation feature of this App. Defaults to ``~1``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#runtime_version FunctionAppFlexConsumption#runtime_version}
        :param twitter_v2: twitter_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#twitter_v2 FunctionAppFlexConsumption#twitter_v2}
        :param unauthenticated_action: The action to take for requests made without authentication. Possible values include ``RedirectToLoginPage``, ``AllowAnonymous``, ``Return401``, and ``Return403``. Defaults to ``RedirectToLoginPage``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#unauthenticated_action FunctionAppFlexConsumption#unauthenticated_action}
        '''
        if isinstance(login, dict):
            login = FunctionAppFlexConsumptionAuthSettingsV2Login(**login)
        if isinstance(active_directory_v2, dict):
            active_directory_v2 = FunctionAppFlexConsumptionAuthSettingsV2ActiveDirectoryV2(**active_directory_v2)
        if isinstance(apple_v2, dict):
            apple_v2 = FunctionAppFlexConsumptionAuthSettingsV2AppleV2(**apple_v2)
        if isinstance(azure_static_web_app_v2, dict):
            azure_static_web_app_v2 = FunctionAppFlexConsumptionAuthSettingsV2AzureStaticWebAppV2(**azure_static_web_app_v2)
        if isinstance(facebook_v2, dict):
            facebook_v2 = FunctionAppFlexConsumptionAuthSettingsV2FacebookV2(**facebook_v2)
        if isinstance(github_v2, dict):
            github_v2 = FunctionAppFlexConsumptionAuthSettingsV2GithubV2(**github_v2)
        if isinstance(google_v2, dict):
            google_v2 = FunctionAppFlexConsumptionAuthSettingsV2GoogleV2(**google_v2)
        if isinstance(microsoft_v2, dict):
            microsoft_v2 = FunctionAppFlexConsumptionAuthSettingsV2MicrosoftV2(**microsoft_v2)
        if isinstance(twitter_v2, dict):
            twitter_v2 = FunctionAppFlexConsumptionAuthSettingsV2TwitterV2(**twitter_v2)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d10ea96e07ddcf30e799b401ca2fd3cfd1045b0c9efb6bf4e9c77121dde39ef6)
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
    def login(self) -> "FunctionAppFlexConsumptionAuthSettingsV2Login":
        '''login block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#login FunctionAppFlexConsumption#login}
        '''
        result = self._values.get("login")
        assert result is not None, "Required property 'login' is missing"
        return typing.cast("FunctionAppFlexConsumptionAuthSettingsV2Login", result)

    @builtins.property
    def active_directory_v2(
        self,
    ) -> typing.Optional["FunctionAppFlexConsumptionAuthSettingsV2ActiveDirectoryV2"]:
        '''active_directory_v2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#active_directory_v2 FunctionAppFlexConsumption#active_directory_v2}
        '''
        result = self._values.get("active_directory_v2")
        return typing.cast(typing.Optional["FunctionAppFlexConsumptionAuthSettingsV2ActiveDirectoryV2"], result)

    @builtins.property
    def apple_v2(
        self,
    ) -> typing.Optional["FunctionAppFlexConsumptionAuthSettingsV2AppleV2"]:
        '''apple_v2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#apple_v2 FunctionAppFlexConsumption#apple_v2}
        '''
        result = self._values.get("apple_v2")
        return typing.cast(typing.Optional["FunctionAppFlexConsumptionAuthSettingsV2AppleV2"], result)

    @builtins.property
    def auth_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the AuthV2 Settings be enabled. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#auth_enabled FunctionAppFlexConsumption#auth_enabled}
        '''
        result = self._values.get("auth_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def azure_static_web_app_v2(
        self,
    ) -> typing.Optional["FunctionAppFlexConsumptionAuthSettingsV2AzureStaticWebAppV2"]:
        '''azure_static_web_app_v2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#azure_static_web_app_v2 FunctionAppFlexConsumption#azure_static_web_app_v2}
        '''
        result = self._values.get("azure_static_web_app_v2")
        return typing.cast(typing.Optional["FunctionAppFlexConsumptionAuthSettingsV2AzureStaticWebAppV2"], result)

    @builtins.property
    def config_file_path(self) -> typing.Optional[builtins.str]:
        '''The path to the App Auth settings. **Note:** Relative Paths are evaluated from the Site Root directory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#config_file_path FunctionAppFlexConsumption#config_file_path}
        '''
        result = self._values.get("config_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_oidc_v2(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionAppFlexConsumptionAuthSettingsV2CustomOidcV2"]]]:
        '''custom_oidc_v2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#custom_oidc_v2 FunctionAppFlexConsumption#custom_oidc_v2}
        '''
        result = self._values.get("custom_oidc_v2")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionAppFlexConsumptionAuthSettingsV2CustomOidcV2"]]], result)

    @builtins.property
    def default_provider(self) -> typing.Optional[builtins.str]:
        '''The Default Authentication Provider to use when the ``unauthenticated_action`` is set to ``RedirectToLoginPage``.

        Possible values include: ``apple``, ``azureactivedirectory``, ``facebook``, ``github``, ``google``, ``twitter`` and the ``name`` of your ``custom_oidc_v2`` provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#default_provider FunctionAppFlexConsumption#default_provider}
        '''
        result = self._values.get("default_provider")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def excluded_paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The paths which should be excluded from the ``unauthenticated_action`` when it is set to ``RedirectToLoginPage``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#excluded_paths FunctionAppFlexConsumption#excluded_paths}
        '''
        result = self._values.get("excluded_paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def facebook_v2(
        self,
    ) -> typing.Optional["FunctionAppFlexConsumptionAuthSettingsV2FacebookV2"]:
        '''facebook_v2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#facebook_v2 FunctionAppFlexConsumption#facebook_v2}
        '''
        result = self._values.get("facebook_v2")
        return typing.cast(typing.Optional["FunctionAppFlexConsumptionAuthSettingsV2FacebookV2"], result)

    @builtins.property
    def forward_proxy_convention(self) -> typing.Optional[builtins.str]:
        '''The convention used to determine the url of the request made.

        Possible values include ``ForwardProxyConventionNoProxy``, ``ForwardProxyConventionStandard``, ``ForwardProxyConventionCustom``. Defaults to ``ForwardProxyConventionNoProxy``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#forward_proxy_convention FunctionAppFlexConsumption#forward_proxy_convention}
        '''
        result = self._values.get("forward_proxy_convention")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def forward_proxy_custom_host_header_name(self) -> typing.Optional[builtins.str]:
        '''The name of the header containing the host of the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#forward_proxy_custom_host_header_name FunctionAppFlexConsumption#forward_proxy_custom_host_header_name}
        '''
        result = self._values.get("forward_proxy_custom_host_header_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def forward_proxy_custom_scheme_header_name(self) -> typing.Optional[builtins.str]:
        '''The name of the header containing the scheme of the request.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#forward_proxy_custom_scheme_header_name FunctionAppFlexConsumption#forward_proxy_custom_scheme_header_name}
        '''
        result = self._values.get("forward_proxy_custom_scheme_header_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def github_v2(
        self,
    ) -> typing.Optional["FunctionAppFlexConsumptionAuthSettingsV2GithubV2"]:
        '''github_v2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#github_v2 FunctionAppFlexConsumption#github_v2}
        '''
        result = self._values.get("github_v2")
        return typing.cast(typing.Optional["FunctionAppFlexConsumptionAuthSettingsV2GithubV2"], result)

    @builtins.property
    def google_v2(
        self,
    ) -> typing.Optional["FunctionAppFlexConsumptionAuthSettingsV2GoogleV2"]:
        '''google_v2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#google_v2 FunctionAppFlexConsumption#google_v2}
        '''
        result = self._values.get("google_v2")
        return typing.cast(typing.Optional["FunctionAppFlexConsumptionAuthSettingsV2GoogleV2"], result)

    @builtins.property
    def http_route_api_prefix(self) -> typing.Optional[builtins.str]:
        '''The prefix that should precede all the authentication and authorisation paths. Defaults to ``/.auth``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#http_route_api_prefix FunctionAppFlexConsumption#http_route_api_prefix}
        '''
        result = self._values.get("http_route_api_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def microsoft_v2(
        self,
    ) -> typing.Optional["FunctionAppFlexConsumptionAuthSettingsV2MicrosoftV2"]:
        '''microsoft_v2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#microsoft_v2 FunctionAppFlexConsumption#microsoft_v2}
        '''
        result = self._values.get("microsoft_v2")
        return typing.cast(typing.Optional["FunctionAppFlexConsumptionAuthSettingsV2MicrosoftV2"], result)

    @builtins.property
    def require_authentication(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the authentication flow be used for all requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#require_authentication FunctionAppFlexConsumption#require_authentication}
        '''
        result = self._values.get("require_authentication")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def require_https(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should HTTPS be required on connections? Defaults to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#require_https FunctionAppFlexConsumption#require_https}
        '''
        result = self._values.get("require_https")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def runtime_version(self) -> typing.Optional[builtins.str]:
        '''The Runtime Version of the Authentication and Authorisation feature of this App. Defaults to ``~1``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#runtime_version FunctionAppFlexConsumption#runtime_version}
        '''
        result = self._values.get("runtime_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def twitter_v2(
        self,
    ) -> typing.Optional["FunctionAppFlexConsumptionAuthSettingsV2TwitterV2"]:
        '''twitter_v2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#twitter_v2 FunctionAppFlexConsumption#twitter_v2}
        '''
        result = self._values.get("twitter_v2")
        return typing.cast(typing.Optional["FunctionAppFlexConsumptionAuthSettingsV2TwitterV2"], result)

    @builtins.property
    def unauthenticated_action(self) -> typing.Optional[builtins.str]:
        '''The action to take for requests made without authentication.

        Possible values include ``RedirectToLoginPage``, ``AllowAnonymous``, ``Return401``, and ``Return403``. Defaults to ``RedirectToLoginPage``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#unauthenticated_action FunctionAppFlexConsumption#unauthenticated_action}
        '''
        result = self._values.get("unauthenticated_action")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionAppFlexConsumptionAuthSettingsV2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsV2ActiveDirectoryV2",
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
class FunctionAppFlexConsumptionAuthSettingsV2ActiveDirectoryV2:
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
        :param client_id: The ID of the Client to use to authenticate with Azure Active Directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_id FunctionAppFlexConsumption#client_id}
        :param tenant_auth_endpoint: The Azure Tenant Endpoint for the Authenticating Tenant. e.g. ``https://login.microsoftonline.com/v2.0/{tenant-guid}/``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#tenant_auth_endpoint FunctionAppFlexConsumption#tenant_auth_endpoint}
        :param allowed_applications: The list of allowed Applications for the Default Authorisation Policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#allowed_applications FunctionAppFlexConsumption#allowed_applications}
        :param allowed_audiences: Specifies a list of Allowed audience values to consider when validating JWTs issued by Azure Active Directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#allowed_audiences FunctionAppFlexConsumption#allowed_audiences}
        :param allowed_groups: The list of allowed Group Names for the Default Authorisation Policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#allowed_groups FunctionAppFlexConsumption#allowed_groups}
        :param allowed_identities: The list of allowed Identities for the Default Authorisation Policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#allowed_identities FunctionAppFlexConsumption#allowed_identities}
        :param client_secret_certificate_thumbprint: The thumbprint of the certificate used for signing purposes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret_certificate_thumbprint FunctionAppFlexConsumption#client_secret_certificate_thumbprint}
        :param client_secret_setting_name: The App Setting name that contains the client secret of the Client. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret_setting_name FunctionAppFlexConsumption#client_secret_setting_name}
        :param jwt_allowed_client_applications: A list of Allowed Client Applications in the JWT Claim. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#jwt_allowed_client_applications FunctionAppFlexConsumption#jwt_allowed_client_applications}
        :param jwt_allowed_groups: A list of Allowed Groups in the JWT Claim. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#jwt_allowed_groups FunctionAppFlexConsumption#jwt_allowed_groups}
        :param login_parameters: A map of key-value pairs to send to the Authorisation Endpoint when a user logs in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#login_parameters FunctionAppFlexConsumption#login_parameters}
        :param www_authentication_disabled: Should the www-authenticate provider should be omitted from the request? Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#www_authentication_disabled FunctionAppFlexConsumption#www_authentication_disabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c826ee12ce712e999382c1dd8274134e138ba026af083581c82e4791b5584d54)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_id FunctionAppFlexConsumption#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tenant_auth_endpoint(self) -> builtins.str:
        '''The Azure Tenant Endpoint for the Authenticating Tenant. e.g. ``https://login.microsoftonline.com/v2.0/{tenant-guid}/``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#tenant_auth_endpoint FunctionAppFlexConsumption#tenant_auth_endpoint}
        '''
        result = self._values.get("tenant_auth_endpoint")
        assert result is not None, "Required property 'tenant_auth_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_applications(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of allowed Applications for the Default Authorisation Policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#allowed_applications FunctionAppFlexConsumption#allowed_applications}
        '''
        result = self._values.get("allowed_applications")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allowed_audiences(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of Allowed audience values to consider when validating JWTs issued by Azure Active Directory.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#allowed_audiences FunctionAppFlexConsumption#allowed_audiences}
        '''
        result = self._values.get("allowed_audiences")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allowed_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of allowed Group Names for the Default Authorisation Policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#allowed_groups FunctionAppFlexConsumption#allowed_groups}
        '''
        result = self._values.get("allowed_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def allowed_identities(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of allowed Identities for the Default Authorisation Policy.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#allowed_identities FunctionAppFlexConsumption#allowed_identities}
        '''
        result = self._values.get("allowed_identities")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def client_secret_certificate_thumbprint(self) -> typing.Optional[builtins.str]:
        '''The thumbprint of the certificate used for signing purposes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret_certificate_thumbprint FunctionAppFlexConsumption#client_secret_certificate_thumbprint}
        '''
        result = self._values.get("client_secret_certificate_thumbprint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret_setting_name(self) -> typing.Optional[builtins.str]:
        '''The App Setting name that contains the client secret of the Client.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret_setting_name FunctionAppFlexConsumption#client_secret_setting_name}
        '''
        result = self._values.get("client_secret_setting_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def jwt_allowed_client_applications(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Allowed Client Applications in the JWT Claim.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#jwt_allowed_client_applications FunctionAppFlexConsumption#jwt_allowed_client_applications}
        '''
        result = self._values.get("jwt_allowed_client_applications")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def jwt_allowed_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Allowed Groups in the JWT Claim.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#jwt_allowed_groups FunctionAppFlexConsumption#jwt_allowed_groups}
        '''
        result = self._values.get("jwt_allowed_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def login_parameters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of key-value pairs to send to the Authorisation Endpoint when a user logs in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#login_parameters FunctionAppFlexConsumption#login_parameters}
        '''
        result = self._values.get("login_parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def www_authentication_disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the www-authenticate provider should be omitted from the request? Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#www_authentication_disabled FunctionAppFlexConsumption#www_authentication_disabled}
        '''
        result = self._values.get("www_authentication_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionAppFlexConsumptionAuthSettingsV2ActiveDirectoryV2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionAppFlexConsumptionAuthSettingsV2ActiveDirectoryV2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsV2ActiveDirectoryV2OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__300d5a5df6a79790a34261ceab61a4b3c550adfd6ba83cfd163216739f88f478)
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
            type_hints = typing.get_type_hints(_typecheckingstub__04c23210f2593d7a077812ffa48d46d9b2ce0c5e8e5462ebe5c3ae8f43076609)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedApplications", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedAudiences")
    def allowed_audiences(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedAudiences"))

    @allowed_audiences.setter
    def allowed_audiences(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb872bcd22f515e7deef8f5b78fca67797ea83501906814209a1ba7baf71f09c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedAudiences", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedGroups")
    def allowed_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedGroups"))

    @allowed_groups.setter
    def allowed_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cb902f4664d37861d1814efc4d135d572ec752913fb348a3afdd59a58ea51ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedGroups", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="allowedIdentities")
    def allowed_identities(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "allowedIdentities"))

    @allowed_identities.setter
    def allowed_identities(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__979908c313cf24f737bcbbf79fa7d38461638c85e2141f0279127bbd81abaf66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedIdentities", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79a8534c638ff44970e1c7bf82b722d4677823d7bab53554418c2d1540277c7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecretCertificateThumbprint")
    def client_secret_certificate_thumbprint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecretCertificateThumbprint"))

    @client_secret_certificate_thumbprint.setter
    def client_secret_certificate_thumbprint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba8b797a2d172ed2d78c9f52ec5c8643a8ec62184ca561239609ad66bee4266f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecretCertificateThumbprint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingName")
    def client_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecretSettingName"))

    @client_secret_setting_name.setter
    def client_secret_setting_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__201005a874cfc6d471fc96ddae6963da3f8a3d52b189a93df71ead56a541ae56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecretSettingName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jwtAllowedClientApplications")
    def jwt_allowed_client_applications(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jwtAllowedClientApplications"))

    @jwt_allowed_client_applications.setter
    def jwt_allowed_client_applications(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e14fcf5dad259e5f96edd82c9af78bd1d07603c39a7c025a82cdea24e095069f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "jwtAllowedClientApplications", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="jwtAllowedGroups")
    def jwt_allowed_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "jwtAllowedGroups"))

    @jwt_allowed_groups.setter
    def jwt_allowed_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02e3bc735f9423fe80977b27be5cbb87cd65e94adecda0e26d5be7dda383ebf1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe89416a082ce4a51812ee64293675faad57ee137343fd36a6ec246c79070382)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginParameters", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tenantAuthEndpoint")
    def tenant_auth_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tenantAuthEndpoint"))

    @tenant_auth_endpoint.setter
    def tenant_auth_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3fbda52e7ca32ac4e15bb14e650bb179a6b2275618f90d6c3d2a180807e6487)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b5d07e647b6e672e5820b4a21c8bd3fdff1bc15ed279e31b5dc30d5d0fad0f2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wwwAuthenticationDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2ActiveDirectoryV2]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2ActiveDirectoryV2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2ActiveDirectoryV2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d5ddb1aaa7f29b07b3e237e8628767d6c6fa5621a91a532b23a907b44756e81)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsV2AppleV2",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "client_secret_setting_name": "clientSecretSettingName",
    },
)
class FunctionAppFlexConsumptionAuthSettingsV2AppleV2:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        client_secret_setting_name: builtins.str,
    ) -> None:
        '''
        :param client_id: The OpenID Connect Client ID for the Apple web application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_id FunctionAppFlexConsumption#client_id}
        :param client_secret_setting_name: The app setting name that contains the ``client_secret`` value used for Apple Login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret_setting_name FunctionAppFlexConsumption#client_secret_setting_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7ac3bea0836b88b805792ef6ba6d70f63eacdcb4741fbeed4271eb140b3566c)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_secret_setting_name", value=client_secret_setting_name, expected_type=type_hints["client_secret_setting_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
            "client_secret_setting_name": client_secret_setting_name,
        }

    @builtins.property
    def client_id(self) -> builtins.str:
        '''The OpenID Connect Client ID for the Apple web application.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_id FunctionAppFlexConsumption#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret_setting_name(self) -> builtins.str:
        '''The app setting name that contains the ``client_secret`` value used for Apple Login.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret_setting_name FunctionAppFlexConsumption#client_secret_setting_name}
        '''
        result = self._values.get("client_secret_setting_name")
        assert result is not None, "Required property 'client_secret_setting_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionAppFlexConsumptionAuthSettingsV2AppleV2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionAppFlexConsumptionAuthSettingsV2AppleV2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsV2AppleV2OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5fa7850dd1d87da9bad3651bad9c4e1d7bc844d84e237fa3ae7116cfe8e7a69c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3af721cdbf3b4a9af2676bf5292ea616f89091410446d3d6cf1a9bbf944627e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingName")
    def client_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecretSettingName"))

    @client_secret_setting_name.setter
    def client_secret_setting_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f68219009a0cdfb81e106fdc8513484ec4a9bbbbb6a6783bf3022529543cfdd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecretSettingName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2AppleV2]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2AppleV2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2AppleV2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d027f4ae24103f6c255ca75be1ac22c92678a4ae5e2c0dfa11015d120f6fad2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsV2AzureStaticWebAppV2",
    jsii_struct_bases=[],
    name_mapping={"client_id": "clientId"},
)
class FunctionAppFlexConsumptionAuthSettingsV2AzureStaticWebAppV2:
    def __init__(self, *, client_id: builtins.str) -> None:
        '''
        :param client_id: The ID of the Client to use to authenticate with Azure Static Web App Authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_id FunctionAppFlexConsumption#client_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__668c3cd99571cde538d3e11ec36734dd9e304386a0874b875364894493010983)
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "client_id": client_id,
        }

    @builtins.property
    def client_id(self) -> builtins.str:
        '''The ID of the Client to use to authenticate with Azure Static Web App Authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_id FunctionAppFlexConsumption#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionAppFlexConsumptionAuthSettingsV2AzureStaticWebAppV2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionAppFlexConsumptionAuthSettingsV2AzureStaticWebAppV2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsV2AzureStaticWebAppV2OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2db193d9dfd906f27d424c03c5de3f92c6cacbd85b896f5f97de65464524cf51)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ca903a9950c68484302618c7b63bd47c286b4972e393e501ba71f22772b3d4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2AzureStaticWebAppV2]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2AzureStaticWebAppV2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2AzureStaticWebAppV2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__257568059d2dc445f662669ca2aa5f7813b4684c88b288e0b805781cce292040)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsV2CustomOidcV2",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "name": "name",
        "openid_configuration_endpoint": "openidConfigurationEndpoint",
        "name_claim_type": "nameClaimType",
        "scopes": "scopes",
    },
)
class FunctionAppFlexConsumptionAuthSettingsV2CustomOidcV2:
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
        :param client_id: The ID of the Client to use to authenticate with this Custom OIDC. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_id FunctionAppFlexConsumption#client_id}
        :param name: The name of the Custom OIDC Authentication Provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#name FunctionAppFlexConsumption#name}
        :param openid_configuration_endpoint: The endpoint that contains all the configuration endpoints for this Custom OIDC provider. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#openid_configuration_endpoint FunctionAppFlexConsumption#openid_configuration_endpoint}
        :param name_claim_type: The name of the claim that contains the users name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#name_claim_type FunctionAppFlexConsumption#name_claim_type}
        :param scopes: The list of the scopes that should be requested while authenticating. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#scopes FunctionAppFlexConsumption#scopes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff5e9967f723ffaae30c4ebbd2ec9caf5dbccf98f95431b6b01a443d4ed86c4d)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_id FunctionAppFlexConsumption#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the Custom OIDC Authentication Provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#name FunctionAppFlexConsumption#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def openid_configuration_endpoint(self) -> builtins.str:
        '''The endpoint that contains all the configuration endpoints for this Custom OIDC provider.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#openid_configuration_endpoint FunctionAppFlexConsumption#openid_configuration_endpoint}
        '''
        result = self._values.get("openid_configuration_endpoint")
        assert result is not None, "Required property 'openid_configuration_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name_claim_type(self) -> typing.Optional[builtins.str]:
        '''The name of the claim that contains the users name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#name_claim_type FunctionAppFlexConsumption#name_claim_type}
        '''
        result = self._values.get("name_claim_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of the scopes that should be requested while authenticating.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#scopes FunctionAppFlexConsumption#scopes}
        '''
        result = self._values.get("scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionAppFlexConsumptionAuthSettingsV2CustomOidcV2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionAppFlexConsumptionAuthSettingsV2CustomOidcV2List(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsV2CustomOidcV2List",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e08a89fdca67dce8d931752c0a33125c2f08800823c8c6c4a3c669a96c279e18)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FunctionAppFlexConsumptionAuthSettingsV2CustomOidcV2OutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da1c0350ff5d5527a2a3f1a754f57ad4b7efe864d17f68362fd50db1e9d5d8e9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FunctionAppFlexConsumptionAuthSettingsV2CustomOidcV2OutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9443482c2b6dbffc37be5e75c4a63175576209b474bdf0ac311db7e90148e6c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a10c07d9fd93314aa45973e1c4569c15b791ccb1c660d2c337563352ee0bc898)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5a5eb50b8777ccc2897fc2d95eef9263536cd34df49f4cf4081eb3a759621fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionAuthSettingsV2CustomOidcV2]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionAuthSettingsV2CustomOidcV2]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionAuthSettingsV2CustomOidcV2]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20721f9eace5797762aa4ec2d8c09dd37deeac1625b5350899bc32f6845ef76c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FunctionAppFlexConsumptionAuthSettingsV2CustomOidcV2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsV2CustomOidcV2OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a87482d93961ab8a7f87d22b4c12ae51ae86ddb0b5f78558986f19ee76e02cbe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__755b9f1c003cdf56913dc9b1cd82cfa039c0f71e088fd1998406e97ca978ee60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e68dbdb3b76fbeb6368abc9275b0f55a6b7c27bcd2817272bdde938bef12915)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nameClaimType")
    def name_claim_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nameClaimType"))

    @name_claim_type.setter
    def name_claim_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ece868a521dd86c6b7876d15425cf6a700ce9b2a3c09806b6a8664d639c9246f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nameClaimType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="openidConfigurationEndpoint")
    def openid_configuration_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "openidConfigurationEndpoint"))

    @openid_configuration_endpoint.setter
    def openid_configuration_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__240634ab896353e5810011aaeacc18d7e6ecd8075ab925ee4a993ce70ccd7413)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "openidConfigurationEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scopes"))

    @scopes.setter
    def scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__785be99058a6fae38d52236f873309601082e744f128f459562f51fa45742029)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionAppFlexConsumptionAuthSettingsV2CustomOidcV2]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionAppFlexConsumptionAuthSettingsV2CustomOidcV2]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionAppFlexConsumptionAuthSettingsV2CustomOidcV2]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdf4bdf758f8ab441c634b4eafff9dca1833165e5ee17163986685eb5db75d3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsV2FacebookV2",
    jsii_struct_bases=[],
    name_mapping={
        "app_id": "appId",
        "app_secret_setting_name": "appSecretSettingName",
        "graph_api_version": "graphApiVersion",
        "login_scopes": "loginScopes",
    },
)
class FunctionAppFlexConsumptionAuthSettingsV2FacebookV2:
    def __init__(
        self,
        *,
        app_id: builtins.str,
        app_secret_setting_name: builtins.str,
        graph_api_version: typing.Optional[builtins.str] = None,
        login_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param app_id: The App ID of the Facebook app used for login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#app_id FunctionAppFlexConsumption#app_id}
        :param app_secret_setting_name: The app setting name that contains the ``app_secret`` value used for Facebook Login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#app_secret_setting_name FunctionAppFlexConsumption#app_secret_setting_name}
        :param graph_api_version: The version of the Facebook API to be used while logging in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#graph_api_version FunctionAppFlexConsumption#graph_api_version}
        :param login_scopes: Specifies a list of scopes to be requested as part of Facebook Login authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#login_scopes FunctionAppFlexConsumption#login_scopes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d16da4ea6bed4b4248197d312acfe2e1b8be3a6099b43e90d80bed5bfbeec3ad)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#app_id FunctionAppFlexConsumption#app_id}
        '''
        result = self._values.get("app_id")
        assert result is not None, "Required property 'app_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_secret_setting_name(self) -> builtins.str:
        '''The app setting name that contains the ``app_secret`` value used for Facebook Login.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#app_secret_setting_name FunctionAppFlexConsumption#app_secret_setting_name}
        '''
        result = self._values.get("app_secret_setting_name")
        assert result is not None, "Required property 'app_secret_setting_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def graph_api_version(self) -> typing.Optional[builtins.str]:
        '''The version of the Facebook API to be used while logging in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#graph_api_version FunctionAppFlexConsumption#graph_api_version}
        '''
        result = self._values.get("graph_api_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def login_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of scopes to be requested as part of Facebook Login authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#login_scopes FunctionAppFlexConsumption#login_scopes}
        '''
        result = self._values.get("login_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionAppFlexConsumptionAuthSettingsV2FacebookV2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionAppFlexConsumptionAuthSettingsV2FacebookV2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsV2FacebookV2OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a903db9c16055aea9286e22e00359c169a731ae93398f269522a8b999eaa639e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c1912b624298a14f66f1294f51e5a3d156f224d260d02ab9ee51016ecb071430)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appSecretSettingName")
    def app_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appSecretSettingName"))

    @app_secret_setting_name.setter
    def app_secret_setting_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__921ca098c26fdc4866660980ebf992db277a10e74cd1f9673eb6b02efe1aeec2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appSecretSettingName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="graphApiVersion")
    def graph_api_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "graphApiVersion"))

    @graph_api_version.setter
    def graph_api_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b5b0c56aa409d003cb5460da84a9e8ea018da30c669c5314062cccce3f944d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "graphApiVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loginScopes")
    def login_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "loginScopes"))

    @login_scopes.setter
    def login_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__398c45e06d49ec3c0413acb4f942b769b04548b649746d0ff2db002ffde25396)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginScopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2FacebookV2]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2FacebookV2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2FacebookV2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a39dd7d29655e118b857a1f989fcf161a28be0db8e2665e8de4915a592a7ba51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsV2GithubV2",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "client_secret_setting_name": "clientSecretSettingName",
        "login_scopes": "loginScopes",
    },
)
class FunctionAppFlexConsumptionAuthSettingsV2GithubV2:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        client_secret_setting_name: builtins.str,
        login_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param client_id: The ID of the GitHub app used for login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_id FunctionAppFlexConsumption#client_id}
        :param client_secret_setting_name: The app setting name that contains the ``client_secret`` value used for GitHub Login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret_setting_name FunctionAppFlexConsumption#client_secret_setting_name}
        :param login_scopes: Specifies a list of OAuth 2.0 scopes that will be requested as part of GitHub Login authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#login_scopes FunctionAppFlexConsumption#login_scopes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a25a58e0b6ac2f8cfdecc006790d5afbed1ceb57bc3bb20925b4fd79a16c9673)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_id FunctionAppFlexConsumption#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret_setting_name(self) -> builtins.str:
        '''The app setting name that contains the ``client_secret`` value used for GitHub Login.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret_setting_name FunctionAppFlexConsumption#client_secret_setting_name}
        '''
        result = self._values.get("client_secret_setting_name")
        assert result is not None, "Required property 'client_secret_setting_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def login_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of OAuth 2.0 scopes that will be requested as part of GitHub Login authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#login_scopes FunctionAppFlexConsumption#login_scopes}
        '''
        result = self._values.get("login_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionAppFlexConsumptionAuthSettingsV2GithubV2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionAppFlexConsumptionAuthSettingsV2GithubV2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsV2GithubV2OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb2b73585726a88a84602ec0bbed7700af474ed50676463088026231d7a1caeb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9daf1998f387fca1ac934b83101ffc0ff79c5550546e63b9a6abf3759af6f145)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingName")
    def client_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecretSettingName"))

    @client_secret_setting_name.setter
    def client_secret_setting_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a9d70f38570294405d4c3160f06c97363b3c82f54574c82ec33fbe26b828492)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecretSettingName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loginScopes")
    def login_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "loginScopes"))

    @login_scopes.setter
    def login_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7b2ce450b450ffe4be772e50fa226b1511b9332875d789c63b9394b4651881c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginScopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2GithubV2]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2GithubV2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2GithubV2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e073870ba5f1571c8bfc771ff4fbab69fb8caa4340fce6b7863cc54f447b661f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsV2GoogleV2",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "client_secret_setting_name": "clientSecretSettingName",
        "allowed_audiences": "allowedAudiences",
        "login_scopes": "loginScopes",
    },
)
class FunctionAppFlexConsumptionAuthSettingsV2GoogleV2:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        client_secret_setting_name: builtins.str,
        allowed_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
        login_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param client_id: The OpenID Connect Client ID for the Google web application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_id FunctionAppFlexConsumption#client_id}
        :param client_secret_setting_name: The app setting name that contains the ``client_secret`` value used for Google Login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret_setting_name FunctionAppFlexConsumption#client_secret_setting_name}
        :param allowed_audiences: Specifies a list of Allowed Audiences that will be requested as part of Google Sign-In authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#allowed_audiences FunctionAppFlexConsumption#allowed_audiences}
        :param login_scopes: Specifies a list of Login scopes that will be requested as part of Google Sign-In authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#login_scopes FunctionAppFlexConsumption#login_scopes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec25a76e6fe6cd742576ae625df87dd6db025ceb7a18f3423a32a67897fa5efd)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_id FunctionAppFlexConsumption#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret_setting_name(self) -> builtins.str:
        '''The app setting name that contains the ``client_secret`` value used for Google Login.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret_setting_name FunctionAppFlexConsumption#client_secret_setting_name}
        '''
        result = self._values.get("client_secret_setting_name")
        assert result is not None, "Required property 'client_secret_setting_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_audiences(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of Allowed Audiences that will be requested as part of Google Sign-In authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#allowed_audiences FunctionAppFlexConsumption#allowed_audiences}
        '''
        result = self._values.get("allowed_audiences")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def login_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of Login scopes that will be requested as part of Google Sign-In authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#login_scopes FunctionAppFlexConsumption#login_scopes}
        '''
        result = self._values.get("login_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionAppFlexConsumptionAuthSettingsV2GoogleV2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionAppFlexConsumptionAuthSettingsV2GoogleV2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsV2GoogleV2OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f151ace84960d61df4510b1b3839c053587b86b5b2b945009689aa54d3ee1f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__39a2244df931e58b227dd11ad238fc723d0e8350e1f927ce1106429fc1b8b292)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedAudiences", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abc946c0719433f1a1edb2d71282648b40ab54a7c9db6dbbc88d65e4f64f364b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingName")
    def client_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecretSettingName"))

    @client_secret_setting_name.setter
    def client_secret_setting_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1b58d725d6b9588cd9ed895a2ed8fb638d842b169968638e85a1fd8d1b78e8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecretSettingName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loginScopes")
    def login_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "loginScopes"))

    @login_scopes.setter
    def login_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78b5472a56e6234cd4e10d3d92125a9fb738d9e5b41f48fe9e10f93bbd7fc85a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginScopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2GoogleV2]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2GoogleV2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2GoogleV2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16e1287ed0248165d0e1923c02a611eb1930451c6981702c9361381da109ead8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsV2Login",
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
class FunctionAppFlexConsumptionAuthSettingsV2Login:
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
        :param allowed_external_redirect_urls: External URLs that can be redirected to as part of logging in or logging out of the app. This is an advanced setting typically only needed by Windows Store application backends. **Note:** URLs within the current domain are always implicitly allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#allowed_external_redirect_urls FunctionAppFlexConsumption#allowed_external_redirect_urls}
        :param cookie_expiration_convention: The method by which cookies expire. Possible values include: ``FixedTime``, and ``IdentityProviderDerived``. Defaults to ``FixedTime``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#cookie_expiration_convention FunctionAppFlexConsumption#cookie_expiration_convention}
        :param cookie_expiration_time: The time after the request is made when the session cookie should expire. Defaults to ``08:00:00``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#cookie_expiration_time FunctionAppFlexConsumption#cookie_expiration_time}
        :param logout_endpoint: The endpoint to which logout requests should be made. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#logout_endpoint FunctionAppFlexConsumption#logout_endpoint}
        :param nonce_expiration_time: The time after the request is made when the nonce should expire. Defaults to ``00:05:00``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#nonce_expiration_time FunctionAppFlexConsumption#nonce_expiration_time}
        :param preserve_url_fragments_for_logins: Should the fragments from the request be preserved after the login request is made. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#preserve_url_fragments_for_logins FunctionAppFlexConsumption#preserve_url_fragments_for_logins}
        :param token_refresh_extension_time: The number of hours after session token expiration that a session token can be used to call the token refresh API. Defaults to ``72`` hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#token_refresh_extension_time FunctionAppFlexConsumption#token_refresh_extension_time}
        :param token_store_enabled: Should the Token Store configuration Enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#token_store_enabled FunctionAppFlexConsumption#token_store_enabled}
        :param token_store_path: The directory path in the App Filesystem in which the tokens will be stored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#token_store_path FunctionAppFlexConsumption#token_store_path}
        :param token_store_sas_setting_name: The name of the app setting which contains the SAS URL of the blob storage containing the tokens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#token_store_sas_setting_name FunctionAppFlexConsumption#token_store_sas_setting_name}
        :param validate_nonce: Should the nonce be validated while completing the login flow. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#validate_nonce FunctionAppFlexConsumption#validate_nonce}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff5540f20938b5f316eae4f8834a2333116c441ab57aa3836d36e42b0a7cdbf8)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#allowed_external_redirect_urls FunctionAppFlexConsumption#allowed_external_redirect_urls}
        '''
        result = self._values.get("allowed_external_redirect_urls")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cookie_expiration_convention(self) -> typing.Optional[builtins.str]:
        '''The method by which cookies expire. Possible values include: ``FixedTime``, and ``IdentityProviderDerived``. Defaults to ``FixedTime``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#cookie_expiration_convention FunctionAppFlexConsumption#cookie_expiration_convention}
        '''
        result = self._values.get("cookie_expiration_convention")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cookie_expiration_time(self) -> typing.Optional[builtins.str]:
        '''The time after the request is made when the session cookie should expire. Defaults to ``08:00:00``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#cookie_expiration_time FunctionAppFlexConsumption#cookie_expiration_time}
        '''
        result = self._values.get("cookie_expiration_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logout_endpoint(self) -> typing.Optional[builtins.str]:
        '''The endpoint to which logout requests should be made.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#logout_endpoint FunctionAppFlexConsumption#logout_endpoint}
        '''
        result = self._values.get("logout_endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nonce_expiration_time(self) -> typing.Optional[builtins.str]:
        '''The time after the request is made when the nonce should expire. Defaults to ``00:05:00``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#nonce_expiration_time FunctionAppFlexConsumption#nonce_expiration_time}
        '''
        result = self._values.get("nonce_expiration_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preserve_url_fragments_for_logins(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the fragments from the request be preserved after the login request is made. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#preserve_url_fragments_for_logins FunctionAppFlexConsumption#preserve_url_fragments_for_logins}
        '''
        result = self._values.get("preserve_url_fragments_for_logins")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def token_refresh_extension_time(self) -> typing.Optional[jsii.Number]:
        '''The number of hours after session token expiration that a session token can be used to call the token refresh API.

        Defaults to ``72`` hours.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#token_refresh_extension_time FunctionAppFlexConsumption#token_refresh_extension_time}
        '''
        result = self._values.get("token_refresh_extension_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def token_store_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the Token Store configuration Enabled. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#token_store_enabled FunctionAppFlexConsumption#token_store_enabled}
        '''
        result = self._values.get("token_store_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def token_store_path(self) -> typing.Optional[builtins.str]:
        '''The directory path in the App Filesystem in which the tokens will be stored.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#token_store_path FunctionAppFlexConsumption#token_store_path}
        '''
        result = self._values.get("token_store_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def token_store_sas_setting_name(self) -> typing.Optional[builtins.str]:
        '''The name of the app setting which contains the SAS URL of the blob storage containing the tokens.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#token_store_sas_setting_name FunctionAppFlexConsumption#token_store_sas_setting_name}
        '''
        result = self._values.get("token_store_sas_setting_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def validate_nonce(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the nonce be validated while completing the login flow. Defaults to ``true``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#validate_nonce FunctionAppFlexConsumption#validate_nonce}
        '''
        result = self._values.get("validate_nonce")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionAppFlexConsumptionAuthSettingsV2Login(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionAppFlexConsumptionAuthSettingsV2LoginOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsV2LoginOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3f91aa6bf8b64401e8b1a2f422c8c72503691afebf96bf6664c934e478a9467)
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
            type_hints = typing.get_type_hints(_typecheckingstub__832314f8872d59fd3a82d0706af0beb83d4d77812afa37608fa405adb4f81199)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedExternalRedirectUrls", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cookieExpirationConvention")
    def cookie_expiration_convention(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cookieExpirationConvention"))

    @cookie_expiration_convention.setter
    def cookie_expiration_convention(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3a2bf6bc4d663084e2972701e320cb6fcb6571433132697557dd54b789b3a06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cookieExpirationConvention", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cookieExpirationTime")
    def cookie_expiration_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cookieExpirationTime"))

    @cookie_expiration_time.setter
    def cookie_expiration_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87e27d0aede4f83252147d05819ea7af23065881f6d14ea656f4e58d781e64e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cookieExpirationTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logoutEndpoint")
    def logout_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logoutEndpoint"))

    @logout_endpoint.setter
    def logout_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5adad561ff9cc2453294fed7f6f22a55a98865eff1969a70d965d99b3f81a49f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logoutEndpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="nonceExpirationTime")
    def nonce_expiration_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "nonceExpirationTime"))

    @nonce_expiration_time.setter
    def nonce_expiration_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68d3ef0294ad411e2f6409d6b9accea13b75987bac515bf7a4ae77f70004f97a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d49cfa31482abe5cfe6573a633fd158c57d67793f03d38337f5f991aa6a651aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preserveUrlFragmentsForLogins", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenRefreshExtensionTime")
    def token_refresh_extension_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "tokenRefreshExtensionTime"))

    @token_refresh_extension_time.setter
    def token_refresh_extension_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14728c9039fa2417a51c1f9b6a89c2fcaa0ed368383a46f92fe0966795458aac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fa8cd67375ef5677380671b991de61b8973d2e0020d6a35c56df58bfcfa5a78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenStoreEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenStorePath")
    def token_store_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenStorePath"))

    @token_store_path.setter
    def token_store_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3154fbd704fcfdb5409f617b1755ef83c62f2f0f195e651ac3e78244095a7fb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tokenStorePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tokenStoreSasSettingName")
    def token_store_sas_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tokenStoreSasSettingName"))

    @token_store_sas_setting_name.setter
    def token_store_sas_setting_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cec48676a4405bfb1a47351373c1e10eb02dd569f331ce1d5e94797f88a132ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fe36276213dfcc2c1d9d12fd322ce3154ec03cdaa429f931970b635e1a9c13f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validateNonce", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2Login]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2Login], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2Login],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08f673c6157b9d4dc944b8b3dd69709d3a5b83a3641b84f90ae6061a5af913bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsV2MicrosoftV2",
    jsii_struct_bases=[],
    name_mapping={
        "client_id": "clientId",
        "client_secret_setting_name": "clientSecretSettingName",
        "allowed_audiences": "allowedAudiences",
        "login_scopes": "loginScopes",
    },
)
class FunctionAppFlexConsumptionAuthSettingsV2MicrosoftV2:
    def __init__(
        self,
        *,
        client_id: builtins.str,
        client_secret_setting_name: builtins.str,
        allowed_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
        login_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param client_id: The OAuth 2.0 client ID that was created for the app used for authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_id FunctionAppFlexConsumption#client_id}
        :param client_secret_setting_name: The app setting name containing the OAuth 2.0 client secret that was created for the app used for authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret_setting_name FunctionAppFlexConsumption#client_secret_setting_name}
        :param allowed_audiences: Specifies a list of Allowed Audiences that will be requested as part of Microsoft Sign-In authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#allowed_audiences FunctionAppFlexConsumption#allowed_audiences}
        :param login_scopes: The list of Login scopes that will be requested as part of Microsoft Account authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#login_scopes FunctionAppFlexConsumption#login_scopes}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5984875dba9d9f68bffe29890c351a6a991d3be4c3497fad1e700e79f267a38)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_id FunctionAppFlexConsumption#client_id}
        '''
        result = self._values.get("client_id")
        assert result is not None, "Required property 'client_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_secret_setting_name(self) -> builtins.str:
        '''The app setting name containing the OAuth 2.0 client secret that was created for the app used for authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret_setting_name FunctionAppFlexConsumption#client_secret_setting_name}
        '''
        result = self._values.get("client_secret_setting_name")
        assert result is not None, "Required property 'client_secret_setting_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def allowed_audiences(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of Allowed Audiences that will be requested as part of Microsoft Sign-In authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#allowed_audiences FunctionAppFlexConsumption#allowed_audiences}
        '''
        result = self._values.get("allowed_audiences")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def login_scopes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of Login scopes that will be requested as part of Microsoft Account authentication.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#login_scopes FunctionAppFlexConsumption#login_scopes}
        '''
        result = self._values.get("login_scopes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionAppFlexConsumptionAuthSettingsV2MicrosoftV2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionAppFlexConsumptionAuthSettingsV2MicrosoftV2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsV2MicrosoftV2OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f292828ab598ef2675fc187061c2a1c4977aeae53288615bdf8111dabc32a66)
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
            type_hints = typing.get_type_hints(_typecheckingstub__46f317d491fd0ce3a2033644ee5b6e6bc3712b1b7f0c2e5ace7e7153ce006623)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allowedAudiences", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3410855493a46ef9087869c0ee961748f1be66517dc043d622a94c323d4ee879)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="clientSecretSettingName")
    def client_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecretSettingName"))

    @client_secret_setting_name.setter
    def client_secret_setting_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__691f0cba3ac700e59eba30f72d09279900d9dd8ac05c3d1cf95d328aa8d83136)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecretSettingName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loginScopes")
    def login_scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "loginScopes"))

    @login_scopes.setter
    def login_scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3874e74e0f6eb5a79e2d474d6b883a479a03cedfc54181d7fe88d321abc88446)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginScopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2MicrosoftV2]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2MicrosoftV2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2MicrosoftV2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f9393097a15bd45fc75769708b7deb71492cc4733e970b1e60896a610c76b48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FunctionAppFlexConsumptionAuthSettingsV2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsV2OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__39de1ae26d108e6961fbf30c657648a4afc309bf5d0366eb34a6ad1c38aac52f)
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
        :param client_id: The ID of the Client to use to authenticate with Azure Active Directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_id FunctionAppFlexConsumption#client_id}
        :param tenant_auth_endpoint: The Azure Tenant Endpoint for the Authenticating Tenant. e.g. ``https://login.microsoftonline.com/v2.0/{tenant-guid}/``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#tenant_auth_endpoint FunctionAppFlexConsumption#tenant_auth_endpoint}
        :param allowed_applications: The list of allowed Applications for the Default Authorisation Policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#allowed_applications FunctionAppFlexConsumption#allowed_applications}
        :param allowed_audiences: Specifies a list of Allowed audience values to consider when validating JWTs issued by Azure Active Directory. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#allowed_audiences FunctionAppFlexConsumption#allowed_audiences}
        :param allowed_groups: The list of allowed Group Names for the Default Authorisation Policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#allowed_groups FunctionAppFlexConsumption#allowed_groups}
        :param allowed_identities: The list of allowed Identities for the Default Authorisation Policy. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#allowed_identities FunctionAppFlexConsumption#allowed_identities}
        :param client_secret_certificate_thumbprint: The thumbprint of the certificate used for signing purposes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret_certificate_thumbprint FunctionAppFlexConsumption#client_secret_certificate_thumbprint}
        :param client_secret_setting_name: The App Setting name that contains the client secret of the Client. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret_setting_name FunctionAppFlexConsumption#client_secret_setting_name}
        :param jwt_allowed_client_applications: A list of Allowed Client Applications in the JWT Claim. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#jwt_allowed_client_applications FunctionAppFlexConsumption#jwt_allowed_client_applications}
        :param jwt_allowed_groups: A list of Allowed Groups in the JWT Claim. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#jwt_allowed_groups FunctionAppFlexConsumption#jwt_allowed_groups}
        :param login_parameters: A map of key-value pairs to send to the Authorisation Endpoint when a user logs in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#login_parameters FunctionAppFlexConsumption#login_parameters}
        :param www_authentication_disabled: Should the www-authenticate provider should be omitted from the request? Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#www_authentication_disabled FunctionAppFlexConsumption#www_authentication_disabled}
        '''
        value = FunctionAppFlexConsumptionAuthSettingsV2ActiveDirectoryV2(
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
        :param client_id: The OpenID Connect Client ID for the Apple web application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_id FunctionAppFlexConsumption#client_id}
        :param client_secret_setting_name: The app setting name that contains the ``client_secret`` value used for Apple Login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret_setting_name FunctionAppFlexConsumption#client_secret_setting_name}
        '''
        value = FunctionAppFlexConsumptionAuthSettingsV2AppleV2(
            client_id=client_id, client_secret_setting_name=client_secret_setting_name
        )

        return typing.cast(None, jsii.invoke(self, "putAppleV2", [value]))

    @jsii.member(jsii_name="putAzureStaticWebAppV2")
    def put_azure_static_web_app_v2(self, *, client_id: builtins.str) -> None:
        '''
        :param client_id: The ID of the Client to use to authenticate with Azure Static Web App Authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_id FunctionAppFlexConsumption#client_id}
        '''
        value = FunctionAppFlexConsumptionAuthSettingsV2AzureStaticWebAppV2(
            client_id=client_id
        )

        return typing.cast(None, jsii.invoke(self, "putAzureStaticWebAppV2", [value]))

    @jsii.member(jsii_name="putCustomOidcV2")
    def put_custom_oidc_v2(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionAppFlexConsumptionAuthSettingsV2CustomOidcV2, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bd0fd50ad9b2c4941e5b967885dc4a2ca03a6ddc848357f656b0474f60c936f)
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
        :param app_id: The App ID of the Facebook app used for login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#app_id FunctionAppFlexConsumption#app_id}
        :param app_secret_setting_name: The app setting name that contains the ``app_secret`` value used for Facebook Login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#app_secret_setting_name FunctionAppFlexConsumption#app_secret_setting_name}
        :param graph_api_version: The version of the Facebook API to be used while logging in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#graph_api_version FunctionAppFlexConsumption#graph_api_version}
        :param login_scopes: Specifies a list of scopes to be requested as part of Facebook Login authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#login_scopes FunctionAppFlexConsumption#login_scopes}
        '''
        value = FunctionAppFlexConsumptionAuthSettingsV2FacebookV2(
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
        :param client_id: The ID of the GitHub app used for login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_id FunctionAppFlexConsumption#client_id}
        :param client_secret_setting_name: The app setting name that contains the ``client_secret`` value used for GitHub Login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret_setting_name FunctionAppFlexConsumption#client_secret_setting_name}
        :param login_scopes: Specifies a list of OAuth 2.0 scopes that will be requested as part of GitHub Login authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#login_scopes FunctionAppFlexConsumption#login_scopes}
        '''
        value = FunctionAppFlexConsumptionAuthSettingsV2GithubV2(
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
        :param client_id: The OpenID Connect Client ID for the Google web application. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_id FunctionAppFlexConsumption#client_id}
        :param client_secret_setting_name: The app setting name that contains the ``client_secret`` value used for Google Login. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret_setting_name FunctionAppFlexConsumption#client_secret_setting_name}
        :param allowed_audiences: Specifies a list of Allowed Audiences that will be requested as part of Google Sign-In authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#allowed_audiences FunctionAppFlexConsumption#allowed_audiences}
        :param login_scopes: Specifies a list of Login scopes that will be requested as part of Google Sign-In authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#login_scopes FunctionAppFlexConsumption#login_scopes}
        '''
        value = FunctionAppFlexConsumptionAuthSettingsV2GoogleV2(
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
        :param allowed_external_redirect_urls: External URLs that can be redirected to as part of logging in or logging out of the app. This is an advanced setting typically only needed by Windows Store application backends. **Note:** URLs within the current domain are always implicitly allowed. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#allowed_external_redirect_urls FunctionAppFlexConsumption#allowed_external_redirect_urls}
        :param cookie_expiration_convention: The method by which cookies expire. Possible values include: ``FixedTime``, and ``IdentityProviderDerived``. Defaults to ``FixedTime``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#cookie_expiration_convention FunctionAppFlexConsumption#cookie_expiration_convention}
        :param cookie_expiration_time: The time after the request is made when the session cookie should expire. Defaults to ``08:00:00``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#cookie_expiration_time FunctionAppFlexConsumption#cookie_expiration_time}
        :param logout_endpoint: The endpoint to which logout requests should be made. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#logout_endpoint FunctionAppFlexConsumption#logout_endpoint}
        :param nonce_expiration_time: The time after the request is made when the nonce should expire. Defaults to ``00:05:00``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#nonce_expiration_time FunctionAppFlexConsumption#nonce_expiration_time}
        :param preserve_url_fragments_for_logins: Should the fragments from the request be preserved after the login request is made. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#preserve_url_fragments_for_logins FunctionAppFlexConsumption#preserve_url_fragments_for_logins}
        :param token_refresh_extension_time: The number of hours after session token expiration that a session token can be used to call the token refresh API. Defaults to ``72`` hours. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#token_refresh_extension_time FunctionAppFlexConsumption#token_refresh_extension_time}
        :param token_store_enabled: Should the Token Store configuration Enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#token_store_enabled FunctionAppFlexConsumption#token_store_enabled}
        :param token_store_path: The directory path in the App Filesystem in which the tokens will be stored. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#token_store_path FunctionAppFlexConsumption#token_store_path}
        :param token_store_sas_setting_name: The name of the app setting which contains the SAS URL of the blob storage containing the tokens. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#token_store_sas_setting_name FunctionAppFlexConsumption#token_store_sas_setting_name}
        :param validate_nonce: Should the nonce be validated while completing the login flow. Defaults to ``true``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#validate_nonce FunctionAppFlexConsumption#validate_nonce}
        '''
        value = FunctionAppFlexConsumptionAuthSettingsV2Login(
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
        :param client_id: The OAuth 2.0 client ID that was created for the app used for authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_id FunctionAppFlexConsumption#client_id}
        :param client_secret_setting_name: The app setting name containing the OAuth 2.0 client secret that was created for the app used for authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_secret_setting_name FunctionAppFlexConsumption#client_secret_setting_name}
        :param allowed_audiences: Specifies a list of Allowed Audiences that will be requested as part of Microsoft Sign-In authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#allowed_audiences FunctionAppFlexConsumption#allowed_audiences}
        :param login_scopes: The list of Login scopes that will be requested as part of Microsoft Account authentication. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#login_scopes FunctionAppFlexConsumption#login_scopes}
        '''
        value = FunctionAppFlexConsumptionAuthSettingsV2MicrosoftV2(
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
        :param consumer_key: The OAuth 1.0a consumer key of the Twitter application used for sign-in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#consumer_key FunctionAppFlexConsumption#consumer_key}
        :param consumer_secret_setting_name: The app setting name that contains the OAuth 1.0a consumer secret of the Twitter application used for sign-in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#consumer_secret_setting_name FunctionAppFlexConsumption#consumer_secret_setting_name}
        '''
        value = FunctionAppFlexConsumptionAuthSettingsV2TwitterV2(
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
    ) -> FunctionAppFlexConsumptionAuthSettingsV2ActiveDirectoryV2OutputReference:
        return typing.cast(FunctionAppFlexConsumptionAuthSettingsV2ActiveDirectoryV2OutputReference, jsii.get(self, "activeDirectoryV2"))

    @builtins.property
    @jsii.member(jsii_name="appleV2")
    def apple_v2(
        self,
    ) -> FunctionAppFlexConsumptionAuthSettingsV2AppleV2OutputReference:
        return typing.cast(FunctionAppFlexConsumptionAuthSettingsV2AppleV2OutputReference, jsii.get(self, "appleV2"))

    @builtins.property
    @jsii.member(jsii_name="azureStaticWebAppV2")
    def azure_static_web_app_v2(
        self,
    ) -> FunctionAppFlexConsumptionAuthSettingsV2AzureStaticWebAppV2OutputReference:
        return typing.cast(FunctionAppFlexConsumptionAuthSettingsV2AzureStaticWebAppV2OutputReference, jsii.get(self, "azureStaticWebAppV2"))

    @builtins.property
    @jsii.member(jsii_name="customOidcV2")
    def custom_oidc_v2(
        self,
    ) -> FunctionAppFlexConsumptionAuthSettingsV2CustomOidcV2List:
        return typing.cast(FunctionAppFlexConsumptionAuthSettingsV2CustomOidcV2List, jsii.get(self, "customOidcV2"))

    @builtins.property
    @jsii.member(jsii_name="facebookV2")
    def facebook_v2(
        self,
    ) -> FunctionAppFlexConsumptionAuthSettingsV2FacebookV2OutputReference:
        return typing.cast(FunctionAppFlexConsumptionAuthSettingsV2FacebookV2OutputReference, jsii.get(self, "facebookV2"))

    @builtins.property
    @jsii.member(jsii_name="githubV2")
    def github_v2(
        self,
    ) -> FunctionAppFlexConsumptionAuthSettingsV2GithubV2OutputReference:
        return typing.cast(FunctionAppFlexConsumptionAuthSettingsV2GithubV2OutputReference, jsii.get(self, "githubV2"))

    @builtins.property
    @jsii.member(jsii_name="googleV2")
    def google_v2(
        self,
    ) -> FunctionAppFlexConsumptionAuthSettingsV2GoogleV2OutputReference:
        return typing.cast(FunctionAppFlexConsumptionAuthSettingsV2GoogleV2OutputReference, jsii.get(self, "googleV2"))

    @builtins.property
    @jsii.member(jsii_name="login")
    def login(self) -> FunctionAppFlexConsumptionAuthSettingsV2LoginOutputReference:
        return typing.cast(FunctionAppFlexConsumptionAuthSettingsV2LoginOutputReference, jsii.get(self, "login"))

    @builtins.property
    @jsii.member(jsii_name="microsoftV2")
    def microsoft_v2(
        self,
    ) -> FunctionAppFlexConsumptionAuthSettingsV2MicrosoftV2OutputReference:
        return typing.cast(FunctionAppFlexConsumptionAuthSettingsV2MicrosoftV2OutputReference, jsii.get(self, "microsoftV2"))

    @builtins.property
    @jsii.member(jsii_name="twitterV2")
    def twitter_v2(
        self,
    ) -> "FunctionAppFlexConsumptionAuthSettingsV2TwitterV2OutputReference":
        return typing.cast("FunctionAppFlexConsumptionAuthSettingsV2TwitterV2OutputReference", jsii.get(self, "twitterV2"))

    @builtins.property
    @jsii.member(jsii_name="activeDirectoryV2Input")
    def active_directory_v2_input(
        self,
    ) -> typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2ActiveDirectoryV2]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2ActiveDirectoryV2], jsii.get(self, "activeDirectoryV2Input"))

    @builtins.property
    @jsii.member(jsii_name="appleV2Input")
    def apple_v2_input(
        self,
    ) -> typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2AppleV2]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2AppleV2], jsii.get(self, "appleV2Input"))

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
    ) -> typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2AzureStaticWebAppV2]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2AzureStaticWebAppV2], jsii.get(self, "azureStaticWebAppV2Input"))

    @builtins.property
    @jsii.member(jsii_name="configFilePathInput")
    def config_file_path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "configFilePathInput"))

    @builtins.property
    @jsii.member(jsii_name="customOidcV2Input")
    def custom_oidc_v2_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionAuthSettingsV2CustomOidcV2]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionAuthSettingsV2CustomOidcV2]]], jsii.get(self, "customOidcV2Input"))

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
    ) -> typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2FacebookV2]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2FacebookV2], jsii.get(self, "facebookV2Input"))

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
    ) -> typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2GithubV2]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2GithubV2], jsii.get(self, "githubV2Input"))

    @builtins.property
    @jsii.member(jsii_name="googleV2Input")
    def google_v2_input(
        self,
    ) -> typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2GoogleV2]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2GoogleV2], jsii.get(self, "googleV2Input"))

    @builtins.property
    @jsii.member(jsii_name="httpRouteApiPrefixInput")
    def http_route_api_prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpRouteApiPrefixInput"))

    @builtins.property
    @jsii.member(jsii_name="loginInput")
    def login_input(
        self,
    ) -> typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2Login]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2Login], jsii.get(self, "loginInput"))

    @builtins.property
    @jsii.member(jsii_name="microsoftV2Input")
    def microsoft_v2_input(
        self,
    ) -> typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2MicrosoftV2]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2MicrosoftV2], jsii.get(self, "microsoftV2Input"))

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
    ) -> typing.Optional["FunctionAppFlexConsumptionAuthSettingsV2TwitterV2"]:
        return typing.cast(typing.Optional["FunctionAppFlexConsumptionAuthSettingsV2TwitterV2"], jsii.get(self, "twitterV2Input"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__a99d2196534586769b2d6790ae00c87788a6a1871124052134a93fb37271db31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="configFilePath")
    def config_file_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "configFilePath"))

    @config_file_path.setter
    def config_file_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebd924b3ebf3cb5796288ccd73047a0b9aa16047ce392d1f3693d2fedde607ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configFilePath", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultProvider")
    def default_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultProvider"))

    @default_provider.setter
    def default_provider(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba9b48b106474fe073f771537e80a80036076af17299346752e1cbc60d6e06ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultProvider", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="excludedPaths")
    def excluded_paths(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "excludedPaths"))

    @excluded_paths.setter
    def excluded_paths(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a01a6198ce3f80d77032c2c24bc430018de2723b61b7c911238536bf7c7883e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludedPaths", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forwardProxyConvention")
    def forward_proxy_convention(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forwardProxyConvention"))

    @forward_proxy_convention.setter
    def forward_proxy_convention(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00dc971a323661e01dc275c1eb7210228e79dbd592d9a21ac874397382a0bac7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardProxyConvention", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forwardProxyCustomHostHeaderName")
    def forward_proxy_custom_host_header_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forwardProxyCustomHostHeaderName"))

    @forward_proxy_custom_host_header_name.setter
    def forward_proxy_custom_host_header_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a5f3f71a0e1832b323d8bc0bb03af54ae87ee77ea2cb912837dad899b073d75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardProxyCustomHostHeaderName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="forwardProxyCustomSchemeHeaderName")
    def forward_proxy_custom_scheme_header_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "forwardProxyCustomSchemeHeaderName"))

    @forward_proxy_custom_scheme_header_name.setter
    def forward_proxy_custom_scheme_header_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9a2f308fe65f4771707237a4c8671bdeadaa26415c42a548f0bb8df113ceea0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "forwardProxyCustomSchemeHeaderName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="httpRouteApiPrefix")
    def http_route_api_prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpRouteApiPrefix"))

    @http_route_api_prefix.setter
    def http_route_api_prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cd193fb8a89e0ce5a1f585e43c3b55a3e90b81bbbcb2360eeb302603ab9b42b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c32b38ff6c36abc806a1144f756da17eb753d31d267d0b7926db36e1858ac4ca)
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
            type_hints = typing.get_type_hints(_typecheckingstub__26f22849e64164d85051cfd6e51c40469b457e615fbe65f582f804b2a6c24d48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "requireHttps", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runtimeVersion")
    def runtime_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runtimeVersion"))

    @runtime_version.setter
    def runtime_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80af725b931875b7e862a25932dd3499a5f5083a3a694d9fa4cf1d798a149b80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="unauthenticatedAction")
    def unauthenticated_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "unauthenticatedAction"))

    @unauthenticated_action.setter
    def unauthenticated_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9941923f3e30544995042bc295db061ae2f0c328bca971165091c83377fb4a8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "unauthenticatedAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__483cce78b83fa5902105c5e29a0c8be8c5d9e5cf0e394c4d77a530aa8a5acf15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsV2TwitterV2",
    jsii_struct_bases=[],
    name_mapping={
        "consumer_key": "consumerKey",
        "consumer_secret_setting_name": "consumerSecretSettingName",
    },
)
class FunctionAppFlexConsumptionAuthSettingsV2TwitterV2:
    def __init__(
        self,
        *,
        consumer_key: builtins.str,
        consumer_secret_setting_name: builtins.str,
    ) -> None:
        '''
        :param consumer_key: The OAuth 1.0a consumer key of the Twitter application used for sign-in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#consumer_key FunctionAppFlexConsumption#consumer_key}
        :param consumer_secret_setting_name: The app setting name that contains the OAuth 1.0a consumer secret of the Twitter application used for sign-in. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#consumer_secret_setting_name FunctionAppFlexConsumption#consumer_secret_setting_name}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78e27d0e425e4d555553aa198e3437ec863ebb76c3e25c19938396352d4b965a)
            check_type(argname="argument consumer_key", value=consumer_key, expected_type=type_hints["consumer_key"])
            check_type(argname="argument consumer_secret_setting_name", value=consumer_secret_setting_name, expected_type=type_hints["consumer_secret_setting_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "consumer_key": consumer_key,
            "consumer_secret_setting_name": consumer_secret_setting_name,
        }

    @builtins.property
    def consumer_key(self) -> builtins.str:
        '''The OAuth 1.0a consumer key of the Twitter application used for sign-in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#consumer_key FunctionAppFlexConsumption#consumer_key}
        '''
        result = self._values.get("consumer_key")
        assert result is not None, "Required property 'consumer_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def consumer_secret_setting_name(self) -> builtins.str:
        '''The app setting name that contains the OAuth 1.0a consumer secret of the Twitter application used for sign-in.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#consumer_secret_setting_name FunctionAppFlexConsumption#consumer_secret_setting_name}
        '''
        result = self._values.get("consumer_secret_setting_name")
        assert result is not None, "Required property 'consumer_secret_setting_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionAppFlexConsumptionAuthSettingsV2TwitterV2(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionAppFlexConsumptionAuthSettingsV2TwitterV2OutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionAuthSettingsV2TwitterV2OutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffc621e52d7e0cb10d5e37fd08c373e67239073e35ecebed267bfaa3737a2726)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0c16c92fc29212ae543fdd9228dac5cf0bdd0afdea1ea60e58e3d18b6068a1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="consumerSecretSettingName")
    def consumer_secret_setting_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "consumerSecretSettingName"))

    @consumer_secret_setting_name.setter
    def consumer_secret_setting_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5fbc4546fb279221a970e4499e6580c86582e3ec27f7fb48be7786a533d9bd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "consumerSecretSettingName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2TwitterV2]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2TwitterV2], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2TwitterV2],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2b55f6eed20705c7a0b4adba1875ce8d0dfbde64fb5fd252ee340c74e610f26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "runtime_name": "runtimeName",
        "runtime_version": "runtimeVersion",
        "service_plan_id": "servicePlanId",
        "site_config": "siteConfig",
        "storage_authentication_type": "storageAuthenticationType",
        "storage_container_endpoint": "storageContainerEndpoint",
        "storage_container_type": "storageContainerType",
        "always_ready": "alwaysReady",
        "app_settings": "appSettings",
        "auth_settings": "authSettings",
        "auth_settings_v2": "authSettingsV2",
        "client_certificate_enabled": "clientCertificateEnabled",
        "client_certificate_exclusion_paths": "clientCertificateExclusionPaths",
        "client_certificate_mode": "clientCertificateMode",
        "connection_string": "connectionString",
        "enabled": "enabled",
        "https_only": "httpsOnly",
        "id": "id",
        "identity": "identity",
        "instance_memory_in_mb": "instanceMemoryInMb",
        "maximum_instance_count": "maximumInstanceCount",
        "public_network_access_enabled": "publicNetworkAccessEnabled",
        "sticky_settings": "stickySettings",
        "storage_access_key": "storageAccessKey",
        "storage_user_assigned_identity_id": "storageUserAssignedIdentityId",
        "tags": "tags",
        "timeouts": "timeouts",
        "virtual_network_subnet_id": "virtualNetworkSubnetId",
        "webdeploy_publish_basic_authentication_enabled": "webdeployPublishBasicAuthenticationEnabled",
        "zip_deploy_file": "zipDeployFile",
    },
)
class FunctionAppFlexConsumptionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        runtime_name: builtins.str,
        runtime_version: builtins.str,
        service_plan_id: builtins.str,
        site_config: typing.Union["FunctionAppFlexConsumptionSiteConfig", typing.Dict[builtins.str, typing.Any]],
        storage_authentication_type: builtins.str,
        storage_container_endpoint: builtins.str,
        storage_container_type: builtins.str,
        always_ready: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionAppFlexConsumptionAlwaysReady, typing.Dict[builtins.str, typing.Any]]]]] = None,
        app_settings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        auth_settings: typing.Optional[typing.Union[FunctionAppFlexConsumptionAuthSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        auth_settings_v2: typing.Optional[typing.Union[FunctionAppFlexConsumptionAuthSettingsV2, typing.Dict[builtins.str, typing.Any]]] = None,
        client_certificate_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        client_certificate_exclusion_paths: typing.Optional[builtins.str] = None,
        client_certificate_mode: typing.Optional[builtins.str] = None,
        connection_string: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FunctionAppFlexConsumptionConnectionString", typing.Dict[builtins.str, typing.Any]]]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        https_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["FunctionAppFlexConsumptionIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        instance_memory_in_mb: typing.Optional[jsii.Number] = None,
        maximum_instance_count: typing.Optional[jsii.Number] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sticky_settings: typing.Optional[typing.Union["FunctionAppFlexConsumptionStickySettings", typing.Dict[builtins.str, typing.Any]]] = None,
        storage_access_key: typing.Optional[builtins.str] = None,
        storage_user_assigned_identity_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["FunctionAppFlexConsumptionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        virtual_network_subnet_id: typing.Optional[builtins.str] = None,
        webdeploy_publish_basic_authentication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        zip_deploy_file: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#location FunctionAppFlexConsumption#location}.
        :param name: Specifies the name of the Function App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#name FunctionAppFlexConsumption#name}
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#resource_group_name FunctionAppFlexConsumption#resource_group_name}.
        :param runtime_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#runtime_name FunctionAppFlexConsumption#runtime_name}.
        :param runtime_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#runtime_version FunctionAppFlexConsumption#runtime_version}.
        :param service_plan_id: The ID of the App Service Plan within which to create this Function App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#service_plan_id FunctionAppFlexConsumption#service_plan_id}
        :param site_config: site_config block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#site_config FunctionAppFlexConsumption#site_config}
        :param storage_authentication_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#storage_authentication_type FunctionAppFlexConsumption#storage_authentication_type}.
        :param storage_container_endpoint: The endpoint of the storage container where the function app's code is hosted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#storage_container_endpoint FunctionAppFlexConsumption#storage_container_endpoint}
        :param storage_container_type: The type of the storage container where the function app's code is hosted. Only ``blobContainer`` is supported currently. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#storage_container_type FunctionAppFlexConsumption#storage_container_type}
        :param always_ready: always_ready block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#always_ready FunctionAppFlexConsumption#always_ready}
        :param app_settings: A map of key-value pairs for `App Settings <https://docs.microsoft.com/en-us/azure/azure-functions/functions-app-settings>`_ and custom values. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#app_settings FunctionAppFlexConsumption#app_settings}
        :param auth_settings: auth_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#auth_settings FunctionAppFlexConsumption#auth_settings}
        :param auth_settings_v2: auth_settings_v2 block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#auth_settings_v2 FunctionAppFlexConsumption#auth_settings_v2}
        :param client_certificate_enabled: Should the function app use Client Certificates. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_certificate_enabled FunctionAppFlexConsumption#client_certificate_enabled}
        :param client_certificate_exclusion_paths: Paths to exclude when using client certificates, separated by ; Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_certificate_exclusion_paths FunctionAppFlexConsumption#client_certificate_exclusion_paths}
        :param client_certificate_mode: The mode of the Function App's client certificates requirement for incoming requests. Possible values are ``Required``, ``Optional``, and ``OptionalInteractiveUser`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_certificate_mode FunctionAppFlexConsumption#client_certificate_mode}
        :param connection_string: connection_string block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#connection_string FunctionAppFlexConsumption#connection_string}
        :param enabled: Is the Function App enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#enabled FunctionAppFlexConsumption#enabled}
        :param https_only: Can the Function App only be accessed via HTTPS? Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#https_only FunctionAppFlexConsumption#https_only}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#id FunctionAppFlexConsumption#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#identity FunctionAppFlexConsumption#identity}
        :param instance_memory_in_mb: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#instance_memory_in_mb FunctionAppFlexConsumption#instance_memory_in_mb}.
        :param maximum_instance_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#maximum_instance_count FunctionAppFlexConsumption#maximum_instance_count}.
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#public_network_access_enabled FunctionAppFlexConsumption#public_network_access_enabled}.
        :param sticky_settings: sticky_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#sticky_settings FunctionAppFlexConsumption#sticky_settings}
        :param storage_access_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#storage_access_key FunctionAppFlexConsumption#storage_access_key}.
        :param storage_user_assigned_identity_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#storage_user_assigned_identity_id FunctionAppFlexConsumption#storage_user_assigned_identity_id}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#tags FunctionAppFlexConsumption#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#timeouts FunctionAppFlexConsumption#timeouts}
        :param virtual_network_subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#virtual_network_subnet_id FunctionAppFlexConsumption#virtual_network_subnet_id}.
        :param webdeploy_publish_basic_authentication_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#webdeploy_publish_basic_authentication_enabled FunctionAppFlexConsumption#webdeploy_publish_basic_authentication_enabled}.
        :param zip_deploy_file: The local path and filename of the Zip packaged application to deploy to this Function App. **Note:** Using this value requires either ``WEBSITE_RUN_FROM_PACKAGE=1`` or ``SCM_DO_BUILD_DURING_DEPLOYMENT=true`` to be set on the App in ``app_settings``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#zip_deploy_file FunctionAppFlexConsumption#zip_deploy_file}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(site_config, dict):
            site_config = FunctionAppFlexConsumptionSiteConfig(**site_config)
        if isinstance(auth_settings, dict):
            auth_settings = FunctionAppFlexConsumptionAuthSettings(**auth_settings)
        if isinstance(auth_settings_v2, dict):
            auth_settings_v2 = FunctionAppFlexConsumptionAuthSettingsV2(**auth_settings_v2)
        if isinstance(identity, dict):
            identity = FunctionAppFlexConsumptionIdentity(**identity)
        if isinstance(sticky_settings, dict):
            sticky_settings = FunctionAppFlexConsumptionStickySettings(**sticky_settings)
        if isinstance(timeouts, dict):
            timeouts = FunctionAppFlexConsumptionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78260cdd889376ff3c639b042de0a356084932ff939e987769ed6b3a17eb80b1)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument runtime_name", value=runtime_name, expected_type=type_hints["runtime_name"])
            check_type(argname="argument runtime_version", value=runtime_version, expected_type=type_hints["runtime_version"])
            check_type(argname="argument service_plan_id", value=service_plan_id, expected_type=type_hints["service_plan_id"])
            check_type(argname="argument site_config", value=site_config, expected_type=type_hints["site_config"])
            check_type(argname="argument storage_authentication_type", value=storage_authentication_type, expected_type=type_hints["storage_authentication_type"])
            check_type(argname="argument storage_container_endpoint", value=storage_container_endpoint, expected_type=type_hints["storage_container_endpoint"])
            check_type(argname="argument storage_container_type", value=storage_container_type, expected_type=type_hints["storage_container_type"])
            check_type(argname="argument always_ready", value=always_ready, expected_type=type_hints["always_ready"])
            check_type(argname="argument app_settings", value=app_settings, expected_type=type_hints["app_settings"])
            check_type(argname="argument auth_settings", value=auth_settings, expected_type=type_hints["auth_settings"])
            check_type(argname="argument auth_settings_v2", value=auth_settings_v2, expected_type=type_hints["auth_settings_v2"])
            check_type(argname="argument client_certificate_enabled", value=client_certificate_enabled, expected_type=type_hints["client_certificate_enabled"])
            check_type(argname="argument client_certificate_exclusion_paths", value=client_certificate_exclusion_paths, expected_type=type_hints["client_certificate_exclusion_paths"])
            check_type(argname="argument client_certificate_mode", value=client_certificate_mode, expected_type=type_hints["client_certificate_mode"])
            check_type(argname="argument connection_string", value=connection_string, expected_type=type_hints["connection_string"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument https_only", value=https_only, expected_type=type_hints["https_only"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument instance_memory_in_mb", value=instance_memory_in_mb, expected_type=type_hints["instance_memory_in_mb"])
            check_type(argname="argument maximum_instance_count", value=maximum_instance_count, expected_type=type_hints["maximum_instance_count"])
            check_type(argname="argument public_network_access_enabled", value=public_network_access_enabled, expected_type=type_hints["public_network_access_enabled"])
            check_type(argname="argument sticky_settings", value=sticky_settings, expected_type=type_hints["sticky_settings"])
            check_type(argname="argument storage_access_key", value=storage_access_key, expected_type=type_hints["storage_access_key"])
            check_type(argname="argument storage_user_assigned_identity_id", value=storage_user_assigned_identity_id, expected_type=type_hints["storage_user_assigned_identity_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument virtual_network_subnet_id", value=virtual_network_subnet_id, expected_type=type_hints["virtual_network_subnet_id"])
            check_type(argname="argument webdeploy_publish_basic_authentication_enabled", value=webdeploy_publish_basic_authentication_enabled, expected_type=type_hints["webdeploy_publish_basic_authentication_enabled"])
            check_type(argname="argument zip_deploy_file", value=zip_deploy_file, expected_type=type_hints["zip_deploy_file"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
            "runtime_name": runtime_name,
            "runtime_version": runtime_version,
            "service_plan_id": service_plan_id,
            "site_config": site_config,
            "storage_authentication_type": storage_authentication_type,
            "storage_container_endpoint": storage_container_endpoint,
            "storage_container_type": storage_container_type,
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
        if always_ready is not None:
            self._values["always_ready"] = always_ready
        if app_settings is not None:
            self._values["app_settings"] = app_settings
        if auth_settings is not None:
            self._values["auth_settings"] = auth_settings
        if auth_settings_v2 is not None:
            self._values["auth_settings_v2"] = auth_settings_v2
        if client_certificate_enabled is not None:
            self._values["client_certificate_enabled"] = client_certificate_enabled
        if client_certificate_exclusion_paths is not None:
            self._values["client_certificate_exclusion_paths"] = client_certificate_exclusion_paths
        if client_certificate_mode is not None:
            self._values["client_certificate_mode"] = client_certificate_mode
        if connection_string is not None:
            self._values["connection_string"] = connection_string
        if enabled is not None:
            self._values["enabled"] = enabled
        if https_only is not None:
            self._values["https_only"] = https_only
        if id is not None:
            self._values["id"] = id
        if identity is not None:
            self._values["identity"] = identity
        if instance_memory_in_mb is not None:
            self._values["instance_memory_in_mb"] = instance_memory_in_mb
        if maximum_instance_count is not None:
            self._values["maximum_instance_count"] = maximum_instance_count
        if public_network_access_enabled is not None:
            self._values["public_network_access_enabled"] = public_network_access_enabled
        if sticky_settings is not None:
            self._values["sticky_settings"] = sticky_settings
        if storage_access_key is not None:
            self._values["storage_access_key"] = storage_access_key
        if storage_user_assigned_identity_id is not None:
            self._values["storage_user_assigned_identity_id"] = storage_user_assigned_identity_id
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if virtual_network_subnet_id is not None:
            self._values["virtual_network_subnet_id"] = virtual_network_subnet_id
        if webdeploy_publish_basic_authentication_enabled is not None:
            self._values["webdeploy_publish_basic_authentication_enabled"] = webdeploy_publish_basic_authentication_enabled
        if zip_deploy_file is not None:
            self._values["zip_deploy_file"] = zip_deploy_file

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
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#location FunctionAppFlexConsumption#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Specifies the name of the Function App.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#name FunctionAppFlexConsumption#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#resource_group_name FunctionAppFlexConsumption#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def runtime_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#runtime_name FunctionAppFlexConsumption#runtime_name}.'''
        result = self._values.get("runtime_name")
        assert result is not None, "Required property 'runtime_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def runtime_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#runtime_version FunctionAppFlexConsumption#runtime_version}.'''
        result = self._values.get("runtime_version")
        assert result is not None, "Required property 'runtime_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_plan_id(self) -> builtins.str:
        '''The ID of the App Service Plan within which to create this Function App.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#service_plan_id FunctionAppFlexConsumption#service_plan_id}
        '''
        result = self._values.get("service_plan_id")
        assert result is not None, "Required property 'service_plan_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def site_config(self) -> "FunctionAppFlexConsumptionSiteConfig":
        '''site_config block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#site_config FunctionAppFlexConsumption#site_config}
        '''
        result = self._values.get("site_config")
        assert result is not None, "Required property 'site_config' is missing"
        return typing.cast("FunctionAppFlexConsumptionSiteConfig", result)

    @builtins.property
    def storage_authentication_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#storage_authentication_type FunctionAppFlexConsumption#storage_authentication_type}.'''
        result = self._values.get("storage_authentication_type")
        assert result is not None, "Required property 'storage_authentication_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_container_endpoint(self) -> builtins.str:
        '''The endpoint of the storage container where the function app's code is hosted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#storage_container_endpoint FunctionAppFlexConsumption#storage_container_endpoint}
        '''
        result = self._values.get("storage_container_endpoint")
        assert result is not None, "Required property 'storage_container_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def storage_container_type(self) -> builtins.str:
        '''The type of the storage container where the function app's code is hosted. Only ``blobContainer`` is supported currently.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#storage_container_type FunctionAppFlexConsumption#storage_container_type}
        '''
        result = self._values.get("storage_container_type")
        assert result is not None, "Required property 'storage_container_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def always_ready(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionAlwaysReady]]]:
        '''always_ready block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#always_ready FunctionAppFlexConsumption#always_ready}
        '''
        result = self._values.get("always_ready")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionAlwaysReady]]], result)

    @builtins.property
    def app_settings(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of key-value pairs for `App Settings <https://docs.microsoft.com/en-us/azure/azure-functions/functions-app-settings>`_ and custom values.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#app_settings FunctionAppFlexConsumption#app_settings}
        '''
        result = self._values.get("app_settings")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def auth_settings(self) -> typing.Optional[FunctionAppFlexConsumptionAuthSettings]:
        '''auth_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#auth_settings FunctionAppFlexConsumption#auth_settings}
        '''
        result = self._values.get("auth_settings")
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionAuthSettings], result)

    @builtins.property
    def auth_settings_v2(
        self,
    ) -> typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2]:
        '''auth_settings_v2 block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#auth_settings_v2 FunctionAppFlexConsumption#auth_settings_v2}
        '''
        result = self._values.get("auth_settings_v2")
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2], result)

    @builtins.property
    def client_certificate_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the function app use Client Certificates.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_certificate_enabled FunctionAppFlexConsumption#client_certificate_enabled}
        '''
        result = self._values.get("client_certificate_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def client_certificate_exclusion_paths(self) -> typing.Optional[builtins.str]:
        '''Paths to exclude when using client certificates, separated by ;

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_certificate_exclusion_paths FunctionAppFlexConsumption#client_certificate_exclusion_paths}
        '''
        result = self._values.get("client_certificate_exclusion_paths")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_certificate_mode(self) -> typing.Optional[builtins.str]:
        '''The mode of the Function App's client certificates requirement for incoming requests.

        Possible values are ``Required``, ``Optional``, and ``OptionalInteractiveUser``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#client_certificate_mode FunctionAppFlexConsumption#client_certificate_mode}
        '''
        result = self._values.get("client_certificate_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connection_string(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionAppFlexConsumptionConnectionString"]]]:
        '''connection_string block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#connection_string FunctionAppFlexConsumption#connection_string}
        '''
        result = self._values.get("connection_string")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionAppFlexConsumptionConnectionString"]]], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Is the Function App enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#enabled FunctionAppFlexConsumption#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def https_only(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Can the Function App only be accessed via HTTPS?

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#https_only FunctionAppFlexConsumption#https_only}
        '''
        result = self._values.get("https_only")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#id FunctionAppFlexConsumption#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(self) -> typing.Optional["FunctionAppFlexConsumptionIdentity"]:
        '''identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#identity FunctionAppFlexConsumption#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional["FunctionAppFlexConsumptionIdentity"], result)

    @builtins.property
    def instance_memory_in_mb(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#instance_memory_in_mb FunctionAppFlexConsumption#instance_memory_in_mb}.'''
        result = self._values.get("instance_memory_in_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def maximum_instance_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#maximum_instance_count FunctionAppFlexConsumption#maximum_instance_count}.'''
        result = self._values.get("maximum_instance_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def public_network_access_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#public_network_access_enabled FunctionAppFlexConsumption#public_network_access_enabled}.'''
        result = self._values.get("public_network_access_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def sticky_settings(
        self,
    ) -> typing.Optional["FunctionAppFlexConsumptionStickySettings"]:
        '''sticky_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#sticky_settings FunctionAppFlexConsumption#sticky_settings}
        '''
        result = self._values.get("sticky_settings")
        return typing.cast(typing.Optional["FunctionAppFlexConsumptionStickySettings"], result)

    @builtins.property
    def storage_access_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#storage_access_key FunctionAppFlexConsumption#storage_access_key}.'''
        result = self._values.get("storage_access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_user_assigned_identity_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#storage_user_assigned_identity_id FunctionAppFlexConsumption#storage_user_assigned_identity_id}.'''
        result = self._values.get("storage_user_assigned_identity_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#tags FunctionAppFlexConsumption#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["FunctionAppFlexConsumptionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#timeouts FunctionAppFlexConsumption#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["FunctionAppFlexConsumptionTimeouts"], result)

    @builtins.property
    def virtual_network_subnet_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#virtual_network_subnet_id FunctionAppFlexConsumption#virtual_network_subnet_id}.'''
        result = self._values.get("virtual_network_subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def webdeploy_publish_basic_authentication_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#webdeploy_publish_basic_authentication_enabled FunctionAppFlexConsumption#webdeploy_publish_basic_authentication_enabled}.'''
        result = self._values.get("webdeploy_publish_basic_authentication_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def zip_deploy_file(self) -> typing.Optional[builtins.str]:
        '''The local path and filename of the Zip packaged application to deploy to this Function App.

        **Note:** Using this value requires either ``WEBSITE_RUN_FROM_PACKAGE=1`` or ``SCM_DO_BUILD_DURING_DEPLOYMENT=true`` to be set on the App in ``app_settings``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#zip_deploy_file FunctionAppFlexConsumption#zip_deploy_file}
        '''
        result = self._values.get("zip_deploy_file")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionAppFlexConsumptionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionConnectionString",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "type": "type", "value": "value"},
)
class FunctionAppFlexConsumptionConnectionString:
    def __init__(
        self,
        *,
        name: builtins.str,
        type: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param name: The name which should be used for this Connection. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#name FunctionAppFlexConsumption#name}
        :param type: Type of database. Possible values include: ``MySQL``, ``SQLServer``, ``SQLAzure``, ``Custom``, ``NotificationHub``, ``ServiceBus``, ``EventHub``, ``APIHub``, ``DocDb``, ``RedisCache``, and ``PostgreSQL``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#type FunctionAppFlexConsumption#type}
        :param value: The connection string value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#value FunctionAppFlexConsumption#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d00811589a6a329b77c5dc0cddc6de28e03c2bed3e769bb716afd51254a2c9f)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#name FunctionAppFlexConsumption#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Type of database. Possible values include: ``MySQL``, ``SQLServer``, ``SQLAzure``, ``Custom``, ``NotificationHub``, ``ServiceBus``, ``EventHub``, ``APIHub``, ``DocDb``, ``RedisCache``, and ``PostgreSQL``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#type FunctionAppFlexConsumption#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''The connection string value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#value FunctionAppFlexConsumption#value}
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionAppFlexConsumptionConnectionString(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionAppFlexConsumptionConnectionStringList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionConnectionStringList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f995ecb07cdd4e153f173751d2dc0999319473ebb1e86c425673109cb1f207bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FunctionAppFlexConsumptionConnectionStringOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cb95f2d03bd6f1c63d930c64b2c3e9510f60184cd361bf4856c399567e95c51)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FunctionAppFlexConsumptionConnectionStringOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__729bd5e27af5f243f035cf3749811804ddc1071e2cf4ee59b3e9f48595777214)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e293bacb12205fb8fe375766c7b65097c9178b598f2ed3afec15426635e373a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ce02a17cd8a65460eabff679512b408442dda65de7e87e00abcafb1caad027f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionConnectionString]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionConnectionString]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionConnectionString]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9df86762635cd19fc3af51bdf5d64652f9fa484b92cd87770433fdfaf82b4a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FunctionAppFlexConsumptionConnectionStringOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionConnectionStringOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__58bc5d57a3a3b4b6093a8196fee1883cedb0830de811ede58e7b523d3d2d3397)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2b3e836b00d2a984b2b3e04b14d5125cab31b34147b2cc4f6e03603ce7b1b9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06ba450da7d5e868965871dc1b370fe1d23b816c56206b3b1e751f9aa868216e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9461fe4461ae425a53fd88f0510be1a5d95d04514b28da0c9286c45d9b573bf8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionAppFlexConsumptionConnectionString]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionAppFlexConsumptionConnectionString]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionAppFlexConsumptionConnectionString]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9a935a5c19e3dbd5a65d4d94132aa0df1bb44c29d5cba90588fcb7ccf7ee7dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionIdentity",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "identity_ids": "identityIds"},
)
class FunctionAppFlexConsumptionIdentity:
    def __init__(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#type FunctionAppFlexConsumption#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#identity_ids FunctionAppFlexConsumption#identity_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c38c6d84f8c80719fa4e2c1884a601b1774f9d5daa430cec0263aff1ba3a860)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if identity_ids is not None:
            self._values["identity_ids"] = identity_ids

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#type FunctionAppFlexConsumption#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#identity_ids FunctionAppFlexConsumption#identity_ids}.'''
        result = self._values.get("identity_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionAppFlexConsumptionIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionAppFlexConsumptionIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2bb52185d0407f4dce849967d84b2e5c4a12b662b2996e2e9bef8bf23d55354)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b196f8230d049ea16fa5d815d8e67cca61f332c5540a00aa5798830854383eb6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae155272c4f7bc5691ddee50f5afc43bb718d64e61f640d151ad6378ea4610ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FunctionAppFlexConsumptionIdentity]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionAppFlexConsumptionIdentity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80e57b53096d19b17630cacb429f83836b1e5e96009325e70ff6f0e9c51f995a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionSiteConfig",
    jsii_struct_bases=[],
    name_mapping={
        "api_definition_url": "apiDefinitionUrl",
        "api_management_api_id": "apiManagementApiId",
        "app_command_line": "appCommandLine",
        "application_insights_connection_string": "applicationInsightsConnectionString",
        "application_insights_key": "applicationInsightsKey",
        "app_service_logs": "appServiceLogs",
        "container_registry_managed_identity_client_id": "containerRegistryManagedIdentityClientId",
        "container_registry_use_managed_identity": "containerRegistryUseManagedIdentity",
        "cors": "cors",
        "default_documents": "defaultDocuments",
        "elastic_instance_minimum": "elasticInstanceMinimum",
        "health_check_eviction_time_in_min": "healthCheckEvictionTimeInMin",
        "health_check_path": "healthCheckPath",
        "http2_enabled": "http2Enabled",
        "ip_restriction": "ipRestriction",
        "ip_restriction_default_action": "ipRestrictionDefaultAction",
        "load_balancing_mode": "loadBalancingMode",
        "managed_pipeline_mode": "managedPipelineMode",
        "minimum_tls_version": "minimumTlsVersion",
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
class FunctionAppFlexConsumptionSiteConfig:
    def __init__(
        self,
        *,
        api_definition_url: typing.Optional[builtins.str] = None,
        api_management_api_id: typing.Optional[builtins.str] = None,
        app_command_line: typing.Optional[builtins.str] = None,
        application_insights_connection_string: typing.Optional[builtins.str] = None,
        application_insights_key: typing.Optional[builtins.str] = None,
        app_service_logs: typing.Optional[typing.Union["FunctionAppFlexConsumptionSiteConfigAppServiceLogs", typing.Dict[builtins.str, typing.Any]]] = None,
        container_registry_managed_identity_client_id: typing.Optional[builtins.str] = None,
        container_registry_use_managed_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        cors: typing.Optional[typing.Union["FunctionAppFlexConsumptionSiteConfigCors", typing.Dict[builtins.str, typing.Any]]] = None,
        default_documents: typing.Optional[typing.Sequence[builtins.str]] = None,
        elastic_instance_minimum: typing.Optional[jsii.Number] = None,
        health_check_eviction_time_in_min: typing.Optional[jsii.Number] = None,
        health_check_path: typing.Optional[builtins.str] = None,
        http2_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ip_restriction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FunctionAppFlexConsumptionSiteConfigIpRestriction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ip_restriction_default_action: typing.Optional[builtins.str] = None,
        load_balancing_mode: typing.Optional[builtins.str] = None,
        managed_pipeline_mode: typing.Optional[builtins.str] = None,
        minimum_tls_version: typing.Optional[builtins.str] = None,
        remote_debugging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        remote_debugging_version: typing.Optional[builtins.str] = None,
        runtime_scale_monitoring_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        scm_ip_restriction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FunctionAppFlexConsumptionSiteConfigScmIpRestriction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        scm_ip_restriction_default_action: typing.Optional[builtins.str] = None,
        scm_minimum_tls_version: typing.Optional[builtins.str] = None,
        scm_use_main_ip_restriction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        use32_bit_worker: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vnet_route_all_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        websockets_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        worker_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param api_definition_url: The URL of the API definition that describes this Linux Function App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#api_definition_url FunctionAppFlexConsumption#api_definition_url}
        :param api_management_api_id: The ID of the API Management API for this Linux Function App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#api_management_api_id FunctionAppFlexConsumption#api_management_api_id}
        :param app_command_line: The program and any arguments used to launch this app via the command line. (Example ``node myapp.js``). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#app_command_line FunctionAppFlexConsumption#app_command_line}
        :param application_insights_connection_string: The Connection String for linking the Linux Function App to Application Insights. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#application_insights_connection_string FunctionAppFlexConsumption#application_insights_connection_string}
        :param application_insights_key: The Instrumentation Key for connecting the Linux Function App to Application Insights. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#application_insights_key FunctionAppFlexConsumption#application_insights_key}
        :param app_service_logs: app_service_logs block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#app_service_logs FunctionAppFlexConsumption#app_service_logs}
        :param container_registry_managed_identity_client_id: The Client ID of the Managed Service Identity to use for connections to the Azure Container Registry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#container_registry_managed_identity_client_id FunctionAppFlexConsumption#container_registry_managed_identity_client_id}
        :param container_registry_use_managed_identity: Should connections for Azure Container Registry use Managed Identity. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#container_registry_use_managed_identity FunctionAppFlexConsumption#container_registry_use_managed_identity}
        :param cors: cors block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#cors FunctionAppFlexConsumption#cors}
        :param default_documents: Specifies a list of Default Documents for the Linux Web App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#default_documents FunctionAppFlexConsumption#default_documents}
        :param elastic_instance_minimum: The number of minimum instances for this Linux Function App. Only affects apps on Elastic Premium plans. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#elastic_instance_minimum FunctionAppFlexConsumption#elastic_instance_minimum}
        :param health_check_eviction_time_in_min: The amount of time in minutes that a node is unhealthy before being removed from the load balancer. Possible values are between ``2`` and ``10``. Only valid in conjunction with ``health_check_path`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#health_check_eviction_time_in_min FunctionAppFlexConsumption#health_check_eviction_time_in_min}
        :param health_check_path: The path to be checked for this function app health. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#health_check_path FunctionAppFlexConsumption#health_check_path}
        :param http2_enabled: Specifies if the http2 protocol should be enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#http2_enabled FunctionAppFlexConsumption#http2_enabled}
        :param ip_restriction: ip_restriction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#ip_restriction FunctionAppFlexConsumption#ip_restriction}
        :param ip_restriction_default_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#ip_restriction_default_action FunctionAppFlexConsumption#ip_restriction_default_action}.
        :param load_balancing_mode: The Site load balancing mode. Possible values include: ``WeightedRoundRobin``, ``LeastRequests``, ``LeastResponseTime``, ``WeightedTotalTraffic``, ``RequestHash``, ``PerSiteRoundRobin``. Defaults to ``LeastRequests`` if omitted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#load_balancing_mode FunctionAppFlexConsumption#load_balancing_mode}
        :param managed_pipeline_mode: The Managed Pipeline mode. Possible values include: ``Integrated``, ``Classic``. Defaults to ``Integrated``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#managed_pipeline_mode FunctionAppFlexConsumption#managed_pipeline_mode}
        :param minimum_tls_version: The configures the minimum version of TLS required for SSL requests. Possible values include: ``1.0``, ``1.1``, and ``1.2``. Defaults to ``1.2``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#minimum_tls_version FunctionAppFlexConsumption#minimum_tls_version}
        :param remote_debugging_enabled: Should Remote Debugging be enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#remote_debugging_enabled FunctionAppFlexConsumption#remote_debugging_enabled}
        :param remote_debugging_version: The Remote Debugging Version. Possible values include ``VS2017``, ``VS2019``, and `VS2022``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#remote_debugging_version FunctionAppFlexConsumption#remote_debugging_version}
        :param runtime_scale_monitoring_enabled: Should Functions Runtime Scale Monitoring be enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#runtime_scale_monitoring_enabled FunctionAppFlexConsumption#runtime_scale_monitoring_enabled}
        :param scm_ip_restriction: scm_ip_restriction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#scm_ip_restriction FunctionAppFlexConsumption#scm_ip_restriction}
        :param scm_ip_restriction_default_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#scm_ip_restriction_default_action FunctionAppFlexConsumption#scm_ip_restriction_default_action}.
        :param scm_minimum_tls_version: Configures the minimum version of TLS required for SSL requests to the SCM site Possible values include: ``1.0``, ``1.1``, and ``1.2``. Defaults to ``1.2``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#scm_minimum_tls_version FunctionAppFlexConsumption#scm_minimum_tls_version}
        :param scm_use_main_ip_restriction: Should the Linux Function App ``ip_restriction`` configuration be used for the SCM also. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#scm_use_main_ip_restriction FunctionAppFlexConsumption#scm_use_main_ip_restriction}
        :param use32_bit_worker: Should the Linux Function App use a 32-bit worker. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#use_32_bit_worker FunctionAppFlexConsumption#use_32_bit_worker}
        :param vnet_route_all_enabled: Should the Linux Function App route all traffic through the virtual network. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#vnet_route_all_enabled FunctionAppFlexConsumption#vnet_route_all_enabled}
        :param websockets_enabled: Should Web Sockets be enabled. Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#websockets_enabled FunctionAppFlexConsumption#websockets_enabled}
        :param worker_count: The number of Workers for this Linux Function App. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#worker_count FunctionAppFlexConsumption#worker_count}
        '''
        if isinstance(app_service_logs, dict):
            app_service_logs = FunctionAppFlexConsumptionSiteConfigAppServiceLogs(**app_service_logs)
        if isinstance(cors, dict):
            cors = FunctionAppFlexConsumptionSiteConfigCors(**cors)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87f0d599c5ba9c6ff9fe7c67da02e6153da4a1b4f4557f64d2075ae9ef1eb56c)
            check_type(argname="argument api_definition_url", value=api_definition_url, expected_type=type_hints["api_definition_url"])
            check_type(argname="argument api_management_api_id", value=api_management_api_id, expected_type=type_hints["api_management_api_id"])
            check_type(argname="argument app_command_line", value=app_command_line, expected_type=type_hints["app_command_line"])
            check_type(argname="argument application_insights_connection_string", value=application_insights_connection_string, expected_type=type_hints["application_insights_connection_string"])
            check_type(argname="argument application_insights_key", value=application_insights_key, expected_type=type_hints["application_insights_key"])
            check_type(argname="argument app_service_logs", value=app_service_logs, expected_type=type_hints["app_service_logs"])
            check_type(argname="argument container_registry_managed_identity_client_id", value=container_registry_managed_identity_client_id, expected_type=type_hints["container_registry_managed_identity_client_id"])
            check_type(argname="argument container_registry_use_managed_identity", value=container_registry_use_managed_identity, expected_type=type_hints["container_registry_use_managed_identity"])
            check_type(argname="argument cors", value=cors, expected_type=type_hints["cors"])
            check_type(argname="argument default_documents", value=default_documents, expected_type=type_hints["default_documents"])
            check_type(argname="argument elastic_instance_minimum", value=elastic_instance_minimum, expected_type=type_hints["elastic_instance_minimum"])
            check_type(argname="argument health_check_eviction_time_in_min", value=health_check_eviction_time_in_min, expected_type=type_hints["health_check_eviction_time_in_min"])
            check_type(argname="argument health_check_path", value=health_check_path, expected_type=type_hints["health_check_path"])
            check_type(argname="argument http2_enabled", value=http2_enabled, expected_type=type_hints["http2_enabled"])
            check_type(argname="argument ip_restriction", value=ip_restriction, expected_type=type_hints["ip_restriction"])
            check_type(argname="argument ip_restriction_default_action", value=ip_restriction_default_action, expected_type=type_hints["ip_restriction_default_action"])
            check_type(argname="argument load_balancing_mode", value=load_balancing_mode, expected_type=type_hints["load_balancing_mode"])
            check_type(argname="argument managed_pipeline_mode", value=managed_pipeline_mode, expected_type=type_hints["managed_pipeline_mode"])
            check_type(argname="argument minimum_tls_version", value=minimum_tls_version, expected_type=type_hints["minimum_tls_version"])
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
        if app_service_logs is not None:
            self._values["app_service_logs"] = app_service_logs
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
    def api_definition_url(self) -> typing.Optional[builtins.str]:
        '''The URL of the API definition that describes this Linux Function App.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#api_definition_url FunctionAppFlexConsumption#api_definition_url}
        '''
        result = self._values.get("api_definition_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def api_management_api_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the API Management API for this Linux Function App.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#api_management_api_id FunctionAppFlexConsumption#api_management_api_id}
        '''
        result = self._values.get("api_management_api_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app_command_line(self) -> typing.Optional[builtins.str]:
        '''The program and any arguments used to launch this app via the command line. (Example ``node myapp.js``).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#app_command_line FunctionAppFlexConsumption#app_command_line}
        '''
        result = self._values.get("app_command_line")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_insights_connection_string(self) -> typing.Optional[builtins.str]:
        '''The Connection String for linking the Linux Function App to Application Insights.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#application_insights_connection_string FunctionAppFlexConsumption#application_insights_connection_string}
        '''
        result = self._values.get("application_insights_connection_string")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def application_insights_key(self) -> typing.Optional[builtins.str]:
        '''The Instrumentation Key for connecting the Linux Function App to Application Insights.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#application_insights_key FunctionAppFlexConsumption#application_insights_key}
        '''
        result = self._values.get("application_insights_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app_service_logs(
        self,
    ) -> typing.Optional["FunctionAppFlexConsumptionSiteConfigAppServiceLogs"]:
        '''app_service_logs block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#app_service_logs FunctionAppFlexConsumption#app_service_logs}
        '''
        result = self._values.get("app_service_logs")
        return typing.cast(typing.Optional["FunctionAppFlexConsumptionSiteConfigAppServiceLogs"], result)

    @builtins.property
    def container_registry_managed_identity_client_id(
        self,
    ) -> typing.Optional[builtins.str]:
        '''The Client ID of the Managed Service Identity to use for connections to the Azure Container Registry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#container_registry_managed_identity_client_id FunctionAppFlexConsumption#container_registry_managed_identity_client_id}
        '''
        result = self._values.get("container_registry_managed_identity_client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def container_registry_use_managed_identity(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should connections for Azure Container Registry use Managed Identity.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#container_registry_use_managed_identity FunctionAppFlexConsumption#container_registry_use_managed_identity}
        '''
        result = self._values.get("container_registry_use_managed_identity")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def cors(self) -> typing.Optional["FunctionAppFlexConsumptionSiteConfigCors"]:
        '''cors block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#cors FunctionAppFlexConsumption#cors}
        '''
        result = self._values.get("cors")
        return typing.cast(typing.Optional["FunctionAppFlexConsumptionSiteConfigCors"], result)

    @builtins.property
    def default_documents(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Specifies a list of Default Documents for the Linux Web App.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#default_documents FunctionAppFlexConsumption#default_documents}
        '''
        result = self._values.get("default_documents")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def elastic_instance_minimum(self) -> typing.Optional[jsii.Number]:
        '''The number of minimum instances for this Linux Function App. Only affects apps on Elastic Premium plans.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#elastic_instance_minimum FunctionAppFlexConsumption#elastic_instance_minimum}
        '''
        result = self._values.get("elastic_instance_minimum")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def health_check_eviction_time_in_min(self) -> typing.Optional[jsii.Number]:
        '''The amount of time in minutes that a node is unhealthy before being removed from the load balancer.

        Possible values are between ``2`` and ``10``. Only valid in conjunction with ``health_check_path``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#health_check_eviction_time_in_min FunctionAppFlexConsumption#health_check_eviction_time_in_min}
        '''
        result = self._values.get("health_check_eviction_time_in_min")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def health_check_path(self) -> typing.Optional[builtins.str]:
        '''The path to be checked for this function app health.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#health_check_path FunctionAppFlexConsumption#health_check_path}
        '''
        result = self._values.get("health_check_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def http2_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Specifies if the http2 protocol should be enabled. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#http2_enabled FunctionAppFlexConsumption#http2_enabled}
        '''
        result = self._values.get("http2_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ip_restriction(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionAppFlexConsumptionSiteConfigIpRestriction"]]]:
        '''ip_restriction block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#ip_restriction FunctionAppFlexConsumption#ip_restriction}
        '''
        result = self._values.get("ip_restriction")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionAppFlexConsumptionSiteConfigIpRestriction"]]], result)

    @builtins.property
    def ip_restriction_default_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#ip_restriction_default_action FunctionAppFlexConsumption#ip_restriction_default_action}.'''
        result = self._values.get("ip_restriction_default_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancing_mode(self) -> typing.Optional[builtins.str]:
        '''The Site load balancing mode. Possible values include: ``WeightedRoundRobin``, ``LeastRequests``, ``LeastResponseTime``, ``WeightedTotalTraffic``, ``RequestHash``, ``PerSiteRoundRobin``. Defaults to ``LeastRequests`` if omitted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#load_balancing_mode FunctionAppFlexConsumption#load_balancing_mode}
        '''
        result = self._values.get("load_balancing_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_pipeline_mode(self) -> typing.Optional[builtins.str]:
        '''The Managed Pipeline mode. Possible values include: ``Integrated``, ``Classic``. Defaults to ``Integrated``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#managed_pipeline_mode FunctionAppFlexConsumption#managed_pipeline_mode}
        '''
        result = self._values.get("managed_pipeline_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def minimum_tls_version(self) -> typing.Optional[builtins.str]:
        '''The configures the minimum version of TLS required for SSL requests.

        Possible values include: ``1.0``, ``1.1``, and  ``1.2``. Defaults to ``1.2``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#minimum_tls_version FunctionAppFlexConsumption#minimum_tls_version}
        '''
        result = self._values.get("minimum_tls_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def remote_debugging_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should Remote Debugging be enabled. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#remote_debugging_enabled FunctionAppFlexConsumption#remote_debugging_enabled}
        '''
        result = self._values.get("remote_debugging_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def remote_debugging_version(self) -> typing.Optional[builtins.str]:
        '''The Remote Debugging Version. Possible values include ``VS2017``, ``VS2019``, and `VS2022``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#remote_debugging_version FunctionAppFlexConsumption#remote_debugging_version}
        '''
        result = self._values.get("remote_debugging_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime_scale_monitoring_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should Functions Runtime Scale Monitoring be enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#runtime_scale_monitoring_enabled FunctionAppFlexConsumption#runtime_scale_monitoring_enabled}
        '''
        result = self._values.get("runtime_scale_monitoring_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def scm_ip_restriction(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionAppFlexConsumptionSiteConfigScmIpRestriction"]]]:
        '''scm_ip_restriction block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#scm_ip_restriction FunctionAppFlexConsumption#scm_ip_restriction}
        '''
        result = self._values.get("scm_ip_restriction")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionAppFlexConsumptionSiteConfigScmIpRestriction"]]], result)

    @builtins.property
    def scm_ip_restriction_default_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#scm_ip_restriction_default_action FunctionAppFlexConsumption#scm_ip_restriction_default_action}.'''
        result = self._values.get("scm_ip_restriction_default_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scm_minimum_tls_version(self) -> typing.Optional[builtins.str]:
        '''Configures the minimum version of TLS required for SSL requests to the SCM site Possible values include: ``1.0``, ``1.1``, and  ``1.2``. Defaults to ``1.2``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#scm_minimum_tls_version FunctionAppFlexConsumption#scm_minimum_tls_version}
        '''
        result = self._values.get("scm_minimum_tls_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scm_use_main_ip_restriction(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the Linux Function App ``ip_restriction`` configuration be used for the SCM also.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#scm_use_main_ip_restriction FunctionAppFlexConsumption#scm_use_main_ip_restriction}
        '''
        result = self._values.get("scm_use_main_ip_restriction")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def use32_bit_worker(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the Linux Function App use a 32-bit worker.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#use_32_bit_worker FunctionAppFlexConsumption#use_32_bit_worker}
        '''
        result = self._values.get("use32_bit_worker")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def vnet_route_all_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the Linux Function App route all traffic through the virtual network.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#vnet_route_all_enabled FunctionAppFlexConsumption#vnet_route_all_enabled}
        '''
        result = self._values.get("vnet_route_all_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def websockets_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should Web Sockets be enabled. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#websockets_enabled FunctionAppFlexConsumption#websockets_enabled}
        '''
        result = self._values.get("websockets_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def worker_count(self) -> typing.Optional[jsii.Number]:
        '''The number of Workers for this Linux Function App.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#worker_count FunctionAppFlexConsumption#worker_count}
        '''
        result = self._values.get("worker_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionAppFlexConsumptionSiteConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionSiteConfigAppServiceLogs",
    jsii_struct_bases=[],
    name_mapping={
        "disk_quota_mb": "diskQuotaMb",
        "retention_period_days": "retentionPeriodDays",
    },
)
class FunctionAppFlexConsumptionSiteConfigAppServiceLogs:
    def __init__(
        self,
        *,
        disk_quota_mb: typing.Optional[jsii.Number] = None,
        retention_period_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param disk_quota_mb: The amount of disk space to use for logs. Valid values are between ``25`` and ``100``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#disk_quota_mb FunctionAppFlexConsumption#disk_quota_mb}
        :param retention_period_days: The retention period for logs in days. Valid values are between ``0`` and ``99999``. Defaults to ``0`` (never delete). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#retention_period_days FunctionAppFlexConsumption#retention_period_days}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1b291dafcb6caacce4d4fc2a5dedd916fe8c31404ced4bbcdb106f9ba3851d3)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#disk_quota_mb FunctionAppFlexConsumption#disk_quota_mb}
        '''
        result = self._values.get("disk_quota_mb")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def retention_period_days(self) -> typing.Optional[jsii.Number]:
        '''The retention period for logs in days. Valid values are between ``0`` and ``99999``. Defaults to ``0`` (never delete).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#retention_period_days FunctionAppFlexConsumption#retention_period_days}
        '''
        result = self._values.get("retention_period_days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionAppFlexConsumptionSiteConfigAppServiceLogs(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionAppFlexConsumptionSiteConfigAppServiceLogsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionSiteConfigAppServiceLogsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af0d04f8553e02834f668597ddd64fb7705222dc28918bd92cbd4fddc3228e57)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a815a991b1f468e4080d848b11b97b5fda2d272321058c10cc84a222b5b74ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "diskQuotaMb", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="retentionPeriodDays")
    def retention_period_days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "retentionPeriodDays"))

    @retention_period_days.setter
    def retention_period_days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e36eaff4b2ab7898b91d78f63b53a9af04a0ff82923f1505399d97949faa6f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retentionPeriodDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FunctionAppFlexConsumptionSiteConfigAppServiceLogs]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionSiteConfigAppServiceLogs], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionAppFlexConsumptionSiteConfigAppServiceLogs],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66c4df363c2db8c73adc2c73eab811e54537cb0fd64615f3b79790b885209b3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionSiteConfigCors",
    jsii_struct_bases=[],
    name_mapping={
        "allowed_origins": "allowedOrigins",
        "support_credentials": "supportCredentials",
    },
)
class FunctionAppFlexConsumptionSiteConfigCors:
    def __init__(
        self,
        *,
        allowed_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
        support_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param allowed_origins: Specifies a list of origins that should be allowed to make cross-origin calls. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#allowed_origins FunctionAppFlexConsumption#allowed_origins}
        :param support_credentials: Are credentials allowed in CORS requests? Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#support_credentials FunctionAppFlexConsumption#support_credentials}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67d65cbb36cc86f8eb47dc6da3bb4c1b34a873ab66937f39813a4df2cee69554)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#allowed_origins FunctionAppFlexConsumption#allowed_origins}
        '''
        result = self._values.get("allowed_origins")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def support_credentials(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Are credentials allowed in CORS requests? Defaults to ``false``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#support_credentials FunctionAppFlexConsumption#support_credentials}
        '''
        result = self._values.get("support_credentials")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionAppFlexConsumptionSiteConfigCors(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionAppFlexConsumptionSiteConfigCorsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionSiteConfigCorsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c31bdc84bc11d87299761a699767e8053aa33a0906f29943e776acc6f8e7eeb6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__917aebede5de6d61cb050eec6f9f61d6819067df40f20775db16856e8123ac61)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4afea39c1f3ef9a86ceffe0f49d87e138c46e0a60b24ceadb20b863e3bf7a658)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "supportCredentials", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FunctionAppFlexConsumptionSiteConfigCors]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionSiteConfigCors], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionAppFlexConsumptionSiteConfigCors],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fb6ad7517fba4a9b0f1b2f1261e735892189d7f6e57142434df1011eb0ef46f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionSiteConfigIpRestriction",
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
class FunctionAppFlexConsumptionSiteConfigIpRestriction:
    def __init__(
        self,
        *,
        action: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FunctionAppFlexConsumptionSiteConfigIpRestrictionHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ip_address: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        service_tag: typing.Optional[builtins.str] = None,
        virtual_network_subnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action: The action to take. Possible values are ``Allow`` or ``Deny``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#action FunctionAppFlexConsumption#action}
        :param description: The description of the IP restriction rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#description FunctionAppFlexConsumption#description}
        :param headers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#headers FunctionAppFlexConsumption#headers}.
        :param ip_address: The CIDR notation of the IP or IP Range to match. For example: ``10.0.0.0/24`` or ``192.168.10.1/32`` or ``fe80::/64`` or ``13.107.6.152/31,13.107.128.0/22`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#ip_address FunctionAppFlexConsumption#ip_address}
        :param name: The name which should be used for this ``ip_restriction``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#name FunctionAppFlexConsumption#name}
        :param priority: The priority value of this ``ip_restriction``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#priority FunctionAppFlexConsumption#priority}
        :param service_tag: The Service Tag used for this IP Restriction. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#service_tag FunctionAppFlexConsumption#service_tag}
        :param virtual_network_subnet_id: The Virtual Network Subnet ID used for this IP Restriction. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#virtual_network_subnet_id FunctionAppFlexConsumption#virtual_network_subnet_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28c4176aef5f3ee89da611fe480ed39d783467f20aff0e4348a7fd56cda75cec)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#action FunctionAppFlexConsumption#action}
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the IP restriction rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#description FunctionAppFlexConsumption#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionAppFlexConsumptionSiteConfigIpRestrictionHeaders"]]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#headers FunctionAppFlexConsumption#headers}.'''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionAppFlexConsumptionSiteConfigIpRestrictionHeaders"]]], result)

    @builtins.property
    def ip_address(self) -> typing.Optional[builtins.str]:
        '''The CIDR notation of the IP or IP Range to match.

        For example: ``10.0.0.0/24`` or ``192.168.10.1/32`` or ``fe80::/64`` or ``13.107.6.152/31,13.107.128.0/22``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#ip_address FunctionAppFlexConsumption#ip_address}
        '''
        result = self._values.get("ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name which should be used for this ``ip_restriction``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#name FunctionAppFlexConsumption#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''The priority value of this ``ip_restriction``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#priority FunctionAppFlexConsumption#priority}
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service_tag(self) -> typing.Optional[builtins.str]:
        '''The Service Tag used for this IP Restriction.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#service_tag FunctionAppFlexConsumption#service_tag}
        '''
        result = self._values.get("service_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def virtual_network_subnet_id(self) -> typing.Optional[builtins.str]:
        '''The Virtual Network Subnet ID used for this IP Restriction.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#virtual_network_subnet_id FunctionAppFlexConsumption#virtual_network_subnet_id}
        '''
        result = self._values.get("virtual_network_subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionAppFlexConsumptionSiteConfigIpRestriction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionSiteConfigIpRestrictionHeaders",
    jsii_struct_bases=[],
    name_mapping={
        "x_azure_fdid": "xAzureFdid",
        "x_fd_health_probe": "xFdHealthProbe",
        "x_forwarded_for": "xForwardedFor",
        "x_forwarded_host": "xForwardedHost",
    },
)
class FunctionAppFlexConsumptionSiteConfigIpRestrictionHeaders:
    def __init__(
        self,
        *,
        x_azure_fdid: typing.Optional[typing.Sequence[builtins.str]] = None,
        x_fd_health_probe: typing.Optional[typing.Sequence[builtins.str]] = None,
        x_forwarded_for: typing.Optional[typing.Sequence[builtins.str]] = None,
        x_forwarded_host: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param x_azure_fdid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#x_azure_fdid FunctionAppFlexConsumption#x_azure_fdid}.
        :param x_fd_health_probe: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#x_fd_health_probe FunctionAppFlexConsumption#x_fd_health_probe}.
        :param x_forwarded_for: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#x_forwarded_for FunctionAppFlexConsumption#x_forwarded_for}.
        :param x_forwarded_host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#x_forwarded_host FunctionAppFlexConsumption#x_forwarded_host}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ea77a56a27dbc98c1072047570fc30bebd2c15dc1a112abcdf93e05a6bcbcb9)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#x_azure_fdid FunctionAppFlexConsumption#x_azure_fdid}.'''
        result = self._values.get("x_azure_fdid")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def x_fd_health_probe(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#x_fd_health_probe FunctionAppFlexConsumption#x_fd_health_probe}.'''
        result = self._values.get("x_fd_health_probe")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def x_forwarded_for(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#x_forwarded_for FunctionAppFlexConsumption#x_forwarded_for}.'''
        result = self._values.get("x_forwarded_for")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def x_forwarded_host(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#x_forwarded_host FunctionAppFlexConsumption#x_forwarded_host}.'''
        result = self._values.get("x_forwarded_host")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionAppFlexConsumptionSiteConfigIpRestrictionHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionAppFlexConsumptionSiteConfigIpRestrictionHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionSiteConfigIpRestrictionHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ea5e60d3c1c62a14fd42499c4b8c19de3b7f318f61469984b77c759195c3d407)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FunctionAppFlexConsumptionSiteConfigIpRestrictionHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f2470ca62cc4de284c0a1806b7636853da1d8ee89046dcee9039e304cf37f09)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FunctionAppFlexConsumptionSiteConfigIpRestrictionHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41f43556c68de36926ff10394fb9cc1597fc9a788fb9bad62fa070ecb903dbf4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a29cb8d1a0629dc2b99bae022b6c9bcd09aba10017d70363010b13f46550d12)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f397c3529cf7683f59d5d972bd809526b6d78dd7e0ab7c71e7189dd5e1862827)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionSiteConfigIpRestrictionHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionSiteConfigIpRestrictionHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionSiteConfigIpRestrictionHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b4d97e4345a346fc4783d0d0d139f171b886685eecef991e83d3ed15edec6cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FunctionAppFlexConsumptionSiteConfigIpRestrictionHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionSiteConfigIpRestrictionHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4c6752a057affccdf984aac218535153eec53349771f82663c22e854cf043d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab8980bb61e73043020f59b1b02bffac726a29e9d9c58afdc91c6f180ae57a3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "xAzureFdid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="xFdHealthProbe")
    def x_fd_health_probe(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "xFdHealthProbe"))

    @x_fd_health_probe.setter
    def x_fd_health_probe(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a0b1c61d58e0991b2016b24859759c8f2a2249fc97fa8ba4172226ae75f15f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "xFdHealthProbe", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="xForwardedFor")
    def x_forwarded_for(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "xForwardedFor"))

    @x_forwarded_for.setter
    def x_forwarded_for(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f947133e9ba50e52b96d5c7a7b703b000e0a68770a5609a0ee06ea2593291fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "xForwardedFor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="xForwardedHost")
    def x_forwarded_host(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "xForwardedHost"))

    @x_forwarded_host.setter
    def x_forwarded_host(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__627b4a0e31aa482a3e8cd2ca838fb8f2ea76b3f25cb2005bc4a6a7510c57c72b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "xForwardedHost", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionAppFlexConsumptionSiteConfigIpRestrictionHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionAppFlexConsumptionSiteConfigIpRestrictionHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionAppFlexConsumptionSiteConfigIpRestrictionHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__349d20a5516a0fdd701646a4cfcc97893e5741fa5763c306fcfecbce24a292e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FunctionAppFlexConsumptionSiteConfigIpRestrictionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionSiteConfigIpRestrictionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__423fd6af292cf874eb6c7ab1699aa92ea0c16c51fac1393e99247fda47a115f7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FunctionAppFlexConsumptionSiteConfigIpRestrictionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1de06de7794fc9e6f8668a92ae8f5cfdf15dc9f56c07fd1f98ccbe9494090ea7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FunctionAppFlexConsumptionSiteConfigIpRestrictionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e67e3c714b0537ce40080af931bd9da9ba1f30dbbb77717afc2051ede48dcda6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__10f5c6e7d01cee8a204e1284156fb7d2ce79ad088502404b1f45220932370490)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbf31618b3e85e28efaae7a389dff148867e64b01a393ad053b2d74635d6eabe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionSiteConfigIpRestriction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionSiteConfigIpRestriction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionSiteConfigIpRestriction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fda29fba2f44d7eadc5ee2e4053178d03e1d8bdcdeffd6a4fe03a2508bf0a52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FunctionAppFlexConsumptionSiteConfigIpRestrictionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionSiteConfigIpRestrictionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2328ba40c20c2a45eedb18ed81afa086d1a90a55fefcc1b401030f1eecb254f6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHeaders")
    def put_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionAppFlexConsumptionSiteConfigIpRestrictionHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efd93cc6dacf4ddd38cc723c634b7fd37bff320f7dff67a6261575545a99bc8f)
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
    def headers(self) -> FunctionAppFlexConsumptionSiteConfigIpRestrictionHeadersList:
        return typing.cast(FunctionAppFlexConsumptionSiteConfigIpRestrictionHeadersList, jsii.get(self, "headers"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionSiteConfigIpRestrictionHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionSiteConfigIpRestrictionHeaders]]], jsii.get(self, "headersInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ed947c1ca290b798e73e766e3b0f0bee75c75a65552b12429f87335cf5b78534)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d10a4093db40e74f4d58fccf3deebc502bf67736e846d53b85949334dc9af91f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8eec6051b80ce842097735a05c9a1e29ba9469da8a92e44f3208fd5f49c4150)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07a39a8c95143d4e49582c018b19814f82fc5b7ff7e17b8fe8171423a02f282a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff98b345fe575aec06b373a579890691a046eb7d3f2a9d7afecdc49834720fe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceTag")
    def service_tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceTag"))

    @service_tag.setter
    def service_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__242d6ee0b075ea956d671d729f2015fff2ac4d0e8820c7d7fe921be6a5a4afe1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceTag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkSubnetId")
    def virtual_network_subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkSubnetId"))

    @virtual_network_subnet_id.setter
    def virtual_network_subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__807410df19125b035cd79791133d1f261a58d69457d410e0babccf9eca37246d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkSubnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionAppFlexConsumptionSiteConfigIpRestriction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionAppFlexConsumptionSiteConfigIpRestriction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionAppFlexConsumptionSiteConfigIpRestriction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e8f79901b3f799a7a631197fc679a4ff2ad774fbd7a46fa52952ae9fbe489a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FunctionAppFlexConsumptionSiteConfigOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionSiteConfigOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e26c5696247970496ae602cb62817aff815e2c35942094ed1f75433ccbc6b3b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAppServiceLogs")
    def put_app_service_logs(
        self,
        *,
        disk_quota_mb: typing.Optional[jsii.Number] = None,
        retention_period_days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param disk_quota_mb: The amount of disk space to use for logs. Valid values are between ``25`` and ``100``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#disk_quota_mb FunctionAppFlexConsumption#disk_quota_mb}
        :param retention_period_days: The retention period for logs in days. Valid values are between ``0`` and ``99999``. Defaults to ``0`` (never delete). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#retention_period_days FunctionAppFlexConsumption#retention_period_days}
        '''
        value = FunctionAppFlexConsumptionSiteConfigAppServiceLogs(
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
        :param allowed_origins: Specifies a list of origins that should be allowed to make cross-origin calls. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#allowed_origins FunctionAppFlexConsumption#allowed_origins}
        :param support_credentials: Are credentials allowed in CORS requests? Defaults to ``false``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#support_credentials FunctionAppFlexConsumption#support_credentials}
        '''
        value = FunctionAppFlexConsumptionSiteConfigCors(
            allowed_origins=allowed_origins, support_credentials=support_credentials
        )

        return typing.cast(None, jsii.invoke(self, "putCors", [value]))

    @jsii.member(jsii_name="putIpRestriction")
    def put_ip_restriction(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionAppFlexConsumptionSiteConfigIpRestriction, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd45ea738c064a8bf9620c4331fa5b0bbcedda0ae3f8151e1bfa79113ddbeb0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIpRestriction", [value]))

    @jsii.member(jsii_name="putScmIpRestriction")
    def put_scm_ip_restriction(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FunctionAppFlexConsumptionSiteConfigScmIpRestriction", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2227865ff2c165fdf35a8dda9d587b653762369133fc2896b6314d81d7658355)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putScmIpRestriction", [value]))

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

    @jsii.member(jsii_name="resetAppServiceLogs")
    def reset_app_service_logs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppServiceLogs", []))

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
    @jsii.member(jsii_name="appServiceLogs")
    def app_service_logs(
        self,
    ) -> FunctionAppFlexConsumptionSiteConfigAppServiceLogsOutputReference:
        return typing.cast(FunctionAppFlexConsumptionSiteConfigAppServiceLogsOutputReference, jsii.get(self, "appServiceLogs"))

    @builtins.property
    @jsii.member(jsii_name="cors")
    def cors(self) -> FunctionAppFlexConsumptionSiteConfigCorsOutputReference:
        return typing.cast(FunctionAppFlexConsumptionSiteConfigCorsOutputReference, jsii.get(self, "cors"))

    @builtins.property
    @jsii.member(jsii_name="detailedErrorLoggingEnabled")
    def detailed_error_logging_enabled(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "detailedErrorLoggingEnabled"))

    @builtins.property
    @jsii.member(jsii_name="ipRestriction")
    def ip_restriction(self) -> FunctionAppFlexConsumptionSiteConfigIpRestrictionList:
        return typing.cast(FunctionAppFlexConsumptionSiteConfigIpRestrictionList, jsii.get(self, "ipRestriction"))

    @builtins.property
    @jsii.member(jsii_name="scmIpRestriction")
    def scm_ip_restriction(
        self,
    ) -> "FunctionAppFlexConsumptionSiteConfigScmIpRestrictionList":
        return typing.cast("FunctionAppFlexConsumptionSiteConfigScmIpRestrictionList", jsii.get(self, "scmIpRestriction"))

    @builtins.property
    @jsii.member(jsii_name="scmType")
    def scm_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scmType"))

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
    @jsii.member(jsii_name="appServiceLogsInput")
    def app_service_logs_input(
        self,
    ) -> typing.Optional[FunctionAppFlexConsumptionSiteConfigAppServiceLogs]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionSiteConfigAppServiceLogs], jsii.get(self, "appServiceLogsInput"))

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
    def cors_input(self) -> typing.Optional[FunctionAppFlexConsumptionSiteConfigCors]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionSiteConfigCors], jsii.get(self, "corsInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultDocumentsInput")
    def default_documents_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "defaultDocumentsInput"))

    @builtins.property
    @jsii.member(jsii_name="elasticInstanceMinimumInput")
    def elastic_instance_minimum_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "elasticInstanceMinimumInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionSiteConfigIpRestriction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionSiteConfigIpRestriction]]], jsii.get(self, "ipRestrictionInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionAppFlexConsumptionSiteConfigScmIpRestriction"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionAppFlexConsumptionSiteConfigScmIpRestriction"]]], jsii.get(self, "scmIpRestrictionInput"))

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
    @jsii.member(jsii_name="apiDefinitionUrl")
    def api_definition_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiDefinitionUrl"))

    @api_definition_url.setter
    def api_definition_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8a9be2bdd279cbd634a62d2126429071ce8e99f43da99fbe2a02ba71ff025db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiDefinitionUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="apiManagementApiId")
    def api_management_api_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiManagementApiId"))

    @api_management_api_id.setter
    def api_management_api_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__190623a678bad8ccd9eab00d7de09fb5172af7e4a393a1059ac9452fa0a853e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiManagementApiId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appCommandLine")
    def app_command_line(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appCommandLine"))

    @app_command_line.setter
    def app_command_line(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c4dbc67e36c054659d91e7cd83798797df09cab12dda7b506333d9875188bc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appCommandLine", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="applicationInsightsConnectionString")
    def application_insights_connection_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationInsightsConnectionString"))

    @application_insights_connection_string.setter
    def application_insights_connection_string(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c32bb8c511ee54f415bfca2783e74ea9ec05d882325ccac676ee03d4b4a8744)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationInsightsConnectionString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="applicationInsightsKey")
    def application_insights_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "applicationInsightsKey"))

    @application_insights_key.setter
    def application_insights_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78dc8b0657d3785bd3195ca676afe090855ee92a80478c1c7f2574f5bf2ad195)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationInsightsKey", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__edc48f505422d342c89d268014c94ee27f49deef99dcd792f79a85a3f0708595)
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
            type_hints = typing.get_type_hints(_typecheckingstub__81b9575782f25a77726ad8078397094991f0e75a9592452f1a4b9cd9defe6f6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerRegistryUseManagedIdentity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultDocuments")
    def default_documents(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "defaultDocuments"))

    @default_documents.setter
    def default_documents(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b91abd55fa648adcf48409b0d85e9ff120645b7653ef5a0568c10569ffcb6f17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultDocuments", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="elasticInstanceMinimum")
    def elastic_instance_minimum(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "elasticInstanceMinimum"))

    @elastic_instance_minimum.setter
    def elastic_instance_minimum(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23ad110787d2fa7ceaadbe08decd2c9de8631fd684757ea976d06014370d25bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "elasticInstanceMinimum", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="healthCheckEvictionTimeInMin")
    def health_check_eviction_time_in_min(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "healthCheckEvictionTimeInMin"))

    @health_check_eviction_time_in_min.setter
    def health_check_eviction_time_in_min(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aff25b0eeb6aa7c289858594a1c5d21f1816fa5cd968717c28137b64b41d6fd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthCheckEvictionTimeInMin", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="healthCheckPath")
    def health_check_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "healthCheckPath"))

    @health_check_path.setter
    def health_check_path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd4415a7e6f3d27cd303490c477cc8bc1697ec1866c6047fa629f8d81cbb684a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__478620669f856375f8a9bd13634b1ab2f5a66af18cfedadc2b128757a781783b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "http2Enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipRestrictionDefaultAction")
    def ip_restriction_default_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipRestrictionDefaultAction"))

    @ip_restriction_default_action.setter
    def ip_restriction_default_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f29935c9ed4b05fd0f8412dde7345dd162e812fb24dbd024796826e99b509511)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipRestrictionDefaultAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="loadBalancingMode")
    def load_balancing_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "loadBalancingMode"))

    @load_balancing_mode.setter
    def load_balancing_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__348e4ed1a4e1246b018b296733f67ab957afac2b01dd1542f821024b602b0f30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loadBalancingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managedPipelineMode")
    def managed_pipeline_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managedPipelineMode"))

    @managed_pipeline_mode.setter
    def managed_pipeline_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d66ebfbf603e9e97c102459187ddc03ff19d30608ec07ff4868efdc867619a2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedPipelineMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimumTlsVersion")
    def minimum_tls_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "minimumTlsVersion"))

    @minimum_tls_version.setter
    def minimum_tls_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__601639ac7c1d3b63325daeb21e4ef2136eae693da412c2a098388fcc39bf433f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumTlsVersion", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__60f2a76533c17d428af81929bbddb79736045492c67ec7276bc642e7be60063e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteDebuggingEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="remoteDebuggingVersion")
    def remote_debugging_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "remoteDebuggingVersion"))

    @remote_debugging_version.setter
    def remote_debugging_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__769acac630bb03cf9960f0d91786e90b09f6fd9633bad6bf1478796c0e2750fc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__16cc3d2b95b8cee30a756399448dc70ba2b3c34913066202354f843a1831fb0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runtimeScaleMonitoringEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scmIpRestrictionDefaultAction")
    def scm_ip_restriction_default_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scmIpRestrictionDefaultAction"))

    @scm_ip_restriction_default_action.setter
    def scm_ip_restriction_default_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e37dc4921df6380ac11a265bdfd7979862074a46a4dc8748dd85faaab2638d1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scmIpRestrictionDefaultAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scmMinimumTlsVersion")
    def scm_minimum_tls_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "scmMinimumTlsVersion"))

    @scm_minimum_tls_version.setter
    def scm_minimum_tls_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__912688703a61d9a9f3097be0662abb5d29204e52ef15cfc7f1aaca66f2a1b30d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__237839eb4a4a4c9f506611a521fa6b9804d2966ce1574c70860ee175d7c5b52a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac533d41d676be5c0a694da929c5ec13d8001735ddd8ddda20a7d522b53aa40b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e88a6ca0db1d0563697fecbacf81cb8cecbf0d7f87e5d8bc4d1e3006d8a5f2b2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a1ea93f62292d95b38809b72849443c5fe2f155ad1df6af7b3804236b9f2c3d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "websocketsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workerCount")
    def worker_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "workerCount"))

    @worker_count.setter
    def worker_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a47bfa7f76c113a5da0ded5b7ed0df569ed82f3b64dcfd2ba0717ba9076c3a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workerCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[FunctionAppFlexConsumptionSiteConfig]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionSiteConfig], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionAppFlexConsumptionSiteConfig],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddb85ac225eea55d1577e6e719483b9c6ea414c128bb7180f1f2bd590d9f5f5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionSiteConfigScmIpRestriction",
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
class FunctionAppFlexConsumptionSiteConfigScmIpRestriction:
    def __init__(
        self,
        *,
        action: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["FunctionAppFlexConsumptionSiteConfigScmIpRestrictionHeaders", typing.Dict[builtins.str, typing.Any]]]]] = None,
        ip_address: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        service_tag: typing.Optional[builtins.str] = None,
        virtual_network_subnet_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param action: The action to take. Possible values are ``Allow`` or ``Deny``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#action FunctionAppFlexConsumption#action}
        :param description: The description of the IP restriction rule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#description FunctionAppFlexConsumption#description}
        :param headers: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#headers FunctionAppFlexConsumption#headers}.
        :param ip_address: The CIDR notation of the IP or IP Range to match. For example: ``10.0.0.0/24`` or ``192.168.10.1/32`` or ``fe80::/64`` or ``13.107.6.152/31,13.107.128.0/22`` Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#ip_address FunctionAppFlexConsumption#ip_address}
        :param name: The name which should be used for this ``ip_restriction``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#name FunctionAppFlexConsumption#name}
        :param priority: The priority value of this ``ip_restriction``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#priority FunctionAppFlexConsumption#priority}
        :param service_tag: The Service Tag used for this IP Restriction. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#service_tag FunctionAppFlexConsumption#service_tag}
        :param virtual_network_subnet_id: The Virtual Network Subnet ID used for this IP Restriction. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#virtual_network_subnet_id FunctionAppFlexConsumption#virtual_network_subnet_id}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06b8b644e276a07b2ecd045a37dbf9f06917b90825604a458780ad2028108912)
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

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#action FunctionAppFlexConsumption#action}
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the IP restriction rule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#description FunctionAppFlexConsumption#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def headers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionAppFlexConsumptionSiteConfigScmIpRestrictionHeaders"]]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#headers FunctionAppFlexConsumption#headers}.'''
        result = self._values.get("headers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["FunctionAppFlexConsumptionSiteConfigScmIpRestrictionHeaders"]]], result)

    @builtins.property
    def ip_address(self) -> typing.Optional[builtins.str]:
        '''The CIDR notation of the IP or IP Range to match.

        For example: ``10.0.0.0/24`` or ``192.168.10.1/32`` or ``fe80::/64`` or ``13.107.6.152/31,13.107.128.0/22``

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#ip_address FunctionAppFlexConsumption#ip_address}
        '''
        result = self._values.get("ip_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name which should be used for this ``ip_restriction``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#name FunctionAppFlexConsumption#name}
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''The priority value of this ``ip_restriction``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#priority FunctionAppFlexConsumption#priority}
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service_tag(self) -> typing.Optional[builtins.str]:
        '''The Service Tag used for this IP Restriction.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#service_tag FunctionAppFlexConsumption#service_tag}
        '''
        result = self._values.get("service_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def virtual_network_subnet_id(self) -> typing.Optional[builtins.str]:
        '''The Virtual Network Subnet ID used for this IP Restriction.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#virtual_network_subnet_id FunctionAppFlexConsumption#virtual_network_subnet_id}
        '''
        result = self._values.get("virtual_network_subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionAppFlexConsumptionSiteConfigScmIpRestriction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionSiteConfigScmIpRestrictionHeaders",
    jsii_struct_bases=[],
    name_mapping={
        "x_azure_fdid": "xAzureFdid",
        "x_fd_health_probe": "xFdHealthProbe",
        "x_forwarded_for": "xForwardedFor",
        "x_forwarded_host": "xForwardedHost",
    },
)
class FunctionAppFlexConsumptionSiteConfigScmIpRestrictionHeaders:
    def __init__(
        self,
        *,
        x_azure_fdid: typing.Optional[typing.Sequence[builtins.str]] = None,
        x_fd_health_probe: typing.Optional[typing.Sequence[builtins.str]] = None,
        x_forwarded_for: typing.Optional[typing.Sequence[builtins.str]] = None,
        x_forwarded_host: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param x_azure_fdid: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#x_azure_fdid FunctionAppFlexConsumption#x_azure_fdid}.
        :param x_fd_health_probe: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#x_fd_health_probe FunctionAppFlexConsumption#x_fd_health_probe}.
        :param x_forwarded_for: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#x_forwarded_for FunctionAppFlexConsumption#x_forwarded_for}.
        :param x_forwarded_host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#x_forwarded_host FunctionAppFlexConsumption#x_forwarded_host}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3458f39701815ec143c3630e0149960fc4e9e8b9fcb8be1737519fbc865dc4f1)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#x_azure_fdid FunctionAppFlexConsumption#x_azure_fdid}.'''
        result = self._values.get("x_azure_fdid")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def x_fd_health_probe(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#x_fd_health_probe FunctionAppFlexConsumption#x_fd_health_probe}.'''
        result = self._values.get("x_fd_health_probe")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def x_forwarded_for(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#x_forwarded_for FunctionAppFlexConsumption#x_forwarded_for}.'''
        result = self._values.get("x_forwarded_for")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def x_forwarded_host(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#x_forwarded_host FunctionAppFlexConsumption#x_forwarded_host}.'''
        result = self._values.get("x_forwarded_host")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionAppFlexConsumptionSiteConfigScmIpRestrictionHeaders(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionAppFlexConsumptionSiteConfigScmIpRestrictionHeadersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionSiteConfigScmIpRestrictionHeadersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e39b9fe7c0c6ddaf5be194b5399e5e9d68cdb57682f6265dcdd0ae117205ce0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FunctionAppFlexConsumptionSiteConfigScmIpRestrictionHeadersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab05d39ca210ad75cf7a730a329b7c2a787b737bd6585bfc262f9d5fe62cf0fa)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FunctionAppFlexConsumptionSiteConfigScmIpRestrictionHeadersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__844e692acd612011ffc76b377c4ef56a4f16ccdec9395dc838e4017ee5cd2291)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ef6903842315a8a72715b083e45354e1fdcac5e06a46fb9738eb1ec977f8a6f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e4400f30b515e4f13914829f599e713c7307fe4d31853dfa10e2d4fe05635ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionSiteConfigScmIpRestrictionHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionSiteConfigScmIpRestrictionHeaders]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionSiteConfigScmIpRestrictionHeaders]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7121b9896c1888ed5d4362cfcb70a2437bb527325b8f802c3c6db0eddf5831ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FunctionAppFlexConsumptionSiteConfigScmIpRestrictionHeadersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionSiteConfigScmIpRestrictionHeadersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__026e5112bd91b5c5efeec1711e1714e3e4c58e44627c2fc8710f7e2e9903f457)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef214e66b29fcada8ab8f2b2d3ce5052354b5d101d429333e15e6c32443a6ced)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "xAzureFdid", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="xFdHealthProbe")
    def x_fd_health_probe(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "xFdHealthProbe"))

    @x_fd_health_probe.setter
    def x_fd_health_probe(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a7efbef0b5207f8b3881a5420f4eff12e5a6d6f77f26a9bf2bfc2a6bb7b8c0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "xFdHealthProbe", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="xForwardedFor")
    def x_forwarded_for(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "xForwardedFor"))

    @x_forwarded_for.setter
    def x_forwarded_for(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02f5be37947ec9bef2e84686b728ba31ea445cec73757783ae68d99e1eefdba3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "xForwardedFor", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="xForwardedHost")
    def x_forwarded_host(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "xForwardedHost"))

    @x_forwarded_host.setter
    def x_forwarded_host(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c84659c6cf1c78248bcb1f4e9d1df7516954ec88aa3b379bc4019ffd6ffac9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "xForwardedHost", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionAppFlexConsumptionSiteConfigScmIpRestrictionHeaders]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionAppFlexConsumptionSiteConfigScmIpRestrictionHeaders]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionAppFlexConsumptionSiteConfigScmIpRestrictionHeaders]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6e38440f1e8ca884fbce12feeb861a01ec87d90ec590d03d710c7eadab169bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FunctionAppFlexConsumptionSiteConfigScmIpRestrictionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionSiteConfigScmIpRestrictionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b3380f7e3258aafe432e96cbdccee20b82264474901b4411dea0925c3fdb9db)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FunctionAppFlexConsumptionSiteConfigScmIpRestrictionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e1c42392302e4e0cce9aa492ed4d23e52826b04d5ddbff1283572e3fae20f47)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FunctionAppFlexConsumptionSiteConfigScmIpRestrictionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__058b19b5f0dcee8e97d298f5cdf193ce4ec8ef2ccfcf433f8f735e82c79c5a22)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b6056d7fd096b71a707d6cbc203dc925e30652f86129520c83222bb508fd7d2b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b492054db77fccae5a6a33c7b3162efdfaa68c85802b4b7ca024979236b12b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionSiteConfigScmIpRestriction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionSiteConfigScmIpRestriction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionSiteConfigScmIpRestriction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ded63078bce796ceb37f59e05411feda4cc6208b9a09d0b06e9e268fb16c536)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class FunctionAppFlexConsumptionSiteConfigScmIpRestrictionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionSiteConfigScmIpRestrictionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9054c6247b79c09714ad0f183da8c9392f2482f978b22f023cde2ae512dcfe10)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHeaders")
    def put_headers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionAppFlexConsumptionSiteConfigScmIpRestrictionHeaders, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fd125ff50abdc7504482c0a85caaa8891d5db31e8d007018d708e1d6a965c14)
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
    def headers(
        self,
    ) -> FunctionAppFlexConsumptionSiteConfigScmIpRestrictionHeadersList:
        return typing.cast(FunctionAppFlexConsumptionSiteConfigScmIpRestrictionHeadersList, jsii.get(self, "headers"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionSiteConfigScmIpRestrictionHeaders]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionSiteConfigScmIpRestrictionHeaders]]], jsii.get(self, "headersInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__fc4e8a0faaa8936c9a11522089153f52b8a83f509f27d3fe19f60f650d1e5412)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c599d9918b15ceea4ca7f1f498efe536f8f4856a316c53a3be037774b6ae8e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipAddress")
    def ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ipAddress"))

    @ip_address.setter
    def ip_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25f546e2af34a3b6a2c36b4147fe8517e1f2d848a2455436c34dda515e02e3af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86badbb3ad87dc0f74e65c0ce40025bc0c96898a4f89226ab93ab97d708b5765)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1963be73330cd1ec4eba2ea753aa3131ff1d3bdfc0e1e2c2e843866a7c72fe70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceTag")
    def service_tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceTag"))

    @service_tag.setter
    def service_tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c87813d2f375e927adba996302e337783cc6eacbdcb59acd922978eab159248)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceTag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="virtualNetworkSubnetId")
    def virtual_network_subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "virtualNetworkSubnetId"))

    @virtual_network_subnet_id.setter
    def virtual_network_subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e15deb627f572da94df0f18489755b07edd016e142f212e9008f7826382891d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualNetworkSubnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionAppFlexConsumptionSiteConfigScmIpRestriction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionAppFlexConsumptionSiteConfigScmIpRestriction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionAppFlexConsumptionSiteConfigScmIpRestriction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad5ac1086df13eceb1ec9443aac3cb84c1a4ad0bd4dd81a35d5cc67079b8c62b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionSiteCredential",
    jsii_struct_bases=[],
    name_mapping={},
)
class FunctionAppFlexConsumptionSiteCredential:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionAppFlexConsumptionSiteCredential(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionAppFlexConsumptionSiteCredentialList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionSiteCredentialList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa904b3ff3b6a0e12b9b85a4eee5e716c53cc822bf61baa08c171ad79103ec15)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "FunctionAppFlexConsumptionSiteCredentialOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34f90608e3b2b6574477139a546a80e8bd0bdd66dafe1d18048d9e196d39ebeb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("FunctionAppFlexConsumptionSiteCredentialOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79aa49e33282b56c9d5e479fa097dd9c8986baef7ea1bfc66660d070cd75505d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3c2bb9d8fb089e0214f425303a55ca0c583161c6879bc38741e0aaa4a257cc4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__84b6af6e161ce5be4ae6e9a34a4c8a164ce2179c57d39ef37dacff88a67007b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class FunctionAppFlexConsumptionSiteCredentialOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionSiteCredentialOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a5d856412c6d9191b0f82a70c24813706b003964367be24b92374675ede8ced)
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
    def internal_value(
        self,
    ) -> typing.Optional[FunctionAppFlexConsumptionSiteCredential]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionSiteCredential], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionAppFlexConsumptionSiteCredential],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fe4efc32501b801641e52f7f4328935f6c083bfc1c15542cb9d488b7bfcf754)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionStickySettings",
    jsii_struct_bases=[],
    name_mapping={
        "app_setting_names": "appSettingNames",
        "connection_string_names": "connectionStringNames",
    },
)
class FunctionAppFlexConsumptionStickySettings:
    def __init__(
        self,
        *,
        app_setting_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        connection_string_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param app_setting_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#app_setting_names FunctionAppFlexConsumption#app_setting_names}.
        :param connection_string_names: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#connection_string_names FunctionAppFlexConsumption#connection_string_names}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79317e5333bcc7f18255fa5eee6b64fa5f94e7fedb9366c365d37cc0040e577e)
            check_type(argname="argument app_setting_names", value=app_setting_names, expected_type=type_hints["app_setting_names"])
            check_type(argname="argument connection_string_names", value=connection_string_names, expected_type=type_hints["connection_string_names"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if app_setting_names is not None:
            self._values["app_setting_names"] = app_setting_names
        if connection_string_names is not None:
            self._values["connection_string_names"] = connection_string_names

    @builtins.property
    def app_setting_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#app_setting_names FunctionAppFlexConsumption#app_setting_names}.'''
        result = self._values.get("app_setting_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def connection_string_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#connection_string_names FunctionAppFlexConsumption#connection_string_names}.'''
        result = self._values.get("connection_string_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionAppFlexConsumptionStickySettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionAppFlexConsumptionStickySettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionStickySettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__23dcf202085a8bc0642667f3c3554f8716048b9e24f9f34f59593d611c26311f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAppSettingNames")
    def reset_app_setting_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppSettingNames", []))

    @jsii.member(jsii_name="resetConnectionStringNames")
    def reset_connection_string_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionStringNames", []))

    @builtins.property
    @jsii.member(jsii_name="appSettingNamesInput")
    def app_setting_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "appSettingNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionStringNamesInput")
    def connection_string_names_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "connectionStringNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="appSettingNames")
    def app_setting_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "appSettingNames"))

    @app_setting_names.setter
    def app_setting_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e6c8498e124fe925b7142331717328c531f9abb8bedbf3fc2c18514da9dcadb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appSettingNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="connectionStringNames")
    def connection_string_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "connectionStringNames"))

    @connection_string_names.setter
    def connection_string_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c44b975efdf5349fe1607081fcd8e963f8bc524946660c5740819f1956ad421f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionStringNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[FunctionAppFlexConsumptionStickySettings]:
        return typing.cast(typing.Optional[FunctionAppFlexConsumptionStickySettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[FunctionAppFlexConsumptionStickySettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f223a672fa694fd5a67d1d1145d61d3b4d09e281b74a38654584121a2265aa56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class FunctionAppFlexConsumptionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#create FunctionAppFlexConsumption#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#delete FunctionAppFlexConsumption#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#read FunctionAppFlexConsumption#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#update FunctionAppFlexConsumption#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfd8edd64cb7b77d5bc7a9c73c1f28f97d8198c92e6dbee354c9b407f192bb03)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#create FunctionAppFlexConsumption#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#delete FunctionAppFlexConsumption#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#read FunctionAppFlexConsumption#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/function_app_flex_consumption#update FunctionAppFlexConsumption#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FunctionAppFlexConsumptionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FunctionAppFlexConsumptionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.functionAppFlexConsumption.FunctionAppFlexConsumptionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e882123d564a3e6f5c852899e4c6f41f3f28aa20370e6c2dc9302a3d89feb21)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9975464084fc5e816336d27b3abf3af5b575ed64a19a215054c6ab211d96fbcd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31a6b571b5649454a323cd37adfbaaa9f80619e9422cd23d678f8464c566b942)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aba6e6325d954f88b7f8cd4bf8d8d3b11d8aa8693d42d8220612fbd39a7a8e31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80dab1f23c78879f2845a1ae1d70abdfd7eadaea80ee1c1b4d3271ac3ac55804)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionAppFlexConsumptionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionAppFlexConsumptionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionAppFlexConsumptionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a001c557bd0bc935756daabc859ef6035cb7d8ba6bd9a2c0b14ecddc81847ba5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "FunctionAppFlexConsumption",
    "FunctionAppFlexConsumptionAlwaysReady",
    "FunctionAppFlexConsumptionAlwaysReadyList",
    "FunctionAppFlexConsumptionAlwaysReadyOutputReference",
    "FunctionAppFlexConsumptionAuthSettings",
    "FunctionAppFlexConsumptionAuthSettingsActiveDirectory",
    "FunctionAppFlexConsumptionAuthSettingsActiveDirectoryOutputReference",
    "FunctionAppFlexConsumptionAuthSettingsFacebook",
    "FunctionAppFlexConsumptionAuthSettingsFacebookOutputReference",
    "FunctionAppFlexConsumptionAuthSettingsGithub",
    "FunctionAppFlexConsumptionAuthSettingsGithubOutputReference",
    "FunctionAppFlexConsumptionAuthSettingsGoogle",
    "FunctionAppFlexConsumptionAuthSettingsGoogleOutputReference",
    "FunctionAppFlexConsumptionAuthSettingsMicrosoft",
    "FunctionAppFlexConsumptionAuthSettingsMicrosoftOutputReference",
    "FunctionAppFlexConsumptionAuthSettingsOutputReference",
    "FunctionAppFlexConsumptionAuthSettingsTwitter",
    "FunctionAppFlexConsumptionAuthSettingsTwitterOutputReference",
    "FunctionAppFlexConsumptionAuthSettingsV2",
    "FunctionAppFlexConsumptionAuthSettingsV2ActiveDirectoryV2",
    "FunctionAppFlexConsumptionAuthSettingsV2ActiveDirectoryV2OutputReference",
    "FunctionAppFlexConsumptionAuthSettingsV2AppleV2",
    "FunctionAppFlexConsumptionAuthSettingsV2AppleV2OutputReference",
    "FunctionAppFlexConsumptionAuthSettingsV2AzureStaticWebAppV2",
    "FunctionAppFlexConsumptionAuthSettingsV2AzureStaticWebAppV2OutputReference",
    "FunctionAppFlexConsumptionAuthSettingsV2CustomOidcV2",
    "FunctionAppFlexConsumptionAuthSettingsV2CustomOidcV2List",
    "FunctionAppFlexConsumptionAuthSettingsV2CustomOidcV2OutputReference",
    "FunctionAppFlexConsumptionAuthSettingsV2FacebookV2",
    "FunctionAppFlexConsumptionAuthSettingsV2FacebookV2OutputReference",
    "FunctionAppFlexConsumptionAuthSettingsV2GithubV2",
    "FunctionAppFlexConsumptionAuthSettingsV2GithubV2OutputReference",
    "FunctionAppFlexConsumptionAuthSettingsV2GoogleV2",
    "FunctionAppFlexConsumptionAuthSettingsV2GoogleV2OutputReference",
    "FunctionAppFlexConsumptionAuthSettingsV2Login",
    "FunctionAppFlexConsumptionAuthSettingsV2LoginOutputReference",
    "FunctionAppFlexConsumptionAuthSettingsV2MicrosoftV2",
    "FunctionAppFlexConsumptionAuthSettingsV2MicrosoftV2OutputReference",
    "FunctionAppFlexConsumptionAuthSettingsV2OutputReference",
    "FunctionAppFlexConsumptionAuthSettingsV2TwitterV2",
    "FunctionAppFlexConsumptionAuthSettingsV2TwitterV2OutputReference",
    "FunctionAppFlexConsumptionConfig",
    "FunctionAppFlexConsumptionConnectionString",
    "FunctionAppFlexConsumptionConnectionStringList",
    "FunctionAppFlexConsumptionConnectionStringOutputReference",
    "FunctionAppFlexConsumptionIdentity",
    "FunctionAppFlexConsumptionIdentityOutputReference",
    "FunctionAppFlexConsumptionSiteConfig",
    "FunctionAppFlexConsumptionSiteConfigAppServiceLogs",
    "FunctionAppFlexConsumptionSiteConfigAppServiceLogsOutputReference",
    "FunctionAppFlexConsumptionSiteConfigCors",
    "FunctionAppFlexConsumptionSiteConfigCorsOutputReference",
    "FunctionAppFlexConsumptionSiteConfigIpRestriction",
    "FunctionAppFlexConsumptionSiteConfigIpRestrictionHeaders",
    "FunctionAppFlexConsumptionSiteConfigIpRestrictionHeadersList",
    "FunctionAppFlexConsumptionSiteConfigIpRestrictionHeadersOutputReference",
    "FunctionAppFlexConsumptionSiteConfigIpRestrictionList",
    "FunctionAppFlexConsumptionSiteConfigIpRestrictionOutputReference",
    "FunctionAppFlexConsumptionSiteConfigOutputReference",
    "FunctionAppFlexConsumptionSiteConfigScmIpRestriction",
    "FunctionAppFlexConsumptionSiteConfigScmIpRestrictionHeaders",
    "FunctionAppFlexConsumptionSiteConfigScmIpRestrictionHeadersList",
    "FunctionAppFlexConsumptionSiteConfigScmIpRestrictionHeadersOutputReference",
    "FunctionAppFlexConsumptionSiteConfigScmIpRestrictionList",
    "FunctionAppFlexConsumptionSiteConfigScmIpRestrictionOutputReference",
    "FunctionAppFlexConsumptionSiteCredential",
    "FunctionAppFlexConsumptionSiteCredentialList",
    "FunctionAppFlexConsumptionSiteCredentialOutputReference",
    "FunctionAppFlexConsumptionStickySettings",
    "FunctionAppFlexConsumptionStickySettingsOutputReference",
    "FunctionAppFlexConsumptionTimeouts",
    "FunctionAppFlexConsumptionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__126b9577b10a7316d290734ff529d809fb5c8dc24deb3c5120963aef8c80f571(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    runtime_name: builtins.str,
    runtime_version: builtins.str,
    service_plan_id: builtins.str,
    site_config: typing.Union[FunctionAppFlexConsumptionSiteConfig, typing.Dict[builtins.str, typing.Any]],
    storage_authentication_type: builtins.str,
    storage_container_endpoint: builtins.str,
    storage_container_type: builtins.str,
    always_ready: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionAppFlexConsumptionAlwaysReady, typing.Dict[builtins.str, typing.Any]]]]] = None,
    app_settings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    auth_settings: typing.Optional[typing.Union[FunctionAppFlexConsumptionAuthSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    auth_settings_v2: typing.Optional[typing.Union[FunctionAppFlexConsumptionAuthSettingsV2, typing.Dict[builtins.str, typing.Any]]] = None,
    client_certificate_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_certificate_exclusion_paths: typing.Optional[builtins.str] = None,
    client_certificate_mode: typing.Optional[builtins.str] = None,
    connection_string: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionAppFlexConsumptionConnectionString, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    https_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[FunctionAppFlexConsumptionIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    instance_memory_in_mb: typing.Optional[jsii.Number] = None,
    maximum_instance_count: typing.Optional[jsii.Number] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sticky_settings: typing.Optional[typing.Union[FunctionAppFlexConsumptionStickySettings, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_access_key: typing.Optional[builtins.str] = None,
    storage_user_assigned_identity_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[FunctionAppFlexConsumptionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_network_subnet_id: typing.Optional[builtins.str] = None,
    webdeploy_publish_basic_authentication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    zip_deploy_file: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__1b7fbacc1be6422c2bc003c26840fbb1c6ea4fd129ee84112f1f70e935898926(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40ce25227edf520677e2d55c45479ce5c68d11de711c6542880cdef81751679f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionAppFlexConsumptionAlwaysReady, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dde6579271f293d0e04989a80087daac9feab94328203426db6bdddcd8ae788f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionAppFlexConsumptionConnectionString, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2feffe7e0c8fd657514c0217544cc4f23aec888f806bb4daede80fed151082a5(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba7e1674fee7b12b4948bf90a2f4c88b99d836db0684c887f47d9c296ab9618a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__338f64c22a046986a86d031df1039f2c5060a765bcc3cf24d9270276d89b5233(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0607c0220302892b64cbade88db326ae339c483aca1f532178dddabf988613ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3365ab7303831e9a6f700eed7a3799ed66203c99cbd2d74820345e79d41fe3b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b29511d734477ea729d4ffe81fec481ecfb24a43334c3e5b7706e170f8bace1(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51f1d08463b971cd1939807c870770d3b17641a6beb0c82f5dbcc22c434ba8be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae4ac2f2b8e826c0416eabcc2c8c8b3dff04818e6d80e5a8071a91c972eb06f1(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad347117faa54590d0661668f502301fd09c7155cdf13dcbda742ed478cb7766(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__195fb5f066fd72f5e533199e9976369c64f607fe9880d078663af15e943cc94a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b1470c16d75211ed1892dc753409ad0f789c6a8f2c76d99227a1b00667908a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2463793ec9606242c88a572e248a680c26cf61fa7665f2377e1765fcb82d0212(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06a58b1961b33915d3d5fe41fa0dff62cfe6fd9fda1f87e1d2e971331aab5040(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72aef464f999321612e8c33c76e97b8d7ee60e6b3017e07a37fdd207d73fc4d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea6f2e9e91e0bd5500fe8b7ce51d4e017e56848137f754cf3333f83738ca532e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f9ca24a10fc09e798a4a2ecfff33f4099aab1de89dbee9a26b7c5aea2053a66(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b3307af676806f38ed1654f0989109e4e6cedd9384cf7cbce7237e55b9d6215(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e63bc31b91af5018234c3f70da7bcf64f3e65fb9d795998ae68e86074a8f108(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06f52a3ac7562f81625802c791490faaa5494f1440e8e434c507f6666f83e557(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88855aace53efc4934e3ba1cbbc6c84a004a9a57281c832bd66d057dbbde9b44(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__760fb3bf0d72bf9596367946fe13c8a010726297c4134b7b2378c7373b15cf31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90e1c37b5ea9b3b7accd8b6ed27471a9b9c6c7302baaffd79389532328abb6f0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9cb623e8c7a4e54dd592258a032d24323dd5a468c7c086b6d3b4465c3ab0956(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c789f5c81b67a781bec1b961e7a1f6ea7b0f3cdf13c2c03ed6b819db4399d54b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65550156545b88b41265d7f8f91fb89c366212463206b9b61a268893c323e188(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8463a737a873ef7e79fda7a9794ba048e43b699cb216eb5ee2a17f57414696dc(
    *,
    name: builtins.str,
    instance_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__601d27bfb3937ba5b7b76f0584163d5cbc72fe11b5cf60fcc3317ef2db676475(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc043e2172cc1e0d72d2874882ab2f315d1d949a8c67223b26fa1c22bf0d4e15(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b05646d97375cac84e7182ba145f3723d88d7a872ffdaf7edd2df5f089d5e5e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b328212f440582ca6b75468ac0864b61e030f43aa46a9804ac8f96c73275035(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2594e6aca29f0cdb572fc4fa6d63af749c8129b6fda471e5646870e45400743e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58c188d29062303309e745b567546760d123f5235054c7bfb3b0de28f70dd921(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionAlwaysReady]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c27c7ce6c3ed96a59d85bdaec62bb1cf28563f81c9227030322e890a0e3a506(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__644b7b7bf463e785eb90942265dedce4fb68833e07af18233e66ee03fb4dc20f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45de20ebc141bea7de9f3c14b61cc7a28a5fee9074bd7a168c0688bdbcf30cbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f7c905decdf813697fd6665266492cd489ce4a8bb7bb86f2d228c3dc55a40f2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionAppFlexConsumptionAlwaysReady]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33a5c2f61785385d03e582398da51411a6061765eaee2b3273c261f58c70a509(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    active_directory: typing.Optional[typing.Union[FunctionAppFlexConsumptionAuthSettingsActiveDirectory, typing.Dict[builtins.str, typing.Any]]] = None,
    additional_login_parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    allowed_external_redirect_urls: typing.Optional[typing.Sequence[builtins.str]] = None,
    default_provider: typing.Optional[builtins.str] = None,
    facebook: typing.Optional[typing.Union[FunctionAppFlexConsumptionAuthSettingsFacebook, typing.Dict[builtins.str, typing.Any]]] = None,
    github: typing.Optional[typing.Union[FunctionAppFlexConsumptionAuthSettingsGithub, typing.Dict[builtins.str, typing.Any]]] = None,
    google: typing.Optional[typing.Union[FunctionAppFlexConsumptionAuthSettingsGoogle, typing.Dict[builtins.str, typing.Any]]] = None,
    issuer: typing.Optional[builtins.str] = None,
    microsoft: typing.Optional[typing.Union[FunctionAppFlexConsumptionAuthSettingsMicrosoft, typing.Dict[builtins.str, typing.Any]]] = None,
    runtime_version: typing.Optional[builtins.str] = None,
    token_refresh_extension_hours: typing.Optional[jsii.Number] = None,
    token_store_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    twitter: typing.Optional[typing.Union[FunctionAppFlexConsumptionAuthSettingsTwitter, typing.Dict[builtins.str, typing.Any]]] = None,
    unauthenticated_client_action: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5e6055c5e1def326ef64c02117c39a68690d59a1ab27e5c099bcbfe176028d8(
    *,
    client_id: builtins.str,
    allowed_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
    client_secret: typing.Optional[builtins.str] = None,
    client_secret_setting_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41fdf5da4f6ce4657aa2c2dae68e2415c04ec83ec05cafd0ef4e23dacd45fc2b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ad38faa354a0fd31af190866d01d8878b47ea8b682c79da43a01cbd4675306b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf79324d2a5cdec7cb3ee11b201477985f673f67558bbcf80a124a8447137a52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a475a5ee81b9e118670a0552330b22066a663b84c00b3a779555e7185812b7bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__984b8016a1515f22b826acb32a9b8315f9dcd3201f4d1d61678f7049fdf50f57(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__631b5338e9a11f26ede5b83b78b6dcc912a4ddb2385f10d5bd31f1e29fcadd7b(
    value: typing.Optional[FunctionAppFlexConsumptionAuthSettingsActiveDirectory],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c9bc3da4ed6fe0bdd2a055f42cc1fe9d8a4bc7a8557519e8ce34a31441601a4(
    *,
    app_id: builtins.str,
    app_secret: typing.Optional[builtins.str] = None,
    app_secret_setting_name: typing.Optional[builtins.str] = None,
    oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9461a898efcf67b81bcbfc874aa50edd07b9247a53058d39f31d935155f34e9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3af25de99670b0fbfe0a8ae003ed06ec11408c8690b6dceaa24b5f4b87d6a9be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dca3ff37da32528c30ddb9ae3b13924e1fef5a3edaca6adf409205d76aedb9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__297b19eb3e8039fd170a75910a4c6aa8e74af2f936f4153209bd1801ced75ad2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1eaf85798af5370eafa1f1a69a0fd5c189449c752a27c99673b8e252d6f6cf3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b66aa716fb035544d9d9b943a5e0379056fcef364e8b407c8a65bcf6f8137a1(
    value: typing.Optional[FunctionAppFlexConsumptionAuthSettingsFacebook],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c79c91699c982418e73af8c56c29efd7dda593ceec4a2da48b2f15c7b51035c8(
    *,
    client_id: builtins.str,
    client_secret: typing.Optional[builtins.str] = None,
    client_secret_setting_name: typing.Optional[builtins.str] = None,
    oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b7dde99db6a75920cfa2b939d43c56d7780e88dfcd40a11b3652abdb3f6a1ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a2ebca37913e5c75d6f9aadc8ec0ca0fc0009486621a8eba881529a583ac1af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0319bc9f8cd8401cae1f08414544d20e642f63ed08b6bf468aecc63059973d62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__624b36a374b5fffeaac90016f4b1550e7b4310e7a0037914911c6ea3c9ffb7a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d23a55441f403a2e772889dd8a6fb50fedbb9dda1e2a0135439ebe70e890e14(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53c7f51cefb6d0e53a21caf54d45e63444093541b317d78c2290176b78ffb89b(
    value: typing.Optional[FunctionAppFlexConsumptionAuthSettingsGithub],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__794063635fa89eb2055cc87f151fce401807ab61f387b80b74b30cd208819687(
    *,
    client_id: builtins.str,
    client_secret: typing.Optional[builtins.str] = None,
    client_secret_setting_name: typing.Optional[builtins.str] = None,
    oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3672946e00797a6c9cd0e2b2fac1d1d7b53c62dd39b3f17ff1ae14026954aa27(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b4a82fdee529d662e7ee852c5ccb750a596b918d25f1cc060021a128b04df77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c940b69a9669c004326680cb3b3cb00834804940bd3ef844a8356997e2c0a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__075283454b4bd3d677f886e38fc5ec801e2949d59fb9ea379b50bc6309f4c2ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__453eef960d6646fabda0de26105466f31fa207043c77410a87bd48e2b2518677(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4ff8d7ea9bb4fc358c7bd64e17b6f51014840357cf6e324f5e74c7753e77d6b(
    value: typing.Optional[FunctionAppFlexConsumptionAuthSettingsGoogle],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98f2797aa67df612d5288813ab95d1c15223b7b4dbe09d4f8a09b0c5586f2c41(
    *,
    client_id: builtins.str,
    client_secret: typing.Optional[builtins.str] = None,
    client_secret_setting_name: typing.Optional[builtins.str] = None,
    oauth_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e63e8b841c7a34e76329ca7c49f2a77b54d7ad838b5586a618340d43c7ce10c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__135bd3c4e55942e8ab53c4b7e36de25ebb54c4f1e16702cb922d430242acbd26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c22080a72461f9a1f210842409de8d455b2e572412e976a172ca65006c74de59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe758c92fc41bd1de24bf364c6faeefb506f958b2bcdce5f8ea5f25e65e69c75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f46453a7bf6d2f3ac36f461612134db053354874205432b31cf597a40941178(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44f4dcd4892432840e6099387ee26acdd1a5d3be92180481224b2bd663ab7d15(
    value: typing.Optional[FunctionAppFlexConsumptionAuthSettingsMicrosoft],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e995ceb8548a695e0b4c0d2d1c5ac09614d61a6305135e54f695f65a1f85e5e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5c92207bc8a3bd7c44199d18b97f28f51e1c6068313a03502b1d93b4c325919(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1626c69318c117f27424bd324df5f1470ec98e26fa2fbd09ffc4892933920c4b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77752df7f71ee219849439584d5cb00d4290916db3af84415cbedafee297967d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5de1e4f08043f02b83115093b5499adce62e8e5da3f9c4f6b0291fd1ea10abcc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b25df2e1dc45b15a8c5cb15da1997cb4ad963ed9f5112f42146e7358464ffa29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9669d52682b32a7135fc4efb57bc61b4a5118b1de04562a2eccc97918d0d7fe7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aa01dee91374af0aca56b60b07f4200720c33922e6bbe491e1420f5147c2e06(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ffd9ae4971930028526b4419e825250a749a31e6572cef7127776b39527209e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fe34949bcc9e793d2537ea101c89dd79a204f98013722adc65270a08685343e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73bce6704887edc788c2317c30c696ce523e905379510ffafea1f6d7179c2c88(
    value: typing.Optional[FunctionAppFlexConsumptionAuthSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dacb4f234063a53547ec53cf68ff7e3971654da48aa2bd924fa83df696c3ce7(
    *,
    consumer_key: builtins.str,
    consumer_secret: typing.Optional[builtins.str] = None,
    consumer_secret_setting_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dae5c770be4f0d8794fe11f76066fcc4108cf2adbdb350f2e7cdd7178e9b4bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8687c9577386820c4da2cd5f55637458b87718975b4b592b7ab3b1bfd42d6f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f5c27fc84a41e5053fa40cd5faa61a9651f1c1cbbac03e86dedc2148cfd2d64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__712974a263b67e04ff13091a035aee3bdf10fed0a456cba2bbbda656a9912d70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__736d6c13225d1e8325aa49acee9fe70c11156b426d856884c733d019e854692d(
    value: typing.Optional[FunctionAppFlexConsumptionAuthSettingsTwitter],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d10ea96e07ddcf30e799b401ca2fd3cfd1045b0c9efb6bf4e9c77121dde39ef6(
    *,
    login: typing.Union[FunctionAppFlexConsumptionAuthSettingsV2Login, typing.Dict[builtins.str, typing.Any]],
    active_directory_v2: typing.Optional[typing.Union[FunctionAppFlexConsumptionAuthSettingsV2ActiveDirectoryV2, typing.Dict[builtins.str, typing.Any]]] = None,
    apple_v2: typing.Optional[typing.Union[FunctionAppFlexConsumptionAuthSettingsV2AppleV2, typing.Dict[builtins.str, typing.Any]]] = None,
    auth_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    azure_static_web_app_v2: typing.Optional[typing.Union[FunctionAppFlexConsumptionAuthSettingsV2AzureStaticWebAppV2, typing.Dict[builtins.str, typing.Any]]] = None,
    config_file_path: typing.Optional[builtins.str] = None,
    custom_oidc_v2: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionAppFlexConsumptionAuthSettingsV2CustomOidcV2, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_provider: typing.Optional[builtins.str] = None,
    excluded_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    facebook_v2: typing.Optional[typing.Union[FunctionAppFlexConsumptionAuthSettingsV2FacebookV2, typing.Dict[builtins.str, typing.Any]]] = None,
    forward_proxy_convention: typing.Optional[builtins.str] = None,
    forward_proxy_custom_host_header_name: typing.Optional[builtins.str] = None,
    forward_proxy_custom_scheme_header_name: typing.Optional[builtins.str] = None,
    github_v2: typing.Optional[typing.Union[FunctionAppFlexConsumptionAuthSettingsV2GithubV2, typing.Dict[builtins.str, typing.Any]]] = None,
    google_v2: typing.Optional[typing.Union[FunctionAppFlexConsumptionAuthSettingsV2GoogleV2, typing.Dict[builtins.str, typing.Any]]] = None,
    http_route_api_prefix: typing.Optional[builtins.str] = None,
    microsoft_v2: typing.Optional[typing.Union[FunctionAppFlexConsumptionAuthSettingsV2MicrosoftV2, typing.Dict[builtins.str, typing.Any]]] = None,
    require_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    require_https: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    runtime_version: typing.Optional[builtins.str] = None,
    twitter_v2: typing.Optional[typing.Union[FunctionAppFlexConsumptionAuthSettingsV2TwitterV2, typing.Dict[builtins.str, typing.Any]]] = None,
    unauthenticated_action: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c826ee12ce712e999382c1dd8274134e138ba026af083581c82e4791b5584d54(
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

def _typecheckingstub__300d5a5df6a79790a34261ceab61a4b3c550adfd6ba83cfd163216739f88f478(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c23210f2593d7a077812ffa48d46d9b2ce0c5e8e5462ebe5c3ae8f43076609(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb872bcd22f515e7deef8f5b78fca67797ea83501906814209a1ba7baf71f09c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb902f4664d37861d1814efc4d135d572ec752913fb348a3afdd59a58ea51ea(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__979908c313cf24f737bcbbf79fa7d38461638c85e2141f0279127bbd81abaf66(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79a8534c638ff44970e1c7bf82b722d4677823d7bab53554418c2d1540277c7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba8b797a2d172ed2d78c9f52ec5c8643a8ec62184ca561239609ad66bee4266f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__201005a874cfc6d471fc96ddae6963da3f8a3d52b189a93df71ead56a541ae56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e14fcf5dad259e5f96edd82c9af78bd1d07603c39a7c025a82cdea24e095069f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e3bc735f9423fe80977b27be5cbb87cd65e94adecda0e26d5be7dda383ebf1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe89416a082ce4a51812ee64293675faad57ee137343fd36a6ec246c79070382(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3fbda52e7ca32ac4e15bb14e650bb179a6b2275618f90d6c3d2a180807e6487(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5d07e647b6e672e5820b4a21c8bd3fdff1bc15ed279e31b5dc30d5d0fad0f2a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d5ddb1aaa7f29b07b3e237e8628767d6c6fa5621a91a532b23a907b44756e81(
    value: typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2ActiveDirectoryV2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7ac3bea0836b88b805792ef6ba6d70f63eacdcb4741fbeed4271eb140b3566c(
    *,
    client_id: builtins.str,
    client_secret_setting_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fa7850dd1d87da9bad3651bad9c4e1d7bc844d84e237fa3ae7116cfe8e7a69c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3af721cdbf3b4a9af2676bf5292ea616f89091410446d3d6cf1a9bbf944627e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f68219009a0cdfb81e106fdc8513484ec4a9bbbbb6a6783bf3022529543cfdd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d027f4ae24103f6c255ca75be1ac22c92678a4ae5e2c0dfa11015d120f6fad2(
    value: typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2AppleV2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__668c3cd99571cde538d3e11ec36734dd9e304386a0874b875364894493010983(
    *,
    client_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2db193d9dfd906f27d424c03c5de3f92c6cacbd85b896f5f97de65464524cf51(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ca903a9950c68484302618c7b63bd47c286b4972e393e501ba71f22772b3d4f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__257568059d2dc445f662669ca2aa5f7813b4684c88b288e0b805781cce292040(
    value: typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2AzureStaticWebAppV2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff5e9967f723ffaae30c4ebbd2ec9caf5dbccf98f95431b6b01a443d4ed86c4d(
    *,
    client_id: builtins.str,
    name: builtins.str,
    openid_configuration_endpoint: builtins.str,
    name_claim_type: typing.Optional[builtins.str] = None,
    scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e08a89fdca67dce8d931752c0a33125c2f08800823c8c6c4a3c669a96c279e18(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da1c0350ff5d5527a2a3f1a754f57ad4b7efe864d17f68362fd50db1e9d5d8e9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9443482c2b6dbffc37be5e75c4a63175576209b474bdf0ac311db7e90148e6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a10c07d9fd93314aa45973e1c4569c15b791ccb1c660d2c337563352ee0bc898(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5a5eb50b8777ccc2897fc2d95eef9263536cd34df49f4cf4081eb3a759621fa(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20721f9eace5797762aa4ec2d8c09dd37deeac1625b5350899bc32f6845ef76c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionAuthSettingsV2CustomOidcV2]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a87482d93961ab8a7f87d22b4c12ae51ae86ddb0b5f78558986f19ee76e02cbe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__755b9f1c003cdf56913dc9b1cd82cfa039c0f71e088fd1998406e97ca978ee60(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e68dbdb3b76fbeb6368abc9275b0f55a6b7c27bcd2817272bdde938bef12915(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ece868a521dd86c6b7876d15425cf6a700ce9b2a3c09806b6a8664d639c9246f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__240634ab896353e5810011aaeacc18d7e6ecd8075ab925ee4a993ce70ccd7413(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__785be99058a6fae38d52236f873309601082e744f128f459562f51fa45742029(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdf4bdf758f8ab441c634b4eafff9dca1833165e5ee17163986685eb5db75d3f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionAppFlexConsumptionAuthSettingsV2CustomOidcV2]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d16da4ea6bed4b4248197d312acfe2e1b8be3a6099b43e90d80bed5bfbeec3ad(
    *,
    app_id: builtins.str,
    app_secret_setting_name: builtins.str,
    graph_api_version: typing.Optional[builtins.str] = None,
    login_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a903db9c16055aea9286e22e00359c169a731ae93398f269522a8b999eaa639e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1912b624298a14f66f1294f51e5a3d156f224d260d02ab9ee51016ecb071430(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__921ca098c26fdc4866660980ebf992db277a10e74cd1f9673eb6b02efe1aeec2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b5b0c56aa409d003cb5460da84a9e8ea018da30c669c5314062cccce3f944d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__398c45e06d49ec3c0413acb4f942b769b04548b649746d0ff2db002ffde25396(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a39dd7d29655e118b857a1f989fcf161a28be0db8e2665e8de4915a592a7ba51(
    value: typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2FacebookV2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a25a58e0b6ac2f8cfdecc006790d5afbed1ceb57bc3bb20925b4fd79a16c9673(
    *,
    client_id: builtins.str,
    client_secret_setting_name: builtins.str,
    login_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb2b73585726a88a84602ec0bbed7700af474ed50676463088026231d7a1caeb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9daf1998f387fca1ac934b83101ffc0ff79c5550546e63b9a6abf3759af6f145(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a9d70f38570294405d4c3160f06c97363b3c82f54574c82ec33fbe26b828492(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7b2ce450b450ffe4be772e50fa226b1511b9332875d789c63b9394b4651881c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e073870ba5f1571c8bfc771ff4fbab69fb8caa4340fce6b7863cc54f447b661f(
    value: typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2GithubV2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec25a76e6fe6cd742576ae625df87dd6db025ceb7a18f3423a32a67897fa5efd(
    *,
    client_id: builtins.str,
    client_secret_setting_name: builtins.str,
    allowed_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
    login_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f151ace84960d61df4510b1b3839c053587b86b5b2b945009689aa54d3ee1f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39a2244df931e58b227dd11ad238fc723d0e8350e1f927ce1106429fc1b8b292(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abc946c0719433f1a1edb2d71282648b40ab54a7c9db6dbbc88d65e4f64f364b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1b58d725d6b9588cd9ed895a2ed8fb638d842b169968638e85a1fd8d1b78e8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78b5472a56e6234cd4e10d3d92125a9fb738d9e5b41f48fe9e10f93bbd7fc85a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16e1287ed0248165d0e1923c02a611eb1930451c6981702c9361381da109ead8(
    value: typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2GoogleV2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff5540f20938b5f316eae4f8834a2333116c441ab57aa3836d36e42b0a7cdbf8(
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

def _typecheckingstub__f3f91aa6bf8b64401e8b1a2f422c8c72503691afebf96bf6664c934e478a9467(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__832314f8872d59fd3a82d0706af0beb83d4d77812afa37608fa405adb4f81199(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3a2bf6bc4d663084e2972701e320cb6fcb6571433132697557dd54b789b3a06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87e27d0aede4f83252147d05819ea7af23065881f6d14ea656f4e58d781e64e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5adad561ff9cc2453294fed7f6f22a55a98865eff1969a70d965d99b3f81a49f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68d3ef0294ad411e2f6409d6b9accea13b75987bac515bf7a4ae77f70004f97a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d49cfa31482abe5cfe6573a633fd158c57d67793f03d38337f5f991aa6a651aa(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14728c9039fa2417a51c1f9b6a89c2fcaa0ed368383a46f92fe0966795458aac(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fa8cd67375ef5677380671b991de61b8973d2e0020d6a35c56df58bfcfa5a78(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3154fbd704fcfdb5409f617b1755ef83c62f2f0f195e651ac3e78244095a7fb1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cec48676a4405bfb1a47351373c1e10eb02dd569f331ce1d5e94797f88a132ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe36276213dfcc2c1d9d12fd322ce3154ec03cdaa429f931970b635e1a9c13f0(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08f673c6157b9d4dc944b8b3dd69709d3a5b83a3641b84f90ae6061a5af913bd(
    value: typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2Login],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5984875dba9d9f68bffe29890c351a6a991d3be4c3497fad1e700e79f267a38(
    *,
    client_id: builtins.str,
    client_secret_setting_name: builtins.str,
    allowed_audiences: typing.Optional[typing.Sequence[builtins.str]] = None,
    login_scopes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f292828ab598ef2675fc187061c2a1c4977aeae53288615bdf8111dabc32a66(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46f317d491fd0ce3a2033644ee5b6e6bc3712b1b7f0c2e5ace7e7153ce006623(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3410855493a46ef9087869c0ee961748f1be66517dc043d622a94c323d4ee879(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__691f0cba3ac700e59eba30f72d09279900d9dd8ac05c3d1cf95d328aa8d83136(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3874e74e0f6eb5a79e2d474d6b883a479a03cedfc54181d7fe88d321abc88446(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f9393097a15bd45fc75769708b7deb71492cc4733e970b1e60896a610c76b48(
    value: typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2MicrosoftV2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39de1ae26d108e6961fbf30c657648a4afc309bf5d0366eb34a6ad1c38aac52f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bd0fd50ad9b2c4941e5b967885dc4a2ca03a6ddc848357f656b0474f60c936f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionAppFlexConsumptionAuthSettingsV2CustomOidcV2, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a99d2196534586769b2d6790ae00c87788a6a1871124052134a93fb37271db31(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebd924b3ebf3cb5796288ccd73047a0b9aa16047ce392d1f3693d2fedde607ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba9b48b106474fe073f771537e80a80036076af17299346752e1cbc60d6e06ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a01a6198ce3f80d77032c2c24bc430018de2723b61b7c911238536bf7c7883e4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00dc971a323661e01dc275c1eb7210228e79dbd592d9a21ac874397382a0bac7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a5f3f71a0e1832b323d8bc0bb03af54ae87ee77ea2cb912837dad899b073d75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9a2f308fe65f4771707237a4c8671bdeadaa26415c42a548f0bb8df113ceea0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cd193fb8a89e0ce5a1f585e43c3b55a3e90b81bbbcb2360eeb302603ab9b42b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c32b38ff6c36abc806a1144f756da17eb753d31d267d0b7926db36e1858ac4ca(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26f22849e64164d85051cfd6e51c40469b457e615fbe65f582f804b2a6c24d48(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80af725b931875b7e862a25932dd3499a5f5083a3a694d9fa4cf1d798a149b80(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9941923f3e30544995042bc295db061ae2f0c328bca971165091c83377fb4a8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__483cce78b83fa5902105c5e29a0c8be8c5d9e5cf0e394c4d77a530aa8a5acf15(
    value: typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78e27d0e425e4d555553aa198e3437ec863ebb76c3e25c19938396352d4b965a(
    *,
    consumer_key: builtins.str,
    consumer_secret_setting_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffc621e52d7e0cb10d5e37fd08c373e67239073e35ecebed267bfaa3737a2726(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0c16c92fc29212ae543fdd9228dac5cf0bdd0afdea1ea60e58e3d18b6068a1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5fbc4546fb279221a970e4499e6580c86582e3ec27f7fb48be7786a533d9bd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2b55f6eed20705c7a0b4adba1875ce8d0dfbde64fb5fd252ee340c74e610f26(
    value: typing.Optional[FunctionAppFlexConsumptionAuthSettingsV2TwitterV2],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78260cdd889376ff3c639b042de0a356084932ff939e987769ed6b3a17eb80b1(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    runtime_name: builtins.str,
    runtime_version: builtins.str,
    service_plan_id: builtins.str,
    site_config: typing.Union[FunctionAppFlexConsumptionSiteConfig, typing.Dict[builtins.str, typing.Any]],
    storage_authentication_type: builtins.str,
    storage_container_endpoint: builtins.str,
    storage_container_type: builtins.str,
    always_ready: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionAppFlexConsumptionAlwaysReady, typing.Dict[builtins.str, typing.Any]]]]] = None,
    app_settings: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    auth_settings: typing.Optional[typing.Union[FunctionAppFlexConsumptionAuthSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    auth_settings_v2: typing.Optional[typing.Union[FunctionAppFlexConsumptionAuthSettingsV2, typing.Dict[builtins.str, typing.Any]]] = None,
    client_certificate_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    client_certificate_exclusion_paths: typing.Optional[builtins.str] = None,
    client_certificate_mode: typing.Optional[builtins.str] = None,
    connection_string: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionAppFlexConsumptionConnectionString, typing.Dict[builtins.str, typing.Any]]]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    https_only: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[FunctionAppFlexConsumptionIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    instance_memory_in_mb: typing.Optional[jsii.Number] = None,
    maximum_instance_count: typing.Optional[jsii.Number] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sticky_settings: typing.Optional[typing.Union[FunctionAppFlexConsumptionStickySettings, typing.Dict[builtins.str, typing.Any]]] = None,
    storage_access_key: typing.Optional[builtins.str] = None,
    storage_user_assigned_identity_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[FunctionAppFlexConsumptionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    virtual_network_subnet_id: typing.Optional[builtins.str] = None,
    webdeploy_publish_basic_authentication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    zip_deploy_file: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d00811589a6a329b77c5dc0cddc6de28e03c2bed3e769bb716afd51254a2c9f(
    *,
    name: builtins.str,
    type: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f995ecb07cdd4e153f173751d2dc0999319473ebb1e86c425673109cb1f207bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cb95f2d03bd6f1c63d930c64b2c3e9510f60184cd361bf4856c399567e95c51(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__729bd5e27af5f243f035cf3749811804ddc1071e2cf4ee59b3e9f48595777214(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e293bacb12205fb8fe375766c7b65097c9178b598f2ed3afec15426635e373a0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ce02a17cd8a65460eabff679512b408442dda65de7e87e00abcafb1caad027f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9df86762635cd19fc3af51bdf5d64652f9fa484b92cd87770433fdfaf82b4a9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionConnectionString]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58bc5d57a3a3b4b6093a8196fee1883cedb0830de811ede58e7b523d3d2d3397(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2b3e836b00d2a984b2b3e04b14d5125cab31b34147b2cc4f6e03603ce7b1b9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06ba450da7d5e868965871dc1b370fe1d23b816c56206b3b1e751f9aa868216e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9461fe4461ae425a53fd88f0510be1a5d95d04514b28da0c9286c45d9b573bf8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9a935a5c19e3dbd5a65d4d94132aa0df1bb44c29d5cba90588fcb7ccf7ee7dd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionAppFlexConsumptionConnectionString]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c38c6d84f8c80719fa4e2c1884a601b1774f9d5daa430cec0263aff1ba3a860(
    *,
    type: builtins.str,
    identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2bb52185d0407f4dce849967d84b2e5c4a12b662b2996e2e9bef8bf23d55354(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b196f8230d049ea16fa5d815d8e67cca61f332c5540a00aa5798830854383eb6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae155272c4f7bc5691ddee50f5afc43bb718d64e61f640d151ad6378ea4610ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80e57b53096d19b17630cacb429f83836b1e5e96009325e70ff6f0e9c51f995a(
    value: typing.Optional[FunctionAppFlexConsumptionIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87f0d599c5ba9c6ff9fe7c67da02e6153da4a1b4f4557f64d2075ae9ef1eb56c(
    *,
    api_definition_url: typing.Optional[builtins.str] = None,
    api_management_api_id: typing.Optional[builtins.str] = None,
    app_command_line: typing.Optional[builtins.str] = None,
    application_insights_connection_string: typing.Optional[builtins.str] = None,
    application_insights_key: typing.Optional[builtins.str] = None,
    app_service_logs: typing.Optional[typing.Union[FunctionAppFlexConsumptionSiteConfigAppServiceLogs, typing.Dict[builtins.str, typing.Any]]] = None,
    container_registry_managed_identity_client_id: typing.Optional[builtins.str] = None,
    container_registry_use_managed_identity: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    cors: typing.Optional[typing.Union[FunctionAppFlexConsumptionSiteConfigCors, typing.Dict[builtins.str, typing.Any]]] = None,
    default_documents: typing.Optional[typing.Sequence[builtins.str]] = None,
    elastic_instance_minimum: typing.Optional[jsii.Number] = None,
    health_check_eviction_time_in_min: typing.Optional[jsii.Number] = None,
    health_check_path: typing.Optional[builtins.str] = None,
    http2_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ip_restriction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionAppFlexConsumptionSiteConfigIpRestriction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ip_restriction_default_action: typing.Optional[builtins.str] = None,
    load_balancing_mode: typing.Optional[builtins.str] = None,
    managed_pipeline_mode: typing.Optional[builtins.str] = None,
    minimum_tls_version: typing.Optional[builtins.str] = None,
    remote_debugging_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    remote_debugging_version: typing.Optional[builtins.str] = None,
    runtime_scale_monitoring_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    scm_ip_restriction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionAppFlexConsumptionSiteConfigScmIpRestriction, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__e1b291dafcb6caacce4d4fc2a5dedd916fe8c31404ced4bbcdb106f9ba3851d3(
    *,
    disk_quota_mb: typing.Optional[jsii.Number] = None,
    retention_period_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af0d04f8553e02834f668597ddd64fb7705222dc28918bd92cbd4fddc3228e57(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a815a991b1f468e4080d848b11b97b5fda2d272321058c10cc84a222b5b74ba(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e36eaff4b2ab7898b91d78f63b53a9af04a0ff82923f1505399d97949faa6f4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66c4df363c2db8c73adc2c73eab811e54537cb0fd64615f3b79790b885209b3e(
    value: typing.Optional[FunctionAppFlexConsumptionSiteConfigAppServiceLogs],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67d65cbb36cc86f8eb47dc6da3bb4c1b34a873ab66937f39813a4df2cee69554(
    *,
    allowed_origins: typing.Optional[typing.Sequence[builtins.str]] = None,
    support_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c31bdc84bc11d87299761a699767e8053aa33a0906f29943e776acc6f8e7eeb6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__917aebede5de6d61cb050eec6f9f61d6819067df40f20775db16856e8123ac61(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4afea39c1f3ef9a86ceffe0f49d87e138c46e0a60b24ceadb20b863e3bf7a658(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fb6ad7517fba4a9b0f1b2f1261e735892189d7f6e57142434df1011eb0ef46f(
    value: typing.Optional[FunctionAppFlexConsumptionSiteConfigCors],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28c4176aef5f3ee89da611fe480ed39d783467f20aff0e4348a7fd56cda75cec(
    *,
    action: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionAppFlexConsumptionSiteConfigIpRestrictionHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ip_address: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    service_tag: typing.Optional[builtins.str] = None,
    virtual_network_subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ea77a56a27dbc98c1072047570fc30bebd2c15dc1a112abcdf93e05a6bcbcb9(
    *,
    x_azure_fdid: typing.Optional[typing.Sequence[builtins.str]] = None,
    x_fd_health_probe: typing.Optional[typing.Sequence[builtins.str]] = None,
    x_forwarded_for: typing.Optional[typing.Sequence[builtins.str]] = None,
    x_forwarded_host: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea5e60d3c1c62a14fd42499c4b8c19de3b7f318f61469984b77c759195c3d407(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f2470ca62cc4de284c0a1806b7636853da1d8ee89046dcee9039e304cf37f09(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41f43556c68de36926ff10394fb9cc1597fc9a788fb9bad62fa070ecb903dbf4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a29cb8d1a0629dc2b99bae022b6c9bcd09aba10017d70363010b13f46550d12(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f397c3529cf7683f59d5d972bd809526b6d78dd7e0ab7c71e7189dd5e1862827(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b4d97e4345a346fc4783d0d0d139f171b886685eecef991e83d3ed15edec6cf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionSiteConfigIpRestrictionHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4c6752a057affccdf984aac218535153eec53349771f82663c22e854cf043d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab8980bb61e73043020f59b1b02bffac726a29e9d9c58afdc91c6f180ae57a3e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a0b1c61d58e0991b2016b24859759c8f2a2249fc97fa8ba4172226ae75f15f0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f947133e9ba50e52b96d5c7a7b703b000e0a68770a5609a0ee06ea2593291fe(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__627b4a0e31aa482a3e8cd2ca838fb8f2ea76b3f25cb2005bc4a6a7510c57c72b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__349d20a5516a0fdd701646a4cfcc97893e5741fa5763c306fcfecbce24a292e5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionAppFlexConsumptionSiteConfigIpRestrictionHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__423fd6af292cf874eb6c7ab1699aa92ea0c16c51fac1393e99247fda47a115f7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1de06de7794fc9e6f8668a92ae8f5cfdf15dc9f56c07fd1f98ccbe9494090ea7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e67e3c714b0537ce40080af931bd9da9ba1f30dbbb77717afc2051ede48dcda6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10f5c6e7d01cee8a204e1284156fb7d2ce79ad088502404b1f45220932370490(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbf31618b3e85e28efaae7a389dff148867e64b01a393ad053b2d74635d6eabe(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fda29fba2f44d7eadc5ee2e4053178d03e1d8bdcdeffd6a4fe03a2508bf0a52(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionSiteConfigIpRestriction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2328ba40c20c2a45eedb18ed81afa086d1a90a55fefcc1b401030f1eecb254f6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efd93cc6dacf4ddd38cc723c634b7fd37bff320f7dff67a6261575545a99bc8f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionAppFlexConsumptionSiteConfigIpRestrictionHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed947c1ca290b798e73e766e3b0f0bee75c75a65552b12429f87335cf5b78534(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d10a4093db40e74f4d58fccf3deebc502bf67736e846d53b85949334dc9af91f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8eec6051b80ce842097735a05c9a1e29ba9469da8a92e44f3208fd5f49c4150(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07a39a8c95143d4e49582c018b19814f82fc5b7ff7e17b8fe8171423a02f282a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff98b345fe575aec06b373a579890691a046eb7d3f2a9d7afecdc49834720fe7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__242d6ee0b075ea956d671d729f2015fff2ac4d0e8820c7d7fe921be6a5a4afe1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__807410df19125b035cd79791133d1f261a58d69457d410e0babccf9eca37246d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e8f79901b3f799a7a631197fc679a4ff2ad774fbd7a46fa52952ae9fbe489a3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionAppFlexConsumptionSiteConfigIpRestriction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e26c5696247970496ae602cb62817aff815e2c35942094ed1f75433ccbc6b3b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd45ea738c064a8bf9620c4331fa5b0bbcedda0ae3f8151e1bfa79113ddbeb0e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionAppFlexConsumptionSiteConfigIpRestriction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2227865ff2c165fdf35a8dda9d587b653762369133fc2896b6314d81d7658355(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionAppFlexConsumptionSiteConfigScmIpRestriction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8a9be2bdd279cbd634a62d2126429071ce8e99f43da99fbe2a02ba71ff025db(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__190623a678bad8ccd9eab00d7de09fb5172af7e4a393a1059ac9452fa0a853e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c4dbc67e36c054659d91e7cd83798797df09cab12dda7b506333d9875188bc3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c32bb8c511ee54f415bfca2783e74ea9ec05d882325ccac676ee03d4b4a8744(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78dc8b0657d3785bd3195ca676afe090855ee92a80478c1c7f2574f5bf2ad195(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edc48f505422d342c89d268014c94ee27f49deef99dcd792f79a85a3f0708595(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81b9575782f25a77726ad8078397094991f0e75a9592452f1a4b9cd9defe6f6a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b91abd55fa648adcf48409b0d85e9ff120645b7653ef5a0568c10569ffcb6f17(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23ad110787d2fa7ceaadbe08decd2c9de8631fd684757ea976d06014370d25bc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aff25b0eeb6aa7c289858594a1c5d21f1816fa5cd968717c28137b64b41d6fd0(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd4415a7e6f3d27cd303490c477cc8bc1697ec1866c6047fa629f8d81cbb684a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__478620669f856375f8a9bd13634b1ab2f5a66af18cfedadc2b128757a781783b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f29935c9ed4b05fd0f8412dde7345dd162e812fb24dbd024796826e99b509511(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__348e4ed1a4e1246b018b296733f67ab957afac2b01dd1542f821024b602b0f30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d66ebfbf603e9e97c102459187ddc03ff19d30608ec07ff4868efdc867619a2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__601639ac7c1d3b63325daeb21e4ef2136eae693da412c2a098388fcc39bf433f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60f2a76533c17d428af81929bbddb79736045492c67ec7276bc642e7be60063e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__769acac630bb03cf9960f0d91786e90b09f6fd9633bad6bf1478796c0e2750fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16cc3d2b95b8cee30a756399448dc70ba2b3c34913066202354f843a1831fb0c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e37dc4921df6380ac11a265bdfd7979862074a46a4dc8748dd85faaab2638d1f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__912688703a61d9a9f3097be0662abb5d29204e52ef15cfc7f1aaca66f2a1b30d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__237839eb4a4a4c9f506611a521fa6b9804d2966ce1574c70860ee175d7c5b52a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac533d41d676be5c0a694da929c5ec13d8001735ddd8ddda20a7d522b53aa40b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e88a6ca0db1d0563697fecbacf81cb8cecbf0d7f87e5d8bc4d1e3006d8a5f2b2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1ea93f62292d95b38809b72849443c5fe2f155ad1df6af7b3804236b9f2c3d6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a47bfa7f76c113a5da0ded5b7ed0df569ed82f3b64dcfd2ba0717ba9076c3a9(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddb85ac225eea55d1577e6e719483b9c6ea414c128bb7180f1f2bd590d9f5f5d(
    value: typing.Optional[FunctionAppFlexConsumptionSiteConfig],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06b8b644e276a07b2ecd045a37dbf9f06917b90825604a458780ad2028108912(
    *,
    action: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    headers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionAppFlexConsumptionSiteConfigScmIpRestrictionHeaders, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ip_address: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    service_tag: typing.Optional[builtins.str] = None,
    virtual_network_subnet_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3458f39701815ec143c3630e0149960fc4e9e8b9fcb8be1737519fbc865dc4f1(
    *,
    x_azure_fdid: typing.Optional[typing.Sequence[builtins.str]] = None,
    x_fd_health_probe: typing.Optional[typing.Sequence[builtins.str]] = None,
    x_forwarded_for: typing.Optional[typing.Sequence[builtins.str]] = None,
    x_forwarded_host: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e39b9fe7c0c6ddaf5be194b5399e5e9d68cdb57682f6265dcdd0ae117205ce0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab05d39ca210ad75cf7a730a329b7c2a787b737bd6585bfc262f9d5fe62cf0fa(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__844e692acd612011ffc76b377c4ef56a4f16ccdec9395dc838e4017ee5cd2291(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ef6903842315a8a72715b083e45354e1fdcac5e06a46fb9738eb1ec977f8a6f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e4400f30b515e4f13914829f599e713c7307fe4d31853dfa10e2d4fe05635ef(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7121b9896c1888ed5d4362cfcb70a2437bb527325b8f802c3c6db0eddf5831ba(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionSiteConfigScmIpRestrictionHeaders]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__026e5112bd91b5c5efeec1711e1714e3e4c58e44627c2fc8710f7e2e9903f457(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef214e66b29fcada8ab8f2b2d3ce5052354b5d101d429333e15e6c32443a6ced(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a7efbef0b5207f8b3881a5420f4eff12e5a6d6f77f26a9bf2bfc2a6bb7b8c0a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02f5be37947ec9bef2e84686b728ba31ea445cec73757783ae68d99e1eefdba3(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c84659c6cf1c78248bcb1f4e9d1df7516954ec88aa3b379bc4019ffd6ffac9f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6e38440f1e8ca884fbce12feeb861a01ec87d90ec590d03d710c7eadab169bc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionAppFlexConsumptionSiteConfigScmIpRestrictionHeaders]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b3380f7e3258aafe432e96cbdccee20b82264474901b4411dea0925c3fdb9db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e1c42392302e4e0cce9aa492ed4d23e52826b04d5ddbff1283572e3fae20f47(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__058b19b5f0dcee8e97d298f5cdf193ce4ec8ef2ccfcf433f8f735e82c79c5a22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6056d7fd096b71a707d6cbc203dc925e30652f86129520c83222bb508fd7d2b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b492054db77fccae5a6a33c7b3162efdfaa68c85802b4b7ca024979236b12b6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ded63078bce796ceb37f59e05411feda4cc6208b9a09d0b06e9e268fb16c536(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[FunctionAppFlexConsumptionSiteConfigScmIpRestriction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9054c6247b79c09714ad0f183da8c9392f2482f978b22f023cde2ae512dcfe10(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fd125ff50abdc7504482c0a85caaa8891d5db31e8d007018d708e1d6a965c14(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[FunctionAppFlexConsumptionSiteConfigScmIpRestrictionHeaders, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc4e8a0faaa8936c9a11522089153f52b8a83f509f27d3fe19f60f650d1e5412(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c599d9918b15ceea4ca7f1f498efe536f8f4856a316c53a3be037774b6ae8e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25f546e2af34a3b6a2c36b4147fe8517e1f2d848a2455436c34dda515e02e3af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86badbb3ad87dc0f74e65c0ce40025bc0c96898a4f89226ab93ab97d708b5765(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1963be73330cd1ec4eba2ea753aa3131ff1d3bdfc0e1e2c2e843866a7c72fe70(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c87813d2f375e927adba996302e337783cc6eacbdcb59acd922978eab159248(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e15deb627f572da94df0f18489755b07edd016e142f212e9008f7826382891d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad5ac1086df13eceb1ec9443aac3cb84c1a4ad0bd4dd81a35d5cc67079b8c62b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionAppFlexConsumptionSiteConfigScmIpRestriction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa904b3ff3b6a0e12b9b85a4eee5e716c53cc822bf61baa08c171ad79103ec15(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34f90608e3b2b6574477139a546a80e8bd0bdd66dafe1d18048d9e196d39ebeb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79aa49e33282b56c9d5e479fa097dd9c8986baef7ea1bfc66660d070cd75505d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3c2bb9d8fb089e0214f425303a55ca0c583161c6879bc38741e0aaa4a257cc4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84b6af6e161ce5be4ae6e9a34a4c8a164ce2179c57d39ef37dacff88a67007b5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a5d856412c6d9191b0f82a70c24813706b003964367be24b92374675ede8ced(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fe4efc32501b801641e52f7f4328935f6c083bfc1c15542cb9d488b7bfcf754(
    value: typing.Optional[FunctionAppFlexConsumptionSiteCredential],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79317e5333bcc7f18255fa5eee6b64fa5f94e7fedb9366c365d37cc0040e577e(
    *,
    app_setting_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    connection_string_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23dcf202085a8bc0642667f3c3554f8716048b9e24f9f34f59593d611c26311f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e6c8498e124fe925b7142331717328c531f9abb8bedbf3fc2c18514da9dcadb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c44b975efdf5349fe1607081fcd8e963f8bc524946660c5740819f1956ad421f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f223a672fa694fd5a67d1d1145d61d3b4d09e281b74a38654584121a2265aa56(
    value: typing.Optional[FunctionAppFlexConsumptionStickySettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfd8edd64cb7b77d5bc7a9c73c1f28f97d8198c92e6dbee354c9b407f192bb03(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e882123d564a3e6f5c852899e4c6f41f3f28aa20370e6c2dc9302a3d89feb21(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9975464084fc5e816336d27b3abf3af5b575ed64a19a215054c6ab211d96fbcd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31a6b571b5649454a323cd37adfbaaa9f80619e9422cd23d678f8464c566b942(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aba6e6325d954f88b7f8cd4bf8d8d3b11d8aa8693d42d8220612fbd39a7a8e31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80dab1f23c78879f2845a1ae1d70abdfd7eadaea80ee1c1b4d3271ac3ac55804(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a001c557bd0bc935756daabc859ef6035cb7d8ba6bd9a2c0b14ecddc81847ba5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, FunctionAppFlexConsumptionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
