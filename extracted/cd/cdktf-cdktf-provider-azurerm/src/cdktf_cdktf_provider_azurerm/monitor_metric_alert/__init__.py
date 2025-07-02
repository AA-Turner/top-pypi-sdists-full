r'''
# `azurerm_monitor_metric_alert`

Refer to the Terraform Registry for docs: [`azurerm_monitor_metric_alert`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert).
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


class MonitorMetricAlert(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorMetricAlert.MonitorMetricAlert",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert azurerm_monitor_metric_alert}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        resource_group_name: builtins.str,
        scopes: typing.Sequence[builtins.str],
        action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorMetricAlertAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        application_insights_web_test_location_availability_criteria: typing.Optional[typing.Union["MonitorMetricAlertApplicationInsightsWebTestLocationAvailabilityCriteria", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_mitigate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        criteria: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorMetricAlertCriteria", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        dynamic_criteria: typing.Optional[typing.Union["MonitorMetricAlertDynamicCriteria", typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        frequency: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        severity: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        target_resource_location: typing.Optional[builtins.str] = None,
        target_resource_type: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["MonitorMetricAlertTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        window_size: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert azurerm_monitor_metric_alert} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#name MonitorMetricAlert#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#resource_group_name MonitorMetricAlert#resource_group_name}.
        :param scopes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#scopes MonitorMetricAlert#scopes}.
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#action MonitorMetricAlert#action}
        :param application_insights_web_test_location_availability_criteria: application_insights_web_test_location_availability_criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#application_insights_web_test_location_availability_criteria MonitorMetricAlert#application_insights_web_test_location_availability_criteria}
        :param auto_mitigate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#auto_mitigate MonitorMetricAlert#auto_mitigate}.
        :param criteria: criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#criteria MonitorMetricAlert#criteria}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#description MonitorMetricAlert#description}.
        :param dynamic_criteria: dynamic_criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#dynamic_criteria MonitorMetricAlert#dynamic_criteria}
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#enabled MonitorMetricAlert#enabled}.
        :param frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#frequency MonitorMetricAlert#frequency}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#id MonitorMetricAlert#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param severity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#severity MonitorMetricAlert#severity}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#tags MonitorMetricAlert#tags}.
        :param target_resource_location: The location of the target pluginsdk. Required when using subscription, resource group scope or multiple scopes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#target_resource_location MonitorMetricAlert#target_resource_location}
        :param target_resource_type: The resource type (e.g. Microsoft.Compute/virtualMachines) of the target pluginsdk. Required when using subscription, resource group scope or multiple scopes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#target_resource_type MonitorMetricAlert#target_resource_type}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#timeouts MonitorMetricAlert#timeouts}
        :param window_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#window_size MonitorMetricAlert#window_size}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a064176265b0567dbf284cff915827b4357ccb233fe03d1a2b8d225b14cfea7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MonitorMetricAlertConfig(
            name=name,
            resource_group_name=resource_group_name,
            scopes=scopes,
            action=action,
            application_insights_web_test_location_availability_criteria=application_insights_web_test_location_availability_criteria,
            auto_mitigate=auto_mitigate,
            criteria=criteria,
            description=description,
            dynamic_criteria=dynamic_criteria,
            enabled=enabled,
            frequency=frequency,
            id=id,
            severity=severity,
            tags=tags,
            target_resource_location=target_resource_location,
            target_resource_type=target_resource_type,
            timeouts=timeouts,
            window_size=window_size,
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
        '''Generates CDKTF code for importing a MonitorMetricAlert resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MonitorMetricAlert to import.
        :param import_from_id: The id of the existing MonitorMetricAlert that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MonitorMetricAlert to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14e0328959b6ae02173c2b3cc57684ad23eb4fedb547fbf1a3b884f711fa7028)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAction")
    def put_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorMetricAlertAction", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__676e7d03c396ea96671bdf5ffec3e001225721f2a356237f9ea877da3c41fe29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAction", [value]))

    @jsii.member(jsii_name="putApplicationInsightsWebTestLocationAvailabilityCriteria")
    def put_application_insights_web_test_location_availability_criteria(
        self,
        *,
        component_id: builtins.str,
        failed_location_count: jsii.Number,
        web_test_id: builtins.str,
    ) -> None:
        '''
        :param component_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#component_id MonitorMetricAlert#component_id}.
        :param failed_location_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#failed_location_count MonitorMetricAlert#failed_location_count}.
        :param web_test_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#web_test_id MonitorMetricAlert#web_test_id}.
        '''
        value = MonitorMetricAlertApplicationInsightsWebTestLocationAvailabilityCriteria(
            component_id=component_id,
            failed_location_count=failed_location_count,
            web_test_id=web_test_id,
        )

        return typing.cast(None, jsii.invoke(self, "putApplicationInsightsWebTestLocationAvailabilityCriteria", [value]))

    @jsii.member(jsii_name="putCriteria")
    def put_criteria(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorMetricAlertCriteria", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__777329c4ddb1673be1ca1f520ca4dae69574985e4989935ece500f8ae0da1589)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCriteria", [value]))

    @jsii.member(jsii_name="putDynamicCriteria")
    def put_dynamic_criteria(
        self,
        *,
        aggregation: builtins.str,
        alert_sensitivity: builtins.str,
        metric_name: builtins.str,
        metric_namespace: builtins.str,
        operator: builtins.str,
        dimension: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorMetricAlertDynamicCriteriaDimension", typing.Dict[builtins.str, typing.Any]]]]] = None,
        evaluation_failure_count: typing.Optional[jsii.Number] = None,
        evaluation_total_count: typing.Optional[jsii.Number] = None,
        ignore_data_before: typing.Optional[builtins.str] = None,
        skip_metric_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param aggregation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#aggregation MonitorMetricAlert#aggregation}.
        :param alert_sensitivity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#alert_sensitivity MonitorMetricAlert#alert_sensitivity}.
        :param metric_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#metric_name MonitorMetricAlert#metric_name}.
        :param metric_namespace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#metric_namespace MonitorMetricAlert#metric_namespace}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#operator MonitorMetricAlert#operator}.
        :param dimension: dimension block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#dimension MonitorMetricAlert#dimension}
        :param evaluation_failure_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#evaluation_failure_count MonitorMetricAlert#evaluation_failure_count}.
        :param evaluation_total_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#evaluation_total_count MonitorMetricAlert#evaluation_total_count}.
        :param ignore_data_before: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#ignore_data_before MonitorMetricAlert#ignore_data_before}.
        :param skip_metric_validation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#skip_metric_validation MonitorMetricAlert#skip_metric_validation}.
        '''
        value = MonitorMetricAlertDynamicCriteria(
            aggregation=aggregation,
            alert_sensitivity=alert_sensitivity,
            metric_name=metric_name,
            metric_namespace=metric_namespace,
            operator=operator,
            dimension=dimension,
            evaluation_failure_count=evaluation_failure_count,
            evaluation_total_count=evaluation_total_count,
            ignore_data_before=ignore_data_before,
            skip_metric_validation=skip_metric_validation,
        )

        return typing.cast(None, jsii.invoke(self, "putDynamicCriteria", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#create MonitorMetricAlert#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#delete MonitorMetricAlert#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#read MonitorMetricAlert#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#update MonitorMetricAlert#update}.
        '''
        value = MonitorMetricAlertTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAction")
    def reset_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAction", []))

    @jsii.member(jsii_name="resetApplicationInsightsWebTestLocationAvailabilityCriteria")
    def reset_application_insights_web_test_location_availability_criteria(
        self,
    ) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApplicationInsightsWebTestLocationAvailabilityCriteria", []))

    @jsii.member(jsii_name="resetAutoMitigate")
    def reset_auto_mitigate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoMitigate", []))

    @jsii.member(jsii_name="resetCriteria")
    def reset_criteria(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCriteria", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetDynamicCriteria")
    def reset_dynamic_criteria(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamicCriteria", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetFrequency")
    def reset_frequency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFrequency", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetSeverity")
    def reset_severity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeverity", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTargetResourceLocation")
    def reset_target_resource_location(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetResourceLocation", []))

    @jsii.member(jsii_name="resetTargetResourceType")
    def reset_target_resource_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetResourceType", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetWindowSize")
    def reset_window_size(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWindowSize", []))

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
    @jsii.member(jsii_name="action")
    def action(self) -> "MonitorMetricAlertActionList":
        return typing.cast("MonitorMetricAlertActionList", jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="applicationInsightsWebTestLocationAvailabilityCriteria")
    def application_insights_web_test_location_availability_criteria(
        self,
    ) -> "MonitorMetricAlertApplicationInsightsWebTestLocationAvailabilityCriteriaOutputReference":
        return typing.cast("MonitorMetricAlertApplicationInsightsWebTestLocationAvailabilityCriteriaOutputReference", jsii.get(self, "applicationInsightsWebTestLocationAvailabilityCriteria"))

    @builtins.property
    @jsii.member(jsii_name="criteria")
    def criteria(self) -> "MonitorMetricAlertCriteriaList":
        return typing.cast("MonitorMetricAlertCriteriaList", jsii.get(self, "criteria"))

    @builtins.property
    @jsii.member(jsii_name="dynamicCriteria")
    def dynamic_criteria(self) -> "MonitorMetricAlertDynamicCriteriaOutputReference":
        return typing.cast("MonitorMetricAlertDynamicCriteriaOutputReference", jsii.get(self, "dynamicCriteria"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MonitorMetricAlertTimeoutsOutputReference":
        return typing.cast("MonitorMetricAlertTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorMetricAlertAction"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorMetricAlertAction"]]], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="applicationInsightsWebTestLocationAvailabilityCriteriaInput")
    def application_insights_web_test_location_availability_criteria_input(
        self,
    ) -> typing.Optional["MonitorMetricAlertApplicationInsightsWebTestLocationAvailabilityCriteria"]:
        return typing.cast(typing.Optional["MonitorMetricAlertApplicationInsightsWebTestLocationAvailabilityCriteria"], jsii.get(self, "applicationInsightsWebTestLocationAvailabilityCriteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="autoMitigateInput")
    def auto_mitigate_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoMitigateInput"))

    @builtins.property
    @jsii.member(jsii_name="criteriaInput")
    def criteria_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorMetricAlertCriteria"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorMetricAlertCriteria"]]], jsii.get(self, "criteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="dynamicCriteriaInput")
    def dynamic_criteria_input(
        self,
    ) -> typing.Optional["MonitorMetricAlertDynamicCriteria"]:
        return typing.cast(typing.Optional["MonitorMetricAlertDynamicCriteria"], jsii.get(self, "dynamicCriteriaInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="frequencyInput")
    def frequency_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "frequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="scopesInput")
    def scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scopesInput"))

    @builtins.property
    @jsii.member(jsii_name="severityInput")
    def severity_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "severityInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="targetResourceLocationInput")
    def target_resource_location_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetResourceLocationInput"))

    @builtins.property
    @jsii.member(jsii_name="targetResourceTypeInput")
    def target_resource_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetResourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MonitorMetricAlertTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MonitorMetricAlertTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="windowSizeInput")
    def window_size_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "windowSizeInput"))

    @builtins.property
    @jsii.member(jsii_name="autoMitigate")
    def auto_mitigate(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoMitigate"))

    @auto_mitigate.setter
    def auto_mitigate(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28a7e775ae260faaf231f95346e19998d1d7438745b96850a42f46f2299aa39b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoMitigate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc0252b0a0e7657cd729e6834eeb77c5a16ed8fb1bf28ba6f51ad7fa1408a622)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

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
            type_hints = typing.get_type_hints(_typecheckingstub__0e98208d12f6d869a29f85a02091f73a8285120c5a2681c829e71e5024f7b283)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="frequency")
    def frequency(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "frequency"))

    @frequency.setter
    def frequency(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cb70cde1bdb2ba46c0f6b6b609123046e6dae71740eb46582a71d855498df5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e1e43cf5e0dfcba1a6a82e13f6be8532c26c9679cdb0f0e1dad42e15d36f7f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99d06220bb9c7374a7b7cf9fe6d938040cb41bb1e79e6315bbc651b4b8084e49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7ccd829e4fa5aedac1b77dafd805e985d6eba0d62914616faebd7a18ba5e564)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scopes"))

    @scopes.setter
    def scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d0107cb37fc8938f79b43846d7ead5463ef4a406065ef86ede37a409d368b9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "severity"))

    @severity.setter
    def severity(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__def21492e9376096aca9a3b5241751c8a428a7e84a8fe0f61b0e7854cfd0add3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "severity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bfca965e56afd9d241e2abf07af9f4813b8329be59a2fd8cb1c7f31f3cb193a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetResourceLocation")
    def target_resource_location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetResourceLocation"))

    @target_resource_location.setter
    def target_resource_location(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e3945815c55ddc333a36d83cba10f59d4c112752a6198b37098c0056fbba231)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetResourceLocation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetResourceType")
    def target_resource_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetResourceType"))

    @target_resource_type.setter
    def target_resource_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__975c7215d417d6ca3a2c467a43a1d436c43b856220b90237b02b36ff6378c061)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetResourceType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="windowSize")
    def window_size(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "windowSize"))

    @window_size.setter
    def window_size(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc298356cbecf817a099da40050027d006866af23de7c378aa7fe7172fb64f2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "windowSize", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorMetricAlert.MonitorMetricAlertAction",
    jsii_struct_bases=[],
    name_mapping={
        "action_group_id": "actionGroupId",
        "webhook_properties": "webhookProperties",
    },
)
class MonitorMetricAlertAction:
    def __init__(
        self,
        *,
        action_group_id: builtins.str,
        webhook_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param action_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#action_group_id MonitorMetricAlert#action_group_id}.
        :param webhook_properties: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#webhook_properties MonitorMetricAlert#webhook_properties}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47d4dae3c3b9dd0f442b2826fe14f1d14a6a7d3b53a45a4da2413a7245f21498)
            check_type(argname="argument action_group_id", value=action_group_id, expected_type=type_hints["action_group_id"])
            check_type(argname="argument webhook_properties", value=webhook_properties, expected_type=type_hints["webhook_properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action_group_id": action_group_id,
        }
        if webhook_properties is not None:
            self._values["webhook_properties"] = webhook_properties

    @builtins.property
    def action_group_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#action_group_id MonitorMetricAlert#action_group_id}.'''
        result = self._values.get("action_group_id")
        assert result is not None, "Required property 'action_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def webhook_properties(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#webhook_properties MonitorMetricAlert#webhook_properties}.'''
        result = self._values.get("webhook_properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorMetricAlertAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorMetricAlertActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorMetricAlert.MonitorMetricAlertActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__835622bc14479ef7614b3498729678b114cde83661bd6621ee45b17d3cc89792)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "MonitorMetricAlertActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__764e4a16ea7c332f44399835410c6f567d8806e56d13ec1e326ac279ab36877c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorMetricAlertActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a94b71bdd87bd512301af24718b39fe4d927d59e8f35f1fa436bc7a9c90f398)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca54b3e6224e9fec326cb4469767728c717942cb17a87c74cc53f0b887417cc1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dac268e7fedb81c6073a902c85b91dafd03f353230e7be48a3962fce572548af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorMetricAlertAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorMetricAlertAction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorMetricAlertAction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d4ffb98a6a4237a5c0a04930fb0111a8f0a441bbfea81e6e05e17b166bf0ae7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorMetricAlertActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorMetricAlert.MonitorMetricAlertActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef91f8c20f6b720facc4882d31e0ea697cdcdf6dd1f6f935a7783050b54dd656)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetWebhookProperties")
    def reset_webhook_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebhookProperties", []))

    @builtins.property
    @jsii.member(jsii_name="actionGroupIdInput")
    def action_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="webhookPropertiesInput")
    def webhook_properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "webhookPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="actionGroupId")
    def action_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actionGroupId"))

    @action_group_id.setter
    def action_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ff2d60cc057a80a373551f73a3260e1d555c1926b89584b0ba92ae7fbbc598c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webhookProperties")
    def webhook_properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "webhookProperties"))

    @webhook_properties.setter
    def webhook_properties(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e25e863fd498b3f63d9e39989371325101eb79c42d6a4be0e111b745d7ed6a80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webhookProperties", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorMetricAlertAction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorMetricAlertAction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorMetricAlertAction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__138b843908f547c5bfbade0b1f0e3a3257c8c32f00928816de1181df3b7ee608)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorMetricAlert.MonitorMetricAlertApplicationInsightsWebTestLocationAvailabilityCriteria",
    jsii_struct_bases=[],
    name_mapping={
        "component_id": "componentId",
        "failed_location_count": "failedLocationCount",
        "web_test_id": "webTestId",
    },
)
class MonitorMetricAlertApplicationInsightsWebTestLocationAvailabilityCriteria:
    def __init__(
        self,
        *,
        component_id: builtins.str,
        failed_location_count: jsii.Number,
        web_test_id: builtins.str,
    ) -> None:
        '''
        :param component_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#component_id MonitorMetricAlert#component_id}.
        :param failed_location_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#failed_location_count MonitorMetricAlert#failed_location_count}.
        :param web_test_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#web_test_id MonitorMetricAlert#web_test_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7edda7b2065adeea22177c438ff278ad9fb26d804615629a4062b56f7c88ec89)
            check_type(argname="argument component_id", value=component_id, expected_type=type_hints["component_id"])
            check_type(argname="argument failed_location_count", value=failed_location_count, expected_type=type_hints["failed_location_count"])
            check_type(argname="argument web_test_id", value=web_test_id, expected_type=type_hints["web_test_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "component_id": component_id,
            "failed_location_count": failed_location_count,
            "web_test_id": web_test_id,
        }

    @builtins.property
    def component_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#component_id MonitorMetricAlert#component_id}.'''
        result = self._values.get("component_id")
        assert result is not None, "Required property 'component_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def failed_location_count(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#failed_location_count MonitorMetricAlert#failed_location_count}.'''
        result = self._values.get("failed_location_count")
        assert result is not None, "Required property 'failed_location_count' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def web_test_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#web_test_id MonitorMetricAlert#web_test_id}.'''
        result = self._values.get("web_test_id")
        assert result is not None, "Required property 'web_test_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorMetricAlertApplicationInsightsWebTestLocationAvailabilityCriteria(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorMetricAlertApplicationInsightsWebTestLocationAvailabilityCriteriaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorMetricAlert.MonitorMetricAlertApplicationInsightsWebTestLocationAvailabilityCriteriaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38378bc40d0c758374b52c25048240f3eb92e90fae7a507b3aec820c7eba2b66)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="componentIdInput")
    def component_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "componentIdInput"))

    @builtins.property
    @jsii.member(jsii_name="failedLocationCountInput")
    def failed_location_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "failedLocationCountInput"))

    @builtins.property
    @jsii.member(jsii_name="webTestIdInput")
    def web_test_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "webTestIdInput"))

    @builtins.property
    @jsii.member(jsii_name="componentId")
    def component_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "componentId"))

    @component_id.setter
    def component_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12c4fc7288ca289d56871f133b9305299a01faea00b2e05e2f9c908cb6103059)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "componentId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="failedLocationCount")
    def failed_location_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "failedLocationCount"))

    @failed_location_count.setter
    def failed_location_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a28e7495bcdf085acd398c16502e9683b44aae21bb7d76d3bc5ecde59c6d8ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "failedLocationCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webTestId")
    def web_test_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webTestId"))

    @web_test_id.setter
    def web_test_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93c97a2a8337558cdcd89eaa8ff1d7a9237bca112b786827cda8ebf55e7fab31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webTestId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorMetricAlertApplicationInsightsWebTestLocationAvailabilityCriteria]:
        return typing.cast(typing.Optional[MonitorMetricAlertApplicationInsightsWebTestLocationAvailabilityCriteria], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorMetricAlertApplicationInsightsWebTestLocationAvailabilityCriteria],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1ea1cdc9caa23ddb89c771214572680de2ab333082b476048a2cc36abb7ec89)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorMetricAlert.MonitorMetricAlertConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "scopes": "scopes",
        "action": "action",
        "application_insights_web_test_location_availability_criteria": "applicationInsightsWebTestLocationAvailabilityCriteria",
        "auto_mitigate": "autoMitigate",
        "criteria": "criteria",
        "description": "description",
        "dynamic_criteria": "dynamicCriteria",
        "enabled": "enabled",
        "frequency": "frequency",
        "id": "id",
        "severity": "severity",
        "tags": "tags",
        "target_resource_location": "targetResourceLocation",
        "target_resource_type": "targetResourceType",
        "timeouts": "timeouts",
        "window_size": "windowSize",
    },
)
class MonitorMetricAlertConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        resource_group_name: builtins.str,
        scopes: typing.Sequence[builtins.str],
        action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorMetricAlertAction, typing.Dict[builtins.str, typing.Any]]]]] = None,
        application_insights_web_test_location_availability_criteria: typing.Optional[typing.Union[MonitorMetricAlertApplicationInsightsWebTestLocationAvailabilityCriteria, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_mitigate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        criteria: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorMetricAlertCriteria", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        dynamic_criteria: typing.Optional[typing.Union["MonitorMetricAlertDynamicCriteria", typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        frequency: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        severity: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        target_resource_location: typing.Optional[builtins.str] = None,
        target_resource_type: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["MonitorMetricAlertTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        window_size: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#name MonitorMetricAlert#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#resource_group_name MonitorMetricAlert#resource_group_name}.
        :param scopes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#scopes MonitorMetricAlert#scopes}.
        :param action: action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#action MonitorMetricAlert#action}
        :param application_insights_web_test_location_availability_criteria: application_insights_web_test_location_availability_criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#application_insights_web_test_location_availability_criteria MonitorMetricAlert#application_insights_web_test_location_availability_criteria}
        :param auto_mitigate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#auto_mitigate MonitorMetricAlert#auto_mitigate}.
        :param criteria: criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#criteria MonitorMetricAlert#criteria}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#description MonitorMetricAlert#description}.
        :param dynamic_criteria: dynamic_criteria block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#dynamic_criteria MonitorMetricAlert#dynamic_criteria}
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#enabled MonitorMetricAlert#enabled}.
        :param frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#frequency MonitorMetricAlert#frequency}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#id MonitorMetricAlert#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param severity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#severity MonitorMetricAlert#severity}.
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#tags MonitorMetricAlert#tags}.
        :param target_resource_location: The location of the target pluginsdk. Required when using subscription, resource group scope or multiple scopes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#target_resource_location MonitorMetricAlert#target_resource_location}
        :param target_resource_type: The resource type (e.g. Microsoft.Compute/virtualMachines) of the target pluginsdk. Required when using subscription, resource group scope or multiple scopes. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#target_resource_type MonitorMetricAlert#target_resource_type}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#timeouts MonitorMetricAlert#timeouts}
        :param window_size: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#window_size MonitorMetricAlert#window_size}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(application_insights_web_test_location_availability_criteria, dict):
            application_insights_web_test_location_availability_criteria = MonitorMetricAlertApplicationInsightsWebTestLocationAvailabilityCriteria(**application_insights_web_test_location_availability_criteria)
        if isinstance(dynamic_criteria, dict):
            dynamic_criteria = MonitorMetricAlertDynamicCriteria(**dynamic_criteria)
        if isinstance(timeouts, dict):
            timeouts = MonitorMetricAlertTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75dc1392dff489d7de757817cff3e482ce8a04e37ac2cebab56471b00d741191)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument scopes", value=scopes, expected_type=type_hints["scopes"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument application_insights_web_test_location_availability_criteria", value=application_insights_web_test_location_availability_criteria, expected_type=type_hints["application_insights_web_test_location_availability_criteria"])
            check_type(argname="argument auto_mitigate", value=auto_mitigate, expected_type=type_hints["auto_mitigate"])
            check_type(argname="argument criteria", value=criteria, expected_type=type_hints["criteria"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument dynamic_criteria", value=dynamic_criteria, expected_type=type_hints["dynamic_criteria"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_resource_location", value=target_resource_location, expected_type=type_hints["target_resource_location"])
            check_type(argname="argument target_resource_type", value=target_resource_type, expected_type=type_hints["target_resource_type"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument window_size", value=window_size, expected_type=type_hints["window_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "resource_group_name": resource_group_name,
            "scopes": scopes,
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
        if action is not None:
            self._values["action"] = action
        if application_insights_web_test_location_availability_criteria is not None:
            self._values["application_insights_web_test_location_availability_criteria"] = application_insights_web_test_location_availability_criteria
        if auto_mitigate is not None:
            self._values["auto_mitigate"] = auto_mitigate
        if criteria is not None:
            self._values["criteria"] = criteria
        if description is not None:
            self._values["description"] = description
        if dynamic_criteria is not None:
            self._values["dynamic_criteria"] = dynamic_criteria
        if enabled is not None:
            self._values["enabled"] = enabled
        if frequency is not None:
            self._values["frequency"] = frequency
        if id is not None:
            self._values["id"] = id
        if severity is not None:
            self._values["severity"] = severity
        if tags is not None:
            self._values["tags"] = tags
        if target_resource_location is not None:
            self._values["target_resource_location"] = target_resource_location
        if target_resource_type is not None:
            self._values["target_resource_type"] = target_resource_type
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if window_size is not None:
            self._values["window_size"] = window_size

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
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#name MonitorMetricAlert#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#resource_group_name MonitorMetricAlert#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scopes(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#scopes MonitorMetricAlert#scopes}.'''
        result = self._values.get("scopes")
        assert result is not None, "Required property 'scopes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def action(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorMetricAlertAction]]]:
        '''action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#action MonitorMetricAlert#action}
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorMetricAlertAction]]], result)

    @builtins.property
    def application_insights_web_test_location_availability_criteria(
        self,
    ) -> typing.Optional[MonitorMetricAlertApplicationInsightsWebTestLocationAvailabilityCriteria]:
        '''application_insights_web_test_location_availability_criteria block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#application_insights_web_test_location_availability_criteria MonitorMetricAlert#application_insights_web_test_location_availability_criteria}
        '''
        result = self._values.get("application_insights_web_test_location_availability_criteria")
        return typing.cast(typing.Optional[MonitorMetricAlertApplicationInsightsWebTestLocationAvailabilityCriteria], result)

    @builtins.property
    def auto_mitigate(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#auto_mitigate MonitorMetricAlert#auto_mitigate}.'''
        result = self._values.get("auto_mitigate")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def criteria(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorMetricAlertCriteria"]]]:
        '''criteria block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#criteria MonitorMetricAlert#criteria}
        '''
        result = self._values.get("criteria")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorMetricAlertCriteria"]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#description MonitorMetricAlert#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dynamic_criteria(self) -> typing.Optional["MonitorMetricAlertDynamicCriteria"]:
        '''dynamic_criteria block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#dynamic_criteria MonitorMetricAlert#dynamic_criteria}
        '''
        result = self._values.get("dynamic_criteria")
        return typing.cast(typing.Optional["MonitorMetricAlertDynamicCriteria"], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#enabled MonitorMetricAlert#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def frequency(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#frequency MonitorMetricAlert#frequency}.'''
        result = self._values.get("frequency")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#id MonitorMetricAlert#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def severity(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#severity MonitorMetricAlert#severity}.'''
        result = self._values.get("severity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#tags MonitorMetricAlert#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def target_resource_location(self) -> typing.Optional[builtins.str]:
        '''The location of the target pluginsdk. Required when using subscription, resource group scope or multiple scopes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#target_resource_location MonitorMetricAlert#target_resource_location}
        '''
        result = self._values.get("target_resource_location")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_resource_type(self) -> typing.Optional[builtins.str]:
        '''The resource type (e.g. Microsoft.Compute/virtualMachines) of the target pluginsdk. Required when using subscription, resource group scope or multiple scopes.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#target_resource_type MonitorMetricAlert#target_resource_type}
        '''
        result = self._values.get("target_resource_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MonitorMetricAlertTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#timeouts MonitorMetricAlert#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MonitorMetricAlertTimeouts"], result)

    @builtins.property
    def window_size(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#window_size MonitorMetricAlert#window_size}.'''
        result = self._values.get("window_size")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorMetricAlertConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorMetricAlert.MonitorMetricAlertCriteria",
    jsii_struct_bases=[],
    name_mapping={
        "aggregation": "aggregation",
        "metric_name": "metricName",
        "metric_namespace": "metricNamespace",
        "operator": "operator",
        "threshold": "threshold",
        "dimension": "dimension",
        "skip_metric_validation": "skipMetricValidation",
    },
)
class MonitorMetricAlertCriteria:
    def __init__(
        self,
        *,
        aggregation: builtins.str,
        metric_name: builtins.str,
        metric_namespace: builtins.str,
        operator: builtins.str,
        threshold: jsii.Number,
        dimension: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorMetricAlertCriteriaDimension", typing.Dict[builtins.str, typing.Any]]]]] = None,
        skip_metric_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param aggregation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#aggregation MonitorMetricAlert#aggregation}.
        :param metric_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#metric_name MonitorMetricAlert#metric_name}.
        :param metric_namespace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#metric_namespace MonitorMetricAlert#metric_namespace}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#operator MonitorMetricAlert#operator}.
        :param threshold: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#threshold MonitorMetricAlert#threshold}.
        :param dimension: dimension block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#dimension MonitorMetricAlert#dimension}
        :param skip_metric_validation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#skip_metric_validation MonitorMetricAlert#skip_metric_validation}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28b950dfce4d969ad3e0767717d08e803c8298cfff7dc03f46aa20cf1d6814b5)
            check_type(argname="argument aggregation", value=aggregation, expected_type=type_hints["aggregation"])
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument metric_namespace", value=metric_namespace, expected_type=type_hints["metric_namespace"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument threshold", value=threshold, expected_type=type_hints["threshold"])
            check_type(argname="argument dimension", value=dimension, expected_type=type_hints["dimension"])
            check_type(argname="argument skip_metric_validation", value=skip_metric_validation, expected_type=type_hints["skip_metric_validation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aggregation": aggregation,
            "metric_name": metric_name,
            "metric_namespace": metric_namespace,
            "operator": operator,
            "threshold": threshold,
        }
        if dimension is not None:
            self._values["dimension"] = dimension
        if skip_metric_validation is not None:
            self._values["skip_metric_validation"] = skip_metric_validation

    @builtins.property
    def aggregation(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#aggregation MonitorMetricAlert#aggregation}.'''
        result = self._values.get("aggregation")
        assert result is not None, "Required property 'aggregation' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#metric_name MonitorMetricAlert#metric_name}.'''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_namespace(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#metric_namespace MonitorMetricAlert#metric_namespace}.'''
        result = self._values.get("metric_namespace")
        assert result is not None, "Required property 'metric_namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#operator MonitorMetricAlert#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def threshold(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#threshold MonitorMetricAlert#threshold}.'''
        result = self._values.get("threshold")
        assert result is not None, "Required property 'threshold' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def dimension(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorMetricAlertCriteriaDimension"]]]:
        '''dimension block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#dimension MonitorMetricAlert#dimension}
        '''
        result = self._values.get("dimension")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorMetricAlertCriteriaDimension"]]], result)

    @builtins.property
    def skip_metric_validation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#skip_metric_validation MonitorMetricAlert#skip_metric_validation}.'''
        result = self._values.get("skip_metric_validation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorMetricAlertCriteria(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorMetricAlert.MonitorMetricAlertCriteriaDimension",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "operator": "operator", "values": "values"},
)
class MonitorMetricAlertCriteriaDimension:
    def __init__(
        self,
        *,
        name: builtins.str,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#name MonitorMetricAlert#name}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#operator MonitorMetricAlert#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#values MonitorMetricAlert#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82dc79024467efcbd4bcb962db52cba23b683c20979c7f9e91646fb1efffc51e)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#name MonitorMetricAlert#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#operator MonitorMetricAlert#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#values MonitorMetricAlert#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorMetricAlertCriteriaDimension(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorMetricAlertCriteriaDimensionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorMetricAlert.MonitorMetricAlertCriteriaDimensionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__efdbf5888b28ca2001cf6f3b0615683d4e731a728fa86a0032b6b28bfbd8573a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorMetricAlertCriteriaDimensionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cf510e198378a34bd9abec127ee2f13cda07ecb16783e68b6c3e6b2b0c0146e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorMetricAlertCriteriaDimensionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06a8d0df6ae42a2fb0244d98914962a24c400fbf8bec7f4f2f715a31268d88ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a33651f10b152c54a06012953bdeebb3474ae75068638dc5e6769f63fb74a8d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c2f9970c1da802a78d2d8b4aceb4b3cbb72d7d3dbaa857ceb5b2f511131343c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorMetricAlertCriteriaDimension]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorMetricAlertCriteriaDimension]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorMetricAlertCriteriaDimension]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b3ff28f9fa68dd7da8a8b8b548a1063fbdb0331aa899e2e963dd11f1a67f48a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorMetricAlertCriteriaDimensionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorMetricAlert.MonitorMetricAlertCriteriaDimensionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c0838a6067abe8de6c7ecf339ea0e030fb67dbb47be7286cce2f2d9c9459b9e5)
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
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c939314914a95bd9d2bbae3c6e4ee9aadd7282da4ed3124a4afe2de7c62f5b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0869a6fc104ccd354a238e7ed4616ce914cbe1ee82b968833b6fdc5e8a66182b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37e5a547e34da74ebda4d174f3c10c7bc9503084ff62d3d3453b4252da01138f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorMetricAlertCriteriaDimension]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorMetricAlertCriteriaDimension]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorMetricAlertCriteriaDimension]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ee8e9e6e13eec078400c26f096fe9b134860f5f40396bd6435e8b1c47f18ef2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorMetricAlertCriteriaList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorMetricAlert.MonitorMetricAlertCriteriaList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__95d6f45cd28554e84c20c0325cd138690d8e7d498b99122a806131976074c4a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "MonitorMetricAlertCriteriaOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__715f157637a382e6d0cd295d9d22bf66fdba8cbebeb861292a297574b5dd5d6f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorMetricAlertCriteriaOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eea0c7cfd6f445eddf84a87473b3930a699be844a21c7e214fef08fb965cf19e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9e02b0987f3ae2e253a5d8773e6f320362fd748ff53e0171596ff04298dbe42)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6173389d913f05c5f9b577254721eb26c89276e3f76ca2a60c33e53416c76b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorMetricAlertCriteria]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorMetricAlertCriteria]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorMetricAlertCriteria]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68ce997850965a2447c1fba197e734d1bbd5b6e0cff986309ecfabe3019960df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorMetricAlertCriteriaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorMetricAlert.MonitorMetricAlertCriteriaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d4ce025ff96c8504505a664a5131767c77487100c065c24c5542f6602511cbb7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putDimension")
    def put_dimension(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorMetricAlertCriteriaDimension, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fa1fd700edb2a5d5f99fc83bc5ec5b792ba572e2bf6ea6545427c115c575e67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDimension", [value]))

    @jsii.member(jsii_name="resetDimension")
    def reset_dimension(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDimension", []))

    @jsii.member(jsii_name="resetSkipMetricValidation")
    def reset_skip_metric_validation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipMetricValidation", []))

    @builtins.property
    @jsii.member(jsii_name="dimension")
    def dimension(self) -> MonitorMetricAlertCriteriaDimensionList:
        return typing.cast(MonitorMetricAlertCriteriaDimensionList, jsii.get(self, "dimension"))

    @builtins.property
    @jsii.member(jsii_name="aggregationInput")
    def aggregation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aggregationInput"))

    @builtins.property
    @jsii.member(jsii_name="dimensionInput")
    def dimension_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorMetricAlertCriteriaDimension]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorMetricAlertCriteriaDimension]]], jsii.get(self, "dimensionInput"))

    @builtins.property
    @jsii.member(jsii_name="metricNameInput")
    def metric_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricNameInput"))

    @builtins.property
    @jsii.member(jsii_name="metricNamespaceInput")
    def metric_namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricNamespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="skipMetricValidationInput")
    def skip_metric_validation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipMetricValidationInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdInput")
    def threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "thresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="aggregation")
    def aggregation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aggregation"))

    @aggregation.setter
    def aggregation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b15b1c26ccfa09bf5219f7b842884ed0fca1de04123ab16cc42555af9f05fd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aggregation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricName")
    def metric_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricName"))

    @metric_name.setter
    def metric_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93ec431bf66b871f74debe293359ca422eb70e83e24e72063ead600d2d3e0509)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricNamespace")
    def metric_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricNamespace"))

    @metric_namespace.setter
    def metric_namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c99246dc36f8182217818b2a1ac9c827fe65b56a72b09d3fce0ed0d446fc8be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricNamespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63f0d337741d15d14483a3f8fcdb19b81eec76340e874d61dbdb397abcff3fda)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipMetricValidation")
    def skip_metric_validation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "skipMetricValidation"))

    @skip_metric_validation.setter
    def skip_metric_validation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d71f0b67686f632db8abe71808fd3d0d4b5c916947d3e424847d866900150b33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipMetricValidation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="threshold")
    def threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "threshold"))

    @threshold.setter
    def threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ff29674dc1bb16d32fcd97bd8879b62be44d4c24877dc3ac19077a4c00706cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "threshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorMetricAlertCriteria]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorMetricAlertCriteria]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorMetricAlertCriteria]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60792f056ff64e2229b36c53555ed942131bdfe82cf9a86d3fe1405e9b2af5f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorMetricAlert.MonitorMetricAlertDynamicCriteria",
    jsii_struct_bases=[],
    name_mapping={
        "aggregation": "aggregation",
        "alert_sensitivity": "alertSensitivity",
        "metric_name": "metricName",
        "metric_namespace": "metricNamespace",
        "operator": "operator",
        "dimension": "dimension",
        "evaluation_failure_count": "evaluationFailureCount",
        "evaluation_total_count": "evaluationTotalCount",
        "ignore_data_before": "ignoreDataBefore",
        "skip_metric_validation": "skipMetricValidation",
    },
)
class MonitorMetricAlertDynamicCriteria:
    def __init__(
        self,
        *,
        aggregation: builtins.str,
        alert_sensitivity: builtins.str,
        metric_name: builtins.str,
        metric_namespace: builtins.str,
        operator: builtins.str,
        dimension: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorMetricAlertDynamicCriteriaDimension", typing.Dict[builtins.str, typing.Any]]]]] = None,
        evaluation_failure_count: typing.Optional[jsii.Number] = None,
        evaluation_total_count: typing.Optional[jsii.Number] = None,
        ignore_data_before: typing.Optional[builtins.str] = None,
        skip_metric_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param aggregation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#aggregation MonitorMetricAlert#aggregation}.
        :param alert_sensitivity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#alert_sensitivity MonitorMetricAlert#alert_sensitivity}.
        :param metric_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#metric_name MonitorMetricAlert#metric_name}.
        :param metric_namespace: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#metric_namespace MonitorMetricAlert#metric_namespace}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#operator MonitorMetricAlert#operator}.
        :param dimension: dimension block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#dimension MonitorMetricAlert#dimension}
        :param evaluation_failure_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#evaluation_failure_count MonitorMetricAlert#evaluation_failure_count}.
        :param evaluation_total_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#evaluation_total_count MonitorMetricAlert#evaluation_total_count}.
        :param ignore_data_before: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#ignore_data_before MonitorMetricAlert#ignore_data_before}.
        :param skip_metric_validation: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#skip_metric_validation MonitorMetricAlert#skip_metric_validation}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13c3d1f4d6af5e9461c3ead61b1ac370f43dad1a30f9ca54e872fb92edcfcdd6)
            check_type(argname="argument aggregation", value=aggregation, expected_type=type_hints["aggregation"])
            check_type(argname="argument alert_sensitivity", value=alert_sensitivity, expected_type=type_hints["alert_sensitivity"])
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
            check_type(argname="argument metric_namespace", value=metric_namespace, expected_type=type_hints["metric_namespace"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument dimension", value=dimension, expected_type=type_hints["dimension"])
            check_type(argname="argument evaluation_failure_count", value=evaluation_failure_count, expected_type=type_hints["evaluation_failure_count"])
            check_type(argname="argument evaluation_total_count", value=evaluation_total_count, expected_type=type_hints["evaluation_total_count"])
            check_type(argname="argument ignore_data_before", value=ignore_data_before, expected_type=type_hints["ignore_data_before"])
            check_type(argname="argument skip_metric_validation", value=skip_metric_validation, expected_type=type_hints["skip_metric_validation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aggregation": aggregation,
            "alert_sensitivity": alert_sensitivity,
            "metric_name": metric_name,
            "metric_namespace": metric_namespace,
            "operator": operator,
        }
        if dimension is not None:
            self._values["dimension"] = dimension
        if evaluation_failure_count is not None:
            self._values["evaluation_failure_count"] = evaluation_failure_count
        if evaluation_total_count is not None:
            self._values["evaluation_total_count"] = evaluation_total_count
        if ignore_data_before is not None:
            self._values["ignore_data_before"] = ignore_data_before
        if skip_metric_validation is not None:
            self._values["skip_metric_validation"] = skip_metric_validation

    @builtins.property
    def aggregation(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#aggregation MonitorMetricAlert#aggregation}.'''
        result = self._values.get("aggregation")
        assert result is not None, "Required property 'aggregation' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alert_sensitivity(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#alert_sensitivity MonitorMetricAlert#alert_sensitivity}.'''
        result = self._values.get("alert_sensitivity")
        assert result is not None, "Required property 'alert_sensitivity' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#metric_name MonitorMetricAlert#metric_name}.'''
        result = self._values.get("metric_name")
        assert result is not None, "Required property 'metric_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def metric_namespace(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#metric_namespace MonitorMetricAlert#metric_namespace}.'''
        result = self._values.get("metric_namespace")
        assert result is not None, "Required property 'metric_namespace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#operator MonitorMetricAlert#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dimension(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorMetricAlertDynamicCriteriaDimension"]]]:
        '''dimension block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#dimension MonitorMetricAlert#dimension}
        '''
        result = self._values.get("dimension")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorMetricAlertDynamicCriteriaDimension"]]], result)

    @builtins.property
    def evaluation_failure_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#evaluation_failure_count MonitorMetricAlert#evaluation_failure_count}.'''
        result = self._values.get("evaluation_failure_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def evaluation_total_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#evaluation_total_count MonitorMetricAlert#evaluation_total_count}.'''
        result = self._values.get("evaluation_total_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ignore_data_before(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#ignore_data_before MonitorMetricAlert#ignore_data_before}.'''
        result = self._values.get("ignore_data_before")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def skip_metric_validation(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#skip_metric_validation MonitorMetricAlert#skip_metric_validation}.'''
        result = self._values.get("skip_metric_validation")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorMetricAlertDynamicCriteria(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorMetricAlert.MonitorMetricAlertDynamicCriteriaDimension",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "operator": "operator", "values": "values"},
)
class MonitorMetricAlertDynamicCriteriaDimension:
    def __init__(
        self,
        *,
        name: builtins.str,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#name MonitorMetricAlert#name}.
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#operator MonitorMetricAlert#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#values MonitorMetricAlert#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3292157cdab70cb9a59eca72bc04e323e568263d296b2d589a2e606087e2a7c9)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#name MonitorMetricAlert#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#operator MonitorMetricAlert#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#values MonitorMetricAlert#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorMetricAlertDynamicCriteriaDimension(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorMetricAlertDynamicCriteriaDimensionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorMetricAlert.MonitorMetricAlertDynamicCriteriaDimensionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b583b56e90523b349fb8a1f03381f38ca874c0bcdfed707c910dfcca92915b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorMetricAlertDynamicCriteriaDimensionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03298530059829e17806f389355832287ef14efb1cc411d578704fd12e1499cd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorMetricAlertDynamicCriteriaDimensionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__deec7566200df5c044ce42a017a8e59e913a36f7a58cf3ecce63491dde1a9275)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f7340c95705207a238aae7ec9a204369b3ef4f038b389d7ab3d78f755dd76a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__494fd3b0cafbd5282abbe06db1a0d0fe4cc4f268b03ef23a146c3cc549a9b157)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorMetricAlertDynamicCriteriaDimension]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorMetricAlertDynamicCriteriaDimension]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorMetricAlertDynamicCriteriaDimension]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a72de36f0fe73ab9f7cd1b66ea6c23d2b7a3a71c71da1baebb23fdb6ed0fb0aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorMetricAlertDynamicCriteriaDimensionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorMetricAlert.MonitorMetricAlertDynamicCriteriaDimensionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c21daa88f5bc4df77bfbac2ed8b35210d46c55b735a90216c6749241c3afa2ab)
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
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5df00c4fa83308890d643b2692cb4add09e10963c210cc502a5c5c44761e1d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__450a035444835001f18dd28ced8b80626243db018f335143f204ad188f8007d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc435b8993014671ccdd44abc4c008f2bf941079ae8f08f7083ae58e2906cfd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorMetricAlertDynamicCriteriaDimension]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorMetricAlertDynamicCriteriaDimension]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorMetricAlertDynamicCriteriaDimension]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31a5e80d17878240c4759a707db457a42abb863c4311a50ef671c85bd8ca9e2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorMetricAlertDynamicCriteriaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorMetricAlert.MonitorMetricAlertDynamicCriteriaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ebb26103bc6890916ba7c7bf46f6b950ed6b914e5565a39d85bc7de0e290628)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDimension")
    def put_dimension(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorMetricAlertDynamicCriteriaDimension, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73a5d66803e57fa2f69708e4be9ff932ea893c6a2102bd9eb082c1939102ccea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDimension", [value]))

    @jsii.member(jsii_name="resetDimension")
    def reset_dimension(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDimension", []))

    @jsii.member(jsii_name="resetEvaluationFailureCount")
    def reset_evaluation_failure_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEvaluationFailureCount", []))

    @jsii.member(jsii_name="resetEvaluationTotalCount")
    def reset_evaluation_total_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEvaluationTotalCount", []))

    @jsii.member(jsii_name="resetIgnoreDataBefore")
    def reset_ignore_data_before(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreDataBefore", []))

    @jsii.member(jsii_name="resetSkipMetricValidation")
    def reset_skip_metric_validation(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSkipMetricValidation", []))

    @builtins.property
    @jsii.member(jsii_name="dimension")
    def dimension(self) -> MonitorMetricAlertDynamicCriteriaDimensionList:
        return typing.cast(MonitorMetricAlertDynamicCriteriaDimensionList, jsii.get(self, "dimension"))

    @builtins.property
    @jsii.member(jsii_name="aggregationInput")
    def aggregation_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "aggregationInput"))

    @builtins.property
    @jsii.member(jsii_name="alertSensitivityInput")
    def alert_sensitivity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alertSensitivityInput"))

    @builtins.property
    @jsii.member(jsii_name="dimensionInput")
    def dimension_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorMetricAlertDynamicCriteriaDimension]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorMetricAlertDynamicCriteriaDimension]]], jsii.get(self, "dimensionInput"))

    @builtins.property
    @jsii.member(jsii_name="evaluationFailureCountInput")
    def evaluation_failure_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "evaluationFailureCountInput"))

    @builtins.property
    @jsii.member(jsii_name="evaluationTotalCountInput")
    def evaluation_total_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "evaluationTotalCountInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreDataBeforeInput")
    def ignore_data_before_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ignoreDataBeforeInput"))

    @builtins.property
    @jsii.member(jsii_name="metricNameInput")
    def metric_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricNameInput"))

    @builtins.property
    @jsii.member(jsii_name="metricNamespaceInput")
    def metric_namespace_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metricNamespaceInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="skipMetricValidationInput")
    def skip_metric_validation_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "skipMetricValidationInput"))

    @builtins.property
    @jsii.member(jsii_name="aggregation")
    def aggregation(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "aggregation"))

    @aggregation.setter
    def aggregation(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59b886698c3d9b577d369004188cf2b490ec314ab3327ef72ba7b23c96614204)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "aggregation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="alertSensitivity")
    def alert_sensitivity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alertSensitivity"))

    @alert_sensitivity.setter
    def alert_sensitivity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b664e26e5a260503d1d9386e8d0139dc089bbc36e674bd0172e65e3c45e918f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alertSensitivity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="evaluationFailureCount")
    def evaluation_failure_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "evaluationFailureCount"))

    @evaluation_failure_count.setter
    def evaluation_failure_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df12027e96666019ef53de2ad46899bc0ecf3024708669fe5a58f00a4ad38fdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "evaluationFailureCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="evaluationTotalCount")
    def evaluation_total_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "evaluationTotalCount"))

    @evaluation_total_count.setter
    def evaluation_total_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24744d9bfe5d05dfb8e3dc2ada540b36e04805b843ad7e9edc36c93d056850db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "evaluationTotalCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ignoreDataBefore")
    def ignore_data_before(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ignoreDataBefore"))

    @ignore_data_before.setter
    def ignore_data_before(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__045cc7c400bfe4f103bcb4da5c2254dc3dd1511db46d02120045f777914eda50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreDataBefore", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricName")
    def metric_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricName"))

    @metric_name.setter
    def metric_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e0777a2925f6aa6f0b505c7d74eb846e8112872bfef7309ab5e6852737df481)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="metricNamespace")
    def metric_namespace(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metricNamespace"))

    @metric_namespace.setter
    def metric_namespace(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__735a67260f2640c191358ad8fc6d63a536971ad874fd010924d3ea706f15d3a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metricNamespace", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20af8cb69fa3f05425df85d54782700fe201f1babcf7fbe5c413af871f5886d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="skipMetricValidation")
    def skip_metric_validation(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "skipMetricValidation"))

    @skip_metric_validation.setter
    def skip_metric_validation(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb449447aadbfa8048b4a117ffa0ab15d04e6ec6ccc34aed15f6ff8a9944ad4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "skipMetricValidation", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitorMetricAlertDynamicCriteria]:
        return typing.cast(typing.Optional[MonitorMetricAlertDynamicCriteria], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorMetricAlertDynamicCriteria],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e1daf1eddf0ce91b5c4bbff7f91596578caf4ae71df28c3ba94629fe0e05085)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorMetricAlert.MonitorMetricAlertTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MonitorMetricAlertTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#create MonitorMetricAlert#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#delete MonitorMetricAlert#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#read MonitorMetricAlert#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#update MonitorMetricAlert#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2f7ac6e35e6b7f4922ae4e9090b80fdfb7952395517f46cbd8a1e7f8aecf895)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#create MonitorMetricAlert#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#delete MonitorMetricAlert#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#read MonitorMetricAlert#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_metric_alert#update MonitorMetricAlert#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorMetricAlertTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorMetricAlertTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorMetricAlert.MonitorMetricAlertTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fcc3e0c4479175fc42f93af4859dbeb5d7522b37f7b7ca54982c2dbca2b53037)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a9be23d284652b50f4168df661db14b4cfe9b6c7c254e3fb1ba45d061174e24d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cce0c6b0b2616673a11de92eb60b012732065e17bf3c3d473813fdb24a9cbbe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0ab3c55325999a17fa46ee908689bb966d0ad235c00203cc07d8e4a7dbf7747)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5d9638c35f64cbbea4285049ce9210b4c83464e853de3ccc34bc6fab06ceb71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorMetricAlertTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorMetricAlertTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorMetricAlertTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ba42c72df658b1d04e0fe8283d86b09f418b9d2d15b1b552b0300f577099e9d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MonitorMetricAlert",
    "MonitorMetricAlertAction",
    "MonitorMetricAlertActionList",
    "MonitorMetricAlertActionOutputReference",
    "MonitorMetricAlertApplicationInsightsWebTestLocationAvailabilityCriteria",
    "MonitorMetricAlertApplicationInsightsWebTestLocationAvailabilityCriteriaOutputReference",
    "MonitorMetricAlertConfig",
    "MonitorMetricAlertCriteria",
    "MonitorMetricAlertCriteriaDimension",
    "MonitorMetricAlertCriteriaDimensionList",
    "MonitorMetricAlertCriteriaDimensionOutputReference",
    "MonitorMetricAlertCriteriaList",
    "MonitorMetricAlertCriteriaOutputReference",
    "MonitorMetricAlertDynamicCriteria",
    "MonitorMetricAlertDynamicCriteriaDimension",
    "MonitorMetricAlertDynamicCriteriaDimensionList",
    "MonitorMetricAlertDynamicCriteriaDimensionOutputReference",
    "MonitorMetricAlertDynamicCriteriaOutputReference",
    "MonitorMetricAlertTimeouts",
    "MonitorMetricAlertTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__7a064176265b0567dbf284cff915827b4357ccb233fe03d1a2b8d225b14cfea7(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    resource_group_name: builtins.str,
    scopes: typing.Sequence[builtins.str],
    action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorMetricAlertAction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    application_insights_web_test_location_availability_criteria: typing.Optional[typing.Union[MonitorMetricAlertApplicationInsightsWebTestLocationAvailabilityCriteria, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_mitigate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    criteria: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorMetricAlertCriteria, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    dynamic_criteria: typing.Optional[typing.Union[MonitorMetricAlertDynamicCriteria, typing.Dict[builtins.str, typing.Any]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    frequency: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    severity: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    target_resource_location: typing.Optional[builtins.str] = None,
    target_resource_type: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[MonitorMetricAlertTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    window_size: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__14e0328959b6ae02173c2b3cc57684ad23eb4fedb547fbf1a3b884f711fa7028(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__676e7d03c396ea96671bdf5ffec3e001225721f2a356237f9ea877da3c41fe29(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorMetricAlertAction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__777329c4ddb1673be1ca1f520ca4dae69574985e4989935ece500f8ae0da1589(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorMetricAlertCriteria, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28a7e775ae260faaf231f95346e19998d1d7438745b96850a42f46f2299aa39b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc0252b0a0e7657cd729e6834eeb77c5a16ed8fb1bf28ba6f51ad7fa1408a622(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e98208d12f6d869a29f85a02091f73a8285120c5a2681c829e71e5024f7b283(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cb70cde1bdb2ba46c0f6b6b609123046e6dae71740eb46582a71d855498df5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e1e43cf5e0dfcba1a6a82e13f6be8532c26c9679cdb0f0e1dad42e15d36f7f9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99d06220bb9c7374a7b7cf9fe6d938040cb41bb1e79e6315bbc651b4b8084e49(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7ccd829e4fa5aedac1b77dafd805e985d6eba0d62914616faebd7a18ba5e564(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d0107cb37fc8938f79b43846d7ead5463ef4a406065ef86ede37a409d368b9e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__def21492e9376096aca9a3b5241751c8a428a7e84a8fe0f61b0e7854cfd0add3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bfca965e56afd9d241e2abf07af9f4813b8329be59a2fd8cb1c7f31f3cb193a(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e3945815c55ddc333a36d83cba10f59d4c112752a6198b37098c0056fbba231(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__975c7215d417d6ca3a2c467a43a1d436c43b856220b90237b02b36ff6378c061(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc298356cbecf817a099da40050027d006866af23de7c378aa7fe7172fb64f2b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47d4dae3c3b9dd0f442b2826fe14f1d14a6a7d3b53a45a4da2413a7245f21498(
    *,
    action_group_id: builtins.str,
    webhook_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__835622bc14479ef7614b3498729678b114cde83661bd6621ee45b17d3cc89792(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__764e4a16ea7c332f44399835410c6f567d8806e56d13ec1e326ac279ab36877c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a94b71bdd87bd512301af24718b39fe4d927d59e8f35f1fa436bc7a9c90f398(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca54b3e6224e9fec326cb4469767728c717942cb17a87c74cc53f0b887417cc1(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dac268e7fedb81c6073a902c85b91dafd03f353230e7be48a3962fce572548af(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d4ffb98a6a4237a5c0a04930fb0111a8f0a441bbfea81e6e05e17b166bf0ae7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorMetricAlertAction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef91f8c20f6b720facc4882d31e0ea697cdcdf6dd1f6f935a7783050b54dd656(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ff2d60cc057a80a373551f73a3260e1d555c1926b89584b0ba92ae7fbbc598c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e25e863fd498b3f63d9e39989371325101eb79c42d6a4be0e111b745d7ed6a80(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__138b843908f547c5bfbade0b1f0e3a3257c8c32f00928816de1181df3b7ee608(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorMetricAlertAction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7edda7b2065adeea22177c438ff278ad9fb26d804615629a4062b56f7c88ec89(
    *,
    component_id: builtins.str,
    failed_location_count: jsii.Number,
    web_test_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38378bc40d0c758374b52c25048240f3eb92e90fae7a507b3aec820c7eba2b66(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12c4fc7288ca289d56871f133b9305299a01faea00b2e05e2f9c908cb6103059(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a28e7495bcdf085acd398c16502e9683b44aae21bb7d76d3bc5ecde59c6d8ad(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93c97a2a8337558cdcd89eaa8ff1d7a9237bca112b786827cda8ebf55e7fab31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1ea1cdc9caa23ddb89c771214572680de2ab333082b476048a2cc36abb7ec89(
    value: typing.Optional[MonitorMetricAlertApplicationInsightsWebTestLocationAvailabilityCriteria],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75dc1392dff489d7de757817cff3e482ce8a04e37ac2cebab56471b00d741191(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    resource_group_name: builtins.str,
    scopes: typing.Sequence[builtins.str],
    action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorMetricAlertAction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    application_insights_web_test_location_availability_criteria: typing.Optional[typing.Union[MonitorMetricAlertApplicationInsightsWebTestLocationAvailabilityCriteria, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_mitigate: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    criteria: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorMetricAlertCriteria, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    dynamic_criteria: typing.Optional[typing.Union[MonitorMetricAlertDynamicCriteria, typing.Dict[builtins.str, typing.Any]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    frequency: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    severity: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    target_resource_location: typing.Optional[builtins.str] = None,
    target_resource_type: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[MonitorMetricAlertTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    window_size: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28b950dfce4d969ad3e0767717d08e803c8298cfff7dc03f46aa20cf1d6814b5(
    *,
    aggregation: builtins.str,
    metric_name: builtins.str,
    metric_namespace: builtins.str,
    operator: builtins.str,
    threshold: jsii.Number,
    dimension: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorMetricAlertCriteriaDimension, typing.Dict[builtins.str, typing.Any]]]]] = None,
    skip_metric_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82dc79024467efcbd4bcb962db52cba23b683c20979c7f9e91646fb1efffc51e(
    *,
    name: builtins.str,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efdbf5888b28ca2001cf6f3b0615683d4e731a728fa86a0032b6b28bfbd8573a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf510e198378a34bd9abec127ee2f13cda07ecb16783e68b6c3e6b2b0c0146e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06a8d0df6ae42a2fb0244d98914962a24c400fbf8bec7f4f2f715a31268d88ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a33651f10b152c54a06012953bdeebb3474ae75068638dc5e6769f63fb74a8d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2f9970c1da802a78d2d8b4aceb4b3cbb72d7d3dbaa857ceb5b2f511131343c4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b3ff28f9fa68dd7da8a8b8b548a1063fbdb0331aa899e2e963dd11f1a67f48a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorMetricAlertCriteriaDimension]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0838a6067abe8de6c7ecf339ea0e030fb67dbb47be7286cce2f2d9c9459b9e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c939314914a95bd9d2bbae3c6e4ee9aadd7282da4ed3124a4afe2de7c62f5b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0869a6fc104ccd354a238e7ed4616ce914cbe1ee82b968833b6fdc5e8a66182b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37e5a547e34da74ebda4d174f3c10c7bc9503084ff62d3d3453b4252da01138f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ee8e9e6e13eec078400c26f096fe9b134860f5f40396bd6435e8b1c47f18ef2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorMetricAlertCriteriaDimension]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95d6f45cd28554e84c20c0325cd138690d8e7d498b99122a806131976074c4a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__715f157637a382e6d0cd295d9d22bf66fdba8cbebeb861292a297574b5dd5d6f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eea0c7cfd6f445eddf84a87473b3930a699be844a21c7e214fef08fb965cf19e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9e02b0987f3ae2e253a5d8773e6f320362fd748ff53e0171596ff04298dbe42(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6173389d913f05c5f9b577254721eb26c89276e3f76ca2a60c33e53416c76b4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68ce997850965a2447c1fba197e734d1bbd5b6e0cff986309ecfabe3019960df(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorMetricAlertCriteria]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ce025ff96c8504505a664a5131767c77487100c065c24c5542f6602511cbb7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fa1fd700edb2a5d5f99fc83bc5ec5b792ba572e2bf6ea6545427c115c575e67(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorMetricAlertCriteriaDimension, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b15b1c26ccfa09bf5219f7b842884ed0fca1de04123ab16cc42555af9f05fd5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93ec431bf66b871f74debe293359ca422eb70e83e24e72063ead600d2d3e0509(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c99246dc36f8182217818b2a1ac9c827fe65b56a72b09d3fce0ed0d446fc8be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63f0d337741d15d14483a3f8fcdb19b81eec76340e874d61dbdb397abcff3fda(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d71f0b67686f632db8abe71808fd3d0d4b5c916947d3e424847d866900150b33(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ff29674dc1bb16d32fcd97bd8879b62be44d4c24877dc3ac19077a4c00706cc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60792f056ff64e2229b36c53555ed942131bdfe82cf9a86d3fe1405e9b2af5f2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorMetricAlertCriteria]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13c3d1f4d6af5e9461c3ead61b1ac370f43dad1a30f9ca54e872fb92edcfcdd6(
    *,
    aggregation: builtins.str,
    alert_sensitivity: builtins.str,
    metric_name: builtins.str,
    metric_namespace: builtins.str,
    operator: builtins.str,
    dimension: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorMetricAlertDynamicCriteriaDimension, typing.Dict[builtins.str, typing.Any]]]]] = None,
    evaluation_failure_count: typing.Optional[jsii.Number] = None,
    evaluation_total_count: typing.Optional[jsii.Number] = None,
    ignore_data_before: typing.Optional[builtins.str] = None,
    skip_metric_validation: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3292157cdab70cb9a59eca72bc04e323e568263d296b2d589a2e606087e2a7c9(
    *,
    name: builtins.str,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b583b56e90523b349fb8a1f03381f38ca874c0bcdfed707c910dfcca92915b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03298530059829e17806f389355832287ef14efb1cc411d578704fd12e1499cd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__deec7566200df5c044ce42a017a8e59e913a36f7a58cf3ecce63491dde1a9275(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f7340c95705207a238aae7ec9a204369b3ef4f038b389d7ab3d78f755dd76a5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__494fd3b0cafbd5282abbe06db1a0d0fe4cc4f268b03ef23a146c3cc549a9b157(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a72de36f0fe73ab9f7cd1b66ea6c23d2b7a3a71c71da1baebb23fdb6ed0fb0aa(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorMetricAlertDynamicCriteriaDimension]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c21daa88f5bc4df77bfbac2ed8b35210d46c55b735a90216c6749241c3afa2ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5df00c4fa83308890d643b2692cb4add09e10963c210cc502a5c5c44761e1d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__450a035444835001f18dd28ced8b80626243db018f335143f204ad188f8007d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc435b8993014671ccdd44abc4c008f2bf941079ae8f08f7083ae58e2906cfd9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31a5e80d17878240c4759a707db457a42abb863c4311a50ef671c85bd8ca9e2c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorMetricAlertDynamicCriteriaDimension]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ebb26103bc6890916ba7c7bf46f6b950ed6b914e5565a39d85bc7de0e290628(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73a5d66803e57fa2f69708e4be9ff932ea893c6a2102bd9eb082c1939102ccea(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorMetricAlertDynamicCriteriaDimension, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59b886698c3d9b577d369004188cf2b490ec314ab3327ef72ba7b23c96614204(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b664e26e5a260503d1d9386e8d0139dc089bbc36e674bd0172e65e3c45e918f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df12027e96666019ef53de2ad46899bc0ecf3024708669fe5a58f00a4ad38fdc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24744d9bfe5d05dfb8e3dc2ada540b36e04805b843ad7e9edc36c93d056850db(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__045cc7c400bfe4f103bcb4da5c2254dc3dd1511db46d02120045f777914eda50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e0777a2925f6aa6f0b505c7d74eb846e8112872bfef7309ab5e6852737df481(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__735a67260f2640c191358ad8fc6d63a536971ad874fd010924d3ea706f15d3a7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20af8cb69fa3f05425df85d54782700fe201f1babcf7fbe5c413af871f5886d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb449447aadbfa8048b4a117ffa0ab15d04e6ec6ccc34aed15f6ff8a9944ad4a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e1daf1eddf0ce91b5c4bbff7f91596578caf4ae71df28c3ba94629fe0e05085(
    value: typing.Optional[MonitorMetricAlertDynamicCriteria],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2f7ac6e35e6b7f4922ae4e9090b80fdfb7952395517f46cbd8a1e7f8aecf895(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcc3e0c4479175fc42f93af4859dbeb5d7522b37f7b7ca54982c2dbca2b53037(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9be23d284652b50f4168df661db14b4cfe9b6c7c254e3fb1ba45d061174e24d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cce0c6b0b2616673a11de92eb60b012732065e17bf3c3d473813fdb24a9cbbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ab3c55325999a17fa46ee908689bb966d0ad235c00203cc07d8e4a7dbf7747(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5d9638c35f64cbbea4285049ce9210b4c83464e853de3ccc34bc6fab06ceb71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ba42c72df658b1d04e0fe8283d86b09f418b9d2d15b1b552b0300f577099e9d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorMetricAlertTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
