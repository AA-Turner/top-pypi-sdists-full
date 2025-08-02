r'''
# `opentelekomcloud_lts_keywords_alarm_rule_v2`

Refer to the Terraform Registry for docs: [`opentelekomcloud_lts_keywords_alarm_rule_v2`](https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2).
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


class LtsKeywordsAlarmRuleV2(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ltsKeywordsAlarmRuleV2.LtsKeywordsAlarmRuleV2",
):
    '''Represents a {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2 opentelekomcloud_lts_keywords_alarm_rule_v2}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        frequency: typing.Union["LtsKeywordsAlarmRuleV2Frequency", typing.Dict[builtins.str, typing.Any]],
        keywords_requests: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LtsKeywordsAlarmRuleV2KeywordsRequests", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        notification_frequency: jsii.Number,
        severity: builtins.str,
        alarm_action_rule_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        notification_rule: typing.Optional[typing.Union["LtsKeywordsAlarmRuleV2NotificationRule", typing.Dict[builtins.str, typing.Any]]] = None,
        recovery_policy: typing.Optional[jsii.Number] = None,
        send_notifications: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        send_recovery_notifications: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        trigger_condition_count: typing.Optional[jsii.Number] = None,
        trigger_condition_frequency: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2 opentelekomcloud_lts_keywords_alarm_rule_v2} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param frequency: frequency block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#frequency LtsKeywordsAlarmRuleV2#frequency}
        :param keywords_requests: keywords_requests block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#keywords_requests LtsKeywordsAlarmRuleV2#keywords_requests}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#name LtsKeywordsAlarmRuleV2#name}.
        :param notification_frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#notification_frequency LtsKeywordsAlarmRuleV2#notification_frequency}.
        :param severity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#severity LtsKeywordsAlarmRuleV2#severity}.
        :param alarm_action_rule_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#alarm_action_rule_name LtsKeywordsAlarmRuleV2#alarm_action_rule_name}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#description LtsKeywordsAlarmRuleV2#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#id LtsKeywordsAlarmRuleV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notification_rule: notification_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#notification_rule LtsKeywordsAlarmRuleV2#notification_rule}
        :param recovery_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#recovery_policy LtsKeywordsAlarmRuleV2#recovery_policy}.
        :param send_notifications: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#send_notifications LtsKeywordsAlarmRuleV2#send_notifications}.
        :param send_recovery_notifications: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#send_recovery_notifications LtsKeywordsAlarmRuleV2#send_recovery_notifications}.
        :param trigger_condition_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#trigger_condition_count LtsKeywordsAlarmRuleV2#trigger_condition_count}.
        :param trigger_condition_frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#trigger_condition_frequency LtsKeywordsAlarmRuleV2#trigger_condition_frequency}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3267343746fbc14a83f47b763f486b412c53efa4fb29810ce75b68bf43bd4b6a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = LtsKeywordsAlarmRuleV2Config(
            frequency=frequency,
            keywords_requests=keywords_requests,
            name=name,
            notification_frequency=notification_frequency,
            severity=severity,
            alarm_action_rule_name=alarm_action_rule_name,
            description=description,
            id=id,
            notification_rule=notification_rule,
            recovery_policy=recovery_policy,
            send_notifications=send_notifications,
            send_recovery_notifications=send_recovery_notifications,
            trigger_condition_count=trigger_condition_count,
            trigger_condition_frequency=trigger_condition_frequency,
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
        '''Generates CDKTF code for importing a LtsKeywordsAlarmRuleV2 resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the LtsKeywordsAlarmRuleV2 to import.
        :param import_from_id: The id of the existing LtsKeywordsAlarmRuleV2 that should be imported. Refer to the {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the LtsKeywordsAlarmRuleV2 to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e6d28fd03977d6d4c0b11fdffd545a86a9476297e32c6786d01222f7bfa1215)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putFrequency")
    def put_frequency(
        self,
        *,
        type: builtins.str,
        cron_expression: typing.Optional[builtins.str] = None,
        day_of_week: typing.Optional[jsii.Number] = None,
        fixed_rate: typing.Optional[jsii.Number] = None,
        fixed_rate_unit: typing.Optional[builtins.str] = None,
        hour_of_day: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#type LtsKeywordsAlarmRuleV2#type}.
        :param cron_expression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#cron_expression LtsKeywordsAlarmRuleV2#cron_expression}.
        :param day_of_week: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#day_of_week LtsKeywordsAlarmRuleV2#day_of_week}.
        :param fixed_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#fixed_rate LtsKeywordsAlarmRuleV2#fixed_rate}.
        :param fixed_rate_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#fixed_rate_unit LtsKeywordsAlarmRuleV2#fixed_rate_unit}.
        :param hour_of_day: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#hour_of_day LtsKeywordsAlarmRuleV2#hour_of_day}.
        '''
        value = LtsKeywordsAlarmRuleV2Frequency(
            type=type,
            cron_expression=cron_expression,
            day_of_week=day_of_week,
            fixed_rate=fixed_rate,
            fixed_rate_unit=fixed_rate_unit,
            hour_of_day=hour_of_day,
        )

        return typing.cast(None, jsii.invoke(self, "putFrequency", [value]))

    @jsii.member(jsii_name="putKeywordsRequests")
    def put_keywords_requests(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LtsKeywordsAlarmRuleV2KeywordsRequests", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58d1afbee2075f9c631acbf1bd0d5c72f31613ee9dded5204cc9e2ae38f51119)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putKeywordsRequests", [value]))

    @jsii.member(jsii_name="putNotificationRule")
    def put_notification_rule(
        self,
        *,
        topics: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LtsKeywordsAlarmRuleV2NotificationRuleTopics", typing.Dict[builtins.str, typing.Any]]]],
        user_name: builtins.str,
        language: typing.Optional[builtins.str] = None,
        template_name: typing.Optional[builtins.str] = None,
        timezone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param topics: topics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#topics LtsKeywordsAlarmRuleV2#topics}
        :param user_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#user_name LtsKeywordsAlarmRuleV2#user_name}.
        :param language: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#language LtsKeywordsAlarmRuleV2#language}.
        :param template_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#template_name LtsKeywordsAlarmRuleV2#template_name}.
        :param timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#timezone LtsKeywordsAlarmRuleV2#timezone}.
        '''
        value = LtsKeywordsAlarmRuleV2NotificationRule(
            topics=topics,
            user_name=user_name,
            language=language,
            template_name=template_name,
            timezone=timezone,
        )

        return typing.cast(None, jsii.invoke(self, "putNotificationRule", [value]))

    @jsii.member(jsii_name="resetAlarmActionRuleName")
    def reset_alarm_action_rule_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlarmActionRuleName", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetNotificationRule")
    def reset_notification_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNotificationRule", []))

    @jsii.member(jsii_name="resetRecoveryPolicy")
    def reset_recovery_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecoveryPolicy", []))

    @jsii.member(jsii_name="resetSendNotifications")
    def reset_send_notifications(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSendNotifications", []))

    @jsii.member(jsii_name="resetSendRecoveryNotifications")
    def reset_send_recovery_notifications(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSendRecoveryNotifications", []))

    @jsii.member(jsii_name="resetTriggerConditionCount")
    def reset_trigger_condition_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTriggerConditionCount", []))

    @jsii.member(jsii_name="resetTriggerConditionFrequency")
    def reset_trigger_condition_frequency(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTriggerConditionFrequency", []))

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
    def created_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "createdAt"))

    @builtins.property
    @jsii.member(jsii_name="domainId")
    def domain_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainId"))

    @builtins.property
    @jsii.member(jsii_name="frequency")
    def frequency(self) -> "LtsKeywordsAlarmRuleV2FrequencyOutputReference":
        return typing.cast("LtsKeywordsAlarmRuleV2FrequencyOutputReference", jsii.get(self, "frequency"))

    @builtins.property
    @jsii.member(jsii_name="keywordsRequests")
    def keywords_requests(self) -> "LtsKeywordsAlarmRuleV2KeywordsRequestsList":
        return typing.cast("LtsKeywordsAlarmRuleV2KeywordsRequestsList", jsii.get(self, "keywordsRequests"))

    @builtins.property
    @jsii.member(jsii_name="notificationRule")
    def notification_rule(
        self,
    ) -> "LtsKeywordsAlarmRuleV2NotificationRuleOutputReference":
        return typing.cast("LtsKeywordsAlarmRuleV2NotificationRuleOutputReference", jsii.get(self, "notificationRule"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @builtins.property
    @jsii.member(jsii_name="updatedAt")
    def updated_at(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updatedAt"))

    @builtins.property
    @jsii.member(jsii_name="alarmActionRuleNameInput")
    def alarm_action_rule_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "alarmActionRuleNameInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="frequencyInput")
    def frequency_input(self) -> typing.Optional["LtsKeywordsAlarmRuleV2Frequency"]:
        return typing.cast(typing.Optional["LtsKeywordsAlarmRuleV2Frequency"], jsii.get(self, "frequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="keywordsRequestsInput")
    def keywords_requests_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LtsKeywordsAlarmRuleV2KeywordsRequests"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LtsKeywordsAlarmRuleV2KeywordsRequests"]]], jsii.get(self, "keywordsRequestsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationFrequencyInput")
    def notification_frequency_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "notificationFrequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="notificationRuleInput")
    def notification_rule_input(
        self,
    ) -> typing.Optional["LtsKeywordsAlarmRuleV2NotificationRule"]:
        return typing.cast(typing.Optional["LtsKeywordsAlarmRuleV2NotificationRule"], jsii.get(self, "notificationRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="recoveryPolicyInput")
    def recovery_policy_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "recoveryPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="sendNotificationsInput")
    def send_notifications_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sendNotificationsInput"))

    @builtins.property
    @jsii.member(jsii_name="sendRecoveryNotificationsInput")
    def send_recovery_notifications_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "sendRecoveryNotificationsInput"))

    @builtins.property
    @jsii.member(jsii_name="severityInput")
    def severity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "severityInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerConditionCountInput")
    def trigger_condition_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "triggerConditionCountInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerConditionFrequencyInput")
    def trigger_condition_frequency_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "triggerConditionFrequencyInput"))

    @builtins.property
    @jsii.member(jsii_name="alarmActionRuleName")
    def alarm_action_rule_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "alarmActionRuleName"))

    @alarm_action_rule_name.setter
    def alarm_action_rule_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46f6675c590bc7469cd1f97210308f0b9ca09e026a79db162a0a4ae1763ac0d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "alarmActionRuleName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f46b46258e6b5cb0f9972e5bd698db97e2533a2106efb0d09148d83e176d743f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b3882bb8296cac85716730ad221a9f8cf3c010a16859d8681a78eac15fcc364)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5797af2e89dc416c4450c21d81b711c613a3c4d319051b404cc42f884e6813d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="notificationFrequency")
    def notification_frequency(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "notificationFrequency"))

    @notification_frequency.setter
    def notification_frequency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36d50fdb924782e1114d70c374c3583d73ffb5802b675e29b8209ac077a1084e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "notificationFrequency", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="recoveryPolicy")
    def recovery_policy(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "recoveryPolicy"))

    @recovery_policy.setter
    def recovery_policy(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a7651e570259b89346591912c19d13af6634fced9cccfe1cd50c159868a8df3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recoveryPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sendNotifications")
    def send_notifications(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sendNotifications"))

    @send_notifications.setter
    def send_notifications(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e10f0d1a8d38cb84977b1a8457f19e38b1a4709731f36c3dc13be997c3cab5ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sendNotifications", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="sendRecoveryNotifications")
    def send_recovery_notifications(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "sendRecoveryNotifications"))

    @send_recovery_notifications.setter
    def send_recovery_notifications(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b982ea186a7ecb408bc7757ca50b4f1af6c37789ed67e15e9acfd43ffa1dc8e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sendRecoveryNotifications", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "severity"))

    @severity.setter
    def severity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__933b8fe996355971c5d054b1d5b3e0eb2a5101464b5727445ee04aa438899d06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "severity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="triggerConditionCount")
    def trigger_condition_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "triggerConditionCount"))

    @trigger_condition_count.setter
    def trigger_condition_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d369051290fa61458216e931ea8f4db4ce4e93bf59d8c77040cb16efc2c51682)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerConditionCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="triggerConditionFrequency")
    def trigger_condition_frequency(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "triggerConditionFrequency"))

    @trigger_condition_frequency.setter
    def trigger_condition_frequency(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80b7c0dab5801d888f69f5171b3f7535c6db4869b9f7f1795940371d0becde48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerConditionFrequency", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ltsKeywordsAlarmRuleV2.LtsKeywordsAlarmRuleV2Config",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "frequency": "frequency",
        "keywords_requests": "keywordsRequests",
        "name": "name",
        "notification_frequency": "notificationFrequency",
        "severity": "severity",
        "alarm_action_rule_name": "alarmActionRuleName",
        "description": "description",
        "id": "id",
        "notification_rule": "notificationRule",
        "recovery_policy": "recoveryPolicy",
        "send_notifications": "sendNotifications",
        "send_recovery_notifications": "sendRecoveryNotifications",
        "trigger_condition_count": "triggerConditionCount",
        "trigger_condition_frequency": "triggerConditionFrequency",
    },
)
class LtsKeywordsAlarmRuleV2Config(_cdktf_9a9027ec.TerraformMetaArguments):
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
        frequency: typing.Union["LtsKeywordsAlarmRuleV2Frequency", typing.Dict[builtins.str, typing.Any]],
        keywords_requests: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LtsKeywordsAlarmRuleV2KeywordsRequests", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        notification_frequency: jsii.Number,
        severity: builtins.str,
        alarm_action_rule_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        notification_rule: typing.Optional[typing.Union["LtsKeywordsAlarmRuleV2NotificationRule", typing.Dict[builtins.str, typing.Any]]] = None,
        recovery_policy: typing.Optional[jsii.Number] = None,
        send_notifications: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        send_recovery_notifications: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        trigger_condition_count: typing.Optional[jsii.Number] = None,
        trigger_condition_frequency: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param frequency: frequency block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#frequency LtsKeywordsAlarmRuleV2#frequency}
        :param keywords_requests: keywords_requests block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#keywords_requests LtsKeywordsAlarmRuleV2#keywords_requests}
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#name LtsKeywordsAlarmRuleV2#name}.
        :param notification_frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#notification_frequency LtsKeywordsAlarmRuleV2#notification_frequency}.
        :param severity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#severity LtsKeywordsAlarmRuleV2#severity}.
        :param alarm_action_rule_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#alarm_action_rule_name LtsKeywordsAlarmRuleV2#alarm_action_rule_name}.
        :param description: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#description LtsKeywordsAlarmRuleV2#description}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#id LtsKeywordsAlarmRuleV2#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param notification_rule: notification_rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#notification_rule LtsKeywordsAlarmRuleV2#notification_rule}
        :param recovery_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#recovery_policy LtsKeywordsAlarmRuleV2#recovery_policy}.
        :param send_notifications: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#send_notifications LtsKeywordsAlarmRuleV2#send_notifications}.
        :param send_recovery_notifications: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#send_recovery_notifications LtsKeywordsAlarmRuleV2#send_recovery_notifications}.
        :param trigger_condition_count: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#trigger_condition_count LtsKeywordsAlarmRuleV2#trigger_condition_count}.
        :param trigger_condition_frequency: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#trigger_condition_frequency LtsKeywordsAlarmRuleV2#trigger_condition_frequency}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(frequency, dict):
            frequency = LtsKeywordsAlarmRuleV2Frequency(**frequency)
        if isinstance(notification_rule, dict):
            notification_rule = LtsKeywordsAlarmRuleV2NotificationRule(**notification_rule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ece74d20fd14026d28a3beaff59ac76b5d99274cd7c08c4c03d44c98a1fa3a28)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument frequency", value=frequency, expected_type=type_hints["frequency"])
            check_type(argname="argument keywords_requests", value=keywords_requests, expected_type=type_hints["keywords_requests"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument notification_frequency", value=notification_frequency, expected_type=type_hints["notification_frequency"])
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
            check_type(argname="argument alarm_action_rule_name", value=alarm_action_rule_name, expected_type=type_hints["alarm_action_rule_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument notification_rule", value=notification_rule, expected_type=type_hints["notification_rule"])
            check_type(argname="argument recovery_policy", value=recovery_policy, expected_type=type_hints["recovery_policy"])
            check_type(argname="argument send_notifications", value=send_notifications, expected_type=type_hints["send_notifications"])
            check_type(argname="argument send_recovery_notifications", value=send_recovery_notifications, expected_type=type_hints["send_recovery_notifications"])
            check_type(argname="argument trigger_condition_count", value=trigger_condition_count, expected_type=type_hints["trigger_condition_count"])
            check_type(argname="argument trigger_condition_frequency", value=trigger_condition_frequency, expected_type=type_hints["trigger_condition_frequency"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "frequency": frequency,
            "keywords_requests": keywords_requests,
            "name": name,
            "notification_frequency": notification_frequency,
            "severity": severity,
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
        if alarm_action_rule_name is not None:
            self._values["alarm_action_rule_name"] = alarm_action_rule_name
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if notification_rule is not None:
            self._values["notification_rule"] = notification_rule
        if recovery_policy is not None:
            self._values["recovery_policy"] = recovery_policy
        if send_notifications is not None:
            self._values["send_notifications"] = send_notifications
        if send_recovery_notifications is not None:
            self._values["send_recovery_notifications"] = send_recovery_notifications
        if trigger_condition_count is not None:
            self._values["trigger_condition_count"] = trigger_condition_count
        if trigger_condition_frequency is not None:
            self._values["trigger_condition_frequency"] = trigger_condition_frequency

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
    def frequency(self) -> "LtsKeywordsAlarmRuleV2Frequency":
        '''frequency block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#frequency LtsKeywordsAlarmRuleV2#frequency}
        '''
        result = self._values.get("frequency")
        assert result is not None, "Required property 'frequency' is missing"
        return typing.cast("LtsKeywordsAlarmRuleV2Frequency", result)

    @builtins.property
    def keywords_requests(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LtsKeywordsAlarmRuleV2KeywordsRequests"]]:
        '''keywords_requests block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#keywords_requests LtsKeywordsAlarmRuleV2#keywords_requests}
        '''
        result = self._values.get("keywords_requests")
        assert result is not None, "Required property 'keywords_requests' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LtsKeywordsAlarmRuleV2KeywordsRequests"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#name LtsKeywordsAlarmRuleV2#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def notification_frequency(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#notification_frequency LtsKeywordsAlarmRuleV2#notification_frequency}.'''
        result = self._values.get("notification_frequency")
        assert result is not None, "Required property 'notification_frequency' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def severity(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#severity LtsKeywordsAlarmRuleV2#severity}.'''
        result = self._values.get("severity")
        assert result is not None, "Required property 'severity' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alarm_action_rule_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#alarm_action_rule_name LtsKeywordsAlarmRuleV2#alarm_action_rule_name}.'''
        result = self._values.get("alarm_action_rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#description LtsKeywordsAlarmRuleV2#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#id LtsKeywordsAlarmRuleV2#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def notification_rule(
        self,
    ) -> typing.Optional["LtsKeywordsAlarmRuleV2NotificationRule"]:
        '''notification_rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#notification_rule LtsKeywordsAlarmRuleV2#notification_rule}
        '''
        result = self._values.get("notification_rule")
        return typing.cast(typing.Optional["LtsKeywordsAlarmRuleV2NotificationRule"], result)

    @builtins.property
    def recovery_policy(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#recovery_policy LtsKeywordsAlarmRuleV2#recovery_policy}.'''
        result = self._values.get("recovery_policy")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def send_notifications(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#send_notifications LtsKeywordsAlarmRuleV2#send_notifications}.'''
        result = self._values.get("send_notifications")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def send_recovery_notifications(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#send_recovery_notifications LtsKeywordsAlarmRuleV2#send_recovery_notifications}.'''
        result = self._values.get("send_recovery_notifications")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def trigger_condition_count(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#trigger_condition_count LtsKeywordsAlarmRuleV2#trigger_condition_count}.'''
        result = self._values.get("trigger_condition_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def trigger_condition_frequency(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#trigger_condition_frequency LtsKeywordsAlarmRuleV2#trigger_condition_frequency}.'''
        result = self._values.get("trigger_condition_frequency")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LtsKeywordsAlarmRuleV2Config(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ltsKeywordsAlarmRuleV2.LtsKeywordsAlarmRuleV2Frequency",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "cron_expression": "cronExpression",
        "day_of_week": "dayOfWeek",
        "fixed_rate": "fixedRate",
        "fixed_rate_unit": "fixedRateUnit",
        "hour_of_day": "hourOfDay",
    },
)
class LtsKeywordsAlarmRuleV2Frequency:
    def __init__(
        self,
        *,
        type: builtins.str,
        cron_expression: typing.Optional[builtins.str] = None,
        day_of_week: typing.Optional[jsii.Number] = None,
        fixed_rate: typing.Optional[jsii.Number] = None,
        fixed_rate_unit: typing.Optional[builtins.str] = None,
        hour_of_day: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#type LtsKeywordsAlarmRuleV2#type}.
        :param cron_expression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#cron_expression LtsKeywordsAlarmRuleV2#cron_expression}.
        :param day_of_week: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#day_of_week LtsKeywordsAlarmRuleV2#day_of_week}.
        :param fixed_rate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#fixed_rate LtsKeywordsAlarmRuleV2#fixed_rate}.
        :param fixed_rate_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#fixed_rate_unit LtsKeywordsAlarmRuleV2#fixed_rate_unit}.
        :param hour_of_day: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#hour_of_day LtsKeywordsAlarmRuleV2#hour_of_day}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a683eaf7083a9e996a9d2b3a7eb8a4121da82a0fb242a651d8b298ed759a6bed)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument cron_expression", value=cron_expression, expected_type=type_hints["cron_expression"])
            check_type(argname="argument day_of_week", value=day_of_week, expected_type=type_hints["day_of_week"])
            check_type(argname="argument fixed_rate", value=fixed_rate, expected_type=type_hints["fixed_rate"])
            check_type(argname="argument fixed_rate_unit", value=fixed_rate_unit, expected_type=type_hints["fixed_rate_unit"])
            check_type(argname="argument hour_of_day", value=hour_of_day, expected_type=type_hints["hour_of_day"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if cron_expression is not None:
            self._values["cron_expression"] = cron_expression
        if day_of_week is not None:
            self._values["day_of_week"] = day_of_week
        if fixed_rate is not None:
            self._values["fixed_rate"] = fixed_rate
        if fixed_rate_unit is not None:
            self._values["fixed_rate_unit"] = fixed_rate_unit
        if hour_of_day is not None:
            self._values["hour_of_day"] = hour_of_day

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#type LtsKeywordsAlarmRuleV2#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cron_expression(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#cron_expression LtsKeywordsAlarmRuleV2#cron_expression}.'''
        result = self._values.get("cron_expression")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def day_of_week(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#day_of_week LtsKeywordsAlarmRuleV2#day_of_week}.'''
        result = self._values.get("day_of_week")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def fixed_rate(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#fixed_rate LtsKeywordsAlarmRuleV2#fixed_rate}.'''
        result = self._values.get("fixed_rate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def fixed_rate_unit(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#fixed_rate_unit LtsKeywordsAlarmRuleV2#fixed_rate_unit}.'''
        result = self._values.get("fixed_rate_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def hour_of_day(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#hour_of_day LtsKeywordsAlarmRuleV2#hour_of_day}.'''
        result = self._values.get("hour_of_day")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LtsKeywordsAlarmRuleV2Frequency(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LtsKeywordsAlarmRuleV2FrequencyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ltsKeywordsAlarmRuleV2.LtsKeywordsAlarmRuleV2FrequencyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__139714787e9af7e5d5fbc96d1ae9bf7e2f179127d41e12bbea3aa56bce530fa6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCronExpression")
    def reset_cron_expression(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCronExpression", []))

    @jsii.member(jsii_name="resetDayOfWeek")
    def reset_day_of_week(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDayOfWeek", []))

    @jsii.member(jsii_name="resetFixedRate")
    def reset_fixed_rate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFixedRate", []))

    @jsii.member(jsii_name="resetFixedRateUnit")
    def reset_fixed_rate_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFixedRateUnit", []))

    @jsii.member(jsii_name="resetHourOfDay")
    def reset_hour_of_day(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHourOfDay", []))

    @builtins.property
    @jsii.member(jsii_name="cronExpressionInput")
    def cron_expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cronExpressionInput"))

    @builtins.property
    @jsii.member(jsii_name="dayOfWeekInput")
    def day_of_week_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dayOfWeekInput"))

    @builtins.property
    @jsii.member(jsii_name="fixedRateInput")
    def fixed_rate_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "fixedRateInput"))

    @builtins.property
    @jsii.member(jsii_name="fixedRateUnitInput")
    def fixed_rate_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "fixedRateUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="hourOfDayInput")
    def hour_of_day_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "hourOfDayInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="cronExpression")
    def cron_expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cronExpression"))

    @cron_expression.setter
    def cron_expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1489733b967e7628a25ee5ba842a5abab43746376d95fa8d3f39e5733b2121f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cronExpression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dayOfWeek")
    def day_of_week(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "dayOfWeek"))

    @day_of_week.setter
    def day_of_week(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be58b243011c39162a31a73e5cb14420edcb6ef922817e7a51092d167f1d2bd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dayOfWeek", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fixedRate")
    def fixed_rate(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "fixedRate"))

    @fixed_rate.setter
    def fixed_rate(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f701dbf9cddd59b8f570de498c84769b427aeb420281380f33fab99ec194f01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixedRate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="fixedRateUnit")
    def fixed_rate_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "fixedRateUnit"))

    @fixed_rate_unit.setter
    def fixed_rate_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87054ff2a9c658c7a1ecbc3c13e7fcaa9618ff3922b35cf63c144dcbef106885)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "fixedRateUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="hourOfDay")
    def hour_of_day(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "hourOfDay"))

    @hour_of_day.setter
    def hour_of_day(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bbbd9e32b4cf1ceba81ff451f2ae031d61601a4e43b4186a4b190c41672ad6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hourOfDay", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__080de96ff28864ec701f65b235c37a0ca056c6685eca6f4bd685f4539fd0c4f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LtsKeywordsAlarmRuleV2Frequency]:
        return typing.cast(typing.Optional[LtsKeywordsAlarmRuleV2Frequency], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LtsKeywordsAlarmRuleV2Frequency],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca9d77963761a120b0da947ea3872b2aff7d697e89d8454367ff173b1541ae4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ltsKeywordsAlarmRuleV2.LtsKeywordsAlarmRuleV2KeywordsRequests",
    jsii_struct_bases=[],
    name_mapping={
        "condition": "condition",
        "keyword": "keyword",
        "log_group_id": "logGroupId",
        "log_stream_id": "logStreamId",
        "number": "number",
        "search_time_range": "searchTimeRange",
        "search_time_range_unit": "searchTimeRangeUnit",
    },
)
class LtsKeywordsAlarmRuleV2KeywordsRequests:
    def __init__(
        self,
        *,
        condition: builtins.str,
        keyword: builtins.str,
        log_group_id: builtins.str,
        log_stream_id: builtins.str,
        number: jsii.Number,
        search_time_range: jsii.Number,
        search_time_range_unit: builtins.str,
    ) -> None:
        '''
        :param condition: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#condition LtsKeywordsAlarmRuleV2#condition}.
        :param keyword: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#keyword LtsKeywordsAlarmRuleV2#keyword}.
        :param log_group_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#log_group_id LtsKeywordsAlarmRuleV2#log_group_id}.
        :param log_stream_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#log_stream_id LtsKeywordsAlarmRuleV2#log_stream_id}.
        :param number: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#number LtsKeywordsAlarmRuleV2#number}.
        :param search_time_range: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#search_time_range LtsKeywordsAlarmRuleV2#search_time_range}.
        :param search_time_range_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#search_time_range_unit LtsKeywordsAlarmRuleV2#search_time_range_unit}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7508e6df88079e2b222f5d6f51322c521073caa3fd2bb99b3ed0c52763815fea)
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument keyword", value=keyword, expected_type=type_hints["keyword"])
            check_type(argname="argument log_group_id", value=log_group_id, expected_type=type_hints["log_group_id"])
            check_type(argname="argument log_stream_id", value=log_stream_id, expected_type=type_hints["log_stream_id"])
            check_type(argname="argument number", value=number, expected_type=type_hints["number"])
            check_type(argname="argument search_time_range", value=search_time_range, expected_type=type_hints["search_time_range"])
            check_type(argname="argument search_time_range_unit", value=search_time_range_unit, expected_type=type_hints["search_time_range_unit"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "condition": condition,
            "keyword": keyword,
            "log_group_id": log_group_id,
            "log_stream_id": log_stream_id,
            "number": number,
            "search_time_range": search_time_range,
            "search_time_range_unit": search_time_range_unit,
        }

    @builtins.property
    def condition(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#condition LtsKeywordsAlarmRuleV2#condition}.'''
        result = self._values.get("condition")
        assert result is not None, "Required property 'condition' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def keyword(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#keyword LtsKeywordsAlarmRuleV2#keyword}.'''
        result = self._values.get("keyword")
        assert result is not None, "Required property 'keyword' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_group_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#log_group_id LtsKeywordsAlarmRuleV2#log_group_id}.'''
        result = self._values.get("log_group_id")
        assert result is not None, "Required property 'log_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def log_stream_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#log_stream_id LtsKeywordsAlarmRuleV2#log_stream_id}.'''
        result = self._values.get("log_stream_id")
        assert result is not None, "Required property 'log_stream_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def number(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#number LtsKeywordsAlarmRuleV2#number}.'''
        result = self._values.get("number")
        assert result is not None, "Required property 'number' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def search_time_range(self) -> jsii.Number:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#search_time_range LtsKeywordsAlarmRuleV2#search_time_range}.'''
        result = self._values.get("search_time_range")
        assert result is not None, "Required property 'search_time_range' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def search_time_range_unit(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#search_time_range_unit LtsKeywordsAlarmRuleV2#search_time_range_unit}.'''
        result = self._values.get("search_time_range_unit")
        assert result is not None, "Required property 'search_time_range_unit' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LtsKeywordsAlarmRuleV2KeywordsRequests(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LtsKeywordsAlarmRuleV2KeywordsRequestsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ltsKeywordsAlarmRuleV2.LtsKeywordsAlarmRuleV2KeywordsRequestsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__80616a35aa07a0332148f76e94334647bccbbb09ef23e0b103d84a9212742287)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LtsKeywordsAlarmRuleV2KeywordsRequestsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c873490196f06f151389b167d8db81acf6b6fba45cbf5cc27015839ab14a45f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LtsKeywordsAlarmRuleV2KeywordsRequestsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44164ad2c91d44c9525dc97af2c3b4af4b79ef7930a7711b8eeac8ba9343a421)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7cf199d689a03b2db8b0f1a42091734df37ac352d0e104fa0963a95d06dbde3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91279720926d331f6b5ba46d2ed9e4c23d3fb2a2160e14aa670510011df46df1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LtsKeywordsAlarmRuleV2KeywordsRequests]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LtsKeywordsAlarmRuleV2KeywordsRequests]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LtsKeywordsAlarmRuleV2KeywordsRequests]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77fa0ecfbd958df8b389609fb144f97d82de0b3e1db6c23775756076cd0abd0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LtsKeywordsAlarmRuleV2KeywordsRequestsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ltsKeywordsAlarmRuleV2.LtsKeywordsAlarmRuleV2KeywordsRequestsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc2c0da5f2fec4042a2403b2650076452ffebf2994e556a6bf2fb4545faa6141)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="keywordInput")
    def keyword_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keywordInput"))

    @builtins.property
    @jsii.member(jsii_name="logGroupIdInput")
    def log_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="logStreamIdInput")
    def log_stream_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logStreamIdInput"))

    @builtins.property
    @jsii.member(jsii_name="numberInput")
    def number_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "numberInput"))

    @builtins.property
    @jsii.member(jsii_name="searchTimeRangeInput")
    def search_time_range_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "searchTimeRangeInput"))

    @builtins.property
    @jsii.member(jsii_name="searchTimeRangeUnitInput")
    def search_time_range_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "searchTimeRangeUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "condition"))

    @condition.setter
    def condition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de60aee2c61b61b07795ee39d09892bbbadb5adfbdaeb04d581438b1797be091)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "condition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="keyword")
    def keyword(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyword"))

    @keyword.setter
    def keyword(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed4843a1b822034a7957f2486f00eeda60017ab6a338606668461d375136d5bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyword", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logGroupId")
    def log_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logGroupId"))

    @log_group_id.setter
    def log_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__417c5975e60fdb0697d74b85327ac0a9d185a8175dbd6c524bc6342aa75e9617)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logGroupId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="logStreamId")
    def log_stream_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logStreamId"))

    @log_stream_id.setter
    def log_stream_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69923373277f0a47e913025ebecadc670b5687ff047f5ba9dd68d0a306a5b946)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logStreamId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="number")
    def number(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "number"))

    @number.setter
    def number(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74f29b33e861fbe88047297719f56e0923237429bee4eca75d08bf877cdf030d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "number", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="searchTimeRange")
    def search_time_range(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "searchTimeRange"))

    @search_time_range.setter
    def search_time_range(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a3ba0bba697c87f781aa270163f7db1e7174913f70e7e4966a83b4abc72463c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "searchTimeRange", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="searchTimeRangeUnit")
    def search_time_range_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "searchTimeRangeUnit"))

    @search_time_range_unit.setter
    def search_time_range_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ad050c3f63790f24942b3be4d167f40603c8f92b2b863fb131208a563106b3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "searchTimeRangeUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LtsKeywordsAlarmRuleV2KeywordsRequests]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LtsKeywordsAlarmRuleV2KeywordsRequests]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LtsKeywordsAlarmRuleV2KeywordsRequests]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98f014852220cb38aa4185c13ea2776a07a32ff868e1ed1dcb43d97d79ff45ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ltsKeywordsAlarmRuleV2.LtsKeywordsAlarmRuleV2NotificationRule",
    jsii_struct_bases=[],
    name_mapping={
        "topics": "topics",
        "user_name": "userName",
        "language": "language",
        "template_name": "templateName",
        "timezone": "timezone",
    },
)
class LtsKeywordsAlarmRuleV2NotificationRule:
    def __init__(
        self,
        *,
        topics: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LtsKeywordsAlarmRuleV2NotificationRuleTopics", typing.Dict[builtins.str, typing.Any]]]],
        user_name: builtins.str,
        language: typing.Optional[builtins.str] = None,
        template_name: typing.Optional[builtins.str] = None,
        timezone: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param topics: topics block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#topics LtsKeywordsAlarmRuleV2#topics}
        :param user_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#user_name LtsKeywordsAlarmRuleV2#user_name}.
        :param language: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#language LtsKeywordsAlarmRuleV2#language}.
        :param template_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#template_name LtsKeywordsAlarmRuleV2#template_name}.
        :param timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#timezone LtsKeywordsAlarmRuleV2#timezone}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66b59531dce107ef2c9eb5fd6e176068a1cd4a6c100e5b3f1f57ac9a08eb8cb7)
            check_type(argname="argument topics", value=topics, expected_type=type_hints["topics"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
            check_type(argname="argument language", value=language, expected_type=type_hints["language"])
            check_type(argname="argument template_name", value=template_name, expected_type=type_hints["template_name"])
            check_type(argname="argument timezone", value=timezone, expected_type=type_hints["timezone"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "topics": topics,
            "user_name": user_name,
        }
        if language is not None:
            self._values["language"] = language
        if template_name is not None:
            self._values["template_name"] = template_name
        if timezone is not None:
            self._values["timezone"] = timezone

    @builtins.property
    def topics(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LtsKeywordsAlarmRuleV2NotificationRuleTopics"]]:
        '''topics block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#topics LtsKeywordsAlarmRuleV2#topics}
        '''
        result = self._values.get("topics")
        assert result is not None, "Required property 'topics' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LtsKeywordsAlarmRuleV2NotificationRuleTopics"]], result)

    @builtins.property
    def user_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#user_name LtsKeywordsAlarmRuleV2#user_name}.'''
        result = self._values.get("user_name")
        assert result is not None, "Required property 'user_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def language(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#language LtsKeywordsAlarmRuleV2#language}.'''
        result = self._values.get("language")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#template_name LtsKeywordsAlarmRuleV2#template_name}.'''
        result = self._values.get("template_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timezone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#timezone LtsKeywordsAlarmRuleV2#timezone}.'''
        result = self._values.get("timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LtsKeywordsAlarmRuleV2NotificationRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LtsKeywordsAlarmRuleV2NotificationRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ltsKeywordsAlarmRuleV2.LtsKeywordsAlarmRuleV2NotificationRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e482af3ef1c20112853ddeb2a19aabd863ad04285f904683944cf8d4efb87ac1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putTopics")
    def put_topics(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["LtsKeywordsAlarmRuleV2NotificationRuleTopics", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa89e9cc874c89a7294bbc30247d650613ae6054d4a7d59d3335ac994aea3452)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTopics", [value]))

    @jsii.member(jsii_name="resetLanguage")
    def reset_language(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLanguage", []))

    @jsii.member(jsii_name="resetTemplateName")
    def reset_template_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTemplateName", []))

    @jsii.member(jsii_name="resetTimezone")
    def reset_timezone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimezone", []))

    @builtins.property
    @jsii.member(jsii_name="topics")
    def topics(self) -> "LtsKeywordsAlarmRuleV2NotificationRuleTopicsList":
        return typing.cast("LtsKeywordsAlarmRuleV2NotificationRuleTopicsList", jsii.get(self, "topics"))

    @builtins.property
    @jsii.member(jsii_name="languageInput")
    def language_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "languageInput"))

    @builtins.property
    @jsii.member(jsii_name="templateNameInput")
    def template_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateNameInput"))

    @builtins.property
    @jsii.member(jsii_name="timezoneInput")
    def timezone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timezoneInput"))

    @builtins.property
    @jsii.member(jsii_name="topicsInput")
    def topics_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LtsKeywordsAlarmRuleV2NotificationRuleTopics"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["LtsKeywordsAlarmRuleV2NotificationRuleTopics"]]], jsii.get(self, "topicsInput"))

    @builtins.property
    @jsii.member(jsii_name="userNameInput")
    def user_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userNameInput"))

    @builtins.property
    @jsii.member(jsii_name="language")
    def language(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "language"))

    @language.setter
    def language(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6c0ca779fa9cc70508e7f963e53df60c65bd4096927e161c10c070592593a4e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "language", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="templateName")
    def template_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "templateName"))

    @template_name.setter
    def template_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc659c50ec7c986717499bfb4148bb39b9a4c6853f7575b0337dc680bd1d82e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timezone")
    def timezone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timezone"))

    @timezone.setter
    def timezone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07c1308a2704eda4b4496c3ca0a9ef5d789825bb5c448c0473d9892f7da3afa7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timezone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userName"))

    @user_name.setter
    def user_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fc066d3f3ecf65c0e7e7dc08aaac39e88d1761d16c3b59167177f62e21811c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[LtsKeywordsAlarmRuleV2NotificationRule]:
        return typing.cast(typing.Optional[LtsKeywordsAlarmRuleV2NotificationRule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[LtsKeywordsAlarmRuleV2NotificationRule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8082d980ae94c9204f05c19a8a30260aef6cb30d3e2ea54d9564b8fee7367094)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-opentelekomcloud.ltsKeywordsAlarmRuleV2.LtsKeywordsAlarmRuleV2NotificationRuleTopics",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "topic_urn": "topicUrn",
        "display_name": "displayName",
        "push_policy": "pushPolicy",
    },
)
class LtsKeywordsAlarmRuleV2NotificationRuleTopics:
    def __init__(
        self,
        *,
        name: builtins.str,
        topic_urn: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
        push_policy: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#name LtsKeywordsAlarmRuleV2#name}.
        :param topic_urn: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#topic_urn LtsKeywordsAlarmRuleV2#topic_urn}.
        :param display_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#display_name LtsKeywordsAlarmRuleV2#display_name}.
        :param push_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#push_policy LtsKeywordsAlarmRuleV2#push_policy}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__071094c6591478073af0ab1d06a3f11285ec8260d7e5f563b94cf6895afb0b39)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument topic_urn", value=topic_urn, expected_type=type_hints["topic_urn"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument push_policy", value=push_policy, expected_type=type_hints["push_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "topic_urn": topic_urn,
        }
        if display_name is not None:
            self._values["display_name"] = display_name
        if push_policy is not None:
            self._values["push_policy"] = push_policy

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#name LtsKeywordsAlarmRuleV2#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def topic_urn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#topic_urn LtsKeywordsAlarmRuleV2#topic_urn}.'''
        result = self._values.get("topic_urn")
        assert result is not None, "Required property 'topic_urn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#display_name LtsKeywordsAlarmRuleV2#display_name}.'''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def push_policy(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/opentelekomcloud/opentelekomcloud/1.36.44/docs/resources/lts_keywords_alarm_rule_v2#push_policy LtsKeywordsAlarmRuleV2#push_policy}.'''
        result = self._values.get("push_policy")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LtsKeywordsAlarmRuleV2NotificationRuleTopics(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class LtsKeywordsAlarmRuleV2NotificationRuleTopicsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ltsKeywordsAlarmRuleV2.LtsKeywordsAlarmRuleV2NotificationRuleTopicsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5648b2cc7d7aa9f35b5719d2386ac61996fd2e24462991f0580a59b8fa57cc08)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "LtsKeywordsAlarmRuleV2NotificationRuleTopicsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5f2671b6a0ebc17fbc12f6684fc297d795cf9660ca43de846a231979ece48cf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("LtsKeywordsAlarmRuleV2NotificationRuleTopicsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b81bc61d269b6d547c12e0c34b20eafa3db8732e5054dd13c016126655c36106)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0ab47d610d1ec63cbe7db552a47c5557d10c34d12ceb550ddc9cea0bf0e2318)
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
            type_hints = typing.get_type_hints(_typecheckingstub__09693d534fa31eaa84247a153611c95b4ecbb2775fed17c83f9b87ba6caa2900)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LtsKeywordsAlarmRuleV2NotificationRuleTopics]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LtsKeywordsAlarmRuleV2NotificationRuleTopics]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LtsKeywordsAlarmRuleV2NotificationRuleTopics]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aae32a28998b8dbeff9248f38644d5ef13ed51a52c75d7286ae11ff2f37f49d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class LtsKeywordsAlarmRuleV2NotificationRuleTopicsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-opentelekomcloud.ltsKeywordsAlarmRuleV2.LtsKeywordsAlarmRuleV2NotificationRuleTopicsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2f94f211283b1f28d2beca63832e599965373cf57dab51b149398c135cb7011)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDisplayName")
    def reset_display_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisplayName", []))

    @jsii.member(jsii_name="resetPushPolicy")
    def reset_push_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPushPolicy", []))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="pushPolicyInput")
    def push_policy_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "pushPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="topicUrnInput")
    def topic_urn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "topicUrnInput"))

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e8d4268b9542b214edad4c8551f7b74d9766d5b1a508ce734ad2ac6060f1084)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__912d66f781fd78146fb68f4d094551c6a4d52abcd8d323930427846216263d05)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="pushPolicy")
    def push_policy(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "pushPolicy"))

    @push_policy.setter
    def push_policy(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__359c63a542840b8022954b03205a82138162023325c4172d5a9916af2183b712)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pushPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="topicUrn")
    def topic_urn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "topicUrn"))

    @topic_urn.setter
    def topic_urn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94a53d64f0fddf321c2d3085fbadcc68a2a8f9b29f9c778c2940d8d7754694ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topicUrn", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LtsKeywordsAlarmRuleV2NotificationRuleTopics]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LtsKeywordsAlarmRuleV2NotificationRuleTopics]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LtsKeywordsAlarmRuleV2NotificationRuleTopics]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d956c3af7de2b6d2c397d9e1d585432f5a337442993cb4666182187ecf19d6d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "LtsKeywordsAlarmRuleV2",
    "LtsKeywordsAlarmRuleV2Config",
    "LtsKeywordsAlarmRuleV2Frequency",
    "LtsKeywordsAlarmRuleV2FrequencyOutputReference",
    "LtsKeywordsAlarmRuleV2KeywordsRequests",
    "LtsKeywordsAlarmRuleV2KeywordsRequestsList",
    "LtsKeywordsAlarmRuleV2KeywordsRequestsOutputReference",
    "LtsKeywordsAlarmRuleV2NotificationRule",
    "LtsKeywordsAlarmRuleV2NotificationRuleOutputReference",
    "LtsKeywordsAlarmRuleV2NotificationRuleTopics",
    "LtsKeywordsAlarmRuleV2NotificationRuleTopicsList",
    "LtsKeywordsAlarmRuleV2NotificationRuleTopicsOutputReference",
]

