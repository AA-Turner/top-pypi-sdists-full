r'''
# `pagerduty_event_orchestration_global`

Refer to the Terraform Registry for docs: [`pagerduty_event_orchestration_global`](https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global).
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


class EventOrchestrationGlobal(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobal",
):
    '''Represents a {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global pagerduty_event_orchestration_global}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        catch_all: typing.Union["EventOrchestrationGlobalCatchAll", typing.Dict[builtins.str, typing.Any]],
        event_orchestration: builtins.str,
        set: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationGlobalSet", typing.Dict[builtins.str, typing.Any]]]],
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global pagerduty_event_orchestration_global} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param catch_all: catch_all block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#catch_all EventOrchestrationGlobal#catch_all}
        :param event_orchestration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#event_orchestration EventOrchestrationGlobal#event_orchestration}.
        :param set: set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#set EventOrchestrationGlobal#set}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#id EventOrchestrationGlobal#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7898293233ae0a207d81241c85b2c654cea3a012503a5e667a77a16de61b9f93)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = EventOrchestrationGlobalConfig(
            catch_all=catch_all,
            event_orchestration=event_orchestration,
            set=set,
            id=id,
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
        '''Generates CDKTF code for importing a EventOrchestrationGlobal resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the EventOrchestrationGlobal to import.
        :param import_from_id: The id of the existing EventOrchestrationGlobal that should be imported. Refer to the {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the EventOrchestrationGlobal to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__564730dbb66f292534c835172ee33821db25f29aacb25b215967b4b679c8956d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCatchAll")
    def put_catch_all(
        self,
        *,
        actions: typing.Union["EventOrchestrationGlobalCatchAllActions", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#actions EventOrchestrationGlobal#actions}
        '''
        value = EventOrchestrationGlobalCatchAll(actions=actions)

        return typing.cast(None, jsii.invoke(self, "putCatchAll", [value]))

    @jsii.member(jsii_name="putSet")
    def put_set(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationGlobalSet", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__458f834b39f750cb2789281a8affa937376c2bdba9048edccd8911e017d439f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSet", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="catchAll")
    def catch_all(self) -> "EventOrchestrationGlobalCatchAllOutputReference":
        return typing.cast("EventOrchestrationGlobalCatchAllOutputReference", jsii.get(self, "catchAll"))

    @builtins.property
    @jsii.member(jsii_name="set")
    def set(self) -> "EventOrchestrationGlobalSetList":
        return typing.cast("EventOrchestrationGlobalSetList", jsii.get(self, "set"))

    @builtins.property
    @jsii.member(jsii_name="catchAllInput")
    def catch_all_input(self) -> typing.Optional["EventOrchestrationGlobalCatchAll"]:
        return typing.cast(typing.Optional["EventOrchestrationGlobalCatchAll"], jsii.get(self, "catchAllInput"))

    @builtins.property
    @jsii.member(jsii_name="eventOrchestrationInput")
    def event_orchestration_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventOrchestrationInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="setInput")
    def set_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalSet"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalSet"]]], jsii.get(self, "setInput"))

    @builtins.property
    @jsii.member(jsii_name="eventOrchestration")
    def event_orchestration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventOrchestration"))

    @event_orchestration.setter
    def event_orchestration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07c2ddceef1fdae2f06bb8bd9dec5394f09451ab1cd1a48d54f4571a2b8ed323)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventOrchestration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2490bb3aa99d65cd452eb67796933377e098ec6c05e1818084d079d36ade2ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalCatchAll",
    jsii_struct_bases=[],
    name_mapping={"actions": "actions"},
)
class EventOrchestrationGlobalCatchAll:
    def __init__(
        self,
        *,
        actions: typing.Union["EventOrchestrationGlobalCatchAllActions", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#actions EventOrchestrationGlobal#actions}
        '''
        if isinstance(actions, dict):
            actions = EventOrchestrationGlobalCatchAllActions(**actions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a2491ea8be6ff2bc6b23ea66c48b78e7a7c902efa56c1eeb82ba035a0ad2ce5)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
        }

    @builtins.property
    def actions(self) -> "EventOrchestrationGlobalCatchAllActions":
        '''actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#actions EventOrchestrationGlobal#actions}
        '''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast("EventOrchestrationGlobalCatchAllActions", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationGlobalCatchAll(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalCatchAllActions",
    jsii_struct_bases=[],
    name_mapping={
        "annotate": "annotate",
        "automation_action": "automationAction",
        "drop_event": "dropEvent",
        "escalation_policy": "escalationPolicy",
        "event_action": "eventAction",
        "extraction": "extraction",
        "incident_custom_field_update": "incidentCustomFieldUpdate",
        "priority": "priority",
        "route_to": "routeTo",
        "severity": "severity",
        "suppress": "suppress",
        "suspend": "suspend",
        "variable": "variable",
    },
)
class EventOrchestrationGlobalCatchAllActions:
    def __init__(
        self,
        *,
        annotate: typing.Optional[builtins.str] = None,
        automation_action: typing.Optional[typing.Union["EventOrchestrationGlobalCatchAllActionsAutomationAction", typing.Dict[builtins.str, typing.Any]]] = None,
        drop_event: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        escalation_policy: typing.Optional[builtins.str] = None,
        event_action: typing.Optional[builtins.str] = None,
        extraction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationGlobalCatchAllActionsExtraction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        incident_custom_field_update: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationGlobalCatchAllActionsIncidentCustomFieldUpdate", typing.Dict[builtins.str, typing.Any]]]]] = None,
        priority: typing.Optional[builtins.str] = None,
        route_to: typing.Optional[builtins.str] = None,
        severity: typing.Optional[builtins.str] = None,
        suppress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        suspend: typing.Optional[jsii.Number] = None,
        variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationGlobalCatchAllActionsVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param annotate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#annotate EventOrchestrationGlobal#annotate}.
        :param automation_action: automation_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#automation_action EventOrchestrationGlobal#automation_action}
        :param drop_event: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#drop_event EventOrchestrationGlobal#drop_event}.
        :param escalation_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#escalation_policy EventOrchestrationGlobal#escalation_policy}.
        :param event_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#event_action EventOrchestrationGlobal#event_action}.
        :param extraction: extraction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#extraction EventOrchestrationGlobal#extraction}
        :param incident_custom_field_update: incident_custom_field_update block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#incident_custom_field_update EventOrchestrationGlobal#incident_custom_field_update}
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#priority EventOrchestrationGlobal#priority}.
        :param route_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#route_to EventOrchestrationGlobal#route_to}.
        :param severity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#severity EventOrchestrationGlobal#severity}.
        :param suppress: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#suppress EventOrchestrationGlobal#suppress}.
        :param suspend: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#suspend EventOrchestrationGlobal#suspend}.
        :param variable: variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#variable EventOrchestrationGlobal#variable}
        '''
        if isinstance(automation_action, dict):
            automation_action = EventOrchestrationGlobalCatchAllActionsAutomationAction(**automation_action)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4583487669670db5685ff768c51203e4dba6962f41aedd2de51e461daa8dc726)
            check_type(argname="argument annotate", value=annotate, expected_type=type_hints["annotate"])
            check_type(argname="argument automation_action", value=automation_action, expected_type=type_hints["automation_action"])
            check_type(argname="argument drop_event", value=drop_event, expected_type=type_hints["drop_event"])
            check_type(argname="argument escalation_policy", value=escalation_policy, expected_type=type_hints["escalation_policy"])
            check_type(argname="argument event_action", value=event_action, expected_type=type_hints["event_action"])
            check_type(argname="argument extraction", value=extraction, expected_type=type_hints["extraction"])
            check_type(argname="argument incident_custom_field_update", value=incident_custom_field_update, expected_type=type_hints["incident_custom_field_update"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument route_to", value=route_to, expected_type=type_hints["route_to"])
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
            check_type(argname="argument suppress", value=suppress, expected_type=type_hints["suppress"])
            check_type(argname="argument suspend", value=suspend, expected_type=type_hints["suspend"])
            check_type(argname="argument variable", value=variable, expected_type=type_hints["variable"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if annotate is not None:
            self._values["annotate"] = annotate
        if automation_action is not None:
            self._values["automation_action"] = automation_action
        if drop_event is not None:
            self._values["drop_event"] = drop_event
        if escalation_policy is not None:
            self._values["escalation_policy"] = escalation_policy
        if event_action is not None:
            self._values["event_action"] = event_action
        if extraction is not None:
            self._values["extraction"] = extraction
        if incident_custom_field_update is not None:
            self._values["incident_custom_field_update"] = incident_custom_field_update
        if priority is not None:
            self._values["priority"] = priority
        if route_to is not None:
            self._values["route_to"] = route_to
        if severity is not None:
            self._values["severity"] = severity
        if suppress is not None:
            self._values["suppress"] = suppress
        if suspend is not None:
            self._values["suspend"] = suspend
        if variable is not None:
            self._values["variable"] = variable

    @builtins.property
    def annotate(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#annotate EventOrchestrationGlobal#annotate}.'''
        result = self._values.get("annotate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def automation_action(
        self,
    ) -> typing.Optional["EventOrchestrationGlobalCatchAllActionsAutomationAction"]:
        '''automation_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#automation_action EventOrchestrationGlobal#automation_action}
        '''
        result = self._values.get("automation_action")
        return typing.cast(typing.Optional["EventOrchestrationGlobalCatchAllActionsAutomationAction"], result)

    @builtins.property
    def drop_event(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#drop_event EventOrchestrationGlobal#drop_event}.'''
        result = self._values.get("drop_event")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def escalation_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#escalation_policy EventOrchestrationGlobal#escalation_policy}.'''
        result = self._values.get("escalation_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#event_action EventOrchestrationGlobal#event_action}.'''
        result = self._values.get("event_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extraction(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalCatchAllActionsExtraction"]]]:
        '''extraction block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#extraction EventOrchestrationGlobal#extraction}
        '''
        result = self._values.get("extraction")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalCatchAllActionsExtraction"]]], result)

    @builtins.property
    def incident_custom_field_update(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalCatchAllActionsIncidentCustomFieldUpdate"]]]:
        '''incident_custom_field_update block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#incident_custom_field_update EventOrchestrationGlobal#incident_custom_field_update}
        '''
        result = self._values.get("incident_custom_field_update")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalCatchAllActionsIncidentCustomFieldUpdate"]]], result)

    @builtins.property
    def priority(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#priority EventOrchestrationGlobal#priority}.'''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def route_to(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#route_to EventOrchestrationGlobal#route_to}.'''
        result = self._values.get("route_to")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def severity(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#severity EventOrchestrationGlobal#severity}.'''
        result = self._values.get("severity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suppress(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#suppress EventOrchestrationGlobal#suppress}.'''
        result = self._values.get("suppress")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def suspend(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#suspend EventOrchestrationGlobal#suspend}.'''
        result = self._values.get("suspend")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def variable(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalCatchAllActionsVariable"]]]:
        '''variable block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#variable EventOrchestrationGlobal#variable}
        '''
        result = self._values.get("variable")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalCatchAllActionsVariable"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationGlobalCatchAllActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalCatchAllActionsAutomationAction",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "url": "url",
        "auto_send": "autoSend",
        "header": "header",
        "parameter": "parameter",
        "trigger_types": "triggerTypes",
    },
)
class EventOrchestrationGlobalCatchAllActionsAutomationAction:
    def __init__(
        self,
        *,
        name: builtins.str,
        url: builtins.str,
        auto_send: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationGlobalCatchAllActionsAutomationActionHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationGlobalCatchAllActionsAutomationActionParameter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        trigger_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#name EventOrchestrationGlobal#name}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#url EventOrchestrationGlobal#url}.
        :param auto_send: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#auto_send EventOrchestrationGlobal#auto_send}.
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#header EventOrchestrationGlobal#header}
        :param parameter: parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#parameter EventOrchestrationGlobal#parameter}
        :param trigger_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#trigger_types EventOrchestrationGlobal#trigger_types}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3aa7554157c3709e9796076b823722a932d57649b3cd18925319019ab07058f4)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument auto_send", value=auto_send, expected_type=type_hints["auto_send"])
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
            check_type(argname="argument parameter", value=parameter, expected_type=type_hints["parameter"])
            check_type(argname="argument trigger_types", value=trigger_types, expected_type=type_hints["trigger_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "url": url,
        }
        if auto_send is not None:
            self._values["auto_send"] = auto_send
        if header is not None:
            self._values["header"] = header
        if parameter is not None:
            self._values["parameter"] = parameter
        if trigger_types is not None:
            self._values["trigger_types"] = trigger_types

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#name EventOrchestrationGlobal#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#url EventOrchestrationGlobal#url}.'''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_send(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#auto_send EventOrchestrationGlobal#auto_send}.'''
        result = self._values.get("auto_send")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalCatchAllActionsAutomationActionHeader"]]]:
        '''header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#header EventOrchestrationGlobal#header}
        '''
        result = self._values.get("header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalCatchAllActionsAutomationActionHeader"]]], result)

    @builtins.property
    def parameter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalCatchAllActionsAutomationActionParameter"]]]:
        '''parameter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#parameter EventOrchestrationGlobal#parameter}
        '''
        result = self._values.get("parameter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalCatchAllActionsAutomationActionParameter"]]], result)

    @builtins.property
    def trigger_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#trigger_types EventOrchestrationGlobal#trigger_types}.'''
        result = self._values.get("trigger_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationGlobalCatchAllActionsAutomationAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalCatchAllActionsAutomationActionHeader",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class EventOrchestrationGlobalCatchAllActionsAutomationActionHeader:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#key EventOrchestrationGlobal#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#value EventOrchestrationGlobal#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25d6263f7f939f16ce5239b58a28df658272be7a72592fe257cae14ddceb0570)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#key EventOrchestrationGlobal#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#value EventOrchestrationGlobal#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationGlobalCatchAllActionsAutomationActionHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationGlobalCatchAllActionsAutomationActionHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalCatchAllActionsAutomationActionHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1208d1337d1bfd14146310afe74504cd73287245531735a42a83b60cd61bef63)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventOrchestrationGlobalCatchAllActionsAutomationActionHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7efa50933d495c44d7ddf858a7f7ae7be337ff8436d39113cf1a815b1c98dad)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationGlobalCatchAllActionsAutomationActionHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e10b61e4b934f6ab3a5af8cd970677b27c96664ffc9533ba1421a59263f9c44f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b31e291f1931262649c0d2862deebe0d226983d59ee53c54193d9e0376e6eae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c9a845064e98833a82650fc568e5816c933421446aa0827d7ae2af3f82799d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalCatchAllActionsAutomationActionHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalCatchAllActionsAutomationActionHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalCatchAllActionsAutomationActionHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__344edf758ceb8c34d9528d36b9a1bdf917875b55d542f1e41545c732de974451)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationGlobalCatchAllActionsAutomationActionHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalCatchAllActionsAutomationActionHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__630f0d8a58eab6009b1f2f9c8fc4b532c9964a8f9de16ddd0f86e7c5914bb5de)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14c7cb588fab74a4079e89634101323820f33887597447679f1a2a2ef0a91809)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b41ec089af1dedea8cf1af491c525eb42bcfccbf25626d972cb723504f511031)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalCatchAllActionsAutomationActionHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalCatchAllActionsAutomationActionHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalCatchAllActionsAutomationActionHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bd6cb6ebf9c313df83f5fca371cad0e006f2f8af6c5839c6cf2418822a2e916)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationGlobalCatchAllActionsAutomationActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalCatchAllActionsAutomationActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a13c3d27fcad67c7f5ddb6fe2554fd71d3d39199dd09f919549836a40d3d9c2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHeader")
    def put_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalCatchAllActionsAutomationActionHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef3bbdb8aa45b505c4ebf7811cbbc24b02261961f0624ba324af4fcf770c8656)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeader", [value]))

    @jsii.member(jsii_name="putParameter")
    def put_parameter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationGlobalCatchAllActionsAutomationActionParameter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5732fd207398678ef815e164358fcef25394c5a3e67613930ae082335a4a9b6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putParameter", [value]))

    @jsii.member(jsii_name="resetAutoSend")
    def reset_auto_send(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoSend", []))

    @jsii.member(jsii_name="resetHeader")
    def reset_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeader", []))

    @jsii.member(jsii_name="resetParameter")
    def reset_parameter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameter", []))

    @jsii.member(jsii_name="resetTriggerTypes")
    def reset_trigger_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTriggerTypes", []))

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(
        self,
    ) -> EventOrchestrationGlobalCatchAllActionsAutomationActionHeaderList:
        return typing.cast(EventOrchestrationGlobalCatchAllActionsAutomationActionHeaderList, jsii.get(self, "header"))

    @builtins.property
    @jsii.member(jsii_name="parameter")
    def parameter(
        self,
    ) -> "EventOrchestrationGlobalCatchAllActionsAutomationActionParameterList":
        return typing.cast("EventOrchestrationGlobalCatchAllActionsAutomationActionParameterList", jsii.get(self, "parameter"))

    @builtins.property
    @jsii.member(jsii_name="autoSendInput")
    def auto_send_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoSendInput"))

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalCatchAllActionsAutomationActionHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalCatchAllActionsAutomationActionHeader]]], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parameterInput")
    def parameter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalCatchAllActionsAutomationActionParameter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalCatchAllActionsAutomationActionParameter"]]], jsii.get(self, "parameterInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerTypesInput")
    def trigger_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "triggerTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="autoSend")
    def auto_send(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoSend"))

    @auto_send.setter
    def auto_send(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93123901f8d1c8e6060473ccc84fd2c772d8aa5de0129f74530a2caea061df12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoSend", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cc0c0b03e9b47a858383c495e183fdce6d09ef29f9fc624d5e08904c085ccf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="triggerTypes")
    def trigger_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "triggerTypes"))

    @trigger_types.setter
    def trigger_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1102093df97fbad28bfb226dd086ee15ef2b401b6ba31a02dc5f8a46ec749cd4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3fe80568f9189b932ce3fed13efbf5d45377faca1278ae17b140b81fc81fead)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventOrchestrationGlobalCatchAllActionsAutomationAction]:
        return typing.cast(typing.Optional[EventOrchestrationGlobalCatchAllActionsAutomationAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventOrchestrationGlobalCatchAllActionsAutomationAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86b3b0fdb72c30c2c124b99b7548a2b195b75eacdcaa77d02d6cb37cd67598b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalCatchAllActionsAutomationActionParameter",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class EventOrchestrationGlobalCatchAllActionsAutomationActionParameter:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#key EventOrchestrationGlobal#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#value EventOrchestrationGlobal#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8bf5cff7ab8d977bde6247d8b87a97cacc34598a770f783a035182d2b9a6bdf)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#key EventOrchestrationGlobal#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#value EventOrchestrationGlobal#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationGlobalCatchAllActionsAutomationActionParameter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationGlobalCatchAllActionsAutomationActionParameterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalCatchAllActionsAutomationActionParameterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e972c64ef36c2c1b80aa86702bdfc44c858b30eeb73e7bbcbe32d7bd6498e099)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventOrchestrationGlobalCatchAllActionsAutomationActionParameterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d608079eea039f33cfba7036550a89d17990f0d23f34141ea84163f340eb44b2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationGlobalCatchAllActionsAutomationActionParameterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__602b0f4f46cbc4f21a8ff6e130453c4374d011b692ddc18bb05322fe6789558d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6abebbba4b7fb067fed8348b708c2c830ceec9c9d9ddf249c174c5f25e2307d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__18e2edb00fc4428edb0ceebd74ce6efe0f7177217df23f888be271b3f3b5331c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalCatchAllActionsAutomationActionParameter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalCatchAllActionsAutomationActionParameter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalCatchAllActionsAutomationActionParameter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3578eec54a1df37f1cb8f74f8ca03ee1f497bea9e2615c4409a7df633071522f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationGlobalCatchAllActionsAutomationActionParameterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalCatchAllActionsAutomationActionParameterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__08c98ccb185373e6ae09a608593faf47b89b8694091438735f4821f75fec3130)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f51f2a93221b0a64e815e529993d934be046152a0333799479c2df91b799fb85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef264dd1e30a54d2e38ba9096d6e9efcaaca3c0493265ebd8c35ebe5a08a6bdb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalCatchAllActionsAutomationActionParameter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalCatchAllActionsAutomationActionParameter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalCatchAllActionsAutomationActionParameter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2424b7d1fe724d27379ab225f5d1c9a21d4e3df8b805d95f7cac4d0e7bbbaa8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalCatchAllActionsExtraction",
    jsii_struct_bases=[],
    name_mapping={
        "target": "target",
        "regex": "regex",
        "source": "source",
        "template": "template",
    },
)
class EventOrchestrationGlobalCatchAllActionsExtraction:
    def __init__(
        self,
        *,
        target: builtins.str,
        regex: typing.Optional[builtins.str] = None,
        source: typing.Optional[builtins.str] = None,
        template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#target EventOrchestrationGlobal#target}.
        :param regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#regex EventOrchestrationGlobal#regex}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#source EventOrchestrationGlobal#source}.
        :param template: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#template EventOrchestrationGlobal#template}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c13c1c34aa2f8009fb969c1c9b9b3e863409eea556e7a2290eb65cdfb019a16)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target": target,
        }
        if regex is not None:
            self._values["regex"] = regex
        if source is not None:
            self._values["source"] = source
        if template is not None:
            self._values["template"] = template

    @builtins.property
    def target(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#target EventOrchestrationGlobal#target}.'''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def regex(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#regex EventOrchestrationGlobal#regex}.'''
        result = self._values.get("regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#source EventOrchestrationGlobal#source}.'''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#template EventOrchestrationGlobal#template}.'''
        result = self._values.get("template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationGlobalCatchAllActionsExtraction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationGlobalCatchAllActionsExtractionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalCatchAllActionsExtractionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1228287f122c2b16186b4a9f43aff0557b56c596c3800bb64d93434176649604)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventOrchestrationGlobalCatchAllActionsExtractionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a736304f9f9fb74c0b6b87de68be05f758342d6709a6f354a76c3b9215c30b8)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationGlobalCatchAllActionsExtractionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a04378a3ad9abb3517820eec92245417bb5b9cde9c3254039cd7c9439f5537d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2ffa71027a693defb82db3ccfcacc1b45793b4054c8dcd097dfb6bc58bb85b5e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c68bcd3f30c7eab876569f6a5f4f0f9244bc893e6bb2efd27dfd1732fc0e9b68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalCatchAllActionsExtraction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalCatchAllActionsExtraction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalCatchAllActionsExtraction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e813b6e26c71e17ecc30e93a4e6a456d2f873c22a04106b3b68848cb1aac967e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationGlobalCatchAllActionsExtractionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalCatchAllActionsExtractionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__62aee2e1f826d80ad26c8451b3e126d24dadbecfcdfd2d5e1eb9b498b52bad8f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9668313c6059c7e83b2c2fac06f331ac3c2cc440e0147875e3925899ebc43b31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75da27cbea83bf3f0ae1fe7e1a2974da6a5ddd9066ef82f1257d5c28741c1277)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca32c5643225a6537b11e362f14ca9400633356e47f9d369c3b03fe2edbfacac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="template")
    def template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "template"))

    @template.setter
    def template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c17762ea1183cb1c9808ba7e2bf5c9ffdaa14e108f2eb1d17a7a3c964f2a59f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "template", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalCatchAllActionsExtraction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalCatchAllActionsExtraction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalCatchAllActionsExtraction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f3ab4df8ffd5d986c2ee0c6d1fae6a536161662453dc81a51678f3364ae37a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalCatchAllActionsIncidentCustomFieldUpdate",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "value": "value"},
)
class EventOrchestrationGlobalCatchAllActionsIncidentCustomFieldUpdate:
    def __init__(self, *, id: builtins.str, value: builtins.str) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#id EventOrchestrationGlobal#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#value EventOrchestrationGlobal#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b375c4b1d808a3f460f31e3cf8a8afd1bf9ad8635ace71d2f46d2ab4d18a3978)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "value": value,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#id EventOrchestrationGlobal#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#value EventOrchestrationGlobal#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationGlobalCatchAllActionsIncidentCustomFieldUpdate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationGlobalCatchAllActionsIncidentCustomFieldUpdateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalCatchAllActionsIncidentCustomFieldUpdateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50641c458e5848b40de67a8f5f49b6fdef1deb6adb0a62f7d6362078043ad0fd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventOrchestrationGlobalCatchAllActionsIncidentCustomFieldUpdateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f64bbd615fd4846255e70b39bdcd407a97566d3bf753ca15f7caec4182764ec5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationGlobalCatchAllActionsIncidentCustomFieldUpdateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c16b77ef8f35adc561de9b7df55e6c6711de5745a2ea5947004b3462048e998a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__274b408483588ace532980bca0728f27be740e3ab5f0d2fed3454f8b7f88b633)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e69ec28386f53cdade49e584a34347e09d827d0a8ecac6211635c561cfe55580)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalCatchAllActionsIncidentCustomFieldUpdate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalCatchAllActionsIncidentCustomFieldUpdate]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalCatchAllActionsIncidentCustomFieldUpdate]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acedca55e8af35ea8020e36b787c74428a70b33fbc5468952f7b6374a65f4970)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationGlobalCatchAllActionsIncidentCustomFieldUpdateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalCatchAllActionsIncidentCustomFieldUpdateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__97662cfc86ec1c9957f890eeba92f5f3f926f8424f4504afcca1cb800fc4d2cb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__888063f1430d54fed06cd4c2388d9b2b857a806f8528366c3fa0d5c156a175c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5ab831a90d2b9460aa1f8140f8aea287693ca91216c2343418a684cac25ef3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalCatchAllActionsIncidentCustomFieldUpdate]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalCatchAllActionsIncidentCustomFieldUpdate]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalCatchAllActionsIncidentCustomFieldUpdate]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d78e5d3a7604e5fd795cfdfa57da28a368e9c8edab7a569b17a6d38d845f114)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationGlobalCatchAllActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalCatchAllActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__318845c7f236a4b07df201ca2d85b3c266e5c51cf2b98641e401f14d5540b2f9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutomationAction")
    def put_automation_action(
        self,
        *,
        name: builtins.str,
        url: builtins.str,
        auto_send: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalCatchAllActionsAutomationActionHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
        parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalCatchAllActionsAutomationActionParameter, typing.Dict[builtins.str, typing.Any]]]]] = None,
        trigger_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#name EventOrchestrationGlobal#name}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#url EventOrchestrationGlobal#url}.
        :param auto_send: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#auto_send EventOrchestrationGlobal#auto_send}.
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#header EventOrchestrationGlobal#header}
        :param parameter: parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#parameter EventOrchestrationGlobal#parameter}
        :param trigger_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#trigger_types EventOrchestrationGlobal#trigger_types}.
        '''
        value = EventOrchestrationGlobalCatchAllActionsAutomationAction(
            name=name,
            url=url,
            auto_send=auto_send,
            header=header,
            parameter=parameter,
            trigger_types=trigger_types,
        )

        return typing.cast(None, jsii.invoke(self, "putAutomationAction", [value]))

    @jsii.member(jsii_name="putExtraction")
    def put_extraction(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalCatchAllActionsExtraction, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__689fdd5bf690ec9f7849e389fa6162498426a850fa96671abfed50ad68ff4d5c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExtraction", [value]))

    @jsii.member(jsii_name="putIncidentCustomFieldUpdate")
    def put_incident_custom_field_update(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalCatchAllActionsIncidentCustomFieldUpdate, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a81465c3b3fea128babbafcea4b47c2db67947ba99baa2c2b3a52dbd387131ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIncidentCustomFieldUpdate", [value]))

    @jsii.member(jsii_name="putVariable")
    def put_variable(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationGlobalCatchAllActionsVariable", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cc704c567dcd60574cdf347d4acef9f3ca10271e415db8e4a8cb6ea5c1cc49f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVariable", [value]))

    @jsii.member(jsii_name="resetAnnotate")
    def reset_annotate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotate", []))

    @jsii.member(jsii_name="resetAutomationAction")
    def reset_automation_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomationAction", []))

    @jsii.member(jsii_name="resetDropEvent")
    def reset_drop_event(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDropEvent", []))

    @jsii.member(jsii_name="resetEscalationPolicy")
    def reset_escalation_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEscalationPolicy", []))

    @jsii.member(jsii_name="resetEventAction")
    def reset_event_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventAction", []))

    @jsii.member(jsii_name="resetExtraction")
    def reset_extraction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtraction", []))

    @jsii.member(jsii_name="resetIncidentCustomFieldUpdate")
    def reset_incident_custom_field_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncidentCustomFieldUpdate", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetRouteTo")
    def reset_route_to(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRouteTo", []))

    @jsii.member(jsii_name="resetSeverity")
    def reset_severity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeverity", []))

    @jsii.member(jsii_name="resetSuppress")
    def reset_suppress(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuppress", []))

    @jsii.member(jsii_name="resetSuspend")
    def reset_suspend(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuspend", []))

    @jsii.member(jsii_name="resetVariable")
    def reset_variable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVariable", []))

    @builtins.property
    @jsii.member(jsii_name="automationAction")
    def automation_action(
        self,
    ) -> EventOrchestrationGlobalCatchAllActionsAutomationActionOutputReference:
        return typing.cast(EventOrchestrationGlobalCatchAllActionsAutomationActionOutputReference, jsii.get(self, "automationAction"))

    @builtins.property
    @jsii.member(jsii_name="extraction")
    def extraction(self) -> EventOrchestrationGlobalCatchAllActionsExtractionList:
        return typing.cast(EventOrchestrationGlobalCatchAllActionsExtractionList, jsii.get(self, "extraction"))

    @builtins.property
    @jsii.member(jsii_name="incidentCustomFieldUpdate")
    def incident_custom_field_update(
        self,
    ) -> EventOrchestrationGlobalCatchAllActionsIncidentCustomFieldUpdateList:
        return typing.cast(EventOrchestrationGlobalCatchAllActionsIncidentCustomFieldUpdateList, jsii.get(self, "incidentCustomFieldUpdate"))

    @builtins.property
    @jsii.member(jsii_name="variable")
    def variable(self) -> "EventOrchestrationGlobalCatchAllActionsVariableList":
        return typing.cast("EventOrchestrationGlobalCatchAllActionsVariableList", jsii.get(self, "variable"))

    @builtins.property
    @jsii.member(jsii_name="annotateInput")
    def annotate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "annotateInput"))

    @builtins.property
    @jsii.member(jsii_name="automationActionInput")
    def automation_action_input(
        self,
    ) -> typing.Optional[EventOrchestrationGlobalCatchAllActionsAutomationAction]:
        return typing.cast(typing.Optional[EventOrchestrationGlobalCatchAllActionsAutomationAction], jsii.get(self, "automationActionInput"))

    @builtins.property
    @jsii.member(jsii_name="dropEventInput")
    def drop_event_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dropEventInput"))

    @builtins.property
    @jsii.member(jsii_name="escalationPolicyInput")
    def escalation_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "escalationPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="eventActionInput")
    def event_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventActionInput"))

    @builtins.property
    @jsii.member(jsii_name="extractionInput")
    def extraction_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalCatchAllActionsExtraction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalCatchAllActionsExtraction]]], jsii.get(self, "extractionInput"))

    @builtins.property
    @jsii.member(jsii_name="incidentCustomFieldUpdateInput")
    def incident_custom_field_update_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalCatchAllActionsIncidentCustomFieldUpdate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalCatchAllActionsIncidentCustomFieldUpdate]]], jsii.get(self, "incidentCustomFieldUpdateInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="routeToInput")
    def route_to_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routeToInput"))

    @builtins.property
    @jsii.member(jsii_name="severityInput")
    def severity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "severityInput"))

    @builtins.property
    @jsii.member(jsii_name="suppressInput")
    def suppress_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "suppressInput"))

    @builtins.property
    @jsii.member(jsii_name="suspendInput")
    def suspend_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "suspendInput"))

    @builtins.property
    @jsii.member(jsii_name="variableInput")
    def variable_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalCatchAllActionsVariable"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalCatchAllActionsVariable"]]], jsii.get(self, "variableInput"))

    @builtins.property
    @jsii.member(jsii_name="annotate")
    def annotate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "annotate"))

    @annotate.setter
    def annotate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea055b34175fc78351f0656be7e68f3cd02099e9b8064885b416af774ae75a19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dropEvent")
    def drop_event(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dropEvent"))

    @drop_event.setter
    def drop_event(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e2c15d5e25c7b8321baf795eb000c1d666e84c255aed75eff2548003038aea8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dropEvent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="escalationPolicy")
    def escalation_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "escalationPolicy"))

    @escalation_policy.setter
    def escalation_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80d8120f541dc2661444cd9200ae6d1112eb55390749f3fe4c936d695591593f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "escalationPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventAction")
    def event_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventAction"))

    @event_action.setter
    def event_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c87815e3b5b954bc10f05a59c1cf8ec640d9fd25db52cf08ff9354fbc3ac76f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0c88068184c3fc48e2c8c3df2e18349fc08457694f05d020d5172efff8d1d52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routeTo")
    def route_to(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routeTo"))

    @route_to.setter
    def route_to(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42d0b1d770d4bd8ea7b8a724a61b03a182b5d5dcc3fa3376faabda9fb7e1afdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeTo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "severity"))

    @severity.setter
    def severity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7f1eb1ba9b0b04fc1a14d6936580d9d72b523c239fab6e15b3300f555638392)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "severity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suppress")
    def suppress(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "suppress"))

    @suppress.setter
    def suppress(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d75d7d20244dcc88dbc7aaccecc5357c94cdea7eab073935cbd5f418c17e6024)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suppress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suspend")
    def suspend(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "suspend"))

    @suspend.setter
    def suspend(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6b765e28c6e4acc79a301522cdf1f823a2c636ef91891c1f67c265fb81e5fb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suspend", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventOrchestrationGlobalCatchAllActions]:
        return typing.cast(typing.Optional[EventOrchestrationGlobalCatchAllActions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventOrchestrationGlobalCatchAllActions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9850dca92fc4f3051ae02f1e0502c52dd6391605108d03f307a5618264efb6a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalCatchAllActionsVariable",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "path": "path", "type": "type", "value": "value"},
)
class EventOrchestrationGlobalCatchAllActionsVariable:
    def __init__(
        self,
        *,
        name: builtins.str,
        path: builtins.str,
        type: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#name EventOrchestrationGlobal#name}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#path EventOrchestrationGlobal#path}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#type EventOrchestrationGlobal#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#value EventOrchestrationGlobal#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d0aeb509773364475895da1136016fd834150cbcd65e6a3c334ee82dbaf2482)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "path": path,
            "type": type,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#name EventOrchestrationGlobal#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#path EventOrchestrationGlobal#path}.'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#type EventOrchestrationGlobal#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#value EventOrchestrationGlobal#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationGlobalCatchAllActionsVariable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationGlobalCatchAllActionsVariableList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalCatchAllActionsVariableList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d3e78bc70f179e784abde44adbadb21be62c52b69dc3fbadd5072a8caa99809d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventOrchestrationGlobalCatchAllActionsVariableOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__241f9a5cfac66e40d53910c022fe5d7efff5986586c15ee92d1d40b1edde73f5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationGlobalCatchAllActionsVariableOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__063e4f107aaea9c2a2cdb6c2d720b568f08157d28d8097e2e36c6fb733c2b106)
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
            type_hints = typing.get_type_hints(_typecheckingstub__29342ebc6a7032ded6e1dae13006e8287e5f3f27dd0ba8babc7681b91ac7f124)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb60e8f191f3271d6dcd5f50888b7fd0154b03e861e10491ce083213b3ee7882)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalCatchAllActionsVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalCatchAllActionsVariable]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalCatchAllActionsVariable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cf34c26b3e1545dfff7a03c97b1e18f3c87af3e8bfc4a7cf42b2e02b80947fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationGlobalCatchAllActionsVariableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalCatchAllActionsVariableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5121f651247daa5059792ab323a62a05c8cac682ba42469309be0fbea3e568d6)
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
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57e3a9e450bc78ced1ec9e9bd8074f1636938ccf7a911395b401ca147f40f0b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fd17d465513cb8c5e94581b22f5a9682a27d6516e3d92567b852436a2b232f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__815afa92d2a5b95632c92e6fea3617eff92eb7173e30d45eaf27e9364c8487a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72a8782b38c95b826d570a84b0ab2423736bde1f6ffcfcdf9171b452b4bb510a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalCatchAllActionsVariable]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalCatchAllActionsVariable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalCatchAllActionsVariable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e2c8cd9ef19d67ece70fe2d1e63ee0b23d3cdd71885f0f83444acb4bd9be19f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationGlobalCatchAllOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalCatchAllOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__29a713818171aac34a6cc70b073f843e13833a232a39d475ac080265b348cea2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putActions")
    def put_actions(
        self,
        *,
        annotate: typing.Optional[builtins.str] = None,
        automation_action: typing.Optional[typing.Union[EventOrchestrationGlobalCatchAllActionsAutomationAction, typing.Dict[builtins.str, typing.Any]]] = None,
        drop_event: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        escalation_policy: typing.Optional[builtins.str] = None,
        event_action: typing.Optional[builtins.str] = None,
        extraction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalCatchAllActionsExtraction, typing.Dict[builtins.str, typing.Any]]]]] = None,
        incident_custom_field_update: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalCatchAllActionsIncidentCustomFieldUpdate, typing.Dict[builtins.str, typing.Any]]]]] = None,
        priority: typing.Optional[builtins.str] = None,
        route_to: typing.Optional[builtins.str] = None,
        severity: typing.Optional[builtins.str] = None,
        suppress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        suspend: typing.Optional[jsii.Number] = None,
        variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalCatchAllActionsVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param annotate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#annotate EventOrchestrationGlobal#annotate}.
        :param automation_action: automation_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#automation_action EventOrchestrationGlobal#automation_action}
        :param drop_event: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#drop_event EventOrchestrationGlobal#drop_event}.
        :param escalation_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#escalation_policy EventOrchestrationGlobal#escalation_policy}.
        :param event_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#event_action EventOrchestrationGlobal#event_action}.
        :param extraction: extraction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#extraction EventOrchestrationGlobal#extraction}
        :param incident_custom_field_update: incident_custom_field_update block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#incident_custom_field_update EventOrchestrationGlobal#incident_custom_field_update}
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#priority EventOrchestrationGlobal#priority}.
        :param route_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#route_to EventOrchestrationGlobal#route_to}.
        :param severity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#severity EventOrchestrationGlobal#severity}.
        :param suppress: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#suppress EventOrchestrationGlobal#suppress}.
        :param suspend: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#suspend EventOrchestrationGlobal#suspend}.
        :param variable: variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#variable EventOrchestrationGlobal#variable}
        '''
        value = EventOrchestrationGlobalCatchAllActions(
            annotate=annotate,
            automation_action=automation_action,
            drop_event=drop_event,
            escalation_policy=escalation_policy,
            event_action=event_action,
            extraction=extraction,
            incident_custom_field_update=incident_custom_field_update,
            priority=priority,
            route_to=route_to,
            severity=severity,
            suppress=suppress,
            suspend=suspend,
            variable=variable,
        )

        return typing.cast(None, jsii.invoke(self, "putActions", [value]))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> EventOrchestrationGlobalCatchAllActionsOutputReference:
        return typing.cast(EventOrchestrationGlobalCatchAllActionsOutputReference, jsii.get(self, "actions"))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(self) -> typing.Optional[EventOrchestrationGlobalCatchAllActions]:
        return typing.cast(typing.Optional[EventOrchestrationGlobalCatchAllActions], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EventOrchestrationGlobalCatchAll]:
        return typing.cast(typing.Optional[EventOrchestrationGlobalCatchAll], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventOrchestrationGlobalCatchAll],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6251be1e9865316cbec35e92db3aa4d8e62d3f97e6cf8a405f7cff110b60c8a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "catch_all": "catchAll",
        "event_orchestration": "eventOrchestration",
        "set": "set",
        "id": "id",
    },
)
class EventOrchestrationGlobalConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        catch_all: typing.Union[EventOrchestrationGlobalCatchAll, typing.Dict[builtins.str, typing.Any]],
        event_orchestration: builtins.str,
        set: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationGlobalSet", typing.Dict[builtins.str, typing.Any]]]],
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param catch_all: catch_all block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#catch_all EventOrchestrationGlobal#catch_all}
        :param event_orchestration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#event_orchestration EventOrchestrationGlobal#event_orchestration}.
        :param set: set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#set EventOrchestrationGlobal#set}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#id EventOrchestrationGlobal#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(catch_all, dict):
            catch_all = EventOrchestrationGlobalCatchAll(**catch_all)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afd75dc293d2a0ad64738537c97bc8b7eb768ec9672e1a6dc574b818ff3792e5)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument catch_all", value=catch_all, expected_type=type_hints["catch_all"])
            check_type(argname="argument event_orchestration", value=event_orchestration, expected_type=type_hints["event_orchestration"])
            check_type(argname="argument set", value=set, expected_type=type_hints["set"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "catch_all": catch_all,
            "event_orchestration": event_orchestration,
            "set": set,
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
        if id is not None:
            self._values["id"] = id

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
    def catch_all(self) -> EventOrchestrationGlobalCatchAll:
        '''catch_all block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#catch_all EventOrchestrationGlobal#catch_all}
        '''
        result = self._values.get("catch_all")
        assert result is not None, "Required property 'catch_all' is missing"
        return typing.cast(EventOrchestrationGlobalCatchAll, result)

    @builtins.property
    def event_orchestration(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#event_orchestration EventOrchestrationGlobal#event_orchestration}.'''
        result = self._values.get("event_orchestration")
        assert result is not None, "Required property 'event_orchestration' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def set(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalSet"]]:
        '''set block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#set EventOrchestrationGlobal#set}
        '''
        result = self._values.get("set")
        assert result is not None, "Required property 'set' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalSet"]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#id EventOrchestrationGlobal#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationGlobalConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalSet",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "rule": "rule"},
)
class EventOrchestrationGlobalSet:
    def __init__(
        self,
        *,
        id: builtins.str,
        rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationGlobalSetRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#id EventOrchestrationGlobal#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#rule EventOrchestrationGlobal#rule}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__305a6830506cb32487336526cc8631fb7f7318d68a61dabd395b65df1c2d7f56)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if rule is not None:
            self._values["rule"] = rule

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#id EventOrchestrationGlobal#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalSetRule"]]]:
        '''rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#rule EventOrchestrationGlobal#rule}
        '''
        result = self._values.get("rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalSetRule"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationGlobalSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationGlobalSetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalSetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8da35d4848f1646e622a6ea7f780d0b564b56f3c01f05e704759450e40302c59)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "EventOrchestrationGlobalSetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__448f4cd565464b901ec80b75a8accdb4d1eedbbd42c305b123563c129d6c2f8e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationGlobalSetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c169784559a5537613e9998466f48abef7b02adda7cf06446cddfa48e66c09f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__291da34fd0264438455c9bc05100b3c77bf5c08086bcf53a2599bd52da81bcd8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22dcb6cd2322d64258b77cb7ad97a911ee4d4bc756873bf06c0b27e50d44b33d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSet]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSet]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSet]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b242bf0c85598522fa67d65a0650049bedf59b5e2b45f761b2111852a05d0e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationGlobalSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dbddb62d7379d6ec8164a43aacd6fa04440cd26e89ea6039465fcee02da06eeb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putRule")
    def put_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationGlobalSetRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2357782e55e3edea8f1ede646b7d6e83af2f13be8a4c278d1699891c8418dbe1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRule", [value]))

    @jsii.member(jsii_name="resetRule")
    def reset_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRule", []))

    @builtins.property
    @jsii.member(jsii_name="rule")
    def rule(self) -> "EventOrchestrationGlobalSetRuleList":
        return typing.cast("EventOrchestrationGlobalSetRuleList", jsii.get(self, "rule"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleInput")
    def rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalSetRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalSetRule"]]], jsii.get(self, "ruleInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b2020bfde0f3cbd17069d18280dfbe8f45cd27d62ba302cce93e0f6405dc1af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalSet]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalSet]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalSet]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1118d83b6b95bdad0f5c7886e80d44c0cc10efd60424d19cc48127c92b5f376f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalSetRule",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "condition": "condition",
        "disabled": "disabled",
        "label": "label",
    },
)
class EventOrchestrationGlobalSetRule:
    def __init__(
        self,
        *,
        actions: typing.Union["EventOrchestrationGlobalSetRuleActions", typing.Dict[builtins.str, typing.Any]],
        condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationGlobalSetRuleCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        label: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#actions EventOrchestrationGlobal#actions}
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#condition EventOrchestrationGlobal#condition}
        :param disabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#disabled EventOrchestrationGlobal#disabled}.
        :param label: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#label EventOrchestrationGlobal#label}.
        '''
        if isinstance(actions, dict):
            actions = EventOrchestrationGlobalSetRuleActions(**actions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6162c0a8b14100ed84de5ebafbd377cdd9354ad5e44008e374977df7e59a651f)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument disabled", value=disabled, expected_type=type_hints["disabled"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
        }
        if condition is not None:
            self._values["condition"] = condition
        if disabled is not None:
            self._values["disabled"] = disabled
        if label is not None:
            self._values["label"] = label

    @builtins.property
    def actions(self) -> "EventOrchestrationGlobalSetRuleActions":
        '''actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#actions EventOrchestrationGlobal#actions}
        '''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast("EventOrchestrationGlobalSetRuleActions", result)

    @builtins.property
    def condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalSetRuleCondition"]]]:
        '''condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#condition EventOrchestrationGlobal#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalSetRuleCondition"]]], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#disabled EventOrchestrationGlobal#disabled}.'''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#label EventOrchestrationGlobal#label}.'''
        result = self._values.get("label")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationGlobalSetRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalSetRuleActions",
    jsii_struct_bases=[],
    name_mapping={
        "annotate": "annotate",
        "automation_action": "automationAction",
        "drop_event": "dropEvent",
        "escalation_policy": "escalationPolicy",
        "event_action": "eventAction",
        "extraction": "extraction",
        "incident_custom_field_update": "incidentCustomFieldUpdate",
        "priority": "priority",
        "route_to": "routeTo",
        "severity": "severity",
        "suppress": "suppress",
        "suspend": "suspend",
        "variable": "variable",
    },
)
class EventOrchestrationGlobalSetRuleActions:
    def __init__(
        self,
        *,
        annotate: typing.Optional[builtins.str] = None,
        automation_action: typing.Optional[typing.Union["EventOrchestrationGlobalSetRuleActionsAutomationAction", typing.Dict[builtins.str, typing.Any]]] = None,
        drop_event: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        escalation_policy: typing.Optional[builtins.str] = None,
        event_action: typing.Optional[builtins.str] = None,
        extraction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationGlobalSetRuleActionsExtraction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        incident_custom_field_update: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationGlobalSetRuleActionsIncidentCustomFieldUpdate", typing.Dict[builtins.str, typing.Any]]]]] = None,
        priority: typing.Optional[builtins.str] = None,
        route_to: typing.Optional[builtins.str] = None,
        severity: typing.Optional[builtins.str] = None,
        suppress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        suspend: typing.Optional[jsii.Number] = None,
        variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationGlobalSetRuleActionsVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param annotate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#annotate EventOrchestrationGlobal#annotate}.
        :param automation_action: automation_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#automation_action EventOrchestrationGlobal#automation_action}
        :param drop_event: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#drop_event EventOrchestrationGlobal#drop_event}.
        :param escalation_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#escalation_policy EventOrchestrationGlobal#escalation_policy}.
        :param event_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#event_action EventOrchestrationGlobal#event_action}.
        :param extraction: extraction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#extraction EventOrchestrationGlobal#extraction}
        :param incident_custom_field_update: incident_custom_field_update block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#incident_custom_field_update EventOrchestrationGlobal#incident_custom_field_update}
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#priority EventOrchestrationGlobal#priority}.
        :param route_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#route_to EventOrchestrationGlobal#route_to}.
        :param severity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#severity EventOrchestrationGlobal#severity}.
        :param suppress: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#suppress EventOrchestrationGlobal#suppress}.
        :param suspend: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#suspend EventOrchestrationGlobal#suspend}.
        :param variable: variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#variable EventOrchestrationGlobal#variable}
        '''
        if isinstance(automation_action, dict):
            automation_action = EventOrchestrationGlobalSetRuleActionsAutomationAction(**automation_action)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ab71f345d2ef6d64b052b7646b40dfe5304ce125093203f5b34465d01138d37)
            check_type(argname="argument annotate", value=annotate, expected_type=type_hints["annotate"])
            check_type(argname="argument automation_action", value=automation_action, expected_type=type_hints["automation_action"])
            check_type(argname="argument drop_event", value=drop_event, expected_type=type_hints["drop_event"])
            check_type(argname="argument escalation_policy", value=escalation_policy, expected_type=type_hints["escalation_policy"])
            check_type(argname="argument event_action", value=event_action, expected_type=type_hints["event_action"])
            check_type(argname="argument extraction", value=extraction, expected_type=type_hints["extraction"])
            check_type(argname="argument incident_custom_field_update", value=incident_custom_field_update, expected_type=type_hints["incident_custom_field_update"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument route_to", value=route_to, expected_type=type_hints["route_to"])
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
            check_type(argname="argument suppress", value=suppress, expected_type=type_hints["suppress"])
            check_type(argname="argument suspend", value=suspend, expected_type=type_hints["suspend"])
            check_type(argname="argument variable", value=variable, expected_type=type_hints["variable"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if annotate is not None:
            self._values["annotate"] = annotate
        if automation_action is not None:
            self._values["automation_action"] = automation_action
        if drop_event is not None:
            self._values["drop_event"] = drop_event
        if escalation_policy is not None:
            self._values["escalation_policy"] = escalation_policy
        if event_action is not None:
            self._values["event_action"] = event_action
        if extraction is not None:
            self._values["extraction"] = extraction
        if incident_custom_field_update is not None:
            self._values["incident_custom_field_update"] = incident_custom_field_update
        if priority is not None:
            self._values["priority"] = priority
        if route_to is not None:
            self._values["route_to"] = route_to
        if severity is not None:
            self._values["severity"] = severity
        if suppress is not None:
            self._values["suppress"] = suppress
        if suspend is not None:
            self._values["suspend"] = suspend
        if variable is not None:
            self._values["variable"] = variable

    @builtins.property
    def annotate(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#annotate EventOrchestrationGlobal#annotate}.'''
        result = self._values.get("annotate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def automation_action(
        self,
    ) -> typing.Optional["EventOrchestrationGlobalSetRuleActionsAutomationAction"]:
        '''automation_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#automation_action EventOrchestrationGlobal#automation_action}
        '''
        result = self._values.get("automation_action")
        return typing.cast(typing.Optional["EventOrchestrationGlobalSetRuleActionsAutomationAction"], result)

    @builtins.property
    def drop_event(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#drop_event EventOrchestrationGlobal#drop_event}.'''
        result = self._values.get("drop_event")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def escalation_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#escalation_policy EventOrchestrationGlobal#escalation_policy}.'''
        result = self._values.get("escalation_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#event_action EventOrchestrationGlobal#event_action}.'''
        result = self._values.get("event_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extraction(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalSetRuleActionsExtraction"]]]:
        '''extraction block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#extraction EventOrchestrationGlobal#extraction}
        '''
        result = self._values.get("extraction")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalSetRuleActionsExtraction"]]], result)

    @builtins.property
    def incident_custom_field_update(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalSetRuleActionsIncidentCustomFieldUpdate"]]]:
        '''incident_custom_field_update block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#incident_custom_field_update EventOrchestrationGlobal#incident_custom_field_update}
        '''
        result = self._values.get("incident_custom_field_update")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalSetRuleActionsIncidentCustomFieldUpdate"]]], result)

    @builtins.property
    def priority(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#priority EventOrchestrationGlobal#priority}.'''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def route_to(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#route_to EventOrchestrationGlobal#route_to}.'''
        result = self._values.get("route_to")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def severity(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#severity EventOrchestrationGlobal#severity}.'''
        result = self._values.get("severity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suppress(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#suppress EventOrchestrationGlobal#suppress}.'''
        result = self._values.get("suppress")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def suspend(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#suspend EventOrchestrationGlobal#suspend}.'''
        result = self._values.get("suspend")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def variable(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalSetRuleActionsVariable"]]]:
        '''variable block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#variable EventOrchestrationGlobal#variable}
        '''
        result = self._values.get("variable")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalSetRuleActionsVariable"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationGlobalSetRuleActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalSetRuleActionsAutomationAction",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "url": "url",
        "auto_send": "autoSend",
        "header": "header",
        "parameter": "parameter",
        "trigger_types": "triggerTypes",
    },
)
class EventOrchestrationGlobalSetRuleActionsAutomationAction:
    def __init__(
        self,
        *,
        name: builtins.str,
        url: builtins.str,
        auto_send: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationGlobalSetRuleActionsAutomationActionHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationGlobalSetRuleActionsAutomationActionParameter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        trigger_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#name EventOrchestrationGlobal#name}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#url EventOrchestrationGlobal#url}.
        :param auto_send: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#auto_send EventOrchestrationGlobal#auto_send}.
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#header EventOrchestrationGlobal#header}
        :param parameter: parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#parameter EventOrchestrationGlobal#parameter}
        :param trigger_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#trigger_types EventOrchestrationGlobal#trigger_types}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__723d2a0275861d95017a3481ff6564df72221d81439af26b87052de7905dd603)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument auto_send", value=auto_send, expected_type=type_hints["auto_send"])
            check_type(argname="argument header", value=header, expected_type=type_hints["header"])
            check_type(argname="argument parameter", value=parameter, expected_type=type_hints["parameter"])
            check_type(argname="argument trigger_types", value=trigger_types, expected_type=type_hints["trigger_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "url": url,
        }
        if auto_send is not None:
            self._values["auto_send"] = auto_send
        if header is not None:
            self._values["header"] = header
        if parameter is not None:
            self._values["parameter"] = parameter
        if trigger_types is not None:
            self._values["trigger_types"] = trigger_types

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#name EventOrchestrationGlobal#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#url EventOrchestrationGlobal#url}.'''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_send(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#auto_send EventOrchestrationGlobal#auto_send}.'''
        result = self._values.get("auto_send")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalSetRuleActionsAutomationActionHeader"]]]:
        '''header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#header EventOrchestrationGlobal#header}
        '''
        result = self._values.get("header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalSetRuleActionsAutomationActionHeader"]]], result)

    @builtins.property
    def parameter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalSetRuleActionsAutomationActionParameter"]]]:
        '''parameter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#parameter EventOrchestrationGlobal#parameter}
        '''
        result = self._values.get("parameter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalSetRuleActionsAutomationActionParameter"]]], result)

    @builtins.property
    def trigger_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#trigger_types EventOrchestrationGlobal#trigger_types}.'''
        result = self._values.get("trigger_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationGlobalSetRuleActionsAutomationAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalSetRuleActionsAutomationActionHeader",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class EventOrchestrationGlobalSetRuleActionsAutomationActionHeader:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#key EventOrchestrationGlobal#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#value EventOrchestrationGlobal#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__541694733fc98eb5135d9d17e596b4cab74578defc3bdbfef6a43a56159f1877)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#key EventOrchestrationGlobal#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#value EventOrchestrationGlobal#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationGlobalSetRuleActionsAutomationActionHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationGlobalSetRuleActionsAutomationActionHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalSetRuleActionsAutomationActionHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c192ed6947c9d47e351e52e7ac3770794b70ad224677b9ae991b40dd8d239d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventOrchestrationGlobalSetRuleActionsAutomationActionHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0967f7a952367da13fc49f57cc02b82f99a43d7f55888f21340a382d446a34bf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationGlobalSetRuleActionsAutomationActionHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f133093d0034db49adecd17de51776d3fa5afcf6026fefac308a6ddd7bb4c06)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e0fe6676e50e6632fd188d495c5e9ee562ce950012daba4586d7bac8260267ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c1caaefa99448a43beea0b451bcf507bd834cf6ca404377537207deb0fee1e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRuleActionsAutomationActionHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRuleActionsAutomationActionHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRuleActionsAutomationActionHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af460587831495a396c824f55ab2eb0d34c77269a6faf1a0457037d43536f7ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationGlobalSetRuleActionsAutomationActionHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalSetRuleActionsAutomationActionHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__925dabb77b721dd39d20aa0b71e44a5bde862a8d75b3be9c94cc4f02b20e527d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eb4db829269dc1e66c774e3d9505aeab6d4ba8c9043a920d5b9e140b64e24b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cd6ccf6bfc824d4253a1f4b01f87367c52fccfde1c5eef20c3ae5687016b46d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalSetRuleActionsAutomationActionHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalSetRuleActionsAutomationActionHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalSetRuleActionsAutomationActionHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__145d57db160504b02473bf43cc68d40b33f31b9c11718a3e41790c9e37722de2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationGlobalSetRuleActionsAutomationActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalSetRuleActionsAutomationActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e9ee2fd010325c91ed5b38e1b9227da710f0a65bc9f4f43a9f41dfcfd0d90961)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHeader")
    def put_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalSetRuleActionsAutomationActionHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8fed2dd79ebe7c44288433f1c89805de4fdf28eaeeeb4585129718756806cab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeader", [value]))

    @jsii.member(jsii_name="putParameter")
    def put_parameter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationGlobalSetRuleActionsAutomationActionParameter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__250838c548738d341f27272f626a1c969ab391291eaf8598c110d30cd9432c63)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putParameter", [value]))

    @jsii.member(jsii_name="resetAutoSend")
    def reset_auto_send(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutoSend", []))

    @jsii.member(jsii_name="resetHeader")
    def reset_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHeader", []))

    @jsii.member(jsii_name="resetParameter")
    def reset_parameter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameter", []))

    @jsii.member(jsii_name="resetTriggerTypes")
    def reset_trigger_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTriggerTypes", []))

    @builtins.property
    @jsii.member(jsii_name="header")
    def header(
        self,
    ) -> EventOrchestrationGlobalSetRuleActionsAutomationActionHeaderList:
        return typing.cast(EventOrchestrationGlobalSetRuleActionsAutomationActionHeaderList, jsii.get(self, "header"))

    @builtins.property
    @jsii.member(jsii_name="parameter")
    def parameter(
        self,
    ) -> "EventOrchestrationGlobalSetRuleActionsAutomationActionParameterList":
        return typing.cast("EventOrchestrationGlobalSetRuleActionsAutomationActionParameterList", jsii.get(self, "parameter"))

    @builtins.property
    @jsii.member(jsii_name="autoSendInput")
    def auto_send_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "autoSendInput"))

    @builtins.property
    @jsii.member(jsii_name="headerInput")
    def header_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRuleActionsAutomationActionHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRuleActionsAutomationActionHeader]]], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parameterInput")
    def parameter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalSetRuleActionsAutomationActionParameter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalSetRuleActionsAutomationActionParameter"]]], jsii.get(self, "parameterInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerTypesInput")
    def trigger_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "triggerTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="urlInput")
    def url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlInput"))

    @builtins.property
    @jsii.member(jsii_name="autoSend")
    def auto_send(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "autoSend"))

    @auto_send.setter
    def auto_send(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8edde0ab8976374e86986f9d9c6015d5024ec409b23f39c2203ad869fc479e3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoSend", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4db32bd70cbe1f69ff175d4ded111cf35f7722cdb1c2ef820ca337aafb86d677)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="triggerTypes")
    def trigger_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "triggerTypes"))

    @trigger_types.setter
    def trigger_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d30e7d51365553fc2bd59007e71a9b0b477e0b32254869e86c64eece0e8ebf53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__128d57b6052abd22efbffefd58be83b2bfa25138daac6e49494621d1980bd0c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventOrchestrationGlobalSetRuleActionsAutomationAction]:
        return typing.cast(typing.Optional[EventOrchestrationGlobalSetRuleActionsAutomationAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventOrchestrationGlobalSetRuleActionsAutomationAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5827bb41de6094284ebd00502f07adf431f1c369b15b592717f41496e9a44493)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalSetRuleActionsAutomationActionParameter",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class EventOrchestrationGlobalSetRuleActionsAutomationActionParameter:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#key EventOrchestrationGlobal#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#value EventOrchestrationGlobal#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__441d5eb0cfb56ea15348461de8ab1eeeb7ba29435b112be08856224068edc133)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#key EventOrchestrationGlobal#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#value EventOrchestrationGlobal#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationGlobalSetRuleActionsAutomationActionParameter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationGlobalSetRuleActionsAutomationActionParameterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalSetRuleActionsAutomationActionParameterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cbc0ad9f4ed1c01cace41981a42f87453b54e6ede03dfbbdcb846e4adfeaa055)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventOrchestrationGlobalSetRuleActionsAutomationActionParameterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__611bc51855f9f23f25269c0ee651e3497b2b6afc684a9bc8cf16f183a017ae72)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationGlobalSetRuleActionsAutomationActionParameterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bff9ba9147a3282fa150f16cd0f425a1817ea00ef125effccb6bf12a4f45f13)
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
            type_hints = typing.get_type_hints(_typecheckingstub__34e4d04292a73fcb461216d1a6ffafb9f78bfbd7af2f12eaf4f169d3fc28ab51)
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
            type_hints = typing.get_type_hints(_typecheckingstub__05e8eb71d200a80cef049dc89b20d2eb1230bb1f137477ef110c0e901f5a0a17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRuleActionsAutomationActionParameter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRuleActionsAutomationActionParameter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRuleActionsAutomationActionParameter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bf35f3819ede69728004519885f3dfd36d947fa92ffb94aa3a0bda8b1b6fc62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationGlobalSetRuleActionsAutomationActionParameterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalSetRuleActionsAutomationActionParameterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5730a11890c169061358eff6c781fda984a09f08bf89fd41c36e38eeef5b132f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="keyInput")
    def key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="key")
    def key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "key"))

    @key.setter
    def key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28b0f738730c83b224d46641a71b55137a0e4f05f26c7b071c756b12bd55e6d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa357d5077c52b74b01078fbb36709cc193eb2a94ac2a72a135b79996483caac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalSetRuleActionsAutomationActionParameter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalSetRuleActionsAutomationActionParameter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalSetRuleActionsAutomationActionParameter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41298003ac6f0a8c2bac6db562d1864fdc0898b9c171bb77651f3482c1a629b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalSetRuleActionsExtraction",
    jsii_struct_bases=[],
    name_mapping={
        "target": "target",
        "regex": "regex",
        "source": "source",
        "template": "template",
    },
)
class EventOrchestrationGlobalSetRuleActionsExtraction:
    def __init__(
        self,
        *,
        target: builtins.str,
        regex: typing.Optional[builtins.str] = None,
        source: typing.Optional[builtins.str] = None,
        template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#target EventOrchestrationGlobal#target}.
        :param regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#regex EventOrchestrationGlobal#regex}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#source EventOrchestrationGlobal#source}.
        :param template: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#template EventOrchestrationGlobal#template}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b92aecb9ded69cbe0d91dde0c5680d12062c234b53c0fd848e59d4dba288176)
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target": target,
        }
        if regex is not None:
            self._values["regex"] = regex
        if source is not None:
            self._values["source"] = source
        if template is not None:
            self._values["template"] = template

    @builtins.property
    def target(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#target EventOrchestrationGlobal#target}.'''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def regex(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#regex EventOrchestrationGlobal#regex}.'''
        result = self._values.get("regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#source EventOrchestrationGlobal#source}.'''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#template EventOrchestrationGlobal#template}.'''
        result = self._values.get("template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationGlobalSetRuleActionsExtraction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationGlobalSetRuleActionsExtractionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalSetRuleActionsExtractionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7df0b35ddb8cf3c60f350bd50085c3615f598c5b08a4406f32697a7d02acafaf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventOrchestrationGlobalSetRuleActionsExtractionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5be2597ac121c396762d3e6759cd18614ecfd85e9d3ce6fa46819068f29924fd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationGlobalSetRuleActionsExtractionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__837596d1e2c3f170b469bc82d4c1c847795abf8654438a9e2c05077d982bd35c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f469f04154a2b221b69d2c39f53b7786912974cb586d0bd90a235a5b625f0f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__73b641091fa0d3cae37eee82d453712bb2493e6c709f5976277a30fb04f94c8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRuleActionsExtraction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRuleActionsExtraction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRuleActionsExtraction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__696faca3260e3b28834272d395095c80296de069385bf100fbc429c0db2432fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationGlobalSetRuleActionsExtractionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalSetRuleActionsExtractionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b35a57eeace5a2f5b909a9acbf477e24e9ea33d13ad9b46800b0928ef01b22dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0437a7bc7f089843742af301c2567a927c49ebf790ce9acc0dd622810c704e41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51eefd439060c577d93cf503b4f40e50bbf21a623c047b06c4349f288f885d08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__029062fabc2820396a7ab87918460d0ac2fb6418ace5d2fb621e12fd4e8168c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="template")
    def template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "template"))

    @template.setter
    def template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8903ae6e0334c57a649d9a4df52e53452e3f53d3a44f0880953f2b9eec172d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "template", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalSetRuleActionsExtraction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalSetRuleActionsExtraction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalSetRuleActionsExtraction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ba9819ab3723bbb9e6fb97c760af64343f85d868ec8832f5da0a5754100c76c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalSetRuleActionsIncidentCustomFieldUpdate",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "value": "value"},
)
class EventOrchestrationGlobalSetRuleActionsIncidentCustomFieldUpdate:
    def __init__(self, *, id: builtins.str, value: builtins.str) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#id EventOrchestrationGlobal#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#value EventOrchestrationGlobal#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e428808da2e632206477fcba5c539e87b77ccf79dd1d8e26b1d7140d8295e18c)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "value": value,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#id EventOrchestrationGlobal#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#value EventOrchestrationGlobal#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationGlobalSetRuleActionsIncidentCustomFieldUpdate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationGlobalSetRuleActionsIncidentCustomFieldUpdateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalSetRuleActionsIncidentCustomFieldUpdateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__65741d58483630bd5ae6d6fa60ac9c354e3b90844703df1b159c05a450d01eb6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventOrchestrationGlobalSetRuleActionsIncidentCustomFieldUpdateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dcde936ae60c7134de199d38135ddea2889923e0e46fb2c4cc58e9b563f57d5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationGlobalSetRuleActionsIncidentCustomFieldUpdateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0b4766b52d3130f9f9fdddf3dce6353c1b767ff0a8e2715c9930119f937ff12)
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
            type_hints = typing.get_type_hints(_typecheckingstub__930ac3691abd743f27c6833b2459db4ace15441937c965312c1b47435789eae9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b694e1b681edf4e61529421aa8d78998622b08ca166e77913a71e4f1c1de3348)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRuleActionsIncidentCustomFieldUpdate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRuleActionsIncidentCustomFieldUpdate]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRuleActionsIncidentCustomFieldUpdate]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c00c8d089978af43b136c54976ede7592c8b84158d223d1cf4174329933d6f80)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationGlobalSetRuleActionsIncidentCustomFieldUpdateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalSetRuleActionsIncidentCustomFieldUpdateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__35bad789610c9f1b6d33712d577d9ddeffa67d33d1d92bcad2d9febf0794f922)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44b104d3bf6b872d4cdaeaed281f7bc37d5aa6e611d802355ba97f90141d707c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b370723c78edf2fbeb99bb972acb2b303f9ba1df2ee46c95ce4afe775b311e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalSetRuleActionsIncidentCustomFieldUpdate]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalSetRuleActionsIncidentCustomFieldUpdate]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalSetRuleActionsIncidentCustomFieldUpdate]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4e9f2de32e2c5bda04162e445ca68a63d5cb5227ed59267ea8bcd79e140d245)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationGlobalSetRuleActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalSetRuleActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0f505684a751f1f088cd451fef4ec2359ee0504befdaa6c680d147d5167b352)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAutomationAction")
    def put_automation_action(
        self,
        *,
        name: builtins.str,
        url: builtins.str,
        auto_send: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalSetRuleActionsAutomationActionHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
        parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalSetRuleActionsAutomationActionParameter, typing.Dict[builtins.str, typing.Any]]]]] = None,
        trigger_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#name EventOrchestrationGlobal#name}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#url EventOrchestrationGlobal#url}.
        :param auto_send: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#auto_send EventOrchestrationGlobal#auto_send}.
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#header EventOrchestrationGlobal#header}
        :param parameter: parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#parameter EventOrchestrationGlobal#parameter}
        :param trigger_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#trigger_types EventOrchestrationGlobal#trigger_types}.
        '''
        value = EventOrchestrationGlobalSetRuleActionsAutomationAction(
            name=name,
            url=url,
            auto_send=auto_send,
            header=header,
            parameter=parameter,
            trigger_types=trigger_types,
        )

        return typing.cast(None, jsii.invoke(self, "putAutomationAction", [value]))

    @jsii.member(jsii_name="putExtraction")
    def put_extraction(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalSetRuleActionsExtraction, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4c3fd98078bd837c55eec1586e06251789ffe67f821d37a333d9cf24d33ebc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExtraction", [value]))

    @jsii.member(jsii_name="putIncidentCustomFieldUpdate")
    def put_incident_custom_field_update(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalSetRuleActionsIncidentCustomFieldUpdate, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63b7e10126ed2db187b40890838fcb94fe2d629daf8e17a2be397f7b81c93d87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIncidentCustomFieldUpdate", [value]))

    @jsii.member(jsii_name="putVariable")
    def put_variable(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationGlobalSetRuleActionsVariable", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c29635cc10b471f381e294a572a6f6ce91e120c2af223d687c38fce181fcd96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVariable", [value]))

    @jsii.member(jsii_name="resetAnnotate")
    def reset_annotate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotate", []))

    @jsii.member(jsii_name="resetAutomationAction")
    def reset_automation_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomationAction", []))

    @jsii.member(jsii_name="resetDropEvent")
    def reset_drop_event(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDropEvent", []))

    @jsii.member(jsii_name="resetEscalationPolicy")
    def reset_escalation_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEscalationPolicy", []))

    @jsii.member(jsii_name="resetEventAction")
    def reset_event_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventAction", []))

    @jsii.member(jsii_name="resetExtraction")
    def reset_extraction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtraction", []))

    @jsii.member(jsii_name="resetIncidentCustomFieldUpdate")
    def reset_incident_custom_field_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIncidentCustomFieldUpdate", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetRouteTo")
    def reset_route_to(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRouteTo", []))

    @jsii.member(jsii_name="resetSeverity")
    def reset_severity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeverity", []))

    @jsii.member(jsii_name="resetSuppress")
    def reset_suppress(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuppress", []))

    @jsii.member(jsii_name="resetSuspend")
    def reset_suspend(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSuspend", []))

    @jsii.member(jsii_name="resetVariable")
    def reset_variable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVariable", []))

    @builtins.property
    @jsii.member(jsii_name="automationAction")
    def automation_action(
        self,
    ) -> EventOrchestrationGlobalSetRuleActionsAutomationActionOutputReference:
        return typing.cast(EventOrchestrationGlobalSetRuleActionsAutomationActionOutputReference, jsii.get(self, "automationAction"))

    @builtins.property
    @jsii.member(jsii_name="extraction")
    def extraction(self) -> EventOrchestrationGlobalSetRuleActionsExtractionList:
        return typing.cast(EventOrchestrationGlobalSetRuleActionsExtractionList, jsii.get(self, "extraction"))

    @builtins.property
    @jsii.member(jsii_name="incidentCustomFieldUpdate")
    def incident_custom_field_update(
        self,
    ) -> EventOrchestrationGlobalSetRuleActionsIncidentCustomFieldUpdateList:
        return typing.cast(EventOrchestrationGlobalSetRuleActionsIncidentCustomFieldUpdateList, jsii.get(self, "incidentCustomFieldUpdate"))

    @builtins.property
    @jsii.member(jsii_name="variable")
    def variable(self) -> "EventOrchestrationGlobalSetRuleActionsVariableList":
        return typing.cast("EventOrchestrationGlobalSetRuleActionsVariableList", jsii.get(self, "variable"))

    @builtins.property
    @jsii.member(jsii_name="annotateInput")
    def annotate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "annotateInput"))

    @builtins.property
    @jsii.member(jsii_name="automationActionInput")
    def automation_action_input(
        self,
    ) -> typing.Optional[EventOrchestrationGlobalSetRuleActionsAutomationAction]:
        return typing.cast(typing.Optional[EventOrchestrationGlobalSetRuleActionsAutomationAction], jsii.get(self, "automationActionInput"))

    @builtins.property
    @jsii.member(jsii_name="dropEventInput")
    def drop_event_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "dropEventInput"))

    @builtins.property
    @jsii.member(jsii_name="escalationPolicyInput")
    def escalation_policy_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "escalationPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="eventActionInput")
    def event_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventActionInput"))

    @builtins.property
    @jsii.member(jsii_name="extractionInput")
    def extraction_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRuleActionsExtraction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRuleActionsExtraction]]], jsii.get(self, "extractionInput"))

    @builtins.property
    @jsii.member(jsii_name="incidentCustomFieldUpdateInput")
    def incident_custom_field_update_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRuleActionsIncidentCustomFieldUpdate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRuleActionsIncidentCustomFieldUpdate]]], jsii.get(self, "incidentCustomFieldUpdateInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="routeToInput")
    def route_to_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routeToInput"))

    @builtins.property
    @jsii.member(jsii_name="severityInput")
    def severity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "severityInput"))

    @builtins.property
    @jsii.member(jsii_name="suppressInput")
    def suppress_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "suppressInput"))

    @builtins.property
    @jsii.member(jsii_name="suspendInput")
    def suspend_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "suspendInput"))

    @builtins.property
    @jsii.member(jsii_name="variableInput")
    def variable_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalSetRuleActionsVariable"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationGlobalSetRuleActionsVariable"]]], jsii.get(self, "variableInput"))

    @builtins.property
    @jsii.member(jsii_name="annotate")
    def annotate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "annotate"))

    @annotate.setter
    def annotate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d24dbc69f0ae8626f57c12d98a004903d91acbc6ab30e2988434affb7ef6f35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="dropEvent")
    def drop_event(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "dropEvent"))

    @drop_event.setter
    def drop_event(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__601cc6514734204b43fefd3f9f0acfe12573580d215520898c6c84e7e32f937d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dropEvent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="escalationPolicy")
    def escalation_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "escalationPolicy"))

    @escalation_policy.setter
    def escalation_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b9f627e19c7e2bbc4f656d65f6a0e0e9d4c84b992546cca7c07f40dc121ba5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "escalationPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventAction")
    def event_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventAction"))

    @event_action.setter
    def event_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53f280b06efc381fc28389eb037650d2e41a3e7bceb2189eb70744b83d53c185)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d56aaf7872939127982b0a1459db57a9a3c56d40f84cb48b1f10f63d4f8ad324)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routeTo")
    def route_to(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routeTo"))

    @route_to.setter
    def route_to(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff8aabdd5cafe2c1381fdf6e0f85ca970a8cf002deaf4aff75568aab58914b6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeTo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "severity"))

    @severity.setter
    def severity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__069c1d1d09d0d0f1e790d2a933abe557749f50d349d4507ebc0187423c11b56f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "severity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suppress")
    def suppress(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "suppress"))

    @suppress.setter
    def suppress(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__130054da170e2bc35ce44182f7120e297daec8bb6ba726fe72f9cf1370f01ca5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suppress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suspend")
    def suspend(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "suspend"))

    @suspend.setter
    def suspend(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef9da27c9c082c023dab8929c2c6397cb8d73de4500624a967ef6d577cbc5f19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suspend", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EventOrchestrationGlobalSetRuleActions]:
        return typing.cast(typing.Optional[EventOrchestrationGlobalSetRuleActions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventOrchestrationGlobalSetRuleActions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a6ff2655bd68fa4369d7665fa46f2adacb6d7d0a9d62c458595c0b7b8601acc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalSetRuleActionsVariable",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "path": "path", "type": "type", "value": "value"},
)
class EventOrchestrationGlobalSetRuleActionsVariable:
    def __init__(
        self,
        *,
        name: builtins.str,
        path: builtins.str,
        type: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#name EventOrchestrationGlobal#name}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#path EventOrchestrationGlobal#path}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#type EventOrchestrationGlobal#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#value EventOrchestrationGlobal#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9975e599b66082aa161a92a72e86a6da50b9cbaa7b3cedfc9ff7f3bf8156c974)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "path": path,
            "type": type,
            "value": value,
        }

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#name EventOrchestrationGlobal#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#path EventOrchestrationGlobal#path}.'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#type EventOrchestrationGlobal#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#value EventOrchestrationGlobal#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationGlobalSetRuleActionsVariable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationGlobalSetRuleActionsVariableList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalSetRuleActionsVariableList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2b60929c58b2b29387b62c066843f8f79422a9a9e441f975868ee45c89bfbed)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventOrchestrationGlobalSetRuleActionsVariableOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__827e44705a90142712e9755906a7f8452931ba60544afd3ba95616aac82b1dd0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationGlobalSetRuleActionsVariableOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69bafd1a8967651cb8e3d4b4c466218dcdfd979f0c35485ec725afdbd932e7c9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__740007e257f8fd817abb8d6451d53ce3a4712fdf97d8f408db6733b484f0d53c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__595210d6d5a25430555b0a3b26f8305c1a54b194f9c2878eeb6cf98c70e31ac4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRuleActionsVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRuleActionsVariable]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRuleActionsVariable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__448d3ff99277d996053ddb0b27e14b2cb27c8570bec9c59e876dfa7286979151)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationGlobalSetRuleActionsVariableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalSetRuleActionsVariableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff5f5e5e5e57b371b46435a16ba1cb13e0c9f8aa497317699eb44881a4d428e1)
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
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ad0ff8d99247b3b89d11a280572243be649cabaec328faf3f9b3b425722b0ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2ac9a1414f529828f4a11e8960e4417a1ec30022295baaa70450dc31133cf30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4da0da39dae90dce7b70e3c5a2cbc8191b733bf6567c157a11eeea3594cabb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ebdf3716fad58785ca67931c467bbebf67b48bd4f924148f44f24f227afd1cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalSetRuleActionsVariable]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalSetRuleActionsVariable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalSetRuleActionsVariable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47afde6482cd6808fcc44fea3a9c4219d74fb35d882ce622b9e4d392cf51d792)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalSetRuleCondition",
    jsii_struct_bases=[],
    name_mapping={"expression": "expression"},
)
class EventOrchestrationGlobalSetRuleCondition:
    def __init__(self, *, expression: builtins.str) -> None:
        '''
        :param expression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#expression EventOrchestrationGlobal#expression}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__195af8a9d56ef9e383b66a3a3513a01f6bfdedfa0d4b13150d22558077655b02)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expression": expression,
        }

    @builtins.property
    def expression(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#expression EventOrchestrationGlobal#expression}.'''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationGlobalSetRuleCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationGlobalSetRuleConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalSetRuleConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__402c2d75788b3e5a6716a20899a02fec0125a69523adea16ec297417b6358a5b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventOrchestrationGlobalSetRuleConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a17c2016eec825744ecc1ed8ff8841b53fa59d61a5b1044b0e53af6015166939)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationGlobalSetRuleConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__348e382a0150f8d2c73c54ab7ba42ad9d59b5a87223eff7dbe833f5c0eb4c9d5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__16087c6ce61dfa3cf72dec62449deeb358b24ca059827efc1e94b1fd5d9ff0de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1fbd88fefc006d31ef0fb55df701cc47fcaeed9b72c207ab4f98443430d83132)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRuleCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRuleCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRuleCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__325fb874a8cd0e638ed8a9045bc87a6b70200be0b54b1e3841a4b46f9bd5ef7d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationGlobalSetRuleConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalSetRuleConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__14140ba5dcaf89645318e32df911b3f2d7dd4d8631c2130f954397e5a287a17f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="expressionInput")
    def expression_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "expressionInput"))

    @builtins.property
    @jsii.member(jsii_name="expression")
    def expression(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "expression"))

    @expression.setter
    def expression(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a5eed38e635f1bb6f63df5b6e4d5e39765d5bd58aa6406a06b99018b68ba4cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalSetRuleCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalSetRuleCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalSetRuleCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6509e74762f5df0f7c008f9d6ac12b14743918e5009915e3f684fe0c0d71f8ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationGlobalSetRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalSetRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__01fd680a6b08cecf2290431bd0e32b0a7b085ea1438a166ecd0ca40288dc1209)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventOrchestrationGlobalSetRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b307780ebe288f563a1599b030711a21e648ce852de1501e05c69fde2eaeebe2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationGlobalSetRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__304f6b49d2c7bf94b9cef4779f8feeca2da1efad681c98b2df2351e7bbf13b25)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8289537f8967ae9ab488de5d1347be9813cc58389b4bdcda4a14fa09cedfc86d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db685b7e936b81cdc353a88bce175fb3415aba05cbf7c1173486f36b7aac6625)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57f3e82836f9e62b0e31fcdf2e1480a4164f045de596616947ad65306281a386)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationGlobalSetRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationGlobal.EventOrchestrationGlobalSetRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3cf78bc1c1bf47c63adac534d295cd76e9965f5e8cc28b99dba5c3d49c812964)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putActions")
    def put_actions(
        self,
        *,
        annotate: typing.Optional[builtins.str] = None,
        automation_action: typing.Optional[typing.Union[EventOrchestrationGlobalSetRuleActionsAutomationAction, typing.Dict[builtins.str, typing.Any]]] = None,
        drop_event: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        escalation_policy: typing.Optional[builtins.str] = None,
        event_action: typing.Optional[builtins.str] = None,
        extraction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalSetRuleActionsExtraction, typing.Dict[builtins.str, typing.Any]]]]] = None,
        incident_custom_field_update: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalSetRuleActionsIncidentCustomFieldUpdate, typing.Dict[builtins.str, typing.Any]]]]] = None,
        priority: typing.Optional[builtins.str] = None,
        route_to: typing.Optional[builtins.str] = None,
        severity: typing.Optional[builtins.str] = None,
        suppress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        suspend: typing.Optional[jsii.Number] = None,
        variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalSetRuleActionsVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param annotate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#annotate EventOrchestrationGlobal#annotate}.
        :param automation_action: automation_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#automation_action EventOrchestrationGlobal#automation_action}
        :param drop_event: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#drop_event EventOrchestrationGlobal#drop_event}.
        :param escalation_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#escalation_policy EventOrchestrationGlobal#escalation_policy}.
        :param event_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#event_action EventOrchestrationGlobal#event_action}.
        :param extraction: extraction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#extraction EventOrchestrationGlobal#extraction}
        :param incident_custom_field_update: incident_custom_field_update block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#incident_custom_field_update EventOrchestrationGlobal#incident_custom_field_update}
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#priority EventOrchestrationGlobal#priority}.
        :param route_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#route_to EventOrchestrationGlobal#route_to}.
        :param severity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#severity EventOrchestrationGlobal#severity}.
        :param suppress: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#suppress EventOrchestrationGlobal#suppress}.
        :param suspend: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#suspend EventOrchestrationGlobal#suspend}.
        :param variable: variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_global#variable EventOrchestrationGlobal#variable}
        '''
        value = EventOrchestrationGlobalSetRuleActions(
            annotate=annotate,
            automation_action=automation_action,
            drop_event=drop_event,
            escalation_policy=escalation_policy,
            event_action=event_action,
            extraction=extraction,
            incident_custom_field_update=incident_custom_field_update,
            priority=priority,
            route_to=route_to,
            severity=severity,
            suppress=suppress,
            suspend=suspend,
            variable=variable,
        )

        return typing.cast(None, jsii.invoke(self, "putActions", [value]))

    @jsii.member(jsii_name="putCondition")
    def put_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalSetRuleCondition, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4df362519df843c8738df1bf088879b04a1d13a3d3e531e41e3a47e2018154a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putCondition", [value]))

    @jsii.member(jsii_name="resetCondition")
    def reset_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCondition", []))

    @jsii.member(jsii_name="resetDisabled")
    def reset_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisabled", []))

    @jsii.member(jsii_name="resetLabel")
    def reset_label(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLabel", []))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> EventOrchestrationGlobalSetRuleActionsOutputReference:
        return typing.cast(EventOrchestrationGlobalSetRuleActionsOutputReference, jsii.get(self, "actions"))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> EventOrchestrationGlobalSetRuleConditionList:
        return typing.cast(EventOrchestrationGlobalSetRuleConditionList, jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(self) -> typing.Optional[EventOrchestrationGlobalSetRuleActions]:
        return typing.cast(typing.Optional[EventOrchestrationGlobalSetRuleActions], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRuleCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRuleCondition]]], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="disabledInput")
    def disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disabledInput"))

    @builtins.property
    @jsii.member(jsii_name="labelInput")
    def label_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "labelInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__8490c88e79aa6729ada8487946e8b4c5a110e3ecfb7d96480d75f4926f72746f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "label"))

    @label.setter
    def label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7823141159a2eb2fa54c0466803b505a53ddfbb1c7c188fefd6591bf3653cbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "label", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalSetRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalSetRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalSetRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9b1f459869b78a8201cfc8e6f27b5dc96a68998e96fe160e1153f6335de8086)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "EventOrchestrationGlobal",
    "EventOrchestrationGlobalCatchAll",
    "EventOrchestrationGlobalCatchAllActions",
    "EventOrchestrationGlobalCatchAllActionsAutomationAction",
    "EventOrchestrationGlobalCatchAllActionsAutomationActionHeader",
    "EventOrchestrationGlobalCatchAllActionsAutomationActionHeaderList",
    "EventOrchestrationGlobalCatchAllActionsAutomationActionHeaderOutputReference",
    "EventOrchestrationGlobalCatchAllActionsAutomationActionOutputReference",
    "EventOrchestrationGlobalCatchAllActionsAutomationActionParameter",
    "EventOrchestrationGlobalCatchAllActionsAutomationActionParameterList",
    "EventOrchestrationGlobalCatchAllActionsAutomationActionParameterOutputReference",
    "EventOrchestrationGlobalCatchAllActionsExtraction",
    "EventOrchestrationGlobalCatchAllActionsExtractionList",
    "EventOrchestrationGlobalCatchAllActionsExtractionOutputReference",
    "EventOrchestrationGlobalCatchAllActionsIncidentCustomFieldUpdate",
    "EventOrchestrationGlobalCatchAllActionsIncidentCustomFieldUpdateList",
    "EventOrchestrationGlobalCatchAllActionsIncidentCustomFieldUpdateOutputReference",
    "EventOrchestrationGlobalCatchAllActionsOutputReference",
    "EventOrchestrationGlobalCatchAllActionsVariable",
    "EventOrchestrationGlobalCatchAllActionsVariableList",
    "EventOrchestrationGlobalCatchAllActionsVariableOutputReference",
    "EventOrchestrationGlobalCatchAllOutputReference",
    "EventOrchestrationGlobalConfig",
    "EventOrchestrationGlobalSet",
    "EventOrchestrationGlobalSetList",
    "EventOrchestrationGlobalSetOutputReference",
    "EventOrchestrationGlobalSetRule",
    "EventOrchestrationGlobalSetRuleActions",
    "EventOrchestrationGlobalSetRuleActionsAutomationAction",
    "EventOrchestrationGlobalSetRuleActionsAutomationActionHeader",
    "EventOrchestrationGlobalSetRuleActionsAutomationActionHeaderList",
    "EventOrchestrationGlobalSetRuleActionsAutomationActionHeaderOutputReference",
    "EventOrchestrationGlobalSetRuleActionsAutomationActionOutputReference",
    "EventOrchestrationGlobalSetRuleActionsAutomationActionParameter",
    "EventOrchestrationGlobalSetRuleActionsAutomationActionParameterList",
    "EventOrchestrationGlobalSetRuleActionsAutomationActionParameterOutputReference",
    "EventOrchestrationGlobalSetRuleActionsExtraction",
    "EventOrchestrationGlobalSetRuleActionsExtractionList",
    "EventOrchestrationGlobalSetRuleActionsExtractionOutputReference",
    "EventOrchestrationGlobalSetRuleActionsIncidentCustomFieldUpdate",
    "EventOrchestrationGlobalSetRuleActionsIncidentCustomFieldUpdateList",
    "EventOrchestrationGlobalSetRuleActionsIncidentCustomFieldUpdateOutputReference",
    "EventOrchestrationGlobalSetRuleActionsOutputReference",
    "EventOrchestrationGlobalSetRuleActionsVariable",
    "EventOrchestrationGlobalSetRuleActionsVariableList",
    "EventOrchestrationGlobalSetRuleActionsVariableOutputReference",
    "EventOrchestrationGlobalSetRuleCondition",
    "EventOrchestrationGlobalSetRuleConditionList",
    "EventOrchestrationGlobalSetRuleConditionOutputReference",
    "EventOrchestrationGlobalSetRuleList",
    "EventOrchestrationGlobalSetRuleOutputReference",
]

publication.publish()

def _typecheckingstub__7898293233ae0a207d81241c85b2c654cea3a012503a5e667a77a16de61b9f93(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    catch_all: typing.Union[EventOrchestrationGlobalCatchAll, typing.Dict[builtins.str, typing.Any]],
    event_orchestration: builtins.str,
    set: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalSet, typing.Dict[builtins.str, typing.Any]]]],
    id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__564730dbb66f292534c835172ee33821db25f29aacb25b215967b4b679c8956d(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__458f834b39f750cb2789281a8affa937376c2bdba9048edccd8911e017d439f1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalSet, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07c2ddceef1fdae2f06bb8bd9dec5394f09451ab1cd1a48d54f4571a2b8ed323(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2490bb3aa99d65cd452eb67796933377e098ec6c05e1818084d079d36ade2ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a2491ea8be6ff2bc6b23ea66c48b78e7a7c902efa56c1eeb82ba035a0ad2ce5(
    *,
    actions: typing.Union[EventOrchestrationGlobalCatchAllActions, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4583487669670db5685ff768c51203e4dba6962f41aedd2de51e461daa8dc726(
    *,
    annotate: typing.Optional[builtins.str] = None,
    automation_action: typing.Optional[typing.Union[EventOrchestrationGlobalCatchAllActionsAutomationAction, typing.Dict[builtins.str, typing.Any]]] = None,
    drop_event: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    escalation_policy: typing.Optional[builtins.str] = None,
    event_action: typing.Optional[builtins.str] = None,
    extraction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalCatchAllActionsExtraction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    incident_custom_field_update: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalCatchAllActionsIncidentCustomFieldUpdate, typing.Dict[builtins.str, typing.Any]]]]] = None,
    priority: typing.Optional[builtins.str] = None,
    route_to: typing.Optional[builtins.str] = None,
    severity: typing.Optional[builtins.str] = None,
    suppress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    suspend: typing.Optional[jsii.Number] = None,
    variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalCatchAllActionsVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3aa7554157c3709e9796076b823722a932d57649b3cd18925319019ab07058f4(
    *,
    name: builtins.str,
    url: builtins.str,
    auto_send: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalCatchAllActionsAutomationActionHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalCatchAllActionsAutomationActionParameter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    trigger_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25d6263f7f939f16ce5239b58a28df658272be7a72592fe257cae14ddceb0570(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1208d1337d1bfd14146310afe74504cd73287245531735a42a83b60cd61bef63(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7efa50933d495c44d7ddf858a7f7ae7be337ff8436d39113cf1a815b1c98dad(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e10b61e4b934f6ab3a5af8cd970677b27c96664ffc9533ba1421a59263f9c44f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b31e291f1931262649c0d2862deebe0d226983d59ee53c54193d9e0376e6eae(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c9a845064e98833a82650fc568e5816c933421446aa0827d7ae2af3f82799d6(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__344edf758ceb8c34d9528d36b9a1bdf917875b55d542f1e41545c732de974451(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalCatchAllActionsAutomationActionHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__630f0d8a58eab6009b1f2f9c8fc4b532c9964a8f9de16ddd0f86e7c5914bb5de(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14c7cb588fab74a4079e89634101323820f33887597447679f1a2a2ef0a91809(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b41ec089af1dedea8cf1af491c525eb42bcfccbf25626d972cb723504f511031(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bd6cb6ebf9c313df83f5fca371cad0e006f2f8af6c5839c6cf2418822a2e916(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalCatchAllActionsAutomationActionHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a13c3d27fcad67c7f5ddb6fe2554fd71d3d39199dd09f919549836a40d3d9c2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef3bbdb8aa45b505c4ebf7811cbbc24b02261961f0624ba324af4fcf770c8656(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalCatchAllActionsAutomationActionHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5732fd207398678ef815e164358fcef25394c5a3e67613930ae082335a4a9b6b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalCatchAllActionsAutomationActionParameter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93123901f8d1c8e6060473ccc84fd2c772d8aa5de0129f74530a2caea061df12(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cc0c0b03e9b47a858383c495e183fdce6d09ef29f9fc624d5e08904c085ccf0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1102093df97fbad28bfb226dd086ee15ef2b401b6ba31a02dc5f8a46ec749cd4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3fe80568f9189b932ce3fed13efbf5d45377faca1278ae17b140b81fc81fead(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86b3b0fdb72c30c2c124b99b7548a2b195b75eacdcaa77d02d6cb37cd67598b9(
    value: typing.Optional[EventOrchestrationGlobalCatchAllActionsAutomationAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8bf5cff7ab8d977bde6247d8b87a97cacc34598a770f783a035182d2b9a6bdf(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e972c64ef36c2c1b80aa86702bdfc44c858b30eeb73e7bbcbe32d7bd6498e099(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d608079eea039f33cfba7036550a89d17990f0d23f34141ea84163f340eb44b2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__602b0f4f46cbc4f21a8ff6e130453c4374d011b692ddc18bb05322fe6789558d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6abebbba4b7fb067fed8348b708c2c830ceec9c9d9ddf249c174c5f25e2307d6(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18e2edb00fc4428edb0ceebd74ce6efe0f7177217df23f888be271b3f3b5331c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3578eec54a1df37f1cb8f74f8ca03ee1f497bea9e2615c4409a7df633071522f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalCatchAllActionsAutomationActionParameter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08c98ccb185373e6ae09a608593faf47b89b8694091438735f4821f75fec3130(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f51f2a93221b0a64e815e529993d934be046152a0333799479c2df91b799fb85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef264dd1e30a54d2e38ba9096d6e9efcaaca3c0493265ebd8c35ebe5a08a6bdb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2424b7d1fe724d27379ab225f5d1c9a21d4e3df8b805d95f7cac4d0e7bbbaa8e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalCatchAllActionsAutomationActionParameter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c13c1c34aa2f8009fb969c1c9b9b3e863409eea556e7a2290eb65cdfb019a16(
    *,
    target: builtins.str,
    regex: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
    template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1228287f122c2b16186b4a9f43aff0557b56c596c3800bb64d93434176649604(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a736304f9f9fb74c0b6b87de68be05f758342d6709a6f354a76c3b9215c30b8(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a04378a3ad9abb3517820eec92245417bb5b9cde9c3254039cd7c9439f5537d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ffa71027a693defb82db3ccfcacc1b45793b4054c8dcd097dfb6bc58bb85b5e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c68bcd3f30c7eab876569f6a5f4f0f9244bc893e6bb2efd27dfd1732fc0e9b68(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e813b6e26c71e17ecc30e93a4e6a456d2f873c22a04106b3b68848cb1aac967e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalCatchAllActionsExtraction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62aee2e1f826d80ad26c8451b3e126d24dadbecfcdfd2d5e1eb9b498b52bad8f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9668313c6059c7e83b2c2fac06f331ac3c2cc440e0147875e3925899ebc43b31(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75da27cbea83bf3f0ae1fe7e1a2974da6a5ddd9066ef82f1257d5c28741c1277(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca32c5643225a6537b11e362f14ca9400633356e47f9d369c3b03fe2edbfacac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c17762ea1183cb1c9808ba7e2bf5c9ffdaa14e108f2eb1d17a7a3c964f2a59f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f3ab4df8ffd5d986c2ee0c6d1fae6a536161662453dc81a51678f3364ae37a4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalCatchAllActionsExtraction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b375c4b1d808a3f460f31e3cf8a8afd1bf9ad8635ace71d2f46d2ab4d18a3978(
    *,
    id: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50641c458e5848b40de67a8f5f49b6fdef1deb6adb0a62f7d6362078043ad0fd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f64bbd615fd4846255e70b39bdcd407a97566d3bf753ca15f7caec4182764ec5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c16b77ef8f35adc561de9b7df55e6c6711de5745a2ea5947004b3462048e998a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__274b408483588ace532980bca0728f27be740e3ab5f0d2fed3454f8b7f88b633(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e69ec28386f53cdade49e584a34347e09d827d0a8ecac6211635c561cfe55580(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acedca55e8af35ea8020e36b787c74428a70b33fbc5468952f7b6374a65f4970(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalCatchAllActionsIncidentCustomFieldUpdate]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97662cfc86ec1c9957f890eeba92f5f3f926f8424f4504afcca1cb800fc4d2cb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__888063f1430d54fed06cd4c2388d9b2b857a806f8528366c3fa0d5c156a175c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5ab831a90d2b9460aa1f8140f8aea287693ca91216c2343418a684cac25ef3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d78e5d3a7604e5fd795cfdfa57da28a368e9c8edab7a569b17a6d38d845f114(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalCatchAllActionsIncidentCustomFieldUpdate]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__318845c7f236a4b07df201ca2d85b3c266e5c51cf2b98641e401f14d5540b2f9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__689fdd5bf690ec9f7849e389fa6162498426a850fa96671abfed50ad68ff4d5c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalCatchAllActionsExtraction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a81465c3b3fea128babbafcea4b47c2db67947ba99baa2c2b3a52dbd387131ac(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalCatchAllActionsIncidentCustomFieldUpdate, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cc704c567dcd60574cdf347d4acef9f3ca10271e415db8e4a8cb6ea5c1cc49f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalCatchAllActionsVariable, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea055b34175fc78351f0656be7e68f3cd02099e9b8064885b416af774ae75a19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e2c15d5e25c7b8321baf795eb000c1d666e84c255aed75eff2548003038aea8(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80d8120f541dc2661444cd9200ae6d1112eb55390749f3fe4c936d695591593f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c87815e3b5b954bc10f05a59c1cf8ec640d9fd25db52cf08ff9354fbc3ac76f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0c88068184c3fc48e2c8c3df2e18349fc08457694f05d020d5172efff8d1d52(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42d0b1d770d4bd8ea7b8a724a61b03a182b5d5dcc3fa3376faabda9fb7e1afdd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7f1eb1ba9b0b04fc1a14d6936580d9d72b523c239fab6e15b3300f555638392(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d75d7d20244dcc88dbc7aaccecc5357c94cdea7eab073935cbd5f418c17e6024(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6b765e28c6e4acc79a301522cdf1f823a2c636ef91891c1f67c265fb81e5fb8(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9850dca92fc4f3051ae02f1e0502c52dd6391605108d03f307a5618264efb6a5(
    value: typing.Optional[EventOrchestrationGlobalCatchAllActions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d0aeb509773364475895da1136016fd834150cbcd65e6a3c334ee82dbaf2482(
    *,
    name: builtins.str,
    path: builtins.str,
    type: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3e78bc70f179e784abde44adbadb21be62c52b69dc3fbadd5072a8caa99809d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__241f9a5cfac66e40d53910c022fe5d7efff5986586c15ee92d1d40b1edde73f5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__063e4f107aaea9c2a2cdb6c2d720b568f08157d28d8097e2e36c6fb733c2b106(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29342ebc6a7032ded6e1dae13006e8287e5f3f27dd0ba8babc7681b91ac7f124(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb60e8f191f3271d6dcd5f50888b7fd0154b03e861e10491ce083213b3ee7882(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf34c26b3e1545dfff7a03c97b1e18f3c87af3e8bfc4a7cf42b2e02b80947fc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalCatchAllActionsVariable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5121f651247daa5059792ab323a62a05c8cac682ba42469309be0fbea3e568d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57e3a9e450bc78ced1ec9e9bd8074f1636938ccf7a911395b401ca147f40f0b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fd17d465513cb8c5e94581b22f5a9682a27d6516e3d92567b852436a2b232f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__815afa92d2a5b95632c92e6fea3617eff92eb7173e30d45eaf27e9364c8487a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72a8782b38c95b826d570a84b0ab2423736bde1f6ffcfcdf9171b452b4bb510a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e2c8cd9ef19d67ece70fe2d1e63ee0b23d3cdd71885f0f83444acb4bd9be19f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalCatchAllActionsVariable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29a713818171aac34a6cc70b073f843e13833a232a39d475ac080265b348cea2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6251be1e9865316cbec35e92db3aa4d8e62d3f97e6cf8a405f7cff110b60c8a0(
    value: typing.Optional[EventOrchestrationGlobalCatchAll],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afd75dc293d2a0ad64738537c97bc8b7eb768ec9672e1a6dc574b818ff3792e5(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    catch_all: typing.Union[EventOrchestrationGlobalCatchAll, typing.Dict[builtins.str, typing.Any]],
    event_orchestration: builtins.str,
    set: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalSet, typing.Dict[builtins.str, typing.Any]]]],
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__305a6830506cb32487336526cc8631fb7f7318d68a61dabd395b65df1c2d7f56(
    *,
    id: builtins.str,
    rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalSetRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8da35d4848f1646e622a6ea7f780d0b564b56f3c01f05e704759450e40302c59(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__448f4cd565464b901ec80b75a8accdb4d1eedbbd42c305b123563c129d6c2f8e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c169784559a5537613e9998466f48abef7b02adda7cf06446cddfa48e66c09f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__291da34fd0264438455c9bc05100b3c77bf5c08086bcf53a2599bd52da81bcd8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22dcb6cd2322d64258b77cb7ad97a911ee4d4bc756873bf06c0b27e50d44b33d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b242bf0c85598522fa67d65a0650049bedf59b5e2b45f761b2111852a05d0e6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSet]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbddb62d7379d6ec8164a43aacd6fa04440cd26e89ea6039465fcee02da06eeb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2357782e55e3edea8f1ede646b7d6e83af2f13be8a4c278d1699891c8418dbe1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalSetRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b2020bfde0f3cbd17069d18280dfbe8f45cd27d62ba302cce93e0f6405dc1af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1118d83b6b95bdad0f5c7886e80d44c0cc10efd60424d19cc48127c92b5f376f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalSet]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6162c0a8b14100ed84de5ebafbd377cdd9354ad5e44008e374977df7e59a651f(
    *,
    actions: typing.Union[EventOrchestrationGlobalSetRuleActions, typing.Dict[builtins.str, typing.Any]],
    condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalSetRuleCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    label: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ab71f345d2ef6d64b052b7646b40dfe5304ce125093203f5b34465d01138d37(
    *,
    annotate: typing.Optional[builtins.str] = None,
    automation_action: typing.Optional[typing.Union[EventOrchestrationGlobalSetRuleActionsAutomationAction, typing.Dict[builtins.str, typing.Any]]] = None,
    drop_event: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    escalation_policy: typing.Optional[builtins.str] = None,
    event_action: typing.Optional[builtins.str] = None,
    extraction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalSetRuleActionsExtraction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    incident_custom_field_update: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalSetRuleActionsIncidentCustomFieldUpdate, typing.Dict[builtins.str, typing.Any]]]]] = None,
    priority: typing.Optional[builtins.str] = None,
    route_to: typing.Optional[builtins.str] = None,
    severity: typing.Optional[builtins.str] = None,
    suppress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    suspend: typing.Optional[jsii.Number] = None,
    variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalSetRuleActionsVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__723d2a0275861d95017a3481ff6564df72221d81439af26b87052de7905dd603(
    *,
    name: builtins.str,
    url: builtins.str,
    auto_send: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalSetRuleActionsAutomationActionHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalSetRuleActionsAutomationActionParameter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    trigger_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__541694733fc98eb5135d9d17e596b4cab74578defc3bdbfef6a43a56159f1877(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c192ed6947c9d47e351e52e7ac3770794b70ad224677b9ae991b40dd8d239d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0967f7a952367da13fc49f57cc02b82f99a43d7f55888f21340a382d446a34bf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f133093d0034db49adecd17de51776d3fa5afcf6026fefac308a6ddd7bb4c06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0fe6676e50e6632fd188d495c5e9ee562ce950012daba4586d7bac8260267ef(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c1caaefa99448a43beea0b451bcf507bd834cf6ca404377537207deb0fee1e0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af460587831495a396c824f55ab2eb0d34c77269a6faf1a0457037d43536f7ae(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRuleActionsAutomationActionHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__925dabb77b721dd39d20aa0b71e44a5bde862a8d75b3be9c94cc4f02b20e527d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eb4db829269dc1e66c774e3d9505aeab6d4ba8c9043a920d5b9e140b64e24b0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cd6ccf6bfc824d4253a1f4b01f87367c52fccfde1c5eef20c3ae5687016b46d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__145d57db160504b02473bf43cc68d40b33f31b9c11718a3e41790c9e37722de2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalSetRuleActionsAutomationActionHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9ee2fd010325c91ed5b38e1b9227da710f0a65bc9f4f43a9f41dfcfd0d90961(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8fed2dd79ebe7c44288433f1c89805de4fdf28eaeeeb4585129718756806cab(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalSetRuleActionsAutomationActionHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__250838c548738d341f27272f626a1c969ab391291eaf8598c110d30cd9432c63(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalSetRuleActionsAutomationActionParameter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8edde0ab8976374e86986f9d9c6015d5024ec409b23f39c2203ad869fc479e3c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4db32bd70cbe1f69ff175d4ded111cf35f7722cdb1c2ef820ca337aafb86d677(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d30e7d51365553fc2bd59007e71a9b0b477e0b32254869e86c64eece0e8ebf53(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__128d57b6052abd22efbffefd58be83b2bfa25138daac6e49494621d1980bd0c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5827bb41de6094284ebd00502f07adf431f1c369b15b592717f41496e9a44493(
    value: typing.Optional[EventOrchestrationGlobalSetRuleActionsAutomationAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__441d5eb0cfb56ea15348461de8ab1eeeb7ba29435b112be08856224068edc133(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbc0ad9f4ed1c01cace41981a42f87453b54e6ede03dfbbdcb846e4adfeaa055(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__611bc51855f9f23f25269c0ee651e3497b2b6afc684a9bc8cf16f183a017ae72(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bff9ba9147a3282fa150f16cd0f425a1817ea00ef125effccb6bf12a4f45f13(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34e4d04292a73fcb461216d1a6ffafb9f78bfbd7af2f12eaf4f169d3fc28ab51(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05e8eb71d200a80cef049dc89b20d2eb1230bb1f137477ef110c0e901f5a0a17(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bf35f3819ede69728004519885f3dfd36d947fa92ffb94aa3a0bda8b1b6fc62(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRuleActionsAutomationActionParameter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5730a11890c169061358eff6c781fda984a09f08bf89fd41c36e38eeef5b132f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28b0f738730c83b224d46641a71b55137a0e4f05f26c7b071c756b12bd55e6d4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa357d5077c52b74b01078fbb36709cc193eb2a94ac2a72a135b79996483caac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41298003ac6f0a8c2bac6db562d1864fdc0898b9c171bb77651f3482c1a629b7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalSetRuleActionsAutomationActionParameter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b92aecb9ded69cbe0d91dde0c5680d12062c234b53c0fd848e59d4dba288176(
    *,
    target: builtins.str,
    regex: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
    template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7df0b35ddb8cf3c60f350bd50085c3615f598c5b08a4406f32697a7d02acafaf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5be2597ac121c396762d3e6759cd18614ecfd85e9d3ce6fa46819068f29924fd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__837596d1e2c3f170b469bc82d4c1c847795abf8654438a9e2c05077d982bd35c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f469f04154a2b221b69d2c39f53b7786912974cb586d0bd90a235a5b625f0f4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73b641091fa0d3cae37eee82d453712bb2493e6c709f5976277a30fb04f94c8c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__696faca3260e3b28834272d395095c80296de069385bf100fbc429c0db2432fb(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRuleActionsExtraction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b35a57eeace5a2f5b909a9acbf477e24e9ea33d13ad9b46800b0928ef01b22dd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0437a7bc7f089843742af301c2567a927c49ebf790ce9acc0dd622810c704e41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__51eefd439060c577d93cf503b4f40e50bbf21a623c047b06c4349f288f885d08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__029062fabc2820396a7ab87918460d0ac2fb6418ace5d2fb621e12fd4e8168c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8903ae6e0334c57a649d9a4df52e53452e3f53d3a44f0880953f2b9eec172d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ba9819ab3723bbb9e6fb97c760af64343f85d868ec8832f5da0a5754100c76c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalSetRuleActionsExtraction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e428808da2e632206477fcba5c539e87b77ccf79dd1d8e26b1d7140d8295e18c(
    *,
    id: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65741d58483630bd5ae6d6fa60ac9c354e3b90844703df1b159c05a450d01eb6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dcde936ae60c7134de199d38135ddea2889923e0e46fb2c4cc58e9b563f57d5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0b4766b52d3130f9f9fdddf3dce6353c1b767ff0a8e2715c9930119f937ff12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__930ac3691abd743f27c6833b2459db4ace15441937c965312c1b47435789eae9(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b694e1b681edf4e61529421aa8d78998622b08ca166e77913a71e4f1c1de3348(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c00c8d089978af43b136c54976ede7592c8b84158d223d1cf4174329933d6f80(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRuleActionsIncidentCustomFieldUpdate]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35bad789610c9f1b6d33712d577d9ddeffa67d33d1d92bcad2d9febf0794f922(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44b104d3bf6b872d4cdaeaed281f7bc37d5aa6e611d802355ba97f90141d707c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b370723c78edf2fbeb99bb972acb2b303f9ba1df2ee46c95ce4afe775b311e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4e9f2de32e2c5bda04162e445ca68a63d5cb5227ed59267ea8bcd79e140d245(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalSetRuleActionsIncidentCustomFieldUpdate]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0f505684a751f1f088cd451fef4ec2359ee0504befdaa6c680d147d5167b352(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4c3fd98078bd837c55eec1586e06251789ffe67f821d37a333d9cf24d33ebc1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalSetRuleActionsExtraction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63b7e10126ed2db187b40890838fcb94fe2d629daf8e17a2be397f7b81c93d87(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalSetRuleActionsIncidentCustomFieldUpdate, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c29635cc10b471f381e294a572a6f6ce91e120c2af223d687c38fce181fcd96(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalSetRuleActionsVariable, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d24dbc69f0ae8626f57c12d98a004903d91acbc6ab30e2988434affb7ef6f35(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__601cc6514734204b43fefd3f9f0acfe12573580d215520898c6c84e7e32f937d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b9f627e19c7e2bbc4f656d65f6a0e0e9d4c84b992546cca7c07f40dc121ba5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53f280b06efc381fc28389eb037650d2e41a3e7bceb2189eb70744b83d53c185(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d56aaf7872939127982b0a1459db57a9a3c56d40f84cb48b1f10f63d4f8ad324(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff8aabdd5cafe2c1381fdf6e0f85ca970a8cf002deaf4aff75568aab58914b6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__069c1d1d09d0d0f1e790d2a933abe557749f50d349d4507ebc0187423c11b56f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__130054da170e2bc35ce44182f7120e297daec8bb6ba726fe72f9cf1370f01ca5(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef9da27c9c082c023dab8929c2c6397cb8d73de4500624a967ef6d577cbc5f19(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a6ff2655bd68fa4369d7665fa46f2adacb6d7d0a9d62c458595c0b7b8601acc(
    value: typing.Optional[EventOrchestrationGlobalSetRuleActions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9975e599b66082aa161a92a72e86a6da50b9cbaa7b3cedfc9ff7f3bf8156c974(
    *,
    name: builtins.str,
    path: builtins.str,
    type: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2b60929c58b2b29387b62c066843f8f79422a9a9e441f975868ee45c89bfbed(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__827e44705a90142712e9755906a7f8452931ba60544afd3ba95616aac82b1dd0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69bafd1a8967651cb8e3d4b4c466218dcdfd979f0c35485ec725afdbd932e7c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__740007e257f8fd817abb8d6451d53ce3a4712fdf97d8f408db6733b484f0d53c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__595210d6d5a25430555b0a3b26f8305c1a54b194f9c2878eeb6cf98c70e31ac4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__448d3ff99277d996053ddb0b27e14b2cb27c8570bec9c59e876dfa7286979151(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRuleActionsVariable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff5f5e5e5e57b371b46435a16ba1cb13e0c9f8aa497317699eb44881a4d428e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad0ff8d99247b3b89d11a280572243be649cabaec328faf3f9b3b425722b0ee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2ac9a1414f529828f4a11e8960e4417a1ec30022295baaa70450dc31133cf30(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4da0da39dae90dce7b70e3c5a2cbc8191b733bf6567c157a11eeea3594cabb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ebdf3716fad58785ca67931c467bbebf67b48bd4f924148f44f24f227afd1cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47afde6482cd6808fcc44fea3a9c4219d74fb35d882ce622b9e4d392cf51d792(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalSetRuleActionsVariable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__195af8a9d56ef9e383b66a3a3513a01f6bfdedfa0d4b13150d22558077655b02(
    *,
    expression: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__402c2d75788b3e5a6716a20899a02fec0125a69523adea16ec297417b6358a5b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a17c2016eec825744ecc1ed8ff8841b53fa59d61a5b1044b0e53af6015166939(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__348e382a0150f8d2c73c54ab7ba42ad9d59b5a87223eff7dbe833f5c0eb4c9d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16087c6ce61dfa3cf72dec62449deeb358b24ca059827efc1e94b1fd5d9ff0de(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fbd88fefc006d31ef0fb55df701cc47fcaeed9b72c207ab4f98443430d83132(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__325fb874a8cd0e638ed8a9045bc87a6b70200be0b54b1e3841a4b46f9bd5ef7d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRuleCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14140ba5dcaf89645318e32df911b3f2d7dd4d8631c2130f954397e5a287a17f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a5eed38e635f1bb6f63df5b6e4d5e39765d5bd58aa6406a06b99018b68ba4cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6509e74762f5df0f7c008f9d6ac12b14743918e5009915e3f684fe0c0d71f8ee(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalSetRuleCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01fd680a6b08cecf2290431bd0e32b0a7b085ea1438a166ecd0ca40288dc1209(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b307780ebe288f563a1599b030711a21e648ce852de1501e05c69fde2eaeebe2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__304f6b49d2c7bf94b9cef4779f8feeca2da1efad681c98b2df2351e7bbf13b25(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8289537f8967ae9ab488de5d1347be9813cc58389b4bdcda4a14fa09cedfc86d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db685b7e936b81cdc353a88bce175fb3415aba05cbf7c1173486f36b7aac6625(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57f3e82836f9e62b0e31fcdf2e1480a4164f045de596616947ad65306281a386(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationGlobalSetRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cf78bc1c1bf47c63adac534d295cd76e9965f5e8cc28b99dba5c3d49c812964(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4df362519df843c8738df1bf088879b04a1d13a3d3e531e41e3a47e2018154a8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationGlobalSetRuleCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8490c88e79aa6729ada8487946e8b4c5a110e3ecfb7d96480d75f4926f72746f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7823141159a2eb2fa54c0466803b505a53ddfbb1c7c188fefd6591bf3653cbf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9b1f459869b78a8201cfc8e6f27b5dc96a68998e96fe160e1153f6335de8086(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationGlobalSetRule]],
) -> None:
    """Type checking stubs"""
    pass
