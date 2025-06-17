r'''
# `pagerduty_ruleset_rule`

Refer to the Terraform Registry for docs: [`pagerduty_ruleset_rule`](https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule).
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


class RulesetRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule pagerduty_ruleset_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        ruleset: builtins.str,
        actions: typing.Optional[typing.Union["RulesetRuleActions", typing.Dict[builtins.str, typing.Any]]] = None,
        catch_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        conditions: typing.Optional[typing.Union["RulesetRuleConditions", typing.Dict[builtins.str, typing.Any]]] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        position: typing.Optional[jsii.Number] = None,
        time_frame: typing.Optional[typing.Union["RulesetRuleTimeFrame", typing.Dict[builtins.str, typing.Any]]] = None,
        variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule pagerduty_ruleset_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param ruleset: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#ruleset RulesetRule#ruleset}.
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#actions RulesetRule#actions}
        :param catch_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#catch_all RulesetRule#catch_all}.
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#conditions RulesetRule#conditions}
        :param disabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#disabled RulesetRule#disabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#id RulesetRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param position: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#position RulesetRule#position}.
        :param time_frame: time_frame block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#time_frame RulesetRule#time_frame}
        :param variable: variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#variable RulesetRule#variable}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50ea29422583f850e6a7095a18a98829f64a49fbfc7a515631e0b62a97a60da5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = RulesetRuleConfig(
            ruleset=ruleset,
            actions=actions,
            catch_all=catch_all,
            conditions=conditions,
            disabled=disabled,
            id=id,
            position=position,
            time_frame=time_frame,
            variable=variable,
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
        '''Generates CDKTF code for importing a RulesetRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the RulesetRule to import.
        :param import_from_id: The id of the existing RulesetRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the RulesetRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__158ac71fc8cdff1c4b9d5faf31414c250a4b0ecea3e796474f66d01984a47fb4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putActions")
    def put_actions(
        self,
        *,
        annotate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleActionsAnnotate", typing.Dict[builtins.str, typing.Any]]]]] = None,
        event_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleActionsEventAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        extractions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleActionsExtractions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        priority: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleActionsPriority", typing.Dict[builtins.str, typing.Any]]]]] = None,
        route: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleActionsRoute", typing.Dict[builtins.str, typing.Any]]]]] = None,
        severity: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleActionsSeverity", typing.Dict[builtins.str, typing.Any]]]]] = None,
        suppress: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleActionsSuppress", typing.Dict[builtins.str, typing.Any]]]]] = None,
        suspend: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleActionsSuspend", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param annotate: annotate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#annotate RulesetRule#annotate}
        :param event_action: event_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#event_action RulesetRule#event_action}
        :param extractions: extractions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#extractions RulesetRule#extractions}
        :param priority: priority block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#priority RulesetRule#priority}
        :param route: route block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#route RulesetRule#route}
        :param severity: severity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#severity RulesetRule#severity}
        :param suppress: suppress block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#suppress RulesetRule#suppress}
        :param suspend: suspend block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#suspend RulesetRule#suspend}
        '''
        value = RulesetRuleActions(
            annotate=annotate,
            event_action=event_action,
            extractions=extractions,
            priority=priority,
            route=route,
            severity=severity,
            suppress=suppress,
            suspend=suspend,
        )

        return typing.cast(None, jsii.invoke(self, "putActions", [value]))

    @jsii.member(jsii_name="putConditions")
    def put_conditions(
        self,
        *,
        operator: typing.Optional[builtins.str] = None,
        subconditions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleConditionsSubconditions", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#operator RulesetRule#operator}.
        :param subconditions: subconditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#subconditions RulesetRule#subconditions}
        '''
        value = RulesetRuleConditions(operator=operator, subconditions=subconditions)

        return typing.cast(None, jsii.invoke(self, "putConditions", [value]))

    @jsii.member(jsii_name="putTimeFrame")
    def put_time_frame(
        self,
        *,
        active_between: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleTimeFrameActiveBetween", typing.Dict[builtins.str, typing.Any]]]]] = None,
        scheduled_weekly: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleTimeFrameScheduledWeekly", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param active_between: active_between block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#active_between RulesetRule#active_between}
        :param scheduled_weekly: scheduled_weekly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#scheduled_weekly RulesetRule#scheduled_weekly}
        '''
        value = RulesetRuleTimeFrame(
            active_between=active_between, scheduled_weekly=scheduled_weekly
        )

        return typing.cast(None, jsii.invoke(self, "putTimeFrame", [value]))

    @jsii.member(jsii_name="putVariable")
    def put_variable(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleVariable", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d7a8960fe64a32152d8051694ea8fcd580b925aa905c074be5d92d456c5448d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVariable", [value]))

    @jsii.member(jsii_name="resetActions")
    def reset_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActions", []))

    @jsii.member(jsii_name="resetCatchAll")
    def reset_catch_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCatchAll", []))

    @jsii.member(jsii_name="resetConditions")
    def reset_conditions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConditions", []))

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPosition")
    def reset_position(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPosition", []))

    @jsii.member(jsii_name="resetTimeFrame")
    def reset_time_frame(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeFrame", []))

    @jsii.member(jsii_name="resetVariable")
    def reset_variable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVariable", []))

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
    @jsii.member(jsii_name="actions")
    def actions(self) -> "RulesetRuleActionsOutputReference":
        return typing.cast("RulesetRuleActionsOutputReference", jsii.get(self, "actions"))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> "RulesetRuleConditionsOutputReference":
        return typing.cast("RulesetRuleConditionsOutputReference", jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="timeFrame")
    def time_frame(self) -> "RulesetRuleTimeFrameOutputReference":
        return typing.cast("RulesetRuleTimeFrameOutputReference", jsii.get(self, "timeFrame"))

    @builtins.property
    @jsii.member(jsii_name="variable")
    def variable(self) -> "RulesetRuleVariableList":
        return typing.cast("RulesetRuleVariableList", jsii.get(self, "variable"))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(self) -> typing.Optional["RulesetRuleActions"]:
        return typing.cast(typing.Optional["RulesetRuleActions"], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="catchAllInput")
    def catch_all_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "catchAllInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionsInput")
    def conditions_input(self) -> typing.Optional["RulesetRuleConditions"]:
        return typing.cast(typing.Optional["RulesetRuleConditions"], jsii.get(self, "conditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="disabledInput")
    def disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="positionInput")
    def position_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "positionInput"))

    @builtins.property
    @jsii.member(jsii_name="rulesetInput")
    def ruleset_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "rulesetInput"))

    @builtins.property
    @jsii.member(jsii_name="timeFrameInput")
    def time_frame_input(self) -> typing.Optional["RulesetRuleTimeFrame"]:
        return typing.cast(typing.Optional["RulesetRuleTimeFrame"], jsii.get(self, "timeFrameInput"))

    @builtins.property
    @jsii.member(jsii_name="variableInput")
    def variable_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleVariable"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleVariable"]]], jsii.get(self, "variableInput"))

    @builtins.property
    @jsii.member(jsii_name="catchAll")
    def catch_all(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "catchAll"))

    @catch_all.setter
    def catch_all(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec2f4ac0065cb05cda8ee5926dc191f923de25156c6b39ef94c2da79bb09a3a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "catchAll", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="disabled")
    def disabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disabled"))

    @disabled.setter
    def disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68ce0bdbbadc6dc577129079ec9e906c5e52b049a4d6afcff754ce4817ab3449)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dd720d70c03dbc4597550fe77d0b6ef9bb0f18c0fc17acbb992375d172a79ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="position")
    def position(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "position"))

    @position.setter
    def position(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d55a7f5127a45da68f51bae66ab9fed29affb4f67cf97450fa1f886365033b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "position", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="ruleset")
    def ruleset(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ruleset"))

    @ruleset.setter
    def ruleset(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14fd0ff066fb01244e02b565bcee7bf7643fb9403c7aa923af04643e9c60b189)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleset", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleActions",
    jsii_struct_bases=[],
    name_mapping={
        "annotate": "annotate",
        "event_action": "eventAction",
        "extractions": "extractions",
        "priority": "priority",
        "route": "route",
        "severity": "severity",
        "suppress": "suppress",
        "suspend": "suspend",
    },
)
class RulesetRuleActions:
    def __init__(
        self,
        *,
        annotate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleActionsAnnotate", typing.Dict[builtins.str, typing.Any]]]]] = None,
        event_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleActionsEventAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        extractions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleActionsExtractions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        priority: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleActionsPriority", typing.Dict[builtins.str, typing.Any]]]]] = None,
        route: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleActionsRoute", typing.Dict[builtins.str, typing.Any]]]]] = None,
        severity: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleActionsSeverity", typing.Dict[builtins.str, typing.Any]]]]] = None,
        suppress: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleActionsSuppress", typing.Dict[builtins.str, typing.Any]]]]] = None,
        suspend: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleActionsSuspend", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param annotate: annotate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#annotate RulesetRule#annotate}
        :param event_action: event_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#event_action RulesetRule#event_action}
        :param extractions: extractions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#extractions RulesetRule#extractions}
        :param priority: priority block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#priority RulesetRule#priority}
        :param route: route block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#route RulesetRule#route}
        :param severity: severity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#severity RulesetRule#severity}
        :param suppress: suppress block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#suppress RulesetRule#suppress}
        :param suspend: suspend block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#suspend RulesetRule#suspend}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfe3dca542f68574a85d81894a4906d7ec690b9108a051f23b7e4893fa9c6a21)
            check_type(argname="argument annotate", value=annotate, expected_type=type_hints["annotate"])
            check_type(argname="argument event_action", value=event_action, expected_type=type_hints["event_action"])
            check_type(argname="argument extractions", value=extractions, expected_type=type_hints["extractions"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument route", value=route, expected_type=type_hints["route"])
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
            check_type(argname="argument suppress", value=suppress, expected_type=type_hints["suppress"])
            check_type(argname="argument suspend", value=suspend, expected_type=type_hints["suspend"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if annotate is not None:
            self._values["annotate"] = annotate
        if event_action is not None:
            self._values["event_action"] = event_action
        if extractions is not None:
            self._values["extractions"] = extractions
        if priority is not None:
            self._values["priority"] = priority
        if route is not None:
            self._values["route"] = route
        if severity is not None:
            self._values["severity"] = severity
        if suppress is not None:
            self._values["suppress"] = suppress
        if suspend is not None:
            self._values["suspend"] = suspend

    @builtins.property
    def annotate(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleActionsAnnotate"]]]:
        '''annotate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#annotate RulesetRule#annotate}
        '''
        result = self._values.get("annotate")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleActionsAnnotate"]]], result)

    @builtins.property
    def event_action(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleActionsEventAction"]]]:
        '''event_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#event_action RulesetRule#event_action}
        '''
        result = self._values.get("event_action")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleActionsEventAction"]]], result)

    @builtins.property
    def extractions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleActionsExtractions"]]]:
        '''extractions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#extractions RulesetRule#extractions}
        '''
        result = self._values.get("extractions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleActionsExtractions"]]], result)

    @builtins.property
    def priority(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleActionsPriority"]]]:
        '''priority block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#priority RulesetRule#priority}
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleActionsPriority"]]], result)

    @builtins.property
    def route(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleActionsRoute"]]]:
        '''route block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#route RulesetRule#route}
        '''
        result = self._values.get("route")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleActionsRoute"]]], result)

    @builtins.property
    def severity(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleActionsSeverity"]]]:
        '''severity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#severity RulesetRule#severity}
        '''
        result = self._values.get("severity")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleActionsSeverity"]]], result)

    @builtins.property
    def suppress(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleActionsSuppress"]]]:
        '''suppress block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#suppress RulesetRule#suppress}
        '''
        result = self._values.get("suppress")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleActionsSuppress"]]], result)

    @builtins.property
    def suspend(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleActionsSuspend"]]]:
        '''suspend block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#suspend RulesetRule#suspend}
        '''
        result = self._values.get("suspend")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleActionsSuspend"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RulesetRuleActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleActionsAnnotate",
    jsii_struct_bases=[],
    name_mapping={"value": "value"},
)
class RulesetRuleActionsAnnotate:
    def __init__(self, *, value: typing.Optional[builtins.str] = None) -> None:
        '''
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#value RulesetRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00e0465b35f16bea50380b2dc13e0150958e917590704c961eb0970c99a0726f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#value RulesetRule#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RulesetRuleActionsAnnotate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RulesetRuleActionsAnnotateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleActionsAnnotateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fb593145f96c6390fb7252ed6388f819c93f35496a03fa692fb78892f666800)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "RulesetRuleActionsAnnotateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70979ef71e987892f9230f8c4a65163e65e75e1873f2242c468361db4113c051)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RulesetRuleActionsAnnotateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c319cee36d194297735df4c57776a273f749db25195d7884e19bfb57de8ae743)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb0f01e0057de24136fee86ddb7a9c5250c40bd5e04166154250d0b6911dbc30)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0d025c6e364684b73ee6c1b6b5ec4c9aaf80a85928edab2a720045eb38c002c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsAnnotate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsAnnotate]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsAnnotate]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3dd2316728c36558c455b161b0e110b019f3a495ccd351e6ea75547a88ed9d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RulesetRuleActionsAnnotateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleActionsAnnotateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b0a17f9fabd73eac80c7bca73ac1c87421b2331dbc10b7f170b5ceacd42dab31)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9c32a946ee1dbbd84181481e6d0a3958abe7cd25ac5030f37a1acd7ff29cb5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleActionsAnnotate]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleActionsAnnotate]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleActionsAnnotate]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23166cd52df9f270dd4b7e9348a709a163b3a0714c5e06f6b9582e0849f0cec9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleActionsEventAction",
    jsii_struct_bases=[],
    name_mapping={"value": "value"},
)
class RulesetRuleActionsEventAction:
    def __init__(self, *, value: typing.Optional[builtins.str] = None) -> None:
        '''
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#value RulesetRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83da07c82981b6df3b78be0d41f9b2f5e26da2a1f5b425080d03b72c43058dae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#value RulesetRule#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RulesetRuleActionsEventAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RulesetRuleActionsEventActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleActionsEventActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a488c23689d3488609869744fbc8acde752d9a41b7ce1164a712fe5674fb950)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "RulesetRuleActionsEventActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3baba02615dd4b2565db8f73dbe16301cdb250bffa5311beab2c8743617f2b8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RulesetRuleActionsEventActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b10609dba2ca418c10b8c91efcbe2d77e9cbd10b8011f95d60a1c38cabddf920)
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
            type_hints = typing.get_type_hints(_typecheckingstub__30e461c73c9009cf4b83c944e6b41b140fbe3f0cf3604d5dab52679f18ecc4b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__849f0f9922cc28b11f6246d809fc3c5094da377d3116aca8b9caa0073439050a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsEventAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsEventAction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsEventAction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d33b250881c6f4b351289a990ff67f8c551f5413dc4934d0b9383ff0eb7d3060)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RulesetRuleActionsEventActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleActionsEventActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bbdc87768cbedc3fb677015fb05bf37c6aacc9315e1e595a5ac59e8b9da5e6a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91e7027cbdaed631be8271385a16515fe2fdb795ca7b6976d2ab7f7c9c987971)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleActionsEventAction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleActionsEventAction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleActionsEventAction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d046ee5cc59692337edecff8ec5ebc473504cc4480d748a5905459fea9a938d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleActionsExtractions",
    jsii_struct_bases=[],
    name_mapping={
        "regex": "regex",
        "source": "source",
        "target": "target",
        "template": "template",
    },
)
class RulesetRuleActionsExtractions:
    def __init__(
        self,
        *,
        regex: typing.Optional[builtins.str] = None,
        source: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
        template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#regex RulesetRule#regex}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#source RulesetRule#source}.
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#target RulesetRule#target}.
        :param template: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#template RulesetRule#template}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de7bd602a9ba80fb07faf0387c900a960c4d57a047b1a34ce3e6a6c5d43c7975)
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if regex is not None:
            self._values["regex"] = regex
        if source is not None:
            self._values["source"] = source
        if target is not None:
            self._values["target"] = target
        if template is not None:
            self._values["template"] = template

    @builtins.property
    def regex(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#regex RulesetRule#regex}.'''
        result = self._values.get("regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#source RulesetRule#source}.'''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#target RulesetRule#target}.'''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#template RulesetRule#template}.'''
        result = self._values.get("template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RulesetRuleActionsExtractions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RulesetRuleActionsExtractionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleActionsExtractionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9c98c48db8c5cee1e5aea8e1b239b5ff557a0b023171e522a1b60dec220b0236)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "RulesetRuleActionsExtractionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84845fa6167b4888dcc3cdd017a196e8379f3069f3fb98c958024cb41864c630)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RulesetRuleActionsExtractionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc8156d05e414a151f121a7f2ee62b1f026f095bd4d1df27fd919ad262d33c97)
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
            type_hints = typing.get_type_hints(_typecheckingstub__41b496c75ba7cd1d1866c7388e437a27b7cd87e5181058ecd48fde14cbba6cae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2bf0c882c4e6a16630519d151629ede0138aff87328809f15c9776f4b9698c63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsExtractions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsExtractions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsExtractions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75c5fd64a3a13944940edf5316088a027f694dd8b3c0e85783c9d19dd0e02191)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RulesetRuleActionsExtractionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleActionsExtractionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__baf9697e44c7cd5a788949d87c00224310c58b08da052f288599f64935d22547)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetRegex")
    def reset_regex(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRegex", []))

    @jsii.member(jsii_name="resetSource")
    def reset_source(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSource", []))

    @jsii.member(jsii_name="resetTarget")
    def reset_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTarget", []))

    @jsii.member(jsii_name="resetTemplate")
    def reset_template(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTemplate", []))

    @builtins.property
    @jsii.member(jsii_name="regexInput")
    def regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regexInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="targetInput")
    def target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetInput"))

    @builtins.property
    @jsii.member(jsii_name="templateInput")
    def template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateInput"))

    @builtins.property
    @jsii.member(jsii_name="regex")
    def regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regex"))

    @regex.setter
    def regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21e81a1e6949045f106a1fccb348edbc1f7749f6023edea82c71a2d2f71604fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ba26365f4a13c60ba4fc68d10022b3728b8061a32f8a01b6d35f9504f97b809)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e84ffb00ecad80a00e083d9f4b7f840a8826e9c0e152bbb8af0ab5da4bf49c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="template")
    def template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "template"))

    @template.setter
    def template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3caa2c7e17ca3f32e5baa35f86ab61254953d846c5d48d15695addf3861a4ef6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "template", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleActionsExtractions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleActionsExtractions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleActionsExtractions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acadeb7e3c342f7296bb58d0cfa960fbe4967f5250804a08cc2ff2fdfa20221e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RulesetRuleActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2829a09e3963a84877d45525cd126583b365e542c3d3c1d78562c8846ef0ca56)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAnnotate")
    def put_annotate(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RulesetRuleActionsAnnotate, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e40717bf005c0910cab751d174130838847a2708a4b426f1a7580db908231fe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAnnotate", [value]))

    @jsii.member(jsii_name="putEventAction")
    def put_event_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RulesetRuleActionsEventAction, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14d067bcd4af46e4ffc751a632154d3e4046d83e5b2861da10bcfe81f49bc465)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEventAction", [value]))

    @jsii.member(jsii_name="putExtractions")
    def put_extractions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RulesetRuleActionsExtractions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18a9b1bd596ab6fa59038ee5a901936a99d67e1a73bb68b5cb41388f9585e0f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExtractions", [value]))

    @jsii.member(jsii_name="putPriority")
    def put_priority(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleActionsPriority", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e70d462b00d35dcd484dd3b7b2007e5d1600a2e574d4e3a89b01220cd337b0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPriority", [value]))

    @jsii.member(jsii_name="putRoute")
    def put_route(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleActionsRoute", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b52e33fe8e9c0dfe2ce80f302765eb1b6ece95d9dd4862537dfc26ed4ae705ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRoute", [value]))

    @jsii.member(jsii_name="putSeverity")
    def put_severity(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleActionsSeverity", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d81c7da51e0d6ad69ca598b64adbce74db90ccbba38c3b6d7b865da4e2d217a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSeverity", [value]))

    @jsii.member(jsii_name="putSuppress")
    def put_suppress(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleActionsSuppress", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25268f4b434613ce8c06ebaf2a15fdcf67a7e18ef6e5e8bd6cae2bba3e3f7a66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSuppress", [value]))

    @jsii.member(jsii_name="putSuspend")
    def put_suspend(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleActionsSuspend", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d15720d83f7b2b3c3b81a965be34b34a6c1cdae49920ac1d7dfbe2eb537f6b60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSuspend", [value]))

    @jsii.member(jsii_name="resetAnnotate")
    def reset_annotate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotate", []))

    @jsii.member(jsii_name="resetEventAction")
    def reset_event_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventAction", []))

    @jsii.member(jsii_name="resetExtractions")
    def reset_extractions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtractions", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetRoute")
    def reset_route(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRoute", []))

    @jsii.member(jsii_name="resetSeverity")
    def reset_severity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeverity", []))

    @jsii.member(jsii_name="resetSuppress")
    def reset_suppress(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuppress", []))

    @jsii.member(jsii_name="resetSuspend")
    def reset_suspend(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuspend", []))

    @builtins.property
    @jsii.member(jsii_name="annotate")
    def annotate(self) -> RulesetRuleActionsAnnotateList:
        return typing.cast(RulesetRuleActionsAnnotateList, jsii.get(self, "annotate"))

    @builtins.property
    @jsii.member(jsii_name="eventAction")
    def event_action(self) -> RulesetRuleActionsEventActionList:
        return typing.cast(RulesetRuleActionsEventActionList, jsii.get(self, "eventAction"))

    @builtins.property
    @jsii.member(jsii_name="extractions")
    def extractions(self) -> RulesetRuleActionsExtractionsList:
        return typing.cast(RulesetRuleActionsExtractionsList, jsii.get(self, "extractions"))

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> "RulesetRuleActionsPriorityList":
        return typing.cast("RulesetRuleActionsPriorityList", jsii.get(self, "priority"))

    @builtins.property
    @jsii.member(jsii_name="route")
    def route(self) -> "RulesetRuleActionsRouteList":
        return typing.cast("RulesetRuleActionsRouteList", jsii.get(self, "route"))

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(self) -> "RulesetRuleActionsSeverityList":
        return typing.cast("RulesetRuleActionsSeverityList", jsii.get(self, "severity"))

    @builtins.property
    @jsii.member(jsii_name="suppress")
    def suppress(self) -> "RulesetRuleActionsSuppressList":
        return typing.cast("RulesetRuleActionsSuppressList", jsii.get(self, "suppress"))

    @builtins.property
    @jsii.member(jsii_name="suspend")
    def suspend(self) -> "RulesetRuleActionsSuspendList":
        return typing.cast("RulesetRuleActionsSuspendList", jsii.get(self, "suspend"))

    @builtins.property
    @jsii.member(jsii_name="annotateInput")
    def annotate_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsAnnotate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsAnnotate]]], jsii.get(self, "annotateInput"))

    @builtins.property
    @jsii.member(jsii_name="eventActionInput")
    def event_action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsEventAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsEventAction]]], jsii.get(self, "eventActionInput"))

    @builtins.property
    @jsii.member(jsii_name="extractionsInput")
    def extractions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsExtractions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsExtractions]]], jsii.get(self, "extractionsInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleActionsPriority"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleActionsPriority"]]], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="routeInput")
    def route_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleActionsRoute"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleActionsRoute"]]], jsii.get(self, "routeInput"))

    @builtins.property
    @jsii.member(jsii_name="severityInput")
    def severity_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleActionsSeverity"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleActionsSeverity"]]], jsii.get(self, "severityInput"))

    @builtins.property
    @jsii.member(jsii_name="suppressInput")
    def suppress_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleActionsSuppress"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleActionsSuppress"]]], jsii.get(self, "suppressInput"))

    @builtins.property
    @jsii.member(jsii_name="suspendInput")
    def suspend_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleActionsSuspend"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleActionsSuspend"]]], jsii.get(self, "suspendInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RulesetRuleActions]:
        return typing.cast(typing.Optional[RulesetRuleActions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RulesetRuleActions]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ba76e2e94a2b5e3e3e051183fa8a7a7fcd8fb4dc7431358567ec41abeb76d03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleActionsPriority",
    jsii_struct_bases=[],
    name_mapping={"value": "value"},
)
class RulesetRuleActionsPriority:
    def __init__(self, *, value: typing.Optional[builtins.str] = None) -> None:
        '''
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#value RulesetRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a9402221f24986fc7d4e87405dce6f6f84632ae97fa5c85c7664142ef9a7c94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#value RulesetRule#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RulesetRuleActionsPriority(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RulesetRuleActionsPriorityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleActionsPriorityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c4a3c3871e6c3e0e5deb7b19e25dab594effd6aa4120e75f6678a3ba4d10040b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "RulesetRuleActionsPriorityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dd81021d62a26714c42a6adecca1b93d1f7e68c1dc7020c857296b739a67e6d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RulesetRuleActionsPriorityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__652c4a279bd23a0e537828834bca213519c9beeea987f72092b3291114358699)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b0d00a07d99184b3d81393eb9213a364c3b0a24ef9fe65e9b1802eab6667166)
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
            type_hints = typing.get_type_hints(_typecheckingstub__32ff7bb2ad1a2bf97afb902cf596dea62911ae82b2f9107387aac7e4d46debee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsPriority]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsPriority]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsPriority]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd0a9639149584aa7dbef1ca2c2f1be5f1b13cddf7c2014627f8040a5c0d78b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RulesetRuleActionsPriorityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleActionsPriorityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7446013366109ba472f86d6cb573b858344957e301c558242c23b8d038d0cb17)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdd6cf66bc045b9068a3d246e0044dcf04b53bad26d6f6205e4a7debd35202c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleActionsPriority]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleActionsPriority]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleActionsPriority]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4c0a53d3f92ff4a8da8d63a6d53e86daa00d818f53b69f91cfb7d4c709b0d8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleActionsRoute",
    jsii_struct_bases=[],
    name_mapping={"value": "value"},
)
class RulesetRuleActionsRoute:
    def __init__(self, *, value: typing.Optional[builtins.str] = None) -> None:
        '''
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#value RulesetRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ca0f0a715db91fafe9493f0140b920af7df8e60a33e61f3c8a8ff2fd59cb63c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#value RulesetRule#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RulesetRuleActionsRoute(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RulesetRuleActionsRouteList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleActionsRouteList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7dd37a26d199aa7f8fe85659e6592af5ec414c194576317144df9d3d66f9a43)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "RulesetRuleActionsRouteOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c8d72a1c9ef6dffc408a70abf3e5cd0f4b1443d4b41cd8620ef42e5d5664820)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RulesetRuleActionsRouteOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f54a59052e1c178ce4e1776eee32a87c7fddc403217ef5510997cac386b037c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__63ec8681bdbc44e608cfa9309cd5fdc12e46d0a273fc2e204cd6567aa0df1aac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__18e62a10369bd74b9e9f35a79dd069c2b634dc8ab823bd2d2e5a05abde43cb6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsRoute]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsRoute]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsRoute]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69ae4a2b30c631ac6c830dfc59fe1ed102601d76b8e83e0756d9edeafd143a1b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RulesetRuleActionsRouteOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleActionsRouteOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__18662d2b1b0335f275a2021b97fb74bb04614cd2849d694d6b2165d6c4e4ced7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43d0b3f9282b6a965a657ff03346e520be69a115599d93ba4865c1472d4fdd75)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleActionsRoute]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleActionsRoute]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleActionsRoute]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f10337dbe404bd8d0cebfdebc751e960c317e2f5473f9645f42ccbe265d1156)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleActionsSeverity",
    jsii_struct_bases=[],
    name_mapping={"value": "value"},
)
class RulesetRuleActionsSeverity:
    def __init__(self, *, value: typing.Optional[builtins.str] = None) -> None:
        '''
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#value RulesetRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6bcb88a687006a3334a7d569c5ed5cc8db6fce4285e943c5aaca73d99f3035c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#value RulesetRule#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RulesetRuleActionsSeverity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RulesetRuleActionsSeverityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleActionsSeverityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9280dcffdee2769e3dce227a7ca01c7728fa35d6ee847a2d14fb9b22bed53b44)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "RulesetRuleActionsSeverityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d52973cfd22cbeaf9e8cf943d9d6d7d3c0e3795334424e8cd5229ae5b66219d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RulesetRuleActionsSeverityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2eb0469297cd83a482f1ecb0f59ef5b676a08fe7541d8cef07826f8ba10a93b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__84952748bc5bf25cc6698b359550320fa01a1c48511105fe58e01f0d50739ac8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c37a4d1dd4b3690948ac056ea95b9a5e76879895b12c185e970df40e4f959107)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsSeverity]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsSeverity]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsSeverity]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed904c474d210c0667f1865710ab93f5652d2ad026a3ee3334ea56450815ed10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RulesetRuleActionsSeverityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleActionsSeverityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd0d784f9f9ab5187dde8aaacb192b30964adaa5f4c8a6e9b91704f646cb73fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c57d901a54a00605e07f31e8841f4c0b92a9e06a81d42663fdef53ddffdc7857)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleActionsSeverity]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleActionsSeverity]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleActionsSeverity]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad997c8d61159ef9d08307f7edce062a9f176aa8ccc17f3a2e77207879096ef7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleActionsSuppress",
    jsii_struct_bases=[],
    name_mapping={
        "threshold_time_amount": "thresholdTimeAmount",
        "threshold_time_unit": "thresholdTimeUnit",
        "threshold_value": "thresholdValue",
        "value": "value",
    },
)
class RulesetRuleActionsSuppress:
    def __init__(
        self,
        *,
        threshold_time_amount: typing.Optional[jsii.Number] = None,
        threshold_time_unit: typing.Optional[builtins.str] = None,
        threshold_value: typing.Optional[jsii.Number] = None,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param threshold_time_amount: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#threshold_time_amount RulesetRule#threshold_time_amount}.
        :param threshold_time_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#threshold_time_unit RulesetRule#threshold_time_unit}.
        :param threshold_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#threshold_value RulesetRule#threshold_value}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#value RulesetRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d18597a0c1fa5133d7e6ec95bbcb4465e932c1e889e03daee0663ec139105f7)
            check_type(argname="argument threshold_time_amount", value=threshold_time_amount, expected_type=type_hints["threshold_time_amount"])
            check_type(argname="argument threshold_time_unit", value=threshold_time_unit, expected_type=type_hints["threshold_time_unit"])
            check_type(argname="argument threshold_value", value=threshold_value, expected_type=type_hints["threshold_value"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if threshold_time_amount is not None:
            self._values["threshold_time_amount"] = threshold_time_amount
        if threshold_time_unit is not None:
            self._values["threshold_time_unit"] = threshold_time_unit
        if threshold_value is not None:
            self._values["threshold_value"] = threshold_value
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def threshold_time_amount(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#threshold_time_amount RulesetRule#threshold_time_amount}.'''
        result = self._values.get("threshold_time_amount")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def threshold_time_unit(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#threshold_time_unit RulesetRule#threshold_time_unit}.'''
        result = self._values.get("threshold_time_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threshold_value(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#threshold_value RulesetRule#threshold_value}.'''
        result = self._values.get("threshold_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def value(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#value RulesetRule#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RulesetRuleActionsSuppress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RulesetRuleActionsSuppressList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleActionsSuppressList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cc65b01e5a63d6b5b51c03449b9f748d1a0aabde818b7b030e1d72494c81558)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "RulesetRuleActionsSuppressOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dcbfa514377106f47ec123fa8bcff22d6887c88f49bbc1e8992a095968565a8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RulesetRuleActionsSuppressOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c21712ab8b9cc45a4d978facfd3c5b62e235794543e5924b98ea37e345054c35)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a0541812d16f0d88aee16884aea1bd0e2ba7113cc8ddef65c115d95aba8e27c4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__20bc458b358324ac219c7d58c6b637d788e3c3ae22a9a38b9c339da8e7757b7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsSuppress]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsSuppress]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsSuppress]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__182bc178446993dabfa7633f44c3fa1c3747df39cb1bb1132838d0dd2752cd7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RulesetRuleActionsSuppressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleActionsSuppressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__32086022a03a6b9df79b590c80886b7ebf3d1c96e8202eb34804e2634989c401)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetThresholdTimeAmount")
    def reset_threshold_time_amount(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThresholdTimeAmount", []))

    @jsii.member(jsii_name="resetThresholdTimeUnit")
    def reset_threshold_time_unit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThresholdTimeUnit", []))

    @jsii.member(jsii_name="resetThresholdValue")
    def reset_threshold_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetThresholdValue", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="thresholdTimeAmountInput")
    def threshold_time_amount_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "thresholdTimeAmountInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdTimeUnitInput")
    def threshold_time_unit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "thresholdTimeUnitInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdValueInput")
    def threshold_value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "thresholdValueInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="thresholdTimeAmount")
    def threshold_time_amount(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "thresholdTimeAmount"))

    @threshold_time_amount.setter
    def threshold_time_amount(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5f6433d4625a5594dde97885ec033e53f4a906a8c86a302e6581e9cb757f1fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thresholdTimeAmount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="thresholdTimeUnit")
    def threshold_time_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thresholdTimeUnit"))

    @threshold_time_unit.setter
    def threshold_time_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16a4251a170ca7a0de1d6108fbe6f0a7f8f5cc35cde67983ee70467b5f6ada27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thresholdTimeUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="thresholdValue")
    def threshold_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "thresholdValue"))

    @threshold_value.setter
    def threshold_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__515ed164eba9623f2b6257989213cb6695649add1443103f3442db55b31a26ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thresholdValue", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "value"))

    @value.setter
    def value(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__625f91391f8ab5cf76f55a284ac8eb0482a097f3ec0138560e4daf8a91446f1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleActionsSuppress]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleActionsSuppress]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleActionsSuppress]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d83a36a633f44c1a87c93592de58144006e3189cab8f5f8aa151da7107528ff7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleActionsSuspend",
    jsii_struct_bases=[],
    name_mapping={"value": "value"},
)
class RulesetRuleActionsSuspend:
    def __init__(self, *, value: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#value RulesetRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__029a78a41489ceb774cd65795328e818277b7f45b9f0ef8e8476711346f7a9ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def value(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#value RulesetRule#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RulesetRuleActionsSuspend(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RulesetRuleActionsSuspendList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleActionsSuspendList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__55079bec2309dc9988ab2f33d8e5f9743e7b90641f042c91f15c0cfc17836544)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "RulesetRuleActionsSuspendOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de24c870bbdf8e92fc9c1101cebfc79b4e63b0d97872bcab0ff2f6100df7c26e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RulesetRuleActionsSuspendOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c402b092f0e8eaeb51b08d2023e1350c79fb1060d1c159ca70306a1c2b9386e2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__317426c2a040c7c54bdfe79219c8db38d18bcc79d88f1bc457ce6795c19e10b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb7b16f7b6013f9276fd0ba66ab97fbfb45c6a45ce19065a80ca03ca6764e842)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsSuspend]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsSuspend]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsSuspend]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b98d52a6809433284239abb99b27bcbd5af95896117c95abeeb0082edd6ab7e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RulesetRuleActionsSuspendOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleActionsSuspendOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__596dc9da2fb0c03a7bdb57665433d4ef7ae7accc8770f613d55e60d189010948)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "value"))

    @value.setter
    def value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a56bdc368a1990dd3da4708ab5274be5efb7248c07701eb40acfe795447890e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleActionsSuspend]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleActionsSuspend]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleActionsSuspend]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ece9ec672bbd16baa8f922d887fda855a42f5ebabc42339a5c752dab1259e2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleConditions",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "subconditions": "subconditions"},
)
class RulesetRuleConditions:
    def __init__(
        self,
        *,
        operator: typing.Optional[builtins.str] = None,
        subconditions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleConditionsSubconditions", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#operator RulesetRule#operator}.
        :param subconditions: subconditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#subconditions RulesetRule#subconditions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4869ecfe45325ad4f5dd00be0cba315ac019612adfdaa47eb6402994eee897ad)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument subconditions", value=subconditions, expected_type=type_hints["subconditions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if operator is not None:
            self._values["operator"] = operator
        if subconditions is not None:
            self._values["subconditions"] = subconditions

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#operator RulesetRule#operator}.'''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subconditions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleConditionsSubconditions"]]]:
        '''subconditions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#subconditions RulesetRule#subconditions}
        '''
        result = self._values.get("subconditions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleConditionsSubconditions"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RulesetRuleConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RulesetRuleConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__898f4c9a04272e0d74b403ac3a9fc629452885fee8a4c68aca22d9bcea1e9de0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSubconditions")
    def put_subconditions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleConditionsSubconditions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__203c5451aa8d4d8d60c783b71e0b6d3790687264234606f839ef42dea00d632f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSubconditions", [value]))

    @jsii.member(jsii_name="resetOperator")
    def reset_operator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperator", []))

    @jsii.member(jsii_name="resetSubconditions")
    def reset_subconditions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubconditions", []))

    @builtins.property
    @jsii.member(jsii_name="subconditions")
    def subconditions(self) -> "RulesetRuleConditionsSubconditionsList":
        return typing.cast("RulesetRuleConditionsSubconditionsList", jsii.get(self, "subconditions"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="subconditionsInput")
    def subconditions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleConditionsSubconditions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleConditionsSubconditions"]]], jsii.get(self, "subconditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cccaff665febfd35fdccf7b28413a752abc72322ab8e8f04b121f828e0b742bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RulesetRuleConditions]:
        return typing.cast(typing.Optional[RulesetRuleConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RulesetRuleConditions]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87df59bf447d1bd0caaa78a89b6010f9d363486b814b3fb52704c16450fcb32c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleConditionsSubconditions",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "parameter": "parameter"},
)
class RulesetRuleConditionsSubconditions:
    def __init__(
        self,
        *,
        operator: typing.Optional[builtins.str] = None,
        parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleConditionsSubconditionsParameter", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#operator RulesetRule#operator}.
        :param parameter: parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#parameter RulesetRule#parameter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b6e420c00e32be13f5d4de5ad374e0c596c13229109bbc0d5839a3a578d6979)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument parameter", value=parameter, expected_type=type_hints["parameter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if operator is not None:
            self._values["operator"] = operator
        if parameter is not None:
            self._values["parameter"] = parameter

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#operator RulesetRule#operator}.'''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleConditionsSubconditionsParameter"]]]:
        '''parameter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#parameter RulesetRule#parameter}
        '''
        result = self._values.get("parameter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleConditionsSubconditionsParameter"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RulesetRuleConditionsSubconditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RulesetRuleConditionsSubconditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleConditionsSubconditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__67c5199654d7ae32e7268b7239b2d37ff9ff90950509e81cd98dbd1a23a6523e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RulesetRuleConditionsSubconditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5e98a7ec84a27b52a9ba1dabc02b831f4271a63643e23760fa4f48366fcdd5b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RulesetRuleConditionsSubconditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0281596ede52659bcc1115c34ab4a658844d2af00e1e2857f872b656719bc11)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf0dfdabbec4879174d9a8057bac210b6c00b14c3027ca9266412060b62669c2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__157eca7307dc25803c7c69abe29273baca1407f4c999d81294d45e06fc08ade0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleConditionsSubconditions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleConditionsSubconditions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleConditionsSubconditions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__819a49f4070c75b28fd1ad710da3a588c3fe865a178dd57f388c831fed3c5649)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RulesetRuleConditionsSubconditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleConditionsSubconditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b940f86674f87b2156b00a7915a68bb36b2894a33f8984995d06c1d66b590db6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putParameter")
    def put_parameter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleConditionsSubconditionsParameter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0c0509b2564e42f2f650efde02d7a05a8587c24be039c81a24006f095c515d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putParameter", [value]))

    @jsii.member(jsii_name="resetOperator")
    def reset_operator(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperator", []))

    @jsii.member(jsii_name="resetParameter")
    def reset_parameter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameter", []))

    @builtins.property
    @jsii.member(jsii_name="parameter")
    def parameter(self) -> "RulesetRuleConditionsSubconditionsParameterList":
        return typing.cast("RulesetRuleConditionsSubconditionsParameterList", jsii.get(self, "parameter"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="parameterInput")
    def parameter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleConditionsSubconditionsParameter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleConditionsSubconditionsParameter"]]], jsii.get(self, "parameterInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96ef6271c9b321b51f9906b108c9410857553b7aeab3561dabac833f896a95f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleConditionsSubconditions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleConditionsSubconditions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleConditionsSubconditions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0bd3263e1209f5ce54671275549bb4fdfd65ebf70bcf253d233014e3c30937b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleConditionsSubconditionsParameter",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "value": "value"},
)
class RulesetRuleConditionsSubconditionsParameter:
    def __init__(
        self,
        *,
        path: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#path RulesetRule#path}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#value RulesetRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f45a9d4e12f85223e1e0454d63d95084b7798607af423bc1e5fe02cfdbd1a102)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if path is not None:
            self._values["path"] = path
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#path RulesetRule#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#value RulesetRule#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RulesetRuleConditionsSubconditionsParameter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RulesetRuleConditionsSubconditionsParameterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleConditionsSubconditionsParameterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7edcf0958ad5e7918c70c4e57022be6a497f500d27d369728bdd12c749b4c95)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RulesetRuleConditionsSubconditionsParameterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41a56b88c2de6ceadbf78172be7350f5a0b7d8480c58957b0a308eb0596c42ce)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RulesetRuleConditionsSubconditionsParameterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d03aa05ec929816f660513f8da1804473e03b29aadca3c39f900fb1754043028)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f31b2ab2bec584208b00ae2c79b21b145ae01d795247885bdf94ad24c475aa2f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c055e0c52392e0882c5c5e3c1dc2c990322d0c9834dd5aa9574ba7613fdbc9e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleConditionsSubconditionsParameter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleConditionsSubconditionsParameter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleConditionsSubconditionsParameter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f538067f44ef96d9d8f68ee1698dcd02e9f9755602a7c9caf28bdea8489eba7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RulesetRuleConditionsSubconditionsParameterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleConditionsSubconditionsParameterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__23890ccf5c59d8b43d5ea8ab0b5496d77e169652ba141334229f6967178cb122)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e288df82c685bec17b65ab8260b21252e9b4ce7c721164d0b2e23fb69561502a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__149c0be45c867d8ce2709cff2f7c51cd653630f041d4442e4824ed1f30c2d1d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleConditionsSubconditionsParameter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleConditionsSubconditionsParameter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleConditionsSubconditionsParameter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1f74442e8b4aeb96938898e568f536536654ae0b335d9d7f69ebbbb89de68cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "ruleset": "ruleset",
        "actions": "actions",
        "catch_all": "catchAll",
        "conditions": "conditions",
        "disabled": "disabled",
        "id": "id",
        "position": "position",
        "time_frame": "timeFrame",
        "variable": "variable",
    },
)
class RulesetRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        ruleset: builtins.str,
        actions: typing.Optional[typing.Union[RulesetRuleActions, typing.Dict[builtins.str, typing.Any]]] = None,
        catch_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        conditions: typing.Optional[typing.Union[RulesetRuleConditions, typing.Dict[builtins.str, typing.Any]]] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        position: typing.Optional[jsii.Number] = None,
        time_frame: typing.Optional[typing.Union["RulesetRuleTimeFrame", typing.Dict[builtins.str, typing.Any]]] = None,
        variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param ruleset: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#ruleset RulesetRule#ruleset}.
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#actions RulesetRule#actions}
        :param catch_all: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#catch_all RulesetRule#catch_all}.
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#conditions RulesetRule#conditions}
        :param disabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#disabled RulesetRule#disabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#id RulesetRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param position: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#position RulesetRule#position}.
        :param time_frame: time_frame block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#time_frame RulesetRule#time_frame}
        :param variable: variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#variable RulesetRule#variable}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(actions, dict):
            actions = RulesetRuleActions(**actions)
        if isinstance(conditions, dict):
            conditions = RulesetRuleConditions(**conditions)
        if isinstance(time_frame, dict):
            time_frame = RulesetRuleTimeFrame(**time_frame)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f71658c558f17455338e28d51240cc8760ae918b3ed39480df2bfe6bd7f7e22)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument ruleset", value=ruleset, expected_type=type_hints["ruleset"])
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument catch_all", value=catch_all, expected_type=type_hints["catch_all"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument position", value=position, expected_type=type_hints["position"])
            check_type(argname="argument time_frame", value=time_frame, expected_type=type_hints["time_frame"])
            check_type(argname="argument variable", value=variable, expected_type=type_hints["variable"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ruleset": ruleset,
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
        if actions is not None:
            self._values["actions"] = actions
        if catch_all is not None:
            self._values["catch_all"] = catch_all
        if conditions is not None:
            self._values["conditions"] = conditions
        if disabled is not None:
            self._values["disabled"] = disabled
        if id is not None:
            self._values["id"] = id
        if position is not None:
            self._values["position"] = position
        if time_frame is not None:
            self._values["time_frame"] = time_frame
        if variable is not None:
            self._values["variable"] = variable

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
    def ruleset(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#ruleset RulesetRule#ruleset}.'''
        result = self._values.get("ruleset")
        assert result is not None, "Required property 'ruleset' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def actions(self) -> typing.Optional[RulesetRuleActions]:
        '''actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#actions RulesetRule#actions}
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[RulesetRuleActions], result)

    @builtins.property
    def catch_all(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#catch_all RulesetRule#catch_all}.'''
        result = self._values.get("catch_all")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def conditions(self) -> typing.Optional[RulesetRuleConditions]:
        '''conditions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#conditions RulesetRule#conditions}
        '''
        result = self._values.get("conditions")
        return typing.cast(typing.Optional[RulesetRuleConditions], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#disabled RulesetRule#disabled}.'''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#id RulesetRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def position(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#position RulesetRule#position}.'''
        result = self._values.get("position")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def time_frame(self) -> typing.Optional["RulesetRuleTimeFrame"]:
        '''time_frame block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#time_frame RulesetRule#time_frame}
        '''
        result = self._values.get("time_frame")
        return typing.cast(typing.Optional["RulesetRuleTimeFrame"], result)

    @builtins.property
    def variable(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleVariable"]]]:
        '''variable block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#variable RulesetRule#variable}
        '''
        result = self._values.get("variable")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleVariable"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RulesetRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleTimeFrame",
    jsii_struct_bases=[],
    name_mapping={
        "active_between": "activeBetween",
        "scheduled_weekly": "scheduledWeekly",
    },
)
class RulesetRuleTimeFrame:
    def __init__(
        self,
        *,
        active_between: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleTimeFrameActiveBetween", typing.Dict[builtins.str, typing.Any]]]]] = None,
        scheduled_weekly: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleTimeFrameScheduledWeekly", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param active_between: active_between block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#active_between RulesetRule#active_between}
        :param scheduled_weekly: scheduled_weekly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#scheduled_weekly RulesetRule#scheduled_weekly}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1fe321ed962ee55d9955b85c8100708accbcd1b0c2d0918d42e9c44ced324e0)
            check_type(argname="argument active_between", value=active_between, expected_type=type_hints["active_between"])
            check_type(argname="argument scheduled_weekly", value=scheduled_weekly, expected_type=type_hints["scheduled_weekly"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if active_between is not None:
            self._values["active_between"] = active_between
        if scheduled_weekly is not None:
            self._values["scheduled_weekly"] = scheduled_weekly

    @builtins.property
    def active_between(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleTimeFrameActiveBetween"]]]:
        '''active_between block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#active_between RulesetRule#active_between}
        '''
        result = self._values.get("active_between")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleTimeFrameActiveBetween"]]], result)

    @builtins.property
    def scheduled_weekly(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleTimeFrameScheduledWeekly"]]]:
        '''scheduled_weekly block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#scheduled_weekly RulesetRule#scheduled_weekly}
        '''
        result = self._values.get("scheduled_weekly")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleTimeFrameScheduledWeekly"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RulesetRuleTimeFrame(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleTimeFrameActiveBetween",
    jsii_struct_bases=[],
    name_mapping={"end_time": "endTime", "start_time": "startTime"},
)
class RulesetRuleTimeFrameActiveBetween:
    def __init__(
        self,
        *,
        end_time: typing.Optional[jsii.Number] = None,
        start_time: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param end_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#end_time RulesetRule#end_time}.
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#start_time RulesetRule#start_time}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5973c60020f0d857bccd20ef33e296eb367457e93bd071793f2c206894ed755b)
            check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if end_time is not None:
            self._values["end_time"] = end_time
        if start_time is not None:
            self._values["start_time"] = start_time

    @builtins.property
    def end_time(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#end_time RulesetRule#end_time}.'''
        result = self._values.get("end_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def start_time(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#start_time RulesetRule#start_time}.'''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RulesetRuleTimeFrameActiveBetween(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RulesetRuleTimeFrameActiveBetweenList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleTimeFrameActiveBetweenList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee88f342673ceb088899f8542af2a39145e172dfec9ab2b8ed2e0ed7beae5d11)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RulesetRuleTimeFrameActiveBetweenOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bad0e891d51bad2487b57113c0e00c1a38a2e55fcbd05591f0a735b8a51ea58e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RulesetRuleTimeFrameActiveBetweenOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4a96c210e0499fd767eb9fdd24a9b7aac6a7fe7e17a5341dca2f1e7d7a4f315)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d53535cc2a294e4bd2cdda8983fceafb39d982289d5946121ced33ca3786fae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c80b45aca71809b92f295a33ea4c319b52d128580bb71191e76529b9c8526268)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleTimeFrameActiveBetween]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleTimeFrameActiveBetween]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleTimeFrameActiveBetween]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf08fe6f0501f8922c84f587c82338bb93c16283084e3477535d9ceb27bfabac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RulesetRuleTimeFrameActiveBetweenOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleTimeFrameActiveBetweenOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb383b76f75571b86c01dc81985d3b6610015dc90a772cbb2417d719dc765996)
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
    @jsii.member(jsii_name="endTimeInput")
    def end_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "endTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="endTime")
    def end_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "endTime"))

    @end_time.setter
    def end_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__092186fd08b610f2a7727f95bef160a442cd242d5ee94805a3f23f2be6bbf379)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51d43c46e17a512b1e0f4ba3b87f5707061488455d6deda697b1b8cee0e53d8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleTimeFrameActiveBetween]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleTimeFrameActiveBetween]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleTimeFrameActiveBetween]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ff05f1232b9ac2079a393e0bf14a3adcbc54e9b45844d978f1921db63af91a7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RulesetRuleTimeFrameOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleTimeFrameOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d4ce43a9f713dde9f0a9bbc36b5e2167d460a2e2aecdcedcdb727013aa94687)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putActiveBetween")
    def put_active_between(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RulesetRuleTimeFrameActiveBetween, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cf23410949087cf7bf2964f22f133ec19818789ad8833f8e02c53fc2564d2eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putActiveBetween", [value]))

    @jsii.member(jsii_name="putScheduledWeekly")
    def put_scheduled_weekly(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleTimeFrameScheduledWeekly", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ef04553c5de03a256944849b72cf7faf69fc2fdbeaa288632a32a06924962dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putScheduledWeekly", [value]))

    @jsii.member(jsii_name="resetActiveBetween")
    def reset_active_between(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActiveBetween", []))

    @jsii.member(jsii_name="resetScheduledWeekly")
    def reset_scheduled_weekly(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScheduledWeekly", []))

    @builtins.property
    @jsii.member(jsii_name="activeBetween")
    def active_between(self) -> RulesetRuleTimeFrameActiveBetweenList:
        return typing.cast(RulesetRuleTimeFrameActiveBetweenList, jsii.get(self, "activeBetween"))

    @builtins.property
    @jsii.member(jsii_name="scheduledWeekly")
    def scheduled_weekly(self) -> "RulesetRuleTimeFrameScheduledWeeklyList":
        return typing.cast("RulesetRuleTimeFrameScheduledWeeklyList", jsii.get(self, "scheduledWeekly"))

    @builtins.property
    @jsii.member(jsii_name="activeBetweenInput")
    def active_between_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleTimeFrameActiveBetween]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleTimeFrameActiveBetween]]], jsii.get(self, "activeBetweenInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduledWeeklyInput")
    def scheduled_weekly_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleTimeFrameScheduledWeekly"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleTimeFrameScheduledWeekly"]]], jsii.get(self, "scheduledWeeklyInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[RulesetRuleTimeFrame]:
        return typing.cast(typing.Optional[RulesetRuleTimeFrame], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[RulesetRuleTimeFrame]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef86b1729ddac8fd62c96e3b51a1bb3dce133b7f99d2b035f68c5e908cd7867f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleTimeFrameScheduledWeekly",
    jsii_struct_bases=[],
    name_mapping={
        "duration": "duration",
        "start_time": "startTime",
        "timezone": "timezone",
        "weekdays": "weekdays",
    },
)
class RulesetRuleTimeFrameScheduledWeekly:
    def __init__(
        self,
        *,
        duration: typing.Optional[jsii.Number] = None,
        start_time: typing.Optional[jsii.Number] = None,
        timezone: typing.Optional[builtins.str] = None,
        weekdays: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#duration RulesetRule#duration}.
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#start_time RulesetRule#start_time}.
        :param timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#timezone RulesetRule#timezone}.
        :param weekdays: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#weekdays RulesetRule#weekdays}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a395229417c5ee7d4d80750873d2a4205a33b3c652b40f3639cc183838c9825f)
            check_type(argname="argument duration", value=duration, expected_type=type_hints["duration"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
            check_type(argname="argument timezone", value=timezone, expected_type=type_hints["timezone"])
            check_type(argname="argument weekdays", value=weekdays, expected_type=type_hints["weekdays"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if duration is not None:
            self._values["duration"] = duration
        if start_time is not None:
            self._values["start_time"] = start_time
        if timezone is not None:
            self._values["timezone"] = timezone
        if weekdays is not None:
            self._values["weekdays"] = weekdays

    @builtins.property
    def duration(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#duration RulesetRule#duration}.'''
        result = self._values.get("duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def start_time(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#start_time RulesetRule#start_time}.'''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timezone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#timezone RulesetRule#timezone}.'''
        result = self._values.get("timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def weekdays(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#weekdays RulesetRule#weekdays}.'''
        result = self._values.get("weekdays")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RulesetRuleTimeFrameScheduledWeekly(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RulesetRuleTimeFrameScheduledWeeklyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleTimeFrameScheduledWeeklyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bfa07da7fee66a3b24703426e0bbb57f7fa59c0c9b5560f564cffb595d105f3a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "RulesetRuleTimeFrameScheduledWeeklyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fa3a75c3947a064c94a55e95b979e7be9e6ed953c094538d0c1004ef690b1f7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RulesetRuleTimeFrameScheduledWeeklyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90ee9472e6c9254124b436495a377258840df890a7c0495a1d8cf08d5ea9ce33)
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
            type_hints = typing.get_type_hints(_typecheckingstub__538afb8aabf925cca11fa2605cb30ee9b4ff156f358f13a7d49ce0ed728807c0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d08f2b21787bb397916dbf6ba27d6fb857ca5d06aac4157c2be531ee5d42d723)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleTimeFrameScheduledWeekly]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleTimeFrameScheduledWeekly]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleTimeFrameScheduledWeekly]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__233ec5fa0b65c44fc2d2dd5fcd312bcf873474497f8944d9600ba0dc65476ced)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RulesetRuleTimeFrameScheduledWeeklyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleTimeFrameScheduledWeeklyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__09d08615421a2049246f1ba911566ead2f3715bb714c269feaa7605ba8fbe45c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetDuration")
    def reset_duration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDuration", []))

    @jsii.member(jsii_name="resetStartTime")
    def reset_start_time(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStartTime", []))

    @jsii.member(jsii_name="resetTimezone")
    def reset_timezone(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimezone", []))

    @jsii.member(jsii_name="resetWeekdays")
    def reset_weekdays(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWeekdays", []))

    @builtins.property
    @jsii.member(jsii_name="durationInput")
    def duration_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "durationInput"))

    @builtins.property
    @jsii.member(jsii_name="startTimeInput")
    def start_time_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "startTimeInput"))

    @builtins.property
    @jsii.member(jsii_name="timezoneInput")
    def timezone_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "timezoneInput"))

    @builtins.property
    @jsii.member(jsii_name="weekdaysInput")
    def weekdays_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "weekdaysInput"))

    @builtins.property
    @jsii.member(jsii_name="duration")
    def duration(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "duration"))

    @duration.setter
    def duration(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c6ff48ef60751cc56f9ef44bc24cb7522f11681a916bb7e6520a78937535cdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b888b7fa6d210b86420038eb5f41720fcd28c4991b2ba936ff66a4606d001411)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timezone")
    def timezone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timezone"))

    @timezone.setter
    def timezone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__737a6bce72ce8d30ab111ca3d0e9d4ce78dbb2cb69423e17f8e750b3f3d3ee9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timezone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekdays")
    def weekdays(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "weekdays"))

    @weekdays.setter
    def weekdays(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__573208598147a55a10dcba757e3e6b92d2fa45243d8e8de91de6978068338993)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekdays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleTimeFrameScheduledWeekly]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleTimeFrameScheduledWeekly]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleTimeFrameScheduledWeekly]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31a523cef77252ed1728ad9087c2ba3e219b2a3d7eb4b317966c449faea70a61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleVariable",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "parameters": "parameters", "type": "type"},
)
class RulesetRuleVariable:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleVariableParameters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#name RulesetRule#name}.
        :param parameters: parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#parameters RulesetRule#parameters}
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#type RulesetRule#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d21a61c9c24eeeb889074e736821382f924272c7c41539cbcfc91a81566c44a5)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if parameters is not None:
            self._values["parameters"] = parameters
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#name RulesetRule#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleVariableParameters"]]]:
        '''parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#parameters RulesetRule#parameters}
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleVariableParameters"]]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#type RulesetRule#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RulesetRuleVariable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RulesetRuleVariableList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleVariableList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__851d40087afbc325009d9f63fe6aa6202e16543f5dc4be25e756771a29966350)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "RulesetRuleVariableOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9929f62963cfc31ef7095c19fd9185b7193370af469826bb5c1b7e2002f2a135)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RulesetRuleVariableOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__452ae80d83a79120fa84a3a4a6651729f84597bbfb0f8a3bb561c29fe5c72466)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d30b48c81d83c73d3cc807bfee57124feccc8c95e8a8c7c4519bad680bc525d5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb12c1c81281b60e337727a5eea088ff14b2babed1bc95076c9124735a8387f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleVariable]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleVariable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44ba01365d2fa11b909559570ada421d0e99a90146a5365a02037284294cdb52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RulesetRuleVariableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleVariableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50a503784461fc5300cd55276a2b35d1b2db15f46e3df3ad4ac3199a237c9d55)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putParameters")
    def put_parameters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["RulesetRuleVariableParameters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c15b4613f565faadb2e1d33a7c63aeaaae050b9c5518d135739bbfbc252df342)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putParameters", [value]))

    @jsii.member(jsii_name="resetName")
    def reset_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetName", []))

    @jsii.member(jsii_name="resetParameters")
    def reset_parameters(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameters", []))

    @jsii.member(jsii_name="resetType")
    def reset_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetType", []))

    @builtins.property
    @jsii.member(jsii_name="parameters")
    def parameters(self) -> "RulesetRuleVariableParametersList":
        return typing.cast("RulesetRuleVariableParametersList", jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleVariableParameters"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["RulesetRuleVariableParameters"]]], jsii.get(self, "parametersInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75285ce8d8c73acfebc8f30046b592e2c7a2f05343363dce93a64be3687ef73a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2a689a87b58957a5d7825ed4331a343067ae7410b523d654b3d28946aeba4a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleVariable]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleVariable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleVariable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb2360cbf544aae38f09a1c85460ad12b975ed2845a95df545e42c331989f54c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleVariableParameters",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "value": "value"},
)
class RulesetRuleVariableParameters:
    def __init__(
        self,
        *,
        path: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#path RulesetRule#path}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#value RulesetRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a01a31d8a5e77e304f063c99df56b62d002b55bb50f63811f8fd72716ff23f0)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if path is not None:
            self._values["path"] = path
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#path RulesetRule#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/ruleset_rule#value RulesetRule#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RulesetRuleVariableParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class RulesetRuleVariableParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleVariableParametersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf844c7ee2fe0d89d5ba8f358a4c8afcb3b2b317d7cbb1dc28fffa0568ab5f5b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "RulesetRuleVariableParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__046d2a5d851959a88519e86167228a6faf0b0c04d62ce62ce8aa27adc5e22823)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("RulesetRuleVariableParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb21ecb06d9494d01ffc5330a498d9d45eb8c7d9e8fbd6ce71496ac5c910241f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c92e0a14d9d0f0d9d3ebd875ce92564ad472563d8a83f690e1e18a8a455b84f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__965f253ce4cefe6c98a13982340f5383bec6a830026e1dc65e00dfa6105c87df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleVariableParameters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleVariableParameters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleVariableParameters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6c3bc5d04c12af36c07fb5f488b539ae1d19960f3359a20185b0f45cab98557)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class RulesetRuleVariableParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.rulesetRule.RulesetRuleVariableParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a66e16f5f9ef255d21f3704f4234e033c7fe4bd2375fe7e8be0eec1926ff5a52)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__222daaef9773332228dc859b0f1926724f5a24993ebba38ff115d318294c12c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5cba7170efbe4b15c31a041e49448d7bb2c9877b3076af22348143c7aff00eea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleVariableParameters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleVariableParameters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleVariableParameters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69788aee433137427887c96328d5824318073bccb5c921107ee2117a4cb8e2ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "RulesetRule",
    "RulesetRuleActions",
    "RulesetRuleActionsAnnotate",
    "RulesetRuleActionsAnnotateList",
    "RulesetRuleActionsAnnotateOutputReference",
    "RulesetRuleActionsEventAction",
    "RulesetRuleActionsEventActionList",
    "RulesetRuleActionsEventActionOutputReference",
    "RulesetRuleActionsExtractions",
    "RulesetRuleActionsExtractionsList",
    "RulesetRuleActionsExtractionsOutputReference",
    "RulesetRuleActionsOutputReference",
    "RulesetRuleActionsPriority",
    "RulesetRuleActionsPriorityList",
    "RulesetRuleActionsPriorityOutputReference",
    "RulesetRuleActionsRoute",
    "RulesetRuleActionsRouteList",
    "RulesetRuleActionsRouteOutputReference",
    "RulesetRuleActionsSeverity",
    "RulesetRuleActionsSeverityList",
    "RulesetRuleActionsSeverityOutputReference",
    "RulesetRuleActionsSuppress",
    "RulesetRuleActionsSuppressList",
    "RulesetRuleActionsSuppressOutputReference",
    "RulesetRuleActionsSuspend",
    "RulesetRuleActionsSuspendList",
    "RulesetRuleActionsSuspendOutputReference",
    "RulesetRuleConditions",
    "RulesetRuleConditionsOutputReference",
    "RulesetRuleConditionsSubconditions",
    "RulesetRuleConditionsSubconditionsList",
    "RulesetRuleConditionsSubconditionsOutputReference",
    "RulesetRuleConditionsSubconditionsParameter",
    "RulesetRuleConditionsSubconditionsParameterList",
    "RulesetRuleConditionsSubconditionsParameterOutputReference",
    "RulesetRuleConfig",
    "RulesetRuleTimeFrame",
    "RulesetRuleTimeFrameActiveBetween",
    "RulesetRuleTimeFrameActiveBetweenList",
    "RulesetRuleTimeFrameActiveBetweenOutputReference",
    "RulesetRuleTimeFrameOutputReference",
    "RulesetRuleTimeFrameScheduledWeekly",
    "RulesetRuleTimeFrameScheduledWeeklyList",
    "RulesetRuleTimeFrameScheduledWeeklyOutputReference",
    "RulesetRuleVariable",
    "RulesetRuleVariableList",
    "RulesetRuleVariableOutputReference",
    "RulesetRuleVariableParameters",
    "RulesetRuleVariableParametersList",
    "RulesetRuleVariableParametersOutputReference",
]

publication.publish()

def _typecheckingstub__50ea29422583f850e6a7095a18a98829f64a49fbfc7a515631e0b62a97a60da5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    ruleset: builtins.str,
    actions: typing.Optional[typing.Union[RulesetRuleActions, typing.Dict[builtins.str, typing.Any]]] = None,
    catch_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    conditions: typing.Optional[typing.Union[RulesetRuleConditions, typing.Dict[builtins.str, typing.Any]]] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    position: typing.Optional[jsii.Number] = None,
    time_frame: typing.Optional[typing.Union[RulesetRuleTimeFrame, typing.Dict[builtins.str, typing.Any]]] = None,
    variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RulesetRuleVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__158ac71fc8cdff1c4b9d5faf31414c250a4b0ecea3e796474f66d01984a47fb4(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d7a8960fe64a32152d8051694ea8fcd580b925aa905c074be5d92d456c5448d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RulesetRuleVariable, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec2f4ac0065cb05cda8ee5926dc191f923de25156c6b39ef94c2da79bb09a3a2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68ce0bdbbadc6dc577129079ec9e906c5e52b049a4d6afcff754ce4817ab3449(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dd720d70c03dbc4597550fe77d0b6ef9bb0f18c0fc17acbb992375d172a79ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d55a7f5127a45da68f51bae66ab9fed29affb4f67cf97450fa1f886365033b3(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14fd0ff066fb01244e02b565bcee7bf7643fb9403c7aa923af04643e9c60b189(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfe3dca542f68574a85d81894a4906d7ec690b9108a051f23b7e4893fa9c6a21(
    *,
    annotate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RulesetRuleActionsAnnotate, typing.Dict[builtins.str, typing.Any]]]]] = None,
    event_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RulesetRuleActionsEventAction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    extractions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RulesetRuleActionsExtractions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    priority: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RulesetRuleActionsPriority, typing.Dict[builtins.str, typing.Any]]]]] = None,
    route: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RulesetRuleActionsRoute, typing.Dict[builtins.str, typing.Any]]]]] = None,
    severity: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RulesetRuleActionsSeverity, typing.Dict[builtins.str, typing.Any]]]]] = None,
    suppress: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RulesetRuleActionsSuppress, typing.Dict[builtins.str, typing.Any]]]]] = None,
    suspend: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RulesetRuleActionsSuspend, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00e0465b35f16bea50380b2dc13e0150958e917590704c961eb0970c99a0726f(
    *,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fb593145f96c6390fb7252ed6388f819c93f35496a03fa692fb78892f666800(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70979ef71e987892f9230f8c4a65163e65e75e1873f2242c468361db4113c051(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c319cee36d194297735df4c57776a273f749db25195d7884e19bfb57de8ae743(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb0f01e0057de24136fee86ddb7a9c5250c40bd5e04166154250d0b6911dbc30(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d025c6e364684b73ee6c1b6b5ec4c9aaf80a85928edab2a720045eb38c002c5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3dd2316728c36558c455b161b0e110b019f3a495ccd351e6ea75547a88ed9d3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsAnnotate]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0a17f9fabd73eac80c7bca73ac1c87421b2331dbc10b7f170b5ceacd42dab31(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9c32a946ee1dbbd84181481e6d0a3958abe7cd25ac5030f37a1acd7ff29cb5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23166cd52df9f270dd4b7e9348a709a163b3a0714c5e06f6b9582e0849f0cec9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleActionsAnnotate]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83da07c82981b6df3b78be0d41f9b2f5e26da2a1f5b425080d03b72c43058dae(
    *,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a488c23689d3488609869744fbc8acde752d9a41b7ce1164a712fe5674fb950(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3baba02615dd4b2565db8f73dbe16301cdb250bffa5311beab2c8743617f2b8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b10609dba2ca418c10b8c91efcbe2d77e9cbd10b8011f95d60a1c38cabddf920(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30e461c73c9009cf4b83c944e6b41b140fbe3f0cf3604d5dab52679f18ecc4b4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__849f0f9922cc28b11f6246d809fc3c5094da377d3116aca8b9caa0073439050a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d33b250881c6f4b351289a990ff67f8c551f5413dc4934d0b9383ff0eb7d3060(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsEventAction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbdc87768cbedc3fb677015fb05bf37c6aacc9315e1e595a5ac59e8b9da5e6a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91e7027cbdaed631be8271385a16515fe2fdb795ca7b6976d2ab7f7c9c987971(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d046ee5cc59692337edecff8ec5ebc473504cc4480d748a5905459fea9a938d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleActionsEventAction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de7bd602a9ba80fb07faf0387c900a960c4d57a047b1a34ce3e6a6c5d43c7975(
    *,
    regex: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
    target: typing.Optional[builtins.str] = None,
    template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c98c48db8c5cee1e5aea8e1b239b5ff557a0b023171e522a1b60dec220b0236(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84845fa6167b4888dcc3cdd017a196e8379f3069f3fb98c958024cb41864c630(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc8156d05e414a151f121a7f2ee62b1f026f095bd4d1df27fd919ad262d33c97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41b496c75ba7cd1d1866c7388e437a27b7cd87e5181058ecd48fde14cbba6cae(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bf0c882c4e6a16630519d151629ede0138aff87328809f15c9776f4b9698c63(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75c5fd64a3a13944940edf5316088a027f694dd8b3c0e85783c9d19dd0e02191(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsExtractions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baf9697e44c7cd5a788949d87c00224310c58b08da052f288599f64935d22547(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21e81a1e6949045f106a1fccb348edbc1f7749f6023edea82c71a2d2f71604fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ba26365f4a13c60ba4fc68d10022b3728b8061a32f8a01b6d35f9504f97b809(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e84ffb00ecad80a00e083d9f4b7f840a8826e9c0e152bbb8af0ab5da4bf49c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3caa2c7e17ca3f32e5baa35f86ab61254953d846c5d48d15695addf3861a4ef6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acadeb7e3c342f7296bb58d0cfa960fbe4967f5250804a08cc2ff2fdfa20221e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleActionsExtractions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2829a09e3963a84877d45525cd126583b365e542c3d3c1d78562c8846ef0ca56(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e40717bf005c0910cab751d174130838847a2708a4b426f1a7580db908231fe7(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RulesetRuleActionsAnnotate, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14d067bcd4af46e4ffc751a632154d3e4046d83e5b2861da10bcfe81f49bc465(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RulesetRuleActionsEventAction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18a9b1bd596ab6fa59038ee5a901936a99d67e1a73bb68b5cb41388f9585e0f3(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RulesetRuleActionsExtractions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e70d462b00d35dcd484dd3b7b2007e5d1600a2e574d4e3a89b01220cd337b0e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RulesetRuleActionsPriority, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b52e33fe8e9c0dfe2ce80f302765eb1b6ece95d9dd4862537dfc26ed4ae705ac(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RulesetRuleActionsRoute, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d81c7da51e0d6ad69ca598b64adbce74db90ccbba38c3b6d7b865da4e2d217a2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RulesetRuleActionsSeverity, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25268f4b434613ce8c06ebaf2a15fdcf67a7e18ef6e5e8bd6cae2bba3e3f7a66(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RulesetRuleActionsSuppress, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d15720d83f7b2b3c3b81a965be34b34a6c1cdae49920ac1d7dfbe2eb537f6b60(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RulesetRuleActionsSuspend, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ba76e2e94a2b5e3e3e051183fa8a7a7fcd8fb4dc7431358567ec41abeb76d03(
    value: typing.Optional[RulesetRuleActions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a9402221f24986fc7d4e87405dce6f6f84632ae97fa5c85c7664142ef9a7c94(
    *,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4a3c3871e6c3e0e5deb7b19e25dab594effd6aa4120e75f6678a3ba4d10040b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dd81021d62a26714c42a6adecca1b93d1f7e68c1dc7020c857296b739a67e6d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__652c4a279bd23a0e537828834bca213519c9beeea987f72092b3291114358699(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b0d00a07d99184b3d81393eb9213a364c3b0a24ef9fe65e9b1802eab6667166(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32ff7bb2ad1a2bf97afb902cf596dea62911ae82b2f9107387aac7e4d46debee(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd0a9639149584aa7dbef1ca2c2f1be5f1b13cddf7c2014627f8040a5c0d78b2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsPriority]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7446013366109ba472f86d6cb573b858344957e301c558242c23b8d038d0cb17(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdd6cf66bc045b9068a3d246e0044dcf04b53bad26d6f6205e4a7debd35202c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4c0a53d3f92ff4a8da8d63a6d53e86daa00d818f53b69f91cfb7d4c709b0d8b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleActionsPriority]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ca0f0a715db91fafe9493f0140b920af7df8e60a33e61f3c8a8ff2fd59cb63c(
    *,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7dd37a26d199aa7f8fe85659e6592af5ec414c194576317144df9d3d66f9a43(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c8d72a1c9ef6dffc408a70abf3e5cd0f4b1443d4b41cd8620ef42e5d5664820(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f54a59052e1c178ce4e1776eee32a87c7fddc403217ef5510997cac386b037c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63ec8681bdbc44e608cfa9309cd5fdc12e46d0a273fc2e204cd6567aa0df1aac(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18e62a10369bd74b9e9f35a79dd069c2b634dc8ab823bd2d2e5a05abde43cb6d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69ae4a2b30c631ac6c830dfc59fe1ed102601d76b8e83e0756d9edeafd143a1b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsRoute]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18662d2b1b0335f275a2021b97fb74bb04614cd2849d694d6b2165d6c4e4ced7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43d0b3f9282b6a965a657ff03346e520be69a115599d93ba4865c1472d4fdd75(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f10337dbe404bd8d0cebfdebc751e960c317e2f5473f9645f42ccbe265d1156(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleActionsRoute]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6bcb88a687006a3334a7d569c5ed5cc8db6fce4285e943c5aaca73d99f3035c(
    *,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9280dcffdee2769e3dce227a7ca01c7728fa35d6ee847a2d14fb9b22bed53b44(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d52973cfd22cbeaf9e8cf943d9d6d7d3c0e3795334424e8cd5229ae5b66219d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2eb0469297cd83a482f1ecb0f59ef5b676a08fe7541d8cef07826f8ba10a93b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84952748bc5bf25cc6698b359550320fa01a1c48511105fe58e01f0d50739ac8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c37a4d1dd4b3690948ac056ea95b9a5e76879895b12c185e970df40e4f959107(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed904c474d210c0667f1865710ab93f5652d2ad026a3ee3334ea56450815ed10(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsSeverity]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd0d784f9f9ab5187dde8aaacb192b30964adaa5f4c8a6e9b91704f646cb73fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c57d901a54a00605e07f31e8841f4c0b92a9e06a81d42663fdef53ddffdc7857(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad997c8d61159ef9d08307f7edce062a9f176aa8ccc17f3a2e77207879096ef7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleActionsSeverity]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d18597a0c1fa5133d7e6ec95bbcb4465e932c1e889e03daee0663ec139105f7(
    *,
    threshold_time_amount: typing.Optional[jsii.Number] = None,
    threshold_time_unit: typing.Optional[builtins.str] = None,
    threshold_value: typing.Optional[jsii.Number] = None,
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cc65b01e5a63d6b5b51c03449b9f748d1a0aabde818b7b030e1d72494c81558(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dcbfa514377106f47ec123fa8bcff22d6887c88f49bbc1e8992a095968565a8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c21712ab8b9cc45a4d978facfd3c5b62e235794543e5924b98ea37e345054c35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0541812d16f0d88aee16884aea1bd0e2ba7113cc8ddef65c115d95aba8e27c4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20bc458b358324ac219c7d58c6b637d788e3c3ae22a9a38b9c339da8e7757b7e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__182bc178446993dabfa7633f44c3fa1c3747df39cb1bb1132838d0dd2752cd7f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsSuppress]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32086022a03a6b9df79b590c80886b7ebf3d1c96e8202eb34804e2634989c401(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5f6433d4625a5594dde97885ec033e53f4a906a8c86a302e6581e9cb757f1fd(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16a4251a170ca7a0de1d6108fbe6f0a7f8f5cc35cde67983ee70467b5f6ada27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__515ed164eba9623f2b6257989213cb6695649add1443103f3442db55b31a26ff(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__625f91391f8ab5cf76f55a284ac8eb0482a097f3ec0138560e4daf8a91446f1f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d83a36a633f44c1a87c93592de58144006e3189cab8f5f8aa151da7107528ff7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleActionsSuppress]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__029a78a41489ceb774cd65795328e818277b7f45b9f0ef8e8476711346f7a9ec(
    *,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55079bec2309dc9988ab2f33d8e5f9743e7b90641f042c91f15c0cfc17836544(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de24c870bbdf8e92fc9c1101cebfc79b4e63b0d97872bcab0ff2f6100df7c26e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c402b092f0e8eaeb51b08d2023e1350c79fb1060d1c159ca70306a1c2b9386e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__317426c2a040c7c54bdfe79219c8db38d18bcc79d88f1bc457ce6795c19e10b4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb7b16f7b6013f9276fd0ba66ab97fbfb45c6a45ce19065a80ca03ca6764e842(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b98d52a6809433284239abb99b27bcbd5af95896117c95abeeb0082edd6ab7e9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleActionsSuspend]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__596dc9da2fb0c03a7bdb57665433d4ef7ae7accc8770f613d55e60d189010948(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a56bdc368a1990dd3da4708ab5274be5efb7248c07701eb40acfe795447890e5(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ece9ec672bbd16baa8f922d887fda855a42f5ebabc42339a5c752dab1259e2c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleActionsSuspend]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4869ecfe45325ad4f5dd00be0cba315ac019612adfdaa47eb6402994eee897ad(
    *,
    operator: typing.Optional[builtins.str] = None,
    subconditions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RulesetRuleConditionsSubconditions, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__898f4c9a04272e0d74b403ac3a9fc629452885fee8a4c68aca22d9bcea1e9de0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__203c5451aa8d4d8d60c783b71e0b6d3790687264234606f839ef42dea00d632f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RulesetRuleConditionsSubconditions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cccaff665febfd35fdccf7b28413a752abc72322ab8e8f04b121f828e0b742bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87df59bf447d1bd0caaa78a89b6010f9d363486b814b3fb52704c16450fcb32c(
    value: typing.Optional[RulesetRuleConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b6e420c00e32be13f5d4de5ad374e0c596c13229109bbc0d5839a3a578d6979(
    *,
    operator: typing.Optional[builtins.str] = None,
    parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RulesetRuleConditionsSubconditionsParameter, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67c5199654d7ae32e7268b7239b2d37ff9ff90950509e81cd98dbd1a23a6523e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5e98a7ec84a27b52a9ba1dabc02b831f4271a63643e23760fa4f48366fcdd5b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0281596ede52659bcc1115c34ab4a658844d2af00e1e2857f872b656719bc11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf0dfdabbec4879174d9a8057bac210b6c00b14c3027ca9266412060b62669c2(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__157eca7307dc25803c7c69abe29273baca1407f4c999d81294d45e06fc08ade0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__819a49f4070c75b28fd1ad710da3a588c3fe865a178dd57f388c831fed3c5649(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleConditionsSubconditions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b940f86674f87b2156b00a7915a68bb36b2894a33f8984995d06c1d66b590db6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0c0509b2564e42f2f650efde02d7a05a8587c24be039c81a24006f095c515d5(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RulesetRuleConditionsSubconditionsParameter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96ef6271c9b321b51f9906b108c9410857553b7aeab3561dabac833f896a95f3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0bd3263e1209f5ce54671275549bb4fdfd65ebf70bcf253d233014e3c30937b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleConditionsSubconditions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f45a9d4e12f85223e1e0454d63d95084b7798607af423bc1e5fe02cfdbd1a102(
    *,
    path: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7edcf0958ad5e7918c70c4e57022be6a497f500d27d369728bdd12c749b4c95(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41a56b88c2de6ceadbf78172be7350f5a0b7d8480c58957b0a308eb0596c42ce(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d03aa05ec929816f660513f8da1804473e03b29aadca3c39f900fb1754043028(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f31b2ab2bec584208b00ae2c79b21b145ae01d795247885bdf94ad24c475aa2f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c055e0c52392e0882c5c5e3c1dc2c990322d0c9834dd5aa9574ba7613fdbc9e5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f538067f44ef96d9d8f68ee1698dcd02e9f9755602a7c9caf28bdea8489eba7f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleConditionsSubconditionsParameter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23890ccf5c59d8b43d5ea8ab0b5496d77e169652ba141334229f6967178cb122(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e288df82c685bec17b65ab8260b21252e9b4ce7c721164d0b2e23fb69561502a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__149c0be45c867d8ce2709cff2f7c51cd653630f041d4442e4824ed1f30c2d1d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1f74442e8b4aeb96938898e568f536536654ae0b335d9d7f69ebbbb89de68cd(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleConditionsSubconditionsParameter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f71658c558f17455338e28d51240cc8760ae918b3ed39480df2bfe6bd7f7e22(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ruleset: builtins.str,
    actions: typing.Optional[typing.Union[RulesetRuleActions, typing.Dict[builtins.str, typing.Any]]] = None,
    catch_all: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    conditions: typing.Optional[typing.Union[RulesetRuleConditions, typing.Dict[builtins.str, typing.Any]]] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    position: typing.Optional[jsii.Number] = None,
    time_frame: typing.Optional[typing.Union[RulesetRuleTimeFrame, typing.Dict[builtins.str, typing.Any]]] = None,
    variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RulesetRuleVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1fe321ed962ee55d9955b85c8100708accbcd1b0c2d0918d42e9c44ced324e0(
    *,
    active_between: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RulesetRuleTimeFrameActiveBetween, typing.Dict[builtins.str, typing.Any]]]]] = None,
    scheduled_weekly: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RulesetRuleTimeFrameScheduledWeekly, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5973c60020f0d857bccd20ef33e296eb367457e93bd071793f2c206894ed755b(
    *,
    end_time: typing.Optional[jsii.Number] = None,
    start_time: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee88f342673ceb088899f8542af2a39145e172dfec9ab2b8ed2e0ed7beae5d11(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bad0e891d51bad2487b57113c0e00c1a38a2e55fcbd05591f0a735b8a51ea58e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4a96c210e0499fd767eb9fdd24a9b7aac6a7fe7e17a5341dca2f1e7d7a4f315(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d53535cc2a294e4bd2cdda8983fceafb39d982289d5946121ced33ca3786fae(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c80b45aca71809b92f295a33ea4c319b52d128580bb71191e76529b9c8526268(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf08fe6f0501f8922c84f587c82338bb93c16283084e3477535d9ceb27bfabac(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleTimeFrameActiveBetween]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb383b76f75571b86c01dc81985d3b6610015dc90a772cbb2417d719dc765996(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__092186fd08b610f2a7727f95bef160a442cd242d5ee94805a3f23f2be6bbf379(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51d43c46e17a512b1e0f4ba3b87f5707061488455d6deda697b1b8cee0e53d8e(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ff05f1232b9ac2079a393e0bf14a3adcbc54e9b45844d978f1921db63af91a7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleTimeFrameActiveBetween]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d4ce43a9f713dde9f0a9bbc36b5e2167d460a2e2aecdcedcdb727013aa94687(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cf23410949087cf7bf2964f22f133ec19818789ad8833f8e02c53fc2564d2eb(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RulesetRuleTimeFrameActiveBetween, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ef04553c5de03a256944849b72cf7faf69fc2fdbeaa288632a32a06924962dd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RulesetRuleTimeFrameScheduledWeekly, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef86b1729ddac8fd62c96e3b51a1bb3dce133b7f99d2b035f68c5e908cd7867f(
    value: typing.Optional[RulesetRuleTimeFrame],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a395229417c5ee7d4d80750873d2a4205a33b3c652b40f3639cc183838c9825f(
    *,
    duration: typing.Optional[jsii.Number] = None,
    start_time: typing.Optional[jsii.Number] = None,
    timezone: typing.Optional[builtins.str] = None,
    weekdays: typing.Optional[typing.Sequence[jsii.Number]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfa07da7fee66a3b24703426e0bbb57f7fa59c0c9b5560f564cffb595d105f3a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fa3a75c3947a064c94a55e95b979e7be9e6ed953c094538d0c1004ef690b1f7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90ee9472e6c9254124b436495a377258840df890a7c0495a1d8cf08d5ea9ce33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__538afb8aabf925cca11fa2605cb30ee9b4ff156f358f13a7d49ce0ed728807c0(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d08f2b21787bb397916dbf6ba27d6fb857ca5d06aac4157c2be531ee5d42d723(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__233ec5fa0b65c44fc2d2dd5fcd312bcf873474497f8944d9600ba0dc65476ced(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleTimeFrameScheduledWeekly]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09d08615421a2049246f1ba911566ead2f3715bb714c269feaa7605ba8fbe45c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c6ff48ef60751cc56f9ef44bc24cb7522f11681a916bb7e6520a78937535cdb(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b888b7fa6d210b86420038eb5f41720fcd28c4991b2ba936ff66a4606d001411(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__737a6bce72ce8d30ab111ca3d0e9d4ce78dbb2cb69423e17f8e750b3f3d3ee9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__573208598147a55a10dcba757e3e6b92d2fa45243d8e8de91de6978068338993(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31a523cef77252ed1728ad9087c2ba3e219b2a3d7eb4b317966c449faea70a61(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleTimeFrameScheduledWeekly]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d21a61c9c24eeeb889074e736821382f924272c7c41539cbcfc91a81566c44a5(
    *,
    name: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RulesetRuleVariableParameters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__851d40087afbc325009d9f63fe6aa6202e16543f5dc4be25e756771a29966350(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9929f62963cfc31ef7095c19fd9185b7193370af469826bb5c1b7e2002f2a135(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__452ae80d83a79120fa84a3a4a6651729f84597bbfb0f8a3bb561c29fe5c72466(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d30b48c81d83c73d3cc807bfee57124feccc8c95e8a8c7c4519bad680bc525d5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb12c1c81281b60e337727a5eea088ff14b2babed1bc95076c9124735a8387f3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44ba01365d2fa11b909559570ada421d0e99a90146a5365a02037284294cdb52(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleVariable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50a503784461fc5300cd55276a2b35d1b2db15f46e3df3ad4ac3199a237c9d55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c15b4613f565faadb2e1d33a7c63aeaaae050b9c5518d135739bbfbc252df342(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[RulesetRuleVariableParameters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75285ce8d8c73acfebc8f30046b592e2c7a2f05343363dce93a64be3687ef73a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2a689a87b58957a5d7825ed4331a343067ae7410b523d654b3d28946aeba4a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb2360cbf544aae38f09a1c85460ad12b975ed2845a95df545e42c331989f54c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleVariable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a01a31d8a5e77e304f063c99df56b62d002b55bb50f63811f8fd72716ff23f0(
    *,
    path: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf844c7ee2fe0d89d5ba8f358a4c8afcb3b2b317d7cbb1dc28fffa0568ab5f5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__046d2a5d851959a88519e86167228a6faf0b0c04d62ce62ce8aa27adc5e22823(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb21ecb06d9494d01ffc5330a498d9d45eb8c7d9e8fbd6ce71496ac5c910241f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c92e0a14d9d0f0d9d3ebd875ce92564ad472563d8a83f690e1e18a8a455b84f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__965f253ce4cefe6c98a13982340f5383bec6a830026e1dc65e00dfa6105c87df(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6c3bc5d04c12af36c07fb5f488b539ae1d19960f3359a20185b0f45cab98557(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[RulesetRuleVariableParameters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a66e16f5f9ef255d21f3704f4234e033c7fe4bd2375fe7e8be0eec1926ff5a52(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__222daaef9773332228dc859b0f1926724f5a24993ebba38ff115d318294c12c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5cba7170efbe4b15c31a041e49448d7bb2c9877b3076af22348143c7aff00eea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69788aee433137427887c96328d5824318073bccb5c921107ee2117a4cb8e2ab(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, RulesetRuleVariableParameters]],
) -> None:
    """Type checking stubs"""
    pass
