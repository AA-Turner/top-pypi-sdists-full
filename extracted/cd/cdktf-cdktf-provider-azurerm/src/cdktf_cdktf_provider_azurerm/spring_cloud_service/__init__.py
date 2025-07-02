r'''
# `azurerm_spring_cloud_service`

Refer to the Terraform Registry for docs: [`azurerm_spring_cloud_service`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service).
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


class SpringCloudService(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudService.SpringCloudService",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service azurerm_spring_cloud_service}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        build_agent_pool_size: typing.Optional[builtins.str] = None,
        config_server_git_setting: typing.Optional[typing.Union["SpringCloudServiceConfigServerGitSetting", typing.Dict[builtins.str, typing.Any]]] = None,
        container_registry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SpringCloudServiceContainerRegistry", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_build_service: typing.Optional[typing.Union["SpringCloudServiceDefaultBuildService", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        log_stream_public_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        managed_environment_id: typing.Optional[builtins.str] = None,
        marketplace: typing.Optional[typing.Union["SpringCloudServiceMarketplace", typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[typing.Union["SpringCloudServiceNetwork", typing.Dict[builtins.str, typing.Any]]] = None,
        service_registry_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sku_name: typing.Optional[builtins.str] = None,
        sku_tier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["SpringCloudServiceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        trace: typing.Optional[typing.Union["SpringCloudServiceTrace", typing.Dict[builtins.str, typing.Any]]] = None,
        zone_redundant: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service azurerm_spring_cloud_service} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#location SpringCloudService#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#name SpringCloudService#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#resource_group_name SpringCloudService#resource_group_name}.
        :param build_agent_pool_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#build_agent_pool_size SpringCloudService#build_agent_pool_size}.
        :param config_server_git_setting: config_server_git_setting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#config_server_git_setting SpringCloudService#config_server_git_setting}
        :param container_registry: container_registry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#container_registry SpringCloudService#container_registry}
        :param default_build_service: default_build_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#default_build_service SpringCloudService#default_build_service}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#id SpringCloudService#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_stream_public_endpoint_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#log_stream_public_endpoint_enabled SpringCloudService#log_stream_public_endpoint_enabled}.
        :param managed_environment_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#managed_environment_id SpringCloudService#managed_environment_id}.
        :param marketplace: marketplace block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#marketplace SpringCloudService#marketplace}
        :param network: network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#network SpringCloudService#network}
        :param service_registry_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#service_registry_enabled SpringCloudService#service_registry_enabled}.
        :param sku_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#sku_name SpringCloudService#sku_name}.
        :param sku_tier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#sku_tier SpringCloudService#sku_tier}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#tags SpringCloudService#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#timeouts SpringCloudService#timeouts}
        :param trace: trace block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#trace SpringCloudService#trace}
        :param zone_redundant: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#zone_redundant SpringCloudService#zone_redundant}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1702dd28d1d9db9d7be035e7419a2e28152baa57c7fc95402841159f4ec39e76)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SpringCloudServiceConfig(
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            build_agent_pool_size=build_agent_pool_size,
            config_server_git_setting=config_server_git_setting,
            container_registry=container_registry,
            default_build_service=default_build_service,
            id=id,
            log_stream_public_endpoint_enabled=log_stream_public_endpoint_enabled,
            managed_environment_id=managed_environment_id,
            marketplace=marketplace,
            network=network,
            service_registry_enabled=service_registry_enabled,
            sku_name=sku_name,
            sku_tier=sku_tier,
            tags=tags,
            timeouts=timeouts,
            trace=trace,
            zone_redundant=zone_redundant,
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
        '''Generates CDKTF code for importing a SpringCloudService resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SpringCloudService to import.
        :param import_from_id: The id of the existing SpringCloudService that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SpringCloudService to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad35bbcc47b03eeee4181155d67373d01fe8e0d51b1ba3618299222a894f7e77)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putConfigServerGitSetting")
    def put_config_server_git_setting(
        self,
        *,
        uri: builtins.str,
        http_basic_auth: typing.Optional[typing.Union["SpringCloudServiceConfigServerGitSettingHttpBasicAuth", typing.Dict[builtins.str, typing.Any]]] = None,
        label: typing.Optional[builtins.str] = None,
        repository: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SpringCloudServiceConfigServerGitSettingRepository", typing.Dict[builtins.str, typing.Any]]]]] = None,
        search_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        ssh_auth: typing.Optional[typing.Union["SpringCloudServiceConfigServerGitSettingSshAuth", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#uri SpringCloudService#uri}.
        :param http_basic_auth: http_basic_auth block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#http_basic_auth SpringCloudService#http_basic_auth}
        :param label: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#label SpringCloudService#label}.
        :param repository: repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#repository SpringCloudService#repository}
        :param search_paths: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#search_paths SpringCloudService#search_paths}.
        :param ssh_auth: ssh_auth block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#ssh_auth SpringCloudService#ssh_auth}
        '''
        value = SpringCloudServiceConfigServerGitSetting(
            uri=uri,
            http_basic_auth=http_basic_auth,
            label=label,
            repository=repository,
            search_paths=search_paths,
            ssh_auth=ssh_auth,
        )

        return typing.cast(None, jsii.invoke(self, "putConfigServerGitSetting", [value]))

    @jsii.member(jsii_name="putContainerRegistry")
    def put_container_registry(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SpringCloudServiceContainerRegistry", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39638aee9671f45d58d6bba2a314939da3a0c386ee157ab14b3592cd0067b636)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putContainerRegistry", [value]))

    @jsii.member(jsii_name="putDefaultBuildService")
    def put_default_build_service(
        self,
        *,
        container_registry_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container_registry_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#container_registry_name SpringCloudService#container_registry_name}.
        '''
        value = SpringCloudServiceDefaultBuildService(
            container_registry_name=container_registry_name
        )

        return typing.cast(None, jsii.invoke(self, "putDefaultBuildService", [value]))

    @jsii.member(jsii_name="putMarketplace")
    def put_marketplace(
        self,
        *,
        plan: builtins.str,
        product: builtins.str,
        publisher: builtins.str,
    ) -> None:
        '''
        :param plan: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#plan SpringCloudService#plan}.
        :param product: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#product SpringCloudService#product}.
        :param publisher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#publisher SpringCloudService#publisher}.
        '''
        value = SpringCloudServiceMarketplace(
            plan=plan, product=product, publisher=publisher
        )

        return typing.cast(None, jsii.invoke(self, "putMarketplace", [value]))

    @jsii.member(jsii_name="putNetwork")
    def put_network(
        self,
        *,
        app_subnet_id: builtins.str,
        cidr_ranges: typing.Sequence[builtins.str],
        service_runtime_subnet_id: builtins.str,
        app_network_resource_group: typing.Optional[builtins.str] = None,
        outbound_type: typing.Optional[builtins.str] = None,
        read_timeout_seconds: typing.Optional[jsii.Number] = None,
        service_runtime_network_resource_group: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param app_subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#app_subnet_id SpringCloudService#app_subnet_id}.
        :param cidr_ranges: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#cidr_ranges SpringCloudService#cidr_ranges}.
        :param service_runtime_subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#service_runtime_subnet_id SpringCloudService#service_runtime_subnet_id}.
        :param app_network_resource_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#app_network_resource_group SpringCloudService#app_network_resource_group}.
        :param outbound_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#outbound_type SpringCloudService#outbound_type}.
        :param read_timeout_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#read_timeout_seconds SpringCloudService#read_timeout_seconds}.
        :param service_runtime_network_resource_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#service_runtime_network_resource_group SpringCloudService#service_runtime_network_resource_group}.
        '''
        value = SpringCloudServiceNetwork(
            app_subnet_id=app_subnet_id,
            cidr_ranges=cidr_ranges,
            service_runtime_subnet_id=service_runtime_subnet_id,
            app_network_resource_group=app_network_resource_group,
            outbound_type=outbound_type,
            read_timeout_seconds=read_timeout_seconds,
            service_runtime_network_resource_group=service_runtime_network_resource_group,
        )

        return typing.cast(None, jsii.invoke(self, "putNetwork", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#create SpringCloudService#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#delete SpringCloudService#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#read SpringCloudService#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#update SpringCloudService#update}.
        '''
        value = SpringCloudServiceTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putTrace")
    def put_trace(
        self,
        *,
        connection_string: typing.Optional[builtins.str] = None,
        sample_rate: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection_string: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#connection_string SpringCloudService#connection_string}.
        :param sample_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#sample_rate SpringCloudService#sample_rate}.
        '''
        value = SpringCloudServiceTrace(
            connection_string=connection_string, sample_rate=sample_rate
        )

        return typing.cast(None, jsii.invoke(self, "putTrace", [value]))

    @jsii.member(jsii_name="resetBuildAgentPoolSize")
    def reset_build_agent_pool_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBuildAgentPoolSize", []))

    @jsii.member(jsii_name="resetConfigServerGitSetting")
    def reset_config_server_git_setting(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfigServerGitSetting", []))

    @jsii.member(jsii_name="resetContainerRegistry")
    def reset_container_registry(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerRegistry", []))

    @jsii.member(jsii_name="resetDefaultBuildService")
    def reset_default_build_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultBuildService", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLogStreamPublicEndpointEnabled")
    def reset_log_stream_public_endpoint_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogStreamPublicEndpointEnabled", []))

    @jsii.member(jsii_name="resetManagedEnvironmentId")
    def reset_managed_environment_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetManagedEnvironmentId", []))

    @jsii.member(jsii_name="resetMarketplace")
    def reset_marketplace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMarketplace", []))

    @jsii.member(jsii_name="resetNetwork")
    def reset_network(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetwork", []))

    @jsii.member(jsii_name="resetServiceRegistryEnabled")
    def reset_service_registry_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceRegistryEnabled", []))

    @jsii.member(jsii_name="resetSkuName")
    def reset_sku_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkuName", []))

    @jsii.member(jsii_name="resetSkuTier")
    def reset_sku_tier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkuTier", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTrace")
    def reset_trace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrace", []))

    @jsii.member(jsii_name="resetZoneRedundant")
    def reset_zone_redundant(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetZoneRedundant", []))

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
    @jsii.member(jsii_name="configServerGitSetting")
    def config_server_git_setting(
        self,
    ) -> "SpringCloudServiceConfigServerGitSettingOutputReference":
        return typing.cast("SpringCloudServiceConfigServerGitSettingOutputReference", jsii.get(self, "configServerGitSetting"))

    @builtins.property
    @jsii.member(jsii_name="containerRegistry")
    def container_registry(self) -> "SpringCloudServiceContainerRegistryList":
        return typing.cast("SpringCloudServiceContainerRegistryList", jsii.get(self, "containerRegistry"))

    @builtins.property
    @jsii.member(jsii_name="defaultBuildService")
    def default_build_service(
        self,
    ) -> "SpringCloudServiceDefaultBuildServiceOutputReference":
        return typing.cast("SpringCloudServiceDefaultBuildServiceOutputReference", jsii.get(self, "defaultBuildService"))

    @builtins.property
    @jsii.member(jsii_name="marketplace")
    def marketplace(self) -> "SpringCloudServiceMarketplaceOutputReference":
        return typing.cast("SpringCloudServiceMarketplaceOutputReference", jsii.get(self, "marketplace"))

    @builtins.property
    @jsii.member(jsii_name="network")
    def network(self) -> "SpringCloudServiceNetworkOutputReference":
        return typing.cast("SpringCloudServiceNetworkOutputReference", jsii.get(self, "network"))

    @builtins.property
    @jsii.member(jsii_name="outboundPublicIpAddresses")
    def outbound_public_ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "outboundPublicIpAddresses"))

    @builtins.property
    @jsii.member(jsii_name="requiredNetworkTrafficRules")
    def required_network_traffic_rules(
        self,
    ) -> "SpringCloudServiceRequiredNetworkTrafficRulesList":
        return typing.cast("SpringCloudServiceRequiredNetworkTrafficRulesList", jsii.get(self, "requiredNetworkTrafficRules"))

    @builtins.property
    @jsii.member(jsii_name="serviceRegistryId")
    def service_registry_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceRegistryId"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "SpringCloudServiceTimeoutsOutputReference":
        return typing.cast("SpringCloudServiceTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="trace")
    def trace(self) -> "SpringCloudServiceTraceOutputReference":
        return typing.cast("SpringCloudServiceTraceOutputReference", jsii.get(self, "trace"))

    @builtins.property
    @jsii.member(jsii_name="buildAgentPoolSizeInput")
    def build_agent_pool_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "buildAgentPoolSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="configServerGitSettingInput")
    def config_server_git_setting_input(
        self,
    ) -> typing.Optional["SpringCloudServiceConfigServerGitSetting"]:
        return typing.cast(typing.Optional["SpringCloudServiceConfigServerGitSetting"], jsii.get(self, "configServerGitSettingInput"))

    @builtins.property
    @jsii.member(jsii_name="containerRegistryInput")
    def container_registry_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SpringCloudServiceContainerRegistry"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SpringCloudServiceContainerRegistry"]]], jsii.get(self, "containerRegistryInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultBuildServiceInput")
    def default_build_service_input(
        self,
    ) -> typing.Optional["SpringCloudServiceDefaultBuildService"]:
        return typing.cast(typing.Optional["SpringCloudServiceDefaultBuildService"], jsii.get(self, "defaultBuildServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="logStreamPublicEndpointEnabledInput")
    def log_stream_public_endpoint_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "logStreamPublicEndpointEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="managedEnvironmentIdInput")
    def managed_environment_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managedEnvironmentIdInput"))

    @builtins.property
    @jsii.member(jsii_name="marketplaceInput")
    def marketplace_input(self) -> typing.Optional["SpringCloudServiceMarketplace"]:
        return typing.cast(typing.Optional["SpringCloudServiceMarketplace"], jsii.get(self, "marketplaceInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="networkInput")
    def network_input(self) -> typing.Optional["SpringCloudServiceNetwork"]:
        return typing.cast(typing.Optional["SpringCloudServiceNetwork"], jsii.get(self, "networkInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceRegistryEnabledInput")
    def service_registry_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "serviceRegistryEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="skuNameInput")
    def sku_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "skuNameInput"))

    @builtins.property
    @jsii.member(jsii_name="skuTierInput")
    def sku_tier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "skuTierInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SpringCloudServiceTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SpringCloudServiceTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="traceInput")
    def trace_input(self) -> typing.Optional["SpringCloudServiceTrace"]:
        return typing.cast(typing.Optional["SpringCloudServiceTrace"], jsii.get(self, "traceInput"))

    @builtins.property
    @jsii.member(jsii_name="zoneRedundantInput")
    def zone_redundant_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "zoneRedundantInput"))

    @builtins.property
    @jsii.member(jsii_name="buildAgentPoolSize")
    def build_agent_pool_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "buildAgentPoolSize"))

    @build_agent_pool_size.setter
    def build_agent_pool_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__523b227bc339dfafd2d32dd936f006061df773c0220770dbd68baf0cb220cdc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buildAgentPoolSize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80d6bc42bdb9af348eb094fc1f277e739f09281d03d42990834933818916ca67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d13564b34e46fd63e34f1ab9cf5c649225e302ff84671592bab6b4e5c327bfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logStreamPublicEndpointEnabled")
    def log_stream_public_endpoint_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "logStreamPublicEndpointEnabled"))

    @log_stream_public_endpoint_enabled.setter
    def log_stream_public_endpoint_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aad94ca0dd2e90d8e05d871d3bd13dadac5c2dcbb13dad3056238f411b319fcb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logStreamPublicEndpointEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="managedEnvironmentId")
    def managed_environment_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managedEnvironmentId"))

    @managed_environment_id.setter
    def managed_environment_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f56193208be4fb8428aca748ad086edc60fdef3ef45928c482c99efce30d3e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedEnvironmentId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aba4130e08d36d0b8fd2579f67924266eb7b456a15884326f5b17b9e75f1cd75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5514d5b56bc3c6e292ade1d5e9208f54b04c73bebc61e51634fbdb28bc46fed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceRegistryEnabled")
    def service_registry_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "serviceRegistryEnabled"))

    @service_registry_enabled.setter
    def service_registry_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2640e539db73f429d5ce5742e15cad3f1537fd520ebd660784f1a56fbec4fdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceRegistryEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skuName")
    def sku_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "skuName"))

    @sku_name.setter
    def sku_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37179df683b8fb159382526be9e73d3e846acfc82b2a61a284bc0a6cda6214f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skuName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skuTier")
    def sku_tier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "skuTier"))

    @sku_tier.setter
    def sku_tier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f39bee6b9393a26f7ce980b335ccb5ab73cbfee36766bde07d3652624c3a437)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skuTier", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d3b72ca445a5271005a2e892291a760357120f1d62df7d989423d5313937bd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="zoneRedundant")
    def zone_redundant(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "zoneRedundant"))

    @zone_redundant.setter
    def zone_redundant(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7992ee5d04d6152937bb1ae0b3d5bdc69dffc926c26782f89e612b209fa90822)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "zoneRedundant", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.springCloudService.SpringCloudServiceConfig",
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
        "build_agent_pool_size": "buildAgentPoolSize",
        "config_server_git_setting": "configServerGitSetting",
        "container_registry": "containerRegistry",
        "default_build_service": "defaultBuildService",
        "id": "id",
        "log_stream_public_endpoint_enabled": "logStreamPublicEndpointEnabled",
        "managed_environment_id": "managedEnvironmentId",
        "marketplace": "marketplace",
        "network": "network",
        "service_registry_enabled": "serviceRegistryEnabled",
        "sku_name": "skuName",
        "sku_tier": "skuTier",
        "tags": "tags",
        "timeouts": "timeouts",
        "trace": "trace",
        "zone_redundant": "zoneRedundant",
    },
)
class SpringCloudServiceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        build_agent_pool_size: typing.Optional[builtins.str] = None,
        config_server_git_setting: typing.Optional[typing.Union["SpringCloudServiceConfigServerGitSetting", typing.Dict[builtins.str, typing.Any]]] = None,
        container_registry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SpringCloudServiceContainerRegistry", typing.Dict[builtins.str, typing.Any]]]]] = None,
        default_build_service: typing.Optional[typing.Union["SpringCloudServiceDefaultBuildService", typing.Dict[builtins.str, typing.Any]]] = None,
        id: typing.Optional[builtins.str] = None,
        log_stream_public_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        managed_environment_id: typing.Optional[builtins.str] = None,
        marketplace: typing.Optional[typing.Union["SpringCloudServiceMarketplace", typing.Dict[builtins.str, typing.Any]]] = None,
        network: typing.Optional[typing.Union["SpringCloudServiceNetwork", typing.Dict[builtins.str, typing.Any]]] = None,
        service_registry_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        sku_name: typing.Optional[builtins.str] = None,
        sku_tier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["SpringCloudServiceTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        trace: typing.Optional[typing.Union["SpringCloudServiceTrace", typing.Dict[builtins.str, typing.Any]]] = None,
        zone_redundant: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#location SpringCloudService#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#name SpringCloudService#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#resource_group_name SpringCloudService#resource_group_name}.
        :param build_agent_pool_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#build_agent_pool_size SpringCloudService#build_agent_pool_size}.
        :param config_server_git_setting: config_server_git_setting block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#config_server_git_setting SpringCloudService#config_server_git_setting}
        :param container_registry: container_registry block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#container_registry SpringCloudService#container_registry}
        :param default_build_service: default_build_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#default_build_service SpringCloudService#default_build_service}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#id SpringCloudService#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_stream_public_endpoint_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#log_stream_public_endpoint_enabled SpringCloudService#log_stream_public_endpoint_enabled}.
        :param managed_environment_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#managed_environment_id SpringCloudService#managed_environment_id}.
        :param marketplace: marketplace block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#marketplace SpringCloudService#marketplace}
        :param network: network block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#network SpringCloudService#network}
        :param service_registry_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#service_registry_enabled SpringCloudService#service_registry_enabled}.
        :param sku_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#sku_name SpringCloudService#sku_name}.
        :param sku_tier: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#sku_tier SpringCloudService#sku_tier}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#tags SpringCloudService#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#timeouts SpringCloudService#timeouts}
        :param trace: trace block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#trace SpringCloudService#trace}
        :param zone_redundant: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#zone_redundant SpringCloudService#zone_redundant}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(config_server_git_setting, dict):
            config_server_git_setting = SpringCloudServiceConfigServerGitSetting(**config_server_git_setting)
        if isinstance(default_build_service, dict):
            default_build_service = SpringCloudServiceDefaultBuildService(**default_build_service)
        if isinstance(marketplace, dict):
            marketplace = SpringCloudServiceMarketplace(**marketplace)
        if isinstance(network, dict):
            network = SpringCloudServiceNetwork(**network)
        if isinstance(timeouts, dict):
            timeouts = SpringCloudServiceTimeouts(**timeouts)
        if isinstance(trace, dict):
            trace = SpringCloudServiceTrace(**trace)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a136544489d7d8f69e5e7df0cac0e23675d630d5fdf5779e39d8e9c6c8ca0903)
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
            check_type(argname="argument build_agent_pool_size", value=build_agent_pool_size, expected_type=type_hints["build_agent_pool_size"])
            check_type(argname="argument config_server_git_setting", value=config_server_git_setting, expected_type=type_hints["config_server_git_setting"])
            check_type(argname="argument container_registry", value=container_registry, expected_type=type_hints["container_registry"])
            check_type(argname="argument default_build_service", value=default_build_service, expected_type=type_hints["default_build_service"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument log_stream_public_endpoint_enabled", value=log_stream_public_endpoint_enabled, expected_type=type_hints["log_stream_public_endpoint_enabled"])
            check_type(argname="argument managed_environment_id", value=managed_environment_id, expected_type=type_hints["managed_environment_id"])
            check_type(argname="argument marketplace", value=marketplace, expected_type=type_hints["marketplace"])
            check_type(argname="argument network", value=network, expected_type=type_hints["network"])
            check_type(argname="argument service_registry_enabled", value=service_registry_enabled, expected_type=type_hints["service_registry_enabled"])
            check_type(argname="argument sku_name", value=sku_name, expected_type=type_hints["sku_name"])
            check_type(argname="argument sku_tier", value=sku_tier, expected_type=type_hints["sku_tier"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument trace", value=trace, expected_type=type_hints["trace"])
            check_type(argname="argument zone_redundant", value=zone_redundant, expected_type=type_hints["zone_redundant"])
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
        if build_agent_pool_size is not None:
            self._values["build_agent_pool_size"] = build_agent_pool_size
        if config_server_git_setting is not None:
            self._values["config_server_git_setting"] = config_server_git_setting
        if container_registry is not None:
            self._values["container_registry"] = container_registry
        if default_build_service is not None:
            self._values["default_build_service"] = default_build_service
        if id is not None:
            self._values["id"] = id
        if log_stream_public_endpoint_enabled is not None:
            self._values["log_stream_public_endpoint_enabled"] = log_stream_public_endpoint_enabled
        if managed_environment_id is not None:
            self._values["managed_environment_id"] = managed_environment_id
        if marketplace is not None:
            self._values["marketplace"] = marketplace
        if network is not None:
            self._values["network"] = network
        if service_registry_enabled is not None:
            self._values["service_registry_enabled"] = service_registry_enabled
        if sku_name is not None:
            self._values["sku_name"] = sku_name
        if sku_tier is not None:
            self._values["sku_tier"] = sku_tier
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if trace is not None:
            self._values["trace"] = trace
        if zone_redundant is not None:
            self._values["zone_redundant"] = zone_redundant

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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#location SpringCloudService#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#name SpringCloudService#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#resource_group_name SpringCloudService#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def build_agent_pool_size(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#build_agent_pool_size SpringCloudService#build_agent_pool_size}.'''
        result = self._values.get("build_agent_pool_size")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def config_server_git_setting(
        self,
    ) -> typing.Optional["SpringCloudServiceConfigServerGitSetting"]:
        '''config_server_git_setting block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#config_server_git_setting SpringCloudService#config_server_git_setting}
        '''
        result = self._values.get("config_server_git_setting")
        return typing.cast(typing.Optional["SpringCloudServiceConfigServerGitSetting"], result)

    @builtins.property
    def container_registry(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SpringCloudServiceContainerRegistry"]]]:
        '''container_registry block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#container_registry SpringCloudService#container_registry}
        '''
        result = self._values.get("container_registry")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SpringCloudServiceContainerRegistry"]]], result)

    @builtins.property
    def default_build_service(
        self,
    ) -> typing.Optional["SpringCloudServiceDefaultBuildService"]:
        '''default_build_service block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#default_build_service SpringCloudService#default_build_service}
        '''
        result = self._values.get("default_build_service")
        return typing.cast(typing.Optional["SpringCloudServiceDefaultBuildService"], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#id SpringCloudService#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_stream_public_endpoint_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#log_stream_public_endpoint_enabled SpringCloudService#log_stream_public_endpoint_enabled}.'''
        result = self._values.get("log_stream_public_endpoint_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def managed_environment_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#managed_environment_id SpringCloudService#managed_environment_id}.'''
        result = self._values.get("managed_environment_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def marketplace(self) -> typing.Optional["SpringCloudServiceMarketplace"]:
        '''marketplace block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#marketplace SpringCloudService#marketplace}
        '''
        result = self._values.get("marketplace")
        return typing.cast(typing.Optional["SpringCloudServiceMarketplace"], result)

    @builtins.property
    def network(self) -> typing.Optional["SpringCloudServiceNetwork"]:
        '''network block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#network SpringCloudService#network}
        '''
        result = self._values.get("network")
        return typing.cast(typing.Optional["SpringCloudServiceNetwork"], result)

    @builtins.property
    def service_registry_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#service_registry_enabled SpringCloudService#service_registry_enabled}.'''
        result = self._values.get("service_registry_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def sku_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#sku_name SpringCloudService#sku_name}.'''
        result = self._values.get("sku_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sku_tier(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#sku_tier SpringCloudService#sku_tier}.'''
        result = self._values.get("sku_tier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#tags SpringCloudService#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["SpringCloudServiceTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#timeouts SpringCloudService#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["SpringCloudServiceTimeouts"], result)

    @builtins.property
    def trace(self) -> typing.Optional["SpringCloudServiceTrace"]:
        '''trace block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#trace SpringCloudService#trace}
        '''
        result = self._values.get("trace")
        return typing.cast(typing.Optional["SpringCloudServiceTrace"], result)

    @builtins.property
    def zone_redundant(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#zone_redundant SpringCloudService#zone_redundant}.'''
        result = self._values.get("zone_redundant")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpringCloudServiceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.springCloudService.SpringCloudServiceConfigServerGitSetting",
    jsii_struct_bases=[],
    name_mapping={
        "uri": "uri",
        "http_basic_auth": "httpBasicAuth",
        "label": "label",
        "repository": "repository",
        "search_paths": "searchPaths",
        "ssh_auth": "sshAuth",
    },
)
class SpringCloudServiceConfigServerGitSetting:
    def __init__(
        self,
        *,
        uri: builtins.str,
        http_basic_auth: typing.Optional[typing.Union["SpringCloudServiceConfigServerGitSettingHttpBasicAuth", typing.Dict[builtins.str, typing.Any]]] = None,
        label: typing.Optional[builtins.str] = None,
        repository: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SpringCloudServiceConfigServerGitSettingRepository", typing.Dict[builtins.str, typing.Any]]]]] = None,
        search_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        ssh_auth: typing.Optional[typing.Union["SpringCloudServiceConfigServerGitSettingSshAuth", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#uri SpringCloudService#uri}.
        :param http_basic_auth: http_basic_auth block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#http_basic_auth SpringCloudService#http_basic_auth}
        :param label: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#label SpringCloudService#label}.
        :param repository: repository block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#repository SpringCloudService#repository}
        :param search_paths: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#search_paths SpringCloudService#search_paths}.
        :param ssh_auth: ssh_auth block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#ssh_auth SpringCloudService#ssh_auth}
        '''
        if isinstance(http_basic_auth, dict):
            http_basic_auth = SpringCloudServiceConfigServerGitSettingHttpBasicAuth(**http_basic_auth)
        if isinstance(ssh_auth, dict):
            ssh_auth = SpringCloudServiceConfigServerGitSettingSshAuth(**ssh_auth)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb9b5edeff9839510436469ee7719fe8a9f066374addfbb8db5d2385e7af4dda)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            check_type(argname="argument http_basic_auth", value=http_basic_auth, expected_type=type_hints["http_basic_auth"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument search_paths", value=search_paths, expected_type=type_hints["search_paths"])
            check_type(argname="argument ssh_auth", value=ssh_auth, expected_type=type_hints["ssh_auth"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "uri": uri,
        }
        if http_basic_auth is not None:
            self._values["http_basic_auth"] = http_basic_auth
        if label is not None:
            self._values["label"] = label
        if repository is not None:
            self._values["repository"] = repository
        if search_paths is not None:
            self._values["search_paths"] = search_paths
        if ssh_auth is not None:
            self._values["ssh_auth"] = ssh_auth

    @builtins.property
    def uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#uri SpringCloudService#uri}.'''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def http_basic_auth(
        self,
    ) -> typing.Optional["SpringCloudServiceConfigServerGitSettingHttpBasicAuth"]:
        '''http_basic_auth block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#http_basic_auth SpringCloudService#http_basic_auth}
        '''
        result = self._values.get("http_basic_auth")
        return typing.cast(typing.Optional["SpringCloudServiceConfigServerGitSettingHttpBasicAuth"], result)

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#label SpringCloudService#label}.'''
        result = self._values.get("label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SpringCloudServiceConfigServerGitSettingRepository"]]]:
        '''repository block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#repository SpringCloudService#repository}
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SpringCloudServiceConfigServerGitSettingRepository"]]], result)

    @builtins.property
    def search_paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#search_paths SpringCloudService#search_paths}.'''
        result = self._values.get("search_paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ssh_auth(
        self,
    ) -> typing.Optional["SpringCloudServiceConfigServerGitSettingSshAuth"]:
        '''ssh_auth block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#ssh_auth SpringCloudService#ssh_auth}
        '''
        result = self._values.get("ssh_auth")
        return typing.cast(typing.Optional["SpringCloudServiceConfigServerGitSettingSshAuth"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpringCloudServiceConfigServerGitSetting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.springCloudService.SpringCloudServiceConfigServerGitSettingHttpBasicAuth",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class SpringCloudServiceConfigServerGitSettingHttpBasicAuth:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#password SpringCloudService#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#username SpringCloudService#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd790ed58b3d2ca9cae7a842e5a23db71fa4210c2d0130eae9aefdd649684051)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#password SpringCloudService#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#username SpringCloudService#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpringCloudServiceConfigServerGitSettingHttpBasicAuth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpringCloudServiceConfigServerGitSettingHttpBasicAuthOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudService.SpringCloudServiceConfigServerGitSettingHttpBasicAuthOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d61a51be17806f917ae73bce785c189e5a0baf6ede9a5ddf6c28b026934c366e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3b74ade0671b3dd345b750062066f81e48e59225328bd2515e83a41a3a1b515)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ea1c1f3bdb10be45958866832686f23718fdcd2469b8bc2f7848b89394c8aeb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SpringCloudServiceConfigServerGitSettingHttpBasicAuth]:
        return typing.cast(typing.Optional[SpringCloudServiceConfigServerGitSettingHttpBasicAuth], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SpringCloudServiceConfigServerGitSettingHttpBasicAuth],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dba473054f7eeb6bf2520bb08503434168866d5345f31169bed86ecd5b216c34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SpringCloudServiceConfigServerGitSettingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudService.SpringCloudServiceConfigServerGitSettingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c74343258f153e5f6d7eb05b0518fc134b87f3a460f6660192b658f60c7c3ed9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHttpBasicAuth")
    def put_http_basic_auth(
        self,
        *,
        password: builtins.str,
        username: builtins.str,
    ) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#password SpringCloudService#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#username SpringCloudService#username}.
        '''
        value = SpringCloudServiceConfigServerGitSettingHttpBasicAuth(
            password=password, username=username
        )

        return typing.cast(None, jsii.invoke(self, "putHttpBasicAuth", [value]))

    @jsii.member(jsii_name="putRepository")
    def put_repository(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SpringCloudServiceConfigServerGitSettingRepository", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b743ab458d3a88175a43a633e864554999d89db0308692968afce50fe4153f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRepository", [value]))

    @jsii.member(jsii_name="putSshAuth")
    def put_ssh_auth(
        self,
        *,
        private_key: builtins.str,
        host_key: typing.Optional[builtins.str] = None,
        host_key_algorithm: typing.Optional[builtins.str] = None,
        strict_host_key_checking_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param private_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#private_key SpringCloudService#private_key}.
        :param host_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#host_key SpringCloudService#host_key}.
        :param host_key_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#host_key_algorithm SpringCloudService#host_key_algorithm}.
        :param strict_host_key_checking_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#strict_host_key_checking_enabled SpringCloudService#strict_host_key_checking_enabled}.
        '''
        value = SpringCloudServiceConfigServerGitSettingSshAuth(
            private_key=private_key,
            host_key=host_key,
            host_key_algorithm=host_key_algorithm,
            strict_host_key_checking_enabled=strict_host_key_checking_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putSshAuth", [value]))

    @jsii.member(jsii_name="resetHttpBasicAuth")
    def reset_http_basic_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpBasicAuth", []))

    @jsii.member(jsii_name="resetLabel")
    def reset_label(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabel", []))

    @jsii.member(jsii_name="resetRepository")
    def reset_repository(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepository", []))

    @jsii.member(jsii_name="resetSearchPaths")
    def reset_search_paths(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSearchPaths", []))

    @jsii.member(jsii_name="resetSshAuth")
    def reset_ssh_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSshAuth", []))

    @builtins.property
    @jsii.member(jsii_name="httpBasicAuth")
    def http_basic_auth(
        self,
    ) -> SpringCloudServiceConfigServerGitSettingHttpBasicAuthOutputReference:
        return typing.cast(SpringCloudServiceConfigServerGitSettingHttpBasicAuthOutputReference, jsii.get(self, "httpBasicAuth"))

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> "SpringCloudServiceConfigServerGitSettingRepositoryList":
        return typing.cast("SpringCloudServiceConfigServerGitSettingRepositoryList", jsii.get(self, "repository"))

    @builtins.property
    @jsii.member(jsii_name="sshAuth")
    def ssh_auth(
        self,
    ) -> "SpringCloudServiceConfigServerGitSettingSshAuthOutputReference":
        return typing.cast("SpringCloudServiceConfigServerGitSettingSshAuthOutputReference", jsii.get(self, "sshAuth"))

    @builtins.property
    @jsii.member(jsii_name="httpBasicAuthInput")
    def http_basic_auth_input(
        self,
    ) -> typing.Optional[SpringCloudServiceConfigServerGitSettingHttpBasicAuth]:
        return typing.cast(typing.Optional[SpringCloudServiceConfigServerGitSettingHttpBasicAuth], jsii.get(self, "httpBasicAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="labelInput")
    def label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "labelInput"))

    @builtins.property
    @jsii.member(jsii_name="repositoryInput")
    def repository_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SpringCloudServiceConfigServerGitSettingRepository"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SpringCloudServiceConfigServerGitSettingRepository"]]], jsii.get(self, "repositoryInput"))

    @builtins.property
    @jsii.member(jsii_name="searchPathsInput")
    def search_paths_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "searchPathsInput"))

    @builtins.property
    @jsii.member(jsii_name="sshAuthInput")
    def ssh_auth_input(
        self,
    ) -> typing.Optional["SpringCloudServiceConfigServerGitSettingSshAuth"]:
        return typing.cast(typing.Optional["SpringCloudServiceConfigServerGitSettingSshAuth"], jsii.get(self, "sshAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "label"))

    @label.setter
    def label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c53d600deba52ff63c718324628d80144a8847db532bcde1811066389aa616c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "label", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="searchPaths")
    def search_paths(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "searchPaths"))

    @search_paths.setter
    def search_paths(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b544065946874e3d350ed49fa152042b0f5ed145e49013178a1431e3b0ffbc25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "searchPaths", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa467e0b9dee1eb98361cd4f528aa1668c36f6f4cda9ad2f833227cc0de83661)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SpringCloudServiceConfigServerGitSetting]:
        return typing.cast(typing.Optional[SpringCloudServiceConfigServerGitSetting], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SpringCloudServiceConfigServerGitSetting],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a714a863cdfb1285cc50f16c86b7ae4f567e34822042018fd78528ddd9174d8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.springCloudService.SpringCloudServiceConfigServerGitSettingRepository",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "uri": "uri",
        "http_basic_auth": "httpBasicAuth",
        "label": "label",
        "pattern": "pattern",
        "search_paths": "searchPaths",
        "ssh_auth": "sshAuth",
    },
)
class SpringCloudServiceConfigServerGitSettingRepository:
    def __init__(
        self,
        *,
        name: builtins.str,
        uri: builtins.str,
        http_basic_auth: typing.Optional[typing.Union["SpringCloudServiceConfigServerGitSettingRepositoryHttpBasicAuth", typing.Dict[builtins.str, typing.Any]]] = None,
        label: typing.Optional[builtins.str] = None,
        pattern: typing.Optional[typing.Sequence[builtins.str]] = None,
        search_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        ssh_auth: typing.Optional[typing.Union["SpringCloudServiceConfigServerGitSettingRepositorySshAuth", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#name SpringCloudService#name}.
        :param uri: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#uri SpringCloudService#uri}.
        :param http_basic_auth: http_basic_auth block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#http_basic_auth SpringCloudService#http_basic_auth}
        :param label: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#label SpringCloudService#label}.
        :param pattern: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#pattern SpringCloudService#pattern}.
        :param search_paths: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#search_paths SpringCloudService#search_paths}.
        :param ssh_auth: ssh_auth block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#ssh_auth SpringCloudService#ssh_auth}
        '''
        if isinstance(http_basic_auth, dict):
            http_basic_auth = SpringCloudServiceConfigServerGitSettingRepositoryHttpBasicAuth(**http_basic_auth)
        if isinstance(ssh_auth, dict):
            ssh_auth = SpringCloudServiceConfigServerGitSettingRepositorySshAuth(**ssh_auth)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__071416543596339a60a8fa051935fbc3f2ac8bf5a80732b1b50b1545c713cf4a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
            check_type(argname="argument http_basic_auth", value=http_basic_auth, expected_type=type_hints["http_basic_auth"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
            check_type(argname="argument search_paths", value=search_paths, expected_type=type_hints["search_paths"])
            check_type(argname="argument ssh_auth", value=ssh_auth, expected_type=type_hints["ssh_auth"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "uri": uri,
        }
        if http_basic_auth is not None:
            self._values["http_basic_auth"] = http_basic_auth
        if label is not None:
            self._values["label"] = label
        if pattern is not None:
            self._values["pattern"] = pattern
        if search_paths is not None:
            self._values["search_paths"] = search_paths
        if ssh_auth is not None:
            self._values["ssh_auth"] = ssh_auth

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#name SpringCloudService#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def uri(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#uri SpringCloudService#uri}.'''
        result = self._values.get("uri")
        assert result is not None, "Required property 'uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def http_basic_auth(
        self,
    ) -> typing.Optional["SpringCloudServiceConfigServerGitSettingRepositoryHttpBasicAuth"]:
        '''http_basic_auth block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#http_basic_auth SpringCloudService#http_basic_auth}
        '''
        result = self._values.get("http_basic_auth")
        return typing.cast(typing.Optional["SpringCloudServiceConfigServerGitSettingRepositoryHttpBasicAuth"], result)

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#label SpringCloudService#label}.'''
        result = self._values.get("label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pattern(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#pattern SpringCloudService#pattern}.'''
        result = self._values.get("pattern")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def search_paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#search_paths SpringCloudService#search_paths}.'''
        result = self._values.get("search_paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ssh_auth(
        self,
    ) -> typing.Optional["SpringCloudServiceConfigServerGitSettingRepositorySshAuth"]:
        '''ssh_auth block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#ssh_auth SpringCloudService#ssh_auth}
        '''
        result = self._values.get("ssh_auth")
        return typing.cast(typing.Optional["SpringCloudServiceConfigServerGitSettingRepositorySshAuth"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpringCloudServiceConfigServerGitSettingRepository(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.springCloudService.SpringCloudServiceConfigServerGitSettingRepositoryHttpBasicAuth",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class SpringCloudServiceConfigServerGitSettingRepositoryHttpBasicAuth:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#password SpringCloudService#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#username SpringCloudService#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65f98e0f9d80ac487d7c7c106a5914b06bcaf8ee7db2161bebc476b54f345c98)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#password SpringCloudService#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#username SpringCloudService#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpringCloudServiceConfigServerGitSettingRepositoryHttpBasicAuth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpringCloudServiceConfigServerGitSettingRepositoryHttpBasicAuthOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudService.SpringCloudServiceConfigServerGitSettingRepositoryHttpBasicAuthOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb2f5ee2e499692b8296d4f0ff0477b6881caf3d9b08d613d161b0fce957b1db)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1727f872df8cc74868b60f1f04e52fc5c79483544ae741d1e3d7d40bd72e9df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__389cdce15c56ef2bad635725b6e91b88d9f04fc689029acd3869bd7866f6fc61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SpringCloudServiceConfigServerGitSettingRepositoryHttpBasicAuth]:
        return typing.cast(typing.Optional[SpringCloudServiceConfigServerGitSettingRepositoryHttpBasicAuth], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SpringCloudServiceConfigServerGitSettingRepositoryHttpBasicAuth],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce1b8a720a099374a0f0702401a6b08a9efca92d6ee620bd65b929a85a8efaef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SpringCloudServiceConfigServerGitSettingRepositoryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudService.SpringCloudServiceConfigServerGitSettingRepositoryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4bb7e5abf84b324ed33c876782219c1b8cdfc284d95770ba9b975d7caf3218ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SpringCloudServiceConfigServerGitSettingRepositoryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03c7fdd114ba33640977ee0cc4fe5576b9b71257fc84ab69eee58561e6567a11)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SpringCloudServiceConfigServerGitSettingRepositoryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1c6cce36bf55aa27c0bba6b954d92333bf0f0be3d0f6b45b03ee96b4da9da93)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9f053bcc47dbf7f6645b1dc0df05285a03e9b0b1dc8eb7ac464596d3d52d790)
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
            type_hints = typing.get_type_hints(_typecheckingstub__06d752d6711c9c8792f3be78ad919d77c8129af5d701be191e270119ffcdb899)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SpringCloudServiceConfigServerGitSettingRepository]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SpringCloudServiceConfigServerGitSettingRepository]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SpringCloudServiceConfigServerGitSettingRepository]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17b0719bdc69341a4d5dc5260e806e203f81943194a52a3903fd02c78640bb55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SpringCloudServiceConfigServerGitSettingRepositoryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudService.SpringCloudServiceConfigServerGitSettingRepositoryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eec260d8d993168b4950a9c7e8ceceafd397085ffb7cfff6fb5f90e683e82445)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putHttpBasicAuth")
    def put_http_basic_auth(
        self,
        *,
        password: builtins.str,
        username: builtins.str,
    ) -> None:
        '''
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#password SpringCloudService#password}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#username SpringCloudService#username}.
        '''
        value = SpringCloudServiceConfigServerGitSettingRepositoryHttpBasicAuth(
            password=password, username=username
        )

        return typing.cast(None, jsii.invoke(self, "putHttpBasicAuth", [value]))

    @jsii.member(jsii_name="putSshAuth")
    def put_ssh_auth(
        self,
        *,
        private_key: builtins.str,
        host_key: typing.Optional[builtins.str] = None,
        host_key_algorithm: typing.Optional[builtins.str] = None,
        strict_host_key_checking_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param private_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#private_key SpringCloudService#private_key}.
        :param host_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#host_key SpringCloudService#host_key}.
        :param host_key_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#host_key_algorithm SpringCloudService#host_key_algorithm}.
        :param strict_host_key_checking_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#strict_host_key_checking_enabled SpringCloudService#strict_host_key_checking_enabled}.
        '''
        value = SpringCloudServiceConfigServerGitSettingRepositorySshAuth(
            private_key=private_key,
            host_key=host_key,
            host_key_algorithm=host_key_algorithm,
            strict_host_key_checking_enabled=strict_host_key_checking_enabled,
        )

        return typing.cast(None, jsii.invoke(self, "putSshAuth", [value]))

    @jsii.member(jsii_name="resetHttpBasicAuth")
    def reset_http_basic_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpBasicAuth", []))

    @jsii.member(jsii_name="resetLabel")
    def reset_label(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabel", []))

    @jsii.member(jsii_name="resetPattern")
    def reset_pattern(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPattern", []))

    @jsii.member(jsii_name="resetSearchPaths")
    def reset_search_paths(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSearchPaths", []))

    @jsii.member(jsii_name="resetSshAuth")
    def reset_ssh_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSshAuth", []))

    @builtins.property
    @jsii.member(jsii_name="httpBasicAuth")
    def http_basic_auth(
        self,
    ) -> SpringCloudServiceConfigServerGitSettingRepositoryHttpBasicAuthOutputReference:
        return typing.cast(SpringCloudServiceConfigServerGitSettingRepositoryHttpBasicAuthOutputReference, jsii.get(self, "httpBasicAuth"))

    @builtins.property
    @jsii.member(jsii_name="sshAuth")
    def ssh_auth(
        self,
    ) -> "SpringCloudServiceConfigServerGitSettingRepositorySshAuthOutputReference":
        return typing.cast("SpringCloudServiceConfigServerGitSettingRepositorySshAuthOutputReference", jsii.get(self, "sshAuth"))

    @builtins.property
    @jsii.member(jsii_name="httpBasicAuthInput")
    def http_basic_auth_input(
        self,
    ) -> typing.Optional[SpringCloudServiceConfigServerGitSettingRepositoryHttpBasicAuth]:
        return typing.cast(typing.Optional[SpringCloudServiceConfigServerGitSettingRepositoryHttpBasicAuth], jsii.get(self, "httpBasicAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="labelInput")
    def label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "labelInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="patternInput")
    def pattern_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "patternInput"))

    @builtins.property
    @jsii.member(jsii_name="searchPathsInput")
    def search_paths_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "searchPathsInput"))

    @builtins.property
    @jsii.member(jsii_name="sshAuthInput")
    def ssh_auth_input(
        self,
    ) -> typing.Optional["SpringCloudServiceConfigServerGitSettingRepositorySshAuth"]:
        return typing.cast(typing.Optional["SpringCloudServiceConfigServerGitSettingRepositorySshAuth"], jsii.get(self, "sshAuthInput"))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "label"))

    @label.setter
    def label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb15a6d0759bd13c4a7ae64436aea7bc01c5f4f85684fa225c997b8ec71ef35f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "label", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50874ca4f3b5f83febf6635a0ebf8b2b341b6328c262d5b65383264f40252ef0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pattern")
    def pattern(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "pattern"))

    @pattern.setter
    def pattern(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3fa4ae7742836e4e0389588390d615b98b8ea2bd57513f99cfa9097687ceb3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="searchPaths")
    def search_paths(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "searchPaths"))

    @search_paths.setter
    def search_paths(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__100de8f2f5f8e08a4c09829d4cceca92ca4b0e7da91e3bfb6ea3ec23333f46f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "searchPaths", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__463bde87289d64e19280b6a4c6a088f31f9c20870c28eb5fc412c2cf30c4f7b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpringCloudServiceConfigServerGitSettingRepository]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpringCloudServiceConfigServerGitSettingRepository]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpringCloudServiceConfigServerGitSettingRepository]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76273b9668f688af74c95a328f1e2c223195b0b9893d8a2fb88c307531e69c3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.springCloudService.SpringCloudServiceConfigServerGitSettingRepositorySshAuth",
    jsii_struct_bases=[],
    name_mapping={
        "private_key": "privateKey",
        "host_key": "hostKey",
        "host_key_algorithm": "hostKeyAlgorithm",
        "strict_host_key_checking_enabled": "strictHostKeyCheckingEnabled",
    },
)
class SpringCloudServiceConfigServerGitSettingRepositorySshAuth:
    def __init__(
        self,
        *,
        private_key: builtins.str,
        host_key: typing.Optional[builtins.str] = None,
        host_key_algorithm: typing.Optional[builtins.str] = None,
        strict_host_key_checking_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param private_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#private_key SpringCloudService#private_key}.
        :param host_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#host_key SpringCloudService#host_key}.
        :param host_key_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#host_key_algorithm SpringCloudService#host_key_algorithm}.
        :param strict_host_key_checking_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#strict_host_key_checking_enabled SpringCloudService#strict_host_key_checking_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49e59b074589c03aa4b0752dd084ae1171a06af6158d78bee6f32df0bc76ec32)
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
            check_type(argname="argument host_key", value=host_key, expected_type=type_hints["host_key"])
            check_type(argname="argument host_key_algorithm", value=host_key_algorithm, expected_type=type_hints["host_key_algorithm"])
            check_type(argname="argument strict_host_key_checking_enabled", value=strict_host_key_checking_enabled, expected_type=type_hints["strict_host_key_checking_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "private_key": private_key,
        }
        if host_key is not None:
            self._values["host_key"] = host_key
        if host_key_algorithm is not None:
            self._values["host_key_algorithm"] = host_key_algorithm
        if strict_host_key_checking_enabled is not None:
            self._values["strict_host_key_checking_enabled"] = strict_host_key_checking_enabled

    @builtins.property
    def private_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#private_key SpringCloudService#private_key}.'''
        result = self._values.get("private_key")
        assert result is not None, "Required property 'private_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#host_key SpringCloudService#host_key}.'''
        result = self._values.get("host_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host_key_algorithm(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#host_key_algorithm SpringCloudService#host_key_algorithm}.'''
        result = self._values.get("host_key_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def strict_host_key_checking_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#strict_host_key_checking_enabled SpringCloudService#strict_host_key_checking_enabled}.'''
        result = self._values.get("strict_host_key_checking_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpringCloudServiceConfigServerGitSettingRepositorySshAuth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpringCloudServiceConfigServerGitSettingRepositorySshAuthOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudService.SpringCloudServiceConfigServerGitSettingRepositorySshAuthOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ef1d1cc40bf927e00fb1fe0a5c80ad49f76ac99068e081a572a1d65cd232c19)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHostKey")
    def reset_host_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostKey", []))

    @jsii.member(jsii_name="resetHostKeyAlgorithm")
    def reset_host_key_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostKeyAlgorithm", []))

    @jsii.member(jsii_name="resetStrictHostKeyCheckingEnabled")
    def reset_strict_host_key_checking_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStrictHostKeyCheckingEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="hostKeyAlgorithmInput")
    def host_key_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostKeyAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="hostKeyInput")
    def host_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="privateKeyInput")
    def private_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="strictHostKeyCheckingEnabledInput")
    def strict_host_key_checking_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "strictHostKeyCheckingEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="hostKey")
    def host_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostKey"))

    @host_key.setter
    def host_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec57e640bfb44b2f027d512257165d72eb4e85b64cbaa14c2179e779ac940de2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostKeyAlgorithm")
    def host_key_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostKeyAlgorithm"))

    @host_key_algorithm.setter
    def host_key_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdfc2c27653e62675b33d80a4a67d0bc7e1ad6be188eca50d7fa3cca834f336a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostKeyAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKey"))

    @private_key.setter
    def private_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9af81b94d815527a62cb98473162187feb87b7e744e354a3d9e534ce156c0603)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="strictHostKeyCheckingEnabled")
    def strict_host_key_checking_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "strictHostKeyCheckingEnabled"))

    @strict_host_key_checking_enabled.setter
    def strict_host_key_checking_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b34dff86f2d2e5c5d067263f6196b63f85577b8dd0308172ec639aa2107b388)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "strictHostKeyCheckingEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SpringCloudServiceConfigServerGitSettingRepositorySshAuth]:
        return typing.cast(typing.Optional[SpringCloudServiceConfigServerGitSettingRepositorySshAuth], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SpringCloudServiceConfigServerGitSettingRepositorySshAuth],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dad7db49b519dc5f3c51a959bc2e14691272f4186d68e5fe274603e01988399)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.springCloudService.SpringCloudServiceConfigServerGitSettingSshAuth",
    jsii_struct_bases=[],
    name_mapping={
        "private_key": "privateKey",
        "host_key": "hostKey",
        "host_key_algorithm": "hostKeyAlgorithm",
        "strict_host_key_checking_enabled": "strictHostKeyCheckingEnabled",
    },
)
class SpringCloudServiceConfigServerGitSettingSshAuth:
    def __init__(
        self,
        *,
        private_key: builtins.str,
        host_key: typing.Optional[builtins.str] = None,
        host_key_algorithm: typing.Optional[builtins.str] = None,
        strict_host_key_checking_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param private_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#private_key SpringCloudService#private_key}.
        :param host_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#host_key SpringCloudService#host_key}.
        :param host_key_algorithm: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#host_key_algorithm SpringCloudService#host_key_algorithm}.
        :param strict_host_key_checking_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#strict_host_key_checking_enabled SpringCloudService#strict_host_key_checking_enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f7532691b857066ae56670b2a7f082bdce3e6b3ae327b245be21a5faec87be5)
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
            check_type(argname="argument host_key", value=host_key, expected_type=type_hints["host_key"])
            check_type(argname="argument host_key_algorithm", value=host_key_algorithm, expected_type=type_hints["host_key_algorithm"])
            check_type(argname="argument strict_host_key_checking_enabled", value=strict_host_key_checking_enabled, expected_type=type_hints["strict_host_key_checking_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "private_key": private_key,
        }
        if host_key is not None:
            self._values["host_key"] = host_key
        if host_key_algorithm is not None:
            self._values["host_key_algorithm"] = host_key_algorithm
        if strict_host_key_checking_enabled is not None:
            self._values["strict_host_key_checking_enabled"] = strict_host_key_checking_enabled

    @builtins.property
    def private_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#private_key SpringCloudService#private_key}.'''
        result = self._values.get("private_key")
        assert result is not None, "Required property 'private_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def host_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#host_key SpringCloudService#host_key}.'''
        result = self._values.get("host_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host_key_algorithm(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#host_key_algorithm SpringCloudService#host_key_algorithm}.'''
        result = self._values.get("host_key_algorithm")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def strict_host_key_checking_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#strict_host_key_checking_enabled SpringCloudService#strict_host_key_checking_enabled}.'''
        result = self._values.get("strict_host_key_checking_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpringCloudServiceConfigServerGitSettingSshAuth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpringCloudServiceConfigServerGitSettingSshAuthOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudService.SpringCloudServiceConfigServerGitSettingSshAuthOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__694657f7e7767f40af3a9d839809472b145a40bdbe8b35fe64eed6df2706aab2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetHostKey")
    def reset_host_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostKey", []))

    @jsii.member(jsii_name="resetHostKeyAlgorithm")
    def reset_host_key_algorithm(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostKeyAlgorithm", []))

    @jsii.member(jsii_name="resetStrictHostKeyCheckingEnabled")
    def reset_strict_host_key_checking_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStrictHostKeyCheckingEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="hostKeyAlgorithmInput")
    def host_key_algorithm_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostKeyAlgorithmInput"))

    @builtins.property
    @jsii.member(jsii_name="hostKeyInput")
    def host_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="privateKeyInput")
    def private_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="strictHostKeyCheckingEnabledInput")
    def strict_host_key_checking_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "strictHostKeyCheckingEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="hostKey")
    def host_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostKey"))

    @host_key.setter
    def host_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db05581714ff982474cbc931aed5c6d7a9b7dd7ef43c70475a8296abd2650e70)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hostKeyAlgorithm")
    def host_key_algorithm(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostKeyAlgorithm"))

    @host_key_algorithm.setter
    def host_key_algorithm(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dc43b05f397564a55ecaeb4402e26502fa1359823028bf359b5b732275d8991)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostKeyAlgorithm", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "privateKey"))

    @private_key.setter
    def private_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed89b6d5c8a961555ac5943289cd03a0af9276fb9f12d9c657b28d6d8ff4ad37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="strictHostKeyCheckingEnabled")
    def strict_host_key_checking_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "strictHostKeyCheckingEnabled"))

    @strict_host_key_checking_enabled.setter
    def strict_host_key_checking_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d76c4ef1585fdb25a17c986fb639b9bba33e83a902d8e3dda1b348c1110038b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "strictHostKeyCheckingEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SpringCloudServiceConfigServerGitSettingSshAuth]:
        return typing.cast(typing.Optional[SpringCloudServiceConfigServerGitSettingSshAuth], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SpringCloudServiceConfigServerGitSettingSshAuth],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41139732b75a6e7e33d7df26897da5f220201b000beea065fef3347c7b6af7eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.springCloudService.SpringCloudServiceContainerRegistry",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "password": "password",
        "server": "server",
        "username": "username",
    },
)
class SpringCloudServiceContainerRegistry:
    def __init__(
        self,
        *,
        name: builtins.str,
        password: builtins.str,
        server: builtins.str,
        username: builtins.str,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#name SpringCloudService#name}.
        :param password: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#password SpringCloudService#password}.
        :param server: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#server SpringCloudService#server}.
        :param username: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#username SpringCloudService#username}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ce265d2bb968386a1187b8971ed3a9d607c69c231856a7e45c0f9b244acb3a1)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument server", value=server, expected_type=type_hints["server"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "password": password,
            "server": server,
            "username": username,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#name SpringCloudService#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#password SpringCloudService#password}.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#server SpringCloudService#server}.'''
        result = self._values.get("server")
        assert result is not None, "Required property 'server' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#username SpringCloudService#username}.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpringCloudServiceContainerRegistry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpringCloudServiceContainerRegistryList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudService.SpringCloudServiceContainerRegistryList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f950a94fadc63543e2144be88b9403b8f3356d3eb0db057bc1df72f12e14607d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SpringCloudServiceContainerRegistryOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deff2b937c5e2de040e70e104f591b3e78267efdf1558a585683942be6bfe2ab)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SpringCloudServiceContainerRegistryOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20d06ddbfe86f8c69333db04fa4b3f11929d47dcb38e1c79b780a4419957290e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f21acf837bf3bd9e2dd03032762cf3da28d56a8ebf4fd0cfc1531bd0709f757e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f00829adef1bf2ea03b53497c3cec605019a283dbd9f67a3b11ece0c3c2a4d2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SpringCloudServiceContainerRegistry]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SpringCloudServiceContainerRegistry]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SpringCloudServiceContainerRegistry]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bc9e1b634e5808f6ca226d7255c2e5576d1ada75a2aa3a60cad60762513b33e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class SpringCloudServiceContainerRegistryOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudService.SpringCloudServiceContainerRegistryOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cecc4203120346bdb3dae135686e42d89090aaf52c383d9f900c0a814893f4f)
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
    @jsii.member(jsii_name="passwordInput")
    def password_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordInput"))

    @builtins.property
    @jsii.member(jsii_name="serverInput")
    def server_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverInput"))

    @builtins.property
    @jsii.member(jsii_name="usernameInput")
    def username_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bf0a071273a11088cfb9508fd3783845ddb8c87b1615bde1474bef925c8b098)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="password")
    def password(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "password"))

    @password.setter
    def password(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d807cba435a6a7db387cc6e43c0367de483fe76eb3eba8e20513d1244c298c86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "password", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="server")
    def server(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "server"))

    @server.setter
    def server(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f80511e51dc758cc761ad8e6437142f66e9cc0da5aa6c9a8abd499ca6d831385)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "server", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="username")
    def username(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "username"))

    @username.setter
    def username(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6756e736b7193a1d81566384a898e0f6a4887c0b8bfd285483fc8354ff4e2598)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "username", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpringCloudServiceContainerRegistry]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpringCloudServiceContainerRegistry]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpringCloudServiceContainerRegistry]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a761d4c5e7022aaeb9eb6cbec7f8ad7e25b6af4cb96cdbb50e90f0958e3c7a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.springCloudService.SpringCloudServiceDefaultBuildService",
    jsii_struct_bases=[],
    name_mapping={"container_registry_name": "containerRegistryName"},
)
class SpringCloudServiceDefaultBuildService:
    def __init__(
        self,
        *,
        container_registry_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param container_registry_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#container_registry_name SpringCloudService#container_registry_name}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2cc09276bb3af22e3d80c59be5234eb9b662ef2dc0d83140ba28accea582c31)
            check_type(argname="argument container_registry_name", value=container_registry_name, expected_type=type_hints["container_registry_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if container_registry_name is not None:
            self._values["container_registry_name"] = container_registry_name

    @builtins.property
    def container_registry_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#container_registry_name SpringCloudService#container_registry_name}.'''
        result = self._values.get("container_registry_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpringCloudServiceDefaultBuildService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpringCloudServiceDefaultBuildServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudService.SpringCloudServiceDefaultBuildServiceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b685ff62d0b8698c9c6b0ce47c0f4f91670e40a0ccaa41d6f93993b694b5267)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetContainerRegistryName")
    def reset_container_registry_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetContainerRegistryName", []))

    @builtins.property
    @jsii.member(jsii_name="containerRegistryNameInput")
    def container_registry_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "containerRegistryNameInput"))

    @builtins.property
    @jsii.member(jsii_name="containerRegistryName")
    def container_registry_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "containerRegistryName"))

    @container_registry_name.setter
    def container_registry_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__702e5ccfb1d3c69495eaf71d9b9ae389ab9f004ebe600c873fce807742382472)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "containerRegistryName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SpringCloudServiceDefaultBuildService]:
        return typing.cast(typing.Optional[SpringCloudServiceDefaultBuildService], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SpringCloudServiceDefaultBuildService],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ef0823f2292cb38d12344f27a1401517378a67965cd70705c1fafb493cc9086)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.springCloudService.SpringCloudServiceMarketplace",
    jsii_struct_bases=[],
    name_mapping={"plan": "plan", "product": "product", "publisher": "publisher"},
)
class SpringCloudServiceMarketplace:
    def __init__(
        self,
        *,
        plan: builtins.str,
        product: builtins.str,
        publisher: builtins.str,
    ) -> None:
        '''
        :param plan: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#plan SpringCloudService#plan}.
        :param product: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#product SpringCloudService#product}.
        :param publisher: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#publisher SpringCloudService#publisher}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f9e4bbcd040381b5d1ffe139f7e54f05fbf700faef3ef22f1d113f539643e3f)
            check_type(argname="argument plan", value=plan, expected_type=type_hints["plan"])
            check_type(argname="argument product", value=product, expected_type=type_hints["product"])
            check_type(argname="argument publisher", value=publisher, expected_type=type_hints["publisher"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "plan": plan,
            "product": product,
            "publisher": publisher,
        }

    @builtins.property
    def plan(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#plan SpringCloudService#plan}.'''
        result = self._values.get("plan")
        assert result is not None, "Required property 'plan' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def product(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#product SpringCloudService#product}.'''
        result = self._values.get("product")
        assert result is not None, "Required property 'product' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def publisher(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#publisher SpringCloudService#publisher}.'''
        result = self._values.get("publisher")
        assert result is not None, "Required property 'publisher' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpringCloudServiceMarketplace(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpringCloudServiceMarketplaceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudService.SpringCloudServiceMarketplaceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c4c77a1be4497eec93f81ad05c34e4b2128f9f2dda1749818872f6074b8d8c1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="planInput")
    def plan_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "planInput"))

    @builtins.property
    @jsii.member(jsii_name="productInput")
    def product_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "productInput"))

    @builtins.property
    @jsii.member(jsii_name="publisherInput")
    def publisher_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publisherInput"))

    @builtins.property
    @jsii.member(jsii_name="plan")
    def plan(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "plan"))

    @plan.setter
    def plan(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__612d49308c4526dd1546150c14054febd1c30acaf586e58e47d7e04c7af3b4dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "plan", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="product")
    def product(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "product"))

    @product.setter
    def product(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b00882e9b72e51101611839d76b18f271a9cd261268713627fabe3110131e2eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "product", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="publisher")
    def publisher(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "publisher"))

    @publisher.setter
    def publisher(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2679a145e3215c8b906992ca804ae2de91b2f46ef6bbba80ba9d062356c99872)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publisher", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SpringCloudServiceMarketplace]:
        return typing.cast(typing.Optional[SpringCloudServiceMarketplace], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SpringCloudServiceMarketplace],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__617cd4717fe6c6222564506e82d0f04a2f86000cd3722fa5c7151b227579d82e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.springCloudService.SpringCloudServiceNetwork",
    jsii_struct_bases=[],
    name_mapping={
        "app_subnet_id": "appSubnetId",
        "cidr_ranges": "cidrRanges",
        "service_runtime_subnet_id": "serviceRuntimeSubnetId",
        "app_network_resource_group": "appNetworkResourceGroup",
        "outbound_type": "outboundType",
        "read_timeout_seconds": "readTimeoutSeconds",
        "service_runtime_network_resource_group": "serviceRuntimeNetworkResourceGroup",
    },
)
class SpringCloudServiceNetwork:
    def __init__(
        self,
        *,
        app_subnet_id: builtins.str,
        cidr_ranges: typing.Sequence[builtins.str],
        service_runtime_subnet_id: builtins.str,
        app_network_resource_group: typing.Optional[builtins.str] = None,
        outbound_type: typing.Optional[builtins.str] = None,
        read_timeout_seconds: typing.Optional[jsii.Number] = None,
        service_runtime_network_resource_group: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param app_subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#app_subnet_id SpringCloudService#app_subnet_id}.
        :param cidr_ranges: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#cidr_ranges SpringCloudService#cidr_ranges}.
        :param service_runtime_subnet_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#service_runtime_subnet_id SpringCloudService#service_runtime_subnet_id}.
        :param app_network_resource_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#app_network_resource_group SpringCloudService#app_network_resource_group}.
        :param outbound_type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#outbound_type SpringCloudService#outbound_type}.
        :param read_timeout_seconds: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#read_timeout_seconds SpringCloudService#read_timeout_seconds}.
        :param service_runtime_network_resource_group: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#service_runtime_network_resource_group SpringCloudService#service_runtime_network_resource_group}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69751b81327a0e961b3c8271acbf3fcc441d5552872d671599ed3c5ae060b85a)
            check_type(argname="argument app_subnet_id", value=app_subnet_id, expected_type=type_hints["app_subnet_id"])
            check_type(argname="argument cidr_ranges", value=cidr_ranges, expected_type=type_hints["cidr_ranges"])
            check_type(argname="argument service_runtime_subnet_id", value=service_runtime_subnet_id, expected_type=type_hints["service_runtime_subnet_id"])
            check_type(argname="argument app_network_resource_group", value=app_network_resource_group, expected_type=type_hints["app_network_resource_group"])
            check_type(argname="argument outbound_type", value=outbound_type, expected_type=type_hints["outbound_type"])
            check_type(argname="argument read_timeout_seconds", value=read_timeout_seconds, expected_type=type_hints["read_timeout_seconds"])
            check_type(argname="argument service_runtime_network_resource_group", value=service_runtime_network_resource_group, expected_type=type_hints["service_runtime_network_resource_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_subnet_id": app_subnet_id,
            "cidr_ranges": cidr_ranges,
            "service_runtime_subnet_id": service_runtime_subnet_id,
        }
        if app_network_resource_group is not None:
            self._values["app_network_resource_group"] = app_network_resource_group
        if outbound_type is not None:
            self._values["outbound_type"] = outbound_type
        if read_timeout_seconds is not None:
            self._values["read_timeout_seconds"] = read_timeout_seconds
        if service_runtime_network_resource_group is not None:
            self._values["service_runtime_network_resource_group"] = service_runtime_network_resource_group

    @builtins.property
    def app_subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#app_subnet_id SpringCloudService#app_subnet_id}.'''
        result = self._values.get("app_subnet_id")
        assert result is not None, "Required property 'app_subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cidr_ranges(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#cidr_ranges SpringCloudService#cidr_ranges}.'''
        result = self._values.get("cidr_ranges")
        assert result is not None, "Required property 'cidr_ranges' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def service_runtime_subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#service_runtime_subnet_id SpringCloudService#service_runtime_subnet_id}.'''
        result = self._values.get("service_runtime_subnet_id")
        assert result is not None, "Required property 'service_runtime_subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def app_network_resource_group(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#app_network_resource_group SpringCloudService#app_network_resource_group}.'''
        result = self._values.get("app_network_resource_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def outbound_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#outbound_type SpringCloudService#outbound_type}.'''
        result = self._values.get("outbound_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read_timeout_seconds(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#read_timeout_seconds SpringCloudService#read_timeout_seconds}.'''
        result = self._values.get("read_timeout_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service_runtime_network_resource_group(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#service_runtime_network_resource_group SpringCloudService#service_runtime_network_resource_group}.'''
        result = self._values.get("service_runtime_network_resource_group")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpringCloudServiceNetwork(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpringCloudServiceNetworkOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudService.SpringCloudServiceNetworkOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57c74997c8be05848790c841e7ec8e7e009a66cf2b9cae93c8792d4ab7f8979a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAppNetworkResourceGroup")
    def reset_app_network_resource_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAppNetworkResourceGroup", []))

    @jsii.member(jsii_name="resetOutboundType")
    def reset_outbound_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutboundType", []))

    @jsii.member(jsii_name="resetReadTimeoutSeconds")
    def reset_read_timeout_seconds(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadTimeoutSeconds", []))

    @jsii.member(jsii_name="resetServiceRuntimeNetworkResourceGroup")
    def reset_service_runtime_network_resource_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceRuntimeNetworkResourceGroup", []))

    @builtins.property
    @jsii.member(jsii_name="appNetworkResourceGroupInput")
    def app_network_resource_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appNetworkResourceGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="appSubnetIdInput")
    def app_subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "appSubnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="cidrRangesInput")
    def cidr_ranges_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "cidrRangesInput"))

    @builtins.property
    @jsii.member(jsii_name="outboundTypeInput")
    def outbound_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outboundTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="readTimeoutSecondsInput")
    def read_timeout_seconds_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "readTimeoutSecondsInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceRuntimeNetworkResourceGroupInput")
    def service_runtime_network_resource_group_input(
        self,
    ) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceRuntimeNetworkResourceGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceRuntimeSubnetIdInput")
    def service_runtime_subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceRuntimeSubnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="appNetworkResourceGroup")
    def app_network_resource_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appNetworkResourceGroup"))

    @app_network_resource_group.setter
    def app_network_resource_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9475c3dcdf57aef01a0099cac7ac930c9516f32ffeb83450b50616ee641b34b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appNetworkResourceGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="appSubnetId")
    def app_subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "appSubnetId"))

    @app_subnet_id.setter
    def app_subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fe230b8e85dcb48a93d971a0ada538f5391e5a2c0a1a89d175850b0fa86eb75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appSubnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="cidrRanges")
    def cidr_ranges(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "cidrRanges"))

    @cidr_ranges.setter
    def cidr_ranges(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a2a5360c2c9260a210806b9fd50a187dbc565a0e53dbcc899a70b26fa5665e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cidrRanges", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="outboundType")
    def outbound_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "outboundType"))

    @outbound_type.setter
    def outbound_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9faea2a9c7cba5765711767789f2aeb4a0c8cf9b8d20ecdb20eef2cd6f932612)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outboundType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="readTimeoutSeconds")
    def read_timeout_seconds(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "readTimeoutSeconds"))

    @read_timeout_seconds.setter
    def read_timeout_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78edd7671975f821a6a1f46a0427115f49d319ac0e40bc16da1c31b81eb47dce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "readTimeoutSeconds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceRuntimeNetworkResourceGroup")
    def service_runtime_network_resource_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceRuntimeNetworkResourceGroup"))

    @service_runtime_network_resource_group.setter
    def service_runtime_network_resource_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ab16444e38497a769d5ff890894b08f44fb43a832d7e1eea247f414bd98f3a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceRuntimeNetworkResourceGroup", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="serviceRuntimeSubnetId")
    def service_runtime_subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serviceRuntimeSubnetId"))

    @service_runtime_subnet_id.setter
    def service_runtime_subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e6a122f46b8a8c33770380fd9d5069e7969b9e55abeda3f345033a1d8966dbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceRuntimeSubnetId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SpringCloudServiceNetwork]:
        return typing.cast(typing.Optional[SpringCloudServiceNetwork], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[SpringCloudServiceNetwork]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3932536a63bbe1ad0c982523f45f189f7513a1859cd63c04fccc736013e07cc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.springCloudService.SpringCloudServiceRequiredNetworkTrafficRules",
    jsii_struct_bases=[],
    name_mapping={},
)
class SpringCloudServiceRequiredNetworkTrafficRules:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpringCloudServiceRequiredNetworkTrafficRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpringCloudServiceRequiredNetworkTrafficRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudService.SpringCloudServiceRequiredNetworkTrafficRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__527f31cb815fbe94cd6719b8cb0ad5dd5b3e404c5a529474bb263100c840da22)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SpringCloudServiceRequiredNetworkTrafficRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53a62ad1ced3cc08f848cfdec9991c938da3a933adbfe253a80634af8b871a4d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SpringCloudServiceRequiredNetworkTrafficRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3b7d8535ae62a3f76ec718d1ae7963f99a7956953ed2520f6f4ca768ef08c5c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f936d9e79f10e586be8d60668a3411ddb353bd03054d2834d873e22aa193edbc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7f7c0ebc1e91f50b46e8c9d7aa3f31f5917f24ba2fd6b6f7ee6d6fb140e4e06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class SpringCloudServiceRequiredNetworkTrafficRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudService.SpringCloudServiceRequiredNetworkTrafficRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf73b70cd70d61354e98570e9b809bef0649c3a8c615ab91b623a2c1f6c635dd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="direction")
    def direction(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "direction"))

    @builtins.property
    @jsii.member(jsii_name="fqdns")
    def fqdns(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "fqdns"))

    @builtins.property
    @jsii.member(jsii_name="ipAddresses")
    def ip_addresses(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipAddresses"))

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "port"))

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SpringCloudServiceRequiredNetworkTrafficRules]:
        return typing.cast(typing.Optional[SpringCloudServiceRequiredNetworkTrafficRules], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SpringCloudServiceRequiredNetworkTrafficRules],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15ac16dd8d47763fd1d22bdba14440587fff1368a78adb2b8308ae8d8be671f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.springCloudService.SpringCloudServiceTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class SpringCloudServiceTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#create SpringCloudService#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#delete SpringCloudService#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#read SpringCloudService#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#update SpringCloudService#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1df6602921dfa74929aabbee65c50741e4c2237d1727c6551ab8af9b2f5b95c3)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#create SpringCloudService#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#delete SpringCloudService#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#read SpringCloudService#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#update SpringCloudService#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpringCloudServiceTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpringCloudServiceTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudService.SpringCloudServiceTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__31eefe97471fc82d8624b0afed2422f0f6738699326db6b7bf528258d9f7c0ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3faa8c837df835d81b0b5f476a967149e101c0494efff322a87b1456032c72b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a81abfe66b93cc7f82c0ec856f30329ae931136c9f43eb44bdc6619de9589f46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf0b575468b1b0ca7c06b4bdd3e74eda8838ab3a38b80865247980245fef4bcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2665a8451c80df7f0e3372051dea6bd89a4832be4a9863d5112294baa219d4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpringCloudServiceTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpringCloudServiceTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpringCloudServiceTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70f155bed59df3875da44069a3e7b59e32a11da6988040a740a67ea1c7927cb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.springCloudService.SpringCloudServiceTrace",
    jsii_struct_bases=[],
    name_mapping={
        "connection_string": "connectionString",
        "sample_rate": "sampleRate",
    },
)
class SpringCloudServiceTrace:
    def __init__(
        self,
        *,
        connection_string: typing.Optional[builtins.str] = None,
        sample_rate: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection_string: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#connection_string SpringCloudService#connection_string}.
        :param sample_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#sample_rate SpringCloudService#sample_rate}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dfa5ef8b8a93d3a913651f68b4547dcf7d3ec089b3b2ce8b08f8297d7bbe185)
            check_type(argname="argument connection_string", value=connection_string, expected_type=type_hints["connection_string"])
            check_type(argname="argument sample_rate", value=sample_rate, expected_type=type_hints["sample_rate"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if connection_string is not None:
            self._values["connection_string"] = connection_string
        if sample_rate is not None:
            self._values["sample_rate"] = sample_rate

    @builtins.property
    def connection_string(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#connection_string SpringCloudService#connection_string}.'''
        result = self._values.get("connection_string")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sample_rate(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_service#sample_rate SpringCloudService#sample_rate}.'''
        result = self._values.get("sample_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpringCloudServiceTrace(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpringCloudServiceTraceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudService.SpringCloudServiceTraceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ca12bf59ad787e8110f7ce3e9a5c1df30a08a5057526d4f383400e045360f8e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetConnectionString")
    def reset_connection_string(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectionString", []))

    @jsii.member(jsii_name="resetSampleRate")
    def reset_sample_rate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSampleRate", []))

    @builtins.property
    @jsii.member(jsii_name="connectionStringInput")
    def connection_string_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionStringInput"))

    @builtins.property
    @jsii.member(jsii_name="sampleRateInput")
    def sample_rate_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "sampleRateInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionString")
    def connection_string(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionString"))

    @connection_string.setter
    def connection_string(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac6fe4a6932b8f2591bc1b88537a1ea653e0b2a98f644e486c7b81a9ed08c8c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionString", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sampleRate")
    def sample_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "sampleRate"))

    @sample_rate.setter
    def sample_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__607aef23025ed6837af06128086f6bda861cb527985ffe7be702450d4aa58257)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sampleRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[SpringCloudServiceTrace]:
        return typing.cast(typing.Optional[SpringCloudServiceTrace], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[SpringCloudServiceTrace]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44487f4e912fdb09ef32f91ab79a230fd873911881beeeb28aca7eef5d6434c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SpringCloudService",
    "SpringCloudServiceConfig",
    "SpringCloudServiceConfigServerGitSetting",
    "SpringCloudServiceConfigServerGitSettingHttpBasicAuth",
    "SpringCloudServiceConfigServerGitSettingHttpBasicAuthOutputReference",
    "SpringCloudServiceConfigServerGitSettingOutputReference",
    "SpringCloudServiceConfigServerGitSettingRepository",
    "SpringCloudServiceConfigServerGitSettingRepositoryHttpBasicAuth",
    "SpringCloudServiceConfigServerGitSettingRepositoryHttpBasicAuthOutputReference",
    "SpringCloudServiceConfigServerGitSettingRepositoryList",
    "SpringCloudServiceConfigServerGitSettingRepositoryOutputReference",
    "SpringCloudServiceConfigServerGitSettingRepositorySshAuth",
    "SpringCloudServiceConfigServerGitSettingRepositorySshAuthOutputReference",
    "SpringCloudServiceConfigServerGitSettingSshAuth",
    "SpringCloudServiceConfigServerGitSettingSshAuthOutputReference",
    "SpringCloudServiceContainerRegistry",
    "SpringCloudServiceContainerRegistryList",
    "SpringCloudServiceContainerRegistryOutputReference",
    "SpringCloudServiceDefaultBuildService",
    "SpringCloudServiceDefaultBuildServiceOutputReference",
    "SpringCloudServiceMarketplace",
    "SpringCloudServiceMarketplaceOutputReference",
    "SpringCloudServiceNetwork",
    "SpringCloudServiceNetworkOutputReference",
    "SpringCloudServiceRequiredNetworkTrafficRules",
    "SpringCloudServiceRequiredNetworkTrafficRulesList",
    "SpringCloudServiceRequiredNetworkTrafficRulesOutputReference",
    "SpringCloudServiceTimeouts",
    "SpringCloudServiceTimeoutsOutputReference",
    "SpringCloudServiceTrace",
    "SpringCloudServiceTraceOutputReference",
]

publication.publish()

def _typecheckingstub__1702dd28d1d9db9d7be035e7419a2e28152baa57c7fc95402841159f4ec39e76(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    build_agent_pool_size: typing.Optional[builtins.str] = None,
    config_server_git_setting: typing.Optional[typing.Union[SpringCloudServiceConfigServerGitSetting, typing.Dict[builtins.str, typing.Any]]] = None,
    container_registry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SpringCloudServiceContainerRegistry, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_build_service: typing.Optional[typing.Union[SpringCloudServiceDefaultBuildService, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    log_stream_public_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    managed_environment_id: typing.Optional[builtins.str] = None,
    marketplace: typing.Optional[typing.Union[SpringCloudServiceMarketplace, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[typing.Union[SpringCloudServiceNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
    service_registry_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sku_name: typing.Optional[builtins.str] = None,
    sku_tier: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[SpringCloudServiceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    trace: typing.Optional[typing.Union[SpringCloudServiceTrace, typing.Dict[builtins.str, typing.Any]]] = None,
    zone_redundant: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__ad35bbcc47b03eeee4181155d67373d01fe8e0d51b1ba3618299222a894f7e77(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39638aee9671f45d58d6bba2a314939da3a0c386ee157ab14b3592cd0067b636(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SpringCloudServiceContainerRegistry, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__523b227bc339dfafd2d32dd936f006061df773c0220770dbd68baf0cb220cdc8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80d6bc42bdb9af348eb094fc1f277e739f09281d03d42990834933818916ca67(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d13564b34e46fd63e34f1ab9cf5c649225e302ff84671592bab6b4e5c327bfb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aad94ca0dd2e90d8e05d871d3bd13dadac5c2dcbb13dad3056238f411b319fcb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f56193208be4fb8428aca748ad086edc60fdef3ef45928c482c99efce30d3e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aba4130e08d36d0b8fd2579f67924266eb7b456a15884326f5b17b9e75f1cd75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5514d5b56bc3c6e292ade1d5e9208f54b04c73bebc61e51634fbdb28bc46fed(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2640e539db73f429d5ce5742e15cad3f1537fd520ebd660784f1a56fbec4fdc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37179df683b8fb159382526be9e73d3e846acfc82b2a61a284bc0a6cda6214f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f39bee6b9393a26f7ce980b335ccb5ab73cbfee36766bde07d3652624c3a437(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d3b72ca445a5271005a2e892291a760357120f1d62df7d989423d5313937bd6(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7992ee5d04d6152937bb1ae0b3d5bdc69dffc926c26782f89e612b209fa90822(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a136544489d7d8f69e5e7df0cac0e23675d630d5fdf5779e39d8e9c6c8ca0903(
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
    build_agent_pool_size: typing.Optional[builtins.str] = None,
    config_server_git_setting: typing.Optional[typing.Union[SpringCloudServiceConfigServerGitSetting, typing.Dict[builtins.str, typing.Any]]] = None,
    container_registry: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SpringCloudServiceContainerRegistry, typing.Dict[builtins.str, typing.Any]]]]] = None,
    default_build_service: typing.Optional[typing.Union[SpringCloudServiceDefaultBuildService, typing.Dict[builtins.str, typing.Any]]] = None,
    id: typing.Optional[builtins.str] = None,
    log_stream_public_endpoint_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    managed_environment_id: typing.Optional[builtins.str] = None,
    marketplace: typing.Optional[typing.Union[SpringCloudServiceMarketplace, typing.Dict[builtins.str, typing.Any]]] = None,
    network: typing.Optional[typing.Union[SpringCloudServiceNetwork, typing.Dict[builtins.str, typing.Any]]] = None,
    service_registry_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    sku_name: typing.Optional[builtins.str] = None,
    sku_tier: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[SpringCloudServiceTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    trace: typing.Optional[typing.Union[SpringCloudServiceTrace, typing.Dict[builtins.str, typing.Any]]] = None,
    zone_redundant: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb9b5edeff9839510436469ee7719fe8a9f066374addfbb8db5d2385e7af4dda(
    *,
    uri: builtins.str,
    http_basic_auth: typing.Optional[typing.Union[SpringCloudServiceConfigServerGitSettingHttpBasicAuth, typing.Dict[builtins.str, typing.Any]]] = None,
    label: typing.Optional[builtins.str] = None,
    repository: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SpringCloudServiceConfigServerGitSettingRepository, typing.Dict[builtins.str, typing.Any]]]]] = None,
    search_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    ssh_auth: typing.Optional[typing.Union[SpringCloudServiceConfigServerGitSettingSshAuth, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd790ed58b3d2ca9cae7a842e5a23db71fa4210c2d0130eae9aefdd649684051(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d61a51be17806f917ae73bce785c189e5a0baf6ede9a5ddf6c28b026934c366e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3b74ade0671b3dd345b750062066f81e48e59225328bd2515e83a41a3a1b515(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ea1c1f3bdb10be45958866832686f23718fdcd2469b8bc2f7848b89394c8aeb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dba473054f7eeb6bf2520bb08503434168866d5345f31169bed86ecd5b216c34(
    value: typing.Optional[SpringCloudServiceConfigServerGitSettingHttpBasicAuth],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c74343258f153e5f6d7eb05b0518fc134b87f3a460f6660192b658f60c7c3ed9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b743ab458d3a88175a43a633e864554999d89db0308692968afce50fe4153f6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SpringCloudServiceConfigServerGitSettingRepository, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c53d600deba52ff63c718324628d80144a8847db532bcde1811066389aa616c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b544065946874e3d350ed49fa152042b0f5ed145e49013178a1431e3b0ffbc25(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa467e0b9dee1eb98361cd4f528aa1668c36f6f4cda9ad2f833227cc0de83661(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a714a863cdfb1285cc50f16c86b7ae4f567e34822042018fd78528ddd9174d8c(
    value: typing.Optional[SpringCloudServiceConfigServerGitSetting],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__071416543596339a60a8fa051935fbc3f2ac8bf5a80732b1b50b1545c713cf4a(
    *,
    name: builtins.str,
    uri: builtins.str,
    http_basic_auth: typing.Optional[typing.Union[SpringCloudServiceConfigServerGitSettingRepositoryHttpBasicAuth, typing.Dict[builtins.str, typing.Any]]] = None,
    label: typing.Optional[builtins.str] = None,
    pattern: typing.Optional[typing.Sequence[builtins.str]] = None,
    search_paths: typing.Optional[typing.Sequence[builtins.str]] = None,
    ssh_auth: typing.Optional[typing.Union[SpringCloudServiceConfigServerGitSettingRepositorySshAuth, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65f98e0f9d80ac487d7c7c106a5914b06bcaf8ee7db2161bebc476b54f345c98(
    *,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb2f5ee2e499692b8296d4f0ff0477b6881caf3d9b08d613d161b0fce957b1db(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1727f872df8cc74868b60f1f04e52fc5c79483544ae741d1e3d7d40bd72e9df(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__389cdce15c56ef2bad635725b6e91b88d9f04fc689029acd3869bd7866f6fc61(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce1b8a720a099374a0f0702401a6b08a9efca92d6ee620bd65b929a85a8efaef(
    value: typing.Optional[SpringCloudServiceConfigServerGitSettingRepositoryHttpBasicAuth],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bb7e5abf84b324ed33c876782219c1b8cdfc284d95770ba9b975d7caf3218ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03c7fdd114ba33640977ee0cc4fe5576b9b71257fc84ab69eee58561e6567a11(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1c6cce36bf55aa27c0bba6b954d92333bf0f0be3d0f6b45b03ee96b4da9da93(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9f053bcc47dbf7f6645b1dc0df05285a03e9b0b1dc8eb7ac464596d3d52d790(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06d752d6711c9c8792f3be78ad919d77c8129af5d701be191e270119ffcdb899(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17b0719bdc69341a4d5dc5260e806e203f81943194a52a3903fd02c78640bb55(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SpringCloudServiceConfigServerGitSettingRepository]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eec260d8d993168b4950a9c7e8ceceafd397085ffb7cfff6fb5f90e683e82445(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb15a6d0759bd13c4a7ae64436aea7bc01c5f4f85684fa225c997b8ec71ef35f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50874ca4f3b5f83febf6635a0ebf8b2b341b6328c262d5b65383264f40252ef0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3fa4ae7742836e4e0389588390d615b98b8ea2bd57513f99cfa9097687ceb3f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__100de8f2f5f8e08a4c09829d4cceca92ca4b0e7da91e3bfb6ea3ec23333f46f9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__463bde87289d64e19280b6a4c6a088f31f9c20870c28eb5fc412c2cf30c4f7b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76273b9668f688af74c95a328f1e2c223195b0b9893d8a2fb88c307531e69c3f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpringCloudServiceConfigServerGitSettingRepository]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49e59b074589c03aa4b0752dd084ae1171a06af6158d78bee6f32df0bc76ec32(
    *,
    private_key: builtins.str,
    host_key: typing.Optional[builtins.str] = None,
    host_key_algorithm: typing.Optional[builtins.str] = None,
    strict_host_key_checking_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ef1d1cc40bf927e00fb1fe0a5c80ad49f76ac99068e081a572a1d65cd232c19(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec57e640bfb44b2f027d512257165d72eb4e85b64cbaa14c2179e779ac940de2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdfc2c27653e62675b33d80a4a67d0bc7e1ad6be188eca50d7fa3cca834f336a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9af81b94d815527a62cb98473162187feb87b7e744e354a3d9e534ce156c0603(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b34dff86f2d2e5c5d067263f6196b63f85577b8dd0308172ec639aa2107b388(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dad7db49b519dc5f3c51a959bc2e14691272f4186d68e5fe274603e01988399(
    value: typing.Optional[SpringCloudServiceConfigServerGitSettingRepositorySshAuth],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f7532691b857066ae56670b2a7f082bdce3e6b3ae327b245be21a5faec87be5(
    *,
    private_key: builtins.str,
    host_key: typing.Optional[builtins.str] = None,
    host_key_algorithm: typing.Optional[builtins.str] = None,
    strict_host_key_checking_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__694657f7e7767f40af3a9d839809472b145a40bdbe8b35fe64eed6df2706aab2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db05581714ff982474cbc931aed5c6d7a9b7dd7ef43c70475a8296abd2650e70(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dc43b05f397564a55ecaeb4402e26502fa1359823028bf359b5b732275d8991(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed89b6d5c8a961555ac5943289cd03a0af9276fb9f12d9c657b28d6d8ff4ad37(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d76c4ef1585fdb25a17c986fb639b9bba33e83a902d8e3dda1b348c1110038b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41139732b75a6e7e33d7df26897da5f220201b000beea065fef3347c7b6af7eb(
    value: typing.Optional[SpringCloudServiceConfigServerGitSettingSshAuth],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ce265d2bb968386a1187b8971ed3a9d607c69c231856a7e45c0f9b244acb3a1(
    *,
    name: builtins.str,
    password: builtins.str,
    server: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f950a94fadc63543e2144be88b9403b8f3356d3eb0db057bc1df72f12e14607d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deff2b937c5e2de040e70e104f591b3e78267efdf1558a585683942be6bfe2ab(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20d06ddbfe86f8c69333db04fa4b3f11929d47dcb38e1c79b780a4419957290e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f21acf837bf3bd9e2dd03032762cf3da28d56a8ebf4fd0cfc1531bd0709f757e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f00829adef1bf2ea03b53497c3cec605019a283dbd9f67a3b11ece0c3c2a4d2d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bc9e1b634e5808f6ca226d7255c2e5576d1ada75a2aa3a60cad60762513b33e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SpringCloudServiceContainerRegistry]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cecc4203120346bdb3dae135686e42d89090aaf52c383d9f900c0a814893f4f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bf0a071273a11088cfb9508fd3783845ddb8c87b1615bde1474bef925c8b098(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d807cba435a6a7db387cc6e43c0367de483fe76eb3eba8e20513d1244c298c86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f80511e51dc758cc761ad8e6437142f66e9cc0da5aa6c9a8abd499ca6d831385(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6756e736b7193a1d81566384a898e0f6a4887c0b8bfd285483fc8354ff4e2598(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a761d4c5e7022aaeb9eb6cbec7f8ad7e25b6af4cb96cdbb50e90f0958e3c7a6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpringCloudServiceContainerRegistry]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2cc09276bb3af22e3d80c59be5234eb9b662ef2dc0d83140ba28accea582c31(
    *,
    container_registry_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b685ff62d0b8698c9c6b0ce47c0f4f91670e40a0ccaa41d6f93993b694b5267(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__702e5ccfb1d3c69495eaf71d9b9ae389ab9f004ebe600c873fce807742382472(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ef0823f2292cb38d12344f27a1401517378a67965cd70705c1fafb493cc9086(
    value: typing.Optional[SpringCloudServiceDefaultBuildService],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f9e4bbcd040381b5d1ffe139f7e54f05fbf700faef3ef22f1d113f539643e3f(
    *,
    plan: builtins.str,
    product: builtins.str,
    publisher: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c4c77a1be4497eec93f81ad05c34e4b2128f9f2dda1749818872f6074b8d8c1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__612d49308c4526dd1546150c14054febd1c30acaf586e58e47d7e04c7af3b4dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b00882e9b72e51101611839d76b18f271a9cd261268713627fabe3110131e2eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2679a145e3215c8b906992ca804ae2de91b2f46ef6bbba80ba9d062356c99872(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__617cd4717fe6c6222564506e82d0f04a2f86000cd3722fa5c7151b227579d82e(
    value: typing.Optional[SpringCloudServiceMarketplace],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69751b81327a0e961b3c8271acbf3fcc441d5552872d671599ed3c5ae060b85a(
    *,
    app_subnet_id: builtins.str,
    cidr_ranges: typing.Sequence[builtins.str],
    service_runtime_subnet_id: builtins.str,
    app_network_resource_group: typing.Optional[builtins.str] = None,
    outbound_type: typing.Optional[builtins.str] = None,
    read_timeout_seconds: typing.Optional[jsii.Number] = None,
    service_runtime_network_resource_group: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57c74997c8be05848790c841e7ec8e7e009a66cf2b9cae93c8792d4ab7f8979a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9475c3dcdf57aef01a0099cac7ac930c9516f32ffeb83450b50616ee641b34b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fe230b8e85dcb48a93d971a0ada538f5391e5a2c0a1a89d175850b0fa86eb75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a2a5360c2c9260a210806b9fd50a187dbc565a0e53dbcc899a70b26fa5665e0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9faea2a9c7cba5765711767789f2aeb4a0c8cf9b8d20ecdb20eef2cd6f932612(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78edd7671975f821a6a1f46a0427115f49d319ac0e40bc16da1c31b81eb47dce(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ab16444e38497a769d5ff890894b08f44fb43a832d7e1eea247f414bd98f3a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e6a122f46b8a8c33770380fd9d5069e7969b9e55abeda3f345033a1d8966dbb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3932536a63bbe1ad0c982523f45f189f7513a1859cd63c04fccc736013e07cc4(
    value: typing.Optional[SpringCloudServiceNetwork],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__527f31cb815fbe94cd6719b8cb0ad5dd5b3e404c5a529474bb263100c840da22(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53a62ad1ced3cc08f848cfdec9991c938da3a933adbfe253a80634af8b871a4d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3b7d8535ae62a3f76ec718d1ae7963f99a7956953ed2520f6f4ca768ef08c5c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f936d9e79f10e586be8d60668a3411ddb353bd03054d2834d873e22aa193edbc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7f7c0ebc1e91f50b46e8c9d7aa3f31f5917f24ba2fd6b6f7ee6d6fb140e4e06(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf73b70cd70d61354e98570e9b809bef0649c3a8c615ab91b623a2c1f6c635dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15ac16dd8d47763fd1d22bdba14440587fff1368a78adb2b8308ae8d8be671f0(
    value: typing.Optional[SpringCloudServiceRequiredNetworkTrafficRules],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1df6602921dfa74929aabbee65c50741e4c2237d1727c6551ab8af9b2f5b95c3(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31eefe97471fc82d8624b0afed2422f0f6738699326db6b7bf528258d9f7c0ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3faa8c837df835d81b0b5f476a967149e101c0494efff322a87b1456032c72b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a81abfe66b93cc7f82c0ec856f30329ae931136c9f43eb44bdc6619de9589f46(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf0b575468b1b0ca7c06b4bdd3e74eda8838ab3a38b80865247980245fef4bcf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2665a8451c80df7f0e3372051dea6bd89a4832be4a9863d5112294baa219d4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70f155bed59df3875da44069a3e7b59e32a11da6988040a740a67ea1c7927cb9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpringCloudServiceTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dfa5ef8b8a93d3a913651f68b4547dcf7d3ec089b3b2ce8b08f8297d7bbe185(
    *,
    connection_string: typing.Optional[builtins.str] = None,
    sample_rate: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ca12bf59ad787e8110f7ce3e9a5c1df30a08a5057526d4f383400e045360f8e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac6fe4a6932b8f2591bc1b88537a1ea653e0b2a98f644e486c7b81a9ed08c8c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__607aef23025ed6837af06128086f6bda861cb527985ffe7be702450d4aa58257(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44487f4e912fdb09ef32f91ab79a230fd873911881beeeb28aca7eef5d6434c9(
    value: typing.Optional[SpringCloudServiceTrace],
) -> None:
    """Type checking stubs"""
    pass
