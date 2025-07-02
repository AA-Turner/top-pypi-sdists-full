r'''
# `azurerm_container_app_environment`

Refer to the Terraform Registry for docs: [`azurerm_container_app_environment`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment).
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


class ContainerAppEnvironment(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppEnvironment.ContainerAppEnvironment",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment azurerm_container_app_environment}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        dapr_application_insights_connection_string: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        infrastructure_resource_group_name: typing.Optional[builtins.str] = None,
        infrastructure_subnet_id: typing.Optional[builtins.str] = None,
        internal_load_balancer_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_analytics_workspace_id: typing.Optional[builtins.str] = None,
        logs_destination: typing.Optional[builtins.str] = None,
        mutual_tls_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ContainerAppEnvironmentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        workload_profile: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppEnvironmentWorkloadProfile", typing.Dict[builtins.str, typing.Any]]]]] = None,
        zone_redundancy_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment azurerm_container_app_environment} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#location ContainerAppEnvironment#location}.
        :param name: The name of the Container Apps Managed Environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#name ContainerAppEnvironment#name}
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#resource_group_name ContainerAppEnvironment#resource_group_name}.
        :param dapr_application_insights_connection_string: Application Insights connection string used by Dapr to export Service to Service communication telemetry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#dapr_application_insights_connection_string ContainerAppEnvironment#dapr_application_insights_connection_string}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#id ContainerAppEnvironment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param infrastructure_resource_group_name: Name of the platform-managed resource group created for the Managed Environment to host infrastructure resources. **Note:** Only valid if a ``workload_profile`` is specified. If ``infrastructure_subnet_id`` is specified, this resource group will be created in the same subscription as ``infrastructure_subnet_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#infrastructure_resource_group_name ContainerAppEnvironment#infrastructure_resource_group_name}
        :param infrastructure_subnet_id: The existing Subnet to use for the Container Apps Control Plane. **NOTE:** The Subnet must have a ``/21`` or larger address space. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#infrastructure_subnet_id ContainerAppEnvironment#infrastructure_subnet_id}
        :param internal_load_balancer_enabled: Should the Container Environment operate in Internal Load Balancing Mode? Defaults to ``false``. **Note:** can only be set to ``true`` if ``infrastructure_subnet_id`` is specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#internal_load_balancer_enabled ContainerAppEnvironment#internal_load_balancer_enabled}
        :param log_analytics_workspace_id: The ID for the Log Analytics Workspace to link this Container Apps Managed Environment to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#log_analytics_workspace_id ContainerAppEnvironment#log_analytics_workspace_id}
        :param logs_destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#logs_destination ContainerAppEnvironment#logs_destination}.
        :param mutual_tls_enabled: Should mutual transport layer security (mTLS) be enabled? Defaults to ``false``. **Note:** This feature is in public preview. Enabling mTLS for your applications may increase response latency and reduce maximum throughput in high-load scenarios. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#mutual_tls_enabled ContainerAppEnvironment#mutual_tls_enabled}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#tags ContainerAppEnvironment#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#timeouts ContainerAppEnvironment#timeouts}
        :param workload_profile: workload_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#workload_profile ContainerAppEnvironment#workload_profile}
        :param zone_redundancy_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#zone_redundancy_enabled ContainerAppEnvironment#zone_redundancy_enabled}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b19d1d63817df063deff264aa6099885d5c35922b26d971bd877152c0a4ef02)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ContainerAppEnvironmentConfig(
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            dapr_application_insights_connection_string=dapr_application_insights_connection_string,
            id=id,
            infrastructure_resource_group_name=infrastructure_resource_group_name,
            infrastructure_subnet_id=infrastructure_subnet_id,
            internal_load_balancer_enabled=internal_load_balancer_enabled,
            log_analytics_workspace_id=log_analytics_workspace_id,
            logs_destination=logs_destination,
            mutual_tls_enabled=mutual_tls_enabled,
            tags=tags,
            timeouts=timeouts,
            workload_profile=workload_profile,
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
        '''Generates CDKTF code for importing a ContainerAppEnvironment resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ContainerAppEnvironment to import.
        :param import_from_id: The id of the existing ContainerAppEnvironment that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ContainerAppEnvironment to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d362b83216e81e073b324c99da6a7d57cab5af3d14d7b48e6c9c88c994156dc)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#create ContainerAppEnvironment#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#delete ContainerAppEnvironment#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#read ContainerAppEnvironment#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#update ContainerAppEnvironment#update}.
        '''
        value = ContainerAppEnvironmentTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putWorkloadProfile")
    def put_workload_profile(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppEnvironmentWorkloadProfile", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d5fce16627180207abd82fdcaf0f526ba25b063ec659e2dd344b892c810c4da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWorkloadProfile", [value]))

    @jsii.member(jsii_name="resetDaprApplicationInsightsConnectionString")
    def reset_dapr_application_insights_connection_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDaprApplicationInsightsConnectionString", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInfrastructureResourceGroupName")
    def reset_infrastructure_resource_group_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInfrastructureResourceGroupName", []))

    @jsii.member(jsii_name="resetInfrastructureSubnetId")
    def reset_infrastructure_subnet_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInfrastructureSubnetId", []))

    @jsii.member(jsii_name="resetInternalLoadBalancerEnabled")
    def reset_internal_load_balancer_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInternalLoadBalancerEnabled", []))

    @jsii.member(jsii_name="resetLogAnalyticsWorkspaceId")
    def reset_log_analytics_workspace_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogAnalyticsWorkspaceId", []))

    @jsii.member(jsii_name="resetLogsDestination")
    def reset_logs_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogsDestination", []))

    @jsii.member(jsii_name="resetMutualTlsEnabled")
    def reset_mutual_tls_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMutualTlsEnabled", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetWorkloadProfile")
    def reset_workload_profile(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWorkloadProfile", []))

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
    @jsii.member(jsii_name="customDomainVerificationId")
    def custom_domain_verification_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customDomainVerificationId"))

    @builtins.property
    @jsii.member(jsii_name="defaultDomain")
    def default_domain(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultDomain"))

    @builtins.property
    @jsii.member(jsii_name="dockerBridgeCidr")
    def docker_bridge_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "dockerBridgeCidr"))

    @builtins.property
    @jsii.member(jsii_name="platformReservedCidr")
    def platform_reserved_cidr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "platformReservedCidr"))

    @builtins.property
    @jsii.member(jsii_name="platformReservedDnsIpAddress")
    def platform_reserved_dns_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "platformReservedDnsIpAddress"))

    @builtins.property
    @jsii.member(jsii_name="staticIpAddress")
    def static_ip_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "staticIpAddress"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ContainerAppEnvironmentTimeoutsOutputReference":
        return typing.cast("ContainerAppEnvironmentTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="workloadProfile")
    def workload_profile(self) -> "ContainerAppEnvironmentWorkloadProfileList":
        return typing.cast("ContainerAppEnvironmentWorkloadProfileList", jsii.get(self, "workloadProfile"))

    @builtins.property
    @jsii.member(jsii_name="daprApplicationInsightsConnectionStringInput")
    def dapr_application_insights_connection_string_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "daprApplicationInsightsConnectionStringInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="infrastructureResourceGroupNameInput")
    def infrastructure_resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "infrastructureResourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="infrastructureSubnetIdInput")
    def infrastructure_subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "infrastructureSubnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="internalLoadBalancerEnabledInput")
    def internal_load_balancer_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalLoadBalancerEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsWorkspaceIdInput")
    def log_analytics_workspace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logAnalyticsWorkspaceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="logsDestinationInput")
    def logs_destination_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logsDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="mutualTlsEnabledInput")
    def mutual_tls_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mutualTlsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ContainerAppEnvironmentTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "ContainerAppEnvironmentTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="workloadProfileInput")
    def workload_profile_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppEnvironmentWorkloadProfile"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppEnvironmentWorkloadProfile"]]], jsii.get(self, "workloadProfileInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneRedundancyEnabledInput")
    def zone_redundancy_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "zoneRedundancyEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="daprApplicationInsightsConnectionString")
    def dapr_application_insights_connection_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "daprApplicationInsightsConnectionString"))

    @dapr_application_insights_connection_string.setter
    def dapr_application_insights_connection_string(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d797bff46364265dace8bfc85614919fe3db5eed8fb056831719d8faf5d7266c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daprApplicationInsightsConnectionString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12ccab076f5a1f46622ffe4ed6697862750b85f834f989a4b94232f37ed1c41d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="infrastructureResourceGroupName")
    def infrastructure_resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "infrastructureResourceGroupName"))

    @infrastructure_resource_group_name.setter
    def infrastructure_resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea8943b45b29c6f7385f26ddc1f5eac82fd58a3fc89c2afc5f0a2449e7f28962)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "infrastructureResourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="infrastructureSubnetId")
    def infrastructure_subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "infrastructureSubnetId"))

    @infrastructure_subnet_id.setter
    def infrastructure_subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__384f2f17ed3e2c65c86113291c3b30a978c44e915ced8a3536a11f383ffad008)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "infrastructureSubnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalLoadBalancerEnabled")
    def internal_load_balancer_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "internalLoadBalancerEnabled"))

    @internal_load_balancer_enabled.setter
    def internal_load_balancer_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__717d61fe7fa831480fd01b91d6603fd6e79a19c66f2a4cf79ef0cee5411857cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalLoadBalancerEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d071764688df555a9e018287a4461e239882891aa60475c18e4e9c8827953905)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsWorkspaceId")
    def log_analytics_workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logAnalyticsWorkspaceId"))

    @log_analytics_workspace_id.setter
    def log_analytics_workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8fa22bac16b617c8ec8694af3a0cb400e2cbb7380b1cbddf5543f91fc2b4ca8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logAnalyticsWorkspaceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logsDestination")
    def logs_destination(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logsDestination"))

    @logs_destination.setter
    def logs_destination(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0e45764ba4d3bd955e2fca9650163af105960f19e031cb2fd4bf9eac04d2619)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logsDestination", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mutualTlsEnabled")
    def mutual_tls_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mutualTlsEnabled"))

    @mutual_tls_enabled.setter
    def mutual_tls_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94badc7dc464057823f027608431de2613b406f7c29bad8378dc64c6cb6c8c0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mutualTlsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13478a6836404491ca2cd73ef1b2a787860c82a417d394bdab344733c7cd85d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cf11246a3f0522ec98a3627a0ff52d8c022b3730bfb67fa75eb71978366fb48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8d0b9e9209e4fe4fdaa4b9f9d78c11ed0ad8b09beae559140243eed8c713e2b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bb7f7ea039f29204c2ba9d5a000ff6504316c2758bf2cc2915009a9fb84268f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneRedundancyEnabled", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerAppEnvironment.ContainerAppEnvironmentConfig",
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
        "dapr_application_insights_connection_string": "daprApplicationInsightsConnectionString",
        "id": "id",
        "infrastructure_resource_group_name": "infrastructureResourceGroupName",
        "infrastructure_subnet_id": "infrastructureSubnetId",
        "internal_load_balancer_enabled": "internalLoadBalancerEnabled",
        "log_analytics_workspace_id": "logAnalyticsWorkspaceId",
        "logs_destination": "logsDestination",
        "mutual_tls_enabled": "mutualTlsEnabled",
        "tags": "tags",
        "timeouts": "timeouts",
        "workload_profile": "workloadProfile",
        "zone_redundancy_enabled": "zoneRedundancyEnabled",
    },
)
class ContainerAppEnvironmentConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        dapr_application_insights_connection_string: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        infrastructure_resource_group_name: typing.Optional[builtins.str] = None,
        infrastructure_subnet_id: typing.Optional[builtins.str] = None,
        internal_load_balancer_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        log_analytics_workspace_id: typing.Optional[builtins.str] = None,
        logs_destination: typing.Optional[builtins.str] = None,
        mutual_tls_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["ContainerAppEnvironmentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        workload_profile: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ContainerAppEnvironmentWorkloadProfile", typing.Dict[builtins.str, typing.Any]]]]] = None,
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
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#location ContainerAppEnvironment#location}.
        :param name: The name of the Container Apps Managed Environment. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#name ContainerAppEnvironment#name}
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#resource_group_name ContainerAppEnvironment#resource_group_name}.
        :param dapr_application_insights_connection_string: Application Insights connection string used by Dapr to export Service to Service communication telemetry. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#dapr_application_insights_connection_string ContainerAppEnvironment#dapr_application_insights_connection_string}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#id ContainerAppEnvironment#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param infrastructure_resource_group_name: Name of the platform-managed resource group created for the Managed Environment to host infrastructure resources. **Note:** Only valid if a ``workload_profile`` is specified. If ``infrastructure_subnet_id`` is specified, this resource group will be created in the same subscription as ``infrastructure_subnet_id``. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#infrastructure_resource_group_name ContainerAppEnvironment#infrastructure_resource_group_name}
        :param infrastructure_subnet_id: The existing Subnet to use for the Container Apps Control Plane. **NOTE:** The Subnet must have a ``/21`` or larger address space. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#infrastructure_subnet_id ContainerAppEnvironment#infrastructure_subnet_id}
        :param internal_load_balancer_enabled: Should the Container Environment operate in Internal Load Balancing Mode? Defaults to ``false``. **Note:** can only be set to ``true`` if ``infrastructure_subnet_id`` is specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#internal_load_balancer_enabled ContainerAppEnvironment#internal_load_balancer_enabled}
        :param log_analytics_workspace_id: The ID for the Log Analytics Workspace to link this Container Apps Managed Environment to. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#log_analytics_workspace_id ContainerAppEnvironment#log_analytics_workspace_id}
        :param logs_destination: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#logs_destination ContainerAppEnvironment#logs_destination}.
        :param mutual_tls_enabled: Should mutual transport layer security (mTLS) be enabled? Defaults to ``false``. **Note:** This feature is in public preview. Enabling mTLS for your applications may increase response latency and reduce maximum throughput in high-load scenarios. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#mutual_tls_enabled ContainerAppEnvironment#mutual_tls_enabled}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#tags ContainerAppEnvironment#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#timeouts ContainerAppEnvironment#timeouts}
        :param workload_profile: workload_profile block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#workload_profile ContainerAppEnvironment#workload_profile}
        :param zone_redundancy_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#zone_redundancy_enabled ContainerAppEnvironment#zone_redundancy_enabled}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = ContainerAppEnvironmentTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b386792634d6fafd95dad595d3471d9b506ef4d714f63215cd04c6ae07ae24e)
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
            check_type(argname="argument dapr_application_insights_connection_string", value=dapr_application_insights_connection_string, expected_type=type_hints["dapr_application_insights_connection_string"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument infrastructure_resource_group_name", value=infrastructure_resource_group_name, expected_type=type_hints["infrastructure_resource_group_name"])
            check_type(argname="argument infrastructure_subnet_id", value=infrastructure_subnet_id, expected_type=type_hints["infrastructure_subnet_id"])
            check_type(argname="argument internal_load_balancer_enabled", value=internal_load_balancer_enabled, expected_type=type_hints["internal_load_balancer_enabled"])
            check_type(argname="argument log_analytics_workspace_id", value=log_analytics_workspace_id, expected_type=type_hints["log_analytics_workspace_id"])
            check_type(argname="argument logs_destination", value=logs_destination, expected_type=type_hints["logs_destination"])
            check_type(argname="argument mutual_tls_enabled", value=mutual_tls_enabled, expected_type=type_hints["mutual_tls_enabled"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument workload_profile", value=workload_profile, expected_type=type_hints["workload_profile"])
            check_type(argname="argument zone_redundancy_enabled", value=zone_redundancy_enabled, expected_type=type_hints["zone_redundancy_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
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
        if dapr_application_insights_connection_string is not None:
            self._values["dapr_application_insights_connection_string"] = dapr_application_insights_connection_string
        if id is not None:
            self._values["id"] = id
        if infrastructure_resource_group_name is not None:
            self._values["infrastructure_resource_group_name"] = infrastructure_resource_group_name
        if infrastructure_subnet_id is not None:
            self._values["infrastructure_subnet_id"] = infrastructure_subnet_id
        if internal_load_balancer_enabled is not None:
            self._values["internal_load_balancer_enabled"] = internal_load_balancer_enabled
        if log_analytics_workspace_id is not None:
            self._values["log_analytics_workspace_id"] = log_analytics_workspace_id
        if logs_destination is not None:
            self._values["logs_destination"] = logs_destination
        if mutual_tls_enabled is not None:
            self._values["mutual_tls_enabled"] = mutual_tls_enabled
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if workload_profile is not None:
            self._values["workload_profile"] = workload_profile
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
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#location ContainerAppEnvironment#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the Container Apps Managed Environment.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#name ContainerAppEnvironment#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#resource_group_name ContainerAppEnvironment#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dapr_application_insights_connection_string(
        self,
    ) -> typing.Optional[builtins.str]:
        '''Application Insights connection string used by Dapr to export Service to Service communication telemetry.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#dapr_application_insights_connection_string ContainerAppEnvironment#dapr_application_insights_connection_string}
        '''
        result = self._values.get("dapr_application_insights_connection_string")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#id ContainerAppEnvironment#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def infrastructure_resource_group_name(self) -> typing.Optional[builtins.str]:
        '''Name of the platform-managed resource group created for the Managed Environment to host infrastructure resources.

        **Note:** Only valid if a ``workload_profile`` is specified. If ``infrastructure_subnet_id`` is specified, this resource group will be created in the same subscription as ``infrastructure_subnet_id``.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#infrastructure_resource_group_name ContainerAppEnvironment#infrastructure_resource_group_name}
        '''
        result = self._values.get("infrastructure_resource_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def infrastructure_subnet_id(self) -> typing.Optional[builtins.str]:
        '''The existing Subnet to use for the Container Apps Control Plane.

        **NOTE:** The Subnet must have a ``/21`` or larger address space.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#infrastructure_subnet_id ContainerAppEnvironment#infrastructure_subnet_id}
        '''
        result = self._values.get("infrastructure_subnet_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def internal_load_balancer_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should the Container Environment operate in Internal Load Balancing Mode?

        Defaults to ``false``. **Note:** can only be set to ``true`` if ``infrastructure_subnet_id`` is specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#internal_load_balancer_enabled ContainerAppEnvironment#internal_load_balancer_enabled}
        '''
        result = self._values.get("internal_load_balancer_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def log_analytics_workspace_id(self) -> typing.Optional[builtins.str]:
        '''The ID for the Log Analytics Workspace to link this Container Apps Managed Environment to.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#log_analytics_workspace_id ContainerAppEnvironment#log_analytics_workspace_id}
        '''
        result = self._values.get("log_analytics_workspace_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def logs_destination(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#logs_destination ContainerAppEnvironment#logs_destination}.'''
        result = self._values.get("logs_destination")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mutual_tls_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Should mutual transport layer security (mTLS) be enabled?

        Defaults to ``false``. **Note:** This feature is in public preview. Enabling mTLS for your applications may increase response latency and reduce maximum throughput in high-load scenarios.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#mutual_tls_enabled ContainerAppEnvironment#mutual_tls_enabled}
        '''
        result = self._values.get("mutual_tls_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#tags ContainerAppEnvironment#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ContainerAppEnvironmentTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#timeouts ContainerAppEnvironment#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ContainerAppEnvironmentTimeouts"], result)

    @builtins.property
    def workload_profile(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppEnvironmentWorkloadProfile"]]]:
        '''workload_profile block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#workload_profile ContainerAppEnvironment#workload_profile}
        '''
        result = self._values.get("workload_profile")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ContainerAppEnvironmentWorkloadProfile"]]], result)

    @builtins.property
    def zone_redundancy_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#zone_redundancy_enabled ContainerAppEnvironment#zone_redundancy_enabled}.'''
        result = self._values.get("zone_redundancy_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppEnvironmentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerAppEnvironment.ContainerAppEnvironmentTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ContainerAppEnvironmentTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#create ContainerAppEnvironment#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#delete ContainerAppEnvironment#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#read ContainerAppEnvironment#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#update ContainerAppEnvironment#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77002480c8b8fc35e7b2ccb1995e4fd16cf516706af269da88d3bbaaef9a9584)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#create ContainerAppEnvironment#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#delete ContainerAppEnvironment#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#read ContainerAppEnvironment#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#update ContainerAppEnvironment#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppEnvironmentTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppEnvironmentTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppEnvironment.ContainerAppEnvironmentTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__71df354c34d390cf6c38450a9a2c71cce033901c5e1d80e59fcb3b2db774ab1d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c8f85371fc45747916cf6b5160b137f25e505a2af53dfde5f98eb86b77f7df9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f49bfcd88890f7a84c561437ce4af0b03eba8b0ad24e0aa4e601e10c8bc1d50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91163d1f299d8a10782a2622c7a24ed9a9e817cc167876d5ca6b3fdd5effe07a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5cba22481f20fed1f70b2c67b6caf0efec87340e7dc641ffddc619990b12611)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppEnvironmentTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppEnvironmentTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppEnvironmentTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a9ef2e0df0894d37f86c6a612e1ea8aed07699ac535bf76448988c60146ff46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.containerAppEnvironment.ContainerAppEnvironmentWorkloadProfile",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "workload_profile_type": "workloadProfileType",
        "maximum_count": "maximumCount",
        "minimum_count": "minimumCount",
    },
)
class ContainerAppEnvironmentWorkloadProfile:
    def __init__(
        self,
        *,
        name: builtins.str,
        workload_profile_type: builtins.str,
        maximum_count: typing.Optional[jsii.Number] = None,
        minimum_count: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#name ContainerAppEnvironment#name}.
        :param workload_profile_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#workload_profile_type ContainerAppEnvironment#workload_profile_type}.
        :param maximum_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#maximum_count ContainerAppEnvironment#maximum_count}.
        :param minimum_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#minimum_count ContainerAppEnvironment#minimum_count}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b0463b13c8e676ff930196425588a055eafab3237fb455e5a6601e6233bff14)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument workload_profile_type", value=workload_profile_type, expected_type=type_hints["workload_profile_type"])
            check_type(argname="argument maximum_count", value=maximum_count, expected_type=type_hints["maximum_count"])
            check_type(argname="argument minimum_count", value=minimum_count, expected_type=type_hints["minimum_count"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "workload_profile_type": workload_profile_type,
        }
        if maximum_count is not None:
            self._values["maximum_count"] = maximum_count
        if minimum_count is not None:
            self._values["minimum_count"] = minimum_count

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#name ContainerAppEnvironment#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def workload_profile_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#workload_profile_type ContainerAppEnvironment#workload_profile_type}.'''
        result = self._values.get("workload_profile_type")
        assert result is not None, "Required property 'workload_profile_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def maximum_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#maximum_count ContainerAppEnvironment#maximum_count}.'''
        result = self._values.get("maximum_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def minimum_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/container_app_environment#minimum_count ContainerAppEnvironment#minimum_count}.'''
        result = self._values.get("minimum_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerAppEnvironmentWorkloadProfile(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ContainerAppEnvironmentWorkloadProfileList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppEnvironment.ContainerAppEnvironmentWorkloadProfileList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__335b942a8917a7923af5356de25f75cbd0b66b802f6cfc7c491ba58ba9d0064f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ContainerAppEnvironmentWorkloadProfileOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15ab9956e9b412cd7a0fbf2e976ed6b9d4253b39002a775ffff9805e2ed8f923)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ContainerAppEnvironmentWorkloadProfileOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f00def140bc64d1b83d424da532617048cf80847930923c9ea91afdb107b55b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b91fb8fa42760c33cab7bf497e2d558a426b35d4f6217b31e947bd5d6b5fe408)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b63a8121c1a399e0ec410bfa671ce2572e4df6854250ec7d4ad175e8cafe22b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppEnvironmentWorkloadProfile]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppEnvironmentWorkloadProfile]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppEnvironmentWorkloadProfile]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0f7be23316f8623a9677410be70c6aa769af33672088b04727a56d8d41fc359)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ContainerAppEnvironmentWorkloadProfileOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.containerAppEnvironment.ContainerAppEnvironmentWorkloadProfileOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfa1367d3caf887219ba66cee3db982f79a08f105cfd486276c5dc591d63ba95)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetMaximumCount")
    def reset_maximum_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaximumCount", []))

    @jsii.member(jsii_name="resetMinimumCount")
    def reset_minimum_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMinimumCount", []))

    @builtins.property
    @jsii.member(jsii_name="maximumCountInput")
    def maximum_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maximumCountInput"))

    @builtins.property
    @jsii.member(jsii_name="minimumCountInput")
    def minimum_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minimumCountInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="workloadProfileTypeInput")
    def workload_profile_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workloadProfileTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="maximumCount")
    def maximum_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maximumCount"))

    @maximum_count.setter
    def maximum_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__332e66a785fb699a83e4435d936d2cced69cdb9ecfc6e4bb70fd4e37db183832)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="minimumCount")
    def minimum_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "minimumCount"))

    @minimum_count.setter
    def minimum_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e223f2af7dd916c6d6a9a51c592366920782658a1f0fade90ce2bae2074e433)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3e9be187254f7d15bf22e6c954d8f50a5f95e5768cdb14174090dfba8701393)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workloadProfileType")
    def workload_profile_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workloadProfileType"))

    @workload_profile_type.setter
    def workload_profile_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c48530a3a71ad0076fce21c5ff15d1a4c2438785f0ff7792fdd47d17e8f7f63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workloadProfileType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppEnvironmentWorkloadProfile]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppEnvironmentWorkloadProfile]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppEnvironmentWorkloadProfile]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69bfbe134eccf54bea69062bc63c69c04ece8c6d418871ef3f4166046cd7c1c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ContainerAppEnvironment",
    "ContainerAppEnvironmentConfig",
    "ContainerAppEnvironmentTimeouts",
    "ContainerAppEnvironmentTimeoutsOutputReference",
    "ContainerAppEnvironmentWorkloadProfile",
    "ContainerAppEnvironmentWorkloadProfileList",
    "ContainerAppEnvironmentWorkloadProfileOutputReference",
]

