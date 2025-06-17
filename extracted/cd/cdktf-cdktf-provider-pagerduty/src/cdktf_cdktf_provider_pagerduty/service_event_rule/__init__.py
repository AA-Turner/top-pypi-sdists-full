r'''
# `pagerduty_service_event_rule`

Refer to the Terraform Registry for docs: [`pagerduty_service_event_rule`](https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule).
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


class ServiceEventRule(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRule",
):
    '''Represents a {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule pagerduty_service_event_rule}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        service: builtins.str,
        actions: typing.Optional[typing.Union["ServiceEventRuleActions", typing.Dict[builtins.str, typing.Any]]] = None,
        conditions: typing.Optional[typing.Union["ServiceEventRuleConditions", typing.Dict[builtins.str, typing.Any]]] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        position: typing.Optional[jsii.Number] = None,
        time_frame: typing.Optional[typing.Union["ServiceEventRuleTimeFrame", typing.Dict[builtins.str, typing.Any]]] = None,
        variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEventRuleVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule pagerduty_service_event_rule} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param service: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#service ServiceEventRule#service}.
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#actions ServiceEventRule#actions}
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#conditions ServiceEventRule#conditions}
        :param disabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#disabled ServiceEventRule#disabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#id ServiceEventRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param position: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#position ServiceEventRule#position}.
        :param time_frame: time_frame block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#time_frame ServiceEventRule#time_frame}
        :param variable: variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#variable ServiceEventRule#variable}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d7e9e403954e4064ee68b0a179f6f99c30f576ea6718e33e915678d4ceaff78)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ServiceEventRuleConfig(
            service=service,
            actions=actions,
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
        '''Generates CDKTF code for importing a ServiceEventRule resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the ServiceEventRule to import.
        :param import_from_id: The id of the existing ServiceEventRule that should be imported. Refer to the {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the ServiceEventRule to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6434e7758e76db1c1e86e304ac5bf8fbe5f399cfdd1e8463727fce89403edfa8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putActions")
    def put_actions(
        self,
        *,
        annotate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEventRuleActionsAnnotate", typing.Dict[builtins.str, typing.Any]]]]] = None,
        event_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEventRuleActionsEventAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        extractions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEventRuleActionsExtractions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        priority: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEventRuleActionsPriority", typing.Dict[builtins.str, typing.Any]]]]] = None,
        severity: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEventRuleActionsSeverity", typing.Dict[builtins.str, typing.Any]]]]] = None,
        suppress: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEventRuleActionsSuppress", typing.Dict[builtins.str, typing.Any]]]]] = None,
        suspend: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEventRuleActionsSuspend", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param annotate: annotate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#annotate ServiceEventRule#annotate}
        :param event_action: event_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#event_action ServiceEventRule#event_action}
        :param extractions: extractions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#extractions ServiceEventRule#extractions}
        :param priority: priority block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#priority ServiceEventRule#priority}
        :param severity: severity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#severity ServiceEventRule#severity}
        :param suppress: suppress block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#suppress ServiceEventRule#suppress}
        :param suspend: suspend block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#suspend ServiceEventRule#suspend}
        '''
        value = ServiceEventRuleActions(
            annotate=annotate,
            event_action=event_action,
            extractions=extractions,
            priority=priority,
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
        subconditions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEventRuleConditionsSubconditions", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#operator ServiceEventRule#operator}.
        :param subconditions: subconditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#subconditions ServiceEventRule#subconditions}
        '''
        value = ServiceEventRuleConditions(
            operator=operator, subconditions=subconditions
        )

        return typing.cast(None, jsii.invoke(self, "putConditions", [value]))

    @jsii.member(jsii_name="putTimeFrame")
    def put_time_frame(
        self,
        *,
        active_between: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEventRuleTimeFrameActiveBetween", typing.Dict[builtins.str, typing.Any]]]]] = None,
        scheduled_weekly: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEventRuleTimeFrameScheduledWeekly", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param active_between: active_between block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#active_between ServiceEventRule#active_between}
        :param scheduled_weekly: scheduled_weekly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#scheduled_weekly ServiceEventRule#scheduled_weekly}
        '''
        value = ServiceEventRuleTimeFrame(
            active_between=active_between, scheduled_weekly=scheduled_weekly
        )

        return typing.cast(None, jsii.invoke(self, "putTimeFrame", [value]))

    @jsii.member(jsii_name="putVariable")
    def put_variable(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEventRuleVariable", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8b342d5bc1813a452e566ecb01b1aec27c1eabe1bf7f1eafb1912f91ed5d689)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVariable", [value]))

    @jsii.member(jsii_name="resetActions")
    def reset_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetActions", []))

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
    def actions(self) -> "ServiceEventRuleActionsOutputReference":
        return typing.cast("ServiceEventRuleActionsOutputReference", jsii.get(self, "actions"))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> "ServiceEventRuleConditionsOutputReference":
        return typing.cast("ServiceEventRuleConditionsOutputReference", jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="timeFrame")
    def time_frame(self) -> "ServiceEventRuleTimeFrameOutputReference":
        return typing.cast("ServiceEventRuleTimeFrameOutputReference", jsii.get(self, "timeFrame"))

    @builtins.property
    @jsii.member(jsii_name="variable")
    def variable(self) -> "ServiceEventRuleVariableList":
        return typing.cast("ServiceEventRuleVariableList", jsii.get(self, "variable"))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(self) -> typing.Optional["ServiceEventRuleActions"]:
        return typing.cast(typing.Optional["ServiceEventRuleActions"], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionsInput")
    def conditions_input(self) -> typing.Optional["ServiceEventRuleConditions"]:
        return typing.cast(typing.Optional["ServiceEventRuleConditions"], jsii.get(self, "conditionsInput"))

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
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="timeFrameInput")
    def time_frame_input(self) -> typing.Optional["ServiceEventRuleTimeFrame"]:
        return typing.cast(typing.Optional["ServiceEventRuleTimeFrame"], jsii.get(self, "timeFrameInput"))

    @builtins.property
    @jsii.member(jsii_name="variableInput")
    def variable_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleVariable"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleVariable"]]], jsii.get(self, "variableInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__9a78f0ebd28c129c5a60d1b51972545b7932cf3e2f5098acc212d0fe6825ba12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5afbf6f3d9965c1c9e12f1f1194a37ffc366883cc726f17e9d397864d38a5b77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="position")
    def position(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "position"))

    @position.setter
    def position(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05a90988db1880b52a04fa27c0b31771838fa54d44f2a2df746b27ae803f7351)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "position", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02dba3703d21b198815dffff3c6dd610e06873cd531bbcdefaec32f0f4dd5f10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleActions",
    jsii_struct_bases=[],
    name_mapping={
        "annotate": "annotate",
        "event_action": "eventAction",
        "extractions": "extractions",
        "priority": "priority",
        "severity": "severity",
        "suppress": "suppress",
        "suspend": "suspend",
    },
)
class ServiceEventRuleActions:
    def __init__(
        self,
        *,
        annotate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEventRuleActionsAnnotate", typing.Dict[builtins.str, typing.Any]]]]] = None,
        event_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEventRuleActionsEventAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        extractions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEventRuleActionsExtractions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        priority: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEventRuleActionsPriority", typing.Dict[builtins.str, typing.Any]]]]] = None,
        severity: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEventRuleActionsSeverity", typing.Dict[builtins.str, typing.Any]]]]] = None,
        suppress: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEventRuleActionsSuppress", typing.Dict[builtins.str, typing.Any]]]]] = None,
        suspend: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEventRuleActionsSuspend", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param annotate: annotate block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#annotate ServiceEventRule#annotate}
        :param event_action: event_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#event_action ServiceEventRule#event_action}
        :param extractions: extractions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#extractions ServiceEventRule#extractions}
        :param priority: priority block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#priority ServiceEventRule#priority}
        :param severity: severity block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#severity ServiceEventRule#severity}
        :param suppress: suppress block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#suppress ServiceEventRule#suppress}
        :param suspend: suspend block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#suspend ServiceEventRule#suspend}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__281623fa6ba3f719ac3a6af25d50712920077c932b8b5255a7b655b15ec6fd90)
            check_type(argname="argument annotate", value=annotate, expected_type=type_hints["annotate"])
            check_type(argname="argument event_action", value=event_action, expected_type=type_hints["event_action"])
            check_type(argname="argument extractions", value=extractions, expected_type=type_hints["extractions"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
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
        if severity is not None:
            self._values["severity"] = severity
        if suppress is not None:
            self._values["suppress"] = suppress
        if suspend is not None:
            self._values["suspend"] = suspend

    @builtins.property
    def annotate(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleActionsAnnotate"]]]:
        '''annotate block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#annotate ServiceEventRule#annotate}
        '''
        result = self._values.get("annotate")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleActionsAnnotate"]]], result)

    @builtins.property
    def event_action(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleActionsEventAction"]]]:
        '''event_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#event_action ServiceEventRule#event_action}
        '''
        result = self._values.get("event_action")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleActionsEventAction"]]], result)

    @builtins.property
    def extractions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleActionsExtractions"]]]:
        '''extractions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#extractions ServiceEventRule#extractions}
        '''
        result = self._values.get("extractions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleActionsExtractions"]]], result)

    @builtins.property
    def priority(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleActionsPriority"]]]:
        '''priority block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#priority ServiceEventRule#priority}
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleActionsPriority"]]], result)

    @builtins.property
    def severity(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleActionsSeverity"]]]:
        '''severity block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#severity ServiceEventRule#severity}
        '''
        result = self._values.get("severity")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleActionsSeverity"]]], result)

    @builtins.property
    def suppress(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleActionsSuppress"]]]:
        '''suppress block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#suppress ServiceEventRule#suppress}
        '''
        result = self._values.get("suppress")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleActionsSuppress"]]], result)

    @builtins.property
    def suspend(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleActionsSuspend"]]]:
        '''suspend block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#suspend ServiceEventRule#suspend}
        '''
        result = self._values.get("suspend")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleActionsSuspend"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceEventRuleActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleActionsAnnotate",
    jsii_struct_bases=[],
    name_mapping={"value": "value"},
)
class ServiceEventRuleActionsAnnotate:
    def __init__(self, *, value: typing.Optional[builtins.str] = None) -> None:
        '''
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#value ServiceEventRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5ebd90e819af37724378e5fb0f2ece1ecd9cb953b056c77c22df52caf69be2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#value ServiceEventRule#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceEventRuleActionsAnnotate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceEventRuleActionsAnnotateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleActionsAnnotateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6289e7717c16893ea9f85591af7c72fc3e17fb071084a752100a301ef6903c4f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceEventRuleActionsAnnotateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c58fe28ae6a8f6c934496a5b2fe5a52ce7a4cace970ae591114d554d8546ae93)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceEventRuleActionsAnnotateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dee63f22b669b621a44f19432b5670c2a5460f8731e67462f6b575d3a1b0187d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c48048673bfc5a4413051325defb2ec7666bf333a72abb703528c9c02c6077b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a85917127a94d00e160e3f8a14e92ee3ab2e37ec789154cf635a382a0a5a0378)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleActionsAnnotate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleActionsAnnotate]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleActionsAnnotate]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db179be9e84eca6066fbdcd98e60ed44bd12ff449b6f096d55c207335b9136a1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceEventRuleActionsAnnotateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleActionsAnnotateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4c3ede6162e5228c07d8643f04129a368f9a4e720a5cf6c62011deb8fdf93a62)
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
            type_hints = typing.get_type_hints(_typecheckingstub__81d471e98962d61a96cbcda22f24a21982a6f05ff3bafe8d8270c4b4d6b8452a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleActionsAnnotate]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleActionsAnnotate]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleActionsAnnotate]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c94639ffee87c756ef45ba9c55f056c2e09a15847f22cf76fee699462c2fdf58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleActionsEventAction",
    jsii_struct_bases=[],
    name_mapping={"value": "value"},
)
class ServiceEventRuleActionsEventAction:
    def __init__(self, *, value: typing.Optional[builtins.str] = None) -> None:
        '''
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#value ServiceEventRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1caf1811775de9ea298bc5eabb8be06ff2ee65ab9cf427e4dee520c82319d1f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#value ServiceEventRule#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceEventRuleActionsEventAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceEventRuleActionsEventActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleActionsEventActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__297aa659e6bbe355ba2369bceb866a7e596cb4df31b014b55be71f1adc688d09)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceEventRuleActionsEventActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__301dffa220b7ee0d3c67b834b3aa3997bc1336287854ca502c88fb9a77b662e2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceEventRuleActionsEventActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99bb9a14c0b8c1f429482c87814a13723ce10dc61b3b8cd9b1cd94f1ef739ca5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__da8b064ca5d0fdc3c0869473301d3f7896e2abecc3c72649340100d4589b47f7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3728d551357c60aefb9b8cedbdfaf15787a5a5eb3722b67c914476148a1bdd43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleActionsEventAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleActionsEventAction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleActionsEventAction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd35ae6f7ac53184d9b9b7b2a9a832c3966485323651e8ac4a1e464ccb391fd7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceEventRuleActionsEventActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleActionsEventActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a3dbef05b3969500f5ed98361d02922ede1c509a1676a67c37f06d39286fdb3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cba8ce46fe157e7ef50a31123d31623fadeab954af056338207317301e254573)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleActionsEventAction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleActionsEventAction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleActionsEventAction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e69777de4b406f9931b990b99c0c5216134f117049e7b87381ca592fc5c25d64)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleActionsExtractions",
    jsii_struct_bases=[],
    name_mapping={
        "regex": "regex",
        "source": "source",
        "target": "target",
        "template": "template",
    },
)
class ServiceEventRuleActionsExtractions:
    def __init__(
        self,
        *,
        regex: typing.Optional[builtins.str] = None,
        source: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
        template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#regex ServiceEventRule#regex}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#source ServiceEventRule#source}.
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#target ServiceEventRule#target}.
        :param template: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#template ServiceEventRule#template}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2f55c66c34aec2195af8711d7207e8db817592fc396c6a0ac665427a33a3795)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#regex ServiceEventRule#regex}.'''
        result = self._values.get("regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#source ServiceEventRule#source}.'''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#target ServiceEventRule#target}.'''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#template ServiceEventRule#template}.'''
        result = self._values.get("template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceEventRuleActionsExtractions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceEventRuleActionsExtractionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleActionsExtractionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__36ba9d1f58fe6513048ce4a2ce5647fc277ae6534ca2dfdbe1ba887d589acc6a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceEventRuleActionsExtractionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfd509b1befd76ac30b7fb04e4a57236a99fc92b42d0545bc04f26072b18d169)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceEventRuleActionsExtractionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5dcccec6745486638b2e9cf24e037e791c081342e7b30cac9656f2d1d96c97f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd524d4728423e8c529813a4b0025edc1a77195cbba58ec9e201d3dc69286f48)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8563c69ef358110ec54491f935fc57966183b6e4dbb8e52452f38c41b50a5242)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleActionsExtractions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleActionsExtractions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleActionsExtractions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3961a784419b0234d001f04bdc0c95b764040fbca31873bca2e4fbf3d86b2a02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceEventRuleActionsExtractionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleActionsExtractionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__13c8a499fe908a6bfdd842fef4498e5d7b146155a5a835b145547aab080e3075)
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
            type_hints = typing.get_type_hints(_typecheckingstub__654cd9c1f2ae3c9f2e501549dd17a1de35ae6686be18285705d0c1fd3ceda683)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ff1f99d789e25bc1ebc1efa846bbdbd323f949d17edbcac59f8923366be999f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a1ce51377655f9073175c16b8529b8e68d7b44d48ff0c4a59ea5840da05ddd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="template")
    def template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "template"))

    @template.setter
    def template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d77f14fc0e20f311722d332c96c4a831cf3f06829ac96424e1a967f2d1148935)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "template", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleActionsExtractions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleActionsExtractions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleActionsExtractions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8adf4e28eda3ce25f282467f0a4bdb561648d8ccd9604715a353f03bfa4193d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceEventRuleActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa4a0f0075c0b9f1c0ba33f6429b44c955a813bd3bdc9e4ecb66ce791296e859)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAnnotate")
    def put_annotate(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEventRuleActionsAnnotate, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51cf3cdf57ea78f375f5fe079b0307b2d4e7533a398dcc3f09b3175de83d9c0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAnnotate", [value]))

    @jsii.member(jsii_name="putEventAction")
    def put_event_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEventRuleActionsEventAction, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__788dda5a6ca82038dfa6e092c504570ac4319b4bc61680b6de291722efeb912e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEventAction", [value]))

    @jsii.member(jsii_name="putExtractions")
    def put_extractions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEventRuleActionsExtractions, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1388ef7ddfb4795d51f85e32751007fb780ade39e2a9efdd9c0f50fb2f1c1603)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExtractions", [value]))

    @jsii.member(jsii_name="putPriority")
    def put_priority(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEventRuleActionsPriority", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e31d73e9c421e375e71447b7a9b8a6429f4d07dcb98718b208b8fc707b356547)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPriority", [value]))

    @jsii.member(jsii_name="putSeverity")
    def put_severity(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEventRuleActionsSeverity", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1f248f6a169408cb0fbf71ef426aff5e3e49811f54ac94e635c5429806dc564)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSeverity", [value]))

    @jsii.member(jsii_name="putSuppress")
    def put_suppress(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEventRuleActionsSuppress", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a508b0c80635946102c5dd14b1848329781ed28c06f5f83b9aaa7f92f59fc5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSuppress", [value]))

    @jsii.member(jsii_name="putSuspend")
    def put_suspend(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEventRuleActionsSuspend", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e67e66e9eed8a7f24d68c8150303d0d8a3528a0c9e105f3cd9f47a694c8e62c)
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
    def annotate(self) -> ServiceEventRuleActionsAnnotateList:
        return typing.cast(ServiceEventRuleActionsAnnotateList, jsii.get(self, "annotate"))

    @builtins.property
    @jsii.member(jsii_name="eventAction")
    def event_action(self) -> ServiceEventRuleActionsEventActionList:
        return typing.cast(ServiceEventRuleActionsEventActionList, jsii.get(self, "eventAction"))

    @builtins.property
    @jsii.member(jsii_name="extractions")
    def extractions(self) -> ServiceEventRuleActionsExtractionsList:
        return typing.cast(ServiceEventRuleActionsExtractionsList, jsii.get(self, "extractions"))

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> "ServiceEventRuleActionsPriorityList":
        return typing.cast("ServiceEventRuleActionsPriorityList", jsii.get(self, "priority"))

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(self) -> "ServiceEventRuleActionsSeverityList":
        return typing.cast("ServiceEventRuleActionsSeverityList", jsii.get(self, "severity"))

    @builtins.property
    @jsii.member(jsii_name="suppress")
    def suppress(self) -> "ServiceEventRuleActionsSuppressList":
        return typing.cast("ServiceEventRuleActionsSuppressList", jsii.get(self, "suppress"))

    @builtins.property
    @jsii.member(jsii_name="suspend")
    def suspend(self) -> "ServiceEventRuleActionsSuspendList":
        return typing.cast("ServiceEventRuleActionsSuspendList", jsii.get(self, "suspend"))

    @builtins.property
    @jsii.member(jsii_name="annotateInput")
    def annotate_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleActionsAnnotate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleActionsAnnotate]]], jsii.get(self, "annotateInput"))

    @builtins.property
    @jsii.member(jsii_name="eventActionInput")
    def event_action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleActionsEventAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleActionsEventAction]]], jsii.get(self, "eventActionInput"))

    @builtins.property
    @jsii.member(jsii_name="extractionsInput")
    def extractions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleActionsExtractions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleActionsExtractions]]], jsii.get(self, "extractionsInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleActionsPriority"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleActionsPriority"]]], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="severityInput")
    def severity_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleActionsSeverity"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleActionsSeverity"]]], jsii.get(self, "severityInput"))

    @builtins.property
    @jsii.member(jsii_name="suppressInput")
    def suppress_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleActionsSuppress"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleActionsSuppress"]]], jsii.get(self, "suppressInput"))

    @builtins.property
    @jsii.member(jsii_name="suspendInput")
    def suspend_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleActionsSuspend"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleActionsSuspend"]]], jsii.get(self, "suspendInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceEventRuleActions]:
        return typing.cast(typing.Optional[ServiceEventRuleActions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceEventRuleActions]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aeff65f0feea3c81d006a74bdafd650f019931805f551ac73e9cc7d53875c49)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleActionsPriority",
    jsii_struct_bases=[],
    name_mapping={"value": "value"},
)
class ServiceEventRuleActionsPriority:
    def __init__(self, *, value: typing.Optional[builtins.str] = None) -> None:
        '''
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#value ServiceEventRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4409ba60c4f1a916eff755a6f58ed8df73aacf94b7454b3cea68f88a8a20ab87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#value ServiceEventRule#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceEventRuleActionsPriority(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceEventRuleActionsPriorityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleActionsPriorityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e544373438ca17afd1f716221fd9c4b8088ff733512c4e2c739d1bc85ab81f36)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceEventRuleActionsPriorityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0de55bdcc45099b1b993e5b0b448e5bb9fbe4cc3e14e4456ff353552d6565faf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceEventRuleActionsPriorityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de7d0dc967e5c7f392031c75eed2a24ca88428d9f8b0b2a39a6a8318d95eacd0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__88a13bff9e508c2d87a8c9b60103148428d14515c8d975150e2e408075cb3173)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6386c3d8c89868944505be96836f1ea946286445b4a72ebfffaa0d454d57450b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleActionsPriority]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleActionsPriority]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleActionsPriority]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__814efd3b8469a9e9e0a1c810c4056f6c371e34446edb6b796d120eefd9ff5098)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceEventRuleActionsPriorityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleActionsPriorityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ceca2df368442ce5c4a94b417f414666f89322f98aa18b2ad94dfc384f0333d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f78e391b5e83b6e5d3546fe6f77e8d8ffa92e945acb4ddf1d1433b30a948a8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleActionsPriority]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleActionsPriority]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleActionsPriority]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f376c2d240864444bd370329aed843779133febb231d4dc3a5002ec03b81a14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleActionsSeverity",
    jsii_struct_bases=[],
    name_mapping={"value": "value"},
)
class ServiceEventRuleActionsSeverity:
    def __init__(self, *, value: typing.Optional[builtins.str] = None) -> None:
        '''
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#value ServiceEventRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05c3a809cec8cec2ea060d4cbd377ea547b313e3e7b612ff2e7c97f8296f1721)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#value ServiceEventRule#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceEventRuleActionsSeverity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceEventRuleActionsSeverityList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleActionsSeverityList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac5176939af438f2e030ea856105fb2f7d3ca7e871b6f09ffd1bd72dc5a95647)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceEventRuleActionsSeverityOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79ad64063d5c2a11455518a4be94ec2a5604caaa7854e998a0963d17ce3e2f0a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceEventRuleActionsSeverityOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f48226a129b6243414f256c2c1fe6fbcfd71ca8a24af8dab045aa5049d5a00b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d39026a5b8fa532a2403876d072390935450d1b06d4e46465c47e5c039995c9c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9074dfc5a113a4ac35997f5eed8631bd4bc52cfe60c1e6e289aea10365c2fb9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleActionsSeverity]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleActionsSeverity]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleActionsSeverity]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b007f2c127683a7d117e8c085a395a662cdef3ca993fde10991bbf90264bc48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceEventRuleActionsSeverityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleActionsSeverityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ac920882f32b191090fcf7b3c6fb1da191b5ac4358479b2f627865094c553505)
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
            type_hints = typing.get_type_hints(_typecheckingstub__548c7cb592c8fd66578d0f09ab9b97728a9fdba9176488d9d09bd7f9bcbe7586)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleActionsSeverity]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleActionsSeverity]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleActionsSeverity]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__459eb4bb9f5aed620a1ed757feda6c7c6136d170b825386d22059b638b2313de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleActionsSuppress",
    jsii_struct_bases=[],
    name_mapping={
        "threshold_time_amount": "thresholdTimeAmount",
        "threshold_time_unit": "thresholdTimeUnit",
        "threshold_value": "thresholdValue",
        "value": "value",
    },
)
class ServiceEventRuleActionsSuppress:
    def __init__(
        self,
        *,
        threshold_time_amount: typing.Optional[jsii.Number] = None,
        threshold_time_unit: typing.Optional[builtins.str] = None,
        threshold_value: typing.Optional[jsii.Number] = None,
        value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param threshold_time_amount: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#threshold_time_amount ServiceEventRule#threshold_time_amount}.
        :param threshold_time_unit: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#threshold_time_unit ServiceEventRule#threshold_time_unit}.
        :param threshold_value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#threshold_value ServiceEventRule#threshold_value}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#value ServiceEventRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f389918a146ebd9d73a1f6bc697b9a893330f76f164dfc9a4a357bf355ef18d5)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#threshold_time_amount ServiceEventRule#threshold_time_amount}.'''
        result = self._values.get("threshold_time_amount")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def threshold_time_unit(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#threshold_time_unit ServiceEventRule#threshold_time_unit}.'''
        result = self._values.get("threshold_time_unit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def threshold_value(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#threshold_value ServiceEventRule#threshold_value}.'''
        result = self._values.get("threshold_value")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def value(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#value ServiceEventRule#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceEventRuleActionsSuppress(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceEventRuleActionsSuppressList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleActionsSuppressList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5f536ef6faf8d8a6f2aae5226cd763991519dc78bc0e7271f30f614d7055149)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceEventRuleActionsSuppressOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beb53e85719dc9226c60a43ec3fb05bb43a24c03cf2563befa76bde575506931)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceEventRuleActionsSuppressOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bb6a6598740f9fe4acd0fca121e93c23732de431ec5d5e72566002b8e52b752)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f92e84692f2afd4aae7ed5e77db2e8819275eba9cfb785190a4894142570efa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd0b7842d70ce19966a2f042881a93b38c1dfa010ce9b208e0b2ce703c239b8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleActionsSuppress]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleActionsSuppress]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleActionsSuppress]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdc9f6b5d206f97865457c989b864a095eff71213fdc29b7ad8df82cdfcd021a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceEventRuleActionsSuppressOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleActionsSuppressOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b76460735c2161d6e069517a1a83f2a1b7d67e29f53d0fe00f86b7af29d9d732)
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
            type_hints = typing.get_type_hints(_typecheckingstub__18a2922a0758b5739724b6fd0f2490d962b11bf0bd8b03dae90d28f5c1fa469b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thresholdTimeAmount", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="thresholdTimeUnit")
    def threshold_time_unit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "thresholdTimeUnit"))

    @threshold_time_unit.setter
    def threshold_time_unit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd7d9573d05a81d95b152828c1a20917ed227ecb97605d8cd2c87274630227cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thresholdTimeUnit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="thresholdValue")
    def threshold_value(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "thresholdValue"))

    @threshold_value.setter
    def threshold_value(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fc82b0ef7be1f03cb537238f08619c8960798296b6dd5a5e49afe4979986786)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdedc7483c63e5d18b6e7d7cee932e846a90160334ce54aacfe8b68dbf14f6d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleActionsSuppress]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleActionsSuppress]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleActionsSuppress]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb9e8dd88563105aa2da629e9a08ff60fd90319e07354d21e40f6d7488f58718)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleActionsSuspend",
    jsii_struct_bases=[],
    name_mapping={"value": "value"},
)
class ServiceEventRuleActionsSuspend:
    def __init__(self, *, value: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#value ServiceEventRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7ba3a51bed4b805ab99c85c8ac39d27220030977225ae4ca449fc48f1b4e673)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def value(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#value ServiceEventRule#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceEventRuleActionsSuspend(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceEventRuleActionsSuspendList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleActionsSuspendList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__43b7c92e6ff0c89e69b9296fd5df51acea6361a4b8a2672d5d7b3a296a631a04)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceEventRuleActionsSuspendOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96864e97449fd104186a99577b74a85680a84883ecf17a7429d1b7b1ababc52d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceEventRuleActionsSuspendOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7be0a6ea185ffef40ef6d792818ad48451fd4a7eeb09194cc735414f4c009b5d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b9ac4cd8de2806d08704137ede57b26644e46b9a211dd1edfbf9295487035719)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eaa60f87268f7f4da52af71dd0886077328863dfc0c3654883f522ef32e8c561)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleActionsSuspend]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleActionsSuspend]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleActionsSuspend]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6199e8355c347b6ceb38e68c2e2eaaea2411810dadbb9dc6356148183bed771)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceEventRuleActionsSuspendOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleActionsSuspendOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__73c394080e04d2f8d9793e8577fd9ea1be4da959d283c0340720f9b657892325)
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
            type_hints = typing.get_type_hints(_typecheckingstub__897157bc5bb4f20b3049e4c7a9775992ef2cf265e5d7dcb841fd433a7de57204)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleActionsSuspend]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleActionsSuspend]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleActionsSuspend]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a58d49d23c91cbbad3ddb52e87302abaf937bf0a80c3dcb5813812bf8b4e61a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleConditions",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "subconditions": "subconditions"},
)
class ServiceEventRuleConditions:
    def __init__(
        self,
        *,
        operator: typing.Optional[builtins.str] = None,
        subconditions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEventRuleConditionsSubconditions", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#operator ServiceEventRule#operator}.
        :param subconditions: subconditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#subconditions ServiceEventRule#subconditions}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fc771c1ff945e8bc3df2c7d59cd91f8f94c7e4487aadfd114ebae9a21adba04)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument subconditions", value=subconditions, expected_type=type_hints["subconditions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if operator is not None:
            self._values["operator"] = operator
        if subconditions is not None:
            self._values["subconditions"] = subconditions

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#operator ServiceEventRule#operator}.'''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subconditions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleConditionsSubconditions"]]]:
        '''subconditions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#subconditions ServiceEventRule#subconditions}
        '''
        result = self._values.get("subconditions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleConditionsSubconditions"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceEventRuleConditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceEventRuleConditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleConditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdf1657a951bb32becfad7837f142ab02a8433ffb6d89792bfc31028173c549d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSubconditions")
    def put_subconditions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEventRuleConditionsSubconditions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3f0fe8e482204b6809f661b7d50e9a6242f44351cf45b2fad802c40b867f75a)
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
    def subconditions(self) -> "ServiceEventRuleConditionsSubconditionsList":
        return typing.cast("ServiceEventRuleConditionsSubconditionsList", jsii.get(self, "subconditions"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="subconditionsInput")
    def subconditions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleConditionsSubconditions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleConditionsSubconditions"]]], jsii.get(self, "subconditionsInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a87bfa74d4de4d0418deeb91337d8dca98ae5179794d05d562bd486b48739f1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceEventRuleConditions]:
        return typing.cast(typing.Optional[ServiceEventRuleConditions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[ServiceEventRuleConditions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3bb3159dd423a64bbcab9f2ed76be7a7bd7a7f26294f8e736859b07e6db0970)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleConditionsSubconditions",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "parameter": "parameter"},
)
class ServiceEventRuleConditionsSubconditions:
    def __init__(
        self,
        *,
        operator: typing.Optional[builtins.str] = None,
        parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEventRuleConditionsSubconditionsParameter", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#operator ServiceEventRule#operator}.
        :param parameter: parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#parameter ServiceEventRule#parameter}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92e32d674371766c27483eb38339be450b2f381fd4c1aab3468ed628575aa3cb)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument parameter", value=parameter, expected_type=type_hints["parameter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if operator is not None:
            self._values["operator"] = operator
        if parameter is not None:
            self._values["parameter"] = parameter

    @builtins.property
    def operator(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#operator ServiceEventRule#operator}.'''
        result = self._values.get("operator")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleConditionsSubconditionsParameter"]]]:
        '''parameter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#parameter ServiceEventRule#parameter}
        '''
        result = self._values.get("parameter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleConditionsSubconditionsParameter"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceEventRuleConditionsSubconditions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceEventRuleConditionsSubconditionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleConditionsSubconditionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__015881765959edfca503bf3e13c4c45ffa95fbe7467c7ffd828334b613c361a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceEventRuleConditionsSubconditionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0b4dbd33e77b83df7c3157b6203de2e860bff6c515b4f57be4c0d501ddef6e9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceEventRuleConditionsSubconditionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b7cf6d639b229fdf2aea78e58d9d162e655a118df8a1b3882c02e4532697ccc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8474d24c9c29713559c3bdc19902785757d2a659cce5f36b5dfa6e447b791f5f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2b1c5facfe0bc10c20f80150847d4e912235b7d25915ce9bf4c9dc1811bd92af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleConditionsSubconditions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleConditionsSubconditions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleConditionsSubconditions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0556bf041a3f297ca080d031c49040efe363cf377ed797e83b8cb189b716ab17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceEventRuleConditionsSubconditionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleConditionsSubconditionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dce9e1c69671d68278047171b823da6600feba7f14b36b0d37c947a43b7cccc9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putParameter")
    def put_parameter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEventRuleConditionsSubconditionsParameter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1108af676fc1610938cb504684c9d098954043a15ecd73b9e9fa3c852c47d518)
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
    def parameter(self) -> "ServiceEventRuleConditionsSubconditionsParameterList":
        return typing.cast("ServiceEventRuleConditionsSubconditionsParameterList", jsii.get(self, "parameter"))

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="parameterInput")
    def parameter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleConditionsSubconditionsParameter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleConditionsSubconditionsParameter"]]], jsii.get(self, "parameterInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64c3659e29752701895b7fb44d3e5d52260c41ae580d68309173922df1b09edf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleConditionsSubconditions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleConditionsSubconditions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleConditionsSubconditions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2a72355ff78b7f1f90a7d290f87afe97006974ecc454ee508745b482136d324)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleConditionsSubconditionsParameter",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "value": "value"},
)
class ServiceEventRuleConditionsSubconditionsParameter:
    def __init__(
        self,
        *,
        path: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#path ServiceEventRule#path}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#value ServiceEventRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79fc2de3f52a6859044927c4337ed777bbd6ebc3bd7ade5900d2f4bced764cbc)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if path is not None:
            self._values["path"] = path
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#path ServiceEventRule#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#value ServiceEventRule#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceEventRuleConditionsSubconditionsParameter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceEventRuleConditionsSubconditionsParameterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleConditionsSubconditionsParameterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a84728a526a4738677d37536b072451ecc69f52a87cdb523af7056083ac581fa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceEventRuleConditionsSubconditionsParameterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd467a28852525e1b3a98dc05f4e137d0712cca8116421e352daef93b45fdf26)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceEventRuleConditionsSubconditionsParameterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b1f6ca2166fd29da4209ea6baa29d15abfc25fc2bdff975d05742219af2efd2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e15a8f10471aba0682e61fb9160fad78b66eb7292a36bfba3caaa7c5b24398f5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4b6ae21ce2e15139bdf0b4271f4157fec87ee82024906bfa9356e0beec8766be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleConditionsSubconditionsParameter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleConditionsSubconditionsParameter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleConditionsSubconditionsParameter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecf3a9cd9300f13eaa0132e0c453a8c65ec57b6bc4c4130dabd2828b071e8020)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceEventRuleConditionsSubconditionsParameterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleConditionsSubconditionsParameterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7a0ef9bb96d326f13d8dc0793dd5ae1f0c2366878c39250d2505caa85c66029e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__95d251604490081a47719a3824009fa37184809b900c9e1667365132e9cd0100)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caa1314b7d481966e17467fe1837a12f809d462d20795160da476e7026c7ec48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleConditionsSubconditionsParameter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleConditionsSubconditionsParameter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleConditionsSubconditionsParameter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6644bee53f851d43933a75ce66acffdb6a87992856ea8df66921c0b7bd4b535b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "service": "service",
        "actions": "actions",
        "conditions": "conditions",
        "disabled": "disabled",
        "id": "id",
        "position": "position",
        "time_frame": "timeFrame",
        "variable": "variable",
    },
)
class ServiceEventRuleConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        service: builtins.str,
        actions: typing.Optional[typing.Union[ServiceEventRuleActions, typing.Dict[builtins.str, typing.Any]]] = None,
        conditions: typing.Optional[typing.Union[ServiceEventRuleConditions, typing.Dict[builtins.str, typing.Any]]] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        position: typing.Optional[jsii.Number] = None,
        time_frame: typing.Optional[typing.Union["ServiceEventRuleTimeFrame", typing.Dict[builtins.str, typing.Any]]] = None,
        variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEventRuleVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param service: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#service ServiceEventRule#service}.
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#actions ServiceEventRule#actions}
        :param conditions: conditions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#conditions ServiceEventRule#conditions}
        :param disabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#disabled ServiceEventRule#disabled}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#id ServiceEventRule#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param position: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#position ServiceEventRule#position}.
        :param time_frame: time_frame block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#time_frame ServiceEventRule#time_frame}
        :param variable: variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#variable ServiceEventRule#variable}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(actions, dict):
            actions = ServiceEventRuleActions(**actions)
        if isinstance(conditions, dict):
            conditions = ServiceEventRuleConditions(**conditions)
        if isinstance(time_frame, dict):
            time_frame = ServiceEventRuleTimeFrame(**time_frame)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32956afa851cd0df6a4cb30c532d23a083042b78f2af62757c083191e42b5be9)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument position", value=position, expected_type=type_hints["position"])
            check_type(argname="argument time_frame", value=time_frame, expected_type=type_hints["time_frame"])
            check_type(argname="argument variable", value=variable, expected_type=type_hints["variable"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service": service,
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
    def service(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#service ServiceEventRule#service}.'''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def actions(self) -> typing.Optional[ServiceEventRuleActions]:
        '''actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#actions ServiceEventRule#actions}
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[ServiceEventRuleActions], result)

    @builtins.property
    def conditions(self) -> typing.Optional[ServiceEventRuleConditions]:
        '''conditions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#conditions ServiceEventRule#conditions}
        '''
        result = self._values.get("conditions")
        return typing.cast(typing.Optional[ServiceEventRuleConditions], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#disabled ServiceEventRule#disabled}.'''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#id ServiceEventRule#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def position(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#position ServiceEventRule#position}.'''
        result = self._values.get("position")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def time_frame(self) -> typing.Optional["ServiceEventRuleTimeFrame"]:
        '''time_frame block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#time_frame ServiceEventRule#time_frame}
        '''
        result = self._values.get("time_frame")
        return typing.cast(typing.Optional["ServiceEventRuleTimeFrame"], result)

    @builtins.property
    def variable(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleVariable"]]]:
        '''variable block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#variable ServiceEventRule#variable}
        '''
        result = self._values.get("variable")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleVariable"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceEventRuleConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleTimeFrame",
    jsii_struct_bases=[],
    name_mapping={
        "active_between": "activeBetween",
        "scheduled_weekly": "scheduledWeekly",
    },
)
class ServiceEventRuleTimeFrame:
    def __init__(
        self,
        *,
        active_between: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEventRuleTimeFrameActiveBetween", typing.Dict[builtins.str, typing.Any]]]]] = None,
        scheduled_weekly: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEventRuleTimeFrameScheduledWeekly", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param active_between: active_between block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#active_between ServiceEventRule#active_between}
        :param scheduled_weekly: scheduled_weekly block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#scheduled_weekly ServiceEventRule#scheduled_weekly}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52354ee370d1e9413c1063dd000e627e6de6caee1944886961e9a6225bcfe1f7)
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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleTimeFrameActiveBetween"]]]:
        '''active_between block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#active_between ServiceEventRule#active_between}
        '''
        result = self._values.get("active_between")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleTimeFrameActiveBetween"]]], result)

    @builtins.property
    def scheduled_weekly(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleTimeFrameScheduledWeekly"]]]:
        '''scheduled_weekly block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#scheduled_weekly ServiceEventRule#scheduled_weekly}
        '''
        result = self._values.get("scheduled_weekly")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleTimeFrameScheduledWeekly"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceEventRuleTimeFrame(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleTimeFrameActiveBetween",
    jsii_struct_bases=[],
    name_mapping={"end_time": "endTime", "start_time": "startTime"},
)
class ServiceEventRuleTimeFrameActiveBetween:
    def __init__(
        self,
        *,
        end_time: typing.Optional[jsii.Number] = None,
        start_time: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param end_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#end_time ServiceEventRule#end_time}.
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#start_time ServiceEventRule#start_time}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4311eba747c1d712b8c8b113d7a6f8b01d121d8fe2d551eb79342c5eb9a0bcad)
            check_type(argname="argument end_time", value=end_time, expected_type=type_hints["end_time"])
            check_type(argname="argument start_time", value=start_time, expected_type=type_hints["start_time"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if end_time is not None:
            self._values["end_time"] = end_time
        if start_time is not None:
            self._values["start_time"] = start_time

    @builtins.property
    def end_time(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#end_time ServiceEventRule#end_time}.'''
        result = self._values.get("end_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def start_time(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#start_time ServiceEventRule#start_time}.'''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceEventRuleTimeFrameActiveBetween(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceEventRuleTimeFrameActiveBetweenList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleTimeFrameActiveBetweenList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e099e2b78d750da51fa6096b80aeb857f23144a74ac2a7572a3ac538ef94998d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceEventRuleTimeFrameActiveBetweenOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7782262e7b8bb08a3a1ef1551d1b2b3f111ca107a7cf727ff2b3ad3361454cc4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceEventRuleTimeFrameActiveBetweenOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e48c19276b50dae823a37c183fb566f042e37b049199f94bbea664e5af90aee4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a292a4aa25422e1a41bd2d97b4885e675645e6b311039db43b74e2006bbeb6e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c65b7e18040d89cd42bcb3d1f9b598e099517984f7eeb317b0e72c649bfafc19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleTimeFrameActiveBetween]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleTimeFrameActiveBetween]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleTimeFrameActiveBetween]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c85143c0c79ebe1f6a4233218bde46021fc8fc53bbae88fb3c35acbc4bcfc77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceEventRuleTimeFrameActiveBetweenOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleTimeFrameActiveBetweenOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__532eee966fc8218f51980087a84c6c5710909771b99f174fd3ad7f8e7c35422d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e4b3848f42160218176e07d81756b8b18f54ee781bf117c465d395384d8b2bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f525b1f22bfed503ea43a470b8fbbefca853c5b84d1d0b576f73259bc4db8a0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleTimeFrameActiveBetween]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleTimeFrameActiveBetween]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleTimeFrameActiveBetween]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69fb52cbb6a0aec4eb27afc777d096da09572da942c960629d54ff666d3c8024)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceEventRuleTimeFrameOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleTimeFrameOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__69a089cb3e8bb5e9227712d94638b45212aee2108cc558b7536fa4e2fed8d8e6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putActiveBetween")
    def put_active_between(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEventRuleTimeFrameActiveBetween, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af3b8b5ee8dd0ccff58645d1ec820a9735117ff73098901d69b66abc4f4d2c3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putActiveBetween", [value]))

    @jsii.member(jsii_name="putScheduledWeekly")
    def put_scheduled_weekly(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEventRuleTimeFrameScheduledWeekly", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45ec944323d8c11bdaddc8253b6b80c9e957056a130e510f5e334da5bc19ce5f)
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
    def active_between(self) -> ServiceEventRuleTimeFrameActiveBetweenList:
        return typing.cast(ServiceEventRuleTimeFrameActiveBetweenList, jsii.get(self, "activeBetween"))

    @builtins.property
    @jsii.member(jsii_name="scheduledWeekly")
    def scheduled_weekly(self) -> "ServiceEventRuleTimeFrameScheduledWeeklyList":
        return typing.cast("ServiceEventRuleTimeFrameScheduledWeeklyList", jsii.get(self, "scheduledWeekly"))

    @builtins.property
    @jsii.member(jsii_name="activeBetweenInput")
    def active_between_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleTimeFrameActiveBetween]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleTimeFrameActiveBetween]]], jsii.get(self, "activeBetweenInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduledWeeklyInput")
    def scheduled_weekly_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleTimeFrameScheduledWeekly"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleTimeFrameScheduledWeekly"]]], jsii.get(self, "scheduledWeeklyInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[ServiceEventRuleTimeFrame]:
        return typing.cast(typing.Optional[ServiceEventRuleTimeFrame], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[ServiceEventRuleTimeFrame]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bf69a3a2e18dddf5720a80625c5bb098e0bc2c01c64cc0bbd14038bc68d892b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleTimeFrameScheduledWeekly",
    jsii_struct_bases=[],
    name_mapping={
        "duration": "duration",
        "start_time": "startTime",
        "timezone": "timezone",
        "weekdays": "weekdays",
    },
)
class ServiceEventRuleTimeFrameScheduledWeekly:
    def __init__(
        self,
        *,
        duration: typing.Optional[jsii.Number] = None,
        start_time: typing.Optional[jsii.Number] = None,
        timezone: typing.Optional[builtins.str] = None,
        weekdays: typing.Optional[typing.Sequence[jsii.Number]] = None,
    ) -> None:
        '''
        :param duration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#duration ServiceEventRule#duration}.
        :param start_time: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#start_time ServiceEventRule#start_time}.
        :param timezone: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#timezone ServiceEventRule#timezone}.
        :param weekdays: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#weekdays ServiceEventRule#weekdays}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e88eb9f4805cabd6b5cfd9d722392054a3af7985b9b8c5a6d8d0f0f27ec6b1b)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#duration ServiceEventRule#duration}.'''
        result = self._values.get("duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def start_time(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#start_time ServiceEventRule#start_time}.'''
        result = self._values.get("start_time")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def timezone(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#timezone ServiceEventRule#timezone}.'''
        result = self._values.get("timezone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def weekdays(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#weekdays ServiceEventRule#weekdays}.'''
        result = self._values.get("weekdays")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceEventRuleTimeFrameScheduledWeekly(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceEventRuleTimeFrameScheduledWeeklyList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleTimeFrameScheduledWeeklyList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ccfabd83e5d623cd009141bd71c473fc2fc74cbab3f2e0f9ab90c851802d5359)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceEventRuleTimeFrameScheduledWeeklyOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e770a9f76d8931e5d5c5f3de344a1f98d7db0c887aab8031f916c9ce0947609a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceEventRuleTimeFrameScheduledWeeklyOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b99084d2139e2d0fa6600f47861104c720f47f4fb0bec2e10008890b4b79ed1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__15bb5b335937c1af2dabd3effad88a385f08f5878b8084d098aef180c63146cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee6b8556d2ffc52ed6c3033de66b996ebadbf3e45f6bd1f401cabc2e70daf9e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleTimeFrameScheduledWeekly]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleTimeFrameScheduledWeekly]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleTimeFrameScheduledWeekly]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85ed5b94990e52b10658926fa41e90012066ab925b0614421c36f61ecc60347b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceEventRuleTimeFrameScheduledWeeklyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleTimeFrameScheduledWeeklyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dde47401d37725f2c6293690f2d809c85d2e2e81ac2a014575480bb6cf22d474)
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
            type_hints = typing.get_type_hints(_typecheckingstub__97265e861a86db449a28c0252e8c68cbb46cf4100dd4db495fcf0776a2826bc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "duration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="startTime")
    def start_time(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "startTime"))

    @start_time.setter
    def start_time(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c68c76b2946e5e9ff872d22f1662303457b657eb427a5d84409c98bcc3b679d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startTime", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="timezone")
    def timezone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "timezone"))

    @timezone.setter
    def timezone(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b8f0c0e2163d4990c038128c671b5c57369ecc2b7b24210b81d4b868c3f27e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "timezone", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="weekdays")
    def weekdays(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "weekdays"))

    @weekdays.setter
    def weekdays(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9293b1ab2bf0116e7be6b2aea4ce0c019194df7f0661732efca024f045c69aca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "weekdays", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleTimeFrameScheduledWeekly]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleTimeFrameScheduledWeekly]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleTimeFrameScheduledWeekly]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3959bbe2a6cdf84fe88abe419e1cdd61ce450743b5eee2f0ffbaec9de577f7ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleVariable",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "parameters": "parameters", "type": "type"},
)
class ServiceEventRuleVariable:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEventRuleVariableParameters", typing.Dict[builtins.str, typing.Any]]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#name ServiceEventRule#name}.
        :param parameters: parameters block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#parameters ServiceEventRule#parameters}
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#type ServiceEventRule#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe2d5ab874b44f036c8ca60bcb461d0f6ea2bd4efd3ba79f34a83419c55cd6dd)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#name ServiceEventRule#name}.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleVariableParameters"]]]:
        '''parameters block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#parameters ServiceEventRule#parameters}
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleVariableParameters"]]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#type ServiceEventRule#type}.'''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceEventRuleVariable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceEventRuleVariableList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleVariableList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__91f9fb029d9e1b77afa796f7771d4f9970b5fda14a923bc0f9e3916f797af95d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "ServiceEventRuleVariableOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1b4a67bdda2106cfc2cde1768a84ef14829a53b922cf707427c19ac154661e9)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceEventRuleVariableOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54ea7eb8aec6d16cf71826c1a91d40b6cd5ce0274926c9ddca1500c8f6e6e960)
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
            type_hints = typing.get_type_hints(_typecheckingstub__81be626d23e4db9187704e0d8ff69cf8a0b096acc000d9260149bf95f71ab121)
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
            type_hints = typing.get_type_hints(_typecheckingstub__301c6b63e277b5e2977a8d68f46b2117ec97dfffcda76c5c61a17827f3ba9d3b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleVariable]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleVariable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a4d413757113c2229c3e0f2993c0550ad606140480345f0c9bd5f12fb5e63e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceEventRuleVariableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleVariableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7597fe96ff06e46b8f143a9a6123921ff048e65ec203618998fc6811bcd646b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putParameters")
    def put_parameters(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServiceEventRuleVariableParameters", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c745418a4459fdacc14b3b9ad25c021a98da5594210302c345f246193b3e279)
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
    def parameters(self) -> "ServiceEventRuleVariableParametersList":
        return typing.cast("ServiceEventRuleVariableParametersList", jsii.get(self, "parameters"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parametersInput")
    def parameters_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleVariableParameters"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServiceEventRuleVariableParameters"]]], jsii.get(self, "parametersInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__4b871a7afce7dccc5fd94b695652feb26f55fa822f51f50f8a275c95fdb175b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96ec52089e88edd0119adeead2832d8ae39b19d277c78f5bab2de95abd15b496)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleVariable]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleVariable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleVariable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8edd1d9dd728839c8000e9ae88e63b7c12f23bb62f6b9d3c2fe5955c6dd18e69)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleVariableParameters",
    jsii_struct_bases=[],
    name_mapping={"path": "path", "value": "value"},
)
class ServiceEventRuleVariableParameters:
    def __init__(
        self,
        *,
        path: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#path ServiceEventRule#path}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#value ServiceEventRule#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a105f82609192c33980a7920dc4639159962e07b5ea248a5a662bd95fda1034b)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if path is not None:
            self._values["path"] = path
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#path ServiceEventRule#path}.'''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/service_event_rule#value ServiceEventRule#value}.'''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServiceEventRuleVariableParameters(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServiceEventRuleVariableParametersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleVariableParametersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b32813b897f0a61878fd4506f3e6801427fd9f6ff0ae938cff4c96b1b66a9e5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServiceEventRuleVariableParametersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9b6db746e91b382b55da14607c934e580d8f76af8dd1f135c105ff6b2793943)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServiceEventRuleVariableParametersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa93c5a86be4ee4cbf0e8f6bea9fe6e99cb27bb433c5370323a29aa7a00ea5e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__19e8befa6fe16c22ad9bdc6d09e38c9fb780fc5508cad45cd5211484d6a76c7b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__82ac1fde40ca3f8f935b880aa85d2a0c630504f3c1e7b0b696dc60be65b264c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleVariableParameters]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleVariableParameters]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleVariableParameters]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf4afecea13c28429c25d7f7a59a6650c82c594d3e6b3e99c6fc026c99698d85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class ServiceEventRuleVariableParametersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.serviceEventRule.ServiceEventRuleVariableParametersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e80704c1793b530e810d225bc1981ed320514896049d80b8dc7f45640d14f98a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db89182f36cea9d0913fa6431c50598ee97ede9502081dfc1bacc6cba670024b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__636a18dd97ee8a0c3e5e3e93ad6c0097a449f9b81320d5edf7de32e5afdf5831)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleVariableParameters]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleVariableParameters]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleVariableParameters]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c158da27b5836728a135b54e05d1a25c5fb478040538d4a62107142d163b02cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "ServiceEventRule",
    "ServiceEventRuleActions",
    "ServiceEventRuleActionsAnnotate",
    "ServiceEventRuleActionsAnnotateList",
    "ServiceEventRuleActionsAnnotateOutputReference",
    "ServiceEventRuleActionsEventAction",
    "ServiceEventRuleActionsEventActionList",
    "ServiceEventRuleActionsEventActionOutputReference",
    "ServiceEventRuleActionsExtractions",
    "ServiceEventRuleActionsExtractionsList",
    "ServiceEventRuleActionsExtractionsOutputReference",
    "ServiceEventRuleActionsOutputReference",
    "ServiceEventRuleActionsPriority",
    "ServiceEventRuleActionsPriorityList",
    "ServiceEventRuleActionsPriorityOutputReference",
    "ServiceEventRuleActionsSeverity",
    "ServiceEventRuleActionsSeverityList",
    "ServiceEventRuleActionsSeverityOutputReference",
    "ServiceEventRuleActionsSuppress",
    "ServiceEventRuleActionsSuppressList",
    "ServiceEventRuleActionsSuppressOutputReference",
    "ServiceEventRuleActionsSuspend",
    "ServiceEventRuleActionsSuspendList",
    "ServiceEventRuleActionsSuspendOutputReference",
    "ServiceEventRuleConditions",
    "ServiceEventRuleConditionsOutputReference",
    "ServiceEventRuleConditionsSubconditions",
    "ServiceEventRuleConditionsSubconditionsList",
    "ServiceEventRuleConditionsSubconditionsOutputReference",
    "ServiceEventRuleConditionsSubconditionsParameter",
    "ServiceEventRuleConditionsSubconditionsParameterList",
    "ServiceEventRuleConditionsSubconditionsParameterOutputReference",
    "ServiceEventRuleConfig",
    "ServiceEventRuleTimeFrame",
    "ServiceEventRuleTimeFrameActiveBetween",
    "ServiceEventRuleTimeFrameActiveBetweenList",
    "ServiceEventRuleTimeFrameActiveBetweenOutputReference",
    "ServiceEventRuleTimeFrameOutputReference",
    "ServiceEventRuleTimeFrameScheduledWeekly",
    "ServiceEventRuleTimeFrameScheduledWeeklyList",
    "ServiceEventRuleTimeFrameScheduledWeeklyOutputReference",
    "ServiceEventRuleVariable",
    "ServiceEventRuleVariableList",
    "ServiceEventRuleVariableOutputReference",
    "ServiceEventRuleVariableParameters",
    "ServiceEventRuleVariableParametersList",
    "ServiceEventRuleVariableParametersOutputReference",
]

