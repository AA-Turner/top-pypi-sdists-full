r'''
# `azurerm_bot_service_azure_bot`

Refer to the Terraform Registry for docs: [`azurerm_bot_service_azure_bot`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot).
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


class BotServiceAzureBot(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.botServiceAzureBot.BotServiceAzureBot",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot azurerm_bot_service_azure_bot}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        microsoft_app_id: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        sku: builtins.str,
        cmk_key_vault_key_url: typing.Optional[builtins.str] = None,
        developer_app_insights_api_key: typing.Optional[builtins.str] = None,
        developer_app_insights_application_id: typing.Optional[builtins.str] = None,
        developer_app_insights_key: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        endpoint: typing.Optional[builtins.str] = None,
        icon_url: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        local_authentication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        luis_app_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        luis_key: typing.Optional[builtins.str] = None,
        microsoft_app_msi_id: typing.Optional[builtins.str] = None,
        microsoft_app_tenant_id: typing.Optional[builtins.str] = None,
        microsoft_app_type: typing.Optional[builtins.str] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        streaming_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["BotServiceAzureBotTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot azurerm_bot_service_azure_bot} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#location BotServiceAzureBot#location}.
        :param microsoft_app_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#microsoft_app_id BotServiceAzureBot#microsoft_app_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#name BotServiceAzureBot#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#resource_group_name BotServiceAzureBot#resource_group_name}.
        :param sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#sku BotServiceAzureBot#sku}.
        :param cmk_key_vault_key_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#cmk_key_vault_key_url BotServiceAzureBot#cmk_key_vault_key_url}.
        :param developer_app_insights_api_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#developer_app_insights_api_key BotServiceAzureBot#developer_app_insights_api_key}.
        :param developer_app_insights_application_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#developer_app_insights_application_id BotServiceAzureBot#developer_app_insights_application_id}.
        :param developer_app_insights_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#developer_app_insights_key BotServiceAzureBot#developer_app_insights_key}.
        :param display_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#display_name BotServiceAzureBot#display_name}.
        :param endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#endpoint BotServiceAzureBot#endpoint}.
        :param icon_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#icon_url BotServiceAzureBot#icon_url}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#id BotServiceAzureBot#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param local_authentication_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#local_authentication_enabled BotServiceAzureBot#local_authentication_enabled}.
        :param luis_app_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#luis_app_ids BotServiceAzureBot#luis_app_ids}.
        :param luis_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#luis_key BotServiceAzureBot#luis_key}.
        :param microsoft_app_msi_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#microsoft_app_msi_id BotServiceAzureBot#microsoft_app_msi_id}.
        :param microsoft_app_tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#microsoft_app_tenant_id BotServiceAzureBot#microsoft_app_tenant_id}.
        :param microsoft_app_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#microsoft_app_type BotServiceAzureBot#microsoft_app_type}.
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#public_network_access_enabled BotServiceAzureBot#public_network_access_enabled}.
        :param streaming_endpoint_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#streaming_endpoint_enabled BotServiceAzureBot#streaming_endpoint_enabled}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#tags BotServiceAzureBot#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#timeouts BotServiceAzureBot#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7b74227bf59fdf6efc172ada372089541b9f8dbff0b55bf7c5500e175f14cf2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = BotServiceAzureBotConfig(
            location=location,
            microsoft_app_id=microsoft_app_id,
            name=name,
            resource_group_name=resource_group_name,
            sku=sku,
            cmk_key_vault_key_url=cmk_key_vault_key_url,
            developer_app_insights_api_key=developer_app_insights_api_key,
            developer_app_insights_application_id=developer_app_insights_application_id,
            developer_app_insights_key=developer_app_insights_key,
            display_name=display_name,
            endpoint=endpoint,
            icon_url=icon_url,
            id=id,
            local_authentication_enabled=local_authentication_enabled,
            luis_app_ids=luis_app_ids,
            luis_key=luis_key,
            microsoft_app_msi_id=microsoft_app_msi_id,
            microsoft_app_tenant_id=microsoft_app_tenant_id,
            microsoft_app_type=microsoft_app_type,
            public_network_access_enabled=public_network_access_enabled,
            streaming_endpoint_enabled=streaming_endpoint_enabled,
            tags=tags,
            timeouts=timeouts,
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
        '''Generates CDKTF code for importing a BotServiceAzureBot resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the BotServiceAzureBot to import.
        :param import_from_id: The id of the existing BotServiceAzureBot that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the BotServiceAzureBot to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2234ab1c543d280a1647c69b48b76117b78305ed055d46c13d292b870545fa63)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#create BotServiceAzureBot#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#delete BotServiceAzureBot#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#read BotServiceAzureBot#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#update BotServiceAzureBot#update}.
        '''
        value = BotServiceAzureBotTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCmkKeyVaultKeyUrl")
    def reset_cmk_key_vault_key_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCmkKeyVaultKeyUrl", []))

    @jsii.member(jsii_name="resetDeveloperAppInsightsApiKey")
    def reset_developer_app_insights_api_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeveloperAppInsightsApiKey", []))

    @jsii.member(jsii_name="resetDeveloperAppInsightsApplicationId")
    def reset_developer_app_insights_application_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeveloperAppInsightsApplicationId", []))

    @jsii.member(jsii_name="resetDeveloperAppInsightsKey")
    def reset_developer_app_insights_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeveloperAppInsightsKey", []))

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetEndpoint")
    def reset_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpoint", []))

    @jsii.member(jsii_name="resetIconUrl")
    def reset_icon_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIconUrl", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLocalAuthenticationEnabled")
    def reset_local_authentication_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocalAuthenticationEnabled", []))

    @jsii.member(jsii_name="resetLuisAppIds")
    def reset_luis_app_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLuisAppIds", []))

    @jsii.member(jsii_name="resetLuisKey")
    def reset_luis_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLuisKey", []))

    @jsii.member(jsii_name="resetMicrosoftAppMsiId")
    def reset_microsoft_app_msi_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMicrosoftAppMsiId", []))

    @jsii.member(jsii_name="resetMicrosoftAppTenantId")
    def reset_microsoft_app_tenant_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMicrosoftAppTenantId", []))

    @jsii.member(jsii_name="resetMicrosoftAppType")
    def reset_microsoft_app_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMicrosoftAppType", []))

    @jsii.member(jsii_name="resetPublicNetworkAccessEnabled")
    def reset_public_network_access_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicNetworkAccessEnabled", []))

    @jsii.member(jsii_name="resetStreamingEndpointEnabled")
    def reset_streaming_endpoint_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStreamingEndpointEnabled", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

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
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "BotServiceAzureBotTimeoutsOutputReference":
        return typing.cast("BotServiceAzureBotTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="cmkKeyVaultKeyUrlInput")
    def cmk_key_vault_key_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cmkKeyVaultKeyUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="developerAppInsightsApiKeyInput")
    def developer_app_insights_api_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "developerAppInsightsApiKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="developerAppInsightsApplicationIdInput")
    def developer_app_insights_application_id_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "developerAppInsightsApplicationIdInput"))

    @builtins.property
    @jsii.member(jsii_name="developerAppInsightsKeyInput")
    def developer_app_insights_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "developerAppInsightsKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointInput")
    def endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endpointInput"))

    @builtins.property
    @jsii.member(jsii_name="iconUrlInput")
    def icon_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iconUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="localAuthenticationEnabledInput")
    def local_authentication_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "localAuthenticationEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="luisAppIdsInput")
    def luis_app_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "luisAppIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="luisKeyInput")
    def luis_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "luisKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="microsoftAppIdInput")
    def microsoft_app_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "microsoftAppIdInput"))

    @builtins.property
    @jsii.member(jsii_name="microsoftAppMsiIdInput")
    def microsoft_app_msi_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "microsoftAppMsiIdInput"))

    @builtins.property
    @jsii.member(jsii_name="microsoftAppTenantIdInput")
    def microsoft_app_tenant_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "microsoftAppTenantIdInput"))

    @builtins.property
    @jsii.member(jsii_name="microsoftAppTypeInput")
    def microsoft_app_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "microsoftAppTypeInput"))

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
    @jsii.member(jsii_name="skuInput")
    def sku_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "skuInput"))

    @builtins.property
    @jsii.member(jsii_name="streamingEndpointEnabledInput")
    def streaming_endpoint_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "streamingEndpointEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BotServiceAzureBotTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "BotServiceAzureBotTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="cmkKeyVaultKeyUrl")
    def cmk_key_vault_key_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cmkKeyVaultKeyUrl"))

    @cmk_key_vault_key_url.setter
    def cmk_key_vault_key_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a2d2b980569795d04ef222269ab01bf6d1b41f37500172272e0d347220308f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cmkKeyVaultKeyUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="developerAppInsightsApiKey")
    def developer_app_insights_api_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "developerAppInsightsApiKey"))

    @developer_app_insights_api_key.setter
    def developer_app_insights_api_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b5ba9670c1e2d5429dbc6b05a9278fda2ddc829e9b246eb393d3efa843c027a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "developerAppInsightsApiKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="developerAppInsightsApplicationId")
    def developer_app_insights_application_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "developerAppInsightsApplicationId"))

    @developer_app_insights_application_id.setter
    def developer_app_insights_application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfafb58a55cb8b5213cd67ccd7a174b21c2675c5574985cbefdb9a1bee432f35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "developerAppInsightsApplicationId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="developerAppInsightsKey")
    def developer_app_insights_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "developerAppInsightsKey"))

    @developer_app_insights_key.setter
    def developer_app_insights_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04685cfeff3e7abd5abcbb139e4062dd5db225b8de2261921d20d57a011d571e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "developerAppInsightsKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ebe5320c8758b2a310074fe3e7cc9dbfb7b8dcaaa1546e0f9090b8f439bf6a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @endpoint.setter
    def endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__256aa4c51ee72388dd8d4f7d0f1274714d0cdb265be9445f21a040b6b644426f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpoint", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iconUrl")
    def icon_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "iconUrl"))

    @icon_url.setter
    def icon_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__723db323714cf70e3b307aab92b097a92e555e9d558b430ec5357fe603b0c55e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iconUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__371c71ff75e188b1de86fd32da898def337a8e8ea45019669ab276aec68debdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="localAuthenticationEnabled")
    def local_authentication_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "localAuthenticationEnabled"))

    @local_authentication_enabled.setter
    def local_authentication_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74acd3fd458498f5e7c1e4d84353fb8081193738d4a3d3b7d2e87371e0b069b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "localAuthenticationEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b88355fb1049489f6e446fe454f925da0b28a51bea7dc42b88a5639b4aa1dc8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="luisAppIds")
    def luis_app_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "luisAppIds"))

    @luis_app_ids.setter
    def luis_app_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb5abc2345d84c1723ab6da41187c1fa8adc5d3673ef96654aaf02de9c2f80bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "luisAppIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="luisKey")
    def luis_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "luisKey"))

    @luis_key.setter
    def luis_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83e59290cd893aea6c0ebc890de679372f6a7dfbc0d59dea6e62e3a86f833605)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "luisKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="microsoftAppId")
    def microsoft_app_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "microsoftAppId"))

    @microsoft_app_id.setter
    def microsoft_app_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e5a96ebf9ed66a112cd225e4bff756c988b486a1b2864ad5ec2e2fa96114e8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "microsoftAppId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="microsoftAppMsiId")
    def microsoft_app_msi_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "microsoftAppMsiId"))

    @microsoft_app_msi_id.setter
    def microsoft_app_msi_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dc63506818e67ad252bc604eb16324f300adb02e3ed764f56419a715d3ac8e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "microsoftAppMsiId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="microsoftAppTenantId")
    def microsoft_app_tenant_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "microsoftAppTenantId"))

    @microsoft_app_tenant_id.setter
    def microsoft_app_tenant_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fab8fa1c83aabc3c52c07865334ea153438815a043a5952b39ed465715dbb2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "microsoftAppTenantId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="microsoftAppType")
    def microsoft_app_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "microsoftAppType"))

    @microsoft_app_type.setter
    def microsoft_app_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f76bbb6e8f68893e0d29d8098d7d1bf76b2b3db858748af639caa1906779897f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "microsoftAppType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a8cd8d9b3f7776726b593a5fd9140249bada1a172642557c42ea8d5efc09c29)
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
            type_hints = typing.get_type_hints(_typecheckingstub__78a6efb7c2bb9b3ae12b5adce9eec73e8820e0f6ac75d63b879d977d67dc2165)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicNetworkAccessEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11163f3d32381f553aafaf4156d82ff1a97c8d4dba42218e71a68485b6703d00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sku")
    def sku(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sku"))

    @sku.setter
    def sku(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b79b03ab105ed6c3993b2f025a7de7b72bfd26a46085cead60582fbf827fbd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sku", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="streamingEndpointEnabled")
    def streaming_endpoint_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "streamingEndpointEnabled"))

    @streaming_endpoint_enabled.setter
    def streaming_endpoint_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f02a7f57533fe3a4d2cca9e85e1eeba36a90e4e2e6dbc88db0b2032b31abf90)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streamingEndpointEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95b2fec24ffd35a995bff5473c74b1b9f9189caab758884cbd79e6f84a184904)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.botServiceAzureBot.BotServiceAzureBotConfig",
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
        "microsoft_app_id": "microsoftAppId",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "sku": "sku",
        "cmk_key_vault_key_url": "cmkKeyVaultKeyUrl",
        "developer_app_insights_api_key": "developerAppInsightsApiKey",
        "developer_app_insights_application_id": "developerAppInsightsApplicationId",
        "developer_app_insights_key": "developerAppInsightsKey",
        "display_name": "displayName",
        "endpoint": "endpoint",
        "icon_url": "iconUrl",
        "id": "id",
        "local_authentication_enabled": "localAuthenticationEnabled",
        "luis_app_ids": "luisAppIds",
        "luis_key": "luisKey",
        "microsoft_app_msi_id": "microsoftAppMsiId",
        "microsoft_app_tenant_id": "microsoftAppTenantId",
        "microsoft_app_type": "microsoftAppType",
        "public_network_access_enabled": "publicNetworkAccessEnabled",
        "streaming_endpoint_enabled": "streamingEndpointEnabled",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class BotServiceAzureBotConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        microsoft_app_id: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        sku: builtins.str,
        cmk_key_vault_key_url: typing.Optional[builtins.str] = None,
        developer_app_insights_api_key: typing.Optional[builtins.str] = None,
        developer_app_insights_application_id: typing.Optional[builtins.str] = None,
        developer_app_insights_key: typing.Optional[builtins.str] = None,
        display_name: typing.Optional[builtins.str] = None,
        endpoint: typing.Optional[builtins.str] = None,
        icon_url: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        local_authentication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        luis_app_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        luis_key: typing.Optional[builtins.str] = None,
        microsoft_app_msi_id: typing.Optional[builtins.str] = None,
        microsoft_app_tenant_id: typing.Optional[builtins.str] = None,
        microsoft_app_type: typing.Optional[builtins.str] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        streaming_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["BotServiceAzureBotTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#location BotServiceAzureBot#location}.
        :param microsoft_app_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#microsoft_app_id BotServiceAzureBot#microsoft_app_id}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#name BotServiceAzureBot#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#resource_group_name BotServiceAzureBot#resource_group_name}.
        :param sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#sku BotServiceAzureBot#sku}.
        :param cmk_key_vault_key_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#cmk_key_vault_key_url BotServiceAzureBot#cmk_key_vault_key_url}.
        :param developer_app_insights_api_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#developer_app_insights_api_key BotServiceAzureBot#developer_app_insights_api_key}.
        :param developer_app_insights_application_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#developer_app_insights_application_id BotServiceAzureBot#developer_app_insights_application_id}.
        :param developer_app_insights_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#developer_app_insights_key BotServiceAzureBot#developer_app_insights_key}.
        :param display_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#display_name BotServiceAzureBot#display_name}.
        :param endpoint: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#endpoint BotServiceAzureBot#endpoint}.
        :param icon_url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#icon_url BotServiceAzureBot#icon_url}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#id BotServiceAzureBot#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param local_authentication_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#local_authentication_enabled BotServiceAzureBot#local_authentication_enabled}.
        :param luis_app_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#luis_app_ids BotServiceAzureBot#luis_app_ids}.
        :param luis_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#luis_key BotServiceAzureBot#luis_key}.
        :param microsoft_app_msi_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#microsoft_app_msi_id BotServiceAzureBot#microsoft_app_msi_id}.
        :param microsoft_app_tenant_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#microsoft_app_tenant_id BotServiceAzureBot#microsoft_app_tenant_id}.
        :param microsoft_app_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#microsoft_app_type BotServiceAzureBot#microsoft_app_type}.
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#public_network_access_enabled BotServiceAzureBot#public_network_access_enabled}.
        :param streaming_endpoint_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#streaming_endpoint_enabled BotServiceAzureBot#streaming_endpoint_enabled}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#tags BotServiceAzureBot#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#timeouts BotServiceAzureBot#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = BotServiceAzureBotTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a48b498e926ed8833398bd7ddd413a755796745379894c82b889aa0dfe39879)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument microsoft_app_id", value=microsoft_app_id, expected_type=type_hints["microsoft_app_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument sku", value=sku, expected_type=type_hints["sku"])
            check_type(argname="argument cmk_key_vault_key_url", value=cmk_key_vault_key_url, expected_type=type_hints["cmk_key_vault_key_url"])
            check_type(argname="argument developer_app_insights_api_key", value=developer_app_insights_api_key, expected_type=type_hints["developer_app_insights_api_key"])
            check_type(argname="argument developer_app_insights_application_id", value=developer_app_insights_application_id, expected_type=type_hints["developer_app_insights_application_id"])
            check_type(argname="argument developer_app_insights_key", value=developer_app_insights_key, expected_type=type_hints["developer_app_insights_key"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            check_type(argname="argument icon_url", value=icon_url, expected_type=type_hints["icon_url"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument local_authentication_enabled", value=local_authentication_enabled, expected_type=type_hints["local_authentication_enabled"])
            check_type(argname="argument luis_app_ids", value=luis_app_ids, expected_type=type_hints["luis_app_ids"])
            check_type(argname="argument luis_key", value=luis_key, expected_type=type_hints["luis_key"])
            check_type(argname="argument microsoft_app_msi_id", value=microsoft_app_msi_id, expected_type=type_hints["microsoft_app_msi_id"])
            check_type(argname="argument microsoft_app_tenant_id", value=microsoft_app_tenant_id, expected_type=type_hints["microsoft_app_tenant_id"])
            check_type(argname="argument microsoft_app_type", value=microsoft_app_type, expected_type=type_hints["microsoft_app_type"])
            check_type(argname="argument public_network_access_enabled", value=public_network_access_enabled, expected_type=type_hints["public_network_access_enabled"])
            check_type(argname="argument streaming_endpoint_enabled", value=streaming_endpoint_enabled, expected_type=type_hints["streaming_endpoint_enabled"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "location": location,
            "microsoft_app_id": microsoft_app_id,
            "name": name,
            "resource_group_name": resource_group_name,
            "sku": sku,
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
        if cmk_key_vault_key_url is not None:
            self._values["cmk_key_vault_key_url"] = cmk_key_vault_key_url
        if developer_app_insights_api_key is not None:
            self._values["developer_app_insights_api_key"] = developer_app_insights_api_key
        if developer_app_insights_application_id is not None:
            self._values["developer_app_insights_application_id"] = developer_app_insights_application_id
        if developer_app_insights_key is not None:
            self._values["developer_app_insights_key"] = developer_app_insights_key
        if display_name is not None:
            self._values["display_name"] = display_name
        if endpoint is not None:
            self._values["endpoint"] = endpoint
        if icon_url is not None:
            self._values["icon_url"] = icon_url
        if id is not None:
            self._values["id"] = id
        if local_authentication_enabled is not None:
            self._values["local_authentication_enabled"] = local_authentication_enabled
        if luis_app_ids is not None:
            self._values["luis_app_ids"] = luis_app_ids
        if luis_key is not None:
            self._values["luis_key"] = luis_key
        if microsoft_app_msi_id is not None:
            self._values["microsoft_app_msi_id"] = microsoft_app_msi_id
        if microsoft_app_tenant_id is not None:
            self._values["microsoft_app_tenant_id"] = microsoft_app_tenant_id
        if microsoft_app_type is not None:
            self._values["microsoft_app_type"] = microsoft_app_type
        if public_network_access_enabled is not None:
            self._values["public_network_access_enabled"] = public_network_access_enabled
        if streaming_endpoint_enabled is not None:
            self._values["streaming_endpoint_enabled"] = streaming_endpoint_enabled
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#location BotServiceAzureBot#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def microsoft_app_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#microsoft_app_id BotServiceAzureBot#microsoft_app_id}.'''
        result = self._values.get("microsoft_app_id")
        assert result is not None, "Required property 'microsoft_app_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#name BotServiceAzureBot#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#resource_group_name BotServiceAzureBot#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sku(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#sku BotServiceAzureBot#sku}.'''
        result = self._values.get("sku")
        assert result is not None, "Required property 'sku' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cmk_key_vault_key_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#cmk_key_vault_key_url BotServiceAzureBot#cmk_key_vault_key_url}.'''
        result = self._values.get("cmk_key_vault_key_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def developer_app_insights_api_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#developer_app_insights_api_key BotServiceAzureBot#developer_app_insights_api_key}.'''
        result = self._values.get("developer_app_insights_api_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def developer_app_insights_application_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#developer_app_insights_application_id BotServiceAzureBot#developer_app_insights_application_id}.'''
        result = self._values.get("developer_app_insights_application_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def developer_app_insights_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#developer_app_insights_key BotServiceAzureBot#developer_app_insights_key}.'''
        result = self._values.get("developer_app_insights_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#display_name BotServiceAzureBot#display_name}.'''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def endpoint(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#endpoint BotServiceAzureBot#endpoint}.'''
        result = self._values.get("endpoint")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def icon_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#icon_url BotServiceAzureBot#icon_url}.'''
        result = self._values.get("icon_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#id BotServiceAzureBot#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def local_authentication_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#local_authentication_enabled BotServiceAzureBot#local_authentication_enabled}.'''
        result = self._values.get("local_authentication_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def luis_app_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#luis_app_ids BotServiceAzureBot#luis_app_ids}.'''
        result = self._values.get("luis_app_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def luis_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#luis_key BotServiceAzureBot#luis_key}.'''
        result = self._values.get("luis_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def microsoft_app_msi_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#microsoft_app_msi_id BotServiceAzureBot#microsoft_app_msi_id}.'''
        result = self._values.get("microsoft_app_msi_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def microsoft_app_tenant_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#microsoft_app_tenant_id BotServiceAzureBot#microsoft_app_tenant_id}.'''
        result = self._values.get("microsoft_app_tenant_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def microsoft_app_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#microsoft_app_type BotServiceAzureBot#microsoft_app_type}.'''
        result = self._values.get("microsoft_app_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_network_access_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#public_network_access_enabled BotServiceAzureBot#public_network_access_enabled}.'''
        result = self._values.get("public_network_access_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def streaming_endpoint_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#streaming_endpoint_enabled BotServiceAzureBot#streaming_endpoint_enabled}.'''
        result = self._values.get("streaming_endpoint_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#tags BotServiceAzureBot#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["BotServiceAzureBotTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#timeouts BotServiceAzureBot#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["BotServiceAzureBotTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BotServiceAzureBotConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.botServiceAzureBot.BotServiceAzureBotTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class BotServiceAzureBotTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#create BotServiceAzureBot#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#delete BotServiceAzureBot#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#read BotServiceAzureBot#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#update BotServiceAzureBot#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbdebda89e6c9f77afd04889aa89b456a7b28d6c5944f1cc7ff99cae8b372622)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#create BotServiceAzureBot#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#delete BotServiceAzureBot#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#read BotServiceAzureBot#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/bot_service_azure_bot#update BotServiceAzureBot#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BotServiceAzureBotTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BotServiceAzureBotTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.botServiceAzureBot.BotServiceAzureBotTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__08ca49468adb503e8ec626e4b502fee5da451231fb6b96826f6e605ce74b48ce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9977ba08592bf2261fa5acd2660b1c55a43df628f279b17243afc2f90175caa8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99e7bcdb219f503c0ad51bba327158ef80c035fe09c8b8be2a675108dc8365cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__297b36c86292e7a817a2837a351be42c8958eefa37691b1d95ac430398e959d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eb190b52f7a09271fd906bdcf97d7957ba2a17e3a56286aa47129ae35ac75e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BotServiceAzureBotTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BotServiceAzureBotTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BotServiceAzureBotTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__094b52521a7b9aa4cbda21d36626b074375c1ecf98770acd9231e0af6c0f84e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "BotServiceAzureBot",
    "BotServiceAzureBotConfig",
    "BotServiceAzureBotTimeouts",
    "BotServiceAzureBotTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f7b74227bf59fdf6efc172ada372089541b9f8dbff0b55bf7c5500e175f14cf2(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    microsoft_app_id: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    sku: builtins.str,
    cmk_key_vault_key_url: typing.Optional[builtins.str] = None,
    developer_app_insights_api_key: typing.Optional[builtins.str] = None,
    developer_app_insights_application_id: typing.Optional[builtins.str] = None,
    developer_app_insights_key: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    endpoint: typing.Optional[builtins.str] = None,
    icon_url: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    local_authentication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    luis_app_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    luis_key: typing.Optional[builtins.str] = None,
    microsoft_app_msi_id: typing.Optional[builtins.str] = None,
    microsoft_app_tenant_id: typing.Optional[builtins.str] = None,
    microsoft_app_type: typing.Optional[builtins.str] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    streaming_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[BotServiceAzureBotTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__2234ab1c543d280a1647c69b48b76117b78305ed055d46c13d292b870545fa63(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a2d2b980569795d04ef222269ab01bf6d1b41f37500172272e0d347220308f7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b5ba9670c1e2d5429dbc6b05a9278fda2ddc829e9b246eb393d3efa843c027a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfafb58a55cb8b5213cd67ccd7a174b21c2675c5574985cbefdb9a1bee432f35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04685cfeff3e7abd5abcbb139e4062dd5db225b8de2261921d20d57a011d571e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ebe5320c8758b2a310074fe3e7cc9dbfb7b8dcaaa1546e0f9090b8f439bf6a1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__256aa4c51ee72388dd8d4f7d0f1274714d0cdb265be9445f21a040b6b644426f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__723db323714cf70e3b307aab92b097a92e555e9d558b430ec5357fe603b0c55e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__371c71ff75e188b1de86fd32da898def337a8e8ea45019669ab276aec68debdb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74acd3fd458498f5e7c1e4d84353fb8081193738d4a3d3b7d2e87371e0b069b5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b88355fb1049489f6e446fe454f925da0b28a51bea7dc42b88a5639b4aa1dc8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb5abc2345d84c1723ab6da41187c1fa8adc5d3673ef96654aaf02de9c2f80bd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83e59290cd893aea6c0ebc890de679372f6a7dfbc0d59dea6e62e3a86f833605(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e5a96ebf9ed66a112cd225e4bff756c988b486a1b2864ad5ec2e2fa96114e8f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dc63506818e67ad252bc604eb16324f300adb02e3ed764f56419a715d3ac8e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fab8fa1c83aabc3c52c07865334ea153438815a043a5952b39ed465715dbb2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f76bbb6e8f68893e0d29d8098d7d1bf76b2b3db858748af639caa1906779897f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a8cd8d9b3f7776726b593a5fd9140249bada1a172642557c42ea8d5efc09c29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78a6efb7c2bb9b3ae12b5adce9eec73e8820e0f6ac75d63b879d977d67dc2165(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11163f3d32381f553aafaf4156d82ff1a97c8d4dba42218e71a68485b6703d00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b79b03ab105ed6c3993b2f025a7de7b72bfd26a46085cead60582fbf827fbd4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f02a7f57533fe3a4d2cca9e85e1eeba36a90e4e2e6dbc88db0b2032b31abf90(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95b2fec24ffd35a995bff5473c74b1b9f9189caab758884cbd79e6f84a184904(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a48b498e926ed8833398bd7ddd413a755796745379894c82b889aa0dfe39879(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    location: builtins.str,
    microsoft_app_id: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    sku: builtins.str,
    cmk_key_vault_key_url: typing.Optional[builtins.str] = None,
    developer_app_insights_api_key: typing.Optional[builtins.str] = None,
    developer_app_insights_application_id: typing.Optional[builtins.str] = None,
    developer_app_insights_key: typing.Optional[builtins.str] = None,
    display_name: typing.Optional[builtins.str] = None,
    endpoint: typing.Optional[builtins.str] = None,
    icon_url: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    local_authentication_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    luis_app_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    luis_key: typing.Optional[builtins.str] = None,
    microsoft_app_msi_id: typing.Optional[builtins.str] = None,
    microsoft_app_tenant_id: typing.Optional[builtins.str] = None,
    microsoft_app_type: typing.Optional[builtins.str] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    streaming_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[BotServiceAzureBotTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbdebda89e6c9f77afd04889aa89b456a7b28d6c5944f1cc7ff99cae8b372622(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08ca49468adb503e8ec626e4b502fee5da451231fb6b96826f6e605ce74b48ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9977ba08592bf2261fa5acd2660b1c55a43df628f279b17243afc2f90175caa8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99e7bcdb219f503c0ad51bba327158ef80c035fe09c8b8be2a675108dc8365cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__297b36c86292e7a817a2837a351be42c8958eefa37691b1d95ac430398e959d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eb190b52f7a09271fd906bdcf97d7957ba2a17e3a56286aa47129ae35ac75e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__094b52521a7b9aa4cbda21d36626b074375c1ecf98770acd9231e0af6c0f84e5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, BotServiceAzureBotTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
