r'''
# `azurerm_monitor_alert_processing_rule_action_group`

Refer to the Terraform Registry for docs: [`azurerm_monitor_alert_processing_rule_action_group`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group).
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


class MonitorAlertProcessingRuleActionGroup(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroup",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group azurerm_monitor_alert_processing_rule_action_group}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        add_action_group_ids: typing.Sequence[builtins.str],
        name: builtins.str,
        resource_group_name: builtins.str,
        scopes: typing.Sequence[builtins.str],
        condition: typing.Optional[typing.Union["MonitorAlertProcessingRuleActionGroupCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[typing.Union["MonitorAlertProcessingRuleActionGroupSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MonitorAlertProcessingRuleActionGroupTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group azurerm_monitor_alert_processing_rule_action_group} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param add_action_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#add_action_group_ids MonitorAlertProcessingRuleActionGroup#add_action_group_ids}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#name MonitorAlertProcessingRuleActionGroup#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#resource_group_name MonitorAlertProcessingRuleActionGroup#resource_group_name}.
        :param scopes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#scopes MonitorAlertProcessingRuleActionGroup#scopes}.
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#condition MonitorAlertProcessingRuleActionGroup#condition}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#description MonitorAlertProcessingRuleActionGroup#description}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#enabled MonitorAlertProcessingRuleActionGroup#enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#id MonitorAlertProcessingRuleActionGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#schedule MonitorAlertProcessingRuleActionGroup#schedule}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#tags MonitorAlertProcessingRuleActionGroup#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#timeouts MonitorAlertProcessingRuleActionGroup#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79a0585d3d6c8b639f37a31ce3fb5e3b2488bbcf3adc76adec39e9c3d53e0f63)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MonitorAlertProcessingRuleActionGroupConfig(
            add_action_group_ids=add_action_group_ids,
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
        '''Generates CDKTF code for importing a MonitorAlertProcessingRuleActionGroup resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the MonitorAlertProcessingRuleActionGroup to import.
        :param import_from_id: The id of the existing MonitorAlertProcessingRuleActionGroup that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the MonitorAlertProcessingRuleActionGroup to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c4ba03ed7e805613bc775579646477e57d502bb5a3130bf86c3ab51c8afa12d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCondition")
    def put_condition(
        self,
        *,
        alert_context: typing.Optional[typing.Union["MonitorAlertProcessingRuleActionGroupConditionAlertContext", typing.Dict[builtins.str, typing.Any]]] = None,
        alert_rule_id: typing.Optional[typing.Union["MonitorAlertProcessingRuleActionGroupConditionAlertRuleId", typing.Dict[builtins.str, typing.Any]]] = None,
        alert_rule_name: typing.Optional[typing.Union["MonitorAlertProcessingRuleActionGroupConditionAlertRuleName", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[typing.Union["MonitorAlertProcessingRuleActionGroupConditionDescription", typing.Dict[builtins.str, typing.Any]]] = None,
        monitor_condition: typing.Optional[typing.Union["MonitorAlertProcessingRuleActionGroupConditionMonitorCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        monitor_service: typing.Optional[typing.Union["MonitorAlertProcessingRuleActionGroupConditionMonitorService", typing.Dict[builtins.str, typing.Any]]] = None,
        severity: typing.Optional[typing.Union["MonitorAlertProcessingRuleActionGroupConditionSeverity", typing.Dict[builtins.str, typing.Any]]] = None,
        signal_type: typing.Optional[typing.Union["MonitorAlertProcessingRuleActionGroupConditionSignalType", typing.Dict[builtins.str, typing.Any]]] = None,
        target_resource: typing.Optional[typing.Union["MonitorAlertProcessingRuleActionGroupConditionTargetResource", typing.Dict[builtins.str, typing.Any]]] = None,
        target_resource_group: typing.Optional[typing.Union["MonitorAlertProcessingRuleActionGroupConditionTargetResourceGroup", typing.Dict[builtins.str, typing.Any]]] = None,
        target_resource_type: typing.Optional[typing.Union["MonitorAlertProcessingRuleActionGroupConditionTargetResourceType", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param alert_context: alert_context block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#alert_context MonitorAlertProcessingRuleActionGroup#alert_context}
        :param alert_rule_id: alert_rule_id block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#alert_rule_id MonitorAlertProcessingRuleActionGroup#alert_rule_id}
        :param alert_rule_name: alert_rule_name block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#alert_rule_name MonitorAlertProcessingRuleActionGroup#alert_rule_name}
        :param description: description block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#description MonitorAlertProcessingRuleActionGroup#description}
        :param monitor_condition: monitor_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#monitor_condition MonitorAlertProcessingRuleActionGroup#monitor_condition}
        :param monitor_service: monitor_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#monitor_service MonitorAlertProcessingRuleActionGroup#monitor_service}
        :param severity: severity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#severity MonitorAlertProcessingRuleActionGroup#severity}
        :param signal_type: signal_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#signal_type MonitorAlertProcessingRuleActionGroup#signal_type}
        :param target_resource: target_resource block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#target_resource MonitorAlertProcessingRuleActionGroup#target_resource}
        :param target_resource_group: target_resource_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#target_resource_group MonitorAlertProcessingRuleActionGroup#target_resource_group}
        :param target_resource_type: target_resource_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#target_resource_type MonitorAlertProcessingRuleActionGroup#target_resource_type}
        '''
        value = MonitorAlertProcessingRuleActionGroupCondition(
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
        recurrence: typing.Optional[typing.Union["MonitorAlertProcessingRuleActionGroupScheduleRecurrence", typing.Dict[builtins.str, typing.Any]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param effective_from: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#effective_from MonitorAlertProcessingRuleActionGroup#effective_from}.
        :param effective_until: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#effective_until MonitorAlertProcessingRuleActionGroup#effective_until}.
        :param recurrence: recurrence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#recurrence MonitorAlertProcessingRuleActionGroup#recurrence}
        :param time_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#time_zone MonitorAlertProcessingRuleActionGroup#time_zone}.
        '''
        value = MonitorAlertProcessingRuleActionGroupSchedule(
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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#create MonitorAlertProcessingRuleActionGroup#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#delete MonitorAlertProcessingRuleActionGroup#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#read MonitorAlertProcessingRuleActionGroup#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#update MonitorAlertProcessingRuleActionGroup#update}.
        '''
        value = MonitorAlertProcessingRuleActionGroupTimeouts(
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
    ) -> "MonitorAlertProcessingRuleActionGroupConditionOutputReference":
        return typing.cast("MonitorAlertProcessingRuleActionGroupConditionOutputReference", jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(
        self,
    ) -> "MonitorAlertProcessingRuleActionGroupScheduleOutputReference":
        return typing.cast("MonitorAlertProcessingRuleActionGroupScheduleOutputReference", jsii.get(self, "schedule"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(
        self,
    ) -> "MonitorAlertProcessingRuleActionGroupTimeoutsOutputReference":
        return typing.cast("MonitorAlertProcessingRuleActionGroupTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="addActionGroupIdsInput")
    def add_action_group_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "addActionGroupIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleActionGroupCondition"]:
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleActionGroupCondition"], jsii.get(self, "conditionInput"))

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
    ) -> typing.Optional["MonitorAlertProcessingRuleActionGroupSchedule"]:
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleActionGroupSchedule"], jsii.get(self, "scheduleInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MonitorAlertProcessingRuleActionGroupTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "MonitorAlertProcessingRuleActionGroupTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="addActionGroupIds")
    def add_action_group_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "addActionGroupIds"))

    @add_action_group_ids.setter
    def add_action_group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ac1384b2f0f352cb19028eda4d80e23fb386d4fad24cbc842894a9c9cf7e9df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "addActionGroupIds", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ad6d8dbd63b2ce7c9bd323fb45892f6326575680b00bc8f06898b45ce64a0bf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__07f59fd655c0e616c6e8325ea60137e6398acc2aed4cc9ef0f10d786524810db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ee8d91a3cef0fd88cdbf01e989ad76c1ba03db20f5d1e4bfec8203a2d5c51a9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd44a3dc8925d3398790305b66de664ba0d9acef6c677c3d9879a1f00097f6ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa568cd68e42238666169928ed8d4e691e11f74a008ed9ac15638db739b60b4c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scopes"))

    @scopes.setter
    def scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__406b0e466eebe2f6b14c2b5cb7d436ac3c4e8f5d8147c63de08fb5f29bc2cf6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bce8269ece5ed11470d1bae26b8485e9ea1fa25ddf5a6a99b5cbd95f6efacd25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupCondition",
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
class MonitorAlertProcessingRuleActionGroupCondition:
    def __init__(
        self,
        *,
        alert_context: typing.Optional[typing.Union["MonitorAlertProcessingRuleActionGroupConditionAlertContext", typing.Dict[builtins.str, typing.Any]]] = None,
        alert_rule_id: typing.Optional[typing.Union["MonitorAlertProcessingRuleActionGroupConditionAlertRuleId", typing.Dict[builtins.str, typing.Any]]] = None,
        alert_rule_name: typing.Optional[typing.Union["MonitorAlertProcessingRuleActionGroupConditionAlertRuleName", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[typing.Union["MonitorAlertProcessingRuleActionGroupConditionDescription", typing.Dict[builtins.str, typing.Any]]] = None,
        monitor_condition: typing.Optional[typing.Union["MonitorAlertProcessingRuleActionGroupConditionMonitorCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        monitor_service: typing.Optional[typing.Union["MonitorAlertProcessingRuleActionGroupConditionMonitorService", typing.Dict[builtins.str, typing.Any]]] = None,
        severity: typing.Optional[typing.Union["MonitorAlertProcessingRuleActionGroupConditionSeverity", typing.Dict[builtins.str, typing.Any]]] = None,
        signal_type: typing.Optional[typing.Union["MonitorAlertProcessingRuleActionGroupConditionSignalType", typing.Dict[builtins.str, typing.Any]]] = None,
        target_resource: typing.Optional[typing.Union["MonitorAlertProcessingRuleActionGroupConditionTargetResource", typing.Dict[builtins.str, typing.Any]]] = None,
        target_resource_group: typing.Optional[typing.Union["MonitorAlertProcessingRuleActionGroupConditionTargetResourceGroup", typing.Dict[builtins.str, typing.Any]]] = None,
        target_resource_type: typing.Optional[typing.Union["MonitorAlertProcessingRuleActionGroupConditionTargetResourceType", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param alert_context: alert_context block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#alert_context MonitorAlertProcessingRuleActionGroup#alert_context}
        :param alert_rule_id: alert_rule_id block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#alert_rule_id MonitorAlertProcessingRuleActionGroup#alert_rule_id}
        :param alert_rule_name: alert_rule_name block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#alert_rule_name MonitorAlertProcessingRuleActionGroup#alert_rule_name}
        :param description: description block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#description MonitorAlertProcessingRuleActionGroup#description}
        :param monitor_condition: monitor_condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#monitor_condition MonitorAlertProcessingRuleActionGroup#monitor_condition}
        :param monitor_service: monitor_service block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#monitor_service MonitorAlertProcessingRuleActionGroup#monitor_service}
        :param severity: severity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#severity MonitorAlertProcessingRuleActionGroup#severity}
        :param signal_type: signal_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#signal_type MonitorAlertProcessingRuleActionGroup#signal_type}
        :param target_resource: target_resource block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#target_resource MonitorAlertProcessingRuleActionGroup#target_resource}
        :param target_resource_group: target_resource_group block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#target_resource_group MonitorAlertProcessingRuleActionGroup#target_resource_group}
        :param target_resource_type: target_resource_type block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#target_resource_type MonitorAlertProcessingRuleActionGroup#target_resource_type}
        '''
        if isinstance(alert_context, dict):
            alert_context = MonitorAlertProcessingRuleActionGroupConditionAlertContext(**alert_context)
        if isinstance(alert_rule_id, dict):
            alert_rule_id = MonitorAlertProcessingRuleActionGroupConditionAlertRuleId(**alert_rule_id)
        if isinstance(alert_rule_name, dict):
            alert_rule_name = MonitorAlertProcessingRuleActionGroupConditionAlertRuleName(**alert_rule_name)
        if isinstance(description, dict):
            description = MonitorAlertProcessingRuleActionGroupConditionDescription(**description)
        if isinstance(monitor_condition, dict):
            monitor_condition = MonitorAlertProcessingRuleActionGroupConditionMonitorCondition(**monitor_condition)
        if isinstance(monitor_service, dict):
            monitor_service = MonitorAlertProcessingRuleActionGroupConditionMonitorService(**monitor_service)
        if isinstance(severity, dict):
            severity = MonitorAlertProcessingRuleActionGroupConditionSeverity(**severity)
        if isinstance(signal_type, dict):
            signal_type = MonitorAlertProcessingRuleActionGroupConditionSignalType(**signal_type)
        if isinstance(target_resource, dict):
            target_resource = MonitorAlertProcessingRuleActionGroupConditionTargetResource(**target_resource)
        if isinstance(target_resource_group, dict):
            target_resource_group = MonitorAlertProcessingRuleActionGroupConditionTargetResourceGroup(**target_resource_group)
        if isinstance(target_resource_type, dict):
            target_resource_type = MonitorAlertProcessingRuleActionGroupConditionTargetResourceType(**target_resource_type)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c8838b2602a7c5b693251e6aa669e165ebc6c0ff1087dce01f731aacb142223)
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
    ) -> typing.Optional["MonitorAlertProcessingRuleActionGroupConditionAlertContext"]:
        '''alert_context block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#alert_context MonitorAlertProcessingRuleActionGroup#alert_context}
        '''
        result = self._values.get("alert_context")
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleActionGroupConditionAlertContext"], result)

    @builtins.property
    def alert_rule_id(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleActionGroupConditionAlertRuleId"]:
        '''alert_rule_id block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#alert_rule_id MonitorAlertProcessingRuleActionGroup#alert_rule_id}
        '''
        result = self._values.get("alert_rule_id")
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleActionGroupConditionAlertRuleId"], result)

    @builtins.property
    def alert_rule_name(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleActionGroupConditionAlertRuleName"]:
        '''alert_rule_name block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#alert_rule_name MonitorAlertProcessingRuleActionGroup#alert_rule_name}
        '''
        result = self._values.get("alert_rule_name")
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleActionGroupConditionAlertRuleName"], result)

    @builtins.property
    def description(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleActionGroupConditionDescription"]:
        '''description block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#description MonitorAlertProcessingRuleActionGroup#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleActionGroupConditionDescription"], result)

    @builtins.property
    def monitor_condition(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleActionGroupConditionMonitorCondition"]:
        '''monitor_condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#monitor_condition MonitorAlertProcessingRuleActionGroup#monitor_condition}
        '''
        result = self._values.get("monitor_condition")
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleActionGroupConditionMonitorCondition"], result)

    @builtins.property
    def monitor_service(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleActionGroupConditionMonitorService"]:
        '''monitor_service block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#monitor_service MonitorAlertProcessingRuleActionGroup#monitor_service}
        '''
        result = self._values.get("monitor_service")
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleActionGroupConditionMonitorService"], result)

    @builtins.property
    def severity(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleActionGroupConditionSeverity"]:
        '''severity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#severity MonitorAlertProcessingRuleActionGroup#severity}
        '''
        result = self._values.get("severity")
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleActionGroupConditionSeverity"], result)

    @builtins.property
    def signal_type(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleActionGroupConditionSignalType"]:
        '''signal_type block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#signal_type MonitorAlertProcessingRuleActionGroup#signal_type}
        '''
        result = self._values.get("signal_type")
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleActionGroupConditionSignalType"], result)

    @builtins.property
    def target_resource(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleActionGroupConditionTargetResource"]:
        '''target_resource block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#target_resource MonitorAlertProcessingRuleActionGroup#target_resource}
        '''
        result = self._values.get("target_resource")
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleActionGroupConditionTargetResource"], result)

    @builtins.property
    def target_resource_group(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleActionGroupConditionTargetResourceGroup"]:
        '''target_resource_group block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#target_resource_group MonitorAlertProcessingRuleActionGroup#target_resource_group}
        '''
        result = self._values.get("target_resource_group")
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleActionGroupConditionTargetResourceGroup"], result)

    @builtins.property
    def target_resource_type(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleActionGroupConditionTargetResourceType"]:
        '''target_resource_type block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#target_resource_type MonitorAlertProcessingRuleActionGroup#target_resource_type}
        '''
        result = self._values.get("target_resource_type")
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleActionGroupConditionTargetResourceType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleActionGroupCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupConditionAlertContext",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorAlertProcessingRuleActionGroupConditionAlertContext:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#operator MonitorAlertProcessingRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#values MonitorAlertProcessingRuleActionGroup#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d5f9f8f9a4cb404d0a44017777ac5687214deea3181542bb6296e1afb09e4f4)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#operator MonitorAlertProcessingRuleActionGroup#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#values MonitorAlertProcessingRuleActionGroup#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleActionGroupConditionAlertContext(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAlertProcessingRuleActionGroupConditionAlertContextOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupConditionAlertContextOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6a29965979d63d0889009dc3927da6ead217598b09bae18b1b8a3cb6c346a73c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d7390749ed1c12a473b0238e141e7e093e0ef7308ee6aef52b4560166b339bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__958a80f9edf8033dd6b4eb30f591de3891cb4a4f72a664082207e69344e8b31c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleActionGroupConditionAlertContext]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleActionGroupConditionAlertContext], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAlertProcessingRuleActionGroupConditionAlertContext],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e73f78afbb2c81173274ca5eb72ef057f98ed62998b312ffa0bb11944bc0da4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupConditionAlertRuleId",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorAlertProcessingRuleActionGroupConditionAlertRuleId:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#operator MonitorAlertProcessingRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#values MonitorAlertProcessingRuleActionGroup#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd5c2280636f5df2f3ff139f4ba91cd1b7ac44f1351c775dcd4da542ea3dcf05)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#operator MonitorAlertProcessingRuleActionGroup#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#values MonitorAlertProcessingRuleActionGroup#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleActionGroupConditionAlertRuleId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAlertProcessingRuleActionGroupConditionAlertRuleIdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupConditionAlertRuleIdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6209d3157abac734874b8e29d1ed0738285f1f186e32b998b50ab792b6f20c6f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b84842441842089b9dc3f40673bfa52da3f956be168b580ca2d739baca3c9c30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__643eed78cfdf4cf106c8de24233747705ce1377e4fd11b4451c1ae46ec46f236)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleActionGroupConditionAlertRuleId]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleActionGroupConditionAlertRuleId], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAlertProcessingRuleActionGroupConditionAlertRuleId],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90861a629eed755d97624342e96e93ffa82bf69ac24aacc6228af96d87995f26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupConditionAlertRuleName",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorAlertProcessingRuleActionGroupConditionAlertRuleName:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#operator MonitorAlertProcessingRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#values MonitorAlertProcessingRuleActionGroup#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7edda79423fe9364636f8444c2bb91f15f5ca3396a9be04ebdb435376175750)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#operator MonitorAlertProcessingRuleActionGroup#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#values MonitorAlertProcessingRuleActionGroup#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleActionGroupConditionAlertRuleName(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAlertProcessingRuleActionGroupConditionAlertRuleNameOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupConditionAlertRuleNameOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__33b615ff2d57a71acf54d69e22115577bedf7a8b96c3e1c139f9410dba227e10)
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
            type_hints = typing.get_type_hints(_typecheckingstub__366de7ff26094a579eb0daa029b96787ddda7327c1cc00f54d0feaa71e64be08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__148980d702a558c8c14e5b2ed0235efe5b0c8a0ece6fb97bde1391d87387ebe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleActionGroupConditionAlertRuleName]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleActionGroupConditionAlertRuleName], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAlertProcessingRuleActionGroupConditionAlertRuleName],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74c282ca65f194d0b21a04503fbc643fb94ffd04361f5e045e6d7468a0326edd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupConditionDescription",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorAlertProcessingRuleActionGroupConditionDescription:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#operator MonitorAlertProcessingRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#values MonitorAlertProcessingRuleActionGroup#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6369eb6ebaf8dd3d285b98b81c6f90805e89485246bc8ccd0d639913cef78639)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#operator MonitorAlertProcessingRuleActionGroup#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#values MonitorAlertProcessingRuleActionGroup#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleActionGroupConditionDescription(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAlertProcessingRuleActionGroupConditionDescriptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupConditionDescriptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2dafac8784376a9c5d87f7a4f0b989a0234116d3d4334fa51412c58e237eaa50)
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
            type_hints = typing.get_type_hints(_typecheckingstub__167a1f3d686d978c381c346c68bb841a6cd6a453825d1a645972e344431190d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__663a9e4b0e45e36f282073668b313308c6abb4926d7a72105c5f555a23a55739)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleActionGroupConditionDescription]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleActionGroupConditionDescription], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAlertProcessingRuleActionGroupConditionDescription],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b394cd7e33b609a25c6b09e62b65ea07b8c0469c48e68ac84b7182550d37da3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupConditionMonitorCondition",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorAlertProcessingRuleActionGroupConditionMonitorCondition:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#operator MonitorAlertProcessingRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#values MonitorAlertProcessingRuleActionGroup#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10851542037b975045fd17efa3cdb23793136ada534ed40882cc8116238e9cac)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#operator MonitorAlertProcessingRuleActionGroup#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#values MonitorAlertProcessingRuleActionGroup#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleActionGroupConditionMonitorCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAlertProcessingRuleActionGroupConditionMonitorConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupConditionMonitorConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__baa6e13162620148d59158b7b4fe9910da7a3433fe8de10ee7da562f4940895f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa9889d3caa16cf1ac0d92b048ffe3f0b5dcc99f05fc8de8ac7f6befbd5458d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e61999cffbd4f1e2fb5bd290c61316df15aaeba811fc89f6d09162ef16b490f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleActionGroupConditionMonitorCondition]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleActionGroupConditionMonitorCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAlertProcessingRuleActionGroupConditionMonitorCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4928d958500a3d2e198d3e2a2effe6dd3b7c2efc7524c328a5ff3bcad7bef2a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupConditionMonitorService",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorAlertProcessingRuleActionGroupConditionMonitorService:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#operator MonitorAlertProcessingRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#values MonitorAlertProcessingRuleActionGroup#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb3303d679fc2a94b026b445f3eca55c3771a3ce82cdf1453ba50e639da3255b)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#operator MonitorAlertProcessingRuleActionGroup#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#values MonitorAlertProcessingRuleActionGroup#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleActionGroupConditionMonitorService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAlertProcessingRuleActionGroupConditionMonitorServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupConditionMonitorServiceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a5aaad85b019c0635bc3c0f51b471252ae6b3735ea8eb53d3f3475b97eed4ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0c20b01e03d9f16ad66f3e3793bbb3a1ad69f8db4f2fa8e934f1e83b0d8b706)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8e3b78488d60266f0d4636c25199967312df143ce52123d581e581cde58b1f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleActionGroupConditionMonitorService]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleActionGroupConditionMonitorService], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAlertProcessingRuleActionGroupConditionMonitorService],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3414a62cea5d3d918563ed7d32a52230c1f740e7bd7f07b252614b57cabcfa3e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorAlertProcessingRuleActionGroupConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e1b7fa32b1700159bf1ecefb249ea1f39a303d2ba6f929025018dd07f26694f)
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
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#operator MonitorAlertProcessingRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#values MonitorAlertProcessingRuleActionGroup#values}.
        '''
        value = MonitorAlertProcessingRuleActionGroupConditionAlertContext(
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
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#operator MonitorAlertProcessingRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#values MonitorAlertProcessingRuleActionGroup#values}.
        '''
        value = MonitorAlertProcessingRuleActionGroupConditionAlertRuleId(
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
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#operator MonitorAlertProcessingRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#values MonitorAlertProcessingRuleActionGroup#values}.
        '''
        value = MonitorAlertProcessingRuleActionGroupConditionAlertRuleName(
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
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#operator MonitorAlertProcessingRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#values MonitorAlertProcessingRuleActionGroup#values}.
        '''
        value = MonitorAlertProcessingRuleActionGroupConditionDescription(
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
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#operator MonitorAlertProcessingRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#values MonitorAlertProcessingRuleActionGroup#values}.
        '''
        value = MonitorAlertProcessingRuleActionGroupConditionMonitorCondition(
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
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#operator MonitorAlertProcessingRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#values MonitorAlertProcessingRuleActionGroup#values}.
        '''
        value = MonitorAlertProcessingRuleActionGroupConditionMonitorService(
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
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#operator MonitorAlertProcessingRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#values MonitorAlertProcessingRuleActionGroup#values}.
        '''
        value = MonitorAlertProcessingRuleActionGroupConditionSeverity(
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
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#operator MonitorAlertProcessingRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#values MonitorAlertProcessingRuleActionGroup#values}.
        '''
        value = MonitorAlertProcessingRuleActionGroupConditionSignalType(
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
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#operator MonitorAlertProcessingRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#values MonitorAlertProcessingRuleActionGroup#values}.
        '''
        value = MonitorAlertProcessingRuleActionGroupConditionTargetResource(
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
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#operator MonitorAlertProcessingRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#values MonitorAlertProcessingRuleActionGroup#values}.
        '''
        value = MonitorAlertProcessingRuleActionGroupConditionTargetResourceGroup(
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
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#operator MonitorAlertProcessingRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#values MonitorAlertProcessingRuleActionGroup#values}.
        '''
        value = MonitorAlertProcessingRuleActionGroupConditionTargetResourceType(
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
    ) -> MonitorAlertProcessingRuleActionGroupConditionAlertContextOutputReference:
        return typing.cast(MonitorAlertProcessingRuleActionGroupConditionAlertContextOutputReference, jsii.get(self, "alertContext"))

    @builtins.property
    @jsii.member(jsii_name="alertRuleId")
    def alert_rule_id(
        self,
    ) -> MonitorAlertProcessingRuleActionGroupConditionAlertRuleIdOutputReference:
        return typing.cast(MonitorAlertProcessingRuleActionGroupConditionAlertRuleIdOutputReference, jsii.get(self, "alertRuleId"))

    @builtins.property
    @jsii.member(jsii_name="alertRuleName")
    def alert_rule_name(
        self,
    ) -> MonitorAlertProcessingRuleActionGroupConditionAlertRuleNameOutputReference:
        return typing.cast(MonitorAlertProcessingRuleActionGroupConditionAlertRuleNameOutputReference, jsii.get(self, "alertRuleName"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(
        self,
    ) -> MonitorAlertProcessingRuleActionGroupConditionDescriptionOutputReference:
        return typing.cast(MonitorAlertProcessingRuleActionGroupConditionDescriptionOutputReference, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="monitorCondition")
    def monitor_condition(
        self,
    ) -> MonitorAlertProcessingRuleActionGroupConditionMonitorConditionOutputReference:
        return typing.cast(MonitorAlertProcessingRuleActionGroupConditionMonitorConditionOutputReference, jsii.get(self, "monitorCondition"))

    @builtins.property
    @jsii.member(jsii_name="monitorService")
    def monitor_service(
        self,
    ) -> MonitorAlertProcessingRuleActionGroupConditionMonitorServiceOutputReference:
        return typing.cast(MonitorAlertProcessingRuleActionGroupConditionMonitorServiceOutputReference, jsii.get(self, "monitorService"))

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(
        self,
    ) -> "MonitorAlertProcessingRuleActionGroupConditionSeverityOutputReference":
        return typing.cast("MonitorAlertProcessingRuleActionGroupConditionSeverityOutputReference", jsii.get(self, "severity"))

    @builtins.property
    @jsii.member(jsii_name="signalType")
    def signal_type(
        self,
    ) -> "MonitorAlertProcessingRuleActionGroupConditionSignalTypeOutputReference":
        return typing.cast("MonitorAlertProcessingRuleActionGroupConditionSignalTypeOutputReference", jsii.get(self, "signalType"))

    @builtins.property
    @jsii.member(jsii_name="targetResource")
    def target_resource(
        self,
    ) -> "MonitorAlertProcessingRuleActionGroupConditionTargetResourceOutputReference":
        return typing.cast("MonitorAlertProcessingRuleActionGroupConditionTargetResourceOutputReference", jsii.get(self, "targetResource"))

    @builtins.property
    @jsii.member(jsii_name="targetResourceGroup")
    def target_resource_group(
        self,
    ) -> "MonitorAlertProcessingRuleActionGroupConditionTargetResourceGroupOutputReference":
        return typing.cast("MonitorAlertProcessingRuleActionGroupConditionTargetResourceGroupOutputReference", jsii.get(self, "targetResourceGroup"))

    @builtins.property
    @jsii.member(jsii_name="targetResourceType")
    def target_resource_type(
        self,
    ) -> "MonitorAlertProcessingRuleActionGroupConditionTargetResourceTypeOutputReference":
        return typing.cast("MonitorAlertProcessingRuleActionGroupConditionTargetResourceTypeOutputReference", jsii.get(self, "targetResourceType"))

    @builtins.property
    @jsii.member(jsii_name="alertContextInput")
    def alert_context_input(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleActionGroupConditionAlertContext]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleActionGroupConditionAlertContext], jsii.get(self, "alertContextInput"))

    @builtins.property
    @jsii.member(jsii_name="alertRuleIdInput")
    def alert_rule_id_input(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleActionGroupConditionAlertRuleId]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleActionGroupConditionAlertRuleId], jsii.get(self, "alertRuleIdInput"))

    @builtins.property
    @jsii.member(jsii_name="alertRuleNameInput")
    def alert_rule_name_input(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleActionGroupConditionAlertRuleName]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleActionGroupConditionAlertRuleName], jsii.get(self, "alertRuleNameInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleActionGroupConditionDescription]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleActionGroupConditionDescription], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorConditionInput")
    def monitor_condition_input(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleActionGroupConditionMonitorCondition]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleActionGroupConditionMonitorCondition], jsii.get(self, "monitorConditionInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorServiceInput")
    def monitor_service_input(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleActionGroupConditionMonitorService]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleActionGroupConditionMonitorService], jsii.get(self, "monitorServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="severityInput")
    def severity_input(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleActionGroupConditionSeverity"]:
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleActionGroupConditionSeverity"], jsii.get(self, "severityInput"))

    @builtins.property
    @jsii.member(jsii_name="signalTypeInput")
    def signal_type_input(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleActionGroupConditionSignalType"]:
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleActionGroupConditionSignalType"], jsii.get(self, "signalTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="targetResourceGroupInput")
    def target_resource_group_input(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleActionGroupConditionTargetResourceGroup"]:
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleActionGroupConditionTargetResourceGroup"], jsii.get(self, "targetResourceGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="targetResourceInput")
    def target_resource_input(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleActionGroupConditionTargetResource"]:
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleActionGroupConditionTargetResource"], jsii.get(self, "targetResourceInput"))

    @builtins.property
    @jsii.member(jsii_name="targetResourceTypeInput")
    def target_resource_type_input(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleActionGroupConditionTargetResourceType"]:
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleActionGroupConditionTargetResourceType"], jsii.get(self, "targetResourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleActionGroupCondition]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleActionGroupCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAlertProcessingRuleActionGroupCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5927f744448b24d240ce8b76b93f7e2b2217b51589367c391d3beeb8b550352a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupConditionSeverity",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorAlertProcessingRuleActionGroupConditionSeverity:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#operator MonitorAlertProcessingRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#values MonitorAlertProcessingRuleActionGroup#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cefdeac143dec7c5b1cd4ff879a4e3347791b12d920f0784478ccc7b47c1a75b)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#operator MonitorAlertProcessingRuleActionGroup#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#values MonitorAlertProcessingRuleActionGroup#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleActionGroupConditionSeverity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAlertProcessingRuleActionGroupConditionSeverityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupConditionSeverityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0bf332b2d38ef833df786ed5c071f7f94dce7c2f84e7b974bd972e4182751168)
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
            type_hints = typing.get_type_hints(_typecheckingstub__388445fa4aafab9f6e61795ec83cffa3448bc38a20a93908343d83336a1d68ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f28778220f23ec21a937b54b60c067584a3dd90b5914aa81fcb58bf853ceb0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleActionGroupConditionSeverity]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleActionGroupConditionSeverity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAlertProcessingRuleActionGroupConditionSeverity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81ea48f6eec60439219e00e0a69bdb79cc53c3fb40c0eafbb8811ad22c13d816)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupConditionSignalType",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorAlertProcessingRuleActionGroupConditionSignalType:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#operator MonitorAlertProcessingRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#values MonitorAlertProcessingRuleActionGroup#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdc1b22cbbe934aafff67004d701585bc786f57b443b21e18604067c1423404b)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#operator MonitorAlertProcessingRuleActionGroup#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#values MonitorAlertProcessingRuleActionGroup#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleActionGroupConditionSignalType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAlertProcessingRuleActionGroupConditionSignalTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupConditionSignalTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__770b603b226703124e5709d165b208e6379394dabc7ce55f5d85e903c091e573)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8de6036cbd6fbfd4660556be6e5ea992fdbf9011c9344f3fa70a32d3ea6c18d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d13073e657b0a10cbbc544664b95c38a762ba08b6450d10688120563adbb4fb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleActionGroupConditionSignalType]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleActionGroupConditionSignalType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAlertProcessingRuleActionGroupConditionSignalType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__385673e0538eac5a028c656cc65a75c9fa1270d68c54a8afe9a52848ebd4ee42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupConditionTargetResource",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorAlertProcessingRuleActionGroupConditionTargetResource:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#operator MonitorAlertProcessingRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#values MonitorAlertProcessingRuleActionGroup#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39d3f2d155fe66e098e8bf778f10a688733e4899a9972febeb840649e5bac42d)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#operator MonitorAlertProcessingRuleActionGroup#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#values MonitorAlertProcessingRuleActionGroup#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleActionGroupConditionTargetResource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupConditionTargetResourceGroup",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorAlertProcessingRuleActionGroupConditionTargetResourceGroup:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#operator MonitorAlertProcessingRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#values MonitorAlertProcessingRuleActionGroup#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b3dbbf254fe4690c2e7c19be5af843312efc4c86e975a2fdeea240e8966aecd)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#operator MonitorAlertProcessingRuleActionGroup#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#values MonitorAlertProcessingRuleActionGroup#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleActionGroupConditionTargetResourceGroup(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAlertProcessingRuleActionGroupConditionTargetResourceGroupOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupConditionTargetResourceGroupOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__230aa727cc438e6075820f367c8f2858c2b2e31cb52a6a662e8642ab8c9c5640)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1ee5f9e5e242499102c0f8977ea7e55a326f32e2b01d6e1ed5c60f7026beefb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cac7969a5a717bbbdcdee069b4876401dee282c4a52c71f6664e9ea1462ee90d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleActionGroupConditionTargetResourceGroup]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleActionGroupConditionTargetResourceGroup], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAlertProcessingRuleActionGroupConditionTargetResourceGroup],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a5233d17158f5576deb7c3481b8e471840197796cb495e3452b7981efd76f24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorAlertProcessingRuleActionGroupConditionTargetResourceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupConditionTargetResourceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6c25c4a60aeecf221b84570d5e02d9337795cafa369f4d137fe4c0e024fdf806)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ba4b57d54032e2634f036ff47f906d911a6b4f1ac18946c9739f6d784a52c549)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__076cd84df1e75db3cc3e86bd62a1dbbde892cc48aeced6c3f3229b84ad236a4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleActionGroupConditionTargetResource]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleActionGroupConditionTargetResource], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAlertProcessingRuleActionGroupConditionTargetResource],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__126d702411fb89065de130abc9294cab8cd030dfb7359bbec9365953c3433fa2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupConditionTargetResourceType",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorAlertProcessingRuleActionGroupConditionTargetResourceType:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#operator MonitorAlertProcessingRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#values MonitorAlertProcessingRuleActionGroup#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5424d5e75bee1b5e278e3c64c2d4154a1c5ee1de8c2e70556b60177fbcda22d5)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#operator MonitorAlertProcessingRuleActionGroup#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#values MonitorAlertProcessingRuleActionGroup#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleActionGroupConditionTargetResourceType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAlertProcessingRuleActionGroupConditionTargetResourceTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupConditionTargetResourceTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d31f4174c4538c74d00cf65e8796ec0b368eefef91853effc1d0076a4cd92333)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6848c720ef30e2d345f24c85e8219c03fd1804d626c4985329745bf96cae1cfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfe5758706b38b98e062fbdff51c7746256e133d9e261975c237e79d814d7534)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleActionGroupConditionTargetResourceType]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleActionGroupConditionTargetResourceType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAlertProcessingRuleActionGroupConditionTargetResourceType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b9fd48ae4026ebebf0bf9b933e2430abb6c5b1465d186f03a9afd7846f62103)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "add_action_group_ids": "addActionGroupIds",
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
class MonitorAlertProcessingRuleActionGroupConfig(
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
        add_action_group_ids: typing.Sequence[builtins.str],
        name: builtins.str,
        resource_group_name: builtins.str,
        scopes: typing.Sequence[builtins.str],
        condition: typing.Optional[typing.Union[MonitorAlertProcessingRuleActionGroupCondition, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[typing.Union["MonitorAlertProcessingRuleActionGroupSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MonitorAlertProcessingRuleActionGroupTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param add_action_group_ids: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#add_action_group_ids MonitorAlertProcessingRuleActionGroup#add_action_group_ids}.
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#name MonitorAlertProcessingRuleActionGroup#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#resource_group_name MonitorAlertProcessingRuleActionGroup#resource_group_name}.
        :param scopes: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#scopes MonitorAlertProcessingRuleActionGroup#scopes}.
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#condition MonitorAlertProcessingRuleActionGroup#condition}
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#description MonitorAlertProcessingRuleActionGroup#description}.
        :param enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#enabled MonitorAlertProcessingRuleActionGroup#enabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#id MonitorAlertProcessingRuleActionGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#schedule MonitorAlertProcessingRuleActionGroup#schedule}
        :param tags: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#tags MonitorAlertProcessingRuleActionGroup#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#timeouts MonitorAlertProcessingRuleActionGroup#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(condition, dict):
            condition = MonitorAlertProcessingRuleActionGroupCondition(**condition)
        if isinstance(schedule, dict):
            schedule = MonitorAlertProcessingRuleActionGroupSchedule(**schedule)
        if isinstance(timeouts, dict):
            timeouts = MonitorAlertProcessingRuleActionGroupTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__371632eb16eb605ce77bee33ca6b0572e70215d6b1126d210855251806534ca9)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument add_action_group_ids", value=add_action_group_ids, expected_type=type_hints["add_action_group_ids"])
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
            "add_action_group_ids": add_action_group_ids,
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
    def add_action_group_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#add_action_group_ids MonitorAlertProcessingRuleActionGroup#add_action_group_ids}.'''
        result = self._values.get("add_action_group_ids")
        assert result is not None, "Required property 'add_action_group_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#name MonitorAlertProcessingRuleActionGroup#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#resource_group_name MonitorAlertProcessingRuleActionGroup#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scopes(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#scopes MonitorAlertProcessingRuleActionGroup#scopes}.'''
        result = self._values.get("scopes")
        assert result is not None, "Required property 'scopes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def condition(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleActionGroupCondition]:
        '''condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#condition MonitorAlertProcessingRuleActionGroup#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleActionGroupCondition], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#description MonitorAlertProcessingRuleActionGroup#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#enabled MonitorAlertProcessingRuleActionGroup#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#id MonitorAlertProcessingRuleActionGroup#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleActionGroupSchedule"]:
        '''schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#schedule MonitorAlertProcessingRuleActionGroup#schedule}
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleActionGroupSchedule"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#tags MonitorAlertProcessingRuleActionGroup#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleActionGroupTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#timeouts MonitorAlertProcessingRuleActionGroup#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleActionGroupTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleActionGroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupSchedule",
    jsii_struct_bases=[],
    name_mapping={
        "effective_from": "effectiveFrom",
        "effective_until": "effectiveUntil",
        "recurrence": "recurrence",
        "time_zone": "timeZone",
    },
)
class MonitorAlertProcessingRuleActionGroupSchedule:
    def __init__(
        self,
        *,
        effective_from: typing.Optional[builtins.str] = None,
        effective_until: typing.Optional[builtins.str] = None,
        recurrence: typing.Optional[typing.Union["MonitorAlertProcessingRuleActionGroupScheduleRecurrence", typing.Dict[builtins.str, typing.Any]]] = None,
        time_zone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param effective_from: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#effective_from MonitorAlertProcessingRuleActionGroup#effective_from}.
        :param effective_until: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#effective_until MonitorAlertProcessingRuleActionGroup#effective_until}.
        :param recurrence: recurrence block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#recurrence MonitorAlertProcessingRuleActionGroup#recurrence}
        :param time_zone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#time_zone MonitorAlertProcessingRuleActionGroup#time_zone}.
        '''
        if isinstance(recurrence, dict):
            recurrence = MonitorAlertProcessingRuleActionGroupScheduleRecurrence(**recurrence)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de78b30dd8e5b7543c0d433adebc3bec0b04cf80ba5e5739978873452452f8f1)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#effective_from MonitorAlertProcessingRuleActionGroup#effective_from}.'''
        result = self._values.get("effective_from")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def effective_until(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#effective_until MonitorAlertProcessingRuleActionGroup#effective_until}.'''
        result = self._values.get("effective_until")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recurrence(
        self,
    ) -> typing.Optional["MonitorAlertProcessingRuleActionGroupScheduleRecurrence"]:
        '''recurrence block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#recurrence MonitorAlertProcessingRuleActionGroup#recurrence}
        '''
        result = self._values.get("recurrence")
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleActionGroupScheduleRecurrence"], result)

    @builtins.property
    def time_zone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#time_zone MonitorAlertProcessingRuleActionGroup#time_zone}.'''
        result = self._values.get("time_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleActionGroupSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAlertProcessingRuleActionGroupScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce142ff9a2302d81f00430a45d29dc0aa08d305ca13a38b9a511e5dbe2acc478)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRecurrence")
    def put_recurrence(
        self,
        *,
        daily: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorAlertProcessingRuleActionGroupScheduleRecurrenceDaily", typing.Dict[builtins.str, typing.Any]]]]] = None,
        monthly: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorAlertProcessingRuleActionGroupScheduleRecurrenceMonthly", typing.Dict[builtins.str, typing.Any]]]]] = None,
        weekly: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorAlertProcessingRuleActionGroupScheduleRecurrenceWeekly", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param daily: daily block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#daily MonitorAlertProcessingRuleActionGroup#daily}
        :param monthly: monthly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#monthly MonitorAlertProcessingRuleActionGroup#monthly}
        :param weekly: weekly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#weekly MonitorAlertProcessingRuleActionGroup#weekly}
        '''
        value = MonitorAlertProcessingRuleActionGroupScheduleRecurrence(
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
    ) -> "MonitorAlertProcessingRuleActionGroupScheduleRecurrenceOutputReference":
        return typing.cast("MonitorAlertProcessingRuleActionGroupScheduleRecurrenceOutputReference", jsii.get(self, "recurrence"))

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
    ) -> typing.Optional["MonitorAlertProcessingRuleActionGroupScheduleRecurrence"]:
        return typing.cast(typing.Optional["MonitorAlertProcessingRuleActionGroupScheduleRecurrence"], jsii.get(self, "recurrenceInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__6b72c65731c0a154cd431f64bf6e306313f81ffbac814abb44920d8c1e9ddc14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effectiveFrom", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="effectiveUntil")
    def effective_until(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "effectiveUntil"))

    @effective_until.setter
    def effective_until(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a79a16038bbfdb148be16c6864b0f17857cf7d6804ae26bacc7e76600741f7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effectiveUntil", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad10abf64f1165a1446b870d3cd3ee759ddf9a95a18e4543da835237a766c1aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleActionGroupSchedule]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleActionGroupSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAlertProcessingRuleActionGroupSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__843cd4bd6969b162a2507e2a62a11a8dcd0f75cdb1df264f2921ffa5eefe33a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupScheduleRecurrence",
    jsii_struct_bases=[],
    name_mapping={"daily": "daily", "monthly": "monthly", "weekly": "weekly"},
)
class MonitorAlertProcessingRuleActionGroupScheduleRecurrence:
    def __init__(
        self,
        *,
        daily: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorAlertProcessingRuleActionGroupScheduleRecurrenceDaily", typing.Dict[builtins.str, typing.Any]]]]] = None,
        monthly: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorAlertProcessingRuleActionGroupScheduleRecurrenceMonthly", typing.Dict[builtins.str, typing.Any]]]]] = None,
        weekly: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorAlertProcessingRuleActionGroupScheduleRecurrenceWeekly", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param daily: daily block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#daily MonitorAlertProcessingRuleActionGroup#daily}
        :param monthly: monthly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#monthly MonitorAlertProcessingRuleActionGroup#monthly}
        :param weekly: weekly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#weekly MonitorAlertProcessingRuleActionGroup#weekly}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__758bf6f819bdb1c8f170a7edf6068cf634862265ff35f6d596f87549d4e96342)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorAlertProcessingRuleActionGroupScheduleRecurrenceDaily"]]]:
        '''daily block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#daily MonitorAlertProcessingRuleActionGroup#daily}
        '''
        result = self._values.get("daily")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorAlertProcessingRuleActionGroupScheduleRecurrenceDaily"]]], result)

    @builtins.property
    def monthly(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorAlertProcessingRuleActionGroupScheduleRecurrenceMonthly"]]]:
        '''monthly block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#monthly MonitorAlertProcessingRuleActionGroup#monthly}
        '''
        result = self._values.get("monthly")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorAlertProcessingRuleActionGroupScheduleRecurrenceMonthly"]]], result)

    @builtins.property
    def weekly(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorAlertProcessingRuleActionGroupScheduleRecurrenceWeekly"]]]:
        '''weekly block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#weekly MonitorAlertProcessingRuleActionGroup#weekly}
        '''
        result = self._values.get("weekly")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorAlertProcessingRuleActionGroupScheduleRecurrenceWeekly"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleActionGroupScheduleRecurrence(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupScheduleRecurrenceDaily",
    jsii_struct_bases=[],
    name_mapping={"end_time": "endTime", "start_time": "startTime"},
)
class MonitorAlertProcessingRuleActionGroupScheduleRecurrenceDaily:
    def __init__(self, *, end_time: builtins.str, start_time: builtins.str) -> None:
        '''
        :param end_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#end_time MonitorAlertProcessingRuleActionGroup#end_time}.
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#start_time MonitorAlertProcessingRuleActionGroup#start_time}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59587af70beb72623899de411d85d9aa0897e9eca278ef9c5b1d864c6392852b)
            check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end_time": end_time,
            "start_time": start_time,
        }

    @builtins.property
    def end_time(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#end_time MonitorAlertProcessingRuleActionGroup#end_time}.'''
        result = self._values.get("end_time")
        assert result is not None, "Required property 'end_time' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_time(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#start_time MonitorAlertProcessingRuleActionGroup#start_time}.'''
        result = self._values.get("start_time")
        assert result is not None, "Required property 'start_time' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleActionGroupScheduleRecurrenceDaily(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAlertProcessingRuleActionGroupScheduleRecurrenceDailyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupScheduleRecurrenceDailyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f36127365f277ac761d02762c415267af93f06739e85335c8c286eb664457e8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorAlertProcessingRuleActionGroupScheduleRecurrenceDailyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3e8c116326b43ade3f9c07aa162f92cb41f43ed674701443a4414aab063dbf2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorAlertProcessingRuleActionGroupScheduleRecurrenceDailyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79cd6df53c204d32a85528b3d6fd6c71a11430b9b34df096815695534bac380d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c559f6d17e49aa0383cc10c65c07e989e00ba3b8a917ebb82e79a10304a9759)
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
            type_hints = typing.get_type_hints(_typecheckingstub__32c31149ab59aee163c397c50654e0b7c88fdfe866b183bc7ec842288dac6a75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAlertProcessingRuleActionGroupScheduleRecurrenceDaily]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAlertProcessingRuleActionGroupScheduleRecurrenceDaily]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAlertProcessingRuleActionGroupScheduleRecurrenceDaily]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c548a6e93eaf16e43ea17977d23729df24600f39a81a61d980445806c2b3801)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorAlertProcessingRuleActionGroupScheduleRecurrenceDailyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupScheduleRecurrenceDailyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1d63caf273f5c6d3dc7f4f252463e915e13cd541e7a1f8ab2156fe97b481a05)
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
            type_hints = typing.get_type_hints(_typecheckingstub__924254ad590565921825653048501692ea35278827bae8d78ea0fe8179b1a885)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf2dc5f567d61a145cd57819ef54ae7c1104d86f97573d420093763e1bdc0ed0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAlertProcessingRuleActionGroupScheduleRecurrenceDaily]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAlertProcessingRuleActionGroupScheduleRecurrenceDaily]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAlertProcessingRuleActionGroupScheduleRecurrenceDaily]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d2602993d4029fcf43716771b950db44071ec8ef2a5c163bc8d4598a6c47c77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupScheduleRecurrenceMonthly",
    jsii_struct_bases=[],
    name_mapping={
        "days_of_month": "daysOfMonth",
        "end_time": "endTime",
        "start_time": "startTime",
    },
)
class MonitorAlertProcessingRuleActionGroupScheduleRecurrenceMonthly:
    def __init__(
        self,
        *,
        days_of_month: typing.Sequence[jsii.Number],
        end_time: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param days_of_month: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#days_of_month MonitorAlertProcessingRuleActionGroup#days_of_month}.
        :param end_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#end_time MonitorAlertProcessingRuleActionGroup#end_time}.
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#start_time MonitorAlertProcessingRuleActionGroup#start_time}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31fc76186242c11c3fa8850216ae6ff5ca86f2713b17faa65434482ff8c6dcac)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#days_of_month MonitorAlertProcessingRuleActionGroup#days_of_month}.'''
        result = self._values.get("days_of_month")
        assert result is not None, "Required property 'days_of_month' is missing"
        return typing.cast(typing.List[jsii.Number], result)

    @builtins.property
    def end_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#end_time MonitorAlertProcessingRuleActionGroup#end_time}.'''
        result = self._values.get("end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#start_time MonitorAlertProcessingRuleActionGroup#start_time}.'''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleActionGroupScheduleRecurrenceMonthly(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAlertProcessingRuleActionGroupScheduleRecurrenceMonthlyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupScheduleRecurrenceMonthlyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c79f488b6a2518e58017df75cc6117f3c1e2181aa843e63e357ed620b01a621b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorAlertProcessingRuleActionGroupScheduleRecurrenceMonthlyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47667ddf29ff096c638f5ec80e5c6535af608bd44469707ff4e936351029404d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorAlertProcessingRuleActionGroupScheduleRecurrenceMonthlyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83b27b55f92bb120bced459742a291b51bb22694dbc4f4af330825d4b5b30ece)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b4a121196ee9a620b15b335e9e5d1d84b2ebff4d62080e4a7dc057c0a807388)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c01be3928fcc43cdf32a3f4d1dd94933f507c693b119991240b4adfa73a66e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAlertProcessingRuleActionGroupScheduleRecurrenceMonthly]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAlertProcessingRuleActionGroupScheduleRecurrenceMonthly]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAlertProcessingRuleActionGroupScheduleRecurrenceMonthly]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e3d338a231360a5dda9c064698b9b13598e2a54101696c585241f7479d519c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorAlertProcessingRuleActionGroupScheduleRecurrenceMonthlyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupScheduleRecurrenceMonthlyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__51000417460e1a0e3d25a89a2b432a95f3ccb30f57cf913eb608449d9da31b55)
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
            type_hints = typing.get_type_hints(_typecheckingstub__66c0ad14b0a778eb4c4841c2b481634e6e831a4f6eaa0fff63d7c3319d8876bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysOfMonth", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @end_time.setter
    def end_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d611db5e50a87cb23251ce6f06f275ca715f8713e17c9a2f63cba89580422059)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fa9f0917ffa6d80d4378d86e9f45981a205308befb8265eb1658cf1d0b187f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAlertProcessingRuleActionGroupScheduleRecurrenceMonthly]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAlertProcessingRuleActionGroupScheduleRecurrenceMonthly]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAlertProcessingRuleActionGroupScheduleRecurrenceMonthly]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1063564c4d4575cba21e2cf3839442f88314b43d687db062706acf206c42bf36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorAlertProcessingRuleActionGroupScheduleRecurrenceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupScheduleRecurrenceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f435b7085ef927f6f77767b1d3c47e8cd59e915643891ffae4d488095d6c7053)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDaily")
    def put_daily(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorAlertProcessingRuleActionGroupScheduleRecurrenceDaily, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09c90ee769627bafc5a0f7e60f9605a1a4d89df139f762bd727e07a430129b8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDaily", [value]))

    @jsii.member(jsii_name="putMonthly")
    def put_monthly(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorAlertProcessingRuleActionGroupScheduleRecurrenceMonthly, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d96494a891b284766c7f2cf55ad1fecc67a9d1393a32893a69fe620f231840f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMonthly", [value]))

    @jsii.member(jsii_name="putWeekly")
    def put_weekly(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorAlertProcessingRuleActionGroupScheduleRecurrenceWeekly", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed452fa3e3ae39f445af73f28c320c0fcc18762f9b0cbfeed2ebfa97085a89e6)
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
    def daily(self) -> MonitorAlertProcessingRuleActionGroupScheduleRecurrenceDailyList:
        return typing.cast(MonitorAlertProcessingRuleActionGroupScheduleRecurrenceDailyList, jsii.get(self, "daily"))

    @builtins.property
    @jsii.member(jsii_name="monthly")
    def monthly(
        self,
    ) -> MonitorAlertProcessingRuleActionGroupScheduleRecurrenceMonthlyList:
        return typing.cast(MonitorAlertProcessingRuleActionGroupScheduleRecurrenceMonthlyList, jsii.get(self, "monthly"))

    @builtins.property
    @jsii.member(jsii_name="weekly")
    def weekly(
        self,
    ) -> "MonitorAlertProcessingRuleActionGroupScheduleRecurrenceWeeklyList":
        return typing.cast("MonitorAlertProcessingRuleActionGroupScheduleRecurrenceWeeklyList", jsii.get(self, "weekly"))

    @builtins.property
    @jsii.member(jsii_name="dailyInput")
    def daily_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAlertProcessingRuleActionGroupScheduleRecurrenceDaily]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAlertProcessingRuleActionGroupScheduleRecurrenceDaily]]], jsii.get(self, "dailyInput"))

    @builtins.property
    @jsii.member(jsii_name="monthlyInput")
    def monthly_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAlertProcessingRuleActionGroupScheduleRecurrenceMonthly]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAlertProcessingRuleActionGroupScheduleRecurrenceMonthly]]], jsii.get(self, "monthlyInput"))

    @builtins.property
    @jsii.member(jsii_name="weeklyInput")
    def weekly_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorAlertProcessingRuleActionGroupScheduleRecurrenceWeekly"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorAlertProcessingRuleActionGroupScheduleRecurrenceWeekly"]]], jsii.get(self, "weeklyInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorAlertProcessingRuleActionGroupScheduleRecurrence]:
        return typing.cast(typing.Optional[MonitorAlertProcessingRuleActionGroupScheduleRecurrence], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAlertProcessingRuleActionGroupScheduleRecurrence],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a6e0e18cdf1e1e1d8d18401518f91eb3be60bf26ab2c6d5d39f7cecf58aaac0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupScheduleRecurrenceWeekly",
    jsii_struct_bases=[],
    name_mapping={
        "days_of_week": "daysOfWeek",
        "end_time": "endTime",
        "start_time": "startTime",
    },
)
class MonitorAlertProcessingRuleActionGroupScheduleRecurrenceWeekly:
    def __init__(
        self,
        *,
        days_of_week: typing.Sequence[builtins.str],
        end_time: typing.Optional[builtins.str] = None,
        start_time: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param days_of_week: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#days_of_week MonitorAlertProcessingRuleActionGroup#days_of_week}.
        :param end_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#end_time MonitorAlertProcessingRuleActionGroup#end_time}.
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#start_time MonitorAlertProcessingRuleActionGroup#start_time}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b55ec3a1a8bd203be12be76533f4a8734cfb1cd0575a5098fdf12af41d9c3e3)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#days_of_week MonitorAlertProcessingRuleActionGroup#days_of_week}.'''
        result = self._values.get("days_of_week")
        assert result is not None, "Required property 'days_of_week' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def end_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#end_time MonitorAlertProcessingRuleActionGroup#end_time}.'''
        result = self._values.get("end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#start_time MonitorAlertProcessingRuleActionGroup#start_time}.'''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleActionGroupScheduleRecurrenceWeekly(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAlertProcessingRuleActionGroupScheduleRecurrenceWeeklyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupScheduleRecurrenceWeeklyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__56a38b76124e3c4d357df250abccfcf9cacbea1d1ef9d52a8c0c6a4f8a2993b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorAlertProcessingRuleActionGroupScheduleRecurrenceWeeklyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80eb81efa3dd3b625d50d31cc6f7caee46f9717d286d34c5d059f815af68ec75)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorAlertProcessingRuleActionGroupScheduleRecurrenceWeeklyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d32c78120afddae97e3ae30b903c65f28d57be1658ee524ce9042adae9117043)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b73578d7d22f9668183710ec20edcfbe3fd8990d7129bda7f11ccb611139721f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__329920b20a5859498c1eec9c4c2069498e445ffb7e69851083eb239bdbe57b39)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAlertProcessingRuleActionGroupScheduleRecurrenceWeekly]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAlertProcessingRuleActionGroupScheduleRecurrenceWeekly]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAlertProcessingRuleActionGroupScheduleRecurrenceWeekly]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30c5712f2ae74a399e74a2a6661223da4a29b91980d8c58e1ccdb7084dbb15d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class MonitorAlertProcessingRuleActionGroupScheduleRecurrenceWeeklyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupScheduleRecurrenceWeeklyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e228727a2aadbafa9d67ad500bb227d5fad5f47c42231b8d4d856181da7014f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5b2aa2c31636bd6763bf570ed93f925add5573ad522ce1a19bee3fb11e4bd27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "daysOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @end_time.setter
    def end_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__733264817e93215bce09e17d12fbb9fe01f62f21a893c492724877a07b129e2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aaf0112f65364590c1d424c78d2706ecbf66080aa75076a8cbdfa1f60c4daa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAlertProcessingRuleActionGroupScheduleRecurrenceWeekly]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAlertProcessingRuleActionGroupScheduleRecurrenceWeekly]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAlertProcessingRuleActionGroupScheduleRecurrenceWeekly]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69c3255f978b57cbb51957e7b6f08040714adabb8bf050887789f2468590c493)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MonitorAlertProcessingRuleActionGroupTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#create MonitorAlertProcessingRuleActionGroup#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#delete MonitorAlertProcessingRuleActionGroup#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#read MonitorAlertProcessingRuleActionGroup#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#update MonitorAlertProcessingRuleActionGroup#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04f6c2b96a3d5fc8728b472ccb53bbb1d2bf93c5fe470f63c2f4d99918d9c0de)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#create MonitorAlertProcessingRuleActionGroup#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#delete MonitorAlertProcessingRuleActionGroup#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#read MonitorAlertProcessingRuleActionGroup#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/monitor_alert_processing_rule_action_group#update MonitorAlertProcessingRuleActionGroup#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAlertProcessingRuleActionGroupTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAlertProcessingRuleActionGroupTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAlertProcessingRuleActionGroup.MonitorAlertProcessingRuleActionGroupTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c991aab8c27725ead094be532079dbdd6448a92d1763a7f86824ba33f815924d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc628a737d2694f7185e3b6be75df910cf87c87f317d79df9a1e56fbba3de312)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dd9df23d339ea073901cee11d484f1ba74c0cc19f30ef61cb0b0ad8ab2dce3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0132aad822e75938519568da7f305a814f2ef39c18f4ceee8367856de244c167)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38a7feb8f5d97622c40a19478e077a5453cc0dd4ea4d801391b123b9789920b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAlertProcessingRuleActionGroupTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAlertProcessingRuleActionGroupTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAlertProcessingRuleActionGroupTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8d3a4b7db4e51f22e08890633df6d6e5997794ddedcb739611f29c45594e42c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "MonitorAlertProcessingRuleActionGroup",
    "MonitorAlertProcessingRuleActionGroupCondition",
    "MonitorAlertProcessingRuleActionGroupConditionAlertContext",
    "MonitorAlertProcessingRuleActionGroupConditionAlertContextOutputReference",
    "MonitorAlertProcessingRuleActionGroupConditionAlertRuleId",
    "MonitorAlertProcessingRuleActionGroupConditionAlertRuleIdOutputReference",
    "MonitorAlertProcessingRuleActionGroupConditionAlertRuleName",
    "MonitorAlertProcessingRuleActionGroupConditionAlertRuleNameOutputReference",
    "MonitorAlertProcessingRuleActionGroupConditionDescription",
    "MonitorAlertProcessingRuleActionGroupConditionDescriptionOutputReference",
    "MonitorAlertProcessingRuleActionGroupConditionMonitorCondition",
    "MonitorAlertProcessingRuleActionGroupConditionMonitorConditionOutputReference",
    "MonitorAlertProcessingRuleActionGroupConditionMonitorService",
    "MonitorAlertProcessingRuleActionGroupConditionMonitorServiceOutputReference",
    "MonitorAlertProcessingRuleActionGroupConditionOutputReference",
    "MonitorAlertProcessingRuleActionGroupConditionSeverity",
    "MonitorAlertProcessingRuleActionGroupConditionSeverityOutputReference",
    "MonitorAlertProcessingRuleActionGroupConditionSignalType",
    "MonitorAlertProcessingRuleActionGroupConditionSignalTypeOutputReference",
    "MonitorAlertProcessingRuleActionGroupConditionTargetResource",
    "MonitorAlertProcessingRuleActionGroupConditionTargetResourceGroup",
    "MonitorAlertProcessingRuleActionGroupConditionTargetResourceGroupOutputReference",
    "MonitorAlertProcessingRuleActionGroupConditionTargetResourceOutputReference",
    "MonitorAlertProcessingRuleActionGroupConditionTargetResourceType",
    "MonitorAlertProcessingRuleActionGroupConditionTargetResourceTypeOutputReference",
    "MonitorAlertProcessingRuleActionGroupConfig",
    "MonitorAlertProcessingRuleActionGroupSchedule",
    "MonitorAlertProcessingRuleActionGroupScheduleOutputReference",
    "MonitorAlertProcessingRuleActionGroupScheduleRecurrence",
    "MonitorAlertProcessingRuleActionGroupScheduleRecurrenceDaily",
    "MonitorAlertProcessingRuleActionGroupScheduleRecurrenceDailyList",
    "MonitorAlertProcessingRuleActionGroupScheduleRecurrenceDailyOutputReference",
    "MonitorAlertProcessingRuleActionGroupScheduleRecurrenceMonthly",
    "MonitorAlertProcessingRuleActionGroupScheduleRecurrenceMonthlyList",
    "MonitorAlertProcessingRuleActionGroupScheduleRecurrenceMonthlyOutputReference",
    "MonitorAlertProcessingRuleActionGroupScheduleRecurrenceOutputReference",
    "MonitorAlertProcessingRuleActionGroupScheduleRecurrenceWeekly",
    "MonitorAlertProcessingRuleActionGroupScheduleRecurrenceWeeklyList",
    "MonitorAlertProcessingRuleActionGroupScheduleRecurrenceWeeklyOutputReference",
    "MonitorAlertProcessingRuleActionGroupTimeouts",
    "MonitorAlertProcessingRuleActionGroupTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__79a0585d3d6c8b639f37a31ce3fb5e3b2488bbcf3adc76adec39e9c3d53e0f63(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    add_action_group_ids: typing.Sequence[builtins.str],
    name: builtins.str,
    resource_group_name: builtins.str,
    scopes: typing.Sequence[builtins.str],
    condition: typing.Optional[typing.Union[MonitorAlertProcessingRuleActionGroupCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[typing.Union[MonitorAlertProcessingRuleActionGroupSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MonitorAlertProcessingRuleActionGroupTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__3c4ba03ed7e805613bc775579646477e57d502bb5a3130bf86c3ab51c8afa12d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ac1384b2f0f352cb19028eda4d80e23fb386d4fad24cbc842894a9c9cf7e9df(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ad6d8dbd63b2ce7c9bd323fb45892f6326575680b00bc8f06898b45ce64a0bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07f59fd655c0e616c6e8325ea60137e6398acc2aed4cc9ef0f10d786524810db(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ee8d91a3cef0fd88cdbf01e989ad76c1ba03db20f5d1e4bfec8203a2d5c51a9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd44a3dc8925d3398790305b66de664ba0d9acef6c677c3d9879a1f00097f6ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa568cd68e42238666169928ed8d4e691e11f74a008ed9ac15638db739b60b4c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__406b0e466eebe2f6b14c2b5cb7d436ac3c4e8f5d8147c63de08fb5f29bc2cf6a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bce8269ece5ed11470d1bae26b8485e9ea1fa25ddf5a6a99b5cbd95f6efacd25(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c8838b2602a7c5b693251e6aa669e165ebc6c0ff1087dce01f731aacb142223(
    *,
    alert_context: typing.Optional[typing.Union[MonitorAlertProcessingRuleActionGroupConditionAlertContext, typing.Dict[builtins.str, typing.Any]]] = None,
    alert_rule_id: typing.Optional[typing.Union[MonitorAlertProcessingRuleActionGroupConditionAlertRuleId, typing.Dict[builtins.str, typing.Any]]] = None,
    alert_rule_name: typing.Optional[typing.Union[MonitorAlertProcessingRuleActionGroupConditionAlertRuleName, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[typing.Union[MonitorAlertProcessingRuleActionGroupConditionDescription, typing.Dict[builtins.str, typing.Any]]] = None,
    monitor_condition: typing.Optional[typing.Union[MonitorAlertProcessingRuleActionGroupConditionMonitorCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    monitor_service: typing.Optional[typing.Union[MonitorAlertProcessingRuleActionGroupConditionMonitorService, typing.Dict[builtins.str, typing.Any]]] = None,
    severity: typing.Optional[typing.Union[MonitorAlertProcessingRuleActionGroupConditionSeverity, typing.Dict[builtins.str, typing.Any]]] = None,
    signal_type: typing.Optional[typing.Union[MonitorAlertProcessingRuleActionGroupConditionSignalType, typing.Dict[builtins.str, typing.Any]]] = None,
    target_resource: typing.Optional[typing.Union[MonitorAlertProcessingRuleActionGroupConditionTargetResource, typing.Dict[builtins.str, typing.Any]]] = None,
    target_resource_group: typing.Optional[typing.Union[MonitorAlertProcessingRuleActionGroupConditionTargetResourceGroup, typing.Dict[builtins.str, typing.Any]]] = None,
    target_resource_type: typing.Optional[typing.Union[MonitorAlertProcessingRuleActionGroupConditionTargetResourceType, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d5f9f8f9a4cb404d0a44017777ac5687214deea3181542bb6296e1afb09e4f4(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a29965979d63d0889009dc3927da6ead217598b09bae18b1b8a3cb6c346a73c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d7390749ed1c12a473b0238e141e7e093e0ef7308ee6aef52b4560166b339bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__958a80f9edf8033dd6b4eb30f591de3891cb4a4f72a664082207e69344e8b31c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e73f78afbb2c81173274ca5eb72ef057f98ed62998b312ffa0bb11944bc0da4(
    value: typing.Optional[MonitorAlertProcessingRuleActionGroupConditionAlertContext],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd5c2280636f5df2f3ff139f4ba91cd1b7ac44f1351c775dcd4da542ea3dcf05(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6209d3157abac734874b8e29d1ed0738285f1f186e32b998b50ab792b6f20c6f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b84842441842089b9dc3f40673bfa52da3f956be168b580ca2d739baca3c9c30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__643eed78cfdf4cf106c8de24233747705ce1377e4fd11b4451c1ae46ec46f236(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90861a629eed755d97624342e96e93ffa82bf69ac24aacc6228af96d87995f26(
    value: typing.Optional[MonitorAlertProcessingRuleActionGroupConditionAlertRuleId],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7edda79423fe9364636f8444c2bb91f15f5ca3396a9be04ebdb435376175750(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33b615ff2d57a71acf54d69e22115577bedf7a8b96c3e1c139f9410dba227e10(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__366de7ff26094a579eb0daa029b96787ddda7327c1cc00f54d0feaa71e64be08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__148980d702a558c8c14e5b2ed0235efe5b0c8a0ece6fb97bde1391d87387ebe7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74c282ca65f194d0b21a04503fbc643fb94ffd04361f5e045e6d7468a0326edd(
    value: typing.Optional[MonitorAlertProcessingRuleActionGroupConditionAlertRuleName],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6369eb6ebaf8dd3d285b98b81c6f90805e89485246bc8ccd0d639913cef78639(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dafac8784376a9c5d87f7a4f0b989a0234116d3d4334fa51412c58e237eaa50(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__167a1f3d686d978c381c346c68bb841a6cd6a453825d1a645972e344431190d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__663a9e4b0e45e36f282073668b313308c6abb4926d7a72105c5f555a23a55739(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b394cd7e33b609a25c6b09e62b65ea07b8c0469c48e68ac84b7182550d37da3(
    value: typing.Optional[MonitorAlertProcessingRuleActionGroupConditionDescription],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10851542037b975045fd17efa3cdb23793136ada534ed40882cc8116238e9cac(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baa6e13162620148d59158b7b4fe9910da7a3433fe8de10ee7da562f4940895f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa9889d3caa16cf1ac0d92b048ffe3f0b5dcc99f05fc8de8ac7f6befbd5458d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e61999cffbd4f1e2fb5bd290c61316df15aaeba811fc89f6d09162ef16b490f8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4928d958500a3d2e198d3e2a2effe6dd3b7c2efc7524c328a5ff3bcad7bef2a1(
    value: typing.Optional[MonitorAlertProcessingRuleActionGroupConditionMonitorCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb3303d679fc2a94b026b445f3eca55c3771a3ce82cdf1453ba50e639da3255b(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a5aaad85b019c0635bc3c0f51b471252ae6b3735ea8eb53d3f3475b97eed4ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c20b01e03d9f16ad66f3e3793bbb3a1ad69f8db4f2fa8e934f1e83b0d8b706(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8e3b78488d60266f0d4636c25199967312df143ce52123d581e581cde58b1f4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3414a62cea5d3d918563ed7d32a52230c1f740e7bd7f07b252614b57cabcfa3e(
    value: typing.Optional[MonitorAlertProcessingRuleActionGroupConditionMonitorService],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e1b7fa32b1700159bf1ecefb249ea1f39a303d2ba6f929025018dd07f26694f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5927f744448b24d240ce8b76b93f7e2b2217b51589367c391d3beeb8b550352a(
    value: typing.Optional[MonitorAlertProcessingRuleActionGroupCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cefdeac143dec7c5b1cd4ff879a4e3347791b12d920f0784478ccc7b47c1a75b(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf332b2d38ef833df786ed5c071f7f94dce7c2f84e7b974bd972e4182751168(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__388445fa4aafab9f6e61795ec83cffa3448bc38a20a93908343d83336a1d68ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f28778220f23ec21a937b54b60c067584a3dd90b5914aa81fcb58bf853ceb0e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81ea48f6eec60439219e00e0a69bdb79cc53c3fb40c0eafbb8811ad22c13d816(
    value: typing.Optional[MonitorAlertProcessingRuleActionGroupConditionSeverity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdc1b22cbbe934aafff67004d701585bc786f57b443b21e18604067c1423404b(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__770b603b226703124e5709d165b208e6379394dabc7ce55f5d85e903c091e573(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8de6036cbd6fbfd4660556be6e5ea992fdbf9011c9344f3fa70a32d3ea6c18d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d13073e657b0a10cbbc544664b95c38a762ba08b6450d10688120563adbb4fb0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__385673e0538eac5a028c656cc65a75c9fa1270d68c54a8afe9a52848ebd4ee42(
    value: typing.Optional[MonitorAlertProcessingRuleActionGroupConditionSignalType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39d3f2d155fe66e098e8bf778f10a688733e4899a9972febeb840649e5bac42d(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b3dbbf254fe4690c2e7c19be5af843312efc4c86e975a2fdeea240e8966aecd(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__230aa727cc438e6075820f367c8f2858c2b2e31cb52a6a662e8642ab8c9c5640(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1ee5f9e5e242499102c0f8977ea7e55a326f32e2b01d6e1ed5c60f7026beefb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cac7969a5a717bbbdcdee069b4876401dee282c4a52c71f6664e9ea1462ee90d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a5233d17158f5576deb7c3481b8e471840197796cb495e3452b7981efd76f24(
    value: typing.Optional[MonitorAlertProcessingRuleActionGroupConditionTargetResourceGroup],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c25c4a60aeecf221b84570d5e02d9337795cafa369f4d137fe4c0e024fdf806(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba4b57d54032e2634f036ff47f906d911a6b4f1ac18946c9739f6d784a52c549(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__076cd84df1e75db3cc3e86bd62a1dbbde892cc48aeced6c3f3229b84ad236a4a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__126d702411fb89065de130abc9294cab8cd030dfb7359bbec9365953c3433fa2(
    value: typing.Optional[MonitorAlertProcessingRuleActionGroupConditionTargetResource],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5424d5e75bee1b5e278e3c64c2d4154a1c5ee1de8c2e70556b60177fbcda22d5(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d31f4174c4538c74d00cf65e8796ec0b368eefef91853effc1d0076a4cd92333(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6848c720ef30e2d345f24c85e8219c03fd1804d626c4985329745bf96cae1cfc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfe5758706b38b98e062fbdff51c7746256e133d9e261975c237e79d814d7534(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b9fd48ae4026ebebf0bf9b933e2430abb6c5b1465d186f03a9afd7846f62103(
    value: typing.Optional[MonitorAlertProcessingRuleActionGroupConditionTargetResourceType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__371632eb16eb605ce77bee33ca6b0572e70215d6b1126d210855251806534ca9(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    add_action_group_ids: typing.Sequence[builtins.str],
    name: builtins.str,
    resource_group_name: builtins.str,
    scopes: typing.Sequence[builtins.str],
    condition: typing.Optional[typing.Union[MonitorAlertProcessingRuleActionGroupCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[typing.Union[MonitorAlertProcessingRuleActionGroupSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MonitorAlertProcessingRuleActionGroupTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de78b30dd8e5b7543c0d433adebc3bec0b04cf80ba5e5739978873452452f8f1(
    *,
    effective_from: typing.Optional[builtins.str] = None,
    effective_until: typing.Optional[builtins.str] = None,
    recurrence: typing.Optional[typing.Union[MonitorAlertProcessingRuleActionGroupScheduleRecurrence, typing.Dict[builtins.str, typing.Any]]] = None,
    time_zone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce142ff9a2302d81f00430a45d29dc0aa08d305ca13a38b9a511e5dbe2acc478(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b72c65731c0a154cd431f64bf6e306313f81ffbac814abb44920d8c1e9ddc14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a79a16038bbfdb148be16c6864b0f17857cf7d6804ae26bacc7e76600741f7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad10abf64f1165a1446b870d3cd3ee759ddf9a95a18e4543da835237a766c1aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__843cd4bd6969b162a2507e2a62a11a8dcd0f75cdb1df264f2921ffa5eefe33a0(
    value: typing.Optional[MonitorAlertProcessingRuleActionGroupSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__758bf6f819bdb1c8f170a7edf6068cf634862265ff35f6d596f87549d4e96342(
    *,
    daily: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorAlertProcessingRuleActionGroupScheduleRecurrenceDaily, typing.Dict[builtins.str, typing.Any]]]]] = None,
    monthly: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorAlertProcessingRuleActionGroupScheduleRecurrenceMonthly, typing.Dict[builtins.str, typing.Any]]]]] = None,
    weekly: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorAlertProcessingRuleActionGroupScheduleRecurrenceWeekly, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59587af70beb72623899de411d85d9aa0897e9eca278ef9c5b1d864c6392852b(
    *,
    end_time: builtins.str,
    start_time: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f36127365f277ac761d02762c415267af93f06739e85335c8c286eb664457e8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3e8c116326b43ade3f9c07aa162f92cb41f43ed674701443a4414aab063dbf2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79cd6df53c204d32a85528b3d6fd6c71a11430b9b34df096815695534bac380d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c559f6d17e49aa0383cc10c65c07e989e00ba3b8a917ebb82e79a10304a9759(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32c31149ab59aee163c397c50654e0b7c88fdfe866b183bc7ec842288dac6a75(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c548a6e93eaf16e43ea17977d23729df24600f39a81a61d980445806c2b3801(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAlertProcessingRuleActionGroupScheduleRecurrenceDaily]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1d63caf273f5c6d3dc7f4f252463e915e13cd541e7a1f8ab2156fe97b481a05(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__924254ad590565921825653048501692ea35278827bae8d78ea0fe8179b1a885(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf2dc5f567d61a145cd57819ef54ae7c1104d86f97573d420093763e1bdc0ed0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d2602993d4029fcf43716771b950db44071ec8ef2a5c163bc8d4598a6c47c77(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAlertProcessingRuleActionGroupScheduleRecurrenceDaily]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31fc76186242c11c3fa8850216ae6ff5ca86f2713b17faa65434482ff8c6dcac(
    *,
    days_of_month: typing.Sequence[jsii.Number],
    end_time: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c79f488b6a2518e58017df75cc6117f3c1e2181aa843e63e357ed620b01a621b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47667ddf29ff096c638f5ec80e5c6535af608bd44469707ff4e936351029404d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83b27b55f92bb120bced459742a291b51bb22694dbc4f4af330825d4b5b30ece(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b4a121196ee9a620b15b335e9e5d1d84b2ebff4d62080e4a7dc057c0a807388(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c01be3928fcc43cdf32a3f4d1dd94933f507c693b119991240b4adfa73a66e8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e3d338a231360a5dda9c064698b9b13598e2a54101696c585241f7479d519c2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAlertProcessingRuleActionGroupScheduleRecurrenceMonthly]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51000417460e1a0e3d25a89a2b432a95f3ccb30f57cf913eb608449d9da31b55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66c0ad14b0a778eb4c4841c2b481634e6e831a4f6eaa0fff63d7c3319d8876bc(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d611db5e50a87cb23251ce6f06f275ca715f8713e17c9a2f63cba89580422059(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fa9f0917ffa6d80d4378d86e9f45981a205308befb8265eb1658cf1d0b187f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1063564c4d4575cba21e2cf3839442f88314b43d687db062706acf206c42bf36(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAlertProcessingRuleActionGroupScheduleRecurrenceMonthly]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f435b7085ef927f6f77767b1d3c47e8cd59e915643891ffae4d488095d6c7053(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09c90ee769627bafc5a0f7e60f9605a1a4d89df139f762bd727e07a430129b8e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorAlertProcessingRuleActionGroupScheduleRecurrenceDaily, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d96494a891b284766c7f2cf55ad1fecc67a9d1393a32893a69fe620f231840f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorAlertProcessingRuleActionGroupScheduleRecurrenceMonthly, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed452fa3e3ae39f445af73f28c320c0fcc18762f9b0cbfeed2ebfa97085a89e6(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorAlertProcessingRuleActionGroupScheduleRecurrenceWeekly, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a6e0e18cdf1e1e1d8d18401518f91eb3be60bf26ab2c6d5d39f7cecf58aaac0(
    value: typing.Optional[MonitorAlertProcessingRuleActionGroupScheduleRecurrence],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b55ec3a1a8bd203be12be76533f4a8734cfb1cd0575a5098fdf12af41d9c3e3(
    *,
    days_of_week: typing.Sequence[builtins.str],
    end_time: typing.Optional[builtins.str] = None,
    start_time: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56a38b76124e3c4d357df250abccfcf9cacbea1d1ef9d52a8c0c6a4f8a2993b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80eb81efa3dd3b625d50d31cc6f7caee46f9717d286d34c5d059f815af68ec75(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d32c78120afddae97e3ae30b903c65f28d57be1658ee524ce9042adae9117043(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b73578d7d22f9668183710ec20edcfbe3fd8990d7129bda7f11ccb611139721f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__329920b20a5859498c1eec9c4c2069498e445ffb7e69851083eb239bdbe57b39(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30c5712f2ae74a399e74a2a6661223da4a29b91980d8c58e1ccdb7084dbb15d1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAlertProcessingRuleActionGroupScheduleRecurrenceWeekly]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e228727a2aadbafa9d67ad500bb227d5fad5f47c42231b8d4d856181da7014f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5b2aa2c31636bd6763bf570ed93f925add5573ad522ce1a19bee3fb11e4bd27(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__733264817e93215bce09e17d12fbb9fe01f62f21a893c492724877a07b129e2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aaf0112f65364590c1d424c78d2706ecbf66080aa75076a8cbdfa1f60c4daa6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69c3255f978b57cbb51957e7b6f08040714adabb8bf050887789f2468590c493(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAlertProcessingRuleActionGroupScheduleRecurrenceWeekly]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04f6c2b96a3d5fc8728b472ccb53bbb1d2bf93c5fe470f63c2f4d99918d9c0de(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c991aab8c27725ead094be532079dbdd6448a92d1763a7f86824ba33f815924d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc628a737d2694f7185e3b6be75df910cf87c87f317d79df9a1e56fbba3de312(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dd9df23d339ea073901cee11d484f1ba74c0cc19f30ef61cb0b0ad8ab2dce3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0132aad822e75938519568da7f305a814f2ef39c18f4ceee8367856de244c167(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38a7feb8f5d97622c40a19478e077a5453cc0dd4ea4d801391b123b9789920b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8d3a4b7db4e51f22e08890633df6d6e5997794ddedcb739611f29c45594e42c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, MonitorAlertProcessingRuleActionGroupTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
