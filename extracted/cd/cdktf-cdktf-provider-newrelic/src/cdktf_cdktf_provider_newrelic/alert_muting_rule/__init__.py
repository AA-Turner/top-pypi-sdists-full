r'''
# `newrelic_alert_muting_rule`

Refer to the Terraform Registry for docs: [`newrelic_alert_muting_rule`](https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule).
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


class AlertMutingRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.alertMutingRule.AlertMutingRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule newrelic_alert_muting_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        condition: typing.Union["AlertMutingRuleCondition", typing.Dict[builtins.str, typing.Any]],
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        name: builtins.str,
        account_id: typing.Optional[jsii.Number] = None,
        action_on_muting_rule_window_ended: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[typing.Union["AlertMutingRuleSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule newrelic_alert_muting_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#condition AlertMutingRule#condition}
        :param enabled: Whether the MutingRule is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#enabled AlertMutingRule#enabled}
        :param name: The name of the MutingRule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#name AlertMutingRule#name}
        :param account_id: The account id of the MutingRule.. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#account_id AlertMutingRule#account_id}
        :param action_on_muting_rule_window_ended: The action when the muting rule window is ended or disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#action_on_muting_rule_window_ended AlertMutingRule#action_on_muting_rule_window_ended}
        :param description: The description of the MutingRule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#description AlertMutingRule#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#id AlertMutingRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#schedule AlertMutingRule#schedule}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75b01e35af0ddbadc3017275fd50b647475c9a9d4beb2ed66867aa33c5cf1746)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = AlertMutingRuleConfig(
            condition=condition,
            enabled=enabled,
            name=name,
            account_id=account_id,
            action_on_muting_rule_window_ended=action_on_muting_rule_window_ended,
            description=description,
            id=id,
            schedule=schedule,
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
        '''Generates CDKTF code for importing a AlertMutingRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the AlertMutingRule to import.
        :param import_from_id: The id of the existing AlertMutingRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the AlertMutingRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86a065f14ef53b4aa40a26a6ce456a2951e1492c061b8b9e4136297706118361)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCondition")
    def put_condition(
        self,
        *,
        conditions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AlertMutingRuleConditionConditions", typing.Dict[builtins.str, typing.Any]]]],
        operator: builtins.str,
    ) -> None:
        '''
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#conditions AlertMutingRule#conditions}
        :param operator: The operator used to combine all the MutingRuleConditions within the group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#operator AlertMutingRule#operator}
        '''
        value = AlertMutingRuleCondition(conditions=conditions, operator=operator)

        return typing.cast(None, jsii.invoke(self, "putCondition", [value]))

    @jsii.member(jsii_name="putSchedule")
    def put_schedule(
        self,
        *,
        time_zone: builtins.str,
        end_repeat: typing.Optional[builtins.str] = None,
        end_time: typing.Optional[builtins.str] = None,
        repeat: typing.Optional[builtins.str] = None,
        repeat_count: typing.Optional[jsii.Number] = None,
        start_time: typing.Optional[builtins.str] = None,
        weekly_repeat_days: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param time_zone: The time zone that applies to the MutingRule schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#time_zone AlertMutingRule#time_zone}
        :param end_repeat: The datetime stamp when the MutingRule schedule should stop repeating. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#end_repeat AlertMutingRule#end_repeat}
        :param end_time: The datetime stamp representing when the MutingRule should end. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#end_time AlertMutingRule#end_time}
        :param repeat: The frequency the MutingRule schedule repeats. One of [DAILY, WEEKLY, MONTHLY]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#repeat AlertMutingRule#repeat}
        :param repeat_count: The number of times the MutingRule schedule should repeat. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#repeat_count AlertMutingRule#repeat_count}
        :param start_time: The datetime stamp representing when the MutingRule should start. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#start_time AlertMutingRule#start_time}
        :param weekly_repeat_days: The day(s) of the week that a MutingRule should repeat when the repeat field is set to WEEKLY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#weekly_repeat_days AlertMutingRule#weekly_repeat_days}
        '''
        value = AlertMutingRuleSchedule(
            time_zone=time_zone,
            end_repeat=end_repeat,
            end_time=end_time,
            repeat=repeat,
            repeat_count=repeat_count,
            start_time=start_time,
            weekly_repeat_days=weekly_repeat_days,
        )

        return typing.cast(None, jsii.invoke(self, "putSchedule", [value]))

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetActionOnMutingRuleWindowEnded")
    def reset_action_on_muting_rule_window_ended(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActionOnMutingRuleWindowEnded", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetSchedule")
    def reset_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedule", []))

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
    def condition(self) -> "AlertMutingRuleConditionOutputReference":
        return typing.cast("AlertMutingRuleConditionOutputReference", jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(self) -> "AlertMutingRuleScheduleOutputReference":
        return typing.cast("AlertMutingRuleScheduleOutputReference", jsii.get(self, "schedule"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="actionOnMutingRuleWindowEndedInput")
    def action_on_muting_rule_window_ended_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionOnMutingRuleWindowEndedInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(self) -> typing.Optional["AlertMutingRuleCondition"]:
        return typing.cast(typing.Optional["AlertMutingRuleCondition"], jsii.get(self, "conditionInput"))

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
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(self) -> typing.Optional["AlertMutingRuleSchedule"]:
        return typing.cast(typing.Optional["AlertMutingRuleSchedule"], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67f44702e16e6f0b90930a49fbacb0e71296591cf37955c73a9d2cb1fe683469)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="actionOnMutingRuleWindowEnded")
    def action_on_muting_rule_window_ended(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actionOnMutingRuleWindowEnded"))

    @action_on_muting_rule_window_ended.setter
    def action_on_muting_rule_window_ended(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f8344c0376651e4cd6788e319f68ddc4ab313ca42c350e1e77d1b438b0e42ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionOnMutingRuleWindowEnded", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06e4f54701b85412f602756b3cc9127d96c4f462de6146c299c8a18e31cd4bcf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__198005dfb1c947313c748a2aa43c6f91ddf637eaafe41d90d20226e7c7117557)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d670d69bef36d44150f9e54e83ce5fadaa626275f63a394ca501de75199ddfe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02f3a6b56469a4ee0ee1786249113b0259dfdab5c91c910f08870006e45380ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.alertMutingRule.AlertMutingRuleCondition",
    jsii_struct_bases=[],
    name_mapping={"conditions": "conditions", "operator": "operator"},
)
class AlertMutingRuleCondition:
    def __init__(
        self,
        *,
        conditions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["AlertMutingRuleConditionConditions", typing.Dict[builtins.str, typing.Any]]]],
        operator: builtins.str,
    ) -> None:
        '''
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#conditions AlertMutingRule#conditions}
        :param operator: The operator used to combine all the MutingRuleConditions within the group. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#operator AlertMutingRule#operator}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd98dc98f01ae80b26c4ac029d5f430720dc0ac872180953a8895612d904102b)
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "conditions": conditions,
            "operator": operator,
        }

    @builtins.property
    def conditions(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AlertMutingRuleConditionConditions"]]:
        '''conditions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#conditions AlertMutingRule#conditions}
        '''
        result = self._values.get("conditions")
        assert result is not None, "Required property 'conditions' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["AlertMutingRuleConditionConditions"]], result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''The operator used to combine all the MutingRuleConditions within the group.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#operator AlertMutingRule#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlertMutingRuleCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.alertMutingRule.AlertMutingRuleConditionConditions",
    jsii_struct_bases=[],
    name_mapping={
        "attribute": "attribute",
        "operator": "operator",
        "values": "values",
    },
)
class AlertMutingRuleConditionConditions:
    def __init__(
        self,
        *,
        attribute: builtins.str,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param attribute: The attribute on an incident. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#attribute AlertMutingRule#attribute}
        :param operator: The operator used to compare the attribute's value with the supplied value(s). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#operator AlertMutingRule#operator}
        :param values: The value(s) to compare against the attribute's value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#values AlertMutingRule#values}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8ca093c0cac3cd5291106045e554f8171ec8ad8191031069202247fc142ac4a)
            check_type(argname="argument attribute", value=attribute, expected_type=type_hints["attribute"])
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "attribute": attribute,
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def attribute(self) -> builtins.str:
        '''The attribute on an incident.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#attribute AlertMutingRule#attribute}
        '''
        result = self._values.get("attribute")
        assert result is not None, "Required property 'attribute' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def operator(self) -> builtins.str:
        '''The operator used to compare the attribute's value with the supplied value(s).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#operator AlertMutingRule#operator}
        '''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''The value(s) to compare against the attribute's value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#values AlertMutingRule#values}
        '''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlertMutingRuleConditionConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlertMutingRuleConditionConditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.alertMutingRule.AlertMutingRuleConditionConditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c1d5bb663ce27731f05e723bec903414f3b699a542d43eeebdf6e7956c57c96)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "AlertMutingRuleConditionConditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b9f2844f2a5fcb0b73cb644f14c6f3938e319300c518d3cb245616e717708b2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("AlertMutingRuleConditionConditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e40c2c991a63dec536aa574692b3362ea11c545f3b28162d6cd758e1716a8bbe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a16f5e02ec30fcb77f286c8b35154f99d3a5730713717afef0f77999d053111a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a677a22023f3f227b708177bc01af3c81f1e62fab52545a71dd1946f3f7d7ba1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlertMutingRuleConditionConditions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlertMutingRuleConditionConditions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlertMutingRuleConditionConditions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a98889170dd87f326e2e393cb6649a0266f6b9f966c78c8468049583cc6dada1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AlertMutingRuleConditionConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.alertMutingRule.AlertMutingRuleConditionConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc235251608e30567d4a32eb44b94e74ef4b27e0b9a3a93d32a81b421250de16)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="attributeInput")
    def attribute_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "attributeInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="attribute")
    def attribute(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "attribute"))

    @attribute.setter
    def attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a8c7cdb10c8ee7f227827d4c129a1ab96254c70b89cae5de45fccc4aabcbc32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "attribute", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ddc61a2f13b904676e5eac2e4ff6e876953c1fc85e9c7bb728fed891bfa42c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__684663841c4f6437ffe06974b9d1870bdbdc99ef70fe7c9d3b229795dcb0e3e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlertMutingRuleConditionConditions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlertMutingRuleConditionConditions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlertMutingRuleConditionConditions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5414c2ff5cbee1d1ad90de166ceecfe6d7c8cfd65fd3c2d6005491b6587af29e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class AlertMutingRuleConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.alertMutingRule.AlertMutingRuleConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4456391eb5f0b224b9ffcf7754d9515a09eec6cdecc2b121f4075f6012e718c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConditions")
    def put_conditions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AlertMutingRuleConditionConditions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6941821941da2f263a05a14439a3d71bccd8fc0c29e4ac69a477b23814f1e790)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConditions", [value]))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> AlertMutingRuleConditionConditionsList:
        return typing.cast(AlertMutingRuleConditionConditionsList, jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="conditionsInput")
    def conditions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlertMutingRuleConditionConditions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlertMutingRuleConditionConditions]]], jsii.get(self, "conditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7e67b024a872dc2384e6bf0d750e5b82da97a71eaa894e528d94d4cd8759178)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AlertMutingRuleCondition]:
        return typing.cast(typing.Optional[AlertMutingRuleCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[AlertMutingRuleCondition]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5105f044050a64d8c14394c846a323840975d203de7e3e7234f122cc16daf52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.alertMutingRule.AlertMutingRuleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "condition": "condition",
        "enabled": "enabled",
        "name": "name",
        "account_id": "accountId",
        "action_on_muting_rule_window_ended": "actionOnMutingRuleWindowEnded",
        "description": "description",
        "id": "id",
        "schedule": "schedule",
    },
)
class AlertMutingRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        condition: typing.Union[AlertMutingRuleCondition, typing.Dict[builtins.str, typing.Any]],
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        name: builtins.str,
        account_id: typing.Optional[jsii.Number] = None,
        action_on_muting_rule_window_ended: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[typing.Union["AlertMutingRuleSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#condition AlertMutingRule#condition}
        :param enabled: Whether the MutingRule is enabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#enabled AlertMutingRule#enabled}
        :param name: The name of the MutingRule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#name AlertMutingRule#name}
        :param account_id: The account id of the MutingRule.. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#account_id AlertMutingRule#account_id}
        :param action_on_muting_rule_window_ended: The action when the muting rule window is ended or disabled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#action_on_muting_rule_window_ended AlertMutingRule#action_on_muting_rule_window_ended}
        :param description: The description of the MutingRule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#description AlertMutingRule#description}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#id AlertMutingRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#schedule AlertMutingRule#schedule}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(condition, dict):
            condition = AlertMutingRuleCondition(**condition)
        if isinstance(schedule, dict):
            schedule = AlertMutingRuleSchedule(**schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a4a3adcb9bb344b4b15e43ae584b346cdbd9b9197f7b50c726517b3e0a98860)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument action_on_muting_rule_window_ended", value=action_on_muting_rule_window_ended, expected_type=type_hints["action_on_muting_rule_window_ended"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "condition": condition,
            "enabled": enabled,
            "name": name,
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
        if account_id is not None:
            self._values["account_id"] = account_id
        if action_on_muting_rule_window_ended is not None:
            self._values["action_on_muting_rule_window_ended"] = action_on_muting_rule_window_ended
        if description is not None:
            self._values["description"] = description
        if id is not None:
            self._values["id"] = id
        if schedule is not None:
            self._values["schedule"] = schedule

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
    def condition(self) -> AlertMutingRuleCondition:
        '''condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#condition AlertMutingRule#condition}
        '''
        result = self._values.get("condition")
        assert result is not None, "Required property 'condition' is missing"
        return typing.cast(AlertMutingRuleCondition, result)

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Whether the MutingRule is enabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#enabled AlertMutingRule#enabled}
        '''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the MutingRule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#name AlertMutingRule#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_id(self) -> typing.Optional[jsii.Number]:
        '''The account id of the MutingRule..

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#account_id AlertMutingRule#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def action_on_muting_rule_window_ended(self) -> typing.Optional[builtins.str]:
        '''The action when the muting rule window is ended or disabled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#action_on_muting_rule_window_ended AlertMutingRule#action_on_muting_rule_window_ended}
        '''
        result = self._values.get("action_on_muting_rule_window_ended")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the MutingRule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#description AlertMutingRule#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#id AlertMutingRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def schedule(self) -> typing.Optional["AlertMutingRuleSchedule"]:
        '''schedule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#schedule AlertMutingRule#schedule}
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional["AlertMutingRuleSchedule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlertMutingRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-newrelic.alertMutingRule.AlertMutingRuleSchedule",
    jsii_struct_bases=[],
    name_mapping={
        "time_zone": "timeZone",
        "end_repeat": "endRepeat",
        "end_time": "endTime",
        "repeat": "repeat",
        "repeat_count": "repeatCount",
        "start_time": "startTime",
        "weekly_repeat_days": "weeklyRepeatDays",
    },
)
class AlertMutingRuleSchedule:
    def __init__(
        self,
        *,
        time_zone: builtins.str,
        end_repeat: typing.Optional[builtins.str] = None,
        end_time: typing.Optional[builtins.str] = None,
        repeat: typing.Optional[builtins.str] = None,
        repeat_count: typing.Optional[jsii.Number] = None,
        start_time: typing.Optional[builtins.str] = None,
        weekly_repeat_days: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param time_zone: The time zone that applies to the MutingRule schedule. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#time_zone AlertMutingRule#time_zone}
        :param end_repeat: The datetime stamp when the MutingRule schedule should stop repeating. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#end_repeat AlertMutingRule#end_repeat}
        :param end_time: The datetime stamp representing when the MutingRule should end. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#end_time AlertMutingRule#end_time}
        :param repeat: The frequency the MutingRule schedule repeats. One of [DAILY, WEEKLY, MONTHLY]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#repeat AlertMutingRule#repeat}
        :param repeat_count: The number of times the MutingRule schedule should repeat. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#repeat_count AlertMutingRule#repeat_count}
        :param start_time: The datetime stamp representing when the MutingRule should start. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#start_time AlertMutingRule#start_time}
        :param weekly_repeat_days: The day(s) of the week that a MutingRule should repeat when the repeat field is set to WEEKLY. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#weekly_repeat_days AlertMutingRule#weekly_repeat_days}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a6411425d56d8aeb41c89558fa120864d42b91b654b108c44f191df98a7fec4)
            check_type(argname="argument time_zone", value=time_zone, expected_type=type_hints["time_zone"])
            check_type(argname="argument end_repeat", value=end_repeat, expected_type=type_hints["end_repeat"])
            check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
            check_type(argname="argument repeat", value=repeat, expected_type=type_hints["repeat"])
            check_type(argname="argument repeat_count", value=repeat_count, expected_type=type_hints["repeat_count"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            check_type(argname="argument weekly_repeat_days", value=weekly_repeat_days, expected_type=type_hints["weekly_repeat_days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "time_zone": time_zone,
        }
        if end_repeat is not None:
            self._values["end_repeat"] = end_repeat
        if end_time is not None:
            self._values["end_time"] = end_time
        if repeat is not None:
            self._values["repeat"] = repeat
        if repeat_count is not None:
            self._values["repeat_count"] = repeat_count
        if start_time is not None:
            self._values["start_time"] = start_time
        if weekly_repeat_days is not None:
            self._values["weekly_repeat_days"] = weekly_repeat_days

    @builtins.property
    def time_zone(self) -> builtins.str:
        '''The time zone that applies to the MutingRule schedule.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#time_zone AlertMutingRule#time_zone}
        '''
        result = self._values.get("time_zone")
        assert result is not None, "Required property 'time_zone' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def end_repeat(self) -> typing.Optional[builtins.str]:
        '''The datetime stamp when the MutingRule schedule should stop repeating.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#end_repeat AlertMutingRule#end_repeat}
        '''
        result = self._values.get("end_repeat")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def end_time(self) -> typing.Optional[builtins.str]:
        '''The datetime stamp representing when the MutingRule should end.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#end_time AlertMutingRule#end_time}
        '''
        result = self._values.get("end_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repeat(self) -> typing.Optional[builtins.str]:
        '''The frequency the MutingRule schedule repeats. One of [DAILY, WEEKLY, MONTHLY].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#repeat AlertMutingRule#repeat}
        '''
        result = self._values.get("repeat")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repeat_count(self) -> typing.Optional[jsii.Number]:
        '''The number of times the MutingRule schedule should repeat.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#repeat_count AlertMutingRule#repeat_count}
        '''
        result = self._values.get("repeat_count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def start_time(self) -> typing.Optional[builtins.str]:
        '''The datetime stamp representing when the MutingRule should start.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#start_time AlertMutingRule#start_time}
        '''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def weekly_repeat_days(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The day(s) of the week that a MutingRule should repeat when the repeat field is set to WEEKLY.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/newrelic/newrelic/3.69.1/docs/resources/alert_muting_rule#weekly_repeat_days AlertMutingRule#weekly_repeat_days}
        '''
        result = self._values.get("weekly_repeat_days")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AlertMutingRuleSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AlertMutingRuleScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-newrelic.alertMutingRule.AlertMutingRuleScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7b1223f28a487f82f24d1a5348df3e5fe806cf7511aee58c2366b21e7fce3e6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEndRepeat")
    def reset_end_repeat(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndRepeat", []))

    @jsii.member(jsii_name="resetEndTime")
    def reset_end_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndTime", []))

    @jsii.member(jsii_name="resetRepeat")
    def reset_repeat(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepeat", []))

    @jsii.member(jsii_name="resetRepeatCount")
    def reset_repeat_count(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRepeatCount", []))

    @jsii.member(jsii_name="resetStartTime")
    def reset_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTime", []))

    @jsii.member(jsii_name="resetWeeklyRepeatDays")
    def reset_weekly_repeat_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeeklyRepeatDays", []))

    @builtins.property
    @jsii.member(jsii_name="endRepeatInput")
    def end_repeat_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endRepeatInput"))

    @builtins.property
    @jsii.member(jsii_name="endTimeInput")
    def end_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="repeatCountInput")
    def repeat_count_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "repeatCountInput"))

    @builtins.property
    @jsii.member(jsii_name="repeatInput")
    def repeat_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repeatInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="timeZoneInput")
    def time_zone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timeZoneInput"))

    @builtins.property
    @jsii.member(jsii_name="weeklyRepeatDaysInput")
    def weekly_repeat_days_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "weeklyRepeatDaysInput"))

    @builtins.property
    @jsii.member(jsii_name="endRepeat")
    def end_repeat(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endRepeat"))

    @end_repeat.setter
    def end_repeat(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bfec4eb5b7d89318807b98ae80126fd26889c8be0a84ca9d3357182c3838726)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endRepeat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endTime"))

    @end_time.setter
    def end_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__854d790aed279e416c23e976ecc4dc1586798f2954f81be8cef7d64bd863ede1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repeat")
    def repeat(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repeat"))

    @repeat.setter
    def repeat(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52fc2dc589540161226a26a780c6e5a4716e65929d3271a4821e6b4e60c4afb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repeat", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="repeatCount")
    def repeat_count(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "repeatCount"))

    @repeat_count.setter
    def repeat_count(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85320e53b0259667c246dc09d84338fc86bbf10dcf62a4acf120d0e57197e8b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repeatCount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36ef0355ccf1ffeb984503886754e827e0a04c433cb10825a83b695b508b9599)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timeZone")
    def time_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timeZone"))

    @time_zone.setter
    def time_zone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c173df0a54f9b23ccfc4843dc06888ff8c26f6e0e9b29903c6502cecafadd2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timeZone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weeklyRepeatDays")
    def weekly_repeat_days(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "weeklyRepeatDays"))

    @weekly_repeat_days.setter
    def weekly_repeat_days(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62358c2a69cc7b97526742addf637407e6e03807dd3f43269105a5e855ef8ffc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weeklyRepeatDays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[AlertMutingRuleSchedule]:
        return typing.cast(typing.Optional[AlertMutingRuleSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[AlertMutingRuleSchedule]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3059dd44c48f123f9965923fa12ba16346346a43550a04cf43699c32594dc1d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "AlertMutingRule",
    "AlertMutingRuleCondition",
    "AlertMutingRuleConditionConditions",
    "AlertMutingRuleConditionConditionsList",
    "AlertMutingRuleConditionConditionsOutputReference",
    "AlertMutingRuleConditionOutputReference",
    "AlertMutingRuleConfig",
    "AlertMutingRuleSchedule",
    "AlertMutingRuleScheduleOutputReference",
]

publication.publish()

def _typecheckingstub__75b01e35af0ddbadc3017275fd50b647475c9a9d4beb2ed66867aa33c5cf1746(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    condition: typing.Union[AlertMutingRuleCondition, typing.Dict[builtins.str, typing.Any]],
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    name: builtins.str,
    account_id: typing.Optional[jsii.Number] = None,
    action_on_muting_rule_window_ended: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[typing.Union[AlertMutingRuleSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__86a065f14ef53b4aa40a26a6ce456a2951e1492c061b8b9e4136297706118361(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67f44702e16e6f0b90930a49fbacb0e71296591cf37955c73a9d2cb1fe683469(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f8344c0376651e4cd6788e319f68ddc4ab313ca42c350e1e77d1b438b0e42ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06e4f54701b85412f602756b3cc9127d96c4f462de6146c299c8a18e31cd4bcf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__198005dfb1c947313c748a2aa43c6f91ddf637eaafe41d90d20226e7c7117557(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d670d69bef36d44150f9e54e83ce5fadaa626275f63a394ca501de75199ddfe7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02f3a6b56469a4ee0ee1786249113b0259dfdab5c91c910f08870006e45380ec(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd98dc98f01ae80b26c4ac029d5f430720dc0ac872180953a8895612d904102b(
    *,
    conditions: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AlertMutingRuleConditionConditions, typing.Dict[builtins.str, typing.Any]]]],
    operator: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8ca093c0cac3cd5291106045e554f8171ec8ad8191031069202247fc142ac4a(
    *,
    attribute: builtins.str,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c1d5bb663ce27731f05e723bec903414f3b699a542d43eeebdf6e7956c57c96(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b9f2844f2a5fcb0b73cb644f14c6f3938e319300c518d3cb245616e717708b2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e40c2c991a63dec536aa574692b3362ea11c545f3b28162d6cd758e1716a8bbe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a16f5e02ec30fcb77f286c8b35154f99d3a5730713717afef0f77999d053111a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a677a22023f3f227b708177bc01af3c81f1e62fab52545a71dd1946f3f7d7ba1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a98889170dd87f326e2e393cb6649a0266f6b9f966c78c8468049583cc6dada1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[AlertMutingRuleConditionConditions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc235251608e30567d4a32eb44b94e74ef4b27e0b9a3a93d32a81b421250de16(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a8c7cdb10c8ee7f227827d4c129a1ab96254c70b89cae5de45fccc4aabcbc32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ddc61a2f13b904676e5eac2e4ff6e876953c1fc85e9c7bb728fed891bfa42c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__684663841c4f6437ffe06974b9d1870bdbdc99ef70fe7c9d3b229795dcb0e3e6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5414c2ff5cbee1d1ad90de166ceecfe6d7c8cfd65fd3c2d6005491b6587af29e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, AlertMutingRuleConditionConditions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4456391eb5f0b224b9ffcf7754d9515a09eec6cdecc2b121f4075f6012e718c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6941821941da2f263a05a14439a3d71bccd8fc0c29e4ac69a477b23814f1e790(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[AlertMutingRuleConditionConditions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7e67b024a872dc2384e6bf0d750e5b82da97a71eaa894e528d94d4cd8759178(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5105f044050a64d8c14394c846a323840975d203de7e3e7234f122cc16daf52(
    value: typing.Optional[AlertMutingRuleCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a4a3adcb9bb344b4b15e43ae584b346cdbd9b9197f7b50c726517b3e0a98860(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    condition: typing.Union[AlertMutingRuleCondition, typing.Dict[builtins.str, typing.Any]],
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    name: builtins.str,
    account_id: typing.Optional[jsii.Number] = None,
    action_on_muting_rule_window_ended: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[typing.Union[AlertMutingRuleSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a6411425d56d8aeb41c89558fa120864d42b91b654b108c44f191df98a7fec4(
    *,
    time_zone: builtins.str,
    end_repeat: typing.Optional[builtins.str] = None,
    end_time: typing.Optional[builtins.str] = None,
    repeat: typing.Optional[builtins.str] = None,
    repeat_count: typing.Optional[jsii.Number] = None,
    start_time: typing.Optional[builtins.str] = None,
    weekly_repeat_days: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7b1223f28a487f82f24d1a5348df3e5fe806cf7511aee58c2366b21e7fce3e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bfec4eb5b7d89318807b98ae80126fd26889c8be0a84ca9d3357182c3838726(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__854d790aed279e416c23e976ecc4dc1586798f2954f81be8cef7d64bd863ede1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52fc2dc589540161226a26a780c6e5a4716e65929d3271a4821e6b4e60c4afb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85320e53b0259667c246dc09d84338fc86bbf10dcf62a4acf120d0e57197e8b5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36ef0355ccf1ffeb984503886754e827e0a04c433cb10825a83b695b508b9599(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c173df0a54f9b23ccfc4843dc06888ff8c26f6e0e9b29903c6502cecafadd2e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62358c2a69cc7b97526742addf637407e6e03807dd3f43269105a5e855ef8ffc(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3059dd44c48f123f9965923fa12ba16346346a43550a04cf43699c32594dc1d(
    value: typing.Optional[AlertMutingRuleSchedule],
) -> None:
    """Type checking stubs"""
    pass
