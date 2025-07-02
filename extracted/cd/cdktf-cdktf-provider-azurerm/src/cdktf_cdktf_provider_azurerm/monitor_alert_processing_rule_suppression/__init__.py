r'''
# `azurerm_monitor_alert_processing_rule_suppression`

Refer to the Terraform Registry for docs: [`azurerm_monitor_alert_processing_rule_suppression`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression).
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


class MonitorAlertProcessingRuleSuppression(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppression",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression azurerm_monitor_alert_processing_rule_suppression}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        resource_group_name: builtins.str,
        scopes: typing.Sequence[builtins.str],
        condition: typing.Optional[typing.Union["MonitorAlertProcessingRuleSuppressionCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[typing.Union["MonitorAlertProcessingRuleSuppressionSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MonitorAlertProcessingRuleSuppressionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression azurerm_monitor_alert_processing_rule_suppression} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#name MonitorAlertProcessingRuleSuppression#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#resource_group_name MonitorAlertProcessingRuleSuppression#resource_group_name}.
        :param scopes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#scopes MonitorAlertProcessingRuleSuppression#scopes}.
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#condition MonitorAlertProcessingRuleSuppression#condition}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#description MonitorAlertProcessingRuleSuppression#description}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#enabled MonitorAlertProcessingRuleSuppression#enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#id MonitorAlertProcessingRuleSuppression#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#schedule MonitorAlertProcessingRuleSuppression#schedule}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#tags MonitorAlertProcessingRuleSuppression#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#timeouts MonitorAlertProcessingRuleSuppression#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2d21e765cf429c7c82ff06f1cdf4bb9029f079eacbd9616564e99d612766be1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MonitorAlertProcessingRuleSuppressionConfig(
            name=name,
            resource_group_name=resource_group_name,
            scopes=scopes,
            condition=condition,
            description=description,
            enabled=enabled,
            id=id,
            schedule=schedule,
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
        '''Generates CDKTF code for importing a MonitorAlertProcessingRuleSuppression resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MonitorAlertProcessingRuleSuppression to import.
        :param import_from_id: The id of the existing MonitorAlertProcessingRuleSuppression that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MonitorAlertProcessingRuleSuppression to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df753cd385f27b209508fca60e94846350fd98b431143167e6b7da4e3369cdcb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCondition")
    def put_condition(
        self,
        *,
        alert_context: typing.Optional[typing.Union["MonitorAlertProcessingRuleSuppressionConditionAlertContext", typing.Dict[builtins.str, typing.Any]]] = None,
        alert_rule_id: typing.Optional[typing.Union["MonitorAlertProcessingRuleSuppressionConditionAlertRuleId", typing.Dict[builtins.str, typing.Any]]] = None,
        alert_rule_name: typing.Optional[typing.Union["MonitorAlertProcessingRuleSuppressionConditionAlertRuleName", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[typing.Union["MonitorAlertProcessingRuleSuppressionConditionDescription", typing.Dict[builtins.str, typing.Any]]] = None,
        monitor_condition: typing.Optional[typing.Union["MonitorAlertProcessingRuleSuppressionConditionMonitorCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        monitor_service: typing.Optional[typing.Union["MonitorAlertProcessingRuleSuppressionConditionMonitorService", typing.Dict[builtins.str, typing.Any]]] = None,
        severity: typing.Optional[typing.Union["MonitorAlertProcessingRuleSuppressionConditionSeverity", typing.Dict[builtins.str, typing.Any]]] = None,
        signal_type: typing.Optional[typing.Union["MonitorAlertProcessingRuleSuppressionConditionSignalType", typing.Dict[builtins.str, typing.Any]]] = None,
        target_resource: typing.Optional[typing.Union["MonitorAlertProcessingRuleSuppressionConditionTargetResource", typing.Dict[builtins.str, typing.Any]]] = None,
        target_resource_group: typing.Optional[typing.Union["MonitorAlertProcessingRuleSuppressionConditionTargetResourceGroup", typing.Dict[builtins.str, typing.Any]]] = None,
        target_resource_type: typing.Optional[typing.Union["MonitorAlertProcessingRuleSuppressionConditionTargetResourceType", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param alert_context: alert_context block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#alert_context MonitorAlertProcessingRuleSuppression#alert_context}
        :param alert_rule_id: alert_rule_id block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#alert_rule_id MonitorAlertProcessingRuleSuppression#alert_rule_id}
        :param alert_rule_name: alert_rule_name block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#alert_rule_name MonitorAlertProcessingRuleSuppression#alert_rule_name}
        :param description: description block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#description MonitorAlertProcessingRuleSuppression#description}
        :param monitor_condition: monitor_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#monitor_condition MonitorAlertProcessingRuleSuppression#monitor_condition}
        :param monitor_service: monitor_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#monitor_service MonitorAlertProcessingRuleSuppression#monitor_service}
        :param severity: severity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#severity MonitorAlertProcessingRuleSuppression#severity}
        :param signal_type: signal_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#signal_type MonitorAlertProcessingRuleSuppression#signal_type}
        :param target_resource: target_resource block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#target_resource MonitorAlertProcessingRuleSuppression#target_resource}
        :param target_resource_group: target_resource_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#target_resource_group MonitorAlertProcessingRuleSuppression#target_resource_group}
        :param target_resource_type: target_resource_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#target_resource_type MonitorAlertProcessingRuleSuppression#target_resource_type}
        '''
        value = MonitorAlertProcessingRuleSuppressionCondition(
            alert_context=alert_context,
            alert_rule_id=alert_rule_id,
            alert_rule_name=alert_rule_name,
            description=description,
            monitor_condition=monitor_condition,
            monitor_service=monitor_service,
            severity=severity,
            signal_type=signal_type,
            target_resource=target_resource,
            target_resource_group=target_resource_group,
            target_resource_type=target_resource_type,
        )

        return typing.cast(None, jsii.invoke(self, "putCondition", [value]))

    @jsii.member(jsii_name="putSchedule")
    def put_schedule(
        self,
        *,
        effective_from: typing.Optional[builtins.str] = None,
        effective_until: typing.Optional[builtins.str] = None,
        recurrence: typing.Optional[typing.Union["MonitorAlertProcessingRuleSuppressionScheduleRecurrence", typing.Dict[builtins.str, typing.Any]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param effective_from: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#effective_from MonitorAlertProcessingRuleSuppression#effective_from}.
        :param effective_until: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#effective_until MonitorAlertProcessingRuleSuppression#effective_until}.
        :param recurrence: recurrence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#recurrence MonitorAlertProcessingRuleSuppression#recurrence}
        :param time_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#time_zone MonitorAlertProcessingRuleSuppression#time_zone}.
        '''
        value = MonitorAlertProcessingRuleSuppressionSchedule(
            effective_from=effective_from,
            effective_until=effective_until,
            recurrence=recurrence,
            time_zone=time_zone,
        )

        return typing.cast(None, jsii.invoke(self, "putSchedule", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#create MonitorAlertProcessingRuleSuppression#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#delete MonitorAlertProcessingRuleSuppression#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#read MonitorAlertProcessingRuleSuppression#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#update MonitorAlertProcessingRuleSuppression#update}.
        '''
        value = MonitorAlertProcessingRuleSuppressionTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCondition")
    def reset_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCondition", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetSchedule")
    def reset_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedule", []))

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
    @jsii.member(jsii_name="condition")
    def condition(
        self,
    ) -> "MonitorAlertProcessingRuleSuppressionConditionOutputReference":
        return typing.cast("MonitorAlertProcessingRuleSuppressionConditionOutputReference", jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(
        self,
    ) -> "MonitorAlertProcessingRuleSuppressionScheduleOutputReference":
        return typing.cast("MonitorAlertProcessingRuleSuppressionScheduleOutputReference", jsii.get(self, "schedule"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "MonitorAlertProcessingRuleSuppressionTimeoutsOutputReference":
        return typing.cast("MonitorAlertProcessingRuleSuppressionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleSuppressionCondition"]:
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleSuppressionCondition"], jsii.get(self, "conditionInput"))

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
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleSuppressionSchedule"]:
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleSuppressionSchedule"], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="scopesInput")
    def scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scopesInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MonitorAlertProcessingRuleSuppressionTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MonitorAlertProcessingRuleSuppressionTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__575b6602c5832bdb6f2f3c23dab7ab87b1e921adc5024994090d99b20d6007a0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0730fa8f874fc56e0b0a3890a44cfba682cfa36635a84b070cbf70e30f5bbf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b647b757c8a7248238e1f0dacbcc4c7213876daf314d455c4890fbe6da169a96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2012d1d3c30ccd50c83f2b5d0d97e3277a2b4e6b8b6a0515e8c183e55b70409)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c806e23a117dffccf9737258908a893cb0d6751b216fdf67250b08792f7251eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scopes"))

    @scopes.setter
    def scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__973aee75c58c71b97d99d8943c3af1ad12c3ac01e22219ce9b62a8c1a4e47e11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__212d4fcb91792d5e85efcc8cfb10fa50421f4e3be711b9b357ac93dca91cc44d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionCondition",
    jsii_struct_bases=[],
    name_mapping={
        "alert_context": "alertContext",
        "alert_rule_id": "alertRuleId",
        "alert_rule_name": "alertRuleName",
        "description": "description",
        "monitor_condition": "monitorCondition",
        "monitor_service": "monitorService",
        "severity": "severity",
        "signal_type": "signalType",
        "target_resource": "targetResource",
        "target_resource_group": "targetResourceGroup",
        "target_resource_type": "targetResourceType",
    },
)
class MonitorAlertProcessingRuleSuppressionCondition:
    def __init__(
        self,
        *,
        alert_context: typing.Optional[typing.Union["MonitorAlertProcessingRuleSuppressionConditionAlertContext", typing.Dict[builtins.str, typing.Any]]] = None,
        alert_rule_id: typing.Optional[typing.Union["MonitorAlertProcessingRuleSuppressionConditionAlertRuleId", typing.Dict[builtins.str, typing.Any]]] = None,
        alert_rule_name: typing.Optional[typing.Union["MonitorAlertProcessingRuleSuppressionConditionAlertRuleName", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[typing.Union["MonitorAlertProcessingRuleSuppressionConditionDescription", typing.Dict[builtins.str, typing.Any]]] = None,
        monitor_condition: typing.Optional[typing.Union["MonitorAlertProcessingRuleSuppressionConditionMonitorCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        monitor_service: typing.Optional[typing.Union["MonitorAlertProcessingRuleSuppressionConditionMonitorService", typing.Dict[builtins.str, typing.Any]]] = None,
        severity: typing.Optional[typing.Union["MonitorAlertProcessingRuleSuppressionConditionSeverity", typing.Dict[builtins.str, typing.Any]]] = None,
        signal_type: typing.Optional[typing.Union["MonitorAlertProcessingRuleSuppressionConditionSignalType", typing.Dict[builtins.str, typing.Any]]] = None,
        target_resource: typing.Optional[typing.Union["MonitorAlertProcessingRuleSuppressionConditionTargetResource", typing.Dict[builtins.str, typing.Any]]] = None,
        target_resource_group: typing.Optional[typing.Union["MonitorAlertProcessingRuleSuppressionConditionTargetResourceGroup", typing.Dict[builtins.str, typing.Any]]] = None,
        target_resource_type: typing.Optional[typing.Union["MonitorAlertProcessingRuleSuppressionConditionTargetResourceType", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param alert_context: alert_context block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#alert_context MonitorAlertProcessingRuleSuppression#alert_context}
        :param alert_rule_id: alert_rule_id block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#alert_rule_id MonitorAlertProcessingRuleSuppression#alert_rule_id}
        :param alert_rule_name: alert_rule_name block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#alert_rule_name MonitorAlertProcessingRuleSuppression#alert_rule_name}
        :param description: description block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#description MonitorAlertProcessingRuleSuppression#description}
        :param monitor_condition: monitor_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#monitor_condition MonitorAlertProcessingRuleSuppression#monitor_condition}
        :param monitor_service: monitor_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#monitor_service MonitorAlertProcessingRuleSuppression#monitor_service}
        :param severity: severity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#severity MonitorAlertProcessingRuleSuppression#severity}
        :param signal_type: signal_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#signal_type MonitorAlertProcessingRuleSuppression#signal_type}
        :param target_resource: target_resource block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#target_resource MonitorAlertProcessingRuleSuppression#target_resource}
        :param target_resource_group: target_resource_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#target_resource_group MonitorAlertProcessingRuleSuppression#target_resource_group}
        :param target_resource_type: target_resource_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#target_resource_type MonitorAlertProcessingRuleSuppression#target_resource_type}
        '''
        if isinstance(alert_context, dict):
            alert_context = MonitorAlertProcessingRuleSuppressionConditionAlertContext(**alert_context)
        if isinstance(alert_rule_id, dict):
            alert_rule_id = MonitorAlertProcessingRuleSuppressionConditionAlertRuleId(**alert_rule_id)
        if isinstance(alert_rule_name, dict):
            alert_rule_name = MonitorAlertProcessingRuleSuppressionConditionAlertRuleName(**alert_rule_name)
        if isinstance(description, dict):
            description = MonitorAlertProcessingRuleSuppressionConditionDescription(**description)
        if isinstance(monitor_condition, dict):
            monitor_condition = MonitorAlertProcessingRuleSuppressionConditionMonitorCondition(**monitor_condition)
        if isinstance(monitor_service, dict):
            monitor_service = MonitorAlertProcessingRuleSuppressionConditionMonitorService(**monitor_service)
        if isinstance(severity, dict):
            severity = MonitorAlertProcessingRuleSuppressionConditionSeverity(**severity)
        if isinstance(signal_type, dict):
            signal_type = MonitorAlertProcessingRuleSuppressionConditionSignalType(**signal_type)
        if isinstance(target_resource, dict):
            target_resource = MonitorAlertProcessingRuleSuppressionConditionTargetResource(**target_resource)
        if isinstance(target_resource_group, dict):
            target_resource_group = MonitorAlertProcessingRuleSuppressionConditionTargetResourceGroup(**target_resource_group)
        if isinstance(target_resource_type, dict):
            target_resource_type = MonitorAlertProcessingRuleSuppressionConditionTargetResourceType(**target_resource_type)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1999dfd4a98c9495fdfeeec27b193fd7e9520b5f5c5361d3c90d05406e8ed348)
            check_type(argname="argument alert_context", value=alert_context, expected_type=type_hints["alert_context"])
            check_type(argname="argument alert_rule_id", value=alert_rule_id, expected_type=type_hints["alert_rule_id"])
            check_type(argname="argument alert_rule_name", value=alert_rule_name, expected_type=type_hints["alert_rule_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument monitor_condition", value=monitor_condition, expected_type=type_hints["monitor_condition"])
            check_type(argname="argument monitor_service", value=monitor_service, expected_type=type_hints["monitor_service"])
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
            check_type(argname="argument signal_type", value=signal_type, expected_type=type_hints["signal_type"])
            check_type(argname="argument target_resource", value=target_resource, expected_type=type_hints["target_resource"])
            check_type(argname="argument target_resource_group", value=target_resource_group, expected_type=type_hints["target_resource_group"])
            check_type(argname="argument target_resource_type", value=target_resource_type, expected_type=type_hints["target_resource_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alert_context is not None:
            self._values["alert_context"] = alert_context
        if alert_rule_id is not None:
            self._values["alert_rule_id"] = alert_rule_id
        if alert_rule_name is not None:
            self._values["alert_rule_name"] = alert_rule_name
        if description is not None:
            self._values["description"] = description
        if monitor_condition is not None:
            self._values["monitor_condition"] = monitor_condition
        if monitor_service is not None:
            self._values["monitor_service"] = monitor_service
        if severity is not None:
            self._values["severity"] = severity
        if signal_type is not None:
            self._values["signal_type"] = signal_type
        if target_resource is not None:
            self._values["target_resource"] = target_resource
        if target_resource_group is not None:
            self._values["target_resource_group"] = target_resource_group
        if target_resource_type is not None:
            self._values["target_resource_type"] = target_resource_type

    @builtins.property
    def alert_context(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleSuppressionConditionAlertContext"]:
        '''alert_context block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#alert_context MonitorAlertProcessingRuleSuppression#alert_context}
        '''
        result = self._values.get("alert_context")
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleSuppressionConditionAlertContext"], result)

    @builtins.property
    def alert_rule_id(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleSuppressionConditionAlertRuleId"]:
        '''alert_rule_id block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#alert_rule_id MonitorAlertProcessingRuleSuppression#alert_rule_id}
        '''
        result = self._values.get("alert_rule_id")
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleSuppressionConditionAlertRuleId"], result)

    @builtins.property
    def alert_rule_name(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleSuppressionConditionAlertRuleName"]:
        '''alert_rule_name block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#alert_rule_name MonitorAlertProcessingRuleSuppression#alert_rule_name}
        '''
        result = self._values.get("alert_rule_name")
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleSuppressionConditionAlertRuleName"], result)

    @builtins.property
    def description(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleSuppressionConditionDescription"]:
        '''description block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#description MonitorAlertProcessingRuleSuppression#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleSuppressionConditionDescription"], result)

    @builtins.property
    def monitor_condition(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleSuppressionConditionMonitorCondition"]:
        '''monitor_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#monitor_condition MonitorAlertProcessingRuleSuppression#monitor_condition}
        '''
        result = self._values.get("monitor_condition")
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleSuppressionConditionMonitorCondition"], result)

    @builtins.property
    def monitor_service(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleSuppressionConditionMonitorService"]:
        '''monitor_service block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#monitor_service MonitorAlertProcessingRuleSuppression#monitor_service}
        '''
        result = self._values.get("monitor_service")
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleSuppressionConditionMonitorService"], result)

    @builtins.property
    def severity(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleSuppressionConditionSeverity"]:
        '''severity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#severity MonitorAlertProcessingRuleSuppression#severity}
        '''
        result = self._values.get("severity")
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleSuppressionConditionSeverity"], result)

    @builtins.property
    def signal_type(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleSuppressionConditionSignalType"]:
        '''signal_type block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#signal_type MonitorAlertProcessingRuleSuppression#signal_type}
        '''
        result = self._values.get("signal_type")
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleSuppressionConditionSignalType"], result)

    @builtins.property
    def target_resource(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleSuppressionConditionTargetResource"]:
        '''target_resource block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#target_resource MonitorAlertProcessingRuleSuppression#target_resource}
        '''
        result = self._values.get("target_resource")
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleSuppressionConditionTargetResource"], result)

    @builtins.property
    def target_resource_group(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleSuppressionConditionTargetResourceGroup"]:
        '''target_resource_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#target_resource_group MonitorAlertProcessingRuleSuppression#target_resource_group}
        '''
        result = self._values.get("target_resource_group")
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleSuppressionConditionTargetResourceGroup"], result)

    @builtins.property
    def target_resource_type(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleSuppressionConditionTargetResourceType"]:
        '''target_resource_type block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#target_resource_type MonitorAlertProcessingRuleSuppression#target_resource_type}
        '''
        result = self._values.get("target_resource_type")
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleSuppressionConditionTargetResourceType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleSuppressionCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionConditionAlertContext",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorAlertProcessingRuleSuppressionConditionAlertContext:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#operator MonitorAlertProcessingRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#values MonitorAlertProcessingRuleSuppression#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c06c9e4976fb79877a76083541005365719d6304af9cd31b17b1f12644e6121)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#operator MonitorAlertProcessingRuleSuppression#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#values MonitorAlertProcessingRuleSuppression#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleSuppressionConditionAlertContext(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAlertProcessingRuleSuppressionConditionAlertContextOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionConditionAlertContextOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e64ccd444cf6281383bec6047eeb6bf789c5541e91e486a36b5d88efb4731cbd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6daa12244f8c76e4647b9a187eef2fdd07ba883bb466de6d5c6bad8bf70db606)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f93565074b99e97bdbb777d7e1c28562eb42a8fd4d7d7960a74421aa24b19ac1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleSuppressionConditionAlertContext]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleSuppressionConditionAlertContext], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAlertProcessingRuleSuppressionConditionAlertContext],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2e81e486877e26879106cccf4d49d182e287a792e117b427f081a1799fe3a04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionConditionAlertRuleId",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorAlertProcessingRuleSuppressionConditionAlertRuleId:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#operator MonitorAlertProcessingRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#values MonitorAlertProcessingRuleSuppression#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6d610bd67251269717996276d0302e55c63086fda7cf056143e934f99df4398)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#operator MonitorAlertProcessingRuleSuppression#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#values MonitorAlertProcessingRuleSuppression#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleSuppressionConditionAlertRuleId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAlertProcessingRuleSuppressionConditionAlertRuleIdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionConditionAlertRuleIdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__14122b72993ade0d18d28b0f02a9f28f3756c908f144a37b9ccdbf6e3ba97276)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dd0aa693c342e66fe5d2069bfe4954012886c4f0e9a17eb98c6d5f4d1590530)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d68c900b501e385c75aea5e18c9b98372be0bfb925ae63246e0c1d12a2779a80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleSuppressionConditionAlertRuleId]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleSuppressionConditionAlertRuleId], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAlertProcessingRuleSuppressionConditionAlertRuleId],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8369d6dcd89fe47a05ed27d0957c21c65b672348289cfdef158ba60b1e88375a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionConditionAlertRuleName",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorAlertProcessingRuleSuppressionConditionAlertRuleName:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#operator MonitorAlertProcessingRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#values MonitorAlertProcessingRuleSuppression#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc3293230bb4cc883dabd0b822441d62b828fd42d65a4274ac75960b9775d437)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#operator MonitorAlertProcessingRuleSuppression#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#values MonitorAlertProcessingRuleSuppression#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleSuppressionConditionAlertRuleName(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAlertProcessingRuleSuppressionConditionAlertRuleNameOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionConditionAlertRuleNameOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__06cdfd79341be8ae3cd9eafd09edd372acee3a994490e43638855f6cde1b5a6b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07d26a82669b01fd4e4c4e002f7d2b7a2852f3549bd34bf029d26d2f50552549)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44208a3b50ac8e8894135af10e5a36b4e6883be1acac497128c501a3cff18e4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleSuppressionConditionAlertRuleName]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleSuppressionConditionAlertRuleName], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAlertProcessingRuleSuppressionConditionAlertRuleName],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edba7466f3ff9eb01069a1a231423f4d4928d9d51b4234339bdf2071869e5b36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionConditionDescription",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorAlertProcessingRuleSuppressionConditionDescription:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#operator MonitorAlertProcessingRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#values MonitorAlertProcessingRuleSuppression#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16b8bfbab6842b91a16b839714be1bbce6cf2b82df027ec286fa9619129d2c7a)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#operator MonitorAlertProcessingRuleSuppression#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#values MonitorAlertProcessingRuleSuppression#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleSuppressionConditionDescription(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAlertProcessingRuleSuppressionConditionDescriptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionConditionDescriptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8628f89f5ea4e642deab9e399aca8f67afd23fc1db7410f0fe9a4fec3576179b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1736aa5c8cc5e56af088968638b09c53074f75301edac236467b183c5ab619ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1ec4f66af05ef51c4a0ed4022b0e822bbc17ab8e3eb68b9c204e8ab2920d3cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleSuppressionConditionDescription]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleSuppressionConditionDescription], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAlertProcessingRuleSuppressionConditionDescription],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b91bd5bc2893911f3c237849650d3b450d7b0896c7eafa420e75d95f90eb90d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionConditionMonitorCondition",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorAlertProcessingRuleSuppressionConditionMonitorCondition:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#operator MonitorAlertProcessingRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#values MonitorAlertProcessingRuleSuppression#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__103568f0c3eeb21dc6ae99e134f9b7f1584c8674dc245c2faff86c9130eb4520)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#operator MonitorAlertProcessingRuleSuppression#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#values MonitorAlertProcessingRuleSuppression#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleSuppressionConditionMonitorCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAlertProcessingRuleSuppressionConditionMonitorConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionConditionMonitorConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e28d1506b9885886155f9dccb53c373c7e25d22ff912e3ada6ab9e90a62b657)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36b8ca69edea190d69fb1e4a7c966f761157b65b277702faebe6d21660a0f63d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20ec05f0d3e6e097cf10dbf5cdb80b74620f3707cf342bbb6c97097c49ccfb6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleSuppressionConditionMonitorCondition]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleSuppressionConditionMonitorCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAlertProcessingRuleSuppressionConditionMonitorCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd915a0db701b022c80e84ff193d3509f23f42cc0721e8907f4c1e696a023349)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionConditionMonitorService",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorAlertProcessingRuleSuppressionConditionMonitorService:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#operator MonitorAlertProcessingRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#values MonitorAlertProcessingRuleSuppression#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fafc58b2aaba305e8e233ee4a01698fb3355ebb1a77642d1b9a54d039683d0f8)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#operator MonitorAlertProcessingRuleSuppression#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#values MonitorAlertProcessingRuleSuppression#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleSuppressionConditionMonitorService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAlertProcessingRuleSuppressionConditionMonitorServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionConditionMonitorServiceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__67a1bf98b4ea8cb45d424bd97ea999f3a39fd745888f906e4e598ef2283f1492)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79dc98b1b5369bb79266c691cb130f2a2513c40cc873a24cbc81b201ea42e165)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac4a7f8b62be15f0de58009a475b4ca2ed567f27cd9362aaa0a57de0e33c2ebd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleSuppressionConditionMonitorService]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleSuppressionConditionMonitorService], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAlertProcessingRuleSuppressionConditionMonitorService],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f36f72cf9fc94fe40f01ec3a5b22f5f315e66b61c86a45e420dda1cacf897caf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorAlertProcessingRuleSuppressionConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__91f2704d857828cbef79158f772ccdeb4d7be0d7379ce08978831993556c63ce)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAlertContext")
    def put_alert_context(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#operator MonitorAlertProcessingRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#values MonitorAlertProcessingRuleSuppression#values}.
        '''
        value = MonitorAlertProcessingRuleSuppressionConditionAlertContext(
            operator=operator, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putAlertContext", [value]))

    @jsii.member(jsii_name="putAlertRuleId")
    def put_alert_rule_id(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#operator MonitorAlertProcessingRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#values MonitorAlertProcessingRuleSuppression#values}.
        '''
        value = MonitorAlertProcessingRuleSuppressionConditionAlertRuleId(
            operator=operator, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putAlertRuleId", [value]))

    @jsii.member(jsii_name="putAlertRuleName")
    def put_alert_rule_name(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#operator MonitorAlertProcessingRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#values MonitorAlertProcessingRuleSuppression#values}.
        '''
        value = MonitorAlertProcessingRuleSuppressionConditionAlertRuleName(
            operator=operator, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putAlertRuleName", [value]))

    @jsii.member(jsii_name="putDescription")
    def put_description(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#operator MonitorAlertProcessingRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#values MonitorAlertProcessingRuleSuppression#values}.
        '''
        value = MonitorAlertProcessingRuleSuppressionConditionDescription(
            operator=operator, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putDescription", [value]))

    @jsii.member(jsii_name="putMonitorCondition")
    def put_monitor_condition(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#operator MonitorAlertProcessingRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#values MonitorAlertProcessingRuleSuppression#values}.
        '''
        value = MonitorAlertProcessingRuleSuppressionConditionMonitorCondition(
            operator=operator, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putMonitorCondition", [value]))

    @jsii.member(jsii_name="putMonitorService")
    def put_monitor_service(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#operator MonitorAlertProcessingRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#values MonitorAlertProcessingRuleSuppression#values}.
        '''
        value = MonitorAlertProcessingRuleSuppressionConditionMonitorService(
            operator=operator, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putMonitorService", [value]))

    @jsii.member(jsii_name="putSeverity")
    def put_severity(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#operator MonitorAlertProcessingRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#values MonitorAlertProcessingRuleSuppression#values}.
        '''
        value = MonitorAlertProcessingRuleSuppressionConditionSeverity(
            operator=operator, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putSeverity", [value]))

    @jsii.member(jsii_name="putSignalType")
    def put_signal_type(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#operator MonitorAlertProcessingRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#values MonitorAlertProcessingRuleSuppression#values}.
        '''
        value = MonitorAlertProcessingRuleSuppressionConditionSignalType(
            operator=operator, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putSignalType", [value]))

    @jsii.member(jsii_name="putTargetResource")
    def put_target_resource(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#operator MonitorAlertProcessingRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#values MonitorAlertProcessingRuleSuppression#values}.
        '''
        value = MonitorAlertProcessingRuleSuppressionConditionTargetResource(
            operator=operator, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putTargetResource", [value]))

    @jsii.member(jsii_name="putTargetResourceGroup")
    def put_target_resource_group(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#operator MonitorAlertProcessingRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#values MonitorAlertProcessingRuleSuppression#values}.
        '''
        value = MonitorAlertProcessingRuleSuppressionConditionTargetResourceGroup(
            operator=operator, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putTargetResourceGroup", [value]))

    @jsii.member(jsii_name="putTargetResourceType")
    def put_target_resource_type(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#operator MonitorAlertProcessingRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#values MonitorAlertProcessingRuleSuppression#values}.
        '''
        value = MonitorAlertProcessingRuleSuppressionConditionTargetResourceType(
            operator=operator, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putTargetResourceType", [value]))

    @jsii.member(jsii_name="resetAlertContext")
    def reset_alert_context(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlertContext", []))

    @jsii.member(jsii_name="resetAlertRuleId")
    def reset_alert_rule_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlertRuleId", []))

    @jsii.member(jsii_name="resetAlertRuleName")
    def reset_alert_rule_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlertRuleName", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetMonitorCondition")
    def reset_monitor_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitorCondition", []))

    @jsii.member(jsii_name="resetMonitorService")
    def reset_monitor_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitorService", []))

    @jsii.member(jsii_name="resetSeverity")
    def reset_severity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeverity", []))

    @jsii.member(jsii_name="resetSignalType")
    def reset_signal_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSignalType", []))

    @jsii.member(jsii_name="resetTargetResource")
    def reset_target_resource(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetResource", []))

    @jsii.member(jsii_name="resetTargetResourceGroup")
    def reset_target_resource_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetResourceGroup", []))

    @jsii.member(jsii_name="resetTargetResourceType")
    def reset_target_resource_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetResourceType", []))

    @builtins.property
    @jsii.member(jsii_name="alertContext")
    def alert_context(
        self,
    ) -> MonitorAlertProcessingRuleSuppressionConditionAlertContextOutputReference:
        return typing.cast(MonitorAlertProcessingRuleSuppressionConditionAlertContextOutputReference, jsii.get(self, "alertContext"))

    @builtins.property
    @jsii.member(jsii_name="alertRuleId")
    def alert_rule_id(
        self,
    ) -> MonitorAlertProcessingRuleSuppressionConditionAlertRuleIdOutputReference:
        return typing.cast(MonitorAlertProcessingRuleSuppressionConditionAlertRuleIdOutputReference, jsii.get(self, "alertRuleId"))

    @builtins.property
    @jsii.member(jsii_name="alertRuleName")
    def alert_rule_name(
        self,
    ) -> MonitorAlertProcessingRuleSuppressionConditionAlertRuleNameOutputReference:
        return typing.cast(MonitorAlertProcessingRuleSuppressionConditionAlertRuleNameOutputReference, jsii.get(self, "alertRuleName"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(
        self,
    ) -> MonitorAlertProcessingRuleSuppressionConditionDescriptionOutputReference:
        return typing.cast(MonitorAlertProcessingRuleSuppressionConditionDescriptionOutputReference, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="monitorCondition")
    def monitor_condition(
        self,
    ) -> MonitorAlertProcessingRuleSuppressionConditionMonitorConditionOutputReference:
        return typing.cast(MonitorAlertProcessingRuleSuppressionConditionMonitorConditionOutputReference, jsii.get(self, "monitorCondition"))

    @builtins.property
    @jsii.member(jsii_name="monitorService")
    def monitor_service(
        self,
    ) -> MonitorAlertProcessingRuleSuppressionConditionMonitorServiceOutputReference:
        return typing.cast(MonitorAlertProcessingRuleSuppressionConditionMonitorServiceOutputReference, jsii.get(self, "monitorService"))

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(
        self,
    ) -> "MonitorAlertProcessingRuleSuppressionConditionSeverityOutputReference":
        return typing.cast("MonitorAlertProcessingRuleSuppressionConditionSeverityOutputReference", jsii.get(self, "severity"))

    @builtins.property
    @jsii.member(jsii_name="signalType")
    def signal_type(
        self,
    ) -> "MonitorAlertProcessingRuleSuppressionConditionSignalTypeOutputReference":
        return typing.cast("MonitorAlertProcessingRuleSuppressionConditionSignalTypeOutputReference", jsii.get(self, "signalType"))

    @builtins.property
    @jsii.member(jsii_name="targetResource")
    def target_resource(
        self,
    ) -> "MonitorAlertProcessingRuleSuppressionConditionTargetResourceOutputReference":
        return typing.cast("MonitorAlertProcessingRuleSuppressionConditionTargetResourceOutputReference", jsii.get(self, "targetResource"))

    @builtins.property
    @jsii.member(jsii_name="targetResourceGroup")
    def target_resource_group(
        self,
    ) -> "MonitorAlertProcessingRuleSuppressionConditionTargetResourceGroupOutputReference":
        return typing.cast("MonitorAlertProcessingRuleSuppressionConditionTargetResourceGroupOutputReference", jsii.get(self, "targetResourceGroup"))

    @builtins.property
    @jsii.member(jsii_name="targetResourceType")
    def target_resource_type(
        self,
    ) -> "MonitorAlertProcessingRuleSuppressionConditionTargetResourceTypeOutputReference":
        return typing.cast("MonitorAlertProcessingRuleSuppressionConditionTargetResourceTypeOutputReference", jsii.get(self, "targetResourceType"))

    @builtins.property
    @jsii.member(jsii_name="alertContextInput")
    def alert_context_input(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleSuppressionConditionAlertContext]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleSuppressionConditionAlertContext], jsii.get(self, "alertContextInput"))

    @builtins.property
    @jsii.member(jsii_name="alertRuleIdInput")
    def alert_rule_id_input(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleSuppressionConditionAlertRuleId]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleSuppressionConditionAlertRuleId], jsii.get(self, "alertRuleIdInput"))

    @builtins.property
    @jsii.member(jsii_name="alertRuleNameInput")
    def alert_rule_name_input(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleSuppressionConditionAlertRuleName]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleSuppressionConditionAlertRuleName], jsii.get(self, "alertRuleNameInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleSuppressionConditionDescription]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleSuppressionConditionDescription], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorConditionInput")
    def monitor_condition_input(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleSuppressionConditionMonitorCondition]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleSuppressionConditionMonitorCondition], jsii.get(self, "monitorConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorServiceInput")
    def monitor_service_input(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleSuppressionConditionMonitorService]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleSuppressionConditionMonitorService], jsii.get(self, "monitorServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="severityInput")
    def severity_input(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleSuppressionConditionSeverity"]:
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleSuppressionConditionSeverity"], jsii.get(self, "severityInput"))

    @builtins.property
    @jsii.member(jsii_name="signalTypeInput")
    def signal_type_input(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleSuppressionConditionSignalType"]:
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleSuppressionConditionSignalType"], jsii.get(self, "signalTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="targetResourceGroupInput")
    def target_resource_group_input(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleSuppressionConditionTargetResourceGroup"]:
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleSuppressionConditionTargetResourceGroup"], jsii.get(self, "targetResourceGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="targetResourceInput")
    def target_resource_input(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleSuppressionConditionTargetResource"]:
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleSuppressionConditionTargetResource"], jsii.get(self, "targetResourceInput"))

    @builtins.property
    @jsii.member(jsii_name="targetResourceTypeInput")
    def target_resource_type_input(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleSuppressionConditionTargetResourceType"]:
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleSuppressionConditionTargetResourceType"], jsii.get(self, "targetResourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleSuppressionCondition]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleSuppressionCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAlertProcessingRuleSuppressionCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45fbdba16646a28e919cba2832dd9c353d09b88b2a297fea93051cbdd359d8ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionConditionSeverity",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorAlertProcessingRuleSuppressionConditionSeverity:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#operator MonitorAlertProcessingRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#values MonitorAlertProcessingRuleSuppression#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56e343f1c173071935b741ce30930e0897fc0fc2380b102bc6bbb4ea53b704b5)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#operator MonitorAlertProcessingRuleSuppression#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#values MonitorAlertProcessingRuleSuppression#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleSuppressionConditionSeverity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAlertProcessingRuleSuppressionConditionSeverityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionConditionSeverityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b401249f1b54dbd937effdfd92f8fe9e0d9c246c6de7597ff8d09819cfcc994)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2d86e162a36017d5219e65318e19b742f71a6ae7b0b53e1e13d7f975682ac2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be6b090fcfaf973cf47600abfdf2a2aeadf24119e9d65bcd8df3d126a6f9e0c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleSuppressionConditionSeverity]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleSuppressionConditionSeverity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAlertProcessingRuleSuppressionConditionSeverity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__091be877ae1b2847f33d0b7903dc6f04ff69bc3caa7c3dadfb624b2c3d4e30ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionConditionSignalType",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorAlertProcessingRuleSuppressionConditionSignalType:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#operator MonitorAlertProcessingRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#values MonitorAlertProcessingRuleSuppression#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50fd0d8389221bff6c07d16e9195a49126916d41975a60afd60ac3d2de5753c9)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#operator MonitorAlertProcessingRuleSuppression#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#values MonitorAlertProcessingRuleSuppression#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleSuppressionConditionSignalType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAlertProcessingRuleSuppressionConditionSignalTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionConditionSignalTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a36c6a8d6754c110b8376c90b10f8d36f3db2fa8f55785ea75135af56dbd92e4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__586232f3941330030f9a19306ecf1e7050b5cb60fd8168becefafbae1aaeba3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__292a6fafd53d5479c122e47d64123789e45adb425f2936ad6a1086d40751afc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleSuppressionConditionSignalType]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleSuppressionConditionSignalType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAlertProcessingRuleSuppressionConditionSignalType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfb6ff87b67e5c67aa177d775c088b44494d11a26a9c531dcca5b1fe70a40037)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionConditionTargetResource",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorAlertProcessingRuleSuppressionConditionTargetResource:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#operator MonitorAlertProcessingRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#values MonitorAlertProcessingRuleSuppression#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21dae9bfacb883a4adb81deb512e6e24b0c7fc24c37db8b3ff895da6cfbb83bd)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#operator MonitorAlertProcessingRuleSuppression#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#values MonitorAlertProcessingRuleSuppression#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleSuppressionConditionTargetResource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionConditionTargetResourceGroup",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorAlertProcessingRuleSuppressionConditionTargetResourceGroup:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#operator MonitorAlertProcessingRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#values MonitorAlertProcessingRuleSuppression#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__263ca34d6fdb4a1de99adfa087c060d54ec8fa2baaf7afe2245cb65358405b9a)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#operator MonitorAlertProcessingRuleSuppression#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#values MonitorAlertProcessingRuleSuppression#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleSuppressionConditionTargetResourceGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAlertProcessingRuleSuppressionConditionTargetResourceGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionConditionTargetResourceGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfc66dde1338975549486bbe7aff023f5ed38022bcb267f708e9c5b776b6e016)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__579bc08168a8398d921f82e6ae9e5df1872e0b88b4efd7b6e361576bc742514f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8814af306e0765557239d8c1948e6f789ab737de9c1e6a90b4be610532ce9c31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleSuppressionConditionTargetResourceGroup]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleSuppressionConditionTargetResourceGroup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAlertProcessingRuleSuppressionConditionTargetResourceGroup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba0b516028acc84cafbaec1f11200aee7e8ae4dd709017ed1d3d9f03d7ef941d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorAlertProcessingRuleSuppressionConditionTargetResourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionConditionTargetResourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f1f400d925197e2c081f43345826f8aeeb06193b1a341f06d9564b0be2681dad)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4bea3c48ee2b81247224ae75a40d6d395cc79e313f4d9dbc00dea6bc64a0c113)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__593984634e803a2dfae64525dbb30a90201a486a752c26fb60b7862357c29f25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleSuppressionConditionTargetResource]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleSuppressionConditionTargetResource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAlertProcessingRuleSuppressionConditionTargetResource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b7b24d4e0fc998e576a098a1131dd4025ff4f36ff3ba0446970d920481c3697)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionConditionTargetResourceType",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorAlertProcessingRuleSuppressionConditionTargetResourceType:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#operator MonitorAlertProcessingRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#values MonitorAlertProcessingRuleSuppression#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a23f1d0d219b5008e0076ac260270ea504024630e286755936d2bd432166d810)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#operator MonitorAlertProcessingRuleSuppression#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#values MonitorAlertProcessingRuleSuppression#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleSuppressionConditionTargetResourceType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAlertProcessingRuleSuppressionConditionTargetResourceTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionConditionTargetResourceTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3db35bb63246a6d98db782ad4b4345e21728c04add8876640445829a4f9d6af1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d3a6848770402b4506bfbd6563714916e514e72657402c5d85470eb6733c796)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c717d84eb636bbc364d450890edda09fc17310781f1dccc7a08ccf0e5a03ea7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleSuppressionConditionTargetResourceType]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleSuppressionConditionTargetResourceType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAlertProcessingRuleSuppressionConditionTargetResourceType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40cf6408c7a5db5be5bf859328840a9a6589faeb462efd79334ca248ffeea379)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionConfig",
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
        "condition": "condition",
        "description": "description",
        "enabled": "enabled",
        "id": "id",
        "schedule": "schedule",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class MonitorAlertProcessingRuleSuppressionConfig(
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
        name: builtins.str,
        resource_group_name: builtins.str,
        scopes: typing.Sequence[builtins.str],
        condition: typing.Optional[typing.Union[MonitorAlertProcessingRuleSuppressionCondition, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[typing.Union["MonitorAlertProcessingRuleSuppressionSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MonitorAlertProcessingRuleSuppressionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#name MonitorAlertProcessingRuleSuppression#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#resource_group_name MonitorAlertProcessingRuleSuppression#resource_group_name}.
        :param scopes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#scopes MonitorAlertProcessingRuleSuppression#scopes}.
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#condition MonitorAlertProcessingRuleSuppression#condition}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#description MonitorAlertProcessingRuleSuppression#description}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#enabled MonitorAlertProcessingRuleSuppression#enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#id MonitorAlertProcessingRuleSuppression#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#schedule MonitorAlertProcessingRuleSuppression#schedule}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#tags MonitorAlertProcessingRuleSuppression#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#timeouts MonitorAlertProcessingRuleSuppression#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(condition, dict):
            condition = MonitorAlertProcessingRuleSuppressionCondition(**condition)
        if isinstance(schedule, dict):
            schedule = MonitorAlertProcessingRuleSuppressionSchedule(**schedule)
        if isinstance(timeouts, dict):
            timeouts = MonitorAlertProcessingRuleSuppressionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62a24bbfcee9fc379f371ae91590305a4fa15d07ddf559ba9578fbdfde7edb2f)
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
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
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
        if condition is not None:
            self._values["condition"] = condition
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if id is not None:
            self._values["id"] = id
        if schedule is not None:
            self._values["schedule"] = schedule
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
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#name MonitorAlertProcessingRuleSuppression#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#resource_group_name MonitorAlertProcessingRuleSuppression#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scopes(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#scopes MonitorAlertProcessingRuleSuppression#scopes}.'''
        result = self._values.get("scopes")
        assert result is not None, "Required property 'scopes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def condition(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleSuppressionCondition]:
        '''condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#condition MonitorAlertProcessingRuleSuppression#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleSuppressionCondition], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#description MonitorAlertProcessingRuleSuppression#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#enabled MonitorAlertProcessingRuleSuppression#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#id MonitorAlertProcessingRuleSuppression#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleSuppressionSchedule"]:
        '''schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#schedule MonitorAlertProcessingRuleSuppression#schedule}
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleSuppressionSchedule"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#tags MonitorAlertProcessingRuleSuppression#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleSuppressionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#timeouts MonitorAlertProcessingRuleSuppression#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleSuppressionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleSuppressionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionSchedule",
    jsii_struct_bases=[],
    name_mapping={
        "effective_from": "effectiveFrom",
        "effective_until": "effectiveUntil",
        "recurrence": "recurrence",
        "time_zone": "timeZone",
    },
)
class MonitorAlertProcessingRuleSuppressionSchedule:
    def __init__(
        self,
        *,
        effective_from: typing.Optional[builtins.str] = None,
        effective_until: typing.Optional[builtins.str] = None,
        recurrence: typing.Optional[typing.Union["MonitorAlertProcessingRuleSuppressionScheduleRecurrence", typing.Dict[builtins.str, typing.Any]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param effective_from: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#effective_from MonitorAlertProcessingRuleSuppression#effective_from}.
        :param effective_until: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#effective_until MonitorAlertProcessingRuleSuppression#effective_until}.
        :param recurrence: recurrence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#recurrence MonitorAlertProcessingRuleSuppression#recurrence}
        :param time_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#time_zone MonitorAlertProcessingRuleSuppression#time_zone}.
        '''
        if isinstance(recurrence, dict):
            recurrence = MonitorAlertProcessingRuleSuppressionScheduleRecurrence(**recurrence)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28503f5c8d76e74e3575933635d08441430d1ba3adadb08d5e5f50cd00c55c3e)
            check_type(argname="argument effective_from", value=effective_from, expected_type=type_hints["effective_from"])
            check_type(argname="argument effective_until", value=effective_until, expected_type=type_hints["effective_until"])
            check_type(argname="argument recurrence", value=recurrence, expected_type=type_hints["recurrence"])
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if effective_from is not None:
            self._values["effective_from"] = effective_from
        if effective_until is not None:
            self._values["effective_until"] = effective_until
        if recurrence is not None:
            self._values["recurrence"] = recurrence
        if time_zone is not None:
            self._values["time_zone"] = time_zone

    @builtins.property
    def effective_from(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#effective_from MonitorAlertProcessingRuleSuppression#effective_from}.'''
        result = self._values.get("effective_from")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def effective_until(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#effective_until MonitorAlertProcessingRuleSuppression#effective_until}.'''
        result = self._values.get("effective_until")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recurrence(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleSuppressionScheduleRecurrence"]:
        '''recurrence block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#recurrence MonitorAlertProcessingRuleSuppression#recurrence}
        '''
        result = self._values.get("recurrence")
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleSuppressionScheduleRecurrence"], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#time_zone MonitorAlertProcessingRuleSuppression#time_zone}.'''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleSuppressionSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAlertProcessingRuleSuppressionScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a93beab1cff24598d62ec6172ff54884492f1babcbb9a72dfe83c56fa3c839a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRecurrence")
    def put_recurrence(
        self,
        *,
        daily: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorAlertProcessingRuleSuppressionScheduleRecurrenceDaily", typing.Dict[builtins.str, typing.Any]]]]] = None,
        monthly: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorAlertProcessingRuleSuppressionScheduleRecurrenceMonthly", typing.Dict[builtins.str, typing.Any]]]]] = None,
        weekly: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorAlertProcessingRuleSuppressionScheduleRecurrenceWeekly", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param daily: daily block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#daily MonitorAlertProcessingRuleSuppression#daily}
        :param monthly: monthly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#monthly MonitorAlertProcessingRuleSuppression#monthly}
        :param weekly: weekly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#weekly MonitorAlertProcessingRuleSuppression#weekly}
        '''
        value = MonitorAlertProcessingRuleSuppressionScheduleRecurrence(
            daily=daily, monthly=monthly, weekly=weekly
        )

        return typing.cast(None, jsii.invoke(self, "putRecurrence", [value]))

    @jsii.member(jsii_name="resetEffectiveFrom")
    def reset_effective_from(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEffectiveFrom", []))

    @jsii.member(jsii_name="resetEffectiveUntil")
    def reset_effective_until(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEffectiveUntil", []))

    @jsii.member(jsii_name="resetRecurrence")
    def reset_recurrence(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecurrence", []))

    @jsii.member(jsii_name="resetTimeZone")
    def reset_time_zone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeZone", []))

    @builtins.property
    @jsii.member(jsii_name="recurrence")
    def recurrence(
        self,
    ) -> "MonitorAlertProcessingRuleSuppressionScheduleRecurrenceOutputReference":
        return typing.cast("MonitorAlertProcessingRuleSuppressionScheduleRecurrenceOutputReference", jsii.get(self, "recurrence"))

    @builtins.property
    @jsii.member(jsii_name="effectiveFromInput")
    def effective_from_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "effectiveFromInput"))

    @builtins.property
    @jsii.member(jsii_name="effectiveUntilInput")
    def effective_until_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "effectiveUntilInput"))

    @builtins.property
    @jsii.member(jsii_name="recurrenceInput")
    def recurrence_input(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleSuppressionScheduleRecurrence"]:
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleSuppressionScheduleRecurrence"], jsii.get(self, "recurrenceInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="effectiveFrom")
    def effective_from(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effectiveFrom"))

    @effective_from.setter
    def effective_from(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e339261ab11e6d4fc3b54282b7739815b7419951bb90d1f927f73473a2705a99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effectiveFrom", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="effectiveUntil")
    def effective_until(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effectiveUntil"))

    @effective_until.setter
    def effective_until(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f22ec339d92e4c6b64905ad580b8d9c487764c2c0456f3d33826a7b5cca032b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effectiveUntil", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cdf237962215f5bac46b9e81686510a51847b4b8b0eed98de902ef9277d0352)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleSuppressionSchedule]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleSuppressionSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAlertProcessingRuleSuppressionSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65195a3516a81bf551d0ae8072958733bac31cd6b5b1553c5fe49c9df918c07a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionScheduleRecurrence",
    jsii_struct_bases=[],
    name_mapping={"daily": "daily", "monthly": "monthly", "weekly": "weekly"},
)
class MonitorAlertProcessingRuleSuppressionScheduleRecurrence:
    def __init__(
        self,
        *,
        daily: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorAlertProcessingRuleSuppressionScheduleRecurrenceDaily", typing.Dict[builtins.str, typing.Any]]]]] = None,
        monthly: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorAlertProcessingRuleSuppressionScheduleRecurrenceMonthly", typing.Dict[builtins.str, typing.Any]]]]] = None,
        weekly: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorAlertProcessingRuleSuppressionScheduleRecurrenceWeekly", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param daily: daily block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#daily MonitorAlertProcessingRuleSuppression#daily}
        :param monthly: monthly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#monthly MonitorAlertProcessingRuleSuppression#monthly}
        :param weekly: weekly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#weekly MonitorAlertProcessingRuleSuppression#weekly}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__552c0eee748170c871ea03b9b6d49336f5ce79822d8458681415e6413f9be7fd)
            check_type(argname="argument daily", value=daily, expected_type=type_hints["daily"])
            check_type(argname="argument monthly", value=monthly, expected_type=type_hints["monthly"])
            check_type(argname="argument weekly", value=weekly, expected_type=type_hints["weekly"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if daily is not None:
            self._values["daily"] = daily
        if monthly is not None:
            self._values["monthly"] = monthly
        if weekly is not None:
            self._values["weekly"] = weekly

    @builtins.property
    def daily(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorAlertProcessingRuleSuppressionScheduleRecurrenceDaily"]]]:
        '''daily block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#daily MonitorAlertProcessingRuleSuppression#daily}
        '''
        result = self._values.get("daily")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorAlertProcessingRuleSuppressionScheduleRecurrenceDaily"]]], result)

    @builtins.property
    def monthly(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorAlertProcessingRuleSuppressionScheduleRecurrenceMonthly"]]]:
        '''monthly block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#monthly MonitorAlertProcessingRuleSuppression#monthly}
        '''
        result = self._values.get("monthly")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorAlertProcessingRuleSuppressionScheduleRecurrenceMonthly"]]], result)

    @builtins.property
    def weekly(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorAlertProcessingRuleSuppressionScheduleRecurrenceWeekly"]]]:
        '''weekly block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#weekly MonitorAlertProcessingRuleSuppression#weekly}
        '''
        result = self._values.get("weekly")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorAlertProcessingRuleSuppressionScheduleRecurrenceWeekly"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleSuppressionScheduleRecurrence(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionScheduleRecurrenceDaily",
    jsii_struct_bases=[],
    name_mapping={"end_time": "endTime", "start_time": "startTime"},
)
class MonitorAlertProcessingRuleSuppressionScheduleRecurrenceDaily:
    def __init__(self, *, end_time: builtins.str, start_time: builtins.str) -> None:
        '''
        :param end_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#end_time MonitorAlertProcessingRuleSuppression#end_time}.
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#start_time MonitorAlertProcessingRuleSuppression#start_time}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd0318eba3c0368af4c7032ea1612aed57dad8ffc1c6b332d52ce70500f3142f)
            check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end_time": end_time,
            "start_time": start_time,
        }

    @builtins.property
    def end_time(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#end_time MonitorAlertProcessingRuleSuppression#end_time}.'''
        result = self._values.get("end_time")
        assert result is not None, "Required property 'end_time' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_time(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#start_time MonitorAlertProcessingRuleSuppression#start_time}.'''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleSuppressionScheduleRecurrenceDaily(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAlertProcessingRuleSuppressionScheduleRecurrenceDailyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionScheduleRecurrenceDailyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ab2467c6c40fe358d41f3105935d847d115df9657ddbdfa176cf08b72b0249a4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorAlertProcessingRuleSuppressionScheduleRecurrenceDailyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c59096b12cb043aade7d64e51b378224ca79c7ea0dbb089c1e77474ba5ef2064)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorAlertProcessingRuleSuppressionScheduleRecurrenceDailyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b10fbeb3a3b832529fda6bdfbb8c6a6b4834433dd0ac1c0a5a526e1a053ac922)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4062cbae95db82e07756b21c2aa78f1137369c1176754463c6e5f75c0695c5e8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f781b4dc12fb1e9e997ac646cb1e30c5127be0c27f6c384ac4a968e31373bf88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAlertProcessingRuleSuppressionScheduleRecurrenceDaily]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAlertProcessingRuleSuppressionScheduleRecurrenceDaily]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAlertProcessingRuleSuppressionScheduleRecurrenceDaily]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96aba3ba4e782c77a5b52df2bd44dbe21ef3c51ad45df59144425082fc7c9ef6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorAlertProcessingRuleSuppressionScheduleRecurrenceDailyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionScheduleRecurrenceDailyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5df8cad0d678bc380f51df465f19a015c94c1340ee3d7e9059cd398943a3b578)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="endTimeInput")
    def end_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @end_time.setter
    def end_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81de65995637499578873acbb27205857ec38cfc4e60acfcf98e5d336230bd0c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0810226843c6997fcd4afa720154dc9c9b2d5ce0340de442de66ddb699374a92)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAlertProcessingRuleSuppressionScheduleRecurrenceDaily]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAlertProcessingRuleSuppressionScheduleRecurrenceDaily]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAlertProcessingRuleSuppressionScheduleRecurrenceDaily]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fd368811bc3e861ff3f94b5f9c6a00d018ef6500ede9c3243358f25c9891d86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionScheduleRecurrenceMonthly",
    jsii_struct_bases=[],
    name_mapping={
        "days_of_month": "daysOfMonth",
        "end_time": "endTime",
        "start_time": "startTime",
    },
)
class MonitorAlertProcessingRuleSuppressionScheduleRecurrenceMonthly:
    def __init__(
        self,
        *,
        days_of_month: typing.Sequence[jsii.Number],
        end_time: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param days_of_month: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#days_of_month MonitorAlertProcessingRuleSuppression#days_of_month}.
        :param end_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#end_time MonitorAlertProcessingRuleSuppression#end_time}.
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#start_time MonitorAlertProcessingRuleSuppression#start_time}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__453b4b61ba8a16282dceb9552f81d320dbd94f78352c2d11d7d792dae008c8bb)
            check_type(argname="argument days_of_month", value=days_of_month, expected_type=type_hints["days_of_month"])
            check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "days_of_month": days_of_month,
        }
        if end_time is not None:
            self._values["end_time"] = end_time
        if start_time is not None:
            self._values["start_time"] = start_time

    @builtins.property
    def days_of_month(self) -> typing.List[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#days_of_month MonitorAlertProcessingRuleSuppression#days_of_month}.'''
        result = self._values.get("days_of_month")
        assert result is not None, "Required property 'days_of_month' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    @builtins.property
    def end_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#end_time MonitorAlertProcessingRuleSuppression#end_time}.'''
        result = self._values.get("end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#start_time MonitorAlertProcessingRuleSuppression#start_time}.'''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleSuppressionScheduleRecurrenceMonthly(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAlertProcessingRuleSuppressionScheduleRecurrenceMonthlyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionScheduleRecurrenceMonthlyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c73db77351f3c1dcbebe2c383d23f1e9d1e45753bea885763333121abf5e2a9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorAlertProcessingRuleSuppressionScheduleRecurrenceMonthlyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3d9aa5855a62b769b69226a74d77744f0ec8e4ac381b4ca1caf5a8b3369b672)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorAlertProcessingRuleSuppressionScheduleRecurrenceMonthlyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20e1c8feb3e279f8d66ac685cf14ce356b9868a111fbe5a4feeec4f3f3b1614d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6fd7a396ff47d033ccbf214d1e269d71708b0c6a3f7d99e60af41b15228606f3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__656ef66f70b8094bead20dcc0561f42998464b0fd685ca5a89b2eca14a6902be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAlertProcessingRuleSuppressionScheduleRecurrenceMonthly]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAlertProcessingRuleSuppressionScheduleRecurrenceMonthly]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAlertProcessingRuleSuppressionScheduleRecurrenceMonthly]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d50415bb3e9a2c2a54d0ab7cf3cec3835d6cbf187583d75f8bdf149afba890ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorAlertProcessingRuleSuppressionScheduleRecurrenceMonthlyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionScheduleRecurrenceMonthlyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb6118f85db3954647c9582405818a38af9d548ec19b692d284a81c864524a3d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEndTime")
    def reset_end_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndTime", []))

    @jsii.member(jsii_name="resetStartTime")
    def reset_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTime", []))

    @builtins.property
    @jsii.member(jsii_name="daysOfMonthInput")
    def days_of_month_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "daysOfMonthInput"))

    @builtins.property
    @jsii.member(jsii_name="endTimeInput")
    def end_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="daysOfMonth")
    def days_of_month(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "daysOfMonth"))

    @days_of_month.setter
    def days_of_month(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17509d334a8c0c87998f2e0943ac9428e80d4162ae65ebee8ec9e65775ffa763)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysOfMonth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @end_time.setter
    def end_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f49877588757d461e2ce5b9a08025dfaaee8d8e1588a80e619b3cea52f56f63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fe5adde7feb1515a4f935c840f49b54c8ff9b38ddb873e2ca91ddf2002fb852)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAlertProcessingRuleSuppressionScheduleRecurrenceMonthly]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAlertProcessingRuleSuppressionScheduleRecurrenceMonthly]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAlertProcessingRuleSuppressionScheduleRecurrenceMonthly]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fafd893b005bd7cdd982062007f0e6df30592fb7b378cf396d940828b0cddc5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorAlertProcessingRuleSuppressionScheduleRecurrenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionScheduleRecurrenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__458b500414966f6bae4e3b5ce368b5091b7490c08be9ab3761599a44f93a123d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDaily")
    def put_daily(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorAlertProcessingRuleSuppressionScheduleRecurrenceDaily, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__080e8b51681c3f55b2e40b899adae43a2140ac927c830462ce457cbe02036f18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDaily", [value]))

    @jsii.member(jsii_name="putMonthly")
    def put_monthly(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorAlertProcessingRuleSuppressionScheduleRecurrenceMonthly, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__036f10de6c4363a7d4e55895a5e09e6a248533484eaeb456b3bc97a90e539480)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMonthly", [value]))

    @jsii.member(jsii_name="putWeekly")
    def put_weekly(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorAlertProcessingRuleSuppressionScheduleRecurrenceWeekly", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cdec8d66d2b510579eb3786d523bf5d9a9927e2737bae2c01571a926027f36c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putWeekly", [value]))

    @jsii.member(jsii_name="resetDaily")
    def reset_daily(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDaily", []))

    @jsii.member(jsii_name="resetMonthly")
    def reset_monthly(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonthly", []))

    @jsii.member(jsii_name="resetWeekly")
    def reset_weekly(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeekly", []))

    @builtins.property
    @jsii.member(jsii_name="daily")
    def daily(self) -> MonitorAlertProcessingRuleSuppressionScheduleRecurrenceDailyList:
        return typing.cast(MonitorAlertProcessingRuleSuppressionScheduleRecurrenceDailyList, jsii.get(self, "daily"))

    @builtins.property
    @jsii.member(jsii_name="monthly")
    def monthly(
        self,
    ) -> MonitorAlertProcessingRuleSuppressionScheduleRecurrenceMonthlyList:
        return typing.cast(MonitorAlertProcessingRuleSuppressionScheduleRecurrenceMonthlyList, jsii.get(self, "monthly"))

    @builtins.property
    @jsii.member(jsii_name="weekly")
    def weekly(
        self,
    ) -> "MonitorAlertProcessingRuleSuppressionScheduleRecurrenceWeeklyList":
        return typing.cast("MonitorAlertProcessingRuleSuppressionScheduleRecurrenceWeeklyList", jsii.get(self, "weekly"))

    @builtins.property
    @jsii.member(jsii_name="dailyInput")
    def daily_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAlertProcessingRuleSuppressionScheduleRecurrenceDaily]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAlertProcessingRuleSuppressionScheduleRecurrenceDaily]]], jsii.get(self, "dailyInput"))

    @builtins.property
    @jsii.member(jsii_name="monthlyInput")
    def monthly_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAlertProcessingRuleSuppressionScheduleRecurrenceMonthly]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAlertProcessingRuleSuppressionScheduleRecurrenceMonthly]]], jsii.get(self, "monthlyInput"))

    @builtins.property
    @jsii.member(jsii_name="weeklyInput")
    def weekly_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorAlertProcessingRuleSuppressionScheduleRecurrenceWeekly"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorAlertProcessingRuleSuppressionScheduleRecurrenceWeekly"]]], jsii.get(self, "weeklyInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleSuppressionScheduleRecurrence]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleSuppressionScheduleRecurrence], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAlertProcessingRuleSuppressionScheduleRecurrence],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aba7d0897d7cfe76a18e2065432b0199a76aaf300d98ee44bccc146e6f22ae1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionScheduleRecurrenceWeekly",
    jsii_struct_bases=[],
    name_mapping={
        "days_of_week": "daysOfWeek",
        "end_time": "endTime",
        "start_time": "startTime",
    },
)
class MonitorAlertProcessingRuleSuppressionScheduleRecurrenceWeekly:
    def __init__(
        self,
        *,
        days_of_week: typing.Sequence[builtins.str],
        end_time: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param days_of_week: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#days_of_week MonitorAlertProcessingRuleSuppression#days_of_week}.
        :param end_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#end_time MonitorAlertProcessingRuleSuppression#end_time}.
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#start_time MonitorAlertProcessingRuleSuppression#start_time}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4c5c790fb92796292c6b29e81cd4e06f52ae1c8ecfc96595eeca82089383c5b)
            check_type(argname="argument days_of_week", value=days_of_week, expected_type=type_hints["days_of_week"])
            check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "days_of_week": days_of_week,
        }
        if end_time is not None:
            self._values["end_time"] = end_time
        if start_time is not None:
            self._values["start_time"] = start_time

    @builtins.property
    def days_of_week(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#days_of_week MonitorAlertProcessingRuleSuppression#days_of_week}.'''
        result = self._values.get("days_of_week")
        assert result is not None, "Required property 'days_of_week' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def end_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#end_time MonitorAlertProcessingRuleSuppression#end_time}.'''
        result = self._values.get("end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#start_time MonitorAlertProcessingRuleSuppression#start_time}.'''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleSuppressionScheduleRecurrenceWeekly(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAlertProcessingRuleSuppressionScheduleRecurrenceWeeklyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionScheduleRecurrenceWeeklyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3ca0caa3a720e601282a4f5c1661d4a05037b6ca0ba0a396aca2b39acdec008)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorAlertProcessingRuleSuppressionScheduleRecurrenceWeeklyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b726fbeb21b19b9b7451c7b5b811f38a8f27debccc0a058ab1730eb0d5e70dd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorAlertProcessingRuleSuppressionScheduleRecurrenceWeeklyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__073ee8a112d2fd8419610f76ac560c495cce039f7dc634403cd1ffb705ca7453)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb6bc1581a45f1380fbbc8297341244d22a492ac15edcc4c415da195f8e41a61)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1dea3899593e419c0a272364e23963d61934f873d8672f98c5f876c8a36a39f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAlertProcessingRuleSuppressionScheduleRecurrenceWeekly]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAlertProcessingRuleSuppressionScheduleRecurrenceWeekly]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAlertProcessingRuleSuppressionScheduleRecurrenceWeekly]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5bae8e5044428ccdea4e209996e95898b8f8f4b50f5ac30932cb27e2f976bb9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorAlertProcessingRuleSuppressionScheduleRecurrenceWeeklyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionScheduleRecurrenceWeeklyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1045e1bf1afee6750b5bd15d7fca97e78f9557d0f883c429edc8bea12d6794b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEndTime")
    def reset_end_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndTime", []))

    @jsii.member(jsii_name="resetStartTime")
    def reset_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTime", []))

    @builtins.property
    @jsii.member(jsii_name="daysOfWeekInput")
    def days_of_week_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "daysOfWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="endTimeInput")
    def end_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="daysOfWeek")
    def days_of_week(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "daysOfWeek"))

    @days_of_week.setter
    def days_of_week(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee9194eae02433c7cf5e25b764e01830bb62e66cca5d99aafbfc8bad1fffd3e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @end_time.setter
    def end_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdd5dbe77bf948afb18c52e43825c81f2483c04ce5ff79f12c9a129158771b98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1a3d3fd9ba18a1d4ca01de2bf6cd4fc3ca2b34ce46c9adec0048e5bbd3b3411)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAlertProcessingRuleSuppressionScheduleRecurrenceWeekly]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAlertProcessingRuleSuppressionScheduleRecurrenceWeekly]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAlertProcessingRuleSuppressionScheduleRecurrenceWeekly]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eccd5e2091d8115f682b3c05e4c50236bac3b00309df44f61bc23e4cc116f733)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MonitorAlertProcessingRuleSuppressionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#create MonitorAlertProcessingRuleSuppression#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#delete MonitorAlertProcessingRuleSuppression#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#read MonitorAlertProcessingRuleSuppression#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#update MonitorAlertProcessingRuleSuppression#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__457f03ee759be3e8fc68aefda8482b5e493e6a9b37122b74545cb4bd946d804d)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#create MonitorAlertProcessingRuleSuppression#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#delete MonitorAlertProcessingRuleSuppression#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#read MonitorAlertProcessingRuleSuppression#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_suppression#update MonitorAlertProcessingRuleSuppression#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleSuppressionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAlertProcessingRuleSuppressionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleSuppression.MonitorAlertProcessingRuleSuppressionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0e0db104dc980c9493d529999d916d1247e96dd1672d503594caa36d60f690d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f754645511e70869188b40315e0ca62f0054fb84c683a662a251fff23605756a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ffa67be650aa3ebf9b92c4a4eced535a97a39eb7c8242db7006a2e5848d3627e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c98d6725de94481968af00e19c8e17f42348d562e1ebbee852200e8e48931277)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77548c94eab260251d4f651e85375b3a9140e3d208196b680da3403eb617ff84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAlertProcessingRuleSuppressionTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAlertProcessingRuleSuppressionTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAlertProcessingRuleSuppressionTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2140f9e511b600308062fe83ea745ebbc25d541e3da031375850b8ba1a56add1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MonitorAlertProcessingRuleSuppression",
    "MonitorAlertProcessingRuleSuppressionCondition",
    "MonitorAlertProcessingRuleSuppressionConditionAlertContext",
    "MonitorAlertProcessingRuleSuppressionConditionAlertContextOutputReference",
    "MonitorAlertProcessingRuleSuppressionConditionAlertRuleId",
    "MonitorAlertProcessingRuleSuppressionConditionAlertRuleIdOutputReference",
    "MonitorAlertProcessingRuleSuppressionConditionAlertRuleName",
    "MonitorAlertProcessingRuleSuppressionConditionAlertRuleNameOutputReference",
    "MonitorAlertProcessingRuleSuppressionConditionDescription",
    "MonitorAlertProcessingRuleSuppressionConditionDescriptionOutputReference",
    "MonitorAlertProcessingRuleSuppressionConditionMonitorCondition",
    "MonitorAlertProcessingRuleSuppressionConditionMonitorConditionOutputReference",
    "MonitorAlertProcessingRuleSuppressionConditionMonitorService",
    "MonitorAlertProcessingRuleSuppressionConditionMonitorServiceOutputReference",
    "MonitorAlertProcessingRuleSuppressionConditionOutputReference",
    "MonitorAlertProcessingRuleSuppressionConditionSeverity",
    "MonitorAlertProcessingRuleSuppressionConditionSeverityOutputReference",
    "MonitorAlertProcessingRuleSuppressionConditionSignalType",
    "MonitorAlertProcessingRuleSuppressionConditionSignalTypeOutputReference",
    "MonitorAlertProcessingRuleSuppressionConditionTargetResource",
    "MonitorAlertProcessingRuleSuppressionConditionTargetResourceGroup",
    "MonitorAlertProcessingRuleSuppressionConditionTargetResourceGroupOutputReference",
    "MonitorAlertProcessingRuleSuppressionConditionTargetResourceOutputReference",
    "MonitorAlertProcessingRuleSuppressionConditionTargetResourceType",
    "MonitorAlertProcessingRuleSuppressionConditionTargetResourceTypeOutputReference",
    "MonitorAlertProcessingRuleSuppressionConfig",
    "MonitorAlertProcessingRuleSuppressionSchedule",
    "MonitorAlertProcessingRuleSuppressionScheduleOutputReference",
    "MonitorAlertProcessingRuleSuppressionScheduleRecurrence",
    "MonitorAlertProcessingRuleSuppressionScheduleRecurrenceDaily",
    "MonitorAlertProcessingRuleSuppressionScheduleRecurrenceDailyList",
    "MonitorAlertProcessingRuleSuppressionScheduleRecurrenceDailyOutputReference",
    "MonitorAlertProcessingRuleSuppressionScheduleRecurrenceMonthly",
    "MonitorAlertProcessingRuleSuppressionScheduleRecurrenceMonthlyList",
    "MonitorAlertProcessingRuleSuppressionScheduleRecurrenceMonthlyOutputReference",
    "MonitorAlertProcessingRuleSuppressionScheduleRecurrenceOutputReference",
    "MonitorAlertProcessingRuleSuppressionScheduleRecurrenceWeekly",
    "MonitorAlertProcessingRuleSuppressionScheduleRecurrenceWeeklyList",
    "MonitorAlertProcessingRuleSuppressionScheduleRecurrenceWeeklyOutputReference",
    "MonitorAlertProcessingRuleSuppressionTimeouts",
    "MonitorAlertProcessingRuleSuppressionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f2d21e765cf429c7c82ff06f1cdf4bb9029f079eacbd9616564e99d612766be1(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    resource_group_name: builtins.str,
    scopes: typing.Sequence[builtins.str],
    condition: typing.Optional[typing.Union[MonitorAlertProcessingRuleSuppressionCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[typing.Union[MonitorAlertProcessingRuleSuppressionSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MonitorAlertProcessingRuleSuppressionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__df753cd385f27b209508fca60e94846350fd98b431143167e6b7da4e3369cdcb(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__575b6602c5832bdb6f2f3c23dab7ab87b1e921adc5024994090d99b20d6007a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0730fa8f874fc56e0b0a3890a44cfba682cfa36635a84b070cbf70e30f5bbf6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b647b757c8a7248238e1f0dacbcc4c7213876daf314d455c4890fbe6da169a96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2012d1d3c30ccd50c83f2b5d0d97e3277a2b4e6b8b6a0515e8c183e55b70409(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c806e23a117dffccf9737258908a893cb0d6751b216fdf67250b08792f7251eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__973aee75c58c71b97d99d8943c3af1ad12c3ac01e22219ce9b62a8c1a4e47e11(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__212d4fcb91792d5e85efcc8cfb10fa50421f4e3be711b9b357ac93dca91cc44d(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1999dfd4a98c9495fdfeeec27b193fd7e9520b5f5c5361d3c90d05406e8ed348(
    *,
    alert_context: typing.Optional[typing.Union[MonitorAlertProcessingRuleSuppressionConditionAlertContext, typing.Dict[builtins.str, typing.Any]]] = None,
    alert_rule_id: typing.Optional[typing.Union[MonitorAlertProcessingRuleSuppressionConditionAlertRuleId, typing.Dict[builtins.str, typing.Any]]] = None,
    alert_rule_name: typing.Optional[typing.Union[MonitorAlertProcessingRuleSuppressionConditionAlertRuleName, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[typing.Union[MonitorAlertProcessingRuleSuppressionConditionDescription, typing.Dict[builtins.str, typing.Any]]] = None,
    monitor_condition: typing.Optional[typing.Union[MonitorAlertProcessingRuleSuppressionConditionMonitorCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    monitor_service: typing.Optional[typing.Union[MonitorAlertProcessingRuleSuppressionConditionMonitorService, typing.Dict[builtins.str, typing.Any]]] = None,
    severity: typing.Optional[typing.Union[MonitorAlertProcessingRuleSuppressionConditionSeverity, typing.Dict[builtins.str, typing.Any]]] = None,
    signal_type: typing.Optional[typing.Union[MonitorAlertProcessingRuleSuppressionConditionSignalType, typing.Dict[builtins.str, typing.Any]]] = None,
    target_resource: typing.Optional[typing.Union[MonitorAlertProcessingRuleSuppressionConditionTargetResource, typing.Dict[builtins.str, typing.Any]]] = None,
    target_resource_group: typing.Optional[typing.Union[MonitorAlertProcessingRuleSuppressionConditionTargetResourceGroup, typing.Dict[builtins.str, typing.Any]]] = None,
    target_resource_type: typing.Optional[typing.Union[MonitorAlertProcessingRuleSuppressionConditionTargetResourceType, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c06c9e4976fb79877a76083541005365719d6304af9cd31b17b1f12644e6121(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e64ccd444cf6281383bec6047eeb6bf789c5541e91e486a36b5d88efb4731cbd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6daa12244f8c76e4647b9a187eef2fdd07ba883bb466de6d5c6bad8bf70db606(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f93565074b99e97bdbb777d7e1c28562eb42a8fd4d7d7960a74421aa24b19ac1(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2e81e486877e26879106cccf4d49d182e287a792e117b427f081a1799fe3a04(
    value: typing.Optional[MonitorAlertProcessingRuleSuppressionConditionAlertContext],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6d610bd67251269717996276d0302e55c63086fda7cf056143e934f99df4398(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14122b72993ade0d18d28b0f02a9f28f3756c908f144a37b9ccdbf6e3ba97276(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dd0aa693c342e66fe5d2069bfe4954012886c4f0e9a17eb98c6d5f4d1590530(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d68c900b501e385c75aea5e18c9b98372be0bfb925ae63246e0c1d12a2779a80(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8369d6dcd89fe47a05ed27d0957c21c65b672348289cfdef158ba60b1e88375a(
    value: typing.Optional[MonitorAlertProcessingRuleSuppressionConditionAlertRuleId],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc3293230bb4cc883dabd0b822441d62b828fd42d65a4274ac75960b9775d437(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06cdfd79341be8ae3cd9eafd09edd372acee3a994490e43638855f6cde1b5a6b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07d26a82669b01fd4e4c4e002f7d2b7a2852f3549bd34bf029d26d2f50552549(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44208a3b50ac8e8894135af10e5a36b4e6883be1acac497128c501a3cff18e4c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edba7466f3ff9eb01069a1a231423f4d4928d9d51b4234339bdf2071869e5b36(
    value: typing.Optional[MonitorAlertProcessingRuleSuppressionConditionAlertRuleName],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16b8bfbab6842b91a16b839714be1bbce6cf2b82df027ec286fa9619129d2c7a(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8628f89f5ea4e642deab9e399aca8f67afd23fc1db7410f0fe9a4fec3576179b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1736aa5c8cc5e56af088968638b09c53074f75301edac236467b183c5ab619ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1ec4f66af05ef51c4a0ed4022b0e822bbc17ab8e3eb68b9c204e8ab2920d3cb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b91bd5bc2893911f3c237849650d3b450d7b0896c7eafa420e75d95f90eb90d6(
    value: typing.Optional[MonitorAlertProcessingRuleSuppressionConditionDescription],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__103568f0c3eeb21dc6ae99e134f9b7f1584c8674dc245c2faff86c9130eb4520(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e28d1506b9885886155f9dccb53c373c7e25d22ff912e3ada6ab9e90a62b657(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36b8ca69edea190d69fb1e4a7c966f761157b65b277702faebe6d21660a0f63d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20ec05f0d3e6e097cf10dbf5cdb80b74620f3707cf342bbb6c97097c49ccfb6e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd915a0db701b022c80e84ff193d3509f23f42cc0721e8907f4c1e696a023349(
    value: typing.Optional[MonitorAlertProcessingRuleSuppressionConditionMonitorCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fafc58b2aaba305e8e233ee4a01698fb3355ebb1a77642d1b9a54d039683d0f8(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67a1bf98b4ea8cb45d424bd97ea999f3a39fd745888f906e4e598ef2283f1492(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79dc98b1b5369bb79266c691cb130f2a2513c40cc873a24cbc81b201ea42e165(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac4a7f8b62be15f0de58009a475b4ca2ed567f27cd9362aaa0a57de0e33c2ebd(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f36f72cf9fc94fe40f01ec3a5b22f5f315e66b61c86a45e420dda1cacf897caf(
    value: typing.Optional[MonitorAlertProcessingRuleSuppressionConditionMonitorService],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91f2704d857828cbef79158f772ccdeb4d7be0d7379ce08978831993556c63ce(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45fbdba16646a28e919cba2832dd9c353d09b88b2a297fea93051cbdd359d8ba(
    value: typing.Optional[MonitorAlertProcessingRuleSuppressionCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56e343f1c173071935b741ce30930e0897fc0fc2380b102bc6bbb4ea53b704b5(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b401249f1b54dbd937effdfd92f8fe9e0d9c246c6de7597ff8d09819cfcc994(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2d86e162a36017d5219e65318e19b742f71a6ae7b0b53e1e13d7f975682ac2d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be6b090fcfaf973cf47600abfdf2a2aeadf24119e9d65bcd8df3d126a6f9e0c8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__091be877ae1b2847f33d0b7903dc6f04ff69bc3caa7c3dadfb624b2c3d4e30ff(
    value: typing.Optional[MonitorAlertProcessingRuleSuppressionConditionSeverity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50fd0d8389221bff6c07d16e9195a49126916d41975a60afd60ac3d2de5753c9(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a36c6a8d6754c110b8376c90b10f8d36f3db2fa8f55785ea75135af56dbd92e4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__586232f3941330030f9a19306ecf1e7050b5cb60fd8168becefafbae1aaeba3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__292a6fafd53d5479c122e47d64123789e45adb425f2936ad6a1086d40751afc6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfb6ff87b67e5c67aa177d775c088b44494d11a26a9c531dcca5b1fe70a40037(
    value: typing.Optional[MonitorAlertProcessingRuleSuppressionConditionSignalType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21dae9bfacb883a4adb81deb512e6e24b0c7fc24c37db8b3ff895da6cfbb83bd(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__263ca34d6fdb4a1de99adfa087c060d54ec8fa2baaf7afe2245cb65358405b9a(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfc66dde1338975549486bbe7aff023f5ed38022bcb267f708e9c5b776b6e016(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__579bc08168a8398d921f82e6ae9e5df1872e0b88b4efd7b6e361576bc742514f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8814af306e0765557239d8c1948e6f789ab737de9c1e6a90b4be610532ce9c31(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba0b516028acc84cafbaec1f11200aee7e8ae4dd709017ed1d3d9f03d7ef941d(
    value: typing.Optional[MonitorAlertProcessingRuleSuppressionConditionTargetResourceGroup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1f400d925197e2c081f43345826f8aeeb06193b1a341f06d9564b0be2681dad(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4bea3c48ee2b81247224ae75a40d6d395cc79e313f4d9dbc00dea6bc64a0c113(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__593984634e803a2dfae64525dbb30a90201a486a752c26fb60b7862357c29f25(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b7b24d4e0fc998e576a098a1131dd4025ff4f36ff3ba0446970d920481c3697(
    value: typing.Optional[MonitorAlertProcessingRuleSuppressionConditionTargetResource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a23f1d0d219b5008e0076ac260270ea504024630e286755936d2bd432166d810(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3db35bb63246a6d98db782ad4b4345e21728c04add8876640445829a4f9d6af1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d3a6848770402b4506bfbd6563714916e514e72657402c5d85470eb6733c796(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c717d84eb636bbc364d450890edda09fc17310781f1dccc7a08ccf0e5a03ea7b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40cf6408c7a5db5be5bf859328840a9a6589faeb462efd79334ca248ffeea379(
    value: typing.Optional[MonitorAlertProcessingRuleSuppressionConditionTargetResourceType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62a24bbfcee9fc379f371ae91590305a4fa15d07ddf559ba9578fbdfde7edb2f(
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
    condition: typing.Optional[typing.Union[MonitorAlertProcessingRuleSuppressionCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[typing.Union[MonitorAlertProcessingRuleSuppressionSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MonitorAlertProcessingRuleSuppressionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28503f5c8d76e74e3575933635d08441430d1ba3adadb08d5e5f50cd00c55c3e(
    *,
    effective_from: typing.Optional[builtins.str] = None,
    effective_until: typing.Optional[builtins.str] = None,
    recurrence: typing.Optional[typing.Union[MonitorAlertProcessingRuleSuppressionScheduleRecurrence, typing.Dict[builtins.str, typing.Any]]] = None,
    time_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a93beab1cff24598d62ec6172ff54884492f1babcbb9a72dfe83c56fa3c839a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e339261ab11e6d4fc3b54282b7739815b7419951bb90d1f927f73473a2705a99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f22ec339d92e4c6b64905ad580b8d9c487764c2c0456f3d33826a7b5cca032b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cdf237962215f5bac46b9e81686510a51847b4b8b0eed98de902ef9277d0352(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65195a3516a81bf551d0ae8072958733bac31cd6b5b1553c5fe49c9df918c07a(
    value: typing.Optional[MonitorAlertProcessingRuleSuppressionSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__552c0eee748170c871ea03b9b6d49336f5ce79822d8458681415e6413f9be7fd(
    *,
    daily: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorAlertProcessingRuleSuppressionScheduleRecurrenceDaily, typing.Dict[builtins.str, typing.Any]]]]] = None,
    monthly: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorAlertProcessingRuleSuppressionScheduleRecurrenceMonthly, typing.Dict[builtins.str, typing.Any]]]]] = None,
    weekly: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorAlertProcessingRuleSuppressionScheduleRecurrenceWeekly, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd0318eba3c0368af4c7032ea1612aed57dad8ffc1c6b332d52ce70500f3142f(
    *,
    end_time: builtins.str,
    start_time: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab2467c6c40fe358d41f3105935d847d115df9657ddbdfa176cf08b72b0249a4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c59096b12cb043aade7d64e51b378224ca79c7ea0dbb089c1e77474ba5ef2064(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b10fbeb3a3b832529fda6bdfbb8c6a6b4834433dd0ac1c0a5a526e1a053ac922(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4062cbae95db82e07756b21c2aa78f1137369c1176754463c6e5f75c0695c5e8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f781b4dc12fb1e9e997ac646cb1e30c5127be0c27f6c384ac4a968e31373bf88(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96aba3ba4e782c77a5b52df2bd44dbe21ef3c51ad45df59144425082fc7c9ef6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAlertProcessingRuleSuppressionScheduleRecurrenceDaily]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5df8cad0d678bc380f51df465f19a015c94c1340ee3d7e9059cd398943a3b578(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81de65995637499578873acbb27205857ec38cfc4e60acfcf98e5d336230bd0c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0810226843c6997fcd4afa720154dc9c9b2d5ce0340de442de66ddb699374a92(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fd368811bc3e861ff3f94b5f9c6a00d018ef6500ede9c3243358f25c9891d86(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAlertProcessingRuleSuppressionScheduleRecurrenceDaily]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__453b4b61ba8a16282dceb9552f81d320dbd94f78352c2d11d7d792dae008c8bb(
    *,
    days_of_month: typing.Sequence[jsii.Number],
    end_time: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c73db77351f3c1dcbebe2c383d23f1e9d1e45753bea885763333121abf5e2a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3d9aa5855a62b769b69226a74d77744f0ec8e4ac381b4ca1caf5a8b3369b672(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20e1c8feb3e279f8d66ac685cf14ce356b9868a111fbe5a4feeec4f3f3b1614d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fd7a396ff47d033ccbf214d1e269d71708b0c6a3f7d99e60af41b15228606f3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__656ef66f70b8094bead20dcc0561f42998464b0fd685ca5a89b2eca14a6902be(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d50415bb3e9a2c2a54d0ab7cf3cec3835d6cbf187583d75f8bdf149afba890ed(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAlertProcessingRuleSuppressionScheduleRecurrenceMonthly]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb6118f85db3954647c9582405818a38af9d548ec19b692d284a81c864524a3d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17509d334a8c0c87998f2e0943ac9428e80d4162ae65ebee8ec9e65775ffa763(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f49877588757d461e2ce5b9a08025dfaaee8d8e1588a80e619b3cea52f56f63(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fe5adde7feb1515a4f935c840f49b54c8ff9b38ddb873e2ca91ddf2002fb852(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fafd893b005bd7cdd982062007f0e6df30592fb7b378cf396d940828b0cddc5b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAlertProcessingRuleSuppressionScheduleRecurrenceMonthly]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__458b500414966f6bae4e3b5ce368b5091b7490c08be9ab3761599a44f93a123d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__080e8b51681c3f55b2e40b899adae43a2140ac927c830462ce457cbe02036f18(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorAlertProcessingRuleSuppressionScheduleRecurrenceDaily, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__036f10de6c4363a7d4e55895a5e09e6a248533484eaeb456b3bc97a90e539480(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorAlertProcessingRuleSuppressionScheduleRecurrenceMonthly, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cdec8d66d2b510579eb3786d523bf5d9a9927e2737bae2c01571a926027f36c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorAlertProcessingRuleSuppressionScheduleRecurrenceWeekly, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aba7d0897d7cfe76a18e2065432b0199a76aaf300d98ee44bccc146e6f22ae1(
    value: typing.Optional[MonitorAlertProcessingRuleSuppressionScheduleRecurrence],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4c5c790fb92796292c6b29e81cd4e06f52ae1c8ecfc96595eeca82089383c5b(
    *,
    days_of_week: typing.Sequence[builtins.str],
    end_time: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3ca0caa3a720e601282a4f5c1661d4a05037b6ca0ba0a396aca2b39acdec008(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b726fbeb21b19b9b7451c7b5b811f38a8f27debccc0a058ab1730eb0d5e70dd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__073ee8a112d2fd8419610f76ac560c495cce039f7dc634403cd1ffb705ca7453(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb6bc1581a45f1380fbbc8297341244d22a492ac15edcc4c415da195f8e41a61(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dea3899593e419c0a272364e23963d61934f873d8672f98c5f876c8a36a39f1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5bae8e5044428ccdea4e209996e95898b8f8f4b50f5ac30932cb27e2f976bb9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAlertProcessingRuleSuppressionScheduleRecurrenceWeekly]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1045e1bf1afee6750b5bd15d7fca97e78f9557d0f883c429edc8bea12d6794b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee9194eae02433c7cf5e25b764e01830bb62e66cca5d99aafbfc8bad1fffd3e5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdd5dbe77bf948afb18c52e43825c81f2483c04ce5ff79f12c9a129158771b98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1a3d3fd9ba18a1d4ca01de2bf6cd4fc3ca2b34ce46c9adec0048e5bbd3b3411(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eccd5e2091d8115f682b3c05e4c50236bac3b00309df44f61bc23e4cc116f733(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAlertProcessingRuleSuppressionScheduleRecurrenceWeekly]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__457f03ee759be3e8fc68aefda8482b5e493e6a9b37122b74545cb4bd946d804d(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0e0db104dc980c9493d529999d916d1247e96dd1672d503594caa36d60f690d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f754645511e70869188b40315e0ca62f0054fb84c683a662a251fff23605756a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffa67be650aa3ebf9b92c4a4eced535a97a39eb7c8242db7006a2e5848d3627e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c98d6725de94481968af00e19c8e17f42348d562e1ebbee852200e8e48931277(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77548c94eab260251d4f651e85375b3a9140e3d208196b680da3403eb617ff84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2140f9e511b600308062fe83ea745ebbc25d541e3da031375850b8ba1a56add1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAlertProcessingRuleSuppressionTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
