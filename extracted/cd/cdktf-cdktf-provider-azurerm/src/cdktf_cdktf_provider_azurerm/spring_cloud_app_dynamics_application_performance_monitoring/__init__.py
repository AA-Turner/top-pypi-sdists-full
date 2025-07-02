r'''
# `azurerm_spring_cloud_app_dynamics_application_performance_monitoring`

Refer to the Terraform Registry for docs: [`azurerm_spring_cloud_app_dynamics_application_performance_monitoring`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring).
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


class SpringCloudAppDynamicsApplicationPerformanceMonitoring(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudAppDynamicsApplicationPerformanceMonitoring.SpringCloudAppDynamicsApplicationPerformanceMonitoring",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring azurerm_spring_cloud_app_dynamics_application_performance_monitoring}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        agent_account_access_key: builtins.str,
        agent_account_name: builtins.str,
        controller_host_name: builtins.str,
        name: builtins.str,
        spring_cloud_service_id: builtins.str,
        agent_application_name: typing.Optional[builtins.str] = None,
        agent_node_name: typing.Optional[builtins.str] = None,
        agent_tier_name: typing.Optional[builtins.str] = None,
        agent_unique_host_id: typing.Optional[builtins.str] = None,
        controller_port: typing.Optional[jsii.Number] = None,
        controller_ssl_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        globally_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["SpringCloudAppDynamicsApplicationPerformanceMonitoringTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring azurerm_spring_cloud_app_dynamics_application_performance_monitoring} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param agent_account_access_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#agent_account_access_key SpringCloudAppDynamicsApplicationPerformanceMonitoring#agent_account_access_key}.
        :param agent_account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#agent_account_name SpringCloudAppDynamicsApplicationPerformanceMonitoring#agent_account_name}.
        :param controller_host_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#controller_host_name SpringCloudAppDynamicsApplicationPerformanceMonitoring#controller_host_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#name SpringCloudAppDynamicsApplicationPerformanceMonitoring#name}.
        :param spring_cloud_service_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#spring_cloud_service_id SpringCloudAppDynamicsApplicationPerformanceMonitoring#spring_cloud_service_id}.
        :param agent_application_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#agent_application_name SpringCloudAppDynamicsApplicationPerformanceMonitoring#agent_application_name}.
        :param agent_node_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#agent_node_name SpringCloudAppDynamicsApplicationPerformanceMonitoring#agent_node_name}.
        :param agent_tier_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#agent_tier_name SpringCloudAppDynamicsApplicationPerformanceMonitoring#agent_tier_name}.
        :param agent_unique_host_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#agent_unique_host_id SpringCloudAppDynamicsApplicationPerformanceMonitoring#agent_unique_host_id}.
        :param controller_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#controller_port SpringCloudAppDynamicsApplicationPerformanceMonitoring#controller_port}.
        :param controller_ssl_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#controller_ssl_enabled SpringCloudAppDynamicsApplicationPerformanceMonitoring#controller_ssl_enabled}.
        :param globally_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#globally_enabled SpringCloudAppDynamicsApplicationPerformanceMonitoring#globally_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#id SpringCloudAppDynamicsApplicationPerformanceMonitoring#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#timeouts SpringCloudAppDynamicsApplicationPerformanceMonitoring#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4c7bf2aa520cc825af904522203d52200e809b59dcc9809ea579aab7748c90c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SpringCloudAppDynamicsApplicationPerformanceMonitoringConfig(
            agent_account_access_key=agent_account_access_key,
            agent_account_name=agent_account_name,
            controller_host_name=controller_host_name,
            name=name,
            spring_cloud_service_id=spring_cloud_service_id,
            agent_application_name=agent_application_name,
            agent_node_name=agent_node_name,
            agent_tier_name=agent_tier_name,
            agent_unique_host_id=agent_unique_host_id,
            controller_port=controller_port,
            controller_ssl_enabled=controller_ssl_enabled,
            globally_enabled=globally_enabled,
            id=id,
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
        '''Generates CDKTF code for importing a SpringCloudAppDynamicsApplicationPerformanceMonitoring resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the SpringCloudAppDynamicsApplicationPerformanceMonitoring to import.
        :param import_from_id: The id of the existing SpringCloudAppDynamicsApplicationPerformanceMonitoring that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the SpringCloudAppDynamicsApplicationPerformanceMonitoring to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15768d899eac466fd0acb8056009253deaa36d4a19d33a974c2ec671b599f8b9)
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#create SpringCloudAppDynamicsApplicationPerformanceMonitoring#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#delete SpringCloudAppDynamicsApplicationPerformanceMonitoring#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#read SpringCloudAppDynamicsApplicationPerformanceMonitoring#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#update SpringCloudAppDynamicsApplicationPerformanceMonitoring#update}.
        '''
        value = SpringCloudAppDynamicsApplicationPerformanceMonitoringTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAgentApplicationName")
    def reset_agent_application_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAgentApplicationName", []))

    @jsii.member(jsii_name="resetAgentNodeName")
    def reset_agent_node_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAgentNodeName", []))

    @jsii.member(jsii_name="resetAgentTierName")
    def reset_agent_tier_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAgentTierName", []))

    @jsii.member(jsii_name="resetAgentUniqueHostId")
    def reset_agent_unique_host_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAgentUniqueHostId", []))

    @jsii.member(jsii_name="resetControllerPort")
    def reset_controller_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetControllerPort", []))

    @jsii.member(jsii_name="resetControllerSslEnabled")
    def reset_controller_ssl_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetControllerSslEnabled", []))

    @jsii.member(jsii_name="resetGloballyEnabled")
    def reset_globally_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGloballyEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    def timeouts(
        self,
    ) -> "SpringCloudAppDynamicsApplicationPerformanceMonitoringTimeoutsOutputReference":
        return typing.cast("SpringCloudAppDynamicsApplicationPerformanceMonitoringTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="agentAccountAccessKeyInput")
    def agent_account_access_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agentAccountAccessKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="agentAccountNameInput")
    def agent_account_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agentAccountNameInput"))

    @builtins.property
    @jsii.member(jsii_name="agentApplicationNameInput")
    def agent_application_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agentApplicationNameInput"))

    @builtins.property
    @jsii.member(jsii_name="agentNodeNameInput")
    def agent_node_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agentNodeNameInput"))

    @builtins.property
    @jsii.member(jsii_name="agentTierNameInput")
    def agent_tier_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agentTierNameInput"))

    @builtins.property
    @jsii.member(jsii_name="agentUniqueHostIdInput")
    def agent_unique_host_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "agentUniqueHostIdInput"))

    @builtins.property
    @jsii.member(jsii_name="controllerHostNameInput")
    def controller_host_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "controllerHostNameInput"))

    @builtins.property
    @jsii.member(jsii_name="controllerPortInput")
    def controller_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "controllerPortInput"))

    @builtins.property
    @jsii.member(jsii_name="controllerSslEnabledInput")
    def controller_ssl_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "controllerSslEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="globallyEnabledInput")
    def globally_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "globallyEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="springCloudServiceIdInput")
    def spring_cloud_service_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "springCloudServiceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SpringCloudAppDynamicsApplicationPerformanceMonitoringTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "SpringCloudAppDynamicsApplicationPerformanceMonitoringTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="agentAccountAccessKey")
    def agent_account_access_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agentAccountAccessKey"))

    @agent_account_access_key.setter
    def agent_account_access_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b874817aaf4c4d44d5b5cca71bcb5bd312763bd94d33fa0c3861fad008641a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentAccountAccessKey", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="agentAccountName")
    def agent_account_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agentAccountName"))

    @agent_account_name.setter
    def agent_account_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6b154f102fe76510b616d1833a7f55bbb7d89bb9e6f46b5ef0eb68114fa07c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentAccountName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="agentApplicationName")
    def agent_application_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agentApplicationName"))

    @agent_application_name.setter
    def agent_application_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d955aef2700fee6033b15831d63dce7453d35cc35da640c8d6aca6b3faae34b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentApplicationName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="agentNodeName")
    def agent_node_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agentNodeName"))

    @agent_node_name.setter
    def agent_node_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad5495b99946e4495d058166c6b22602e583af772bea3a3572bbd46e65c2cfbc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentNodeName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="agentTierName")
    def agent_tier_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agentTierName"))

    @agent_tier_name.setter
    def agent_tier_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3716b9f0c61bd9e13f4a734c35af4f1aff9dc97373bd6f50bf5b36830141833a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentTierName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="agentUniqueHostId")
    def agent_unique_host_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "agentUniqueHostId"))

    @agent_unique_host_id.setter
    def agent_unique_host_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2331cca0114957861e949f1b12efe0059b95ea3708656ded2f4ae4fb2d796699)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentUniqueHostId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="controllerHostName")
    def controller_host_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "controllerHostName"))

    @controller_host_name.setter
    def controller_host_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26dd65d85f6250b105d164bb789e01e9c1acda787b66884131a75ed835b7c5cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controllerHostName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="controllerPort")
    def controller_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "controllerPort"))

    @controller_port.setter
    def controller_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39392e2738ea050783f9acf59da6f9c4bae32f5929e270011ae2c741ab9ce7f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controllerPort", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="controllerSslEnabled")
    def controller_ssl_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "controllerSslEnabled"))

    @controller_ssl_enabled.setter
    def controller_ssl_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f9a3565f22d2d5448963a83d48f885d9e3f310812c660df11423a937a4759b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "controllerSslEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="globallyEnabled")
    def globally_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "globallyEnabled"))

    @globally_enabled.setter
    def globally_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abe50d9f6d007ba6422565fc8ec8b3dbd890173f20b7a0e77b6a83cdb88b9574)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "globallyEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82bce8a65ea8c1361377b4db20844e63e19980d6e6c14a9809ae6d5bad54a97f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a3c84d3038f69bef6b87f9fd8af684d2abc1e64ec88d7dc9747bb650322636d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="springCloudServiceId")
    def spring_cloud_service_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "springCloudServiceId"))

    @spring_cloud_service_id.setter
    def spring_cloud_service_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59c061faf7e30142933a6e100857f3daca21ebb570ee98bdb8728c134162bcad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "springCloudServiceId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.springCloudAppDynamicsApplicationPerformanceMonitoring.SpringCloudAppDynamicsApplicationPerformanceMonitoringConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "agent_account_access_key": "agentAccountAccessKey",
        "agent_account_name": "agentAccountName",
        "controller_host_name": "controllerHostName",
        "name": "name",
        "spring_cloud_service_id": "springCloudServiceId",
        "agent_application_name": "agentApplicationName",
        "agent_node_name": "agentNodeName",
        "agent_tier_name": "agentTierName",
        "agent_unique_host_id": "agentUniqueHostId",
        "controller_port": "controllerPort",
        "controller_ssl_enabled": "controllerSslEnabled",
        "globally_enabled": "globallyEnabled",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class SpringCloudAppDynamicsApplicationPerformanceMonitoringConfig(
    _cdktf_9a9027ec.TerraformMetaArguments,
):
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
        agent_account_access_key: builtins.str,
        agent_account_name: builtins.str,
        controller_host_name: builtins.str,
        name: builtins.str,
        spring_cloud_service_id: builtins.str,
        agent_application_name: typing.Optional[builtins.str] = None,
        agent_node_name: typing.Optional[builtins.str] = None,
        agent_tier_name: typing.Optional[builtins.str] = None,
        agent_unique_host_id: typing.Optional[builtins.str] = None,
        controller_port: typing.Optional[jsii.Number] = None,
        controller_ssl_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        globally_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["SpringCloudAppDynamicsApplicationPerformanceMonitoringTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param agent_account_access_key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#agent_account_access_key SpringCloudAppDynamicsApplicationPerformanceMonitoring#agent_account_access_key}.
        :param agent_account_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#agent_account_name SpringCloudAppDynamicsApplicationPerformanceMonitoring#agent_account_name}.
        :param controller_host_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#controller_host_name SpringCloudAppDynamicsApplicationPerformanceMonitoring#controller_host_name}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#name SpringCloudAppDynamicsApplicationPerformanceMonitoring#name}.
        :param spring_cloud_service_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#spring_cloud_service_id SpringCloudAppDynamicsApplicationPerformanceMonitoring#spring_cloud_service_id}.
        :param agent_application_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#agent_application_name SpringCloudAppDynamicsApplicationPerformanceMonitoring#agent_application_name}.
        :param agent_node_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#agent_node_name SpringCloudAppDynamicsApplicationPerformanceMonitoring#agent_node_name}.
        :param agent_tier_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#agent_tier_name SpringCloudAppDynamicsApplicationPerformanceMonitoring#agent_tier_name}.
        :param agent_unique_host_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#agent_unique_host_id SpringCloudAppDynamicsApplicationPerformanceMonitoring#agent_unique_host_id}.
        :param controller_port: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#controller_port SpringCloudAppDynamicsApplicationPerformanceMonitoring#controller_port}.
        :param controller_ssl_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#controller_ssl_enabled SpringCloudAppDynamicsApplicationPerformanceMonitoring#controller_ssl_enabled}.
        :param globally_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#globally_enabled SpringCloudAppDynamicsApplicationPerformanceMonitoring#globally_enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#id SpringCloudAppDynamicsApplicationPerformanceMonitoring#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#timeouts SpringCloudAppDynamicsApplicationPerformanceMonitoring#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = SpringCloudAppDynamicsApplicationPerformanceMonitoringTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88aefcc737d0a7402b08216f501259e88beee430dbe8cc9e4b429da8cae45ae5)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument agent_account_access_key", value=agent_account_access_key, expected_type=type_hints["agent_account_access_key"])
            check_type(argname="argument agent_account_name", value=agent_account_name, expected_type=type_hints["agent_account_name"])
            check_type(argname="argument controller_host_name", value=controller_host_name, expected_type=type_hints["controller_host_name"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument spring_cloud_service_id", value=spring_cloud_service_id, expected_type=type_hints["spring_cloud_service_id"])
            check_type(argname="argument agent_application_name", value=agent_application_name, expected_type=type_hints["agent_application_name"])
            check_type(argname="argument agent_node_name", value=agent_node_name, expected_type=type_hints["agent_node_name"])
            check_type(argname="argument agent_tier_name", value=agent_tier_name, expected_type=type_hints["agent_tier_name"])
            check_type(argname="argument agent_unique_host_id", value=agent_unique_host_id, expected_type=type_hints["agent_unique_host_id"])
            check_type(argname="argument controller_port", value=controller_port, expected_type=type_hints["controller_port"])
            check_type(argname="argument controller_ssl_enabled", value=controller_ssl_enabled, expected_type=type_hints["controller_ssl_enabled"])
            check_type(argname="argument globally_enabled", value=globally_enabled, expected_type=type_hints["globally_enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "agent_account_access_key": agent_account_access_key,
            "agent_account_name": agent_account_name,
            "controller_host_name": controller_host_name,
            "name": name,
            "spring_cloud_service_id": spring_cloud_service_id,
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
        if agent_application_name is not None:
            self._values["agent_application_name"] = agent_application_name
        if agent_node_name is not None:
            self._values["agent_node_name"] = agent_node_name
        if agent_tier_name is not None:
            self._values["agent_tier_name"] = agent_tier_name
        if agent_unique_host_id is not None:
            self._values["agent_unique_host_id"] = agent_unique_host_id
        if controller_port is not None:
            self._values["controller_port"] = controller_port
        if controller_ssl_enabled is not None:
            self._values["controller_ssl_enabled"] = controller_ssl_enabled
        if globally_enabled is not None:
            self._values["globally_enabled"] = globally_enabled
        if id is not None:
            self._values["id"] = id
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
    def agent_account_access_key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#agent_account_access_key SpringCloudAppDynamicsApplicationPerformanceMonitoring#agent_account_access_key}.'''
        result = self._values.get("agent_account_access_key")
        assert result is not None, "Required property 'agent_account_access_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def agent_account_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#agent_account_name SpringCloudAppDynamicsApplicationPerformanceMonitoring#agent_account_name}.'''
        result = self._values.get("agent_account_name")
        assert result is not None, "Required property 'agent_account_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def controller_host_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#controller_host_name SpringCloudAppDynamicsApplicationPerformanceMonitoring#controller_host_name}.'''
        result = self._values.get("controller_host_name")
        assert result is not None, "Required property 'controller_host_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#name SpringCloudAppDynamicsApplicationPerformanceMonitoring#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def spring_cloud_service_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#spring_cloud_service_id SpringCloudAppDynamicsApplicationPerformanceMonitoring#spring_cloud_service_id}.'''
        result = self._values.get("spring_cloud_service_id")
        assert result is not None, "Required property 'spring_cloud_service_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def agent_application_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#agent_application_name SpringCloudAppDynamicsApplicationPerformanceMonitoring#agent_application_name}.'''
        result = self._values.get("agent_application_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def agent_node_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#agent_node_name SpringCloudAppDynamicsApplicationPerformanceMonitoring#agent_node_name}.'''
        result = self._values.get("agent_node_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def agent_tier_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#agent_tier_name SpringCloudAppDynamicsApplicationPerformanceMonitoring#agent_tier_name}.'''
        result = self._values.get("agent_tier_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def agent_unique_host_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#agent_unique_host_id SpringCloudAppDynamicsApplicationPerformanceMonitoring#agent_unique_host_id}.'''
        result = self._values.get("agent_unique_host_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def controller_port(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#controller_port SpringCloudAppDynamicsApplicationPerformanceMonitoring#controller_port}.'''
        result = self._values.get("controller_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def controller_ssl_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#controller_ssl_enabled SpringCloudAppDynamicsApplicationPerformanceMonitoring#controller_ssl_enabled}.'''
        result = self._values.get("controller_ssl_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def globally_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#globally_enabled SpringCloudAppDynamicsApplicationPerformanceMonitoring#globally_enabled}.'''
        result = self._values.get("globally_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#id SpringCloudAppDynamicsApplicationPerformanceMonitoring#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["SpringCloudAppDynamicsApplicationPerformanceMonitoringTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#timeouts SpringCloudAppDynamicsApplicationPerformanceMonitoring#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["SpringCloudAppDynamicsApplicationPerformanceMonitoringTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpringCloudAppDynamicsApplicationPerformanceMonitoringConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.springCloudAppDynamicsApplicationPerformanceMonitoring.SpringCloudAppDynamicsApplicationPerformanceMonitoringTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class SpringCloudAppDynamicsApplicationPerformanceMonitoringTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#create SpringCloudAppDynamicsApplicationPerformanceMonitoring#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#delete SpringCloudAppDynamicsApplicationPerformanceMonitoring#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#read SpringCloudAppDynamicsApplicationPerformanceMonitoring#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#update SpringCloudAppDynamicsApplicationPerformanceMonitoring#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91d9342ae80577ff2abb3cb8b419b78e86f7de6964efe32e98a523de463e36ac)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#create SpringCloudAppDynamicsApplicationPerformanceMonitoring#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#delete SpringCloudAppDynamicsApplicationPerformanceMonitoring#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#read SpringCloudAppDynamicsApplicationPerformanceMonitoring#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/spring_cloud_app_dynamics_application_performance_monitoring#update SpringCloudAppDynamicsApplicationPerformanceMonitoring#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SpringCloudAppDynamicsApplicationPerformanceMonitoringTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SpringCloudAppDynamicsApplicationPerformanceMonitoringTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.springCloudAppDynamicsApplicationPerformanceMonitoring.SpringCloudAppDynamicsApplicationPerformanceMonitoringTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__81be8f902ed246d9708f77349dbf9a6ad6a45ea116feb423cf665e7a0de10869)
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
            type_hints = typing.get_type_hints(_typecheckingstub__49f7dc1049302c1952541ff770147ef6c2dae74a59f882a8c386a7716e51c2d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__468cec3655676ef8c9b41067c929070ed6e35140248c33a53e269096f1cf1048)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c7549a8e3872bed1ab4e19f0c1270738dcfefb7fc1f7166146ff6f1586f3642)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24bd22a5eb37e9eca839b610d2aa80ae15bb28521732112a2e7c9c1bc1210a53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpringCloudAppDynamicsApplicationPerformanceMonitoringTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpringCloudAppDynamicsApplicationPerformanceMonitoringTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpringCloudAppDynamicsApplicationPerformanceMonitoringTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a27f0891edff90d185c5f38923b01042b83b81bd3aba253ba39a47669cc72920)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "SpringCloudAppDynamicsApplicationPerformanceMonitoring",
    "SpringCloudAppDynamicsApplicationPerformanceMonitoringConfig",
    "SpringCloudAppDynamicsApplicationPerformanceMonitoringTimeouts",
    "SpringCloudAppDynamicsApplicationPerformanceMonitoringTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f4c7bf2aa520cc825af904522203d52200e809b59dcc9809ea579aab7748c90c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    agent_account_access_key: builtins.str,
    agent_account_name: builtins.str,
    controller_host_name: builtins.str,
    name: builtins.str,
    spring_cloud_service_id: builtins.str,
    agent_application_name: typing.Optional[builtins.str] = None,
    agent_node_name: typing.Optional[builtins.str] = None,
    agent_tier_name: typing.Optional[builtins.str] = None,
    agent_unique_host_id: typing.Optional[builtins.str] = None,
    controller_port: typing.Optional[jsii.Number] = None,
    controller_ssl_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    globally_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[SpringCloudAppDynamicsApplicationPerformanceMonitoringTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__15768d899eac466fd0acb8056009253deaa36d4a19d33a974c2ec671b599f8b9(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b874817aaf4c4d44d5b5cca71bcb5bd312763bd94d33fa0c3861fad008641a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6b154f102fe76510b616d1833a7f55bbb7d89bb9e6f46b5ef0eb68114fa07c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d955aef2700fee6033b15831d63dce7453d35cc35da640c8d6aca6b3faae34b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad5495b99946e4495d058166c6b22602e583af772bea3a3572bbd46e65c2cfbc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3716b9f0c61bd9e13f4a734c35af4f1aff9dc97373bd6f50bf5b36830141833a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2331cca0114957861e949f1b12efe0059b95ea3708656ded2f4ae4fb2d796699(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26dd65d85f6250b105d164bb789e01e9c1acda787b66884131a75ed835b7c5cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39392e2738ea050783f9acf59da6f9c4bae32f5929e270011ae2c741ab9ce7f4(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f9a3565f22d2d5448963a83d48f885d9e3f310812c660df11423a937a4759b5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abe50d9f6d007ba6422565fc8ec8b3dbd890173f20b7a0e77b6a83cdb88b9574(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82bce8a65ea8c1361377b4db20844e63e19980d6e6c14a9809ae6d5bad54a97f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a3c84d3038f69bef6b87f9fd8af684d2abc1e64ec88d7dc9747bb650322636d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59c061faf7e30142933a6e100857f3daca21ebb570ee98bdb8728c134162bcad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88aefcc737d0a7402b08216f501259e88beee430dbe8cc9e4b429da8cae45ae5(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    agent_account_access_key: builtins.str,
    agent_account_name: builtins.str,
    controller_host_name: builtins.str,
    name: builtins.str,
    spring_cloud_service_id: builtins.str,
    agent_application_name: typing.Optional[builtins.str] = None,
    agent_node_name: typing.Optional[builtins.str] = None,
    agent_tier_name: typing.Optional[builtins.str] = None,
    agent_unique_host_id: typing.Optional[builtins.str] = None,
    controller_port: typing.Optional[jsii.Number] = None,
    controller_ssl_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    globally_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[SpringCloudAppDynamicsApplicationPerformanceMonitoringTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91d9342ae80577ff2abb3cb8b419b78e86f7de6964efe32e98a523de463e36ac(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81be8f902ed246d9708f77349dbf9a6ad6a45ea116feb423cf665e7a0de10869(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49f7dc1049302c1952541ff770147ef6c2dae74a59f882a8c386a7716e51c2d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__468cec3655676ef8c9b41067c929070ed6e35140248c33a53e269096f1cf1048(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c7549a8e3872bed1ab4e19f0c1270738dcfefb7fc1f7166146ff6f1586f3642(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24bd22a5eb37e9eca839b610d2aa80ae15bb28521732112a2e7c9c1bc1210a53(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a27f0891edff90d185c5f38923b01042b83b81bd3aba253ba39a47669cc72920(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, SpringCloudAppDynamicsApplicationPerformanceMonitoringTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