publication.publish()

def _typecheckingstub__8d7e9e403954e4064ee68b0a179f6f99c30f576ea6718e33e915678d4ceaff78(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    service: builtins.str,
    actions: typing.Optional[typing.Union[ServiceEventRuleActions, typing.Dict[builtins.str, typing.Any]]] = None,
    conditions: typing.Optional[typing.Union[ServiceEventRuleConditions, typing.Dict[builtins.str, typing.Any]]] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    position: typing.Optional[jsii.Number] = None,
    time_frame: typing.Optional[typing.Union[ServiceEventRuleTimeFrame, typing.Dict[builtins.str, typing.Any]]] = None,
    variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEventRuleVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__6434e7758e76db1c1e86e304ac5bf8fbe5f399cfdd1e8463727fce89403edfa8(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8b342d5bc1813a452e566ecb01b1aec27c1eabe1bf7f1eafb1912f91ed5d689(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEventRuleVariable, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a78f0ebd28c129c5a60d1b51972545b7932cf3e2f5098acc212d0fe6825ba12(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5afbf6f3d9965c1c9e12f1f1194a37ffc366883cc726f17e9d397864d38a5b77(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05a90988db1880b52a04fa27c0b31771838fa54d44f2a2df746b27ae803f7351(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02dba3703d21b198815dffff3c6dd610e06873cd531bbcdefaec32f0f4dd5f10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__281623fa6ba3f719ac3a6af25d50712920077c932b8b5255a7b655b15ec6fd90(
    *,
    annotate: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEventRuleActionsAnnotate, typing.Dict[builtins.str, typing.Any]]]]] = None,
    event_action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEventRuleActionsEventAction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    extractions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEventRuleActionsExtractions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    priority: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEventRuleActionsPriority, typing.Dict[builtins.str, typing.Any]]]]] = None,
    severity: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEventRuleActionsSeverity, typing.Dict[builtins.str, typing.Any]]]]] = None,
    suppress: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEventRuleActionsSuppress, typing.Dict[builtins.str, typing.Any]]]]] = None,
    suspend: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEventRuleActionsSuspend, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5ebd90e819af37724378e5fb0f2ece1ecd9cb953b056c77c22df52caf69be2b(
    *,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6289e7717c16893ea9f85591af7c72fc3e17fb071084a752100a301ef6903c4f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c58fe28ae6a8f6c934496a5b2fe5a52ce7a4cace970ae591114d554d8546ae93(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dee63f22b669b621a44f19432b5670c2a5460f8731e67462f6b575d3a1b0187d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c48048673bfc5a4413051325defb2ec7666bf333a72abb703528c9c02c6077b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a85917127a94d00e160e3f8a14e92ee3ab2e37ec789154cf635a382a0a5a0378(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db179be9e84eca6066fbdcd98e60ed44bd12ff449b6f096d55c207335b9136a1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleActionsAnnotate]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c3ede6162e5228c07d8643f04129a368f9a4e720a5cf6c62011deb8fdf93a62(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81d471e98962d61a96cbcda22f24a21982a6f05ff3bafe8d8270c4b4d6b8452a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c94639ffee87c756ef45ba9c55f056c2e09a15847f22cf76fee699462c2fdf58(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleActionsAnnotate]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1caf1811775de9ea298bc5eabb8be06ff2ee65ab9cf427e4dee520c82319d1f0(
    *,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__297aa659e6bbe355ba2369bceb866a7e596cb4df31b014b55be71f1adc688d09(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__301dffa220b7ee0d3c67b834b3aa3997bc1336287854ca502c88fb9a77b662e2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99bb9a14c0b8c1f429482c87814a13723ce10dc61b3b8cd9b1cd94f1ef739ca5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da8b064ca5d0fdc3c0869473301d3f7896e2abecc3c72649340100d4589b47f7(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3728d551357c60aefb9b8cedbdfaf15787a5a5eb3722b67c914476148a1bdd43(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd35ae6f7ac53184d9b9b7b2a9a832c3966485323651e8ac4a1e464ccb391fd7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleActionsEventAction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a3dbef05b3969500f5ed98361d02922ede1c509a1676a67c37f06d39286fdb3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cba8ce46fe157e7ef50a31123d31623fadeab954af056338207317301e254573(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e69777de4b406f9931b990b99c0c5216134f117049e7b87381ca592fc5c25d64(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleActionsEventAction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2f55c66c34aec2195af8711d7207e8db817592fc396c6a0ac665427a33a3795(
    *,
    regex: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
    target: typing.Optional[builtins.str] = None,
    template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36ba9d1f58fe6513048ce4a2ce5647fc277ae6534ca2dfdbe1ba887d589acc6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfd509b1befd76ac30b7fb04e4a57236a99fc92b42d0545bc04f26072b18d169(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5dcccec6745486638b2e9cf24e037e791c081342e7b30cac9656f2d1d96c97f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd524d4728423e8c529813a4b0025edc1a77195cbba58ec9e201d3dc69286f48(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8563c69ef358110ec54491f935fc57966183b6e4dbb8e52452f38c41b50a5242(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3961a784419b0234d001f04bdc0c95b764040fbca31873bca2e4fbf3d86b2a02(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleActionsExtractions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13c8a499fe908a6bfdd842fef4498e5d7b146155a5a835b145547aab080e3075(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__654cd9c1f2ae3c9f2e501549dd17a1de35ae6686be18285705d0c1fd3ceda683(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ff1f99d789e25bc1ebc1efa846bbdbd323f949d17edbcac59f8923366be999f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a1ce51377655f9073175c16b8529b8e68d7b44d48ff0c4a59ea5840da05ddd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d77f14fc0e20f311722d332c96c4a831cf3f06829ac96424e1a967f2d1148935(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8adf4e28eda3ce25f282467f0a4bdb561648d8ccd9604715a353f03bfa4193d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleActionsExtractions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa4a0f0075c0b9f1c0ba33f6429b44c955a813bd3bdc9e4ecb66ce791296e859(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51cf3cdf57ea78f375f5fe079b0307b2d4e7533a398dcc3f09b3175de83d9c0f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEventRuleActionsAnnotate, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__788dda5a6ca82038dfa6e092c504570ac4319b4bc61680b6de291722efeb912e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEventRuleActionsEventAction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1388ef7ddfb4795d51f85e32751007fb780ade39e2a9efdd9c0f50fb2f1c1603(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEventRuleActionsExtractions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e31d73e9c421e375e71447b7a9b8a6429f4d07dcb98718b208b8fc707b356547(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEventRuleActionsPriority, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1f248f6a169408cb0fbf71ef426aff5e3e49811f54ac94e635c5429806dc564(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEventRuleActionsSeverity, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a508b0c80635946102c5dd14b1848329781ed28c06f5f83b9aaa7f92f59fc5e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEventRuleActionsSuppress, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e67e66e9eed8a7f24d68c8150303d0d8a3528a0c9e105f3cd9f47a694c8e62c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEventRuleActionsSuspend, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aeff65f0feea3c81d006a74bdafd650f019931805f551ac73e9cc7d53875c49(
    value: typing.Optional[ServiceEventRuleActions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4409ba60c4f1a916eff755a6f58ed8df73aacf94b7454b3cea68f88a8a20ab87(
    *,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e544373438ca17afd1f716221fd9c4b8088ff733512c4e2c739d1bc85ab81f36(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0de55bdcc45099b1b993e5b0b448e5bb9fbe4cc3e14e4456ff353552d6565faf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de7d0dc967e5c7f392031c75eed2a24ca88428d9f8b0b2a39a6a8318d95eacd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88a13bff9e508c2d87a8c9b60103148428d14515c8d975150e2e408075cb3173(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6386c3d8c89868944505be96836f1ea946286445b4a72ebfffaa0d454d57450b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__814efd3b8469a9e9e0a1c810c4056f6c371e34446edb6b796d120eefd9ff5098(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleActionsPriority]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ceca2df368442ce5c4a94b417f414666f89322f98aa18b2ad94dfc384f0333d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f78e391b5e83b6e5d3546fe6f77e8d8ffa92e945acb4ddf1d1433b30a948a8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f376c2d240864444bd370329aed843779133febb231d4dc3a5002ec03b81a14(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleActionsPriority]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05c3a809cec8cec2ea060d4cbd377ea547b313e3e7b612ff2e7c97f8296f1721(
    *,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac5176939af438f2e030ea856105fb2f7d3ca7e871b6f09ffd1bd72dc5a95647(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79ad64063d5c2a11455518a4be94ec2a5604caaa7854e998a0963d17ce3e2f0a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f48226a129b6243414f256c2c1fe6fbcfd71ca8a24af8dab045aa5049d5a00b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d39026a5b8fa532a2403876d072390935450d1b06d4e46465c47e5c039995c9c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9074dfc5a113a4ac35997f5eed8631bd4bc52cfe60c1e6e289aea10365c2fb9f(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b007f2c127683a7d117e8c085a395a662cdef3ca993fde10991bbf90264bc48(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleActionsSeverity]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac920882f32b191090fcf7b3c6fb1da191b5ac4358479b2f627865094c553505(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__548c7cb592c8fd66578d0f09ab9b97728a9fdba9176488d9d09bd7f9bcbe7586(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__459eb4bb9f5aed620a1ed757feda6c7c6136d170b825386d22059b638b2313de(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleActionsSeverity]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f389918a146ebd9d73a1f6bc697b9a893330f76f164dfc9a4a357bf355ef18d5(
    *,
    threshold_time_amount: typing.Optional[jsii.Number] = None,
    threshold_time_unit: typing.Optional[builtins.str] = None,
    threshold_value: typing.Optional[jsii.Number] = None,
    value: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5f536ef6faf8d8a6f2aae5226cd763991519dc78bc0e7271f30f614d7055149(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beb53e85719dc9226c60a43ec3fb05bb43a24c03cf2563befa76bde575506931(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bb6a6598740f9fe4acd0fca121e93c23732de431ec5d5e72566002b8e52b752(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f92e84692f2afd4aae7ed5e77db2e8819275eba9cfb785190a4894142570efa(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd0b7842d70ce19966a2f042881a93b38c1dfa010ce9b208e0b2ce703c239b8c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdc9f6b5d206f97865457c989b864a095eff71213fdc29b7ad8df82cdfcd021a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleActionsSuppress]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b76460735c2161d6e069517a1a83f2a1b7d67e29f53d0fe00f86b7af29d9d732(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18a2922a0758b5739724b6fd0f2490d962b11bf0bd8b03dae90d28f5c1fa469b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd7d9573d05a81d95b152828c1a20917ed227ecb97605d8cd2c87274630227cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fc82b0ef7be1f03cb537238f08619c8960798296b6dd5a5e49afe4979986786(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdedc7483c63e5d18b6e7d7cee932e846a90160334ce54aacfe8b68dbf14f6d6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb9e8dd88563105aa2da629e9a08ff60fd90319e07354d21e40f6d7488f58718(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleActionsSuppress]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7ba3a51bed4b805ab99c85c8ac39d27220030977225ae4ca449fc48f1b4e673(
    *,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43b7c92e6ff0c89e69b9296fd5df51acea6361a4b8a2672d5d7b3a296a631a04(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96864e97449fd104186a99577b74a85680a84883ecf17a7429d1b7b1ababc52d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7be0a6ea185ffef40ef6d792818ad48451fd4a7eeb09194cc735414f4c009b5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9ac4cd8de2806d08704137ede57b26644e46b9a211dd1edfbf9295487035719(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaa60f87268f7f4da52af71dd0886077328863dfc0c3654883f522ef32e8c561(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6199e8355c347b6ceb38e68c2e2eaaea2411810dadbb9dc6356148183bed771(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleActionsSuspend]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73c394080e04d2f8d9793e8577fd9ea1be4da959d283c0340720f9b657892325(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__897157bc5bb4f20b3049e4c7a9775992ef2cf265e5d7dcb841fd433a7de57204(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a58d49d23c91cbbad3ddb52e87302abaf937bf0a80c3dcb5813812bf8b4e61a0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleActionsSuspend]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fc771c1ff945e8bc3df2c7d59cd91f8f94c7e4487aadfd114ebae9a21adba04(
    *,
    operator: typing.Optional[builtins.str] = None,
    subconditions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEventRuleConditionsSubconditions, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdf1657a951bb32becfad7837f142ab02a8433ffb6d89792bfc31028173c549d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3f0fe8e482204b6809f661b7d50e9a6242f44351cf45b2fad802c40b867f75a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEventRuleConditionsSubconditions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a87bfa74d4de4d0418deeb91337d8dca98ae5179794d05d562bd486b48739f1a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3bb3159dd423a64bbcab9f2ed76be7a7bd7a7f26294f8e736859b07e6db0970(
    value: typing.Optional[ServiceEventRuleConditions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92e32d674371766c27483eb38339be450b2f381fd4c1aab3468ed628575aa3cb(
    *,
    operator: typing.Optional[builtins.str] = None,
    parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEventRuleConditionsSubconditionsParameter, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__015881765959edfca503bf3e13c4c45ffa95fbe7467c7ffd828334b613c361a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0b4dbd33e77b83df7c3157b6203de2e860bff6c515b4f57be4c0d501ddef6e9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b7cf6d639b229fdf2aea78e58d9d162e655a118df8a1b3882c02e4532697ccc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8474d24c9c29713559c3bdc19902785757d2a659cce5f36b5dfa6e447b791f5f(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b1c5facfe0bc10c20f80150847d4e912235b7d25915ce9bf4c9dc1811bd92af(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0556bf041a3f297ca080d031c49040efe363cf377ed797e83b8cb189b716ab17(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleConditionsSubconditions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dce9e1c69671d68278047171b823da6600feba7f14b36b0d37c947a43b7cccc9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1108af676fc1610938cb504684c9d098954043a15ecd73b9e9fa3c852c47d518(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEventRuleConditionsSubconditionsParameter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64c3659e29752701895b7fb44d3e5d52260c41ae580d68309173922df1b09edf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2a72355ff78b7f1f90a7d290f87afe97006974ecc454ee508745b482136d324(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleConditionsSubconditions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79fc2de3f52a6859044927c4337ed777bbd6ebc3bd7ade5900d2f4bced764cbc(
    *,
    path: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a84728a526a4738677d37536b072451ecc69f52a87cdb523af7056083ac581fa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd467a28852525e1b3a98dc05f4e137d0712cca8116421e352daef93b45fdf26(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b1f6ca2166fd29da4209ea6baa29d15abfc25fc2bdff975d05742219af2efd2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e15a8f10471aba0682e61fb9160fad78b66eb7292a36bfba3caaa7c5b24398f5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b6ae21ce2e15139bdf0b4271f4157fec87ee82024906bfa9356e0beec8766be(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecf3a9cd9300f13eaa0132e0c453a8c65ec57b6bc4c4130dabd2828b071e8020(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleConditionsSubconditionsParameter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a0ef9bb96d326f13d8dc0793dd5ae1f0c2366878c39250d2505caa85c66029e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95d251604490081a47719a3824009fa37184809b900c9e1667365132e9cd0100(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caa1314b7d481966e17467fe1837a12f809d462d20795160da476e7026c7ec48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6644bee53f851d43933a75ce66acffdb6a87992856ea8df66921c0b7bd4b535b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleConditionsSubconditionsParameter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32956afa851cd0df6a4cb30c532d23a083042b78f2af62757c083191e42b5be9(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    service: builtins.str,
    actions: typing.Optional[typing.Union[ServiceEventRuleActions, typing.Dict[builtins.str, typing.Any]]] = None,
    conditions: typing.Optional[typing.Union[ServiceEventRuleConditions, typing.Dict[builtins.str, typing.Any]]] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    position: typing.Optional[jsii.Number] = None,
    time_frame: typing.Optional[typing.Union[ServiceEventRuleTimeFrame, typing.Dict[builtins.str, typing.Any]]] = None,
    variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEventRuleVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52354ee370d1e9413c1063dd000e627e6de6caee1944886961e9a6225bcfe1f7(
    *,
    active_between: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEventRuleTimeFrameActiveBetween, typing.Dict[builtins.str, typing.Any]]]]] = None,
    scheduled_weekly: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEventRuleTimeFrameScheduledWeekly, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4311eba747c1d712b8c8b113d7a6f8b01d121d8fe2d551eb79342c5eb9a0bcad(
    *,
    end_time: typing.Optional[jsii.Number] = None,
    start_time: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e099e2b78d750da51fa6096b80aeb857f23144a74ac2a7572a3ac538ef94998d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7782262e7b8bb08a3a1ef1551d1b2b3f111ca107a7cf727ff2b3ad3361454cc4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e48c19276b50dae823a37c183fb566f042e37b049199f94bbea664e5af90aee4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a292a4aa25422e1a41bd2d97b4885e675645e6b311039db43b74e2006bbeb6e6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c65b7e18040d89cd42bcb3d1f9b598e099517984f7eeb317b0e72c649bfafc19(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c85143c0c79ebe1f6a4233218bde46021fc8fc53bbae88fb3c35acbc4bcfc77(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleTimeFrameActiveBetween]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__532eee966fc8218f51980087a84c6c5710909771b99f174fd3ad7f8e7c35422d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e4b3848f42160218176e07d81756b8b18f54ee781bf117c465d395384d8b2bc(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f525b1f22bfed503ea43a470b8fbbefca853c5b84d1d0b576f73259bc4db8a0d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69fb52cbb6a0aec4eb27afc777d096da09572da942c960629d54ff666d3c8024(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleTimeFrameActiveBetween]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69a089cb3e8bb5e9227712d94638b45212aee2108cc558b7536fa4e2fed8d8e6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af3b8b5ee8dd0ccff58645d1ec820a9735117ff73098901d69b66abc4f4d2c3d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEventRuleTimeFrameActiveBetween, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45ec944323d8c11bdaddc8253b6b80c9e957056a130e510f5e334da5bc19ce5f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEventRuleTimeFrameScheduledWeekly, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bf69a3a2e18dddf5720a80625c5bb098e0bc2c01c64cc0bbd14038bc68d892b(
    value: typing.Optional[ServiceEventRuleTimeFrame],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e88eb9f4805cabd6b5cfd9d722392054a3af7985b9b8c5a6d8d0f0f27ec6b1b(
    *,
    duration: typing.Optional[jsii.Number] = None,
    start_time: typing.Optional[jsii.Number] = None,
    timezone: typing.Optional[builtins.str] = None,
    weekdays: typing.Optional[typing.Sequence[jsii.Number]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccfabd83e5d623cd009141bd71c473fc2fc74cbab3f2e0f9ab90c851802d5359(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e770a9f76d8931e5d5c5f3de344a1f98d7db0c887aab8031f916c9ce0947609a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b99084d2139e2d0fa6600f47861104c720f47f4fb0bec2e10008890b4b79ed1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15bb5b335937c1af2dabd3effad88a385f08f5878b8084d098aef180c63146cc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee6b8556d2ffc52ed6c3033de66b996ebadbf3e45f6bd1f401cabc2e70daf9e5(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85ed5b94990e52b10658926fa41e90012066ab925b0614421c36f61ecc60347b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleTimeFrameScheduledWeekly]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dde47401d37725f2c6293690f2d809c85d2e2e81ac2a014575480bb6cf22d474(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97265e861a86db449a28c0252e8c68cbb46cf4100dd4db495fcf0776a2826bc8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c68c76b2946e5e9ff872d22f1662303457b657eb427a5d84409c98bcc3b679d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b8f0c0e2163d4990c038128c671b5c57369ecc2b7b24210b81d4b868c3f27e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9293b1ab2bf0116e7be6b2aea4ce0c019194df7f0661732efca024f045c69aca(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3959bbe2a6cdf84fe88abe419e1cdd61ce450743b5eee2f0ffbaec9de577f7ba(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleTimeFrameScheduledWeekly]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe2d5ab874b44f036c8ca60bcb461d0f6ea2bd4efd3ba79f34a83419c55cd6dd(
    *,
    name: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEventRuleVariableParameters, typing.Dict[builtins.str, typing.Any]]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91f9fb029d9e1b77afa796f7771d4f9970b5fda14a923bc0f9e3916f797af95d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1b4a67bdda2106cfc2cde1768a84ef14829a53b922cf707427c19ac154661e9(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54ea7eb8aec6d16cf71826c1a91d40b6cd5ce0274926c9ddca1500c8f6e6e960(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81be626d23e4db9187704e0d8ff69cf8a0b096acc000d9260149bf95f71ab121(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__301c6b63e277b5e2977a8d68f46b2117ec97dfffcda76c5c61a17827f3ba9d3b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a4d413757113c2229c3e0f2993c0550ad606140480345f0c9bd5f12fb5e63e5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleVariable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7597fe96ff06e46b8f143a9a6123921ff048e65ec203618998fc6811bcd646b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c745418a4459fdacc14b3b9ad25c021a98da5594210302c345f246193b3e279(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServiceEventRuleVariableParameters, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b871a7afce7dccc5fd94b695652feb26f55fa822f51f50f8a275c95fdb175b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96ec52089e88edd0119adeead2832d8ae39b19d277c78f5bab2de95abd15b496(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8edd1d9dd728839c8000e9ae88e63b7c12f23bb62f6b9d3c2fe5955c6dd18e69(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleVariable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a105f82609192c33980a7920dc4639159962e07b5ea248a5a662bd95fda1034b(
    *,
    path: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b32813b897f0a61878fd4506f3e6801427fd9f6ff0ae938cff4c96b1b66a9e5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9b6db746e91b382b55da14607c934e580d8f76af8dd1f135c105ff6b2793943(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa93c5a86be4ee4cbf0e8f6bea9fe6e99cb27bb433c5370323a29aa7a00ea5e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19e8befa6fe16c22ad9bdc6d09e38c9fb780fc5508cad45cd5211484d6a76c7b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82ac1fde40ca3f8f935b880aa85d2a0c630504f3c1e7b0b696dc60be65b264c7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf4afecea13c28429c25d7f7a59a6650c82c594d3e6b3e99c6fc026c99698d85(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServiceEventRuleVariableParameters]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e80704c1793b530e810d225bc1981ed320514896049d80b8dc7f45640d14f98a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db89182f36cea9d0913fa6431c50598ee97ede9502081dfc1bacc6cba670024b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__636a18dd97ee8a0c3e5e3e93ad6c0097a449f9b81320d5edf7de32e5afdf5831(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c158da27b5836728a135b54e05d1a25c5fb478040538d4a62107142d163b02cb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, ServiceEventRuleVariableParameters]],
) -> None:
    """Type checking stubs"""
    pass
