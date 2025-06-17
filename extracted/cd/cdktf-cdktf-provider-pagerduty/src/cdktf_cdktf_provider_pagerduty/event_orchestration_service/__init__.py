r'''
# `pagerduty_event_orchestration_service`

Refer to the Terraform Registry for docs: [`pagerduty_event_orchestration_service`](https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service).
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


class EventOrchestrationService(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationService",
):
    '''Represents a {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service pagerduty_event_orchestration_service}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        catch_all: typing.Union["EventOrchestrationServiceCatchAll", typing.Dict[builtins.str, typing.Any]],
        service: builtins.str,
        set: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationServiceSet", typing.Dict[builtins.str, typing.Any]]]],
        enable_event_orchestration_for_service: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service pagerduty_event_orchestration_service} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param catch_all: catch_all block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#catch_all EventOrchestrationService#catch_all}
        :param service: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#service EventOrchestrationService#service}.
        :param set: set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#set EventOrchestrationService#set}
        :param enable_event_orchestration_for_service: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#enable_event_orchestration_for_service EventOrchestrationService#enable_event_orchestration_for_service}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#id EventOrchestrationService#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d08348341dceec64836b9fb2870e446abc537ad52e6577d3f00cce3b2b4c5bc9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = EventOrchestrationServiceConfig(
            catch_all=catch_all,
            service=service,
            set=set,
            enable_event_orchestration_for_service=enable_event_orchestration_for_service,
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
        '''Generates CDKTF code for importing a EventOrchestrationService resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the EventOrchestrationService to import.
        :param import_from_id: The id of the existing EventOrchestrationService that should be imported. Refer to the {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the EventOrchestrationService to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b892f457ef0302b120620940a071657ed5e358ec77fb3778d39ec84273cb55ec)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCatchAll")
    def put_catch_all(
        self,
        *,
        actions: typing.Union["EventOrchestrationServiceCatchAllActions", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#actions EventOrchestrationService#actions}
        '''
        value = EventOrchestrationServiceCatchAll(actions=actions)

        return typing.cast(None, jsii.invoke(self, "putCatchAll", [value]))

    @jsii.member(jsii_name="putSet")
    def put_set(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationServiceSet", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e46084fbb0dac8b50a00e9ccad8ae950ee1e6db3090453ec68694394b57dfd3f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSet", [value]))

    @jsii.member(jsii_name="resetEnableEventOrchestrationForService")
    def reset_enable_event_orchestration_for_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableEventOrchestrationForService", []))

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
    def catch_all(self) -> "EventOrchestrationServiceCatchAllOutputReference":
        return typing.cast("EventOrchestrationServiceCatchAllOutputReference", jsii.get(self, "catchAll"))

    @builtins.property
    @jsii.member(jsii_name="set")
    def set(self) -> "EventOrchestrationServiceSetList":
        return typing.cast("EventOrchestrationServiceSetList", jsii.get(self, "set"))

    @builtins.property
    @jsii.member(jsii_name="catchAllInput")
    def catch_all_input(self) -> typing.Optional["EventOrchestrationServiceCatchAll"]:
        return typing.cast(typing.Optional["EventOrchestrationServiceCatchAll"], jsii.get(self, "catchAllInput"))

    @builtins.property
    @jsii.member(jsii_name="enableEventOrchestrationForServiceInput")
    def enable_event_orchestration_for_service_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableEventOrchestrationForServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="setInput")
    def set_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceSet"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceSet"]]], jsii.get(self, "setInput"))

    @builtins.property
    @jsii.member(jsii_name="enableEventOrchestrationForService")
    def enable_event_orchestration_for_service(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableEventOrchestrationForService"))

    @enable_event_orchestration_for_service.setter
    def enable_event_orchestration_for_service(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7d3d9ef71f8f1cfb5352b56523a95ea60a202847c4dc3fe0402efc31a269fc2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableEventOrchestrationForService", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cba48748c584698416a859fd552b344e64eb341772bc5c0ce9c524a7ae6dc398)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b2b0d7389d27fe2a680eb7bc85d700e3d3d33efb58a82ab17798b81012f13b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceCatchAll",
    jsii_struct_bases=[],
    name_mapping={"actions": "actions"},
)
class EventOrchestrationServiceCatchAll:
    def __init__(
        self,
        *,
        actions: typing.Union["EventOrchestrationServiceCatchAllActions", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#actions EventOrchestrationService#actions}
        '''
        if isinstance(actions, dict):
            actions = EventOrchestrationServiceCatchAllActions(**actions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b227d67adc0b66eb81065c2e1c6abc53ea00647b286583b69c9b2e24a2d7993a)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
        }

    @builtins.property
    def actions(self) -> "EventOrchestrationServiceCatchAllActions":
        '''actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#actions EventOrchestrationService#actions}
        '''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast("EventOrchestrationServiceCatchAllActions", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationServiceCatchAll(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceCatchAllActions",
    jsii_struct_bases=[],
    name_mapping={
        "annotate": "annotate",
        "automation_action": "automationAction",
        "escalation_policy": "escalationPolicy",
        "event_action": "eventAction",
        "extraction": "extraction",
        "incident_custom_field_update": "incidentCustomFieldUpdate",
        "pagerduty_automation_action": "pagerdutyAutomationAction",
        "priority": "priority",
        "route_to": "routeTo",
        "severity": "severity",
        "suppress": "suppress",
        "suspend": "suspend",
        "variable": "variable",
    },
)
class EventOrchestrationServiceCatchAllActions:
    def __init__(
        self,
        *,
        annotate: typing.Optional[builtins.str] = None,
        automation_action: typing.Optional[typing.Union["EventOrchestrationServiceCatchAllActionsAutomationAction", typing.Dict[builtins.str, typing.Any]]] = None,
        escalation_policy: typing.Optional[builtins.str] = None,
        event_action: typing.Optional[builtins.str] = None,
        extraction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationServiceCatchAllActionsExtraction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        incident_custom_field_update: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationServiceCatchAllActionsIncidentCustomFieldUpdate", typing.Dict[builtins.str, typing.Any]]]]] = None,
        pagerduty_automation_action: typing.Optional[typing.Union["EventOrchestrationServiceCatchAllActionsPagerdutyAutomationAction", typing.Dict[builtins.str, typing.Any]]] = None,
        priority: typing.Optional[builtins.str] = None,
        route_to: typing.Optional[builtins.str] = None,
        severity: typing.Optional[builtins.str] = None,
        suppress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        suspend: typing.Optional[jsii.Number] = None,
        variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationServiceCatchAllActionsVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param annotate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#annotate EventOrchestrationService#annotate}.
        :param automation_action: automation_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#automation_action EventOrchestrationService#automation_action}
        :param escalation_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#escalation_policy EventOrchestrationService#escalation_policy}.
        :param event_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#event_action EventOrchestrationService#event_action}.
        :param extraction: extraction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#extraction EventOrchestrationService#extraction}
        :param incident_custom_field_update: incident_custom_field_update block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#incident_custom_field_update EventOrchestrationService#incident_custom_field_update}
        :param pagerduty_automation_action: pagerduty_automation_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#pagerduty_automation_action EventOrchestrationService#pagerduty_automation_action}
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#priority EventOrchestrationService#priority}.
        :param route_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#route_to EventOrchestrationService#route_to}.
        :param severity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#severity EventOrchestrationService#severity}.
        :param suppress: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#suppress EventOrchestrationService#suppress}.
        :param suspend: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#suspend EventOrchestrationService#suspend}.
        :param variable: variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#variable EventOrchestrationService#variable}
        '''
        if isinstance(automation_action, dict):
            automation_action = EventOrchestrationServiceCatchAllActionsAutomationAction(**automation_action)
        if isinstance(pagerduty_automation_action, dict):
            pagerduty_automation_action = EventOrchestrationServiceCatchAllActionsPagerdutyAutomationAction(**pagerduty_automation_action)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beda496736753331da07674d5c1607aa07ba1c479670cc6ddf2e0acb104b6e1a)
            check_type(argname="argument annotate", value=annotate, expected_type=type_hints["annotate"])
            check_type(argname="argument automation_action", value=automation_action, expected_type=type_hints["automation_action"])
            check_type(argname="argument escalation_policy", value=escalation_policy, expected_type=type_hints["escalation_policy"])
            check_type(argname="argument event_action", value=event_action, expected_type=type_hints["event_action"])
            check_type(argname="argument extraction", value=extraction, expected_type=type_hints["extraction"])
            check_type(argname="argument incident_custom_field_update", value=incident_custom_field_update, expected_type=type_hints["incident_custom_field_update"])
            check_type(argname="argument pagerduty_automation_action", value=pagerduty_automation_action, expected_type=type_hints["pagerduty_automation_action"])
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
        if escalation_policy is not None:
            self._values["escalation_policy"] = escalation_policy
        if event_action is not None:
            self._values["event_action"] = event_action
        if extraction is not None:
            self._values["extraction"] = extraction
        if incident_custom_field_update is not None:
            self._values["incident_custom_field_update"] = incident_custom_field_update
        if pagerduty_automation_action is not None:
            self._values["pagerduty_automation_action"] = pagerduty_automation_action
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#annotate EventOrchestrationService#annotate}.'''
        result = self._values.get("annotate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def automation_action(
        self,
    ) -> typing.Optional["EventOrchestrationServiceCatchAllActionsAutomationAction"]:
        '''automation_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#automation_action EventOrchestrationService#automation_action}
        '''
        result = self._values.get("automation_action")
        return typing.cast(typing.Optional["EventOrchestrationServiceCatchAllActionsAutomationAction"], result)

    @builtins.property
    def escalation_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#escalation_policy EventOrchestrationService#escalation_policy}.'''
        result = self._values.get("escalation_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#event_action EventOrchestrationService#event_action}.'''
        result = self._values.get("event_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extraction(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceCatchAllActionsExtraction"]]]:
        '''extraction block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#extraction EventOrchestrationService#extraction}
        '''
        result = self._values.get("extraction")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceCatchAllActionsExtraction"]]], result)

    @builtins.property
    def incident_custom_field_update(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceCatchAllActionsIncidentCustomFieldUpdate"]]]:
        '''incident_custom_field_update block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#incident_custom_field_update EventOrchestrationService#incident_custom_field_update}
        '''
        result = self._values.get("incident_custom_field_update")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceCatchAllActionsIncidentCustomFieldUpdate"]]], result)

    @builtins.property
    def pagerduty_automation_action(
        self,
    ) -> typing.Optional["EventOrchestrationServiceCatchAllActionsPagerdutyAutomationAction"]:
        '''pagerduty_automation_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#pagerduty_automation_action EventOrchestrationService#pagerduty_automation_action}
        '''
        result = self._values.get("pagerduty_automation_action")
        return typing.cast(typing.Optional["EventOrchestrationServiceCatchAllActionsPagerdutyAutomationAction"], result)

    @builtins.property
    def priority(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#priority EventOrchestrationService#priority}.'''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def route_to(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#route_to EventOrchestrationService#route_to}.'''
        result = self._values.get("route_to")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def severity(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#severity EventOrchestrationService#severity}.'''
        result = self._values.get("severity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suppress(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#suppress EventOrchestrationService#suppress}.'''
        result = self._values.get("suppress")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def suspend(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#suspend EventOrchestrationService#suspend}.'''
        result = self._values.get("suspend")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def variable(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceCatchAllActionsVariable"]]]:
        '''variable block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#variable EventOrchestrationService#variable}
        '''
        result = self._values.get("variable")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceCatchAllActionsVariable"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationServiceCatchAllActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceCatchAllActionsAutomationAction",
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
class EventOrchestrationServiceCatchAllActionsAutomationAction:
    def __init__(
        self,
        *,
        name: builtins.str,
        url: builtins.str,
        auto_send: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationServiceCatchAllActionsAutomationActionHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationServiceCatchAllActionsAutomationActionParameter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        trigger_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#name EventOrchestrationService#name}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#url EventOrchestrationService#url}.
        :param auto_send: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#auto_send EventOrchestrationService#auto_send}.
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#header EventOrchestrationService#header}
        :param parameter: parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#parameter EventOrchestrationService#parameter}
        :param trigger_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#trigger_types EventOrchestrationService#trigger_types}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efd5f1e070bb8fd6be2fbc035155fcc33d1d50c82cf65ca64bd88817a497c9d6)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#name EventOrchestrationService#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#url EventOrchestrationService#url}.'''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_send(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#auto_send EventOrchestrationService#auto_send}.'''
        result = self._values.get("auto_send")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceCatchAllActionsAutomationActionHeader"]]]:
        '''header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#header EventOrchestrationService#header}
        '''
        result = self._values.get("header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceCatchAllActionsAutomationActionHeader"]]], result)

    @builtins.property
    def parameter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceCatchAllActionsAutomationActionParameter"]]]:
        '''parameter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#parameter EventOrchestrationService#parameter}
        '''
        result = self._values.get("parameter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceCatchAllActionsAutomationActionParameter"]]], result)

    @builtins.property
    def trigger_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#trigger_types EventOrchestrationService#trigger_types}.'''
        result = self._values.get("trigger_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationServiceCatchAllActionsAutomationAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceCatchAllActionsAutomationActionHeader",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class EventOrchestrationServiceCatchAllActionsAutomationActionHeader:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#key EventOrchestrationService#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#value EventOrchestrationService#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12d73bf329b31b590843bd447dac4068fb86b0f35560c424dceb75b7523d8348)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#key EventOrchestrationService#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#value EventOrchestrationService#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationServiceCatchAllActionsAutomationActionHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationServiceCatchAllActionsAutomationActionHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceCatchAllActionsAutomationActionHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2cc7bcfc39ed3677c2f9416313a9f15ce1fae793b00746d5653bb3d6f8b5ce93)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventOrchestrationServiceCatchAllActionsAutomationActionHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aad05e6b5c624ecb9105659a06bfd2a4ba9c8185409e1e7f8fb0e97ca53e61a3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationServiceCatchAllActionsAutomationActionHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84d997361fa39e02764464043b92c786b9910a275ca12126d245af825ca3803c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7ce513cffae669415d030c2b47a3756fe66da6b22a2a9ad8e3a54c3585d5e90)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3cb47a705ca522c3d9ba95e97e3aa9fd154f9c7d0b74acc6537549f88777eea1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceCatchAllActionsAutomationActionHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceCatchAllActionsAutomationActionHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceCatchAllActionsAutomationActionHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f76943919149dfb4c4af0e0a694afabdf78fc45b41ce794fca4275d0eb97ba4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationServiceCatchAllActionsAutomationActionHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceCatchAllActionsAutomationActionHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2e7fefdd2464e472dd0fd1304b3033d418e51a27a857792cf1b8b819d0a0cf3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dff40a8f24d0522e72179af91ae38445505b2de29cd0e63f8ad99fd1c816c08f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4430d32f833017dc62fb01bce25c54079366bb10b3a67637ea3fe300868b82fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceCatchAllActionsAutomationActionHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceCatchAllActionsAutomationActionHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceCatchAllActionsAutomationActionHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af57416408e219597b3dec5f7377499b5cbef0ce78085893faf5f9fc2b86244b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationServiceCatchAllActionsAutomationActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceCatchAllActionsAutomationActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ff7cedf1f06dc82c8dba47cb3907b78be58df2a675491b92bfe0f91730183764)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHeader")
    def put_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceCatchAllActionsAutomationActionHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dbbad64dd726b2b9544eecd7568f2711194684870856c8d72fe3c47a8d53402)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeader", [value]))

    @jsii.member(jsii_name="putParameter")
    def put_parameter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationServiceCatchAllActionsAutomationActionParameter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3f8697d8015d49bf0fcc3adde9dcf02b67f20a8b006f10a79303bf37022a140)
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
    ) -> EventOrchestrationServiceCatchAllActionsAutomationActionHeaderList:
        return typing.cast(EventOrchestrationServiceCatchAllActionsAutomationActionHeaderList, jsii.get(self, "header"))

    @builtins.property
    @jsii.member(jsii_name="parameter")
    def parameter(
        self,
    ) -> "EventOrchestrationServiceCatchAllActionsAutomationActionParameterList":
        return typing.cast("EventOrchestrationServiceCatchAllActionsAutomationActionParameterList", jsii.get(self, "parameter"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceCatchAllActionsAutomationActionHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceCatchAllActionsAutomationActionHeader]]], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parameterInput")
    def parameter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceCatchAllActionsAutomationActionParameter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceCatchAllActionsAutomationActionParameter"]]], jsii.get(self, "parameterInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__4b36c5532a34a9c9a6d52f97d1ece95b6225a25d945a855560a56de2813d98c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoSend", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83124f62a012b7888f47918ac98ad82955941b410df9810f8278c22b11de8363)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="triggerTypes")
    def trigger_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "triggerTypes"))

    @trigger_types.setter
    def trigger_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b5dca257feece5aa0296bc5c1495fec20af5ac00afa46d6994ed9ec4bff3613)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9d21f3b82013ed5c6a7ccb17997d3335c8bcf508549d07a17d3bb14b10acfce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventOrchestrationServiceCatchAllActionsAutomationAction]:
        return typing.cast(typing.Optional[EventOrchestrationServiceCatchAllActionsAutomationAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventOrchestrationServiceCatchAllActionsAutomationAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98aec7455cfaf172c7a1be08fc36c9e714a4d11a2644bbceb222e3ceef70bc07)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceCatchAllActionsAutomationActionParameter",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class EventOrchestrationServiceCatchAllActionsAutomationActionParameter:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#key EventOrchestrationService#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#value EventOrchestrationService#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f77ccf016a5ec27250748c3b8d7d5355a57cb2b23f0da03c4af1fbe0ec6bad4)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#key EventOrchestrationService#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#value EventOrchestrationService#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationServiceCatchAllActionsAutomationActionParameter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationServiceCatchAllActionsAutomationActionParameterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceCatchAllActionsAutomationActionParameterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb3761323c243fe2b43295ba8360f5c994579a744113a52012a30d59e4bfa6eb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventOrchestrationServiceCatchAllActionsAutomationActionParameterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3351980f2e77b126f695f08906f74090032b9657af59e902e558e5cc3fd3fc0e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationServiceCatchAllActionsAutomationActionParameterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00b0ace084cab22f3b1ef6df0d8ad8536b8d7008ed3ae19ce51ca6b096a8b8a6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__970d8dcc5e2cb152c98c52ec236d3a6bb961bc4bc84b69595be7b3d0360e0e32)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c8a14a696bf92e1c082ee0c39296a587387a51c50668820fa3038d2661d7529b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceCatchAllActionsAutomationActionParameter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceCatchAllActionsAutomationActionParameter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceCatchAllActionsAutomationActionParameter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac34ff5582fa85e662944d802cde427031d9403afaae2102bc82a8c697b2e116)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationServiceCatchAllActionsAutomationActionParameterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceCatchAllActionsAutomationActionParameterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9110e7ff690e382564c5ca73e86597fabf8de2c16aa332feac24d2cbc70a9875)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f7947d86c45a39779f08a7dad1dc91065a36f2575c15463db8764212b4622d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50c63310c33cca88b38409ed4d7dee6d8e15b7326345d15b9aefc9dd83e848c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceCatchAllActionsAutomationActionParameter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceCatchAllActionsAutomationActionParameter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceCatchAllActionsAutomationActionParameter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4ca61714f5f83d6fa15a4630675d5aa438c4620f2c051ec03cee9d53331b6d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceCatchAllActionsExtraction",
    jsii_struct_bases=[],
    name_mapping={
        "target": "target",
        "regex": "regex",
        "source": "source",
        "template": "template",
    },
)
class EventOrchestrationServiceCatchAllActionsExtraction:
    def __init__(
        self,
        *,
        target: builtins.str,
        regex: typing.Optional[builtins.str] = None,
        source: typing.Optional[builtins.str] = None,
        template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#target EventOrchestrationService#target}.
        :param regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#regex EventOrchestrationService#regex}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#source EventOrchestrationService#source}.
        :param template: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#template EventOrchestrationService#template}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f58412ceaa4b443b64995d85bbe4e834b3498866453b4a02bfde851b48a6d87)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#target EventOrchestrationService#target}.'''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def regex(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#regex EventOrchestrationService#regex}.'''
        result = self._values.get("regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#source EventOrchestrationService#source}.'''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#template EventOrchestrationService#template}.'''
        result = self._values.get("template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationServiceCatchAllActionsExtraction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationServiceCatchAllActionsExtractionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceCatchAllActionsExtractionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4f33499a54fa41481cc71417ecbbdf3e9fa1f329e438c60d64e49630dfdccfdf)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventOrchestrationServiceCatchAllActionsExtractionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e93f6d3492309228dafbec939c7ac8294503f1cbceec374f9a6a030ed408e77f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationServiceCatchAllActionsExtractionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4497185fae3a44c83b7a335b26d3a12e10511477b0c6fc43c1959c69ec36064f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a22b98f8b92a5cb3f29e9ce9033791392dd726922fa1c176527415c19a12830)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22278744b9b674857b25176abf93e0642b5768216c903f2e416f1921e61c9423)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceCatchAllActionsExtraction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceCatchAllActionsExtraction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceCatchAllActionsExtraction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d10ed1726ec1bdba660d527a81e4eaba3f3ab0e83ec8a4653d3dae8a17924ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationServiceCatchAllActionsExtractionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceCatchAllActionsExtractionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ffa68d26fddac64eb2f7ea7f859c64883b68af01f8e4e93dacc489c3ee7bfa8d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e1f5afff845d8c3b3b7723aa0364379b420e941ba31f3a9b36d5eec0c3a31bf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6eb10546f056d62f686cca9e4014fcfed9e087f3dd66685409ad1bd721c8c940)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d2f6a47a2f75a6e1a69399e8727597430bd88179c735d9b194f3e9ff5f0828c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="template")
    def template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "template"))

    @template.setter
    def template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53ddd62bdd642450917ca1c8c6423a915bac235572f81b4e0410bcfaa693ba18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "template", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceCatchAllActionsExtraction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceCatchAllActionsExtraction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceCatchAllActionsExtraction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__955d3b2404015c64dc01f453ae8a593f2d9a9788f9d4d7e7283124fecba7dba1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceCatchAllActionsIncidentCustomFieldUpdate",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "value": "value"},
)
class EventOrchestrationServiceCatchAllActionsIncidentCustomFieldUpdate:
    def __init__(self, *, id: builtins.str, value: builtins.str) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#id EventOrchestrationService#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#value EventOrchestrationService#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01c0a9c05e20146e2fbbf0f5af59e520a0ab811ae8ef69b936a08bfba4f12841)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "value": value,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#id EventOrchestrationService#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#value EventOrchestrationService#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationServiceCatchAllActionsIncidentCustomFieldUpdate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationServiceCatchAllActionsIncidentCustomFieldUpdateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceCatchAllActionsIncidentCustomFieldUpdateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__af2e9d21783215883a12a82a16b43cad514ea8b982bbaedf770dc0ff180471f8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventOrchestrationServiceCatchAllActionsIncidentCustomFieldUpdateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd85779a67094424f1ad8c5716fe8d59aef933a14295066d6df3387c8844e746)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationServiceCatchAllActionsIncidentCustomFieldUpdateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb7a33de99b8396d0f606d51d456360418441a9f10b29d34fc30ce0c92a63c01)
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
            type_hints = typing.get_type_hints(_typecheckingstub__333491a1b5d1937e52e5ce178b326b78d4f2066b85069501f8ec14cd84ca30a5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fefc2ace9d08f8dfa42a96c1ee70cbd0138f891f404784e14cfe789d776a7553)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceCatchAllActionsIncidentCustomFieldUpdate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceCatchAllActionsIncidentCustomFieldUpdate]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceCatchAllActionsIncidentCustomFieldUpdate]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38cc3cd94d58efb4d4f8c7e86724e4c83e08d329ac50ca475adc45a9b878a79b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationServiceCatchAllActionsIncidentCustomFieldUpdateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceCatchAllActionsIncidentCustomFieldUpdateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c084db4e2919ce91d89472be23915b3181e6e0efac8e81210bb23f4feb65a843)
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
            type_hints = typing.get_type_hints(_typecheckingstub__382689c1b1146d190f503f7735623845ebe79352f84d6e99003952c461a9ea24)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__811321dcfd3f9c27d81b98cb45814d26e86c3ce1115657a400406d535e563f48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceCatchAllActionsIncidentCustomFieldUpdate]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceCatchAllActionsIncidentCustomFieldUpdate]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceCatchAllActionsIncidentCustomFieldUpdate]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4a5bde59fd077fb13bc3390986492a560ceabb8dfceb5373935f0003db83ae4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationServiceCatchAllActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceCatchAllActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b8e4074613d1e8949bb47ade1ca67315a7ff981c5c7ebd3ac9d65a0571e47654)
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
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceCatchAllActionsAutomationActionHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
        parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceCatchAllActionsAutomationActionParameter, typing.Dict[builtins.str, typing.Any]]]]] = None,
        trigger_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#name EventOrchestrationService#name}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#url EventOrchestrationService#url}.
        :param auto_send: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#auto_send EventOrchestrationService#auto_send}.
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#header EventOrchestrationService#header}
        :param parameter: parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#parameter EventOrchestrationService#parameter}
        :param trigger_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#trigger_types EventOrchestrationService#trigger_types}.
        '''
        value = EventOrchestrationServiceCatchAllActionsAutomationAction(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceCatchAllActionsExtraction, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32dbb53f21524e45be09cfac77f8643db6d56d7d1bf8f6e3aab8adefb452d77f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExtraction", [value]))

    @jsii.member(jsii_name="putIncidentCustomFieldUpdate")
    def put_incident_custom_field_update(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceCatchAllActionsIncidentCustomFieldUpdate, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__685fd28b1d68820fb065771a742c2b574663e76fbc7dc6192d2696d61c61fb18)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIncidentCustomFieldUpdate", [value]))

    @jsii.member(jsii_name="putPagerdutyAutomationAction")
    def put_pagerduty_automation_action(
        self,
        *,
        action_id: builtins.str,
        trigger_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param action_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#action_id EventOrchestrationService#action_id}.
        :param trigger_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#trigger_types EventOrchestrationService#trigger_types}.
        '''
        value = EventOrchestrationServiceCatchAllActionsPagerdutyAutomationAction(
            action_id=action_id, trigger_types=trigger_types
        )

        return typing.cast(None, jsii.invoke(self, "putPagerdutyAutomationAction", [value]))

    @jsii.member(jsii_name="putVariable")
    def put_variable(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationServiceCatchAllActionsVariable", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7fbac385a3cc6463601d9d52057e415e170b731537a0bac97745cf1ccc1ea8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVariable", [value]))

    @jsii.member(jsii_name="resetAnnotate")
    def reset_annotate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotate", []))

    @jsii.member(jsii_name="resetAutomationAction")
    def reset_automation_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomationAction", []))

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

    @jsii.member(jsii_name="resetPagerdutyAutomationAction")
    def reset_pagerduty_automation_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPagerdutyAutomationAction", []))

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
    ) -> EventOrchestrationServiceCatchAllActionsAutomationActionOutputReference:
        return typing.cast(EventOrchestrationServiceCatchAllActionsAutomationActionOutputReference, jsii.get(self, "automationAction"))

    @builtins.property
    @jsii.member(jsii_name="extraction")
    def extraction(self) -> EventOrchestrationServiceCatchAllActionsExtractionList:
        return typing.cast(EventOrchestrationServiceCatchAllActionsExtractionList, jsii.get(self, "extraction"))

    @builtins.property
    @jsii.member(jsii_name="incidentCustomFieldUpdate")
    def incident_custom_field_update(
        self,
    ) -> EventOrchestrationServiceCatchAllActionsIncidentCustomFieldUpdateList:
        return typing.cast(EventOrchestrationServiceCatchAllActionsIncidentCustomFieldUpdateList, jsii.get(self, "incidentCustomFieldUpdate"))

    @builtins.property
    @jsii.member(jsii_name="pagerdutyAutomationAction")
    def pagerduty_automation_action(
        self,
    ) -> "EventOrchestrationServiceCatchAllActionsPagerdutyAutomationActionOutputReference":
        return typing.cast("EventOrchestrationServiceCatchAllActionsPagerdutyAutomationActionOutputReference", jsii.get(self, "pagerdutyAutomationAction"))

    @builtins.property
    @jsii.member(jsii_name="variable")
    def variable(self) -> "EventOrchestrationServiceCatchAllActionsVariableList":
        return typing.cast("EventOrchestrationServiceCatchAllActionsVariableList", jsii.get(self, "variable"))

    @builtins.property
    @jsii.member(jsii_name="annotateInput")
    def annotate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "annotateInput"))

    @builtins.property
    @jsii.member(jsii_name="automationActionInput")
    def automation_action_input(
        self,
    ) -> typing.Optional[EventOrchestrationServiceCatchAllActionsAutomationAction]:
        return typing.cast(typing.Optional[EventOrchestrationServiceCatchAllActionsAutomationAction], jsii.get(self, "automationActionInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceCatchAllActionsExtraction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceCatchAllActionsExtraction]]], jsii.get(self, "extractionInput"))

    @builtins.property
    @jsii.member(jsii_name="incidentCustomFieldUpdateInput")
    def incident_custom_field_update_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceCatchAllActionsIncidentCustomFieldUpdate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceCatchAllActionsIncidentCustomFieldUpdate]]], jsii.get(self, "incidentCustomFieldUpdateInput"))

    @builtins.property
    @jsii.member(jsii_name="pagerdutyAutomationActionInput")
    def pagerduty_automation_action_input(
        self,
    ) -> typing.Optional["EventOrchestrationServiceCatchAllActionsPagerdutyAutomationAction"]:
        return typing.cast(typing.Optional["EventOrchestrationServiceCatchAllActionsPagerdutyAutomationAction"], jsii.get(self, "pagerdutyAutomationActionInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceCatchAllActionsVariable"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceCatchAllActionsVariable"]]], jsii.get(self, "variableInput"))

    @builtins.property
    @jsii.member(jsii_name="annotate")
    def annotate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "annotate"))

    @annotate.setter
    def annotate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6068ff5148d7065f07e1849c9b135708e390d307454ddb5b679ed636a38888d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="escalationPolicy")
    def escalation_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "escalationPolicy"))

    @escalation_policy.setter
    def escalation_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d5d7e3a9e5fbfb4df62bc37ac8b154fc3a9493394a779db7451286ee79c0c99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "escalationPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventAction")
    def event_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventAction"))

    @event_action.setter
    def event_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82505222497a3807b05b8ae86653bc1267ec13242eddd69bc864fdd2e3a396a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b8d8c2be25bf4c6dcf31936cd1f576796c1165ea856ad9c1bee59df645a0264)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routeTo")
    def route_to(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routeTo"))

    @route_to.setter
    def route_to(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1cd9d02b6e37f3b61e799d08655481cb8a790f80e967d3a650ae69c670e5d71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeTo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "severity"))

    @severity.setter
    def severity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04550b07dade91d853fa2f276c5e028c1928fe3a764e553e4998c5a814422f58)
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
            type_hints = typing.get_type_hints(_typecheckingstub__db0ca7322be53357bcf11fa0853e4d21b371903f2f003fda3a2b625a4facde73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suppress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suspend")
    def suspend(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "suspend"))

    @suspend.setter
    def suspend(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89bfbeb9323588c07ecbcab90b87568f6531a82a624ba1dc51739d9f29292280)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suspend", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventOrchestrationServiceCatchAllActions]:
        return typing.cast(typing.Optional[EventOrchestrationServiceCatchAllActions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventOrchestrationServiceCatchAllActions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16700c79dd19273d3d1ee91d8e9e86dfb200d47cb477abb2bc747e1c6699f37d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceCatchAllActionsPagerdutyAutomationAction",
    jsii_struct_bases=[],
    name_mapping={"action_id": "actionId", "trigger_types": "triggerTypes"},
)
class EventOrchestrationServiceCatchAllActionsPagerdutyAutomationAction:
    def __init__(
        self,
        *,
        action_id: builtins.str,
        trigger_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param action_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#action_id EventOrchestrationService#action_id}.
        :param trigger_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#trigger_types EventOrchestrationService#trigger_types}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36c445cd297e9983fefb5c67dfff11fbb2c473c5aa0a831366f53587769ce7d2)
            check_type(argname="argument action_id", value=action_id, expected_type=type_hints["action_id"])
            check_type(argname="argument trigger_types", value=trigger_types, expected_type=type_hints["trigger_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action_id": action_id,
        }
        if trigger_types is not None:
            self._values["trigger_types"] = trigger_types

    @builtins.property
    def action_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#action_id EventOrchestrationService#action_id}.'''
        result = self._values.get("action_id")
        assert result is not None, "Required property 'action_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def trigger_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#trigger_types EventOrchestrationService#trigger_types}.'''
        result = self._values.get("trigger_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationServiceCatchAllActionsPagerdutyAutomationAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationServiceCatchAllActionsPagerdutyAutomationActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceCatchAllActionsPagerdutyAutomationActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c19a2f26e740d4e85341574218ea80011bd6add0a2a885edd95480fc5b99e552)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTriggerTypes")
    def reset_trigger_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTriggerTypes", []))

    @builtins.property
    @jsii.member(jsii_name="actionIdInput")
    def action_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerTypesInput")
    def trigger_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "triggerTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="actionId")
    def action_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actionId"))

    @action_id.setter
    def action_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f69f46e2b7946b74db45f94a894ef6cf882abd02c01d0c9ae78df68de993599)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="triggerTypes")
    def trigger_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "triggerTypes"))

    @trigger_types.setter
    def trigger_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5667b8032b5a7e88b2ee7db68fb6a9f76c442e8a79f20d170c477392e7b7d3a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventOrchestrationServiceCatchAllActionsPagerdutyAutomationAction]:
        return typing.cast(typing.Optional[EventOrchestrationServiceCatchAllActionsPagerdutyAutomationAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventOrchestrationServiceCatchAllActionsPagerdutyAutomationAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71592b1487987b109a5df7578de2e1a3320c09160d2b399aab6e4f8d4f4c53fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceCatchAllActionsVariable",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "path": "path", "type": "type", "value": "value"},
)
class EventOrchestrationServiceCatchAllActionsVariable:
    def __init__(
        self,
        *,
        name: builtins.str,
        path: builtins.str,
        type: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#name EventOrchestrationService#name}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#path EventOrchestrationService#path}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#type EventOrchestrationService#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#value EventOrchestrationService#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fdf61e0dc61ba126fbdee02c7fed508a1d24e9330930b98770fd63c46593c81)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#name EventOrchestrationService#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#path EventOrchestrationService#path}.'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#type EventOrchestrationService#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#value EventOrchestrationService#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationServiceCatchAllActionsVariable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationServiceCatchAllActionsVariableList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceCatchAllActionsVariableList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__471b7129eee1c155786eebbb22d07db7d78cf732304bd455763d63c647dfbdb8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventOrchestrationServiceCatchAllActionsVariableOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f58aa2dddc511da9902979ccd1e2fc28b105926ee2f5d91757741c6c2ad8322a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationServiceCatchAllActionsVariableOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__651a6813b49ad706a1226d4370493ce1cb5ff09111d487524afc125831f57a11)
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
            type_hints = typing.get_type_hints(_typecheckingstub__929e4a2e8912ad0bae377ef0b03851c33c0b5468ee88f6ff77d02d26723b6a7a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40847430adc64cb182c04bfa3dd359fec4b6b1c37ce0ff893f18f1ac4a61af34)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceCatchAllActionsVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceCatchAllActionsVariable]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceCatchAllActionsVariable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__165f347ab0d9518892c2f457f02cc2bf8e52d330dff763f13d8c08d89069a3d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationServiceCatchAllActionsVariableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceCatchAllActionsVariableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7222d931cac9090003d8e1fef21a6d957651e50f50bd0403ff52a0649f94773)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d8dd033dd6c502ee38ec2cfd971c748eed5c15791e16e4441931181d7eb306d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1d1229cbcceb2a903b723c3efc5a65d4d35aec1b4796b1841bbe9d8d42d5b9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab75bf8c44e2e797ada09d95034220bfcf00402a422274d71df6b7ba960674dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__467373559c7b461fba54cc5de6db1e9a6bb615ea893d862fd0b69d1787480f6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceCatchAllActionsVariable]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceCatchAllActionsVariable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceCatchAllActionsVariable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12cd43d9a0c2a22ed8519f5a2fc94375c9aefacb455ea6c9b23c1e50b6d7a52a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationServiceCatchAllOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceCatchAllOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7c8aea69cfc21d6d60daa10018defd18c8596c87e26caabc75ad3e00f0a9f615)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putActions")
    def put_actions(
        self,
        *,
        annotate: typing.Optional[builtins.str] = None,
        automation_action: typing.Optional[typing.Union[EventOrchestrationServiceCatchAllActionsAutomationAction, typing.Dict[builtins.str, typing.Any]]] = None,
        escalation_policy: typing.Optional[builtins.str] = None,
        event_action: typing.Optional[builtins.str] = None,
        extraction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceCatchAllActionsExtraction, typing.Dict[builtins.str, typing.Any]]]]] = None,
        incident_custom_field_update: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceCatchAllActionsIncidentCustomFieldUpdate, typing.Dict[builtins.str, typing.Any]]]]] = None,
        pagerduty_automation_action: typing.Optional[typing.Union[EventOrchestrationServiceCatchAllActionsPagerdutyAutomationAction, typing.Dict[builtins.str, typing.Any]]] = None,
        priority: typing.Optional[builtins.str] = None,
        route_to: typing.Optional[builtins.str] = None,
        severity: typing.Optional[builtins.str] = None,
        suppress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        suspend: typing.Optional[jsii.Number] = None,
        variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceCatchAllActionsVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param annotate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#annotate EventOrchestrationService#annotate}.
        :param automation_action: automation_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#automation_action EventOrchestrationService#automation_action}
        :param escalation_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#escalation_policy EventOrchestrationService#escalation_policy}.
        :param event_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#event_action EventOrchestrationService#event_action}.
        :param extraction: extraction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#extraction EventOrchestrationService#extraction}
        :param incident_custom_field_update: incident_custom_field_update block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#incident_custom_field_update EventOrchestrationService#incident_custom_field_update}
        :param pagerduty_automation_action: pagerduty_automation_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#pagerduty_automation_action EventOrchestrationService#pagerduty_automation_action}
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#priority EventOrchestrationService#priority}.
        :param route_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#route_to EventOrchestrationService#route_to}.
        :param severity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#severity EventOrchestrationService#severity}.
        :param suppress: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#suppress EventOrchestrationService#suppress}.
        :param suspend: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#suspend EventOrchestrationService#suspend}.
        :param variable: variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#variable EventOrchestrationService#variable}
        '''
        value = EventOrchestrationServiceCatchAllActions(
            annotate=annotate,
            automation_action=automation_action,
            escalation_policy=escalation_policy,
            event_action=event_action,
            extraction=extraction,
            incident_custom_field_update=incident_custom_field_update,
            pagerduty_automation_action=pagerduty_automation_action,
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
    def actions(self) -> EventOrchestrationServiceCatchAllActionsOutputReference:
        return typing.cast(EventOrchestrationServiceCatchAllActionsOutputReference, jsii.get(self, "actions"))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(
        self,
    ) -> typing.Optional[EventOrchestrationServiceCatchAllActions]:
        return typing.cast(typing.Optional[EventOrchestrationServiceCatchAllActions], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EventOrchestrationServiceCatchAll]:
        return typing.cast(typing.Optional[EventOrchestrationServiceCatchAll], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventOrchestrationServiceCatchAll],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a304eee8caf4d82eb549418271a8876f8a01abd44c4f79c9de2968cb1f4965bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceConfig",
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
        "service": "service",
        "set": "set",
        "enable_event_orchestration_for_service": "enableEventOrchestrationForService",
        "id": "id",
    },
)
class EventOrchestrationServiceConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        catch_all: typing.Union[EventOrchestrationServiceCatchAll, typing.Dict[builtins.str, typing.Any]],
        service: builtins.str,
        set: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationServiceSet", typing.Dict[builtins.str, typing.Any]]]],
        enable_event_orchestration_for_service: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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
        :param catch_all: catch_all block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#catch_all EventOrchestrationService#catch_all}
        :param service: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#service EventOrchestrationService#service}.
        :param set: set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#set EventOrchestrationService#set}
        :param enable_event_orchestration_for_service: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#enable_event_orchestration_for_service EventOrchestrationService#enable_event_orchestration_for_service}.
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#id EventOrchestrationService#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(catch_all, dict):
            catch_all = EventOrchestrationServiceCatchAll(**catch_all)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f651de5f1691568a4b4fa927ecf5771ad962a04758bd1655111cabd9d341034)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument catch_all", value=catch_all, expected_type=type_hints["catch_all"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument set", value=set, expected_type=type_hints["set"])
            check_type(argname="argument enable_event_orchestration_for_service", value=enable_event_orchestration_for_service, expected_type=type_hints["enable_event_orchestration_for_service"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "catch_all": catch_all,
            "service": service,
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
        if enable_event_orchestration_for_service is not None:
            self._values["enable_event_orchestration_for_service"] = enable_event_orchestration_for_service
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
    def catch_all(self) -> EventOrchestrationServiceCatchAll:
        '''catch_all block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#catch_all EventOrchestrationService#catch_all}
        '''
        result = self._values.get("catch_all")
        assert result is not None, "Required property 'catch_all' is missing"
        return typing.cast(EventOrchestrationServiceCatchAll, result)

    @builtins.property
    def service(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#service EventOrchestrationService#service}.'''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def set(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceSet"]]:
        '''set block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#set EventOrchestrationService#set}
        '''
        result = self._values.get("set")
        assert result is not None, "Required property 'set' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceSet"]], result)

    @builtins.property
    def enable_event_orchestration_for_service(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#enable_event_orchestration_for_service EventOrchestrationService#enable_event_orchestration_for_service}.'''
        result = self._values.get("enable_event_orchestration_for_service")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#id EventOrchestrationService#id}.

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
        return "EventOrchestrationServiceConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceSet",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "rule": "rule"},
)
class EventOrchestrationServiceSet:
    def __init__(
        self,
        *,
        id: builtins.str,
        rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationServiceSetRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#id EventOrchestrationService#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#rule EventOrchestrationService#rule}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__831a7daf13fa654b6bfdc2368c67a1c298cf892ebcb126748659f37eddff0eeb)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if rule is not None:
            self._values["rule"] = rule

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#id EventOrchestrationService#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceSetRule"]]]:
        '''rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#rule EventOrchestrationService#rule}
        '''
        result = self._values.get("rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceSetRule"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationServiceSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationServiceSetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceSetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2a43490d29cbcbb15884ee08506659396ea022805850f947718781b006d00c15)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "EventOrchestrationServiceSetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b535eb9c572d11645c3eb74cff27963b50ae103942c7ae5577bdae8f9ed8683)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationServiceSetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a76fc580ad7f75b873038e6eda731949bf641dd0f50572183577abe05b2580d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7657db75e9247e387fba7b6f0e984b40e13130adaaa0b3c7c9c9a69be840e24)
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
            type_hints = typing.get_type_hints(_typecheckingstub__71d2fbdfaaedf19eb739ee7c87e1b86041b6939abb96063c11afd152b382cbb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSet]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSet]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSet]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1735431724e4acdd36a77b5ad4859995cf787e2bb89b574504cfb5fc11efebb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationServiceSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d51539ece17bd4bd69b03bfb9dce4df5427c74718658aa814ba13b4de8ecc5b2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putRule")
    def put_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationServiceSetRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4f44f5abfcd24bed3759164541bee1a16375f25a3f1f68c7f619e9a944ce3ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRule", [value]))

    @jsii.member(jsii_name="resetRule")
    def reset_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRule", []))

    @builtins.property
    @jsii.member(jsii_name="rule")
    def rule(self) -> "EventOrchestrationServiceSetRuleList":
        return typing.cast("EventOrchestrationServiceSetRuleList", jsii.get(self, "rule"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleInput")
    def rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceSetRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceSetRule"]]], jsii.get(self, "ruleInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__196ceb27cec271056c566d70d2aab2aad0b560a4705ffd5c955cd8d9c824f690)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceSet]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceSet]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceSet]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__820e6f19b3056b4f1d8a37cb621335e84b9b59e8e2ec757f415a4d41d4194df6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceSetRule",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "condition": "condition",
        "disabled": "disabled",
        "label": "label",
    },
)
class EventOrchestrationServiceSetRule:
    def __init__(
        self,
        *,
        actions: typing.Union["EventOrchestrationServiceSetRuleActions", typing.Dict[builtins.str, typing.Any]],
        condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationServiceSetRuleCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        label: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#actions EventOrchestrationService#actions}
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#condition EventOrchestrationService#condition}
        :param disabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#disabled EventOrchestrationService#disabled}.
        :param label: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#label EventOrchestrationService#label}.
        '''
        if isinstance(actions, dict):
            actions = EventOrchestrationServiceSetRuleActions(**actions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a295a4681da8ad5dd4353d198513715dae734136f36bcfdb0b3d4d588bcd0a4e)
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
    def actions(self) -> "EventOrchestrationServiceSetRuleActions":
        '''actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#actions EventOrchestrationService#actions}
        '''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast("EventOrchestrationServiceSetRuleActions", result)

    @builtins.property
    def condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceSetRuleCondition"]]]:
        '''condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#condition EventOrchestrationService#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceSetRuleCondition"]]], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#disabled EventOrchestrationService#disabled}.'''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#label EventOrchestrationService#label}.'''
        result = self._values.get("label")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationServiceSetRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceSetRuleActions",
    jsii_struct_bases=[],
    name_mapping={
        "annotate": "annotate",
        "automation_action": "automationAction",
        "escalation_policy": "escalationPolicy",
        "event_action": "eventAction",
        "extraction": "extraction",
        "incident_custom_field_update": "incidentCustomFieldUpdate",
        "pagerduty_automation_action": "pagerdutyAutomationAction",
        "priority": "priority",
        "route_to": "routeTo",
        "severity": "severity",
        "suppress": "suppress",
        "suspend": "suspend",
        "variable": "variable",
    },
)
class EventOrchestrationServiceSetRuleActions:
    def __init__(
        self,
        *,
        annotate: typing.Optional[builtins.str] = None,
        automation_action: typing.Optional[typing.Union["EventOrchestrationServiceSetRuleActionsAutomationAction", typing.Dict[builtins.str, typing.Any]]] = None,
        escalation_policy: typing.Optional[builtins.str] = None,
        event_action: typing.Optional[builtins.str] = None,
        extraction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationServiceSetRuleActionsExtraction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        incident_custom_field_update: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationServiceSetRuleActionsIncidentCustomFieldUpdate", typing.Dict[builtins.str, typing.Any]]]]] = None,
        pagerduty_automation_action: typing.Optional[typing.Union["EventOrchestrationServiceSetRuleActionsPagerdutyAutomationAction", typing.Dict[builtins.str, typing.Any]]] = None,
        priority: typing.Optional[builtins.str] = None,
        route_to: typing.Optional[builtins.str] = None,
        severity: typing.Optional[builtins.str] = None,
        suppress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        suspend: typing.Optional[jsii.Number] = None,
        variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationServiceSetRuleActionsVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param annotate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#annotate EventOrchestrationService#annotate}.
        :param automation_action: automation_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#automation_action EventOrchestrationService#automation_action}
        :param escalation_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#escalation_policy EventOrchestrationService#escalation_policy}.
        :param event_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#event_action EventOrchestrationService#event_action}.
        :param extraction: extraction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#extraction EventOrchestrationService#extraction}
        :param incident_custom_field_update: incident_custom_field_update block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#incident_custom_field_update EventOrchestrationService#incident_custom_field_update}
        :param pagerduty_automation_action: pagerduty_automation_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#pagerduty_automation_action EventOrchestrationService#pagerduty_automation_action}
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#priority EventOrchestrationService#priority}.
        :param route_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#route_to EventOrchestrationService#route_to}.
        :param severity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#severity EventOrchestrationService#severity}.
        :param suppress: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#suppress EventOrchestrationService#suppress}.
        :param suspend: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#suspend EventOrchestrationService#suspend}.
        :param variable: variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#variable EventOrchestrationService#variable}
        '''
        if isinstance(automation_action, dict):
            automation_action = EventOrchestrationServiceSetRuleActionsAutomationAction(**automation_action)
        if isinstance(pagerduty_automation_action, dict):
            pagerduty_automation_action = EventOrchestrationServiceSetRuleActionsPagerdutyAutomationAction(**pagerduty_automation_action)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92d01a8d7979022feb679e0e11e8d9988bb013c9596d06df8bd8fe112cf360fa)
            check_type(argname="argument annotate", value=annotate, expected_type=type_hints["annotate"])
            check_type(argname="argument automation_action", value=automation_action, expected_type=type_hints["automation_action"])
            check_type(argname="argument escalation_policy", value=escalation_policy, expected_type=type_hints["escalation_policy"])
            check_type(argname="argument event_action", value=event_action, expected_type=type_hints["event_action"])
            check_type(argname="argument extraction", value=extraction, expected_type=type_hints["extraction"])
            check_type(argname="argument incident_custom_field_update", value=incident_custom_field_update, expected_type=type_hints["incident_custom_field_update"])
            check_type(argname="argument pagerduty_automation_action", value=pagerduty_automation_action, expected_type=type_hints["pagerduty_automation_action"])
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
        if escalation_policy is not None:
            self._values["escalation_policy"] = escalation_policy
        if event_action is not None:
            self._values["event_action"] = event_action
        if extraction is not None:
            self._values["extraction"] = extraction
        if incident_custom_field_update is not None:
            self._values["incident_custom_field_update"] = incident_custom_field_update
        if pagerduty_automation_action is not None:
            self._values["pagerduty_automation_action"] = pagerduty_automation_action
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#annotate EventOrchestrationService#annotate}.'''
        result = self._values.get("annotate")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def automation_action(
        self,
    ) -> typing.Optional["EventOrchestrationServiceSetRuleActionsAutomationAction"]:
        '''automation_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#automation_action EventOrchestrationService#automation_action}
        '''
        result = self._values.get("automation_action")
        return typing.cast(typing.Optional["EventOrchestrationServiceSetRuleActionsAutomationAction"], result)

    @builtins.property
    def escalation_policy(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#escalation_policy EventOrchestrationService#escalation_policy}.'''
        result = self._values.get("escalation_policy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#event_action EventOrchestrationService#event_action}.'''
        result = self._values.get("event_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extraction(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceSetRuleActionsExtraction"]]]:
        '''extraction block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#extraction EventOrchestrationService#extraction}
        '''
        result = self._values.get("extraction")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceSetRuleActionsExtraction"]]], result)

    @builtins.property
    def incident_custom_field_update(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceSetRuleActionsIncidentCustomFieldUpdate"]]]:
        '''incident_custom_field_update block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#incident_custom_field_update EventOrchestrationService#incident_custom_field_update}
        '''
        result = self._values.get("incident_custom_field_update")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceSetRuleActionsIncidentCustomFieldUpdate"]]], result)

    @builtins.property
    def pagerduty_automation_action(
        self,
    ) -> typing.Optional["EventOrchestrationServiceSetRuleActionsPagerdutyAutomationAction"]:
        '''pagerduty_automation_action block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#pagerduty_automation_action EventOrchestrationService#pagerduty_automation_action}
        '''
        result = self._values.get("pagerduty_automation_action")
        return typing.cast(typing.Optional["EventOrchestrationServiceSetRuleActionsPagerdutyAutomationAction"], result)

    @builtins.property
    def priority(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#priority EventOrchestrationService#priority}.'''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def route_to(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#route_to EventOrchestrationService#route_to}.'''
        result = self._values.get("route_to")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def severity(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#severity EventOrchestrationService#severity}.'''
        result = self._values.get("severity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def suppress(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#suppress EventOrchestrationService#suppress}.'''
        result = self._values.get("suppress")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def suspend(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#suspend EventOrchestrationService#suspend}.'''
        result = self._values.get("suspend")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def variable(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceSetRuleActionsVariable"]]]:
        '''variable block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#variable EventOrchestrationService#variable}
        '''
        result = self._values.get("variable")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceSetRuleActionsVariable"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationServiceSetRuleActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceSetRuleActionsAutomationAction",
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
class EventOrchestrationServiceSetRuleActionsAutomationAction:
    def __init__(
        self,
        *,
        name: builtins.str,
        url: builtins.str,
        auto_send: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationServiceSetRuleActionsAutomationActionHeader", typing.Dict[builtins.str, typing.Any]]]]] = None,
        parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationServiceSetRuleActionsAutomationActionParameter", typing.Dict[builtins.str, typing.Any]]]]] = None,
        trigger_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#name EventOrchestrationService#name}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#url EventOrchestrationService#url}.
        :param auto_send: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#auto_send EventOrchestrationService#auto_send}.
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#header EventOrchestrationService#header}
        :param parameter: parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#parameter EventOrchestrationService#parameter}
        :param trigger_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#trigger_types EventOrchestrationService#trigger_types}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8409c756e9c88bbd47141608bcf02872fa8a893f32dd2996d0d0f430842cefd)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#name EventOrchestrationService#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def url(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#url EventOrchestrationService#url}.'''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auto_send(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#auto_send EventOrchestrationService#auto_send}.'''
        result = self._values.get("auto_send")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def header(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceSetRuleActionsAutomationActionHeader"]]]:
        '''header block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#header EventOrchestrationService#header}
        '''
        result = self._values.get("header")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceSetRuleActionsAutomationActionHeader"]]], result)

    @builtins.property
    def parameter(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceSetRuleActionsAutomationActionParameter"]]]:
        '''parameter block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#parameter EventOrchestrationService#parameter}
        '''
        result = self._values.get("parameter")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceSetRuleActionsAutomationActionParameter"]]], result)

    @builtins.property
    def trigger_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#trigger_types EventOrchestrationService#trigger_types}.'''
        result = self._values.get("trigger_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationServiceSetRuleActionsAutomationAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceSetRuleActionsAutomationActionHeader",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class EventOrchestrationServiceSetRuleActionsAutomationActionHeader:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#key EventOrchestrationService#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#value EventOrchestrationService#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a266dfea797f0686985ed7480dbe6c112195b764c4d37fd6f94389fb233003c)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#key EventOrchestrationService#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#value EventOrchestrationService#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationServiceSetRuleActionsAutomationActionHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationServiceSetRuleActionsAutomationActionHeaderList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceSetRuleActionsAutomationActionHeaderList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0b7affe36b9f06d4c844f6dedc5c998c0d52604ee09f53e361f9af89706bb05)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventOrchestrationServiceSetRuleActionsAutomationActionHeaderOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d59a2b6cbbf93396f3212ad12f145e3d21c1eaa171e87277963630f7a56b34cf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationServiceSetRuleActionsAutomationActionHeaderOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7d0fa1c75c61871d9a9320fd1833f51df896abe11ad7f5b477769214fab9bc0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a498d275380dd0a4a754d77f188fd0a5b606dc1b301246ced6da13ea9c676630)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d2b6d1331bafa65ec5ef99521726d7c44a14d9e72058cd826ca5df1e2e31d3ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRuleActionsAutomationActionHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRuleActionsAutomationActionHeader]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRuleActionsAutomationActionHeader]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89cb4ac9dbd5fe4ee5d6634ca117edeffc8023087094871671e5670b32bfb8b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationServiceSetRuleActionsAutomationActionHeaderOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceSetRuleActionsAutomationActionHeaderOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e307d87a6183a13d1830b97456bb1b4ae8f5ff61c08792a2353ab72d7847c135)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f5bb7381c1d69d89f18f889914b7998aeac94900da5021f61e64948f52126c62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f09f8aef0844542ec02edb61df53effe49f9468971c6b6f871701586de934399)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceSetRuleActionsAutomationActionHeader]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceSetRuleActionsAutomationActionHeader]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceSetRuleActionsAutomationActionHeader]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c100ff7aadd6a03370a5407fb87ed62013bb17bce7a5a45649b8313b08a6f2ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationServiceSetRuleActionsAutomationActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceSetRuleActionsAutomationActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e4e098c4fc91bf4c45d8502b48d25e0307cc7e886219471d3f8dc735d189b6a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putHeader")
    def put_header(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceSetRuleActionsAutomationActionHeader, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6187c208a367afab493d55110a033853cb29d183153fa40c98f5f19bae7e6f9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putHeader", [value]))

    @jsii.member(jsii_name="putParameter")
    def put_parameter(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationServiceSetRuleActionsAutomationActionParameter", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__545057a4a36d026ec1be292a57db8ed35f150410db35ff662ce0b0725ba059fa)
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
    ) -> EventOrchestrationServiceSetRuleActionsAutomationActionHeaderList:
        return typing.cast(EventOrchestrationServiceSetRuleActionsAutomationActionHeaderList, jsii.get(self, "header"))

    @builtins.property
    @jsii.member(jsii_name="parameter")
    def parameter(
        self,
    ) -> "EventOrchestrationServiceSetRuleActionsAutomationActionParameterList":
        return typing.cast("EventOrchestrationServiceSetRuleActionsAutomationActionParameterList", jsii.get(self, "parameter"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRuleActionsAutomationActionHeader]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRuleActionsAutomationActionHeader]]], jsii.get(self, "headerInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="parameterInput")
    def parameter_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceSetRuleActionsAutomationActionParameter"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceSetRuleActionsAutomationActionParameter"]]], jsii.get(self, "parameterInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__e12fe079b6d40f0fca82cf9320f8d7103380e328c47417ef5eec6225c6aa176a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoSend", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__388ca7e60be8f1502ae64bb01b2697b4cc5d42221a70e9a925227e3ee1d78cc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="triggerTypes")
    def trigger_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "triggerTypes"))

    @trigger_types.setter
    def trigger_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba5a5ae8ef9b9f2311d212c9e4714ebc124f35b697d343802ef077deb24c2dd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "url"))

    @url.setter
    def url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a2a38c4f010ee03302af8203716a38a3f74649012dcab840a2681aad80040e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventOrchestrationServiceSetRuleActionsAutomationAction]:
        return typing.cast(typing.Optional[EventOrchestrationServiceSetRuleActionsAutomationAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventOrchestrationServiceSetRuleActionsAutomationAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63246cdd76f31b528fc4b39471f3fd1c6c8ad3500e3964cc39eb996c00c88437)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceSetRuleActionsAutomationActionParameter",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class EventOrchestrationServiceSetRuleActionsAutomationActionParameter:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''
        :param key: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#key EventOrchestrationService#key}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#value EventOrchestrationService#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67d80436ba744c79afdb60856ad38e37577b5c51931653fc782f22e52e25e41e)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#key EventOrchestrationService#key}.'''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#value EventOrchestrationService#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationServiceSetRuleActionsAutomationActionParameter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationServiceSetRuleActionsAutomationActionParameterList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceSetRuleActionsAutomationActionParameterList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1e213f89e7c89d2fc2dafeb99e04800c5725335eaa2ae7193ac9e539fef57c9e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventOrchestrationServiceSetRuleActionsAutomationActionParameterOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b013d32418374a06a309a421a38d53fff4eb881791d214e073e1cae21fa39f88)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationServiceSetRuleActionsAutomationActionParameterOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b0975176433b7bd4521d3bd8aeaf687a0fa1d58a1a2624d7154f2c5cd14fecf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8a4afcbdec4e8460c0fc2ed3c2195a571120d6d66de23dc458d348de5b3e0071)
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
            type_hints = typing.get_type_hints(_typecheckingstub__306038016fceed40affd17000f93ea9efee3d9e97bc688ba12afbd5076554135)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRuleActionsAutomationActionParameter]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRuleActionsAutomationActionParameter]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRuleActionsAutomationActionParameter]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22baf8c306d0e99bc4fc10d13f16e5fc3bb4b185c20e3f10b750cebb497a0a36)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationServiceSetRuleActionsAutomationActionParameterOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceSetRuleActionsAutomationActionParameterOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__91ae38355f8c6efd78eed50304ae5873e755294ea0993bf451d680ff1772f483)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8170ad7111d3a36ada9f2eebddb8e131499175d5cf9f23213804607546506ae4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "key", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f89d18d50bb1b7681cf598ac4b6e2b00a4ff3993dc9e2dde512d460b75062f48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceSetRuleActionsAutomationActionParameter]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceSetRuleActionsAutomationActionParameter]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceSetRuleActionsAutomationActionParameter]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7de10156f1a32bdeda81e6d2044758e1c124ce343b950f9eaeb2ede90005c16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceSetRuleActionsExtraction",
    jsii_struct_bases=[],
    name_mapping={
        "target": "target",
        "regex": "regex",
        "source": "source",
        "template": "template",
    },
)
class EventOrchestrationServiceSetRuleActionsExtraction:
    def __init__(
        self,
        *,
        target: builtins.str,
        regex: typing.Optional[builtins.str] = None,
        source: typing.Optional[builtins.str] = None,
        template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#target EventOrchestrationService#target}.
        :param regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#regex EventOrchestrationService#regex}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#source EventOrchestrationService#source}.
        :param template: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#template EventOrchestrationService#template}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9138b3998b450ceabb3c6ac2921c89d32e2406df0ebe9be0977195617fceb236)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#target EventOrchestrationService#target}.'''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def regex(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#regex EventOrchestrationService#regex}.'''
        result = self._values.get("regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#source EventOrchestrationService#source}.'''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#template EventOrchestrationService#template}.'''
        result = self._values.get("template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationServiceSetRuleActionsExtraction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationServiceSetRuleActionsExtractionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceSetRuleActionsExtractionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__da40c9336f4b9d6c7f6dd256e3fe596499e4e03029514d08e1fc1f9c77f5dc27)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventOrchestrationServiceSetRuleActionsExtractionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fab1f9b7a3c5ef5cacbb5cbc3d9a07fb8dcac83056d596cc14379e0488baba3d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationServiceSetRuleActionsExtractionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1dd5232707e2fc428edddb984e53accf8957144b1a2a00e852c30315281763c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7bc7b219efa2e5180bdb7c281b55a3e9062dc01bd25b843a4dcc85e33d85257c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6090b6676cbcd9c4eb49325e2e7cf2cf5e4dbd5b82fcd41fad7b3284ee4953cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRuleActionsExtraction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRuleActionsExtraction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRuleActionsExtraction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__064873590eff0721971329f3c6df98353ceeac3df837aeebc41f9423b015292e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationServiceSetRuleActionsExtractionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceSetRuleActionsExtractionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c329f3806c7b562d274029ff73edc15c7178468afd2e22083229bf17cedb4b32)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e908f70e88d54ed2b6105bfc869dd2d799d858e36460c0ea80b648de5835d7b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c459760aecf1388a36da672ebf81d0df60a476735d25f8aa0fb5dd5747276c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d28beacea07e5b968d71e7df621d30a0b10ba4b111cb0f5ea907e2f74afc61cd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="template")
    def template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "template"))

    @template.setter
    def template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f0e3d24a3f12d602987708952ab6be8793bd9ef06f210d9611914d998515f06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "template", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceSetRuleActionsExtraction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceSetRuleActionsExtraction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceSetRuleActionsExtraction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc05d00c98121d6bbbf797fc6a75685ac2b2b48d37717b565cc338dd7c485aec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceSetRuleActionsIncidentCustomFieldUpdate",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "value": "value"},
)
class EventOrchestrationServiceSetRuleActionsIncidentCustomFieldUpdate:
    def __init__(self, *, id: builtins.str, value: builtins.str) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#id EventOrchestrationService#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#value EventOrchestrationService#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31f6fe127b5965fad04ba280bc2b0717d92426f136ed60e964ca92c3c58da09a)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "value": value,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#id EventOrchestrationService#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#value EventOrchestrationService#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationServiceSetRuleActionsIncidentCustomFieldUpdate(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationServiceSetRuleActionsIncidentCustomFieldUpdateList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceSetRuleActionsIncidentCustomFieldUpdateList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__04a46e3f60c8f1cbaa855f45141abbcb421c4b60f9738f4c1d0c939edc22a4f4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventOrchestrationServiceSetRuleActionsIncidentCustomFieldUpdateOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f0c8dc90ffb2f1437f2f829307704a2739b0ef2aebf82b15f4bd3fd55730962)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationServiceSetRuleActionsIncidentCustomFieldUpdateOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baee1352b3a3a5a344c7d86b86046b68a9ed502998fde3c0469b7fa061512bfe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d5a9bbe3b304db45653ef1a27fa534750d87aa28fbd99296f3fa983d4f274cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b275d69a69b360a1e7cc2435e62750024a45dbb47b5b64da117e3fa08fcb7732)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRuleActionsIncidentCustomFieldUpdate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRuleActionsIncidentCustomFieldUpdate]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRuleActionsIncidentCustomFieldUpdate]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f42c4449ee9e0137b2b1efecab9a5d7d056c9ec1cdc540c309555071335b29c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationServiceSetRuleActionsIncidentCustomFieldUpdateOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceSetRuleActionsIncidentCustomFieldUpdateOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b76511bc5a3d0e949046fe28350b3e945a560ad47b31818379598d1cf447045)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc5d5717b1ee73fdb0719b97b5bb5f38dd68889acc3b2039d546ac142543daee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0333ebce896d701681164be3cfb8833760df92454178af6c3ab1a058df4f0fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceSetRuleActionsIncidentCustomFieldUpdate]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceSetRuleActionsIncidentCustomFieldUpdate]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceSetRuleActionsIncidentCustomFieldUpdate]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a020f60ebbed77c23be1d976fc5eba6c2fd8c495753f5dbfe85f6d0905dfb77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationServiceSetRuleActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceSetRuleActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__74a2eed5c2f5cbc8119b8237a4b08ca7e8cc3925050e0d33131c0b661c66521c)
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
        header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceSetRuleActionsAutomationActionHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
        parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceSetRuleActionsAutomationActionParameter, typing.Dict[builtins.str, typing.Any]]]]] = None,
        trigger_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#name EventOrchestrationService#name}.
        :param url: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#url EventOrchestrationService#url}.
        :param auto_send: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#auto_send EventOrchestrationService#auto_send}.
        :param header: header block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#header EventOrchestrationService#header}
        :param parameter: parameter block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#parameter EventOrchestrationService#parameter}
        :param trigger_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#trigger_types EventOrchestrationService#trigger_types}.
        '''
        value = EventOrchestrationServiceSetRuleActionsAutomationAction(
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceSetRuleActionsExtraction, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd7c0d6da250f89b4292bed64c6456927aa1737e65197592487bbf0e20abe379)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExtraction", [value]))

    @jsii.member(jsii_name="putIncidentCustomFieldUpdate")
    def put_incident_custom_field_update(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceSetRuleActionsIncidentCustomFieldUpdate, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d19c1ab50576ddbeebbe90961057beff6aa9771c495fa5dfc3df34d9f262c5a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIncidentCustomFieldUpdate", [value]))

    @jsii.member(jsii_name="putPagerdutyAutomationAction")
    def put_pagerduty_automation_action(
        self,
        *,
        action_id: builtins.str,
        trigger_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param action_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#action_id EventOrchestrationService#action_id}.
        :param trigger_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#trigger_types EventOrchestrationService#trigger_types}.
        '''
        value = EventOrchestrationServiceSetRuleActionsPagerdutyAutomationAction(
            action_id=action_id, trigger_types=trigger_types
        )

        return typing.cast(None, jsii.invoke(self, "putPagerdutyAutomationAction", [value]))

    @jsii.member(jsii_name="putVariable")
    def put_variable(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationServiceSetRuleActionsVariable", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c44cea23f6bd3ccf1fdf28af9baffb91dc40f34c6327e1c72684e0d2aa5c1251)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVariable", [value]))

    @jsii.member(jsii_name="resetAnnotate")
    def reset_annotate(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnnotate", []))

    @jsii.member(jsii_name="resetAutomationAction")
    def reset_automation_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAutomationAction", []))

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

    @jsii.member(jsii_name="resetPagerdutyAutomationAction")
    def reset_pagerduty_automation_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPagerdutyAutomationAction", []))

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
    ) -> EventOrchestrationServiceSetRuleActionsAutomationActionOutputReference:
        return typing.cast(EventOrchestrationServiceSetRuleActionsAutomationActionOutputReference, jsii.get(self, "automationAction"))

    @builtins.property
    @jsii.member(jsii_name="extraction")
    def extraction(self) -> EventOrchestrationServiceSetRuleActionsExtractionList:
        return typing.cast(EventOrchestrationServiceSetRuleActionsExtractionList, jsii.get(self, "extraction"))

    @builtins.property
    @jsii.member(jsii_name="incidentCustomFieldUpdate")
    def incident_custom_field_update(
        self,
    ) -> EventOrchestrationServiceSetRuleActionsIncidentCustomFieldUpdateList:
        return typing.cast(EventOrchestrationServiceSetRuleActionsIncidentCustomFieldUpdateList, jsii.get(self, "incidentCustomFieldUpdate"))

    @builtins.property
    @jsii.member(jsii_name="pagerdutyAutomationAction")
    def pagerduty_automation_action(
        self,
    ) -> "EventOrchestrationServiceSetRuleActionsPagerdutyAutomationActionOutputReference":
        return typing.cast("EventOrchestrationServiceSetRuleActionsPagerdutyAutomationActionOutputReference", jsii.get(self, "pagerdutyAutomationAction"))

    @builtins.property
    @jsii.member(jsii_name="variable")
    def variable(self) -> "EventOrchestrationServiceSetRuleActionsVariableList":
        return typing.cast("EventOrchestrationServiceSetRuleActionsVariableList", jsii.get(self, "variable"))

    @builtins.property
    @jsii.member(jsii_name="annotateInput")
    def annotate_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "annotateInput"))

    @builtins.property
    @jsii.member(jsii_name="automationActionInput")
    def automation_action_input(
        self,
    ) -> typing.Optional[EventOrchestrationServiceSetRuleActionsAutomationAction]:
        return typing.cast(typing.Optional[EventOrchestrationServiceSetRuleActionsAutomationAction], jsii.get(self, "automationActionInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRuleActionsExtraction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRuleActionsExtraction]]], jsii.get(self, "extractionInput"))

    @builtins.property
    @jsii.member(jsii_name="incidentCustomFieldUpdateInput")
    def incident_custom_field_update_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRuleActionsIncidentCustomFieldUpdate]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRuleActionsIncidentCustomFieldUpdate]]], jsii.get(self, "incidentCustomFieldUpdateInput"))

    @builtins.property
    @jsii.member(jsii_name="pagerdutyAutomationActionInput")
    def pagerduty_automation_action_input(
        self,
    ) -> typing.Optional["EventOrchestrationServiceSetRuleActionsPagerdutyAutomationAction"]:
        return typing.cast(typing.Optional["EventOrchestrationServiceSetRuleActionsPagerdutyAutomationAction"], jsii.get(self, "pagerdutyAutomationActionInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceSetRuleActionsVariable"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationServiceSetRuleActionsVariable"]]], jsii.get(self, "variableInput"))

    @builtins.property
    @jsii.member(jsii_name="annotate")
    def annotate(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "annotate"))

    @annotate.setter
    def annotate(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a2f96bf0583c6c17889a63fddecaf346a3d54127f1be252d01b516ce7baba87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "annotate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="escalationPolicy")
    def escalation_policy(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "escalationPolicy"))

    @escalation_policy.setter
    def escalation_policy(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d46dd7640bb20e227293ffc2a5d4df407a53ec08f38f23739d1bc09c8e63b9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "escalationPolicy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventAction")
    def event_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventAction"))

    @event_action.setter
    def event_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02139bc93b33ee38fafed1ea1a9b4d9a264bbdd0ecb2a25c22c06b5e27137f33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87180e10b8a037bda15e43dfeca4b7a1ea3e883b3d91fa9ef0cb95420934f752)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routeTo")
    def route_to(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routeTo"))

    @route_to.setter
    def route_to(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__334538c8dc1b91f49f87aeb08541d00383e567a14a28797cde62d6eabc19a754)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeTo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "severity"))

    @severity.setter
    def severity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f65e82a20cec7bf0ba3d892affc09c8af1484544e208e495f492b75972041613)
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
            type_hints = typing.get_type_hints(_typecheckingstub__53189badad9137f52d902abd37d39fde6365afc70bd4a27fdbbe34a558fdef4f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suppress", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="suspend")
    def suspend(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "suspend"))

    @suspend.setter
    def suspend(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afd9da796963054bdbf5a946a5e9d16e276e962b3c599ea26363faf9792459d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suspend", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventOrchestrationServiceSetRuleActions]:
        return typing.cast(typing.Optional[EventOrchestrationServiceSetRuleActions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventOrchestrationServiceSetRuleActions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d4de1fcfccd41d6b78d4e10cf89e4a0eafec3afab04240db585111e12104713)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceSetRuleActionsPagerdutyAutomationAction",
    jsii_struct_bases=[],
    name_mapping={"action_id": "actionId", "trigger_types": "triggerTypes"},
)
class EventOrchestrationServiceSetRuleActionsPagerdutyAutomationAction:
    def __init__(
        self,
        *,
        action_id: builtins.str,
        trigger_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param action_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#action_id EventOrchestrationService#action_id}.
        :param trigger_types: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#trigger_types EventOrchestrationService#trigger_types}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b45c1286128603948566d39c36b5a18e107173c14e9836c53497bfcfa6cb770e)
            check_type(argname="argument action_id", value=action_id, expected_type=type_hints["action_id"])
            check_type(argname="argument trigger_types", value=trigger_types, expected_type=type_hints["trigger_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action_id": action_id,
        }
        if trigger_types is not None:
            self._values["trigger_types"] = trigger_types

    @builtins.property
    def action_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#action_id EventOrchestrationService#action_id}.'''
        result = self._values.get("action_id")
        assert result is not None, "Required property 'action_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def trigger_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#trigger_types EventOrchestrationService#trigger_types}.'''
        result = self._values.get("trigger_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationServiceSetRuleActionsPagerdutyAutomationAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationServiceSetRuleActionsPagerdutyAutomationActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceSetRuleActionsPagerdutyAutomationActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f145ce3a2669a5f06113f96acb12d445cfbbc36a21c8dc5fd5a2e0c96e927db1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetTriggerTypes")
    def reset_trigger_types(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTriggerTypes", []))

    @builtins.property
    @jsii.member(jsii_name="actionIdInput")
    def action_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionIdInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerTypesInput")
    def trigger_types_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "triggerTypesInput"))

    @builtins.property
    @jsii.member(jsii_name="actionId")
    def action_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actionId"))

    @action_id.setter
    def action_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fd3e43a1a7ad6acdc4d203fc97f701c14605c65701058233a57e7f83d384568)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="triggerTypes")
    def trigger_types(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "triggerTypes"))

    @trigger_types.setter
    def trigger_types(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39428ed3556f0d7cdfea7682845147bcde460e2a7f6a6a859b7443ac89ff04de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "triggerTypes", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventOrchestrationServiceSetRuleActionsPagerdutyAutomationAction]:
        return typing.cast(typing.Optional[EventOrchestrationServiceSetRuleActionsPagerdutyAutomationAction], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventOrchestrationServiceSetRuleActionsPagerdutyAutomationAction],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa1e7e2820b462cd124951529d8099f6cae9c60bb0c910fc9047f021eeeb3aab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceSetRuleActionsVariable",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "path": "path", "type": "type", "value": "value"},
)
class EventOrchestrationServiceSetRuleActionsVariable:
    def __init__(
        self,
        *,
        name: builtins.str,
        path: builtins.str,
        type: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#name EventOrchestrationService#name}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#path EventOrchestrationService#path}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#type EventOrchestrationService#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#value EventOrchestrationService#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9632f4e1b4c7828074e1887f22a1e0143e4c315242b0a620ea3afef8607337d)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#name EventOrchestrationService#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#path EventOrchestrationService#path}.'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#type EventOrchestrationService#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#value EventOrchestrationService#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationServiceSetRuleActionsVariable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationServiceSetRuleActionsVariableList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceSetRuleActionsVariableList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__157e59a852f2c88a2451eebb2b980973ba4748a080bb8ac6e3bfd556eb795ae8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventOrchestrationServiceSetRuleActionsVariableOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__849d707d9e722b175b73e7cc0ba48c65c3d798e295f5643647de87f9ade3e88c)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationServiceSetRuleActionsVariableOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6d3b52df54c0b93669c0127a08a6862c95210e8be7fd1fce2fb1f4ba24166d7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__50fd6ee9f21e449197780ade61994602c4506f7533d24a76e5e8587cf5bf5267)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4074839864b179d116a4dbe92a6548acd0a1ba15524aca16ceb8d51598e3857)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRuleActionsVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRuleActionsVariable]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRuleActionsVariable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eedcd81f907e1fb2f533eaa0bbef2f281a642e4a4a251099d9c3a1e099688bb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationServiceSetRuleActionsVariableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceSetRuleActionsVariableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c33c26ac3b6274881156955b5342a0ff7dd1ee2a2260ac3ba8d14bcdc1f97d90)
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
            type_hints = typing.get_type_hints(_typecheckingstub__899a21391a5ff29d00066c6234faf9c97fab4cde47f7a2186a33e5838c37d23c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a180fef2176ea111abad61840d6371a37ddbe44719d6ad54761a17b4cd8c5fe0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d25d5250e404318548b2d22cd79e6ea97e95e518c18c95be37ff1216c5940e59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b02c531fb5aa189841fde91412ec6a5efdab39e86b7b7174547d64f8d8a73f06)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceSetRuleActionsVariable]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceSetRuleActionsVariable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceSetRuleActionsVariable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b395bc847e25e726cb399a74a7a07996888b0028ec5421c4da7aebb52fd6fefc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceSetRuleCondition",
    jsii_struct_bases=[],
    name_mapping={"expression": "expression"},
)
class EventOrchestrationServiceSetRuleCondition:
    def __init__(self, *, expression: builtins.str) -> None:
        '''
        :param expression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#expression EventOrchestrationService#expression}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78c6e1554d173ad12b3039d4110ca671876f66a2b24da2ee61d832b8237bf56e)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expression": expression,
        }

    @builtins.property
    def expression(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#expression EventOrchestrationService#expression}.'''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationServiceSetRuleCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationServiceSetRuleConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceSetRuleConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4202e7b3ca2a71c6f571f570359f185f6143058e326fc74852d82afb7734218)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventOrchestrationServiceSetRuleConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4ddc90e073babf31501302a3d9715f5ccdf1bcba77c335f5221670df5b7fc8f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationServiceSetRuleConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d6408addcbd386269425969fd233bd02672b2dbef6f7fce3e32d83e061793a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__eac5f54b10dd1ff2b7111316c59887562b369d0ba23747e3c919ebd8df6737be)
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
            type_hints = typing.get_type_hints(_typecheckingstub__008fe07658f279a3ca0c14cff5ca31b4743357803cad9eb9f30b903eca46735c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRuleCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRuleCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRuleCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd63c76b983fefec82eda46561a905dd5cdc2a6916463b2861c0cb120a8eabf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationServiceSetRuleConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceSetRuleConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__061961c96f6ae1071258191a3cb6749b8687fb43b577c008b31aae02458dac1d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__832f4858e1000bd1ccb4dd1feaad6d7a96a479636e31f3fd3b24f0f0efcfa202)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceSetRuleCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceSetRuleCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceSetRuleCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ae36541cd6383859c86772b8f9dabc9de344e32f9e1f1b8d58eb86ca54f0cb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationServiceSetRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceSetRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cf05d02861db97ddfb9f85b244e0a452f8286cf54456897e93a86fb67894d0e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventOrchestrationServiceSetRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5071aeba815e497a1926ba2798b21984f3cd79e52d902ba7e2a64bd756f6d99a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationServiceSetRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89b87e388c691f280832fca5193c083b7192c5bf2d1b813637c1f3be21e5ccf8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d93e72c339e7762247bcd31f384ce6184af6a5a40232fcaca9b8a0bfe70ea06c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f328e10231eefbb1ff571b623ed77686e621acbda09aa9ee078ebc30020230e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24594e100a4b3e64b8c1273a5a5f81d8d88f33f9719f81316e4c5bc806643f33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationServiceSetRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationService.EventOrchestrationServiceSetRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1b1026de29f7eaa703929d68be30815e39bbc2ac923bf8a3009851a16c57aef)
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
        automation_action: typing.Optional[typing.Union[EventOrchestrationServiceSetRuleActionsAutomationAction, typing.Dict[builtins.str, typing.Any]]] = None,
        escalation_policy: typing.Optional[builtins.str] = None,
        event_action: typing.Optional[builtins.str] = None,
        extraction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceSetRuleActionsExtraction, typing.Dict[builtins.str, typing.Any]]]]] = None,
        incident_custom_field_update: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceSetRuleActionsIncidentCustomFieldUpdate, typing.Dict[builtins.str, typing.Any]]]]] = None,
        pagerduty_automation_action: typing.Optional[typing.Union[EventOrchestrationServiceSetRuleActionsPagerdutyAutomationAction, typing.Dict[builtins.str, typing.Any]]] = None,
        priority: typing.Optional[builtins.str] = None,
        route_to: typing.Optional[builtins.str] = None,
        severity: typing.Optional[builtins.str] = None,
        suppress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        suspend: typing.Optional[jsii.Number] = None,
        variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceSetRuleActionsVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param annotate: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#annotate EventOrchestrationService#annotate}.
        :param automation_action: automation_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#automation_action EventOrchestrationService#automation_action}
        :param escalation_policy: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#escalation_policy EventOrchestrationService#escalation_policy}.
        :param event_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#event_action EventOrchestrationService#event_action}.
        :param extraction: extraction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#extraction EventOrchestrationService#extraction}
        :param incident_custom_field_update: incident_custom_field_update block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#incident_custom_field_update EventOrchestrationService#incident_custom_field_update}
        :param pagerduty_automation_action: pagerduty_automation_action block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#pagerduty_automation_action EventOrchestrationService#pagerduty_automation_action}
        :param priority: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#priority EventOrchestrationService#priority}.
        :param route_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#route_to EventOrchestrationService#route_to}.
        :param severity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#severity EventOrchestrationService#severity}.
        :param suppress: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#suppress EventOrchestrationService#suppress}.
        :param suspend: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#suspend EventOrchestrationService#suspend}.
        :param variable: variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_service#variable EventOrchestrationService#variable}
        '''
        value = EventOrchestrationServiceSetRuleActions(
            annotate=annotate,
            automation_action=automation_action,
            escalation_policy=escalation_policy,
            event_action=event_action,
            extraction=extraction,
            incident_custom_field_update=incident_custom_field_update,
            pagerduty_automation_action=pagerduty_automation_action,
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceSetRuleCondition, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12b826365b08246a8175b4c8abf5e84b6a4c5f4caab9e580147f4001439dbd85)
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
    def actions(self) -> EventOrchestrationServiceSetRuleActionsOutputReference:
        return typing.cast(EventOrchestrationServiceSetRuleActionsOutputReference, jsii.get(self, "actions"))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> EventOrchestrationServiceSetRuleConditionList:
        return typing.cast(EventOrchestrationServiceSetRuleConditionList, jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(self) -> typing.Optional[EventOrchestrationServiceSetRuleActions]:
        return typing.cast(typing.Optional[EventOrchestrationServiceSetRuleActions], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRuleCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRuleCondition]]], jsii.get(self, "conditionInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__d594e7748eb9da4dac1726a778653074e3842685bcaa41f8ae3e27c17fefb44a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "label"))

    @label.setter
    def label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f69528ccd5f98970bf8b9c99402120df7bc5b5e1336554b54636f65c367e1129)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "label", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceSetRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceSetRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceSetRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5963a98a6a21eeeba56fc5040c8800521d7378e48a7f1e37f154369cadb43bf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "EventOrchestrationService",
    "EventOrchestrationServiceCatchAll",
    "EventOrchestrationServiceCatchAllActions",
    "EventOrchestrationServiceCatchAllActionsAutomationAction",
    "EventOrchestrationServiceCatchAllActionsAutomationActionHeader",
    "EventOrchestrationServiceCatchAllActionsAutomationActionHeaderList",
    "EventOrchestrationServiceCatchAllActionsAutomationActionHeaderOutputReference",
    "EventOrchestrationServiceCatchAllActionsAutomationActionOutputReference",
    "EventOrchestrationServiceCatchAllActionsAutomationActionParameter",
    "EventOrchestrationServiceCatchAllActionsAutomationActionParameterList",
    "EventOrchestrationServiceCatchAllActionsAutomationActionParameterOutputReference",
    "EventOrchestrationServiceCatchAllActionsExtraction",
    "EventOrchestrationServiceCatchAllActionsExtractionList",
    "EventOrchestrationServiceCatchAllActionsExtractionOutputReference",
    "EventOrchestrationServiceCatchAllActionsIncidentCustomFieldUpdate",
    "EventOrchestrationServiceCatchAllActionsIncidentCustomFieldUpdateList",
    "EventOrchestrationServiceCatchAllActionsIncidentCustomFieldUpdateOutputReference",
    "EventOrchestrationServiceCatchAllActionsOutputReference",
    "EventOrchestrationServiceCatchAllActionsPagerdutyAutomationAction",
    "EventOrchestrationServiceCatchAllActionsPagerdutyAutomationActionOutputReference",
    "EventOrchestrationServiceCatchAllActionsVariable",
    "EventOrchestrationServiceCatchAllActionsVariableList",
    "EventOrchestrationServiceCatchAllActionsVariableOutputReference",
    "EventOrchestrationServiceCatchAllOutputReference",
    "EventOrchestrationServiceConfig",
    "EventOrchestrationServiceSet",
    "EventOrchestrationServiceSetList",
    "EventOrchestrationServiceSetOutputReference",
    "EventOrchestrationServiceSetRule",
    "EventOrchestrationServiceSetRuleActions",
    "EventOrchestrationServiceSetRuleActionsAutomationAction",
    "EventOrchestrationServiceSetRuleActionsAutomationActionHeader",
    "EventOrchestrationServiceSetRuleActionsAutomationActionHeaderList",
    "EventOrchestrationServiceSetRuleActionsAutomationActionHeaderOutputReference",
    "EventOrchestrationServiceSetRuleActionsAutomationActionOutputReference",
    "EventOrchestrationServiceSetRuleActionsAutomationActionParameter",
    "EventOrchestrationServiceSetRuleActionsAutomationActionParameterList",
    "EventOrchestrationServiceSetRuleActionsAutomationActionParameterOutputReference",
    "EventOrchestrationServiceSetRuleActionsExtraction",
    "EventOrchestrationServiceSetRuleActionsExtractionList",
    "EventOrchestrationServiceSetRuleActionsExtractionOutputReference",
    "EventOrchestrationServiceSetRuleActionsIncidentCustomFieldUpdate",
    "EventOrchestrationServiceSetRuleActionsIncidentCustomFieldUpdateList",
    "EventOrchestrationServiceSetRuleActionsIncidentCustomFieldUpdateOutputReference",
    "EventOrchestrationServiceSetRuleActionsOutputReference",
    "EventOrchestrationServiceSetRuleActionsPagerdutyAutomationAction",
    "EventOrchestrationServiceSetRuleActionsPagerdutyAutomationActionOutputReference",
    "EventOrchestrationServiceSetRuleActionsVariable",
    "EventOrchestrationServiceSetRuleActionsVariableList",
    "EventOrchestrationServiceSetRuleActionsVariableOutputReference",
    "EventOrchestrationServiceSetRuleCondition",
    "EventOrchestrationServiceSetRuleConditionList",
    "EventOrchestrationServiceSetRuleConditionOutputReference",
    "EventOrchestrationServiceSetRuleList",
    "EventOrchestrationServiceSetRuleOutputReference",
]

publication.publish()

def _typecheckingstub__d08348341dceec64836b9fb2870e446abc537ad52e6577d3f00cce3b2b4c5bc9(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    catch_all: typing.Union[EventOrchestrationServiceCatchAll, typing.Dict[builtins.str, typing.Any]],
    service: builtins.str,
    set: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceSet, typing.Dict[builtins.str, typing.Any]]]],
    enable_event_orchestration_for_service: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__b892f457ef0302b120620940a071657ed5e358ec77fb3778d39ec84273cb55ec(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e46084fbb0dac8b50a00e9ccad8ae950ee1e6db3090453ec68694394b57dfd3f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceSet, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7d3d9ef71f8f1cfb5352b56523a95ea60a202847c4dc3fe0402efc31a269fc2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cba48748c584698416a859fd552b344e64eb341772bc5c0ce9c524a7ae6dc398(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b2b0d7389d27fe2a680eb7bc85d700e3d3d33efb58a82ab17798b81012f13b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b227d67adc0b66eb81065c2e1c6abc53ea00647b286583b69c9b2e24a2d7993a(
    *,
    actions: typing.Union[EventOrchestrationServiceCatchAllActions, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beda496736753331da07674d5c1607aa07ba1c479670cc6ddf2e0acb104b6e1a(
    *,
    annotate: typing.Optional[builtins.str] = None,
    automation_action: typing.Optional[typing.Union[EventOrchestrationServiceCatchAllActionsAutomationAction, typing.Dict[builtins.str, typing.Any]]] = None,
    escalation_policy: typing.Optional[builtins.str] = None,
    event_action: typing.Optional[builtins.str] = None,
    extraction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceCatchAllActionsExtraction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    incident_custom_field_update: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceCatchAllActionsIncidentCustomFieldUpdate, typing.Dict[builtins.str, typing.Any]]]]] = None,
    pagerduty_automation_action: typing.Optional[typing.Union[EventOrchestrationServiceCatchAllActionsPagerdutyAutomationAction, typing.Dict[builtins.str, typing.Any]]] = None,
    priority: typing.Optional[builtins.str] = None,
    route_to: typing.Optional[builtins.str] = None,
    severity: typing.Optional[builtins.str] = None,
    suppress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    suspend: typing.Optional[jsii.Number] = None,
    variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceCatchAllActionsVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__efd5f1e070bb8fd6be2fbc035155fcc33d1d50c82cf65ca64bd88817a497c9d6(
    *,
    name: builtins.str,
    url: builtins.str,
    auto_send: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceCatchAllActionsAutomationActionHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceCatchAllActionsAutomationActionParameter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    trigger_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12d73bf329b31b590843bd447dac4068fb86b0f35560c424dceb75b7523d8348(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cc7bcfc39ed3677c2f9416313a9f15ce1fae793b00746d5653bb3d6f8b5ce93(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aad05e6b5c624ecb9105659a06bfd2a4ba9c8185409e1e7f8fb0e97ca53e61a3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84d997361fa39e02764464043b92c786b9910a275ca12126d245af825ca3803c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7ce513cffae669415d030c2b47a3756fe66da6b22a2a9ad8e3a54c3585d5e90(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb47a705ca522c3d9ba95e97e3aa9fd154f9c7d0b74acc6537549f88777eea1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f76943919149dfb4c4af0e0a694afabdf78fc45b41ce794fca4275d0eb97ba4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceCatchAllActionsAutomationActionHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2e7fefdd2464e472dd0fd1304b3033d418e51a27a857792cf1b8b819d0a0cf3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dff40a8f24d0522e72179af91ae38445505b2de29cd0e63f8ad99fd1c816c08f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4430d32f833017dc62fb01bce25c54079366bb10b3a67637ea3fe300868b82fb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af57416408e219597b3dec5f7377499b5cbef0ce78085893faf5f9fc2b86244b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceCatchAllActionsAutomationActionHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff7cedf1f06dc82c8dba47cb3907b78be58df2a675491b92bfe0f91730183764(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dbbad64dd726b2b9544eecd7568f2711194684870856c8d72fe3c47a8d53402(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceCatchAllActionsAutomationActionHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3f8697d8015d49bf0fcc3adde9dcf02b67f20a8b006f10a79303bf37022a140(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceCatchAllActionsAutomationActionParameter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b36c5532a34a9c9a6d52f97d1ece95b6225a25d945a855560a56de2813d98c2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83124f62a012b7888f47918ac98ad82955941b410df9810f8278c22b11de8363(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b5dca257feece5aa0296bc5c1495fec20af5ac00afa46d6994ed9ec4bff3613(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9d21f3b82013ed5c6a7ccb17997d3335c8bcf508549d07a17d3bb14b10acfce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98aec7455cfaf172c7a1be08fc36c9e714a4d11a2644bbceb222e3ceef70bc07(
    value: typing.Optional[EventOrchestrationServiceCatchAllActionsAutomationAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f77ccf016a5ec27250748c3b8d7d5355a57cb2b23f0da03c4af1fbe0ec6bad4(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb3761323c243fe2b43295ba8360f5c994579a744113a52012a30d59e4bfa6eb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3351980f2e77b126f695f08906f74090032b9657af59e902e558e5cc3fd3fc0e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00b0ace084cab22f3b1ef6df0d8ad8536b8d7008ed3ae19ce51ca6b096a8b8a6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__970d8dcc5e2cb152c98c52ec236d3a6bb961bc4bc84b69595be7b3d0360e0e32(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8a14a696bf92e1c082ee0c39296a587387a51c50668820fa3038d2661d7529b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac34ff5582fa85e662944d802cde427031d9403afaae2102bc82a8c697b2e116(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceCatchAllActionsAutomationActionParameter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9110e7ff690e382564c5ca73e86597fabf8de2c16aa332feac24d2cbc70a9875(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f7947d86c45a39779f08a7dad1dc91065a36f2575c15463db8764212b4622d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50c63310c33cca88b38409ed4d7dee6d8e15b7326345d15b9aefc9dd83e848c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4ca61714f5f83d6fa15a4630675d5aa438c4620f2c051ec03cee9d53331b6d4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceCatchAllActionsAutomationActionParameter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f58412ceaa4b443b64995d85bbe4e834b3498866453b4a02bfde851b48a6d87(
    *,
    target: builtins.str,
    regex: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
    template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f33499a54fa41481cc71417ecbbdf3e9fa1f329e438c60d64e49630dfdccfdf(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e93f6d3492309228dafbec939c7ac8294503f1cbceec374f9a6a030ed408e77f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4497185fae3a44c83b7a335b26d3a12e10511477b0c6fc43c1959c69ec36064f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a22b98f8b92a5cb3f29e9ce9033791392dd726922fa1c176527415c19a12830(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22278744b9b674857b25176abf93e0642b5768216c903f2e416f1921e61c9423(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d10ed1726ec1bdba660d527a81e4eaba3f3ab0e83ec8a4653d3dae8a17924ef(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceCatchAllActionsExtraction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffa68d26fddac64eb2f7ea7f859c64883b68af01f8e4e93dacc489c3ee7bfa8d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1f5afff845d8c3b3b7723aa0364379b420e941ba31f3a9b36d5eec0c3a31bf4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eb10546f056d62f686cca9e4014fcfed9e087f3dd66685409ad1bd721c8c940(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d2f6a47a2f75a6e1a69399e8727597430bd88179c735d9b194f3e9ff5f0828c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53ddd62bdd642450917ca1c8c6423a915bac235572f81b4e0410bcfaa693ba18(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__955d3b2404015c64dc01f453ae8a593f2d9a9788f9d4d7e7283124fecba7dba1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceCatchAllActionsExtraction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01c0a9c05e20146e2fbbf0f5af59e520a0ab811ae8ef69b936a08bfba4f12841(
    *,
    id: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af2e9d21783215883a12a82a16b43cad514ea8b982bbaedf770dc0ff180471f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd85779a67094424f1ad8c5716fe8d59aef933a14295066d6df3387c8844e746(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb7a33de99b8396d0f606d51d456360418441a9f10b29d34fc30ce0c92a63c01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__333491a1b5d1937e52e5ce178b326b78d4f2066b85069501f8ec14cd84ca30a5(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fefc2ace9d08f8dfa42a96c1ee70cbd0138f891f404784e14cfe789d776a7553(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38cc3cd94d58efb4d4f8c7e86724e4c83e08d329ac50ca475adc45a9b878a79b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceCatchAllActionsIncidentCustomFieldUpdate]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c084db4e2919ce91d89472be23915b3181e6e0efac8e81210bb23f4feb65a843(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__382689c1b1146d190f503f7735623845ebe79352f84d6e99003952c461a9ea24(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__811321dcfd3f9c27d81b98cb45814d26e86c3ce1115657a400406d535e563f48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4a5bde59fd077fb13bc3390986492a560ceabb8dfceb5373935f0003db83ae4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceCatchAllActionsIncidentCustomFieldUpdate]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8e4074613d1e8949bb47ade1ca67315a7ff981c5c7ebd3ac9d65a0571e47654(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32dbb53f21524e45be09cfac77f8643db6d56d7d1bf8f6e3aab8adefb452d77f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceCatchAllActionsExtraction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__685fd28b1d68820fb065771a742c2b574663e76fbc7dc6192d2696d61c61fb18(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceCatchAllActionsIncidentCustomFieldUpdate, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7fbac385a3cc6463601d9d52057e415e170b731537a0bac97745cf1ccc1ea8f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceCatchAllActionsVariable, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6068ff5148d7065f07e1849c9b135708e390d307454ddb5b679ed636a38888d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d5d7e3a9e5fbfb4df62bc37ac8b154fc3a9493394a779db7451286ee79c0c99(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82505222497a3807b05b8ae86653bc1267ec13242eddd69bc864fdd2e3a396a8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b8d8c2be25bf4c6dcf31936cd1f576796c1165ea856ad9c1bee59df645a0264(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1cd9d02b6e37f3b61e799d08655481cb8a790f80e967d3a650ae69c670e5d71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04550b07dade91d853fa2f276c5e028c1928fe3a764e553e4998c5a814422f58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db0ca7322be53357bcf11fa0853e4d21b371903f2f003fda3a2b625a4facde73(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89bfbeb9323588c07ecbcab90b87568f6531a82a624ba1dc51739d9f29292280(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16700c79dd19273d3d1ee91d8e9e86dfb200d47cb477abb2bc747e1c6699f37d(
    value: typing.Optional[EventOrchestrationServiceCatchAllActions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36c445cd297e9983fefb5c67dfff11fbb2c473c5aa0a831366f53587769ce7d2(
    *,
    action_id: builtins.str,
    trigger_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c19a2f26e740d4e85341574218ea80011bd6add0a2a885edd95480fc5b99e552(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f69f46e2b7946b74db45f94a894ef6cf882abd02c01d0c9ae78df68de993599(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5667b8032b5a7e88b2ee7db68fb6a9f76c442e8a79f20d170c477392e7b7d3a5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71592b1487987b109a5df7578de2e1a3320c09160d2b399aab6e4f8d4f4c53fa(
    value: typing.Optional[EventOrchestrationServiceCatchAllActionsPagerdutyAutomationAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fdf61e0dc61ba126fbdee02c7fed508a1d24e9330930b98770fd63c46593c81(
    *,
    name: builtins.str,
    path: builtins.str,
    type: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__471b7129eee1c155786eebbb22d07db7d78cf732304bd455763d63c647dfbdb8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f58aa2dddc511da9902979ccd1e2fc28b105926ee2f5d91757741c6c2ad8322a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__651a6813b49ad706a1226d4370493ce1cb5ff09111d487524afc125831f57a11(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__929e4a2e8912ad0bae377ef0b03851c33c0b5468ee88f6ff77d02d26723b6a7a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40847430adc64cb182c04bfa3dd359fec4b6b1c37ce0ff893f18f1ac4a61af34(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__165f347ab0d9518892c2f457f02cc2bf8e52d330dff763f13d8c08d89069a3d7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceCatchAllActionsVariable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7222d931cac9090003d8e1fef21a6d957651e50f50bd0403ff52a0649f94773(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8dd033dd6c502ee38ec2cfd971c748eed5c15791e16e4441931181d7eb306d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1d1229cbcceb2a903b723c3efc5a65d4d35aec1b4796b1841bbe9d8d42d5b9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab75bf8c44e2e797ada09d95034220bfcf00402a422274d71df6b7ba960674dd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__467373559c7b461fba54cc5de6db1e9a6bb615ea893d862fd0b69d1787480f6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12cd43d9a0c2a22ed8519f5a2fc94375c9aefacb455ea6c9b23c1e50b6d7a52a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceCatchAllActionsVariable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c8aea69cfc21d6d60daa10018defd18c8596c87e26caabc75ad3e00f0a9f615(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a304eee8caf4d82eb549418271a8876f8a01abd44c4f79c9de2968cb1f4965bf(
    value: typing.Optional[EventOrchestrationServiceCatchAll],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f651de5f1691568a4b4fa927ecf5771ad962a04758bd1655111cabd9d341034(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    catch_all: typing.Union[EventOrchestrationServiceCatchAll, typing.Dict[builtins.str, typing.Any]],
    service: builtins.str,
    set: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceSet, typing.Dict[builtins.str, typing.Any]]]],
    enable_event_orchestration_for_service: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__831a7daf13fa654b6bfdc2368c67a1c298cf892ebcb126748659f37eddff0eeb(
    *,
    id: builtins.str,
    rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceSetRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a43490d29cbcbb15884ee08506659396ea022805850f947718781b006d00c15(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b535eb9c572d11645c3eb74cff27963b50ae103942c7ae5577bdae8f9ed8683(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a76fc580ad7f75b873038e6eda731949bf641dd0f50572183577abe05b2580d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7657db75e9247e387fba7b6f0e984b40e13130adaaa0b3c7c9c9a69be840e24(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71d2fbdfaaedf19eb739ee7c87e1b86041b6939abb96063c11afd152b382cbb3(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1735431724e4acdd36a77b5ad4859995cf787e2bb89b574504cfb5fc11efebb1(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSet]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d51539ece17bd4bd69b03bfb9dce4df5427c74718658aa814ba13b4de8ecc5b2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4f44f5abfcd24bed3759164541bee1a16375f25a3f1f68c7f619e9a944ce3ab(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceSetRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__196ceb27cec271056c566d70d2aab2aad0b560a4705ffd5c955cd8d9c824f690(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__820e6f19b3056b4f1d8a37cb621335e84b9b59e8e2ec757f415a4d41d4194df6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceSet]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a295a4681da8ad5dd4353d198513715dae734136f36bcfdb0b3d4d588bcd0a4e(
    *,
    actions: typing.Union[EventOrchestrationServiceSetRuleActions, typing.Dict[builtins.str, typing.Any]],
    condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceSetRuleCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    label: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92d01a8d7979022feb679e0e11e8d9988bb013c9596d06df8bd8fe112cf360fa(
    *,
    annotate: typing.Optional[builtins.str] = None,
    automation_action: typing.Optional[typing.Union[EventOrchestrationServiceSetRuleActionsAutomationAction, typing.Dict[builtins.str, typing.Any]]] = None,
    escalation_policy: typing.Optional[builtins.str] = None,
    event_action: typing.Optional[builtins.str] = None,
    extraction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceSetRuleActionsExtraction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    incident_custom_field_update: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceSetRuleActionsIncidentCustomFieldUpdate, typing.Dict[builtins.str, typing.Any]]]]] = None,
    pagerduty_automation_action: typing.Optional[typing.Union[EventOrchestrationServiceSetRuleActionsPagerdutyAutomationAction, typing.Dict[builtins.str, typing.Any]]] = None,
    priority: typing.Optional[builtins.str] = None,
    route_to: typing.Optional[builtins.str] = None,
    severity: typing.Optional[builtins.str] = None,
    suppress: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    suspend: typing.Optional[jsii.Number] = None,
    variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceSetRuleActionsVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8409c756e9c88bbd47141608bcf02872fa8a893f32dd2996d0d0f430842cefd(
    *,
    name: builtins.str,
    url: builtins.str,
    auto_send: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    header: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceSetRuleActionsAutomationActionHeader, typing.Dict[builtins.str, typing.Any]]]]] = None,
    parameter: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceSetRuleActionsAutomationActionParameter, typing.Dict[builtins.str, typing.Any]]]]] = None,
    trigger_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a266dfea797f0686985ed7480dbe6c112195b764c4d37fd6f94389fb233003c(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0b7affe36b9f06d4c844f6dedc5c998c0d52604ee09f53e361f9af89706bb05(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d59a2b6cbbf93396f3212ad12f145e3d21c1eaa171e87277963630f7a56b34cf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7d0fa1c75c61871d9a9320fd1833f51df896abe11ad7f5b477769214fab9bc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a498d275380dd0a4a754d77f188fd0a5b606dc1b301246ced6da13ea9c676630(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2b6d1331bafa65ec5ef99521726d7c44a14d9e72058cd826ca5df1e2e31d3ff(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89cb4ac9dbd5fe4ee5d6634ca117edeffc8023087094871671e5670b32bfb8b6(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRuleActionsAutomationActionHeader]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e307d87a6183a13d1830b97456bb1b4ae8f5ff61c08792a2353ab72d7847c135(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5bb7381c1d69d89f18f889914b7998aeac94900da5021f61e64948f52126c62(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f09f8aef0844542ec02edb61df53effe49f9468971c6b6f871701586de934399(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c100ff7aadd6a03370a5407fb87ed62013bb17bce7a5a45649b8313b08a6f2ea(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceSetRuleActionsAutomationActionHeader]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e4e098c4fc91bf4c45d8502b48d25e0307cc7e886219471d3f8dc735d189b6a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6187c208a367afab493d55110a033853cb29d183153fa40c98f5f19bae7e6f9a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceSetRuleActionsAutomationActionHeader, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__545057a4a36d026ec1be292a57db8ed35f150410db35ff662ce0b0725ba059fa(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceSetRuleActionsAutomationActionParameter, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e12fe079b6d40f0fca82cf9320f8d7103380e328c47417ef5eec6225c6aa176a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__388ca7e60be8f1502ae64bb01b2697b4cc5d42221a70e9a925227e3ee1d78cc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba5a5ae8ef9b9f2311d212c9e4714ebc124f35b697d343802ef077deb24c2dd6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a2a38c4f010ee03302af8203716a38a3f74649012dcab840a2681aad80040e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63246cdd76f31b528fc4b39471f3fd1c6c8ad3500e3964cc39eb996c00c88437(
    value: typing.Optional[EventOrchestrationServiceSetRuleActionsAutomationAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67d80436ba744c79afdb60856ad38e37577b5c51931653fc782f22e52e25e41e(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e213f89e7c89d2fc2dafeb99e04800c5725335eaa2ae7193ac9e539fef57c9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b013d32418374a06a309a421a38d53fff4eb881791d214e073e1cae21fa39f88(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b0975176433b7bd4521d3bd8aeaf687a0fa1d58a1a2624d7154f2c5cd14fecf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a4afcbdec4e8460c0fc2ed3c2195a571120d6d66de23dc458d348de5b3e0071(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__306038016fceed40affd17000f93ea9efee3d9e97bc688ba12afbd5076554135(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22baf8c306d0e99bc4fc10d13f16e5fc3bb4b185c20e3f10b750cebb497a0a36(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRuleActionsAutomationActionParameter]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91ae38355f8c6efd78eed50304ae5873e755294ea0993bf451d680ff1772f483(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8170ad7111d3a36ada9f2eebddb8e131499175d5cf9f23213804607546506ae4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f89d18d50bb1b7681cf598ac4b6e2b00a4ff3993dc9e2dde512d460b75062f48(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7de10156f1a32bdeda81e6d2044758e1c124ce343b950f9eaeb2ede90005c16(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceSetRuleActionsAutomationActionParameter]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9138b3998b450ceabb3c6ac2921c89d32e2406df0ebe9be0977195617fceb236(
    *,
    target: builtins.str,
    regex: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
    template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da40c9336f4b9d6c7f6dd256e3fe596499e4e03029514d08e1fc1f9c77f5dc27(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fab1f9b7a3c5ef5cacbb5cbc3d9a07fb8dcac83056d596cc14379e0488baba3d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1dd5232707e2fc428edddb984e53accf8957144b1a2a00e852c30315281763c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bc7b219efa2e5180bdb7c281b55a3e9062dc01bd25b843a4dcc85e33d85257c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6090b6676cbcd9c4eb49325e2e7cf2cf5e4dbd5b82fcd41fad7b3284ee4953cd(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__064873590eff0721971329f3c6df98353ceeac3df837aeebc41f9423b015292e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRuleActionsExtraction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c329f3806c7b562d274029ff73edc15c7178468afd2e22083229bf17cedb4b32(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e908f70e88d54ed2b6105bfc869dd2d799d858e36460c0ea80b648de5835d7b2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c459760aecf1388a36da672ebf81d0df60a476735d25f8aa0fb5dd5747276c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d28beacea07e5b968d71e7df621d30a0b10ba4b111cb0f5ea907e2f74afc61cd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f0e3d24a3f12d602987708952ab6be8793bd9ef06f210d9611914d998515f06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc05d00c98121d6bbbf797fc6a75685ac2b2b48d37717b565cc338dd7c485aec(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceSetRuleActionsExtraction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31f6fe127b5965fad04ba280bc2b0717d92426f136ed60e964ca92c3c58da09a(
    *,
    id: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04a46e3f60c8f1cbaa855f45141abbcb421c4b60f9738f4c1d0c939edc22a4f4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f0c8dc90ffb2f1437f2f829307704a2739b0ef2aebf82b15f4bd3fd55730962(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baee1352b3a3a5a344c7d86b86046b68a9ed502998fde3c0469b7fa061512bfe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d5a9bbe3b304db45653ef1a27fa534750d87aa28fbd99296f3fa983d4f274cd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b275d69a69b360a1e7cc2435e62750024a45dbb47b5b64da117e3fa08fcb7732(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f42c4449ee9e0137b2b1efecab9a5d7d056c9ec1cdc540c309555071335b29c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRuleActionsIncidentCustomFieldUpdate]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b76511bc5a3d0e949046fe28350b3e945a560ad47b31818379598d1cf447045(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc5d5717b1ee73fdb0719b97b5bb5f38dd68889acc3b2039d546ac142543daee(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0333ebce896d701681164be3cfb8833760df92454178af6c3ab1a058df4f0fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a020f60ebbed77c23be1d976fc5eba6c2fd8c495753f5dbfe85f6d0905dfb77(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceSetRuleActionsIncidentCustomFieldUpdate]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74a2eed5c2f5cbc8119b8237a4b08ca7e8cc3925050e0d33131c0b661c66521c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd7c0d6da250f89b4292bed64c6456927aa1737e65197592487bbf0e20abe379(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceSetRuleActionsExtraction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d19c1ab50576ddbeebbe90961057beff6aa9771c495fa5dfc3df34d9f262c5a4(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceSetRuleActionsIncidentCustomFieldUpdate, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c44cea23f6bd3ccf1fdf28af9baffb91dc40f34c6327e1c72684e0d2aa5c1251(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceSetRuleActionsVariable, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a2f96bf0583c6c17889a63fddecaf346a3d54127f1be252d01b516ce7baba87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d46dd7640bb20e227293ffc2a5d4df407a53ec08f38f23739d1bc09c8e63b9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02139bc93b33ee38fafed1ea1a9b4d9a264bbdd0ecb2a25c22c06b5e27137f33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87180e10b8a037bda15e43dfeca4b7a1ea3e883b3d91fa9ef0cb95420934f752(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__334538c8dc1b91f49f87aeb08541d00383e567a14a28797cde62d6eabc19a754(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f65e82a20cec7bf0ba3d892affc09c8af1484544e208e495f492b75972041613(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53189badad9137f52d902abd37d39fde6365afc70bd4a27fdbbe34a558fdef4f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afd9da796963054bdbf5a946a5e9d16e276e962b3c599ea26363faf9792459d6(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d4de1fcfccd41d6b78d4e10cf89e4a0eafec3afab04240db585111e12104713(
    value: typing.Optional[EventOrchestrationServiceSetRuleActions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b45c1286128603948566d39c36b5a18e107173c14e9836c53497bfcfa6cb770e(
    *,
    action_id: builtins.str,
    trigger_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f145ce3a2669a5f06113f96acb12d445cfbbc36a21c8dc5fd5a2e0c96e927db1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fd3e43a1a7ad6acdc4d203fc97f701c14605c65701058233a57e7f83d384568(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39428ed3556f0d7cdfea7682845147bcde460e2a7f6a6a859b7443ac89ff04de(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa1e7e2820b462cd124951529d8099f6cae9c60bb0c910fc9047f021eeeb3aab(
    value: typing.Optional[EventOrchestrationServiceSetRuleActionsPagerdutyAutomationAction],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9632f4e1b4c7828074e1887f22a1e0143e4c315242b0a620ea3afef8607337d(
    *,
    name: builtins.str,
    path: builtins.str,
    type: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__157e59a852f2c88a2451eebb2b980973ba4748a080bb8ac6e3bfd556eb795ae8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__849d707d9e722b175b73e7cc0ba48c65c3d798e295f5643647de87f9ade3e88c(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6d3b52df54c0b93669c0127a08a6862c95210e8be7fd1fce2fb1f4ba24166d7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50fd6ee9f21e449197780ade61994602c4506f7533d24a76e5e8587cf5bf5267(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4074839864b179d116a4dbe92a6548acd0a1ba15524aca16ceb8d51598e3857(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eedcd81f907e1fb2f533eaa0bbef2f281a642e4a4a251099d9c3a1e099688bb4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRuleActionsVariable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c33c26ac3b6274881156955b5342a0ff7dd1ee2a2260ac3ba8d14bcdc1f97d90(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__899a21391a5ff29d00066c6234faf9c97fab4cde47f7a2186a33e5838c37d23c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a180fef2176ea111abad61840d6371a37ddbe44719d6ad54761a17b4cd8c5fe0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d25d5250e404318548b2d22cd79e6ea97e95e518c18c95be37ff1216c5940e59(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b02c531fb5aa189841fde91412ec6a5efdab39e86b7b7174547d64f8d8a73f06(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b395bc847e25e726cb399a74a7a07996888b0028ec5421c4da7aebb52fd6fefc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceSetRuleActionsVariable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78c6e1554d173ad12b3039d4110ca671876f66a2b24da2ee61d832b8237bf56e(
    *,
    expression: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4202e7b3ca2a71c6f571f570359f185f6143058e326fc74852d82afb7734218(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ddc90e073babf31501302a3d9715f5ccdf1bcba77c335f5221670df5b7fc8f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d6408addcbd386269425969fd233bd02672b2dbef6f7fce3e32d83e061793a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eac5f54b10dd1ff2b7111316c59887562b369d0ba23747e3c919ebd8df6737be(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__008fe07658f279a3ca0c14cff5ca31b4743357803cad9eb9f30b903eca46735c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd63c76b983fefec82eda46561a905dd5cdc2a6916463b2861c0cb120a8eabf7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRuleCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__061961c96f6ae1071258191a3cb6749b8687fb43b577c008b31aae02458dac1d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__832f4858e1000bd1ccb4dd1feaad6d7a96a479636e31f3fd3b24f0f0efcfa202(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ae36541cd6383859c86772b8f9dabc9de344e32f9e1f1b8d58eb86ca54f0cb2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceSetRuleCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cf05d02861db97ddfb9f85b244e0a452f8286cf54456897e93a86fb67894d0e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5071aeba815e497a1926ba2798b21984f3cd79e52d902ba7e2a64bd756f6d99a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89b87e388c691f280832fca5193c083b7192c5bf2d1b813637c1f3be21e5ccf8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d93e72c339e7762247bcd31f384ce6184af6a5a40232fcaca9b8a0bfe70ea06c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f328e10231eefbb1ff571b623ed77686e621acbda09aa9ee078ebc30020230e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24594e100a4b3e64b8c1273a5a5f81d8d88f33f9719f81316e4c5bc806643f33(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationServiceSetRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1b1026de29f7eaa703929d68be30815e39bbc2ac923bf8a3009851a16c57aef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12b826365b08246a8175b4c8abf5e84b6a4c5f4caab9e580147f4001439dbd85(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationServiceSetRuleCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d594e7748eb9da4dac1726a778653074e3842685bcaa41f8ae3e27c17fefb44a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f69528ccd5f98970bf8b9c99402120df7bc5b5e1336554b54636f65c367e1129(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5963a98a6a21eeeba56fc5040c8800521d7378e48a7f1e37f154369cadb43bf9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationServiceSetRule]],
) -> None:
    """Type checking stubs"""
    pass
