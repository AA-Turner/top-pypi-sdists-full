r'''
# `newrelic_infra_alert_condition`

Refer to the Terraform Registry for docs: [`newrelic_infra_alert_condition`](https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition).
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


class InfraAlertCondition(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.infraAlertCondition.InfraAlertCondition",
):
    '''Represents a {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition newrelic_infra_alert_condition}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        policy_id: jsii.Number,
        type: builtins.str,
        comparison: typing.Optional[builtins.str] = None,
        critical: typing.Optional[typing.Union["InfraAlertConditionCritical", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        event: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        integration_provider: typing.Optional[builtins.str] = None,
        process_where: typing.Optional[builtins.str] = None,
        runbook_url: typing.Optional[builtins.str] = None,
        select: typing.Optional[builtins.str] = None,
        violation_close_timer: typing.Optional[jsii.Number] = None,
        warning: typing.Optional[typing.Union["InfraAlertConditionWarning", typing.Dict[builtins.str, typing.Any]]] = None,
        where: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition newrelic_infra_alert_condition} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: The Infrastructure alert condition's name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#name InfraAlertCondition#name}
        :param policy_id: The ID of the alert policy where this condition should be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#policy_id InfraAlertCondition#policy_id}
        :param type: The type of Infrastructure alert condition. Valid values are infra_process_running, infra_metric, and infra_host_not_reporting. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#type InfraAlertCondition#type}
        :param comparison: The operator used to evaluate the threshold value. Valid values are above, below, and equal. Supported by the infra_metric and infra_process_running condition types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#comparison InfraAlertCondition#comparison}
        :param critical: critical block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#critical InfraAlertCondition#critical}
        :param description: The description of the Infrastructure alert condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#description InfraAlertCondition#description}
        :param enabled: Whether the condition is turned on or off. Valid values are true and false. Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#enabled InfraAlertCondition#enabled}
        :param event: The metric event; for example, SystemSample or StorageSample. Supported by the infra_metric condition type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#event InfraAlertCondition#event}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#id InfraAlertCondition#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param integration_provider: For alerts on integrations, use this instead of event. Supported by the infra_metric condition type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#integration_provider InfraAlertCondition#integration_provider}
        :param process_where: Any filters applied to processes; for example: commandName = 'java'. Supported by the infra_process_running condition type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#process_where InfraAlertCondition#process_where}
        :param runbook_url: Runbook URL to display in notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#runbook_url InfraAlertCondition#runbook_url}
        :param select: The attribute name to identify the metric being targeted; for example, cpuPercent, diskFreePercent, or memoryResidentSizeBytes. The underlying API will automatically populate this value for Infrastructure integrations (for example diskFreePercent), so make sure to explicitly include this value to avoid diff issues. Supported by the infra_metric condition type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#select InfraAlertCondition#select}
        :param violation_close_timer: Determines how much time, in hours, will pass before an incident is automatically closed. Valid values are 1, 2, 4, 8, 12, 24, 48, or 72 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#violation_close_timer InfraAlertCondition#violation_close_timer}
        :param warning: warning block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#warning InfraAlertCondition#warning}
        :param where: If applicable, this identifies any Infrastructure host filters used; for example: hostname LIKE '%cassandra%'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#where InfraAlertCondition#where}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecf785162ae09f0fa002a7e14d143948463d51adac1d4c6c3ad782b2dff251c6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = InfraAlertConditionConfig(
            name=name,
            policy_id=policy_id,
            type=type,
            comparison=comparison,
            critical=critical,
            description=description,
            enabled=enabled,
            event=event,
            id=id,
            integration_provider=integration_provider,
            process_where=process_where,
            runbook_url=runbook_url,
            select=select,
            violation_close_timer=violation_close_timer,
            warning=warning,
            where=where,
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
        '''Generates CDKTF code for importing a InfraAlertCondition resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the InfraAlertCondition to import.
        :param import_from_id: The id of the existing InfraAlertCondition that should be imported. Refer to the {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the InfraAlertCondition to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b85ed163e27faabb2ab406a839b7de0cf548d2d918a0a5b9da13bc16a88061ac)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCritical")
    def put_critical(
        self,
        *,
        duration: jsii.Number,
        time_function: typing.Optional[builtins.str] = None,
        value: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#duration InfraAlertCondition#duration}.
        :param time_function: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#time_function InfraAlertCondition#time_function}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#value InfraAlertCondition#value}.
        '''
        value_ = InfraAlertConditionCritical(
            duration=duration, time_function=time_function, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putCritical", [value_]))

    @jsii.member(jsii_name="putWarning")
    def put_warning(
        self,
        *,
        duration: jsii.Number,
        time_function: typing.Optional[builtins.str] = None,
        value: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#duration InfraAlertCondition#duration}.
        :param time_function: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#time_function InfraAlertCondition#time_function}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#value InfraAlertCondition#value}.
        '''
        value_ = InfraAlertConditionWarning(
            duration=duration, time_function=time_function, value=value
        )

        return typing.cast(None, jsii.invoke(self, "putWarning", [value_]))

    @jsii.member(jsii_name="resetComparison")
    def reset_comparison(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetComparison", []))

    @jsii.member(jsii_name="resetCritical")
    def reset_critical(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCritical", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetEvent")
    def reset_event(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEvent", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIntegrationProvider")
    def reset_integration_provider(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntegrationProvider", []))

    @jsii.member(jsii_name="resetProcessWhere")
    def reset_process_where(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProcessWhere", []))

    @jsii.member(jsii_name="resetRunbookUrl")
    def reset_runbook_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRunbookUrl", []))

    @jsii.member(jsii_name="resetSelect")
    def reset_select(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSelect", []))

    @jsii.member(jsii_name="resetViolationCloseTimer")
    def reset_violation_close_timer(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetViolationCloseTimer", []))

    @jsii.member(jsii_name="resetWarning")
    def reset_warning(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWarning", []))

    @jsii.member(jsii_name="resetWhere")
    def reset_where(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWhere", []))

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
    @jsii.member(jsii_name="createdAt")
    def created_at(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="critical")
    def critical(self) -> "InfraAlertConditionCriticalOutputReference":
        return typing.cast("InfraAlertConditionCriticalOutputReference", jsii.get(self, "critical"))

    @builtins.property
    @jsii.member(jsii_name="entityGuid")
    def entity_guid(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "entityGuid"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="warning")
    def warning(self) -> "InfraAlertConditionWarningOutputReference":
        return typing.cast("InfraAlertConditionWarningOutputReference", jsii.get(self, "warning"))

    @builtins.property
    @jsii.member(jsii_name="comparisonInput")
    def comparison_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comparisonInput"))

    @builtins.property
    @jsii.member(jsii_name="criticalInput")
    def critical_input(self) -> typing.Optional["InfraAlertConditionCritical"]:
        return typing.cast(typing.Optional["InfraAlertConditionCritical"], jsii.get(self, "criticalInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="eventInput")
    def event_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="integrationProviderInput")
    def integration_provider_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "integrationProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="policyIdInput")
    def policy_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "policyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="processWhereInput")
    def process_where_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "processWhereInput"))

    @builtins.property
    @jsii.member(jsii_name="runbookUrlInput")
    def runbook_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "runbookUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="selectInput")
    def select_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "selectInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="violationCloseTimerInput")
    def violation_close_timer_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "violationCloseTimerInput"))

    @builtins.property
    @jsii.member(jsii_name="warningInput")
    def warning_input(self) -> typing.Optional["InfraAlertConditionWarning"]:
        return typing.cast(typing.Optional["InfraAlertConditionWarning"], jsii.get(self, "warningInput"))

    @builtins.property
    @jsii.member(jsii_name="whereInput")
    def where_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "whereInput"))

    @builtins.property
    @jsii.member(jsii_name="comparison")
    def comparison(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "comparison"))

    @comparison.setter
    def comparison(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9576f891a6141e60904897cecccd21442b0bb21a352b52b73ca6048d7710ade4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "comparison", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97b0edd4f16e06f3cfc2c14617cd28cd1aeb8632cd3e288748020c8cf7379cd3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f8d69ce7d2f1093f6413ea1774f02f7e409352a7b6bb3832194e80d7d473737)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="event")
    def event(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "event"))

    @event.setter
    def event(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac829794a69a83554ccb0cccc54319cf874721190c4f3df4f182a9c6a691ad32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "event", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d58f172e03ad5221534389d17cda7e2c7716666b8e315643f46ed958e0c5101f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="integrationProvider")
    def integration_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "integrationProvider"))

    @integration_provider.setter
    def integration_provider(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2c2df077beb4169f725ff3675630d5d085062179362b68cebfbbcaa0a6a5dbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationProvider", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ef18ff8ded58a18f32489d473d611198132dadfaf94fc03e4132fbd0c2642cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="policyId")
    def policy_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "policyId"))

    @policy_id.setter
    def policy_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f5af5e3aff43c749fbeb1226a2d6a5650af9a4513f91bf7529dd20899a5307a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="processWhere")
    def process_where(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "processWhere"))

    @process_where.setter
    def process_where(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5896a401aa513d48c2100e856ebd255c398d1008cdb17b26b9b183f038a97a5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "processWhere", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="runbookUrl")
    def runbook_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "runbookUrl"))

    @runbook_url.setter
    def runbook_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc353ce2e0f8de12ae030ab441b6db5b9c46ded19d6932bd3aef17b9c99d2801)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "runbookUrl", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="select")
    def select(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "select"))

    @select.setter
    def select(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb0fd209382c41d7859015318a9bca3198cfefd2f1ce7fe28cdc17079cc7516c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "select", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa89b7ef2a9af7610fe6404af810275944fa53ada8ec3404a4d93e08eefa6796)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="violationCloseTimer")
    def violation_close_timer(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "violationCloseTimer"))

    @violation_close_timer.setter
    def violation_close_timer(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1325d16db02567c34fb7bc7ba1fb5c86684d508ffd9974ae04d00d984729c45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "violationCloseTimer", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="where")
    def where(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "where"))

    @where.setter
    def where(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d65f55505e19d0f1376ad9f1c1fdcb5a7f2b4b92e5819f1d7ce3369b50e2616c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "where", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.infraAlertCondition.InfraAlertConditionConfig",
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
        "policy_id": "policyId",
        "type": "type",
        "comparison": "comparison",
        "critical": "critical",
        "description": "description",
        "enabled": "enabled",
        "event": "event",
        "id": "id",
        "integration_provider": "integrationProvider",
        "process_where": "processWhere",
        "runbook_url": "runbookUrl",
        "select": "select",
        "violation_close_timer": "violationCloseTimer",
        "warning": "warning",
        "where": "where",
    },
)
class InfraAlertConditionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        policy_id: jsii.Number,
        type: builtins.str,
        comparison: typing.Optional[builtins.str] = None,
        critical: typing.Optional[typing.Union["InfraAlertConditionCritical", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        event: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        integration_provider: typing.Optional[builtins.str] = None,
        process_where: typing.Optional[builtins.str] = None,
        runbook_url: typing.Optional[builtins.str] = None,
        select: typing.Optional[builtins.str] = None,
        violation_close_timer: typing.Optional[jsii.Number] = None,
        warning: typing.Optional[typing.Union["InfraAlertConditionWarning", typing.Dict[builtins.str, typing.Any]]] = None,
        where: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: The Infrastructure alert condition's name. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#name InfraAlertCondition#name}
        :param policy_id: The ID of the alert policy where this condition should be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#policy_id InfraAlertCondition#policy_id}
        :param type: The type of Infrastructure alert condition. Valid values are infra_process_running, infra_metric, and infra_host_not_reporting. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#type InfraAlertCondition#type}
        :param comparison: The operator used to evaluate the threshold value. Valid values are above, below, and equal. Supported by the infra_metric and infra_process_running condition types. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#comparison InfraAlertCondition#comparison}
        :param critical: critical block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#critical InfraAlertCondition#critical}
        :param description: The description of the Infrastructure alert condition. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#description InfraAlertCondition#description}
        :param enabled: Whether the condition is turned on or off. Valid values are true and false. Defaults to true. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#enabled InfraAlertCondition#enabled}
        :param event: The metric event; for example, SystemSample or StorageSample. Supported by the infra_metric condition type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#event InfraAlertCondition#event}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#id InfraAlertCondition#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param integration_provider: For alerts on integrations, use this instead of event. Supported by the infra_metric condition type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#integration_provider InfraAlertCondition#integration_provider}
        :param process_where: Any filters applied to processes; for example: commandName = 'java'. Supported by the infra_process_running condition type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#process_where InfraAlertCondition#process_where}
        :param runbook_url: Runbook URL to display in notifications. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#runbook_url InfraAlertCondition#runbook_url}
        :param select: The attribute name to identify the metric being targeted; for example, cpuPercent, diskFreePercent, or memoryResidentSizeBytes. The underlying API will automatically populate this value for Infrastructure integrations (for example diskFreePercent), so make sure to explicitly include this value to avoid diff issues. Supported by the infra_metric condition type. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#select InfraAlertCondition#select}
        :param violation_close_timer: Determines how much time, in hours, will pass before an incident is automatically closed. Valid values are 1, 2, 4, 8, 12, 24, 48, or 72 Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#violation_close_timer InfraAlertCondition#violation_close_timer}
        :param warning: warning block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#warning InfraAlertCondition#warning}
        :param where: If applicable, this identifies any Infrastructure host filters used; for example: hostname LIKE '%cassandra%'. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#where InfraAlertCondition#where}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(critical, dict):
            critical = InfraAlertConditionCritical(**critical)
        if isinstance(warning, dict):
            warning = InfraAlertConditionWarning(**warning)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d5da1b3bc5738700eb833da9ab9b90648cc906ef3af73fc78b0a44f2135ef05)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument policy_id", value=policy_id, expected_type=type_hints["policy_id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument comparison", value=comparison, expected_type=type_hints["comparison"])
            check_type(argname="argument critical", value=critical, expected_type=type_hints["critical"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument event", value=event, expected_type=type_hints["event"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument integration_provider", value=integration_provider, expected_type=type_hints["integration_provider"])
            check_type(argname="argument process_where", value=process_where, expected_type=type_hints["process_where"])
            check_type(argname="argument runbook_url", value=runbook_url, expected_type=type_hints["runbook_url"])
            check_type(argname="argument select", value=select, expected_type=type_hints["select"])
            check_type(argname="argument violation_close_timer", value=violation_close_timer, expected_type=type_hints["violation_close_timer"])
            check_type(argname="argument warning", value=warning, expected_type=type_hints["warning"])
            check_type(argname="argument where", value=where, expected_type=type_hints["where"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "policy_id": policy_id,
            "type": type,
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
        if comparison is not None:
            self._values["comparison"] = comparison
        if critical is not None:
            self._values["critical"] = critical
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if event is not None:
            self._values["event"] = event
        if id is not None:
            self._values["id"] = id
        if integration_provider is not None:
            self._values["integration_provider"] = integration_provider
        if process_where is not None:
            self._values["process_where"] = process_where
        if runbook_url is not None:
            self._values["runbook_url"] = runbook_url
        if select is not None:
            self._values["select"] = select
        if violation_close_timer is not None:
            self._values["violation_close_timer"] = violation_close_timer
        if warning is not None:
            self._values["warning"] = warning
        if where is not None:
            self._values["where"] = where

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
        '''The Infrastructure alert condition's name.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#name InfraAlertCondition#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def policy_id(self) -> jsii.Number:
        '''The ID of the alert policy where this condition should be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#policy_id InfraAlertCondition#policy_id}
        '''
        result = self._values.get("policy_id")
        assert result is not None, "Required property 'policy_id' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of Infrastructure alert condition. Valid values are infra_process_running, infra_metric, and infra_host_not_reporting.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#type InfraAlertCondition#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def comparison(self) -> typing.Optional[builtins.str]:
        '''The operator used to evaluate the threshold value.

        Valid values are above, below, and equal. Supported by the infra_metric and infra_process_running condition types.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#comparison InfraAlertCondition#comparison}
        '''
        result = self._values.get("comparison")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def critical(self) -> typing.Optional["InfraAlertConditionCritical"]:
        '''critical block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#critical InfraAlertCondition#critical}
        '''
        result = self._values.get("critical")
        return typing.cast(typing.Optional["InfraAlertConditionCritical"], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the Infrastructure alert condition.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#description InfraAlertCondition#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether the condition is turned on or off. Valid values are true and false. Defaults to true.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#enabled InfraAlertCondition#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def event(self) -> typing.Optional[builtins.str]:
        '''The metric event; for example, SystemSample or StorageSample. Supported by the infra_metric condition type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#event InfraAlertCondition#event}
        '''
        result = self._values.get("event")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#id InfraAlertCondition#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def integration_provider(self) -> typing.Optional[builtins.str]:
        '''For alerts on integrations, use this instead of event. Supported by the infra_metric condition type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#integration_provider InfraAlertCondition#integration_provider}
        '''
        result = self._values.get("integration_provider")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def process_where(self) -> typing.Optional[builtins.str]:
        '''Any filters applied to processes; for example: commandName = 'java'. Supported by the infra_process_running condition type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#process_where InfraAlertCondition#process_where}
        '''
        result = self._values.get("process_where")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runbook_url(self) -> typing.Optional[builtins.str]:
        '''Runbook URL to display in notifications.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#runbook_url InfraAlertCondition#runbook_url}
        '''
        result = self._values.get("runbook_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def select(self) -> typing.Optional[builtins.str]:
        '''The attribute name to identify the metric being targeted;

        for example, cpuPercent, diskFreePercent, or memoryResidentSizeBytes. The underlying API will automatically populate this value for Infrastructure integrations (for example diskFreePercent), so make sure to explicitly include this value to avoid diff issues. Supported by the infra_metric condition type.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#select InfraAlertCondition#select}
        '''
        result = self._values.get("select")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def violation_close_timer(self) -> typing.Optional[jsii.Number]:
        '''Determines how much time, in hours, will pass before an incident is automatically closed.

        Valid values are 1, 2, 4, 8, 12, 24, 48, or 72

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#violation_close_timer InfraAlertCondition#violation_close_timer}
        '''
        result = self._values.get("violation_close_timer")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def warning(self) -> typing.Optional["InfraAlertConditionWarning"]:
        '''warning block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#warning InfraAlertCondition#warning}
        '''
        result = self._values.get("warning")
        return typing.cast(typing.Optional["InfraAlertConditionWarning"], result)

    @builtins.property
    def where(self) -> typing.Optional[builtins.str]:
        '''If applicable, this identifies any Infrastructure host filters used; for example: hostname LIKE '%cassandra%'.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#where InfraAlertCondition#where}
        '''
        result = self._values.get("where")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InfraAlertConditionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.infraAlertCondition.InfraAlertConditionCritical",
    jsii_struct_bases=[],
    name_mapping={
        "duration": "duration",
        "time_function": "timeFunction",
        "value": "value",
    },
)
class InfraAlertConditionCritical:
    def __init__(
        self,
        *,
        duration: jsii.Number,
        time_function: typing.Optional[builtins.str] = None,
        value: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#duration InfraAlertCondition#duration}.
        :param time_function: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#time_function InfraAlertCondition#time_function}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#value InfraAlertCondition#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7296760f72a4c0211f75374f9d66ff404e5b40874fa56eed8c0e564c69b9daeb)
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
            check_type(argname="argument time_function", value=time_function, expected_type=type_hints["time_function"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "duration": duration,
        }
        if time_function is not None:
            self._values["time_function"] = time_function
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def duration(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#duration InfraAlertCondition#duration}.'''
        result = self._values.get("duration")
        assert result is not None, "Required property 'duration' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def time_function(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#time_function InfraAlertCondition#time_function}.'''
        result = self._values.get("time_function")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#value InfraAlertCondition#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InfraAlertConditionCritical(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class InfraAlertConditionCriticalOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.infraAlertCondition.InfraAlertConditionCriticalOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b50f2e18cbb81a4e8c062bec8994c607dc98c5c6af0fde9de86c87aa9494e92)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTimeFunction")
    def reset_time_function(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeFunction", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="durationInput")
    def duration_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "durationInput"))

    @builtins.property
    @jsii.member(jsii_name="timeFunctionInput")
    def time_function_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeFunctionInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "duration"))

    @duration.setter
    def duration(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7609435dc0e7970176528250934edf38406ba7a2efd751fc4cdc942cf0663069)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeFunction")
    def time_function(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeFunction"))

    @time_function.setter
    def time_function(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1657fb7adcf04afaac17b982cfffbd36ae2e9c224733397f358b662f46ce5a7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeFunction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5097b2b0c8664772da5ef5d4ce9e67713a879489d6d241ee2734793a12011de6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[InfraAlertConditionCritical]:
        return typing.cast(typing.Optional[InfraAlertConditionCritical], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[InfraAlertConditionCritical],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f88a8c591a7e2002aaff69703ed863373382373992daa4afe4a579299cddf2e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.infraAlertCondition.InfraAlertConditionWarning",
    jsii_struct_bases=[],
    name_mapping={
        "duration": "duration",
        "time_function": "timeFunction",
        "value": "value",
    },
)
class InfraAlertConditionWarning:
    def __init__(
        self,
        *,
        duration: jsii.Number,
        time_function: typing.Optional[builtins.str] = None,
        value: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#duration InfraAlertCondition#duration}.
        :param time_function: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#time_function InfraAlertCondition#time_function}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#value InfraAlertCondition#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5e07f2290f7788a889de4e4869c793e946a660ecede10497ba45ec8bb49b1b3)
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
            check_type(argname="argument time_function", value=time_function, expected_type=type_hints["time_function"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "duration": duration,
        }
        if time_function is not None:
            self._values["time_function"] = time_function
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def duration(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#duration InfraAlertCondition#duration}.'''
        result = self._values.get("duration")
        assert result is not None, "Required property 'duration' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def time_function(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#time_function InfraAlertCondition#time_function}.'''
        result = self._values.get("time_function")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/infra_alert_condition#value InfraAlertCondition#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InfraAlertConditionWarning(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class InfraAlertConditionWarningOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.infraAlertCondition.InfraAlertConditionWarningOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__15b63a5f6915bf5f22c5f5c2bb9ab12f4bc8da99f967e60f0692b88529b95753)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTimeFunction")
    def reset_time_function(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeFunction", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="durationInput")
    def duration_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "durationInput"))

    @builtins.property
    @jsii.member(jsii_name="timeFunctionInput")
    def time_function_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeFunctionInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "duration"))

    @duration.setter
    def duration(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__160294fd684c60ca823dc4d0719b821fb1bbb338a09ee4d81e90624b87ef4325)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeFunction")
    def time_function(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeFunction"))

    @time_function.setter
    def time_function(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45a5f4563ebead0b744e16095ed84a63137525cd0e1a7576f7823bc677628cec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeFunction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24cea1e04857204254cfce82c5932a95f53284ee35b52578d2d734906315b21b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[InfraAlertConditionWarning]:
        return typing.cast(typing.Optional[InfraAlertConditionWarning], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[InfraAlertConditionWarning],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4538f9b4361b0dcf47b8e61dc71b728cdc9e05fa6599e343739bf2368f90bf01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "InfraAlertCondition",
    "InfraAlertConditionConfig",
    "InfraAlertConditionCritical",
    "InfraAlertConditionCriticalOutputReference",
    "InfraAlertConditionWarning",
    "InfraAlertConditionWarningOutputReference",
]

publication.publish()

def _typecheckingstub__ecf785162ae09f0fa002a7e14d143948463d51adac1d4c6c3ad782b2dff251c6(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    policy_id: jsii.Number,
    type: builtins.str,
    comparison: typing.Optional[builtins.str] = None,
    critical: typing.Optional[typing.Union[InfraAlertConditionCritical, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    event: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    integration_provider: typing.Optional[builtins.str] = None,
    process_where: typing.Optional[builtins.str] = None,
    runbook_url: typing.Optional[builtins.str] = None,
    select: typing.Optional[builtins.str] = None,
    violation_close_timer: typing.Optional[jsii.Number] = None,
    warning: typing.Optional[typing.Union[InfraAlertConditionWarning, typing.Dict[builtins.str, typing.Any]]] = None,
    where: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__b85ed163e27faabb2ab406a839b7de0cf548d2d918a0a5b9da13bc16a88061ac(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9576f891a6141e60904897cecccd21442b0bb21a352b52b73ca6048d7710ade4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97b0edd4f16e06f3cfc2c14617cd28cd1aeb8632cd3e288748020c8cf7379cd3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f8d69ce7d2f1093f6413ea1774f02f7e409352a7b6bb3832194e80d7d473737(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac829794a69a83554ccb0cccc54319cf874721190c4f3df4f182a9c6a691ad32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d58f172e03ad5221534389d17cda7e2c7716666b8e315643f46ed958e0c5101f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2c2df077beb4169f725ff3675630d5d085062179362b68cebfbbcaa0a6a5dbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ef18ff8ded58a18f32489d473d611198132dadfaf94fc03e4132fbd0c2642cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f5af5e3aff43c749fbeb1226a2d6a5650af9a4513f91bf7529dd20899a5307a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5896a401aa513d48c2100e856ebd255c398d1008cdb17b26b9b183f038a97a5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc353ce2e0f8de12ae030ab441b6db5b9c46ded19d6932bd3aef17b9c99d2801(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb0fd209382c41d7859015318a9bca3198cfefd2f1ce7fe28cdc17079cc7516c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa89b7ef2a9af7610fe6404af810275944fa53ada8ec3404a4d93e08eefa6796(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1325d16db02567c34fb7bc7ba1fb5c86684d508ffd9974ae04d00d984729c45(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d65f55505e19d0f1376ad9f1c1fdcb5a7f2b4b92e5819f1d7ce3369b50e2616c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d5da1b3bc5738700eb833da9ab9b90648cc906ef3af73fc78b0a44f2135ef05(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    policy_id: jsii.Number,
    type: builtins.str,
    comparison: typing.Optional[builtins.str] = None,
    critical: typing.Optional[typing.Union[InfraAlertConditionCritical, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    event: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    integration_provider: typing.Optional[builtins.str] = None,
    process_where: typing.Optional[builtins.str] = None,
    runbook_url: typing.Optional[builtins.str] = None,
    select: typing.Optional[builtins.str] = None,
    violation_close_timer: typing.Optional[jsii.Number] = None,
    warning: typing.Optional[typing.Union[InfraAlertConditionWarning, typing.Dict[builtins.str, typing.Any]]] = None,
    where: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7296760f72a4c0211f75374f9d66ff404e5b40874fa56eed8c0e564c69b9daeb(
    *,
    duration: jsii.Number,
    time_function: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b50f2e18cbb81a4e8c062bec8994c607dc98c5c6af0fde9de86c87aa9494e92(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7609435dc0e7970176528250934edf38406ba7a2efd751fc4cdc942cf0663069(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1657fb7adcf04afaac17b982cfffbd36ae2e9c224733397f358b662f46ce5a7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5097b2b0c8664772da5ef5d4ce9e67713a879489d6d241ee2734793a12011de6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f88a8c591a7e2002aaff69703ed863373382373992daa4afe4a579299cddf2e9(
    value: typing.Optional[InfraAlertConditionCritical],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5e07f2290f7788a889de4e4869c793e946a660ecede10497ba45ec8bb49b1b3(
    *,
    duration: jsii.Number,
    time_function: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15b63a5f6915bf5f22c5f5c2bb9ab12f4bc8da99f967e60f0692b88529b95753(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__160294fd684c60ca823dc4d0719b821fb1bbb338a09ee4d81e90624b87ef4325(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45a5f4563ebead0b744e16095ed84a63137525cd0e1a7576f7823bc677628cec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24cea1e04857204254cfce82c5932a95f53284ee35b52578d2d734906315b21b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4538f9b4361b0dcf47b8e61dc71b728cdc9e05fa6599e343739bf2368f90bf01(
    value: typing.Optional[InfraAlertConditionWarning],
) -> None:
    """Type checking stubs"""
    pass