publication.publish()

def _typecheckingstub__3267343746fbc14a83f47b763f486b412c53efa4fb29810ce75b68bf43bd4b6a(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    frequency: typing.Union[LtsKeywordsAlarmRuleV2Frequency, typing.Dict[builtins.str, typing.Any]],
    keywords_requests: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LtsKeywordsAlarmRuleV2KeywordsRequests, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    notification_frequency: jsii.Number,
    severity: builtins.str,
    alarm_action_rule_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    notification_rule: typing.Optional[typing.Union[LtsKeywordsAlarmRuleV2NotificationRule, typing.Dict[builtins.str, typing.Any]]] = None,
    recovery_policy: typing.Optional[jsii.Number] = None,
    send_notifications: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    send_recovery_notifications: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    trigger_condition_count: typing.Optional[jsii.Number] = None,
    trigger_condition_frequency: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__1e6d28fd03977d6d4c0b11fdffd545a86a9476297e32c6786d01222f7bfa1215(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58d1afbee2075f9c631acbf1bd0d5c72f31613ee9dded5204cc9e2ae38f51119(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LtsKeywordsAlarmRuleV2KeywordsRequests, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46f6675c590bc7469cd1f97210308f0b9ca09e026a79db162a0a4ae1763ac0d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f46b46258e6b5cb0f9972e5bd698db97e2533a2106efb0d09148d83e176d743f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b3882bb8296cac85716730ad221a9f8cf3c010a16859d8681a78eac15fcc364(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5797af2e89dc416c4450c21d81b711c613a3c4d319051b404cc42f884e6813d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36d50fdb924782e1114d70c374c3583d73ffb5802b675e29b8209ac077a1084e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a7651e570259b89346591912c19d13af6634fced9cccfe1cd50c159868a8df3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e10f0d1a8d38cb84977b1a8457f19e38b1a4709731f36c3dc13be997c3cab5ed(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b982ea186a7ecb408bc7757ca50b4f1af6c37789ed67e15e9acfd43ffa1dc8e4(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__933b8fe996355971c5d054b1d5b3e0eb2a5101464b5727445ee04aa438899d06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d369051290fa61458216e931ea8f4db4ce4e93bf59d8c77040cb16efc2c51682(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80b7c0dab5801d888f69f5171b3f7535c6db4869b9f7f1795940371d0becde48(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ece74d20fd14026d28a3beaff59ac76b5d99274cd7c08c4c03d44c98a1fa3a28(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    frequency: typing.Union[LtsKeywordsAlarmRuleV2Frequency, typing.Dict[builtins.str, typing.Any]],
    keywords_requests: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LtsKeywordsAlarmRuleV2KeywordsRequests, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    notification_frequency: jsii.Number,
    severity: builtins.str,
    alarm_action_rule_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    notification_rule: typing.Optional[typing.Union[LtsKeywordsAlarmRuleV2NotificationRule, typing.Dict[builtins.str, typing.Any]]] = None,
    recovery_policy: typing.Optional[jsii.Number] = None,
    send_notifications: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    send_recovery_notifications: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    trigger_condition_count: typing.Optional[jsii.Number] = None,
    trigger_condition_frequency: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a683eaf7083a9e996a9d2b3a7eb8a4121da82a0fb242a651d8b298ed759a6bed(
    *,
    type: builtins.str,
    cron_expression: typing.Optional[builtins.str] = None,
    day_of_week: typing.Optional[jsii.Number] = None,
    fixed_rate: typing.Optional[jsii.Number] = None,
    fixed_rate_unit: typing.Optional[builtins.str] = None,
    hour_of_day: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__139714787e9af7e5d5fbc96d1ae9bf7e2f179127d41e12bbea3aa56bce530fa6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1489733b967e7628a25ee5ba842a5abab43746376d95fa8d3f39e5733b2121f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be58b243011c39162a31a73e5cb14420edcb6ef922817e7a51092d167f1d2bd5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f701dbf9cddd59b8f570de498c84769b427aeb420281380f33fab99ec194f01(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87054ff2a9c658c7a1ecbc3c13e7fcaa9618ff3922b35cf63c144dcbef106885(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bbbd9e32b4cf1ceba81ff451f2ae031d61601a4e43b4186a4b190c41672ad6f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__080de96ff28864ec701f65b235c37a0ca056c6685eca6f4bd685f4539fd0c4f4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca9d77963761a120b0da947ea3872b2aff7d697e89d8454367ff173b1541ae4b(
    value: typing.Optional[LtsKeywordsAlarmRuleV2Frequency],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7508e6df88079e2b222f5d6f51322c521073caa3fd2bb99b3ed0c52763815fea(
    *,
    condition: builtins.str,
    keyword: builtins.str,
    log_group_id: builtins.str,
    log_stream_id: builtins.str,
    number: jsii.Number,
    search_time_range: jsii.Number,
    search_time_range_unit: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80616a35aa07a0332148f76e94334647bccbbb09ef23e0b103d84a9212742287(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c873490196f06f151389b167d8db81acf6b6fba45cbf5cc27015839ab14a45f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44164ad2c91d44c9525dc97af2c3b4af4b79ef7930a7711b8eeac8ba9343a421(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7cf199d689a03b2db8b0f1a42091734df37ac352d0e104fa0963a95d06dbde3(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91279720926d331f6b5ba46d2ed9e4c23d3fb2a2160e14aa670510011df46df1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77fa0ecfbd958df8b389609fb144f97d82de0b3e1db6c23775756076cd0abd0d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LtsKeywordsAlarmRuleV2KeywordsRequests]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc2c0da5f2fec4042a2403b2650076452ffebf2994e556a6bf2fb4545faa6141(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de60aee2c61b61b07795ee39d09892bbbadb5adfbdaeb04d581438b1797be091(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed4843a1b822034a7957f2486f00eeda60017ab6a338606668461d375136d5bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__417c5975e60fdb0697d74b85327ac0a9d185a8175dbd6c524bc6342aa75e9617(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69923373277f0a47e913025ebecadc670b5687ff047f5ba9dd68d0a306a5b946(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74f29b33e861fbe88047297719f56e0923237429bee4eca75d08bf877cdf030d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a3ba0bba697c87f781aa270163f7db1e7174913f70e7e4966a83b4abc72463c(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ad050c3f63790f24942b3be4d167f40603c8f92b2b863fb131208a563106b3b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98f014852220cb38aa4185c13ea2776a07a32ff868e1ed1dcb43d97d79ff45ae(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LtsKeywordsAlarmRuleV2KeywordsRequests]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66b59531dce107ef2c9eb5fd6e176068a1cd4a6c100e5b3f1f57ac9a08eb8cb7(
    *,
    topics: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LtsKeywordsAlarmRuleV2NotificationRuleTopics, typing.Dict[builtins.str, typing.Any]]]],
    user_name: builtins.str,
    language: typing.Optional[builtins.str] = None,
    template_name: typing.Optional[builtins.str] = None,
    timezone: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e482af3ef1c20112853ddeb2a19aabd863ad04285f904683944cf8d4efb87ac1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa89e9cc874c89a7294bbc30247d650613ae6054d4a7d59d3335ac994aea3452(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[LtsKeywordsAlarmRuleV2NotificationRuleTopics, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6c0ca779fa9cc70508e7f963e53df60c65bd4096927e161c10c070592593a4e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc659c50ec7c986717499bfb4148bb39b9a4c6853f7575b0337dc680bd1d82e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07c1308a2704eda4b4496c3ca0a9ef5d789825bb5c448c0473d9892f7da3afa7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fc066d3f3ecf65c0e7e7dc08aaac39e88d1761d16c3b59167177f62e21811c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8082d980ae94c9204f05c19a8a30260aef6cb30d3e2ea54d9564b8fee7367094(
    value: typing.Optional[LtsKeywordsAlarmRuleV2NotificationRule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__071094c6591478073af0ab1d06a3f11285ec8260d7e5f563b94cf6895afb0b39(
    *,
    name: builtins.str,
    topic_urn: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
    push_policy: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5648b2cc7d7aa9f35b5719d2386ac61996fd2e24462991f0580a59b8fa57cc08(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5f2671b6a0ebc17fbc12f6684fc297d795cf9660ca43de846a231979ece48cf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b81bc61d269b6d547c12e0c34b20eafa3db8732e5054dd13c016126655c36106(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0ab47d610d1ec63cbe7db552a47c5557d10c34d12ceb550ddc9cea0bf0e2318(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09693d534fa31eaa84247a153611c95b4ecbb2775fed17c83f9b87ba6caa2900(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aae32a28998b8dbeff9248f38644d5ef13ed51a52c75d7286ae11ff2f37f49d1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[LtsKeywordsAlarmRuleV2NotificationRuleTopics]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2f94f211283b1f28d2beca63832e599965373cf57dab51b149398c135cb7011(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e8d4268b9542b214edad4c8551f7b74d9766d5b1a508ce734ad2ac6060f1084(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__912d66f781fd78146fb68f4d094551c6a4d52abcd8d323930427846216263d05(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__359c63a542840b8022954b03205a82138162023325c4172d5a9916af2183b712(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94a53d64f0fddf321c2d3085fbadcc68a2a8f9b29f9c778c2940d8d7754694ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d956c3af7de2b6d2c397d9e1d585432f5a337442993cb4666182187ecf19d6d7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, LtsKeywordsAlarmRuleV2NotificationRuleTopics]],
) -> None:
    """Type checking stubs"""
    pass
