r'''
# `azurerm_iot_security_solution`

Refer to the Terraform Registry for docs: [`azurerm_iot_security_solution`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution).
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


class IotSecuritySolution(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.iotSecuritySolution.IotSecuritySolution",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution azurerm_iot_security_solution}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        iothub_ids: typing.Sequence[builtins.str],
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        additional_workspace: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotSecuritySolutionAdditionalWorkspace", typing.Dict[builtins.str, typing.Any]]]]] = None,
        disabled_data_sources: typing.Optional[typing.Sequence[builtins.str]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        events_to_export: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        log_analytics_workspace_id: typing.Optional[builtins.str] = None,
        log_unmasked_ips_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        query_for_resources: typing.Optional[builtins.str] = None,
        query_subscription_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        recommendations_enabled: typing.Optional[typing.Union["IotSecuritySolutionRecommendationsEnabled", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["IotSecuritySolutionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution azurerm_iot_security_solution} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#display_name IotSecuritySolution#display_name}.
        :param iothub_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#iothub_ids IotSecuritySolution#iothub_ids}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#location IotSecuritySolution#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#name IotSecuritySolution#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#resource_group_name IotSecuritySolution#resource_group_name}.
        :param additional_workspace: additional_workspace block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#additional_workspace IotSecuritySolution#additional_workspace}
        :param disabled_data_sources: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#disabled_data_sources IotSecuritySolution#disabled_data_sources}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#enabled IotSecuritySolution#enabled}.
        :param events_to_export: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#events_to_export IotSecuritySolution#events_to_export}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#id IotSecuritySolution#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#log_analytics_workspace_id IotSecuritySolution#log_analytics_workspace_id}.
        :param log_unmasked_ips_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#log_unmasked_ips_enabled IotSecuritySolution#log_unmasked_ips_enabled}.
        :param query_for_resources: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#query_for_resources IotSecuritySolution#query_for_resources}.
        :param query_subscription_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#query_subscription_ids IotSecuritySolution#query_subscription_ids}.
        :param recommendations_enabled: recommendations_enabled block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#recommendations_enabled IotSecuritySolution#recommendations_enabled}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#tags IotSecuritySolution#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#timeouts IotSecuritySolution#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__976f32ea276c518cd31e488a6a6b611a0e2dfeb44c89eba63aa3b65792b77453)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = IotSecuritySolutionConfig(
            display_name=display_name,
            iothub_ids=iothub_ids,
            location=location,
            name=name,
            resource_group_name=resource_group_name,
            additional_workspace=additional_workspace,
            disabled_data_sources=disabled_data_sources,
            enabled=enabled,
            events_to_export=events_to_export,
            id=id,
            log_analytics_workspace_id=log_analytics_workspace_id,
            log_unmasked_ips_enabled=log_unmasked_ips_enabled,
            query_for_resources=query_for_resources,
            query_subscription_ids=query_subscription_ids,
            recommendations_enabled=recommendations_enabled,
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
        '''Generates CDKTF code for importing a IotSecuritySolution resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the IotSecuritySolution to import.
        :param import_from_id: The id of the existing IotSecuritySolution that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the IotSecuritySolution to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e20eaaaa368dc72a7f4673e35e3558bdb5d876b39776dd7b79902b6ff13c0580)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAdditionalWorkspace")
    def put_additional_workspace(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["IotSecuritySolutionAdditionalWorkspace", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__707b0e31b5eca676a55708b524d645ef965b8bd07ad3e0558aba552ad8d531ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAdditionalWorkspace", [value]))

    @jsii.member(jsii_name="putRecommendationsEnabled")
    def put_recommendations_enabled(
        self,
        *,
        acr_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        agent_send_unutilized_msg: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        baseline: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        edge_hub_mem_optimize: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        edge_logging_option: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        inconsistent_module_settings: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        install_agent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ip_filter_deny_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ip_filter_permissive_rule: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        open_ports: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        permissive_firewall_policy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        permissive_input_firewall_rules: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        permissive_output_firewall_rules: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        privileged_docker_options: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        shared_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vulnerable_tls_cipher_suite: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param acr_authentication: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#acr_authentication IotSecuritySolution#acr_authentication}.
        :param agent_send_unutilized_msg: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#agent_send_unutilized_msg IotSecuritySolution#agent_send_unutilized_msg}.
        :param baseline: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#baseline IotSecuritySolution#baseline}.
        :param edge_hub_mem_optimize: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#edge_hub_mem_optimize IotSecuritySolution#edge_hub_mem_optimize}.
        :param edge_logging_option: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#edge_logging_option IotSecuritySolution#edge_logging_option}.
        :param inconsistent_module_settings: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#inconsistent_module_settings IotSecuritySolution#inconsistent_module_settings}.
        :param install_agent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#install_agent IotSecuritySolution#install_agent}.
        :param ip_filter_deny_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#ip_filter_deny_all IotSecuritySolution#ip_filter_deny_all}.
        :param ip_filter_permissive_rule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#ip_filter_permissive_rule IotSecuritySolution#ip_filter_permissive_rule}.
        :param open_ports: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#open_ports IotSecuritySolution#open_ports}.
        :param permissive_firewall_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#permissive_firewall_policy IotSecuritySolution#permissive_firewall_policy}.
        :param permissive_input_firewall_rules: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#permissive_input_firewall_rules IotSecuritySolution#permissive_input_firewall_rules}.
        :param permissive_output_firewall_rules: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#permissive_output_firewall_rules IotSecuritySolution#permissive_output_firewall_rules}.
        :param privileged_docker_options: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#privileged_docker_options IotSecuritySolution#privileged_docker_options}.
        :param shared_credentials: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#shared_credentials IotSecuritySolution#shared_credentials}.
        :param vulnerable_tls_cipher_suite: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#vulnerable_tls_cipher_suite IotSecuritySolution#vulnerable_tls_cipher_suite}.
        '''
        value = IotSecuritySolutionRecommendationsEnabled(
            acr_authentication=acr_authentication,
            agent_send_unutilized_msg=agent_send_unutilized_msg,
            baseline=baseline,
            edge_hub_mem_optimize=edge_hub_mem_optimize,
            edge_logging_option=edge_logging_option,
            inconsistent_module_settings=inconsistent_module_settings,
            install_agent=install_agent,
            ip_filter_deny_all=ip_filter_deny_all,
            ip_filter_permissive_rule=ip_filter_permissive_rule,
            open_ports=open_ports,
            permissive_firewall_policy=permissive_firewall_policy,
            permissive_input_firewall_rules=permissive_input_firewall_rules,
            permissive_output_firewall_rules=permissive_output_firewall_rules,
            privileged_docker_options=privileged_docker_options,
            shared_credentials=shared_credentials,
            vulnerable_tls_cipher_suite=vulnerable_tls_cipher_suite,
        )

        return typing.cast(None, jsii.invoke(self, "putRecommendationsEnabled", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#create IotSecuritySolution#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#delete IotSecuritySolution#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#read IotSecuritySolution#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#update IotSecuritySolution#update}.
        '''
        value = IotSecuritySolutionTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAdditionalWorkspace")
    def reset_additional_workspace(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdditionalWorkspace", []))

    @jsii.member(jsii_name="resetDisabledDataSources")
    def reset_disabled_data_sources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabledDataSources", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetEventsToExport")
    def reset_events_to_export(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventsToExport", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLogAnalyticsWorkspaceId")
    def reset_log_analytics_workspace_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogAnalyticsWorkspaceId", []))

    @jsii.member(jsii_name="resetLogUnmaskedIpsEnabled")
    def reset_log_unmasked_ips_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogUnmaskedIpsEnabled", []))

    @jsii.member(jsii_name="resetQueryForResources")
    def reset_query_for_resources(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQueryForResources", []))

    @jsii.member(jsii_name="resetQuerySubscriptionIds")
    def reset_query_subscription_ids(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetQuerySubscriptionIds", []))

    @jsii.member(jsii_name="resetRecommendationsEnabled")
    def reset_recommendations_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecommendationsEnabled", []))

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
    @jsii.member(jsii_name="additionalWorkspace")
    def additional_workspace(self) -> "IotSecuritySolutionAdditionalWorkspaceList":
        return typing.cast("IotSecuritySolutionAdditionalWorkspaceList", jsii.get(self, "additionalWorkspace"))

    @builtins.property
    @jsii.member(jsii_name="recommendationsEnabled")
    def recommendations_enabled(
        self,
    ) -> "IotSecuritySolutionRecommendationsEnabledOutputReference":
        return typing.cast("IotSecuritySolutionRecommendationsEnabledOutputReference", jsii.get(self, "recommendationsEnabled"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "IotSecuritySolutionTimeoutsOutputReference":
        return typing.cast("IotSecuritySolutionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="additionalWorkspaceInput")
    def additional_workspace_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotSecuritySolutionAdditionalWorkspace"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["IotSecuritySolutionAdditionalWorkspace"]]], jsii.get(self, "additionalWorkspaceInput"))

    @builtins.property
    @jsii.member(jsii_name="disabledDataSourcesInput")
    def disabled_data_sources_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "disabledDataSourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="eventsToExportInput")
    def events_to_export_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "eventsToExportInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="iothubIdsInput")
    def iothub_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "iothubIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationInput")
    def location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "locationInput"))

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsWorkspaceIdInput")
    def log_analytics_workspace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logAnalyticsWorkspaceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="logUnmaskedIpsEnabledInput")
    def log_unmasked_ips_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "logUnmaskedIpsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="queryForResourcesInput")
    def query_for_resources_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "queryForResourcesInput"))

    @builtins.property
    @jsii.member(jsii_name="querySubscriptionIdsInput")
    def query_subscription_ids_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "querySubscriptionIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="recommendationsEnabledInput")
    def recommendations_enabled_input(
        self,
    ) -> typing.Optional["IotSecuritySolutionRecommendationsEnabled"]:
        return typing.cast(typing.Optional["IotSecuritySolutionRecommendationsEnabled"], jsii.get(self, "recommendationsEnabledInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IotSecuritySolutionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "IotSecuritySolutionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="disabledDataSources")
    def disabled_data_sources(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "disabledDataSources"))

    @disabled_data_sources.setter
    def disabled_data_sources(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45dbbd47b945ac0573bce4a1a5ce51ea00e8e58c9531ce83f95ec6e97b63d017)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabledDataSources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e373e1973e8fc221d35262b46832e2658fc86331cde9c9ff6b14293c56e855fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__a892de80615bc8d78ab1bea3a1dbb18e152e0c72d11495b2bbb2a78d47ac7a97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventsToExport")
    def events_to_export(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "eventsToExport"))

    @events_to_export.setter
    def events_to_export(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70aeb80d4b48daef2cd8e35bf6be6667db32521db8c974bf72058f4366f1e05e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventsToExport", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79205b31fa147c5bf4df2593cd2445f91db7d7caf387f3b9a54197d48d9d60b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="iothubIds")
    def iothub_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "iothubIds"))

    @iothub_ids.setter
    def iothub_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30b957e6991c52fd2cf979dbaf60638f8d7cb43b39e8bf01a4c1f3d154e996ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iothubIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @location.setter
    def location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00218b6e9a0bea8b628e6e6ba1b25ad0d2374dfa74290b67aeeb32cf65f0d0e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "location", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsWorkspaceId")
    def log_analytics_workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logAnalyticsWorkspaceId"))

    @log_analytics_workspace_id.setter
    def log_analytics_workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e24e6ef2e19430d8313da024b21844b4e088832b4c4e1a080d274cacdb8ce00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logAnalyticsWorkspaceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logUnmaskedIpsEnabled")
    def log_unmasked_ips_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "logUnmaskedIpsEnabled"))

    @log_unmasked_ips_enabled.setter
    def log_unmasked_ips_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9adba4cf4adaa3b879bb4e293c8eafad3fe95244e7142d65cbee6c0b23aead99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logUnmaskedIpsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e003e8e53e157da747da3778094cd96c8f655ad777fc02346b62a9b2e8b2018)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="queryForResources")
    def query_for_resources(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "queryForResources"))

    @query_for_resources.setter
    def query_for_resources(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cf69b7bd13463b68995c64daba222fbd1e381ee4fe17a16f7e52cd70749e05e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "queryForResources", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="querySubscriptionIds")
    def query_subscription_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "querySubscriptionIds"))

    @query_subscription_ids.setter
    def query_subscription_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4e9d2628dcf2fe55cb54a18a8013bfe96fa866db29db0a704360ee83cd5d84d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "querySubscriptionIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70f837151273cbba16f1e4ac0adc4508db2a73d9c5c8049054e119425d760a07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9ba1e860b57ff6afd87b881d97e29fb5fdbd6a1e48a8e815c7277df1c421149)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.iotSecuritySolution.IotSecuritySolutionAdditionalWorkspace",
    jsii_struct_bases=[],
    name_mapping={"data_types": "dataTypes", "workspace_id": "workspaceId"},
)
class IotSecuritySolutionAdditionalWorkspace:
    def __init__(
        self,
        *,
        data_types: typing.Sequence[builtins.str],
        workspace_id: builtins.str,
    ) -> None:
        '''
        :param data_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#data_types IotSecuritySolution#data_types}.
        :param workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#workspace_id IotSecuritySolution#workspace_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b4054912fed52c829cda404212e0f22c6810d129ec525fa77655afebec4c3ca)
            check_type(argname="argument data_types", value=data_types, expected_type=type_hints["data_types"])
            check_type(argname="argument workspace_id", value=workspace_id, expected_type=type_hints["workspace_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "data_types": data_types,
            "workspace_id": workspace_id,
        }

    @builtins.property
    def data_types(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#data_types IotSecuritySolution#data_types}.'''
        result = self._values.get("data_types")
        assert result is not None, "Required property 'data_types' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def workspace_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#workspace_id IotSecuritySolution#workspace_id}.'''
        result = self._values.get("workspace_id")
        assert result is not None, "Required property 'workspace_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotSecuritySolutionAdditionalWorkspace(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotSecuritySolutionAdditionalWorkspaceList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.iotSecuritySolution.IotSecuritySolutionAdditionalWorkspaceList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d55a669905b89d72dacc74c398b395a8c2e7ae38b9a8fbbc557fb5fa57006bba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "IotSecuritySolutionAdditionalWorkspaceOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c2b00ae2ba77c358815d575f03d42b381e1440837928e3e2ced9dca2cd753c3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("IotSecuritySolutionAdditionalWorkspaceOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51b624bfd3d1375833d717f8c5eb704e42608079f238c247f1d8d43e83906034)
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
            type_hints = typing.get_type_hints(_typecheckingstub__788bf96c49bfc79c490fe2b1e42a03d71f67b31da233e8c631910c2a30132405)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af8c62c88b16fc1899cf358ddcce928fa80bdb7a51334f2476645af2348a66a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotSecuritySolutionAdditionalWorkspace]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotSecuritySolutionAdditionalWorkspace]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotSecuritySolutionAdditionalWorkspace]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00039544e895b2f724162e1073f6d2872e1af7cfecad0f88861f5c979c09e515)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class IotSecuritySolutionAdditionalWorkspaceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.iotSecuritySolution.IotSecuritySolutionAdditionalWorkspaceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d176ef3f5bc3f597e9b6056b6f6601699c015af7ac9de095db40b0330dda123)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="dataTypesInput")
    def data_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "dataTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="workspaceIdInput")
    def workspace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "workspaceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="dataTypes")
    def data_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dataTypes"))

    @data_types.setter
    def data_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1d33be03e83e5f0ed88af48bd31abce03dab890b52ff1d3311d604e2bc262c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="workspaceId")
    def workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workspaceId"))

    @workspace_id.setter
    def workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c0e29f189783913fefb862cfcd2312cf27a1765e470f6058bedb4adeefb06b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "workspaceId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotSecuritySolutionAdditionalWorkspace]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotSecuritySolutionAdditionalWorkspace]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotSecuritySolutionAdditionalWorkspace]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62270ade7e8547a10ab72548f7462368b42d4980a12fc03c6cb6c37892d81b78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.iotSecuritySolution.IotSecuritySolutionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "display_name": "displayName",
        "iothub_ids": "iothubIds",
        "location": "location",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "additional_workspace": "additionalWorkspace",
        "disabled_data_sources": "disabledDataSources",
        "enabled": "enabled",
        "events_to_export": "eventsToExport",
        "id": "id",
        "log_analytics_workspace_id": "logAnalyticsWorkspaceId",
        "log_unmasked_ips_enabled": "logUnmaskedIpsEnabled",
        "query_for_resources": "queryForResources",
        "query_subscription_ids": "querySubscriptionIds",
        "recommendations_enabled": "recommendationsEnabled",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class IotSecuritySolutionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        display_name: builtins.str,
        iothub_ids: typing.Sequence[builtins.str],
        location: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        additional_workspace: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotSecuritySolutionAdditionalWorkspace, typing.Dict[builtins.str, typing.Any]]]]] = None,
        disabled_data_sources: typing.Optional[typing.Sequence[builtins.str]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        events_to_export: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        log_analytics_workspace_id: typing.Optional[builtins.str] = None,
        log_unmasked_ips_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        query_for_resources: typing.Optional[builtins.str] = None,
        query_subscription_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        recommendations_enabled: typing.Optional[typing.Union["IotSecuritySolutionRecommendationsEnabled", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["IotSecuritySolutionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#display_name IotSecuritySolution#display_name}.
        :param iothub_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#iothub_ids IotSecuritySolution#iothub_ids}.
        :param location: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#location IotSecuritySolution#location}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#name IotSecuritySolution#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#resource_group_name IotSecuritySolution#resource_group_name}.
        :param additional_workspace: additional_workspace block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#additional_workspace IotSecuritySolution#additional_workspace}
        :param disabled_data_sources: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#disabled_data_sources IotSecuritySolution#disabled_data_sources}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#enabled IotSecuritySolution#enabled}.
        :param events_to_export: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#events_to_export IotSecuritySolution#events_to_export}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#id IotSecuritySolution#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#log_analytics_workspace_id IotSecuritySolution#log_analytics_workspace_id}.
        :param log_unmasked_ips_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#log_unmasked_ips_enabled IotSecuritySolution#log_unmasked_ips_enabled}.
        :param query_for_resources: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#query_for_resources IotSecuritySolution#query_for_resources}.
        :param query_subscription_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#query_subscription_ids IotSecuritySolution#query_subscription_ids}.
        :param recommendations_enabled: recommendations_enabled block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#recommendations_enabled IotSecuritySolution#recommendations_enabled}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#tags IotSecuritySolution#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#timeouts IotSecuritySolution#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(recommendations_enabled, dict):
            recommendations_enabled = IotSecuritySolutionRecommendationsEnabled(**recommendations_enabled)
        if isinstance(timeouts, dict):
            timeouts = IotSecuritySolutionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d9a67a81694b14289fd471c31ab28175c28d74e6ca9a038f06a8b2c99db6ef8)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument iothub_ids", value=iothub_ids, expected_type=type_hints["iothub_ids"])
            check_type(argname="argument location", value=location, expected_type=type_hints["location"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument additional_workspace", value=additional_workspace, expected_type=type_hints["additional_workspace"])
            check_type(argname="argument disabled_data_sources", value=disabled_data_sources, expected_type=type_hints["disabled_data_sources"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument events_to_export", value=events_to_export, expected_type=type_hints["events_to_export"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument log_analytics_workspace_id", value=log_analytics_workspace_id, expected_type=type_hints["log_analytics_workspace_id"])
            check_type(argname="argument log_unmasked_ips_enabled", value=log_unmasked_ips_enabled, expected_type=type_hints["log_unmasked_ips_enabled"])
            check_type(argname="argument query_for_resources", value=query_for_resources, expected_type=type_hints["query_for_resources"])
            check_type(argname="argument query_subscription_ids", value=query_subscription_ids, expected_type=type_hints["query_subscription_ids"])
            check_type(argname="argument recommendations_enabled", value=recommendations_enabled, expected_type=type_hints["recommendations_enabled"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
            "iothub_ids": iothub_ids,
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
        if additional_workspace is not None:
            self._values["additional_workspace"] = additional_workspace
        if disabled_data_sources is not None:
            self._values["disabled_data_sources"] = disabled_data_sources
        if enabled is not None:
            self._values["enabled"] = enabled
        if events_to_export is not None:
            self._values["events_to_export"] = events_to_export
        if id is not None:
            self._values["id"] = id
        if log_analytics_workspace_id is not None:
            self._values["log_analytics_workspace_id"] = log_analytics_workspace_id
        if log_unmasked_ips_enabled is not None:
            self._values["log_unmasked_ips_enabled"] = log_unmasked_ips_enabled
        if query_for_resources is not None:
            self._values["query_for_resources"] = query_for_resources
        if query_subscription_ids is not None:
            self._values["query_subscription_ids"] = query_subscription_ids
        if recommendations_enabled is not None:
            self._values["recommendations_enabled"] = recommendations_enabled
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
    def display_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#display_name IotSecuritySolution#display_name}.'''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def iothub_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#iothub_ids IotSecuritySolution#iothub_ids}.'''
        result = self._values.get("iothub_ids")
        assert result is not None, "Required property 'iothub_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def location(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#location IotSecuritySolution#location}.'''
        result = self._values.get("location")
        assert result is not None, "Required property 'location' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#name IotSecuritySolution#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#resource_group_name IotSecuritySolution#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def additional_workspace(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotSecuritySolutionAdditionalWorkspace]]]:
        '''additional_workspace block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#additional_workspace IotSecuritySolution#additional_workspace}
        '''
        result = self._values.get("additional_workspace")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotSecuritySolutionAdditionalWorkspace]]], result)

    @builtins.property
    def disabled_data_sources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#disabled_data_sources IotSecuritySolution#disabled_data_sources}.'''
        result = self._values.get("disabled_data_sources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#enabled IotSecuritySolution#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def events_to_export(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#events_to_export IotSecuritySolution#events_to_export}.'''
        result = self._values.get("events_to_export")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#id IotSecuritySolution#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_analytics_workspace_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#log_analytics_workspace_id IotSecuritySolution#log_analytics_workspace_id}.'''
        result = self._values.get("log_analytics_workspace_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_unmasked_ips_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#log_unmasked_ips_enabled IotSecuritySolution#log_unmasked_ips_enabled}.'''
        result = self._values.get("log_unmasked_ips_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def query_for_resources(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#query_for_resources IotSecuritySolution#query_for_resources}.'''
        result = self._values.get("query_for_resources")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def query_subscription_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#query_subscription_ids IotSecuritySolution#query_subscription_ids}.'''
        result = self._values.get("query_subscription_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def recommendations_enabled(
        self,
    ) -> typing.Optional["IotSecuritySolutionRecommendationsEnabled"]:
        '''recommendations_enabled block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#recommendations_enabled IotSecuritySolution#recommendations_enabled}
        '''
        result = self._values.get("recommendations_enabled")
        return typing.cast(typing.Optional["IotSecuritySolutionRecommendationsEnabled"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#tags IotSecuritySolution#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["IotSecuritySolutionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#timeouts IotSecuritySolution#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["IotSecuritySolutionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotSecuritySolutionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.iotSecuritySolution.IotSecuritySolutionRecommendationsEnabled",
    jsii_struct_bases=[],
    name_mapping={
        "acr_authentication": "acrAuthentication",
        "agent_send_unutilized_msg": "agentSendUnutilizedMsg",
        "baseline": "baseline",
        "edge_hub_mem_optimize": "edgeHubMemOptimize",
        "edge_logging_option": "edgeLoggingOption",
        "inconsistent_module_settings": "inconsistentModuleSettings",
        "install_agent": "installAgent",
        "ip_filter_deny_all": "ipFilterDenyAll",
        "ip_filter_permissive_rule": "ipFilterPermissiveRule",
        "open_ports": "openPorts",
        "permissive_firewall_policy": "permissiveFirewallPolicy",
        "permissive_input_firewall_rules": "permissiveInputFirewallRules",
        "permissive_output_firewall_rules": "permissiveOutputFirewallRules",
        "privileged_docker_options": "privilegedDockerOptions",
        "shared_credentials": "sharedCredentials",
        "vulnerable_tls_cipher_suite": "vulnerableTlsCipherSuite",
    },
)
class IotSecuritySolutionRecommendationsEnabled:
    def __init__(
        self,
        *,
        acr_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        agent_send_unutilized_msg: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        baseline: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        edge_hub_mem_optimize: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        edge_logging_option: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        inconsistent_module_settings: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        install_agent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ip_filter_deny_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ip_filter_permissive_rule: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        open_ports: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        permissive_firewall_policy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        permissive_input_firewall_rules: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        permissive_output_firewall_rules: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        privileged_docker_options: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        shared_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        vulnerable_tls_cipher_suite: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param acr_authentication: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#acr_authentication IotSecuritySolution#acr_authentication}.
        :param agent_send_unutilized_msg: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#agent_send_unutilized_msg IotSecuritySolution#agent_send_unutilized_msg}.
        :param baseline: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#baseline IotSecuritySolution#baseline}.
        :param edge_hub_mem_optimize: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#edge_hub_mem_optimize IotSecuritySolution#edge_hub_mem_optimize}.
        :param edge_logging_option: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#edge_logging_option IotSecuritySolution#edge_logging_option}.
        :param inconsistent_module_settings: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#inconsistent_module_settings IotSecuritySolution#inconsistent_module_settings}.
        :param install_agent: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#install_agent IotSecuritySolution#install_agent}.
        :param ip_filter_deny_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#ip_filter_deny_all IotSecuritySolution#ip_filter_deny_all}.
        :param ip_filter_permissive_rule: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#ip_filter_permissive_rule IotSecuritySolution#ip_filter_permissive_rule}.
        :param open_ports: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#open_ports IotSecuritySolution#open_ports}.
        :param permissive_firewall_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#permissive_firewall_policy IotSecuritySolution#permissive_firewall_policy}.
        :param permissive_input_firewall_rules: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#permissive_input_firewall_rules IotSecuritySolution#permissive_input_firewall_rules}.
        :param permissive_output_firewall_rules: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#permissive_output_firewall_rules IotSecuritySolution#permissive_output_firewall_rules}.
        :param privileged_docker_options: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#privileged_docker_options IotSecuritySolution#privileged_docker_options}.
        :param shared_credentials: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#shared_credentials IotSecuritySolution#shared_credentials}.
        :param vulnerable_tls_cipher_suite: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#vulnerable_tls_cipher_suite IotSecuritySolution#vulnerable_tls_cipher_suite}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__224b7f22ddf111ebf7749fd8a911347ae3aa78875ae5c2b9242701aa2607d0a7)
            check_type(argname="argument acr_authentication", value=acr_authentication, expected_type=type_hints["acr_authentication"])
            check_type(argname="argument agent_send_unutilized_msg", value=agent_send_unutilized_msg, expected_type=type_hints["agent_send_unutilized_msg"])
            check_type(argname="argument baseline", value=baseline, expected_type=type_hints["baseline"])
            check_type(argname="argument edge_hub_mem_optimize", value=edge_hub_mem_optimize, expected_type=type_hints["edge_hub_mem_optimize"])
            check_type(argname="argument edge_logging_option", value=edge_logging_option, expected_type=type_hints["edge_logging_option"])
            check_type(argname="argument inconsistent_module_settings", value=inconsistent_module_settings, expected_type=type_hints["inconsistent_module_settings"])
            check_type(argname="argument install_agent", value=install_agent, expected_type=type_hints["install_agent"])
            check_type(argname="argument ip_filter_deny_all", value=ip_filter_deny_all, expected_type=type_hints["ip_filter_deny_all"])
            check_type(argname="argument ip_filter_permissive_rule", value=ip_filter_permissive_rule, expected_type=type_hints["ip_filter_permissive_rule"])
            check_type(argname="argument open_ports", value=open_ports, expected_type=type_hints["open_ports"])
            check_type(argname="argument permissive_firewall_policy", value=permissive_firewall_policy, expected_type=type_hints["permissive_firewall_policy"])
            check_type(argname="argument permissive_input_firewall_rules", value=permissive_input_firewall_rules, expected_type=type_hints["permissive_input_firewall_rules"])
            check_type(argname="argument permissive_output_firewall_rules", value=permissive_output_firewall_rules, expected_type=type_hints["permissive_output_firewall_rules"])
            check_type(argname="argument privileged_docker_options", value=privileged_docker_options, expected_type=type_hints["privileged_docker_options"])
            check_type(argname="argument shared_credentials", value=shared_credentials, expected_type=type_hints["shared_credentials"])
            check_type(argname="argument vulnerable_tls_cipher_suite", value=vulnerable_tls_cipher_suite, expected_type=type_hints["vulnerable_tls_cipher_suite"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if acr_authentication is not None:
            self._values["acr_authentication"] = acr_authentication
        if agent_send_unutilized_msg is not None:
            self._values["agent_send_unutilized_msg"] = agent_send_unutilized_msg
        if baseline is not None:
            self._values["baseline"] = baseline
        if edge_hub_mem_optimize is not None:
            self._values["edge_hub_mem_optimize"] = edge_hub_mem_optimize
        if edge_logging_option is not None:
            self._values["edge_logging_option"] = edge_logging_option
        if inconsistent_module_settings is not None:
            self._values["inconsistent_module_settings"] = inconsistent_module_settings
        if install_agent is not None:
            self._values["install_agent"] = install_agent
        if ip_filter_deny_all is not None:
            self._values["ip_filter_deny_all"] = ip_filter_deny_all
        if ip_filter_permissive_rule is not None:
            self._values["ip_filter_permissive_rule"] = ip_filter_permissive_rule
        if open_ports is not None:
            self._values["open_ports"] = open_ports
        if permissive_firewall_policy is not None:
            self._values["permissive_firewall_policy"] = permissive_firewall_policy
        if permissive_input_firewall_rules is not None:
            self._values["permissive_input_firewall_rules"] = permissive_input_firewall_rules
        if permissive_output_firewall_rules is not None:
            self._values["permissive_output_firewall_rules"] = permissive_output_firewall_rules
        if privileged_docker_options is not None:
            self._values["privileged_docker_options"] = privileged_docker_options
        if shared_credentials is not None:
            self._values["shared_credentials"] = shared_credentials
        if vulnerable_tls_cipher_suite is not None:
            self._values["vulnerable_tls_cipher_suite"] = vulnerable_tls_cipher_suite

    @builtins.property
    def acr_authentication(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#acr_authentication IotSecuritySolution#acr_authentication}.'''
        result = self._values.get("acr_authentication")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def agent_send_unutilized_msg(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#agent_send_unutilized_msg IotSecuritySolution#agent_send_unutilized_msg}.'''
        result = self._values.get("agent_send_unutilized_msg")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def baseline(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#baseline IotSecuritySolution#baseline}.'''
        result = self._values.get("baseline")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def edge_hub_mem_optimize(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#edge_hub_mem_optimize IotSecuritySolution#edge_hub_mem_optimize}.'''
        result = self._values.get("edge_hub_mem_optimize")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def edge_logging_option(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#edge_logging_option IotSecuritySolution#edge_logging_option}.'''
        result = self._values.get("edge_logging_option")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def inconsistent_module_settings(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#inconsistent_module_settings IotSecuritySolution#inconsistent_module_settings}.'''
        result = self._values.get("inconsistent_module_settings")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def install_agent(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#install_agent IotSecuritySolution#install_agent}.'''
        result = self._values.get("install_agent")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ip_filter_deny_all(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#ip_filter_deny_all IotSecuritySolution#ip_filter_deny_all}.'''
        result = self._values.get("ip_filter_deny_all")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ip_filter_permissive_rule(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#ip_filter_permissive_rule IotSecuritySolution#ip_filter_permissive_rule}.'''
        result = self._values.get("ip_filter_permissive_rule")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def open_ports(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#open_ports IotSecuritySolution#open_ports}.'''
        result = self._values.get("open_ports")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def permissive_firewall_policy(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#permissive_firewall_policy IotSecuritySolution#permissive_firewall_policy}.'''
        result = self._values.get("permissive_firewall_policy")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def permissive_input_firewall_rules(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#permissive_input_firewall_rules IotSecuritySolution#permissive_input_firewall_rules}.'''
        result = self._values.get("permissive_input_firewall_rules")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def permissive_output_firewall_rules(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#permissive_output_firewall_rules IotSecuritySolution#permissive_output_firewall_rules}.'''
        result = self._values.get("permissive_output_firewall_rules")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def privileged_docker_options(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#privileged_docker_options IotSecuritySolution#privileged_docker_options}.'''
        result = self._values.get("privileged_docker_options")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def shared_credentials(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#shared_credentials IotSecuritySolution#shared_credentials}.'''
        result = self._values.get("shared_credentials")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def vulnerable_tls_cipher_suite(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#vulnerable_tls_cipher_suite IotSecuritySolution#vulnerable_tls_cipher_suite}.'''
        result = self._values.get("vulnerable_tls_cipher_suite")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotSecuritySolutionRecommendationsEnabled(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotSecuritySolutionRecommendationsEnabledOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.iotSecuritySolution.IotSecuritySolutionRecommendationsEnabledOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d46378d0102d44fbdfe7687f4214d44648ceaedca17a027c350fa72d4e851c7d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetAcrAuthentication")
    def reset_acr_authentication(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAcrAuthentication", []))

    @jsii.member(jsii_name="resetAgentSendUnutilizedMsg")
    def reset_agent_send_unutilized_msg(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAgentSendUnutilizedMsg", []))

    @jsii.member(jsii_name="resetBaseline")
    def reset_baseline(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBaseline", []))

    @jsii.member(jsii_name="resetEdgeHubMemOptimize")
    def reset_edge_hub_mem_optimize(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEdgeHubMemOptimize", []))

    @jsii.member(jsii_name="resetEdgeLoggingOption")
    def reset_edge_logging_option(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEdgeLoggingOption", []))

    @jsii.member(jsii_name="resetInconsistentModuleSettings")
    def reset_inconsistent_module_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInconsistentModuleSettings", []))

    @jsii.member(jsii_name="resetInstallAgent")
    def reset_install_agent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInstallAgent", []))

    @jsii.member(jsii_name="resetIpFilterDenyAll")
    def reset_ip_filter_deny_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpFilterDenyAll", []))

    @jsii.member(jsii_name="resetIpFilterPermissiveRule")
    def reset_ip_filter_permissive_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpFilterPermissiveRule", []))

    @jsii.member(jsii_name="resetOpenPorts")
    def reset_open_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOpenPorts", []))

    @jsii.member(jsii_name="resetPermissiveFirewallPolicy")
    def reset_permissive_firewall_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermissiveFirewallPolicy", []))

    @jsii.member(jsii_name="resetPermissiveInputFirewallRules")
    def reset_permissive_input_firewall_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermissiveInputFirewallRules", []))

    @jsii.member(jsii_name="resetPermissiveOutputFirewallRules")
    def reset_permissive_output_firewall_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPermissiveOutputFirewallRules", []))

    @jsii.member(jsii_name="resetPrivilegedDockerOptions")
    def reset_privileged_docker_options(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrivilegedDockerOptions", []))

    @jsii.member(jsii_name="resetSharedCredentials")
    def reset_shared_credentials(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSharedCredentials", []))

    @jsii.member(jsii_name="resetVulnerableTlsCipherSuite")
    def reset_vulnerable_tls_cipher_suite(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVulnerableTlsCipherSuite", []))

    @builtins.property
    @jsii.member(jsii_name="acrAuthenticationInput")
    def acr_authentication_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "acrAuthenticationInput"))

    @builtins.property
    @jsii.member(jsii_name="agentSendUnutilizedMsgInput")
    def agent_send_unutilized_msg_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "agentSendUnutilizedMsgInput"))

    @builtins.property
    @jsii.member(jsii_name="baselineInput")
    def baseline_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "baselineInput"))

    @builtins.property
    @jsii.member(jsii_name="edgeHubMemOptimizeInput")
    def edge_hub_mem_optimize_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "edgeHubMemOptimizeInput"))

    @builtins.property
    @jsii.member(jsii_name="edgeLoggingOptionInput")
    def edge_logging_option_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "edgeLoggingOptionInput"))

    @builtins.property
    @jsii.member(jsii_name="inconsistentModuleSettingsInput")
    def inconsistent_module_settings_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "inconsistentModuleSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="installAgentInput")
    def install_agent_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "installAgentInput"))

    @builtins.property
    @jsii.member(jsii_name="ipFilterDenyAllInput")
    def ip_filter_deny_all_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ipFilterDenyAllInput"))

    @builtins.property
    @jsii.member(jsii_name="ipFilterPermissiveRuleInput")
    def ip_filter_permissive_rule_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ipFilterPermissiveRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="openPortsInput")
    def open_ports_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "openPortsInput"))

    @builtins.property
    @jsii.member(jsii_name="permissiveFirewallPolicyInput")
    def permissive_firewall_policy_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "permissiveFirewallPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="permissiveInputFirewallRulesInput")
    def permissive_input_firewall_rules_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "permissiveInputFirewallRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="permissiveOutputFirewallRulesInput")
    def permissive_output_firewall_rules_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "permissiveOutputFirewallRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="privilegedDockerOptionsInput")
    def privileged_docker_options_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "privilegedDockerOptionsInput"))

    @builtins.property
    @jsii.member(jsii_name="sharedCredentialsInput")
    def shared_credentials_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sharedCredentialsInput"))

    @builtins.property
    @jsii.member(jsii_name="vulnerableTlsCipherSuiteInput")
    def vulnerable_tls_cipher_suite_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "vulnerableTlsCipherSuiteInput"))

    @builtins.property
    @jsii.member(jsii_name="acrAuthentication")
    def acr_authentication(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "acrAuthentication"))

    @acr_authentication.setter
    def acr_authentication(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21dce07427d0b46a19cf64284edd6e5361e06976f5139706103486cb2da62f75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "acrAuthentication", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="agentSendUnutilizedMsg")
    def agent_send_unutilized_msg(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "agentSendUnutilizedMsg"))

    @agent_send_unutilized_msg.setter
    def agent_send_unutilized_msg(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37a6399cb390e9036c721abd4dafc25b58c6f5376b03010bf376722aaeff7cf3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentSendUnutilizedMsg", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="baseline")
    def baseline(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "baseline"))

    @baseline.setter
    def baseline(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3d01d5d12e2f93bf3cdf7f64780c6f900c3ea4275aead3c6bfadde240eed623)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "baseline", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="edgeHubMemOptimize")
    def edge_hub_mem_optimize(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "edgeHubMemOptimize"))

    @edge_hub_mem_optimize.setter
    def edge_hub_mem_optimize(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7127f897c871babe59c17450396dc657f4cdb83f10fe0ededfe16844cfec6c20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edgeHubMemOptimize", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="edgeLoggingOption")
    def edge_logging_option(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "edgeLoggingOption"))

    @edge_logging_option.setter
    def edge_logging_option(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c8fda17269efdb0deecc7c5d80fb8024cf5781696ae6b8a7d988b2976a4037c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "edgeLoggingOption", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inconsistentModuleSettings")
    def inconsistent_module_settings(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "inconsistentModuleSettings"))

    @inconsistent_module_settings.setter
    def inconsistent_module_settings(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80b94cfbeb978b41bc730b9d0c1f8d6595e309aa50c953516222fea445ae58d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inconsistentModuleSettings", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="installAgent")
    def install_agent(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "installAgent"))

    @install_agent.setter
    def install_agent(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77d99a0a95365da9dffc6a84201407d9fc69c1e45fbaf40ca78f38fe852655c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "installAgent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipFilterDenyAll")
    def ip_filter_deny_all(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ipFilterDenyAll"))

    @ip_filter_deny_all.setter
    def ip_filter_deny_all(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98b50ea0179b2f721e40aa37390030e3a2248c4776c9a065134b38f37022f91b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipFilterDenyAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ipFilterPermissiveRule")
    def ip_filter_permissive_rule(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ipFilterPermissiveRule"))

    @ip_filter_permissive_rule.setter
    def ip_filter_permissive_rule(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1757526cfec0232bc797390c8980d2c384489a71f18ab240cad69dda573d413f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipFilterPermissiveRule", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="openPorts")
    def open_ports(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "openPorts"))

    @open_ports.setter
    def open_ports(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__090f8b470579b843c0ed1614d7f21786d21391f501cb3aab7b9c9e093d7a873a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "openPorts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permissiveFirewallPolicy")
    def permissive_firewall_policy(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "permissiveFirewallPolicy"))

    @permissive_firewall_policy.setter
    def permissive_firewall_policy(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__942a97453ad1317d799e163b85f542f15962c27ea951a023bceb1acd3b5b69bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissiveFirewallPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permissiveInputFirewallRules")
    def permissive_input_firewall_rules(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "permissiveInputFirewallRules"))

    @permissive_input_firewall_rules.setter
    def permissive_input_firewall_rules(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__859608f55a17ce1408a0e173ddc2a916d92bdac2920dfc97231468944333fe7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissiveInputFirewallRules", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="permissiveOutputFirewallRules")
    def permissive_output_firewall_rules(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "permissiveOutputFirewallRules"))

    @permissive_output_firewall_rules.setter
    def permissive_output_firewall_rules(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__513fb50dd09d98f96129e8aad918ac16b16fdf45f024a72b5f82f2ed28227cba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissiveOutputFirewallRules", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="privilegedDockerOptions")
    def privileged_docker_options(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "privilegedDockerOptions"))

    @privileged_docker_options.setter
    def privileged_docker_options(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf424cbc565132590553e9a005fc5a94309ef226e04ef4b860b1f4b9e68ef023)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privilegedDockerOptions", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sharedCredentials")
    def shared_credentials(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sharedCredentials"))

    @shared_credentials.setter
    def shared_credentials(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64eefdb05d727acee1edb2ac2d049c6c82ffa4af36777fbdcfeed120be6eb489)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sharedCredentials", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="vulnerableTlsCipherSuite")
    def vulnerable_tls_cipher_suite(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "vulnerableTlsCipherSuite"))

    @vulnerable_tls_cipher_suite.setter
    def vulnerable_tls_cipher_suite(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c6c496576240e6737a25ff379fbb7f5c30df169f22e35d348cb43af48170a53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vulnerableTlsCipherSuite", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[IotSecuritySolutionRecommendationsEnabled]:
        return typing.cast(typing.Optional[IotSecuritySolutionRecommendationsEnabled], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[IotSecuritySolutionRecommendationsEnabled],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3960bb652a5f716ec320db02ebfefc03b7f552739055dc86896203298c36ddd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.iotSecuritySolution.IotSecuritySolutionTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class IotSecuritySolutionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#create IotSecuritySolution#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#delete IotSecuritySolution#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#read IotSecuritySolution#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#update IotSecuritySolution#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3ae64e8141313375f8b39de2398152667858b500c585c9ba58649185d9056b2)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#create IotSecuritySolution#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#delete IotSecuritySolution#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#read IotSecuritySolution#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/iot_security_solution#update IotSecuritySolution#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IotSecuritySolutionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IotSecuritySolutionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.iotSecuritySolution.IotSecuritySolutionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d053ad152ee4b36592eecc0256cfc984ac77597483289693b112441fdd5909bf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5812fd6ea632aa675d33628a5a6147d6898baee92e8ff0b37af8aa17f08d7140)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a3f109b2ea5062d8cd78136de991b0fad1cacd245d98afac0d881d018f2a826)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__662805b2342150357b161231bba9fbdb562017c8e8bcd54ead9d4f438044f8dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fb883e182c29695d8f0b16700e5719b33d3e2d93596f976f81911bb9a4d86f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotSecuritySolutionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotSecuritySolutionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotSecuritySolutionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23681a5943ecfea7a0c391024a1a674f56a9252d4231e5bef93819c6b9dcb9ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "IotSecuritySolution",
    "IotSecuritySolutionAdditionalWorkspace",
    "IotSecuritySolutionAdditionalWorkspaceList",
    "IotSecuritySolutionAdditionalWorkspaceOutputReference",
    "IotSecuritySolutionConfig",
    "IotSecuritySolutionRecommendationsEnabled",
    "IotSecuritySolutionRecommendationsEnabledOutputReference",
    "IotSecuritySolutionTimeouts",
    "IotSecuritySolutionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__976f32ea276c518cd31e488a6a6b611a0e2dfeb44c89eba63aa3b65792b77453(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    iothub_ids: typing.Sequence[builtins.str],
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    additional_workspace: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotSecuritySolutionAdditionalWorkspace, typing.Dict[builtins.str, typing.Any]]]]] = None,
    disabled_data_sources: typing.Optional[typing.Sequence[builtins.str]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    events_to_export: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    log_analytics_workspace_id: typing.Optional[builtins.str] = None,
    log_unmasked_ips_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    query_for_resources: typing.Optional[builtins.str] = None,
    query_subscription_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    recommendations_enabled: typing.Optional[typing.Union[IotSecuritySolutionRecommendationsEnabled, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[IotSecuritySolutionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__e20eaaaa368dc72a7f4673e35e3558bdb5d876b39776dd7b79902b6ff13c0580(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__707b0e31b5eca676a55708b524d645ef965b8bd07ad3e0558aba552ad8d531ab(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotSecuritySolutionAdditionalWorkspace, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45dbbd47b945ac0573bce4a1a5ce51ea00e8e58c9531ce83f95ec6e97b63d017(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e373e1973e8fc221d35262b46832e2658fc86331cde9c9ff6b14293c56e855fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a892de80615bc8d78ab1bea3a1dbb18e152e0c72d11495b2bbb2a78d47ac7a97(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70aeb80d4b48daef2cd8e35bf6be6667db32521db8c974bf72058f4366f1e05e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79205b31fa147c5bf4df2593cd2445f91db7d7caf387f3b9a54197d48d9d60b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30b957e6991c52fd2cf979dbaf60638f8d7cb43b39e8bf01a4c1f3d154e996ca(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00218b6e9a0bea8b628e6e6ba1b25ad0d2374dfa74290b67aeeb32cf65f0d0e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e24e6ef2e19430d8313da024b21844b4e088832b4c4e1a080d274cacdb8ce00(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9adba4cf4adaa3b879bb4e293c8eafad3fe95244e7142d65cbee6c0b23aead99(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e003e8e53e157da747da3778094cd96c8f655ad777fc02346b62a9b2e8b2018(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf69b7bd13463b68995c64daba222fbd1e381ee4fe17a16f7e52cd70749e05e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4e9d2628dcf2fe55cb54a18a8013bfe96fa866db29db0a704360ee83cd5d84d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70f837151273cbba16f1e4ac0adc4508db2a73d9c5c8049054e119425d760a07(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9ba1e860b57ff6afd87b881d97e29fb5fdbd6a1e48a8e815c7277df1c421149(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b4054912fed52c829cda404212e0f22c6810d129ec525fa77655afebec4c3ca(
    *,
    data_types: typing.Sequence[builtins.str],
    workspace_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d55a669905b89d72dacc74c398b395a8c2e7ae38b9a8fbbc557fb5fa57006bba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c2b00ae2ba77c358815d575f03d42b381e1440837928e3e2ced9dca2cd753c3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51b624bfd3d1375833d717f8c5eb704e42608079f238c247f1d8d43e83906034(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__788bf96c49bfc79c490fe2b1e42a03d71f67b31da233e8c631910c2a30132405(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af8c62c88b16fc1899cf358ddcce928fa80bdb7a51334f2476645af2348a66a8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00039544e895b2f724162e1073f6d2872e1af7cfecad0f88861f5c979c09e515(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[IotSecuritySolutionAdditionalWorkspace]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d176ef3f5bc3f597e9b6056b6f6601699c015af7ac9de095db40b0330dda123(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1d33be03e83e5f0ed88af48bd31abce03dab890b52ff1d3311d604e2bc262c6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c0e29f189783913fefb862cfcd2312cf27a1765e470f6058bedb4adeefb06b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62270ade7e8547a10ab72548f7462368b42d4980a12fc03c6cb6c37892d81b78(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotSecuritySolutionAdditionalWorkspace]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d9a67a81694b14289fd471c31ab28175c28d74e6ca9a038f06a8b2c99db6ef8(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: builtins.str,
    iothub_ids: typing.Sequence[builtins.str],
    location: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    additional_workspace: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[IotSecuritySolutionAdditionalWorkspace, typing.Dict[builtins.str, typing.Any]]]]] = None,
    disabled_data_sources: typing.Optional[typing.Sequence[builtins.str]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    events_to_export: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    log_analytics_workspace_id: typing.Optional[builtins.str] = None,
    log_unmasked_ips_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    query_for_resources: typing.Optional[builtins.str] = None,
    query_subscription_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    recommendations_enabled: typing.Optional[typing.Union[IotSecuritySolutionRecommendationsEnabled, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[IotSecuritySolutionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__224b7f22ddf111ebf7749fd8a911347ae3aa78875ae5c2b9242701aa2607d0a7(
    *,
    acr_authentication: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    agent_send_unutilized_msg: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    baseline: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    edge_hub_mem_optimize: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    edge_logging_option: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    inconsistent_module_settings: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    install_agent: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ip_filter_deny_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ip_filter_permissive_rule: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    open_ports: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    permissive_firewall_policy: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    permissive_input_firewall_rules: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    permissive_output_firewall_rules: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    privileged_docker_options: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    shared_credentials: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    vulnerable_tls_cipher_suite: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d46378d0102d44fbdfe7687f4214d44648ceaedca17a027c350fa72d4e851c7d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21dce07427d0b46a19cf64284edd6e5361e06976f5139706103486cb2da62f75(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37a6399cb390e9036c721abd4dafc25b58c6f5376b03010bf376722aaeff7cf3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3d01d5d12e2f93bf3cdf7f64780c6f900c3ea4275aead3c6bfadde240eed623(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7127f897c871babe59c17450396dc657f4cdb83f10fe0ededfe16844cfec6c20(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c8fda17269efdb0deecc7c5d80fb8024cf5781696ae6b8a7d988b2976a4037c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80b94cfbeb978b41bc730b9d0c1f8d6595e309aa50c953516222fea445ae58d7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77d99a0a95365da9dffc6a84201407d9fc69c1e45fbaf40ca78f38fe852655c7(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98b50ea0179b2f721e40aa37390030e3a2248c4776c9a065134b38f37022f91b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1757526cfec0232bc797390c8980d2c384489a71f18ab240cad69dda573d413f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__090f8b470579b843c0ed1614d7f21786d21391f501cb3aab7b9c9e093d7a873a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__942a97453ad1317d799e163b85f542f15962c27ea951a023bceb1acd3b5b69bb(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__859608f55a17ce1408a0e173ddc2a916d92bdac2920dfc97231468944333fe7b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__513fb50dd09d98f96129e8aad918ac16b16fdf45f024a72b5f82f2ed28227cba(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf424cbc565132590553e9a005fc5a94309ef226e04ef4b860b1f4b9e68ef023(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64eefdb05d727acee1edb2ac2d049c6c82ffa4af36777fbdcfeed120be6eb489(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c6c496576240e6737a25ff379fbb7f5c30df169f22e35d348cb43af48170a53(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3960bb652a5f716ec320db02ebfefc03b7f552739055dc86896203298c36ddd4(
    value: typing.Optional[IotSecuritySolutionRecommendationsEnabled],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3ae64e8141313375f8b39de2398152667858b500c585c9ba58649185d9056b2(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d053ad152ee4b36592eecc0256cfc984ac77597483289693b112441fdd5909bf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5812fd6ea632aa675d33628a5a6147d6898baee92e8ff0b37af8aa17f08d7140(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a3f109b2ea5062d8cd78136de991b0fad1cacd245d98afac0d881d018f2a826(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__662805b2342150357b161231bba9fbdb562017c8e8bcd54ead9d4f438044f8dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fb883e182c29695d8f0b16700e5719b33d3e2d93596f976f81911bb9a4d86f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23681a5943ecfea7a0c391024a1a674f56a9252d4231e5bef93819c6b9dcb9ab(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, IotSecuritySolutionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