publication.publish()

def _typecheckingstub__7b19d1d63817df063deff264aa6099885d5c35922b26d971bd877152c0a4ef02(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    dapr_application_insights_connection_string: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    infrastructure_resource_group_name: typing.Optional[builtins.str] = None,
    infrastructure_subnet_id: typing.Optional[builtins.str] = None,
    internal_load_balancer_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    log_analytics_workspace_id: typing.Optional[builtins.str] = None,
    logs_destination: typing.Optional[builtins.str] = None,
    mutual_tls_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ContainerAppEnvironmentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    workload_profile: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppEnvironmentWorkloadProfile, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__6d362b83216e81e073b324c99da6a7d57cab5af3d14d7b48e6c9c88c994156dc(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d5fce16627180207abd82fdcaf0f526ba25b063ec659e2dd344b892c810c4da(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppEnvironmentWorkloadProfile, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d797bff46364265dace8bfc85614919fe3db5eed8fb056831719d8faf5d7266c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12ccab076f5a1f46622ffe4ed6697862750b85f834f989a4b94232f37ed1c41d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea8943b45b29c6f7385f26ddc1f5eac82fd58a3fc89c2afc5f0a2449e7f28962(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__384f2f17ed3e2c65c86113291c3b30a978c44e915ced8a3536a11f383ffad008(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__717d61fe7fa831480fd01b91d6603fd6e79a19c66f2a4cf79ef0cee5411857cd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d071764688df555a9e018287a4461e239882891aa60475c18e4e9c8827953905(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8fa22bac16b617c8ec8694af3a0cb400e2cbb7380b1cbddf5543f91fc2b4ca8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0e45764ba4d3bd955e2fca9650163af105960f19e031cb2fd4bf9eac04d2619(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94badc7dc464057823f027608431de2613b406f7c29bad8378dc64c6cb6c8c0e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13478a6836404491ca2cd73ef1b2a787860c82a417d394bdab344733c7cd85d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cf11246a3f0522ec98a3627a0ff52d8c022b3730bfb67fa75eb71978366fb48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8d0b9e9209e4fe4fdaa4b9f9d78c11ed0ad8b09beae559140243eed8c713e2b(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bb7f7ea039f29204c2ba9d5a000ff6504316c2758bf2cc2915009a9fb84268f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b386792634d6fafd95dad595d3471d9b506ef4d714f63215cd04c6ae07ae24e(
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
    dapr_application_insights_connection_string: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    infrastructure_resource_group_name: typing.Optional[builtins.str] = None,
    infrastructure_subnet_id: typing.Optional[builtins.str] = None,
    internal_load_balancer_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    log_analytics_workspace_id: typing.Optional[builtins.str] = None,
    logs_destination: typing.Optional[builtins.str] = None,
    mutual_tls_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[ContainerAppEnvironmentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    workload_profile: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ContainerAppEnvironmentWorkloadProfile, typing.Dict[builtins.str, typing.Any]]]]] = None,
    zone_redundancy_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77002480c8b8fc35e7b2ccb1995e4fd16cf516706af269da88d3bbaaef9a9584(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71df354c34d390cf6c38450a9a2c71cce033901c5e1d80e59fcb3b2db774ab1d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c8f85371fc45747916cf6b5160b137f25e505a2af53dfde5f98eb86b77f7df9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f49bfcd88890f7a84c561437ce4af0b03eba8b0ad24e0aa4e601e10c8bc1d50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91163d1f299d8a10782a2622c7a24ed9a9e817cc167876d5ca6b3fdd5effe07a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5cba22481f20fed1f70b2c67b6caf0efec87340e7dc641ffddc619990b12611(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a9ef2e0df0894d37f86c6a612e1ea8aed07699ac535bf76448988c60146ff46(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppEnvironmentTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b0463b13c8e676ff930196425588a055eafab3237fb455e5a6601e6233bff14(
    *,
    name: builtins.str,
    workload_profile_type: builtins.str,
    maximum_count: typing.Optional[jsii.Number] = None,
    minimum_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__335b942a8917a7923af5356de25f75cbd0b66b802f6cfc7c491ba58ba9d0064f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15ab9956e9b412cd7a0fbf2e976ed6b9d4253b39002a775ffff9805e2ed8f923(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f00def140bc64d1b83d424da532617048cf80847930923c9ea91afdb107b55b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b91fb8fa42760c33cab7bf497e2d558a426b35d4f6217b31e947bd5d6b5fe408(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b63a8121c1a399e0ec410bfa671ce2572e4df6854250ec7d4ad175e8cafe22b1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0f7be23316f8623a9677410be70c6aa769af33672088b04727a56d8d41fc359(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ContainerAppEnvironmentWorkloadProfile]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfa1367d3caf887219ba66cee3db982f79a08f105cfd486276c5dc591d63ba95(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__332e66a785fb699a83e4435d936d2cced69cdb9ecfc6e4bb70fd4e37db183832(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e223f2af7dd916c6d6a9a51c592366920782658a1f0fade90ce2bae2074e433(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3e9be187254f7d15bf22e6c954d8f50a5f95e5768cdb14174090dfba8701393(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c48530a3a71ad0076fce21c5ff15d1a4c2438785f0ff7792fdd47d17e8f7f63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69bfbe134eccf54bea69062bc63c69c04ece8c6d418871ef3f4166046cd7c1c7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ContainerAppEnvironmentWorkloadProfile]],
) -> None:
    """Type checking stubs"""
    pass
