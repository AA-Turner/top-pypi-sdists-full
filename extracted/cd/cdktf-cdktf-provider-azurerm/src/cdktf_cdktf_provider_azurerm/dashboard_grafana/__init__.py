r'''
# `azurerm_dashboard_grafana`

Refer to the Terraform Registry for docs: [`azurerm_dashboard_grafana`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana).
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


class DashboardGrafana(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dashboardGrafana.DashboardGrafana",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana azurerm_dashboard_grafana}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        grafana_major_version: builtins.str,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        api_key_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auto_generated_domain_name_label_scope: typing.Optional[builtins.str] = None,
        azure_monitor_workspace_integrations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DashboardGrafanaAzureMonitorWorkspaceIntegrations", typing.Dict[builtins.str, typing.Any]]]]] = None,
        deterministic_outbound_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["DashboardGrafanaIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sku: typing.Optional[builtins.str] = None,
        smtp: typing.Optional[typing.Union["DashboardGrafanaSmtp", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["DashboardGrafanaTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        zone_redundancy_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana azurerm_dashboard_grafana} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param grafana_major_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#grafana_major_version DashboardGrafana#grafana_major_version}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#location DashboardGrafana#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#name DashboardGrafana#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#resource_group_name DashboardGrafana#resource_group_name}.
        :param api_key_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#api_key_enabled DashboardGrafana#api_key_enabled}.
        :param auto_generated_domain_name_label_scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#auto_generated_domain_name_label_scope DashboardGrafana#auto_generated_domain_name_label_scope}.
        :param azure_monitor_workspace_integrations: azure_monitor_workspace_integrations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#azure_monitor_workspace_integrations DashboardGrafana#azure_monitor_workspace_integrations}
        :param deterministic_outbound_ip_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#deterministic_outbound_ip_enabled DashboardGrafana#deterministic_outbound_ip_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#id DashboardGrafana#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#identity DashboardGrafana#identity}
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#public_network_access_enabled DashboardGrafana#public_network_access_enabled}.
        :param sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#sku DashboardGrafana#sku}.
        :param smtp: smtp block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#smtp DashboardGrafana#smtp}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#tags DashboardGrafana#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#timeouts DashboardGrafana#timeouts}
        :param zone_redundancy_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#zone_redundancy_enabled DashboardGrafana#zone_redundancy_enabled}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc5938b2c8ddc6b8644dc4f33200cbc13ac613f0f8d799c191941118dafc5bc6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DashboardGrafanaConfig(
            grafana_major_version=grafana_major_version,
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            api_key_enabled=api_key_enabled,
            auto_generated_domain_name_label_scope=auto_generated_domain_name_label_scope,
            azure_monitor_workspace_integrations=azure_monitor_workspace_integrations,
            deterministic_outbound_ip_enabled=deterministic_outbound_ip_enabled,
            id=id,
            identity=identity,
            public_network_access_enabled=public_network_access_enabled,
            sku=sku,
            smtp=smtp,
            tags=tags,
            timeouts=timeouts,
            zone_redundancy_enabled=zone_redundancy_enabled,
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
        '''Generates CDKTF code for importing a DashboardGrafana resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DashboardGrafana to import.
        :param import_from_id: The id of the existing DashboardGrafana that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DashboardGrafana to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41f0a4539b7f30e6fc6868b27e446ef9b93d7a5eb8fe527a7416fb5c60044713)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAzureMonitorWorkspaceIntegrations")
    def put_azure_monitor_workspace_integrations(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DashboardGrafanaAzureMonitorWorkspaceIntegrations", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ade56b9dc4341fb3c04a285c0f4fcd9c6bd499bda5007477d87559b2a6626e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAzureMonitorWorkspaceIntegrations", [value]))

    @jsii.member(jsii_name="putIdentity")
    def put_identity(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#type DashboardGrafana#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#identity_ids DashboardGrafana#identity_ids}.
        '''
        value = DashboardGrafanaIdentity(type=type, identity_ids=identity_ids)

        return typing.cast(None, jsii.invoke(self, "putIdentity", [value]))

    @jsii.member(jsii_name="putSmtp")
    def put_smtp(
        self,
        *,
        from_address: builtins.str,
        host: builtins.str,
        password: builtins.str,
        start_tls_policy: builtins.str,
        user: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        from_name: typing.Optional[builtins.str] = None,
        verification_skip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param from_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#from_address DashboardGrafana#from_address}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#host DashboardGrafana#host}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#password DashboardGrafana#password}.
        :param start_tls_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#start_tls_policy DashboardGrafana#start_tls_policy}.
        :param user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#user DashboardGrafana#user}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#enabled DashboardGrafana#enabled}.
        :param from_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#from_name DashboardGrafana#from_name}.
        :param verification_skip_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#verification_skip_enabled DashboardGrafana#verification_skip_enabled}.
        '''
        value = DashboardGrafanaSmtp(
            from_address=from_address,
            host=host,
            password=password,
            start_tls_policy=start_tls_policy,
            user=user,
            enabled=enabled,
            from_name=from_name,
            verification_skip_enabled=verification_skip_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putSmtp", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#create DashboardGrafana#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#delete DashboardGrafana#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#read DashboardGrafana#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#update DashboardGrafana#update}.
        '''
        value = DashboardGrafanaTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetApiKeyEnabled")
    def reset_api_key_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiKeyEnabled", []))

    @jsii.member(jsii_name="resetAutoGeneratedDomainNameLabelScope")
    def reset_auto_generated_domain_name_label_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoGeneratedDomainNameLabelScope", []))

    @jsii.member(jsii_name="resetAzureMonitorWorkspaceIntegrations")
    def reset_azure_monitor_workspace_integrations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAzureMonitorWorkspaceIntegrations", []))

    @jsii.member(jsii_name="resetDeterministicOutboundIpEnabled")
    def reset_deterministic_outbound_ip_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeterministicOutboundIpEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentity")
    def reset_identity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentity", []))

    @jsii.member(jsii_name="resetPublicNetworkAccessEnabled")
    def reset_public_network_access_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicNetworkAccessEnabled", []))

    @jsii.member(jsii_name="resetSku")
    def reset_sku(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSku", []))

    @jsii.member(jsii_name="resetSmtp")
    def reset_smtp(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSmtp", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetZoneRedundancyEnabled")
    def reset_zone_redundancy_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZoneRedundancyEnabled", []))

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
    @jsii.member(jsii_name="azureMonitorWorkspaceIntegrations")
    def azure_monitor_workspace_integrations(
        self,
    ) -> "DashboardGrafanaAzureMonitorWorkspaceIntegrationsList":
        return typing.cast("DashboardGrafanaAzureMonitorWorkspaceIntegrationsList", jsii.get(self, "azureMonitorWorkspaceIntegrations"))

    @builtins.property
    @jsii.member(jsii_name="endpoint")
    def endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpoint"))

    @builtins.property
    @jsii.member(jsii_name="grafanaVersion")
    def grafana_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "grafanaVersion"))

    @builtins.property
    @jsii.member(jsii_name="identity")
    def identity(self) -> "DashboardGrafanaIdentityOutputReference":
        return typing.cast("DashboardGrafanaIdentityOutputReference", jsii.get(self, "identity"))

    @builtins.property
    @jsii.member(jsii_name="outboundIp")
    def outbound_ip(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "outboundIp"))

    @builtins.property
    @jsii.member(jsii_name="smtp")
    def smtp(self) -> "DashboardGrafanaSmtpOutputReference":
        return typing.cast("DashboardGrafanaSmtpOutputReference", jsii.get(self, "smtp"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DashboardGrafanaTimeoutsOutputReference":
        return typing.cast("DashboardGrafanaTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="apiKeyEnabledInput")
    def api_key_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "apiKeyEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="autoGeneratedDomainNameLabelScopeInput")
    def auto_generated_domain_name_label_scope_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoGeneratedDomainNameLabelScopeInput"))

    @builtins.property
    @jsii.member(jsii_name="azureMonitorWorkspaceIntegrationsInput")
    def azure_monitor_workspace_integrations_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DashboardGrafanaAzureMonitorWorkspaceIntegrations"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DashboardGrafanaAzureMonitorWorkspaceIntegrations"]]], jsii.get(self, "azureMonitorWorkspaceIntegrationsInput"))

    @builtins.property
    @jsii.member(jsii_name="deterministicOutboundIpEnabledInput")
    def deterministic_outbound_ip_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deterministicOutboundIpEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="grafanaMajorVersionInput")
    def grafana_major_version_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "grafanaMajorVersionInput"))

    @builtins.property
    @jsii.member(jsii_name="identityInput")
    def identity_input(self) -> typing.Optional["DashboardGrafanaIdentity"]:
        return typing.cast(typing.Optional["DashboardGrafanaIdentity"], jsii.get(self, "identityInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

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
    @jsii.member(jsii_name="smtpInput")
    def smtp_input(self) -> typing.Optional["DashboardGrafanaSmtp"]:
        return typing.cast(typing.Optional["DashboardGrafanaSmtp"], jsii.get(self, "smtpInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DashboardGrafanaTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DashboardGrafanaTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneRedundancyEnabledInput")
    def zone_redundancy_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "zoneRedundancyEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="apiKeyEnabled")
    def api_key_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "apiKeyEnabled"))

    @api_key_enabled.setter
    def api_key_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bd3de7dfb9e3d5157ce2c4c3591f4e01436b55f2345d01d989d6aaab2c53303)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiKeyEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="autoGeneratedDomainNameLabelScope")
    def auto_generated_domain_name_label_scope(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "autoGeneratedDomainNameLabelScope"))

    @auto_generated_domain_name_label_scope.setter
    def auto_generated_domain_name_label_scope(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__538ba396c0c43df96f1a4b4cbdecfbe2e542847d7d9366089fde9d07aafdbe24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoGeneratedDomainNameLabelScope", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="deterministicOutboundIpEnabled")
    def deterministic_outbound_ip_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deterministicOutboundIpEnabled"))

    @deterministic_outbound_ip_enabled.setter
    def deterministic_outbound_ip_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6656206d20c6ba253d70e24c1b37d2d978382cd9340f6bd0dbbc925cfe92832e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deterministicOutboundIpEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="grafanaMajorVersion")
    def grafana_major_version(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "grafanaMajorVersion"))

    @grafana_major_version.setter
    def grafana_major_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a55e67c6018b909592a2e71c1c1f1dfa5d7264851803e00424a2d73baa4690e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "grafanaMajorVersion", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b538bc858a7f379a4a7ff677769bef2b30401a5ca739996e41854c655ba6935)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__989d738bd2150f87667069e448b2585c59552ef9661d203be66dfe8cc2e819f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__685673915e51f4bd5112b3daf90b87af77f4bf88353834a375e958ad4f407740)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e03cc25bbff8055ccb669f4f41039e952ab17f5c55890e9ecb6f0931583f7bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicNetworkAccessEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9051dcbe3a7dd60d448982c7cf79ef166c5ee819c0c8473558054efcabc2c4be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sku")
    def sku(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sku"))

    @sku.setter
    def sku(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7f533a832c4c92409a39162cd087e58a9315ce4b0fca908a750f7f7bc54db4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sku", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__797408c919cac079476e26852344c7ed1a014190f2bbfa560d6f4563894817d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zoneRedundancyEnabled")
    def zone_redundancy_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "zoneRedundancyEnabled"))

    @zone_redundancy_enabled.setter
    def zone_redundancy_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0ebe9cca76a8cb33b5fcad8e2e5548dc48b7cd3440880953799a109ca744b7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneRedundancyEnabled", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dashboardGrafana.DashboardGrafanaAzureMonitorWorkspaceIntegrations",
    jsii_struct_bases=[],
    name_mapping={"resource_id": "resourceId"},
)
class DashboardGrafanaAzureMonitorWorkspaceIntegrations:
    def __init__(self, *, resource_id: builtins.str) -> None:
        '''
        :param resource_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#resource_id DashboardGrafana#resource_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e43aa4a8d245b695a5a3ed8800404f3bd95850f5359ed8f1d478d062b7d7f7b)
            check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_id": resource_id,
        }

    @builtins.property
    def resource_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#resource_id DashboardGrafana#resource_id}.'''
        result = self._values.get("resource_id")
        assert result is not None, "Required property 'resource_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DashboardGrafanaAzureMonitorWorkspaceIntegrations(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DashboardGrafanaAzureMonitorWorkspaceIntegrationsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dashboardGrafana.DashboardGrafanaAzureMonitorWorkspaceIntegrationsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b179933e6d6aea3aacbc598124c7fb01e7c6880e62bc46fc18e47709d046c495)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DashboardGrafanaAzureMonitorWorkspaceIntegrationsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83c4a3c77785f824f92311a94c157e50281a48f89db3f3ba551dd5b0b9636cfc)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DashboardGrafanaAzureMonitorWorkspaceIntegrationsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__773d5d1146b4c81a707b3eb2ad603323557991f9247acc375e93baee8ad6656b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__779b3b9bc792e9800473f4dcb0228a3c54098253500f11de746f48735680f560)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b4f3832caad24d9db2926a4fb272542ba67fa2af333e2e05cb78d11e12bd6ae6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DashboardGrafanaAzureMonitorWorkspaceIntegrations]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DashboardGrafanaAzureMonitorWorkspaceIntegrations]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DashboardGrafanaAzureMonitorWorkspaceIntegrations]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf8ffcc1f3715a5e64c4bdf3cd5c95ed2ccb756e812b32836704cf1670ca3be2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DashboardGrafanaAzureMonitorWorkspaceIntegrationsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dashboardGrafana.DashboardGrafanaAzureMonitorWorkspaceIntegrationsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__53d226f7444cb227b597796a5e90ed2f1049361b9c4679de97e4fee2907f70d1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="resourceIdInput")
    def resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceId"))

    @resource_id.setter
    def resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97989eeffe78f1714e31b1b7ee010eced9fa6fec2d36cbf2b7065fc442b83613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DashboardGrafanaAzureMonitorWorkspaceIntegrations]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DashboardGrafanaAzureMonitorWorkspaceIntegrations]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DashboardGrafanaAzureMonitorWorkspaceIntegrations]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b210ee86b1364fff38bae4819ec478d0c45f18f2c69b7e0f41e8b3ada1709d61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dashboardGrafana.DashboardGrafanaConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "grafana_major_version": "grafanaMajorVersion",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "api_key_enabled": "apiKeyEnabled",
        "auto_generated_domain_name_label_scope": "autoGeneratedDomainNameLabelScope",
        "azure_monitor_workspace_integrations": "azureMonitorWorkspaceIntegrations",
        "deterministic_outbound_ip_enabled": "deterministicOutboundIpEnabled",
        "id": "id",
        "identity": "identity",
        "public_network_access_enabled": "publicNetworkAccessEnabled",
        "sku": "sku",
        "smtp": "smtp",
        "tags": "tags",
        "timeouts": "timeouts",
        "zone_redundancy_enabled": "zoneRedundancyEnabled",
    },
)
class DashboardGrafanaConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        grafana_major_version: builtins.str,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        api_key_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        auto_generated_domain_name_label_scope: typing.Optional[builtins.str] = None,
        azure_monitor_workspace_integrations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DashboardGrafanaAzureMonitorWorkspaceIntegrations, typing.Dict[builtins.str, typing.Any]]]]] = None,
        deterministic_outbound_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        identity: typing.Optional[typing.Union["DashboardGrafanaIdentity", typing.Dict[builtins.str, typing.Any]]] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sku: typing.Optional[builtins.str] = None,
        smtp: typing.Optional[typing.Union["DashboardGrafanaSmtp", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["DashboardGrafanaTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        zone_redundancy_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param grafana_major_version: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#grafana_major_version DashboardGrafana#grafana_major_version}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#location DashboardGrafana#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#name DashboardGrafana#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#resource_group_name DashboardGrafana#resource_group_name}.
        :param api_key_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#api_key_enabled DashboardGrafana#api_key_enabled}.
        :param auto_generated_domain_name_label_scope: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#auto_generated_domain_name_label_scope DashboardGrafana#auto_generated_domain_name_label_scope}.
        :param azure_monitor_workspace_integrations: azure_monitor_workspace_integrations block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#azure_monitor_workspace_integrations DashboardGrafana#azure_monitor_workspace_integrations}
        :param deterministic_outbound_ip_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#deterministic_outbound_ip_enabled DashboardGrafana#deterministic_outbound_ip_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#id DashboardGrafana#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identity: identity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#identity DashboardGrafana#identity}
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#public_network_access_enabled DashboardGrafana#public_network_access_enabled}.
        :param sku: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#sku DashboardGrafana#sku}.
        :param smtp: smtp block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#smtp DashboardGrafana#smtp}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#tags DashboardGrafana#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#timeouts DashboardGrafana#timeouts}
        :param zone_redundancy_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#zone_redundancy_enabled DashboardGrafana#zone_redundancy_enabled}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(identity, dict):
            identity = DashboardGrafanaIdentity(**identity)
        if isinstance(smtp, dict):
            smtp = DashboardGrafanaSmtp(**smtp)
        if isinstance(timeouts, dict):
            timeouts = DashboardGrafanaTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8aa716058c0e4a73da5cc689aeff1d8aeaefe2dedf5d794edd0041951eb9f53c)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument grafana_major_version", value=grafana_major_version, expected_type=type_hints["grafana_major_version"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument api_key_enabled", value=api_key_enabled, expected_type=type_hints["api_key_enabled"])
            check_type(argname="argument auto_generated_domain_name_label_scope", value=auto_generated_domain_name_label_scope, expected_type=type_hints["auto_generated_domain_name_label_scope"])
            check_type(argname="argument azure_monitor_workspace_integrations", value=azure_monitor_workspace_integrations, expected_type=type_hints["azure_monitor_workspace_integrations"])
            check_type(argname="argument deterministic_outbound_ip_enabled", value=deterministic_outbound_ip_enabled, expected_type=type_hints["deterministic_outbound_ip_enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument public_network_access_enabled", value=public_network_access_enabled, expected_type=type_hints["public_network_access_enabled"])
            check_type(argname="argument sku", value=sku, expected_type=type_hints["sku"])
            check_type(argname="argument smtp", value=smtp, expected_type=type_hints["smtp"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument zone_redundancy_enabled", value=zone_redundancy_enabled, expected_type=type_hints["zone_redundancy_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "grafana_major_version": grafana_major_version,
            "location": location,
            "name": name,
            "resource_group_name": resource_group_name,
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
        if api_key_enabled is not None:
            self._values["api_key_enabled"] = api_key_enabled
        if auto_generated_domain_name_label_scope is not None:
            self._values["auto_generated_domain_name_label_scope"] = auto_generated_domain_name_label_scope
        if azure_monitor_workspace_integrations is not None:
            self._values["azure_monitor_workspace_integrations"] = azure_monitor_workspace_integrations
        if deterministic_outbound_ip_enabled is not None:
            self._values["deterministic_outbound_ip_enabled"] = deterministic_outbound_ip_enabled
        if id is not None:
            self._values["id"] = id
        if identity is not None:
            self._values["identity"] = identity
        if public_network_access_enabled is not None:
            self._values["public_network_access_enabled"] = public_network_access_enabled
        if sku is not None:
            self._values["sku"] = sku
        if smtp is not None:
            self._values["smtp"] = smtp
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if zone_redundancy_enabled is not None:
            self._values["zone_redundancy_enabled"] = zone_redundancy_enabled

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
    def grafana_major_version(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#grafana_major_version DashboardGrafana#grafana_major_version}.'''
        result = self._values.get("grafana_major_version")
        assert result is not None, "Required property 'grafana_major_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#location DashboardGrafana#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#name DashboardGrafana#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#resource_group_name DashboardGrafana#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def api_key_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#api_key_enabled DashboardGrafana#api_key_enabled}.'''
        result = self._values.get("api_key_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def auto_generated_domain_name_label_scope(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#auto_generated_domain_name_label_scope DashboardGrafana#auto_generated_domain_name_label_scope}.'''
        result = self._values.get("auto_generated_domain_name_label_scope")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def azure_monitor_workspace_integrations(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DashboardGrafanaAzureMonitorWorkspaceIntegrations]]]:
        '''azure_monitor_workspace_integrations block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#azure_monitor_workspace_integrations DashboardGrafana#azure_monitor_workspace_integrations}
        '''
        result = self._values.get("azure_monitor_workspace_integrations")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DashboardGrafanaAzureMonitorWorkspaceIntegrations]]], result)

    @builtins.property
    def deterministic_outbound_ip_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#deterministic_outbound_ip_enabled DashboardGrafana#deterministic_outbound_ip_enabled}.'''
        result = self._values.get("deterministic_outbound_ip_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#id DashboardGrafana#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identity(self) -> typing.Optional["DashboardGrafanaIdentity"]:
        '''identity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#identity DashboardGrafana#identity}
        '''
        result = self._values.get("identity")
        return typing.cast(typing.Optional["DashboardGrafanaIdentity"], result)

    @builtins.property
    def public_network_access_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#public_network_access_enabled DashboardGrafana#public_network_access_enabled}.'''
        result = self._values.get("public_network_access_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def sku(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#sku DashboardGrafana#sku}.'''
        result = self._values.get("sku")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def smtp(self) -> typing.Optional["DashboardGrafanaSmtp"]:
        '''smtp block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#smtp DashboardGrafana#smtp}
        '''
        result = self._values.get("smtp")
        return typing.cast(typing.Optional["DashboardGrafanaSmtp"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#tags DashboardGrafana#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DashboardGrafanaTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#timeouts DashboardGrafana#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DashboardGrafanaTimeouts"], result)

    @builtins.property
    def zone_redundancy_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#zone_redundancy_enabled DashboardGrafana#zone_redundancy_enabled}.'''
        result = self._values.get("zone_redundancy_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DashboardGrafanaConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dashboardGrafana.DashboardGrafanaIdentity",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "identity_ids": "identityIds"},
)
class DashboardGrafanaIdentity:
    def __init__(
        self,
        *,
        type: builtins.str,
        identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#type DashboardGrafana#type}.
        :param identity_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#identity_ids DashboardGrafana#identity_ids}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__236c99dab129b07570cf389a1dea199490b3df544c9a3668dcb3cb0ebcf93a33)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument identity_ids", value=identity_ids, expected_type=type_hints["identity_ids"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if identity_ids is not None:
            self._values["identity_ids"] = identity_ids

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#type DashboardGrafana#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def identity_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#identity_ids DashboardGrafana#identity_ids}.'''
        result = self._values.get("identity_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DashboardGrafanaIdentity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DashboardGrafanaIdentityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dashboardGrafana.DashboardGrafanaIdentityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7e02b88c1a971f9c5f8d5d2f38321f062eec16f727c4bea6a72f915a49724f79)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dcd3adf404c4b7a11d0fe54af9932bed62cad994f2890d64050071c5238fbf23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identityIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f73cf45ddc4481d371338317c0929f8c78564674c8129867fb383e1b4dc38dee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DashboardGrafanaIdentity]:
        return typing.cast(typing.Optional[DashboardGrafanaIdentity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DashboardGrafanaIdentity]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f6a0149bd1cfd8b7ecebce493d90f56018f3a4cc5978f5b504db4ef0d1bff97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dashboardGrafana.DashboardGrafanaSmtp",
    jsii_struct_bases=[],
    name_mapping={
        "from_address": "fromAddress",
        "host": "host",
        "password": "password",
        "start_tls_policy": "startTlsPolicy",
        "user": "user",
        "enabled": "enabled",
        "from_name": "fromName",
        "verification_skip_enabled": "verificationSkipEnabled",
    },
)
class DashboardGrafanaSmtp:
    def __init__(
        self,
        *,
        from_address: builtins.str,
        host: builtins.str,
        password: builtins.str,
        start_tls_policy: builtins.str,
        user: builtins.str,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        from_name: typing.Optional[builtins.str] = None,
        verification_skip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param from_address: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#from_address DashboardGrafana#from_address}.
        :param host: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#host DashboardGrafana#host}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#password DashboardGrafana#password}.
        :param start_tls_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#start_tls_policy DashboardGrafana#start_tls_policy}.
        :param user: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#user DashboardGrafana#user}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#enabled DashboardGrafana#enabled}.
        :param from_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#from_name DashboardGrafana#from_name}.
        :param verification_skip_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#verification_skip_enabled DashboardGrafana#verification_skip_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5941a50e34d9fc7b277fe178f8a5bc991e79758ea37a77ff70f6927e792ce7af)
            check_type(argname="argument from_address", value=from_address, expected_type=type_hints["from_address"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument start_tls_policy", value=start_tls_policy, expected_type=type_hints["start_tls_policy"])
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument from_name", value=from_name, expected_type=type_hints["from_name"])
            check_type(argname="argument verification_skip_enabled", value=verification_skip_enabled, expected_type=type_hints["verification_skip_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "from_address": from_address,
            "host": host,
            "password": password,
            "start_tls_policy": start_tls_policy,
            "user": user,
        }
        if enabled is not None:
            self._values["enabled"] = enabled
        if from_name is not None:
            self._values["from_name"] = from_name
        if verification_skip_enabled is not None:
            self._values["verification_skip_enabled"] = verification_skip_enabled

    @builtins.property
    def from_address(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#from_address DashboardGrafana#from_address}.'''
        result = self._values.get("from_address")
        assert result is not None, "Required property 'from_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#host DashboardGrafana#host}.'''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#password DashboardGrafana#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_tls_policy(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#start_tls_policy DashboardGrafana#start_tls_policy}.'''
        result = self._values.get("start_tls_policy")
        assert result is not None, "Required property 'start_tls_policy' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#user DashboardGrafana#user}.'''
        result = self._values.get("user")
        assert result is not None, "Required property 'user' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#enabled DashboardGrafana#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def from_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#from_name DashboardGrafana#from_name}.'''
        result = self._values.get("from_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def verification_skip_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#verification_skip_enabled DashboardGrafana#verification_skip_enabled}.'''
        result = self._values.get("verification_skip_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DashboardGrafanaSmtp(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DashboardGrafanaSmtpOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dashboardGrafana.DashboardGrafanaSmtpOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31f8e839ee570e39e340101a33c83981177625fd49c064afc9fb9f1420830ee2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetFromName")
    def reset_from_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFromName", []))

    @jsii.member(jsii_name="resetVerificationSkipEnabled")
    def reset_verification_skip_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVerificationSkipEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="fromAddressInput")
    def from_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fromAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="fromNameInput")
    def from_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fromNameInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="startTlsPolicyInput")
    def start_tls_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTlsPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="userInput")
    def user_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userInput"))

    @builtins.property
    @jsii.member(jsii_name="verificationSkipEnabledInput")
    def verification_skip_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "verificationSkipEnabledInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__650b9a9902ec70b41a1eee58426ceea63860b691d10eef3fbd46dbd6f65c864d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fromAddress")
    def from_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fromAddress"))

    @from_address.setter
    def from_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb0eb44d42327a8262080d60137d1be6c8567df152277a31951c19fd49c34378)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fromAddress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fromName")
    def from_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fromName"))

    @from_name.setter
    def from_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3112c5de272483205b2e18d522e5c4396129d27b650416dfd9410daeb5d0881d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fromName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3968e27189eddd242e8eddbbba28ea4a51d9135c26f8ba6e67432c9b1d672cab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4406b5ad24981b35886462905b151ee278898c0637490f975cb23a838ac91cc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTlsPolicy")
    def start_tls_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTlsPolicy"))

    @start_tls_policy.setter
    def start_tls_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e196cc0d6afabbf06b3efe3dff1125e08e75bee0b2229e5f2b0ede8fa448f715)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTlsPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="user")
    def user(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "user"))

    @user.setter
    def user(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ca8eee0aa1a0497f2753df02f48b4f951aa9f4beaf173b230267a308474d7e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "user", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="verificationSkipEnabled")
    def verification_skip_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "verificationSkipEnabled"))

    @verification_skip_enabled.setter
    def verification_skip_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__badeece22233f33d6dc621d81f27a08101d8358d3ad513e4f3c1b48339c58948)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "verificationSkipEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DashboardGrafanaSmtp]:
        return typing.cast(typing.Optional[DashboardGrafanaSmtp], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[DashboardGrafanaSmtp]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96591e45be7a56063ce3d149464b0d23613e2b1b402f45d76bb2bce6b4049af5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.dashboardGrafana.DashboardGrafanaTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class DashboardGrafanaTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#create DashboardGrafana#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#delete DashboardGrafana#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#read DashboardGrafana#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#update DashboardGrafana#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6231c9783352c2edc5ebd492568bf65d9d862e6b6691aa89a41ab8815cce0f12)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#create DashboardGrafana#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#delete DashboardGrafana#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#read DashboardGrafana#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/dashboard_grafana#update DashboardGrafana#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DashboardGrafanaTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DashboardGrafanaTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.dashboardGrafana.DashboardGrafanaTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c2aa684e9c0e6e78c831380fe15dc2da65b9dc3cbce00c7d62ada8f1fec1a98)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a4f5d32eaf29f86fd003f889766b410be8f5b5801c81b6e6df84429a4ce897d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8264f7bb5ec18e997867fcfe9cc8cfa58a0a8f0775393f70a74388bdafbabf1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76638bbf6cb02458b89241a64acbe819ffc0ed09f3c92ca3a95564805b0976eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff8fe0c5342b5b5595847e826efbc23063b80753212eee7c6a64e376ee34c69a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DashboardGrafanaTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DashboardGrafanaTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DashboardGrafanaTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c96dccb74e73f5507392aab7c3b1cefadd11fe9d69577c67c04969e13b9a72ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DashboardGrafana",
    "DashboardGrafanaAzureMonitorWorkspaceIntegrations",
    "DashboardGrafanaAzureMonitorWorkspaceIntegrationsList",
    "DashboardGrafanaAzureMonitorWorkspaceIntegrationsOutputReference",
    "DashboardGrafanaConfig",
    "DashboardGrafanaIdentity",
    "DashboardGrafanaIdentityOutputReference",
    "DashboardGrafanaSmtp",
    "DashboardGrafanaSmtpOutputReference",
    "DashboardGrafanaTimeouts",
    "DashboardGrafanaTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__cc5938b2c8ddc6b8644dc4f33200cbc13ac613f0f8d799c191941118dafc5bc6(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    grafana_major_version: builtins.str,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    api_key_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auto_generated_domain_name_label_scope: typing.Optional[builtins.str] = None,
    azure_monitor_workspace_integrations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DashboardGrafanaAzureMonitorWorkspaceIntegrations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    deterministic_outbound_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[DashboardGrafanaIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sku: typing.Optional[builtins.str] = None,
    smtp: typing.Optional[typing.Union[DashboardGrafanaSmtp, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[DashboardGrafanaTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    zone_redundancy_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__41f0a4539b7f30e6fc6868b27e446ef9b93d7a5eb8fe527a7416fb5c60044713(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ade56b9dc4341fb3c04a285c0f4fcd9c6bd499bda5007477d87559b2a6626e2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DashboardGrafanaAzureMonitorWorkspaceIntegrations, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bd3de7dfb9e3d5157ce2c4c3591f4e01436b55f2345d01d989d6aaab2c53303(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__538ba396c0c43df96f1a4b4cbdecfbe2e542847d7d9366089fde9d07aafdbe24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6656206d20c6ba253d70e24c1b37d2d978382cd9340f6bd0dbbc925cfe92832e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a55e67c6018b909592a2e71c1c1f1dfa5d7264851803e00424a2d73baa4690e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b538bc858a7f379a4a7ff677769bef2b30401a5ca739996e41854c655ba6935(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__989d738bd2150f87667069e448b2585c59552ef9661d203be66dfe8cc2e819f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__685673915e51f4bd5112b3daf90b87af77f4bf88353834a375e958ad4f407740(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e03cc25bbff8055ccb669f4f41039e952ab17f5c55890e9ecb6f0931583f7bd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9051dcbe3a7dd60d448982c7cf79ef166c5ee819c0c8473558054efcabc2c4be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7f533a832c4c92409a39162cd087e58a9315ce4b0fca908a750f7f7bc54db4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__797408c919cac079476e26852344c7ed1a014190f2bbfa560d6f4563894817d0(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ebe9cca76a8cb33b5fcad8e2e5548dc48b7cd3440880953799a109ca744b7f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e43aa4a8d245b695a5a3ed8800404f3bd95850f5359ed8f1d478d062b7d7f7b(
    *,
    resource_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b179933e6d6aea3aacbc598124c7fb01e7c6880e62bc46fc18e47709d046c495(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83c4a3c77785f824f92311a94c157e50281a48f89db3f3ba551dd5b0b9636cfc(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__773d5d1146b4c81a707b3eb2ad603323557991f9247acc375e93baee8ad6656b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__779b3b9bc792e9800473f4dcb0228a3c54098253500f11de746f48735680f560(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4f3832caad24d9db2926a4fb272542ba67fa2af333e2e05cb78d11e12bd6ae6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf8ffcc1f3715a5e64c4bdf3cd5c95ed2ccb756e812b32836704cf1670ca3be2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DashboardGrafanaAzureMonitorWorkspaceIntegrations]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53d226f7444cb227b597796a5e90ed2f1049361b9c4679de97e4fee2907f70d1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97989eeffe78f1714e31b1b7ee010eced9fa6fec2d36cbf2b7065fc442b83613(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b210ee86b1364fff38bae4819ec478d0c45f18f2c69b7e0f41e8b3ada1709d61(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DashboardGrafanaAzureMonitorWorkspaceIntegrations]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aa716058c0e4a73da5cc689aeff1d8aeaefe2dedf5d794edd0041951eb9f53c(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    grafana_major_version: builtins.str,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    api_key_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    auto_generated_domain_name_label_scope: typing.Optional[builtins.str] = None,
    azure_monitor_workspace_integrations: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DashboardGrafanaAzureMonitorWorkspaceIntegrations, typing.Dict[builtins.str, typing.Any]]]]] = None,
    deterministic_outbound_ip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    identity: typing.Optional[typing.Union[DashboardGrafanaIdentity, typing.Dict[builtins.str, typing.Any]]] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sku: typing.Optional[builtins.str] = None,
    smtp: typing.Optional[typing.Union[DashboardGrafanaSmtp, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[DashboardGrafanaTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    zone_redundancy_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__236c99dab129b07570cf389a1dea199490b3df544c9a3668dcb3cb0ebcf93a33(
    *,
    type: builtins.str,
    identity_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e02b88c1a971f9c5f8d5d2f38321f062eec16f727c4bea6a72f915a49724f79(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcd3adf404c4b7a11d0fe54af9932bed62cad994f2890d64050071c5238fbf23(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f73cf45ddc4481d371338317c0929f8c78564674c8129867fb383e1b4dc38dee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f6a0149bd1cfd8b7ecebce493d90f56018f3a4cc5978f5b504db4ef0d1bff97(
    value: typing.Optional[DashboardGrafanaIdentity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5941a50e34d9fc7b277fe178f8a5bc991e79758ea37a77ff70f6927e792ce7af(
    *,
    from_address: builtins.str,
    host: builtins.str,
    password: builtins.str,
    start_tls_policy: builtins.str,
    user: builtins.str,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    from_name: typing.Optional[builtins.str] = None,
    verification_skip_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31f8e839ee570e39e340101a33c83981177625fd49c064afc9fb9f1420830ee2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__650b9a9902ec70b41a1eee58426ceea63860b691d10eef3fbd46dbd6f65c864d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb0eb44d42327a8262080d60137d1be6c8567df152277a31951c19fd49c34378(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3112c5de272483205b2e18d522e5c4396129d27b650416dfd9410daeb5d0881d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3968e27189eddd242e8eddbbba28ea4a51d9135c26f8ba6e67432c9b1d672cab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4406b5ad24981b35886462905b151ee278898c0637490f975cb23a838ac91cc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e196cc0d6afabbf06b3efe3dff1125e08e75bee0b2229e5f2b0ede8fa448f715(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ca8eee0aa1a0497f2753df02f48b4f951aa9f4beaf173b230267a308474d7e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__badeece22233f33d6dc621d81f27a08101d8358d3ad513e4f3c1b48339c58948(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96591e45be7a56063ce3d149464b0d23613e2b1b402f45d76bb2bce6b4049af5(
    value: typing.Optional[DashboardGrafanaSmtp],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6231c9783352c2edc5ebd492568bf65d9d862e6b6691aa89a41ab8815cce0f12(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c2aa684e9c0e6e78c831380fe15dc2da65b9dc3cbce00c7d62ada8f1fec1a98(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a4f5d32eaf29f86fd003f889766b410be8f5b5801c81b6e6df84429a4ce897d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8264f7bb5ec18e997867fcfe9cc8cfa58a0a8f0775393f70a74388bdafbabf1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76638bbf6cb02458b89241a64acbe819ffc0ed09f3c92ca3a95564805b0976eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff8fe0c5342b5b5595847e826efbc23063b80753212eee7c6a64e376ee34c69a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c96dccb74e73f5507392aab7c3b1cefadd11fe9d69577c67c04969e13b9a72ef(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DashboardGrafanaTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
