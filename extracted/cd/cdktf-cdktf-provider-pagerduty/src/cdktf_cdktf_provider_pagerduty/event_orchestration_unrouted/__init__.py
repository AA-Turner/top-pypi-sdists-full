r'''
# `pagerduty_event_orchestration_unrouted`

Refer to the Terraform Registry for docs: [`pagerduty_event_orchestration_unrouted`](https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted).
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


class EventOrchestrationUnrouted(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationUnrouted.EventOrchestrationUnrouted",
):
    '''Represents a {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted pagerduty_event_orchestration_unrouted}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        catch_all: typing.Union["EventOrchestrationUnroutedCatchAll", typing.Dict[builtins.str, typing.Any]],
        event_orchestration: builtins.str,
        set: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationUnroutedSet", typing.Dict[builtins.str, typing.Any]]]],
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted pagerduty_event_orchestration_unrouted} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param catch_all: catch_all block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#catch_all EventOrchestrationUnrouted#catch_all}
        :param event_orchestration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#event_orchestration EventOrchestrationUnrouted#event_orchestration}.
        :param set: set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#set EventOrchestrationUnrouted#set}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#id EventOrchestrationUnrouted#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8275f256338e5751768f444091a5b8068e8f5bb29eb2d709101305f01c17607c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = EventOrchestrationUnroutedConfig(
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
        '''Generates CDKTF code for importing a EventOrchestrationUnrouted resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the EventOrchestrationUnrouted to import.
        :param import_from_id: The id of the existing EventOrchestrationUnrouted that should be imported. Refer to the {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the EventOrchestrationUnrouted to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbdee9f778de5a90e9bb378e4cc1b309983ef7863d142c414e704d8bad4d4342)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCatchAll")
    def put_catch_all(
        self,
        *,
        actions: typing.Union["EventOrchestrationUnroutedCatchAllActions", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#actions EventOrchestrationUnrouted#actions}
        '''
        value = EventOrchestrationUnroutedCatchAll(actions=actions)

        return typing.cast(None, jsii.invoke(self, "putCatchAll", [value]))

    @jsii.member(jsii_name="putSet")
    def put_set(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationUnroutedSet", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__018d268dee74aace0a2368e3a3adbf56b4e2755ed3460d5e2145d21da93dffa0)
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
    def catch_all(self) -> "EventOrchestrationUnroutedCatchAllOutputReference":
        return typing.cast("EventOrchestrationUnroutedCatchAllOutputReference", jsii.get(self, "catchAll"))

    @builtins.property
    @jsii.member(jsii_name="set")
    def set(self) -> "EventOrchestrationUnroutedSetList":
        return typing.cast("EventOrchestrationUnroutedSetList", jsii.get(self, "set"))

    @builtins.property
    @jsii.member(jsii_name="catchAllInput")
    def catch_all_input(self) -> typing.Optional["EventOrchestrationUnroutedCatchAll"]:
        return typing.cast(typing.Optional["EventOrchestrationUnroutedCatchAll"], jsii.get(self, "catchAllInput"))

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
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationUnroutedSet"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationUnroutedSet"]]], jsii.get(self, "setInput"))

    @builtins.property
    @jsii.member(jsii_name="eventOrchestration")
    def event_orchestration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventOrchestration"))

    @event_orchestration.setter
    def event_orchestration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53e4b0ca3d3f8bc5751e5175370f6ef6493a38a288b88c3ffca9b27ac62dcdc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventOrchestration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b00c652ebc1bf8a813059274a274ccbc4a976e7128d9802ac9d151a7ce4f0f41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationUnrouted.EventOrchestrationUnroutedCatchAll",
    jsii_struct_bases=[],
    name_mapping={"actions": "actions"},
)
class EventOrchestrationUnroutedCatchAll:
    def __init__(
        self,
        *,
        actions: typing.Union["EventOrchestrationUnroutedCatchAllActions", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#actions EventOrchestrationUnrouted#actions}
        '''
        if isinstance(actions, dict):
            actions = EventOrchestrationUnroutedCatchAllActions(**actions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__06f503a56f272d5c2f99e818b6a494953007278b215cf9e8009bc7756d63894c)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
        }

    @builtins.property
    def actions(self) -> "EventOrchestrationUnroutedCatchAllActions":
        '''actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#actions EventOrchestrationUnrouted#actions}
        '''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast("EventOrchestrationUnroutedCatchAllActions", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationUnroutedCatchAll(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationUnrouted.EventOrchestrationUnroutedCatchAllActions",
    jsii_struct_bases=[],
    name_mapping={
        "event_action": "eventAction",
        "extraction": "extraction",
        "severity": "severity",
        "variable": "variable",
    },
)
class EventOrchestrationUnroutedCatchAllActions:
    def __init__(
        self,
        *,
        event_action: typing.Optional[builtins.str] = None,
        extraction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationUnroutedCatchAllActionsExtraction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        severity: typing.Optional[builtins.str] = None,
        variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationUnroutedCatchAllActionsVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param event_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#event_action EventOrchestrationUnrouted#event_action}.
        :param extraction: extraction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#extraction EventOrchestrationUnrouted#extraction}
        :param severity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#severity EventOrchestrationUnrouted#severity}.
        :param variable: variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#variable EventOrchestrationUnrouted#variable}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6574dcb4a0e638aece27cc74f601e14a17d0b4395adc2458762bf0dd9ef29cd)
            check_type(argname="argument event_action", value=event_action, expected_type=type_hints["event_action"])
            check_type(argname="argument extraction", value=extraction, expected_type=type_hints["extraction"])
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
            check_type(argname="argument variable", value=variable, expected_type=type_hints["variable"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if event_action is not None:
            self._values["event_action"] = event_action
        if extraction is not None:
            self._values["extraction"] = extraction
        if severity is not None:
            self._values["severity"] = severity
        if variable is not None:
            self._values["variable"] = variable

    @builtins.property
    def event_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#event_action EventOrchestrationUnrouted#event_action}.'''
        result = self._values.get("event_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extraction(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationUnroutedCatchAllActionsExtraction"]]]:
        '''extraction block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#extraction EventOrchestrationUnrouted#extraction}
        '''
        result = self._values.get("extraction")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationUnroutedCatchAllActionsExtraction"]]], result)

    @builtins.property
    def severity(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#severity EventOrchestrationUnrouted#severity}.'''
        result = self._values.get("severity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def variable(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationUnroutedCatchAllActionsVariable"]]]:
        '''variable block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#variable EventOrchestrationUnrouted#variable}
        '''
        result = self._values.get("variable")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationUnroutedCatchAllActionsVariable"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationUnroutedCatchAllActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationUnrouted.EventOrchestrationUnroutedCatchAllActionsExtraction",
    jsii_struct_bases=[],
    name_mapping={
        "target": "target",
        "regex": "regex",
        "source": "source",
        "template": "template",
    },
)
class EventOrchestrationUnroutedCatchAllActionsExtraction:
    def __init__(
        self,
        *,
        target: builtins.str,
        regex: typing.Optional[builtins.str] = None,
        source: typing.Optional[builtins.str] = None,
        template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#target EventOrchestrationUnrouted#target}.
        :param regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#regex EventOrchestrationUnrouted#regex}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#source EventOrchestrationUnrouted#source}.
        :param template: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#template EventOrchestrationUnrouted#template}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__873057e6f5f2b8466ff463cc0428da1d09eef943c149dc85c306d593a566df69)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#target EventOrchestrationUnrouted#target}.'''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def regex(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#regex EventOrchestrationUnrouted#regex}.'''
        result = self._values.get("regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#source EventOrchestrationUnrouted#source}.'''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#template EventOrchestrationUnrouted#template}.'''
        result = self._values.get("template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationUnroutedCatchAllActionsExtraction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationUnroutedCatchAllActionsExtractionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationUnrouted.EventOrchestrationUnroutedCatchAllActionsExtractionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e0027e63576683e30c8816d4bacdb7fa19e7e06955c20981a00d5b69753b26b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventOrchestrationUnroutedCatchAllActionsExtractionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2c8a4e2bd5d821506986e6c1b7ef02e09cfe36f9835a1b2098161c15040f14f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationUnroutedCatchAllActionsExtractionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__954af6d347c97be0c28756a0911fbdfdaf96e2c519716ea74a10b5287d55ca14)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb9e457abc33e3760870fc13261efc44341d44b54df603440bb35031ccf2c69d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__10a4a6475dfa7e67907bf0e67a89e1366380cb148115d49fb68d484d5230f25e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationUnroutedCatchAllActionsExtraction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationUnroutedCatchAllActionsExtraction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationUnroutedCatchAllActionsExtraction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__619013fd37aff2d18a117c3b3607169e2f96985d8dca86444d23e930482b4e6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationUnroutedCatchAllActionsExtractionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationUnrouted.EventOrchestrationUnroutedCatchAllActionsExtractionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6f097efbed909b984662332fa19b2cff5b615e7429e03e3bf09432ba2383c8d2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ee17cb133954e63108ae95a70a7a0b096a2b4f1cdb443a762760170c8a4f2ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35b1ebaeecf768fbd2da1a915451cc1e8c055420aa74dfb95e8ba0cbe93e6b5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fafc1345d70cccbbf3bd424f6fc27f9975ef6e7ac067f55de9bc210c26f26730)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="template")
    def template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "template"))

    @template.setter
    def template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf268df5daefc13ef41f99344ebe5f03f32861b1cd17f656b3b436b19b7cf262)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "template", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationUnroutedCatchAllActionsExtraction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationUnroutedCatchAllActionsExtraction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationUnroutedCatchAllActionsExtraction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be05d22a23d358c52138241589e59196792ce534f761d38e956c71ada1772dc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationUnroutedCatchAllActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationUnrouted.EventOrchestrationUnroutedCatchAllActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__df4afcc52b90728bc39ba8aead7f054c495cf538a5523c0ec110c2a346cc577f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExtraction")
    def put_extraction(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationUnroutedCatchAllActionsExtraction, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dca0edaf380c2ae04f9a8029200db324145326711199176f420c9ddfd6cb505)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExtraction", [value]))

    @jsii.member(jsii_name="putVariable")
    def put_variable(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationUnroutedCatchAllActionsVariable", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d437d1e56027293873c7a151a3a266d036670f7548385125e8aedfc1d82afa7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVariable", [value]))

    @jsii.member(jsii_name="resetEventAction")
    def reset_event_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventAction", []))

    @jsii.member(jsii_name="resetExtraction")
    def reset_extraction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtraction", []))

    @jsii.member(jsii_name="resetSeverity")
    def reset_severity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeverity", []))

    @jsii.member(jsii_name="resetVariable")
    def reset_variable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVariable", []))

    @builtins.property
    @jsii.member(jsii_name="extraction")
    def extraction(self) -> EventOrchestrationUnroutedCatchAllActionsExtractionList:
        return typing.cast(EventOrchestrationUnroutedCatchAllActionsExtractionList, jsii.get(self, "extraction"))

    @builtins.property
    @jsii.member(jsii_name="suppress")
    def suppress(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "suppress"))

    @builtins.property
    @jsii.member(jsii_name="variable")
    def variable(self) -> "EventOrchestrationUnroutedCatchAllActionsVariableList":
        return typing.cast("EventOrchestrationUnroutedCatchAllActionsVariableList", jsii.get(self, "variable"))

    @builtins.property
    @jsii.member(jsii_name="eventActionInput")
    def event_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventActionInput"))

    @builtins.property
    @jsii.member(jsii_name="extractionInput")
    def extraction_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationUnroutedCatchAllActionsExtraction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationUnroutedCatchAllActionsExtraction]]], jsii.get(self, "extractionInput"))

    @builtins.property
    @jsii.member(jsii_name="severityInput")
    def severity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "severityInput"))

    @builtins.property
    @jsii.member(jsii_name="variableInput")
    def variable_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationUnroutedCatchAllActionsVariable"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationUnroutedCatchAllActionsVariable"]]], jsii.get(self, "variableInput"))

    @builtins.property
    @jsii.member(jsii_name="eventAction")
    def event_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventAction"))

    @event_action.setter
    def event_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19be63d73a870f653dab26f5c94daff0eed587619e15e3e30bb1f71bab0b49a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "severity"))

    @severity.setter
    def severity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfd00bb58d0830780fbeda8396f16d666b3069bad231c7f98b714bb287710bb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "severity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventOrchestrationUnroutedCatchAllActions]:
        return typing.cast(typing.Optional[EventOrchestrationUnroutedCatchAllActions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventOrchestrationUnroutedCatchAllActions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0624943abcc45135d61d7e71399afbd62ce94d725dcf47414d95b6b88c7d236)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationUnrouted.EventOrchestrationUnroutedCatchAllActionsVariable",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "path": "path", "type": "type", "value": "value"},
)
class EventOrchestrationUnroutedCatchAllActionsVariable:
    def __init__(
        self,
        *,
        name: builtins.str,
        path: builtins.str,
        type: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#name EventOrchestrationUnrouted#name}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#path EventOrchestrationUnrouted#path}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#type EventOrchestrationUnrouted#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#value EventOrchestrationUnrouted#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d16718dd84c51311e04997b4675de9db9aec5dd9d5debae2b5d98162b78bced)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#name EventOrchestrationUnrouted#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#path EventOrchestrationUnrouted#path}.'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#type EventOrchestrationUnrouted#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#value EventOrchestrationUnrouted#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationUnroutedCatchAllActionsVariable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationUnroutedCatchAllActionsVariableList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationUnrouted.EventOrchestrationUnroutedCatchAllActionsVariableList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__69a49b662949a36b0ffaf8895b79d623f8a36f496ad6177721f4250810615f52)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventOrchestrationUnroutedCatchAllActionsVariableOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1380b93653f78fe6914bca9ec71c8bfdccadbaa30099e9500246c38c561e981b)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationUnroutedCatchAllActionsVariableOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3a7f4af5291f0265269958f1c6d1ca638ba28bb43a31319634d8e36cdc20a96)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a6addc45164afaf9240265f0cfe96ec481f3f03027622ac244c6908af1391a6e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1870fe5e1dbee87c2f3945f4550be60a344c74b44aeb47ebc6bf9adddb1ebaf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationUnroutedCatchAllActionsVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationUnroutedCatchAllActionsVariable]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationUnroutedCatchAllActionsVariable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cd2958db1c59646663d2cfb6a7ed94596f5a43dc1b1563332270b30c74ea5c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationUnroutedCatchAllActionsVariableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationUnrouted.EventOrchestrationUnroutedCatchAllActionsVariableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__196e18aa7284a5aea561ffa32ea04f9e17096b827a372bee1e24c642dcce6ce2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__514cc3738b0757e7a17486c13d2f38cb98a40de470cea5affcdb2147511ebae7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ab8d960654895992ab0db79d7ee8f58161e4d5484cc1f7821a02c84a70ce02e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f47cef1ec88628b76c3724948de8f1af50a92b08adc0a2220982b81358555d15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba93494ae89f53068f3bf4b8bba7f0b7538cd4ee201548535a7a5e44580d8d87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationUnroutedCatchAllActionsVariable]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationUnroutedCatchAllActionsVariable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationUnroutedCatchAllActionsVariable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeca7d344c747657fb4d8c34ad118a33707e209b6bb1f1f897cdd7b1fc4e300e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationUnroutedCatchAllOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationUnrouted.EventOrchestrationUnroutedCatchAllOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__dd8aa5ad6f8ff58a49d792a41b1505092c30f86f07f621704000df770e53ead3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putActions")
    def put_actions(
        self,
        *,
        event_action: typing.Optional[builtins.str] = None,
        extraction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationUnroutedCatchAllActionsExtraction, typing.Dict[builtins.str, typing.Any]]]]] = None,
        severity: typing.Optional[builtins.str] = None,
        variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationUnroutedCatchAllActionsVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param event_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#event_action EventOrchestrationUnrouted#event_action}.
        :param extraction: extraction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#extraction EventOrchestrationUnrouted#extraction}
        :param severity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#severity EventOrchestrationUnrouted#severity}.
        :param variable: variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#variable EventOrchestrationUnrouted#variable}
        '''
        value = EventOrchestrationUnroutedCatchAllActions(
            event_action=event_action,
            extraction=extraction,
            severity=severity,
            variable=variable,
        )

        return typing.cast(None, jsii.invoke(self, "putActions", [value]))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> EventOrchestrationUnroutedCatchAllActionsOutputReference:
        return typing.cast(EventOrchestrationUnroutedCatchAllActionsOutputReference, jsii.get(self, "actions"))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(
        self,
    ) -> typing.Optional[EventOrchestrationUnroutedCatchAllActions]:
        return typing.cast(typing.Optional[EventOrchestrationUnroutedCatchAllActions], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EventOrchestrationUnroutedCatchAll]:
        return typing.cast(typing.Optional[EventOrchestrationUnroutedCatchAll], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventOrchestrationUnroutedCatchAll],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7845e0940d40b2a61bc15180a1f421c130c26f83a4338490932e8c7b5734ae94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationUnrouted.EventOrchestrationUnroutedConfig",
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
class EventOrchestrationUnroutedConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        catch_all: typing.Union[EventOrchestrationUnroutedCatchAll, typing.Dict[builtins.str, typing.Any]],
        event_orchestration: builtins.str,
        set: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationUnroutedSet", typing.Dict[builtins.str, typing.Any]]]],
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
        :param catch_all: catch_all block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#catch_all EventOrchestrationUnrouted#catch_all}
        :param event_orchestration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#event_orchestration EventOrchestrationUnrouted#event_orchestration}.
        :param set: set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#set EventOrchestrationUnrouted#set}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#id EventOrchestrationUnrouted#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(catch_all, dict):
            catch_all = EventOrchestrationUnroutedCatchAll(**catch_all)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3337998421b1ba5b03def6960dc3e2a48bb7c187bc08eb62a67d24c843f57849)
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
    def catch_all(self) -> EventOrchestrationUnroutedCatchAll:
        '''catch_all block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#catch_all EventOrchestrationUnrouted#catch_all}
        '''
        result = self._values.get("catch_all")
        assert result is not None, "Required property 'catch_all' is missing"
        return typing.cast(EventOrchestrationUnroutedCatchAll, result)

    @builtins.property
    def event_orchestration(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#event_orchestration EventOrchestrationUnrouted#event_orchestration}.'''
        result = self._values.get("event_orchestration")
        assert result is not None, "Required property 'event_orchestration' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def set(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationUnroutedSet"]]:
        '''set block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#set EventOrchestrationUnrouted#set}
        '''
        result = self._values.get("set")
        assert result is not None, "Required property 'set' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationUnroutedSet"]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#id EventOrchestrationUnrouted#id}.

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
        return "EventOrchestrationUnroutedConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationUnrouted.EventOrchestrationUnroutedSet",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "rule": "rule"},
)
class EventOrchestrationUnroutedSet:
    def __init__(
        self,
        *,
        id: builtins.str,
        rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationUnroutedSetRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#id EventOrchestrationUnrouted#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#rule EventOrchestrationUnrouted#rule}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d008f014806e1f881fbd832e0f0859fbb79a6023defe775d45620826b97169c9)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if rule is not None:
            self._values["rule"] = rule

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#id EventOrchestrationUnrouted#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationUnroutedSetRule"]]]:
        '''rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#rule EventOrchestrationUnrouted#rule}
        '''
        result = self._values.get("rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationUnroutedSetRule"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationUnroutedSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationUnroutedSetList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationUnrouted.EventOrchestrationUnroutedSetList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__27dac7bee1374e8a6d71d3f8cce1a731b40501dcfd907d6b450b6a02ac1972af)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "EventOrchestrationUnroutedSetOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2060c8b4fca371bffa9b2df36d1e227d5dcf27b3446f716d4b8c8a45aee387ce)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationUnroutedSetOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__589426e4a6f278f25cef6b077fe3944ec855cde428e0ad25b062d5993a83795a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fdfe9b29d400ad94627041edb8dc8a65f238a5e3513a2a369f41a71c699e7fc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d957f5fc025a8f93d8c2ea7ae2be6e19fd3784db7d25bf5f71f7e43daf5676a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationUnroutedSet]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationUnroutedSet]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationUnroutedSet]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddec66fccb4a0cf0ae4c523cc4c7797124e47a62794d2fd225f2772b1492c286)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationUnroutedSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationUnrouted.EventOrchestrationUnroutedSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__034de521d11fde7f36cdcb6a8b289dd3d4abff7a4828961701e694c5b9c0f996)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putRule")
    def put_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationUnroutedSetRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14096c8150d9cf77ab0422f25e18773a63486679ea7582931560905ae6cd495c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRule", [value]))

    @jsii.member(jsii_name="resetRule")
    def reset_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRule", []))

    @builtins.property
    @jsii.member(jsii_name="rule")
    def rule(self) -> "EventOrchestrationUnroutedSetRuleList":
        return typing.cast("EventOrchestrationUnroutedSetRuleList", jsii.get(self, "rule"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleInput")
    def rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationUnroutedSetRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationUnroutedSetRule"]]], jsii.get(self, "ruleInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66b860a7db2b579877641045d626773900a3c8eba1097bb0820a6234667cff10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationUnroutedSet]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationUnroutedSet]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationUnroutedSet]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9549d3aadf2e2a27d807dd15f5295d14a41d0175cdf12e7999b9ae8907844c65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationUnrouted.EventOrchestrationUnroutedSetRule",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "condition": "condition",
        "disabled": "disabled",
        "label": "label",
    },
)
class EventOrchestrationUnroutedSetRule:
    def __init__(
        self,
        *,
        actions: typing.Union["EventOrchestrationUnroutedSetRuleActions", typing.Dict[builtins.str, typing.Any]],
        condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationUnroutedSetRuleCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        label: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#actions EventOrchestrationUnrouted#actions}
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#condition EventOrchestrationUnrouted#condition}
        :param disabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#disabled EventOrchestrationUnrouted#disabled}.
        :param label: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#label EventOrchestrationUnrouted#label}.
        '''
        if isinstance(actions, dict):
            actions = EventOrchestrationUnroutedSetRuleActions(**actions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90f64f64a017d7112db8e5120d1e7674247f6faf8869d10751346f3ec813dbba)
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
    def actions(self) -> "EventOrchestrationUnroutedSetRuleActions":
        '''actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#actions EventOrchestrationUnrouted#actions}
        '''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast("EventOrchestrationUnroutedSetRuleActions", result)

    @builtins.property
    def condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationUnroutedSetRuleCondition"]]]:
        '''condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#condition EventOrchestrationUnrouted#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationUnroutedSetRuleCondition"]]], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#disabled EventOrchestrationUnrouted#disabled}.'''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#label EventOrchestrationUnrouted#label}.'''
        result = self._values.get("label")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationUnroutedSetRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationUnrouted.EventOrchestrationUnroutedSetRuleActions",
    jsii_struct_bases=[],
    name_mapping={
        "event_action": "eventAction",
        "extraction": "extraction",
        "route_to": "routeTo",
        "severity": "severity",
        "variable": "variable",
    },
)
class EventOrchestrationUnroutedSetRuleActions:
    def __init__(
        self,
        *,
        event_action: typing.Optional[builtins.str] = None,
        extraction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationUnroutedSetRuleActionsExtraction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        route_to: typing.Optional[builtins.str] = None,
        severity: typing.Optional[builtins.str] = None,
        variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationUnroutedSetRuleActionsVariable", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param event_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#event_action EventOrchestrationUnrouted#event_action}.
        :param extraction: extraction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#extraction EventOrchestrationUnrouted#extraction}
        :param route_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#route_to EventOrchestrationUnrouted#route_to}.
        :param severity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#severity EventOrchestrationUnrouted#severity}.
        :param variable: variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#variable EventOrchestrationUnrouted#variable}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7de69daeae1a5cd1a1063bd644434991e938ef8d905f1e00d5b411fef8b3a529)
            check_type(argname="argument event_action", value=event_action, expected_type=type_hints["event_action"])
            check_type(argname="argument extraction", value=extraction, expected_type=type_hints["extraction"])
            check_type(argname="argument route_to", value=route_to, expected_type=type_hints["route_to"])
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
            check_type(argname="argument variable", value=variable, expected_type=type_hints["variable"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if event_action is not None:
            self._values["event_action"] = event_action
        if extraction is not None:
            self._values["extraction"] = extraction
        if route_to is not None:
            self._values["route_to"] = route_to
        if severity is not None:
            self._values["severity"] = severity
        if variable is not None:
            self._values["variable"] = variable

    @builtins.property
    def event_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#event_action EventOrchestrationUnrouted#event_action}.'''
        result = self._values.get("event_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def extraction(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationUnroutedSetRuleActionsExtraction"]]]:
        '''extraction block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#extraction EventOrchestrationUnrouted#extraction}
        '''
        result = self._values.get("extraction")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationUnroutedSetRuleActionsExtraction"]]], result)

    @builtins.property
    def route_to(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#route_to EventOrchestrationUnrouted#route_to}.'''
        result = self._values.get("route_to")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def severity(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#severity EventOrchestrationUnrouted#severity}.'''
        result = self._values.get("severity")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def variable(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationUnroutedSetRuleActionsVariable"]]]:
        '''variable block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#variable EventOrchestrationUnrouted#variable}
        '''
        result = self._values.get("variable")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationUnroutedSetRuleActionsVariable"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationUnroutedSetRuleActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationUnrouted.EventOrchestrationUnroutedSetRuleActionsExtraction",
    jsii_struct_bases=[],
    name_mapping={
        "target": "target",
        "regex": "regex",
        "source": "source",
        "template": "template",
    },
)
class EventOrchestrationUnroutedSetRuleActionsExtraction:
    def __init__(
        self,
        *,
        target: builtins.str,
        regex: typing.Optional[builtins.str] = None,
        source: typing.Optional[builtins.str] = None,
        template: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param target: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#target EventOrchestrationUnrouted#target}.
        :param regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#regex EventOrchestrationUnrouted#regex}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#source EventOrchestrationUnrouted#source}.
        :param template: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#template EventOrchestrationUnrouted#template}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b3013dd35226ec76dc2f09e9719e1c12966fdd5323214ccba59c06037e0e915)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#target EventOrchestrationUnrouted#target}.'''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def regex(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#regex EventOrchestrationUnrouted#regex}.'''
        result = self._values.get("regex")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#source EventOrchestrationUnrouted#source}.'''
        result = self._values.get("source")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#template EventOrchestrationUnrouted#template}.'''
        result = self._values.get("template")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationUnroutedSetRuleActionsExtraction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationUnroutedSetRuleActionsExtractionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationUnrouted.EventOrchestrationUnroutedSetRuleActionsExtractionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b5ba409596cf7458e3df246b3027fe9ec592a34c20638922a72259b76af8735)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventOrchestrationUnroutedSetRuleActionsExtractionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d8d7a2bcbf08049c18b3816e0abbea800b1ba2c505c436d3ec3c7cdfe3ca2a5)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationUnroutedSetRuleActionsExtractionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe5367753a7f9176ec09d326b2e3285af7417505ef30b9abb14fbd1c0545316a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5920f18d561fff2aa0285aaebc7fcf2173233ba8ae7a35ebaa159ef2db5d5abe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__66a3846ecdd940034b38502a27a804a4cc9cba57740ac075957b6dfc85b64ae8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationUnroutedSetRuleActionsExtraction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationUnroutedSetRuleActionsExtraction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationUnroutedSetRuleActionsExtraction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0ddec5465e9dd8c4635ef2f4fcc42b709c8a4a80c9891ac1147c39ec1b786b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationUnroutedSetRuleActionsExtractionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationUnrouted.EventOrchestrationUnroutedSetRuleActionsExtractionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a0f4866a14ef5d5072c18ed875a0de10ebac1f9b9937503f4c26f5383f3aca4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__218b77d250f7488272c6687fa4af89330b0d9ee114e66eee0395cc11c6662a91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4d5aa72bf6b2ca3a515b908c319b06f5806e844dd126c208ab37e488be83d94)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @target.setter
    def target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2f5193c00bbb1c792c7ce2c8c0fe9b1ce12b7e6608712130c60d6f6e8699730)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "target", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="template")
    def template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "template"))

    @template.setter
    def template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c54a36ec938b57bc01e6ddd9ccae6c1ea8e3b8824fc1ef1f2c860f938b793b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "template", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationUnroutedSetRuleActionsExtraction]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationUnroutedSetRuleActionsExtraction]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationUnroutedSetRuleActionsExtraction]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fc553cc1c300a70de0ab2da830e9ee63f911336d697a50b6207d1e3ce06fe77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationUnroutedSetRuleActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationUnrouted.EventOrchestrationUnroutedSetRuleActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__060d73ba53830954fb97a051575dbd2589ebf9dc5edb52afec2cebb3e361f168)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putExtraction")
    def put_extraction(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationUnroutedSetRuleActionsExtraction, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcac8d5312b10e6ad6ba79da0d02e87bdcdf3d2127986c97eb07afcecc9fdffd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putExtraction", [value]))

    @jsii.member(jsii_name="putVariable")
    def put_variable(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationUnroutedSetRuleActionsVariable", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17c35ea486dbcb50b9de002b68d378f59a50806975cd173e828f77c0e89a4de1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putVariable", [value]))

    @jsii.member(jsii_name="resetEventAction")
    def reset_event_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventAction", []))

    @jsii.member(jsii_name="resetExtraction")
    def reset_extraction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetExtraction", []))

    @jsii.member(jsii_name="resetRouteTo")
    def reset_route_to(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRouteTo", []))

    @jsii.member(jsii_name="resetSeverity")
    def reset_severity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeverity", []))

    @jsii.member(jsii_name="resetVariable")
    def reset_variable(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetVariable", []))

    @builtins.property
    @jsii.member(jsii_name="extraction")
    def extraction(self) -> EventOrchestrationUnroutedSetRuleActionsExtractionList:
        return typing.cast(EventOrchestrationUnroutedSetRuleActionsExtractionList, jsii.get(self, "extraction"))

    @builtins.property
    @jsii.member(jsii_name="variable")
    def variable(self) -> "EventOrchestrationUnroutedSetRuleActionsVariableList":
        return typing.cast("EventOrchestrationUnroutedSetRuleActionsVariableList", jsii.get(self, "variable"))

    @builtins.property
    @jsii.member(jsii_name="eventActionInput")
    def event_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventActionInput"))

    @builtins.property
    @jsii.member(jsii_name="extractionInput")
    def extraction_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationUnroutedSetRuleActionsExtraction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationUnroutedSetRuleActionsExtraction]]], jsii.get(self, "extractionInput"))

    @builtins.property
    @jsii.member(jsii_name="routeToInput")
    def route_to_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routeToInput"))

    @builtins.property
    @jsii.member(jsii_name="severityInput")
    def severity_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "severityInput"))

    @builtins.property
    @jsii.member(jsii_name="variableInput")
    def variable_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationUnroutedSetRuleActionsVariable"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationUnroutedSetRuleActionsVariable"]]], jsii.get(self, "variableInput"))

    @builtins.property
    @jsii.member(jsii_name="eventAction")
    def event_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventAction"))

    @event_action.setter
    def event_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1723f97a85f09bf3944806bae183cfc27c526b848ed12c4c8e125d9a2251ead)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventAction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="routeTo")
    def route_to(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routeTo"))

    @route_to.setter
    def route_to(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39fe95870492f0e1b093afe8831231caab3ccf368dd09414f2196ca3a737d296)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeTo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "severity"))

    @severity.setter
    def severity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bb14685b0386392b6aa0c1d71acb035260657ef724bf5b4365d11eda37a17d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "severity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventOrchestrationUnroutedSetRuleActions]:
        return typing.cast(typing.Optional[EventOrchestrationUnroutedSetRuleActions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventOrchestrationUnroutedSetRuleActions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__427529fd67ee11028870e05d50549fabe448fdf16073724786ecbcfaccc64a82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationUnrouted.EventOrchestrationUnroutedSetRuleActionsVariable",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "path": "path", "type": "type", "value": "value"},
)
class EventOrchestrationUnroutedSetRuleActionsVariable:
    def __init__(
        self,
        *,
        name: builtins.str,
        path: builtins.str,
        type: builtins.str,
        value: builtins.str,
    ) -> None:
        '''
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#name EventOrchestrationUnrouted#name}.
        :param path: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#path EventOrchestrationUnrouted#path}.
        :param type: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#type EventOrchestrationUnrouted#type}.
        :param value: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#value EventOrchestrationUnrouted#value}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd0c5f57df347bcae15394cd70a29867473ac8aa3688e6f0dc355fc21a2ef2d8)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#name EventOrchestrationUnrouted#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#path EventOrchestrationUnrouted#path}.'''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#type EventOrchestrationUnrouted#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#value EventOrchestrationUnrouted#value}.'''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationUnroutedSetRuleActionsVariable(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationUnroutedSetRuleActionsVariableList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationUnrouted.EventOrchestrationUnroutedSetRuleActionsVariableList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4edd0e7e73a8fb39569de97506fd9f55fd448720c532e4207b9ecdb84e31da6e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventOrchestrationUnroutedSetRuleActionsVariableOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2ddf8b2a45e89e86e9e46569f7dedb775adc3ac181d7904793c98f43ec75676)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationUnroutedSetRuleActionsVariableOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__722825992fcb1853144b603822ca88e63b97607df16fd008037da2b8ecacdb41)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ddb24cf319f30935b5696581bd93424cc627c068f7f8341df59a92bb15f13d4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__52aa34464eac9ca489253376eb0d9ed5b380d8082fb95972d66c996312fb26b7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationUnroutedSetRuleActionsVariable]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationUnroutedSetRuleActionsVariable]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationUnroutedSetRuleActionsVariable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b2a40f82c6f75b06f1f5280a872b4df3220e18095fdee32938685b5af6c977b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationUnroutedSetRuleActionsVariableOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationUnrouted.EventOrchestrationUnroutedSetRuleActionsVariableOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0194ee5442517143811b4a4870649cbbbad62551fec68a1d9bbdcd49cac97d29)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0e3f5a741892ad226203f465bf55ecbe9147ae32e4ad1e3e3caf652f63ed2d86)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__693ec9ab33827be2c1ed28dd0ef461d2a187126bb4311b1e596c059e4822fecc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__696bac573c81714669a3c7b5a3ba20a6bc3dd38a66ed856cb0794bf66b1efe6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8edc9be515059c450c2c4c1ffa2fc90302988f2362990f7c5a4c95ebcbb316e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationUnroutedSetRuleActionsVariable]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationUnroutedSetRuleActionsVariable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationUnroutedSetRuleActionsVariable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65a142b41cb3d7e2279f4448e7771aa9d8e691ee7f14b1fa794c0d08f8a893c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationUnrouted.EventOrchestrationUnroutedSetRuleCondition",
    jsii_struct_bases=[],
    name_mapping={"expression": "expression"},
)
class EventOrchestrationUnroutedSetRuleCondition:
    def __init__(self, *, expression: builtins.str) -> None:
        '''
        :param expression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#expression EventOrchestrationUnrouted#expression}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e07b5dc138d66b32d7ebe6a7836500090439b0c193c8ab86ebe5120b056af3f)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expression": expression,
        }

    @builtins.property
    def expression(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#expression EventOrchestrationUnrouted#expression}.'''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationUnroutedSetRuleCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationUnroutedSetRuleConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationUnrouted.EventOrchestrationUnroutedSetRuleConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4803e1fd51a51e8626ad7d5f61fd462c2dbbcf7f85db4d5558bd57677cbb0bc0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventOrchestrationUnroutedSetRuleConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d2660f40645bd0b0dc91bcfed005e1a378ef8130d9117565e126bd3a2e796c3)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationUnroutedSetRuleConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8cab0c348e39d936624ccc0f614f2331e90d074238c95787027f044b5fa946f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b595a3fe589a322e0a70256437066e756c68e1a6c3012f92f9c145dc94c9fd11)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b1398556532a535c621bf360035898fa93e16ae08052e8b256e945dfe9bfb226)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationUnroutedSetRuleCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationUnroutedSetRuleCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationUnroutedSetRuleCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75a0955b97a4a8b8c7ce55ec6863f0651da1bf09c7bbc27ee7bbf55a0cf531d4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationUnroutedSetRuleConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationUnrouted.EventOrchestrationUnroutedSetRuleConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8c6b126f665ec40ce74d76aee4719855e7d93a1ecd724de349314253d004000)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8bc8ed6780b3ff240166da8fdd6209682ef85daf829e724c27011158f5181401)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationUnroutedSetRuleCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationUnroutedSetRuleCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationUnroutedSetRuleCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b99d5a1b09ad5c0b230f6e39109def4c7ec44b1a3cbba9e36af42525fef1d6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationUnroutedSetRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationUnrouted.EventOrchestrationUnroutedSetRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__eb3bf60f3d6a317e2b0dcc02da6c920558c65b8ed5e6fee67fe8f5d889853faa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventOrchestrationUnroutedSetRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d1b1c69108c8e0a254db050e1e6700b17f76e2d7d972056ce8fbfcfcff05ce4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationUnroutedSetRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98a443f869641f970b84e36283c92ec6e5ce176678792404ea9bf74a1dd30f8d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b11371214d8877555d458cc710371c5d7e4ef12141373b90066e34259c05544)
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
            type_hints = typing.get_type_hints(_typecheckingstub__16fc637d8dba6acb5945a873415b60ab44b3fdcee39a78a1f64af4edb6236225)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationUnroutedSetRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationUnroutedSetRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationUnroutedSetRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63557a88b911c664e57c8c44775c20d9d3b983a15be732ab6e24a542896d5916)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationUnroutedSetRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationUnrouted.EventOrchestrationUnroutedSetRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2396bf7f2a77cc24dfba04a370a6dbdd982a781e3923505d1de47940271f09a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putActions")
    def put_actions(
        self,
        *,
        event_action: typing.Optional[builtins.str] = None,
        extraction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationUnroutedSetRuleActionsExtraction, typing.Dict[builtins.str, typing.Any]]]]] = None,
        route_to: typing.Optional[builtins.str] = None,
        severity: typing.Optional[builtins.str] = None,
        variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationUnroutedSetRuleActionsVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param event_action: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#event_action EventOrchestrationUnrouted#event_action}.
        :param extraction: extraction block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#extraction EventOrchestrationUnrouted#extraction}
        :param route_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#route_to EventOrchestrationUnrouted#route_to}.
        :param severity: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#severity EventOrchestrationUnrouted#severity}.
        :param variable: variable block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_unrouted#variable EventOrchestrationUnrouted#variable}
        '''
        value = EventOrchestrationUnroutedSetRuleActions(
            event_action=event_action,
            extraction=extraction,
            route_to=route_to,
            severity=severity,
            variable=variable,
        )

        return typing.cast(None, jsii.invoke(self, "putActions", [value]))

    @jsii.member(jsii_name="putCondition")
    def put_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationUnroutedSetRuleCondition, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7be9c853ffec7e800ae3283f4f298af07f7da7d284d2883366047eedefaed04)
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
    def actions(self) -> EventOrchestrationUnroutedSetRuleActionsOutputReference:
        return typing.cast(EventOrchestrationUnroutedSetRuleActionsOutputReference, jsii.get(self, "actions"))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> EventOrchestrationUnroutedSetRuleConditionList:
        return typing.cast(EventOrchestrationUnroutedSetRuleConditionList, jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(
        self,
    ) -> typing.Optional[EventOrchestrationUnroutedSetRuleActions]:
        return typing.cast(typing.Optional[EventOrchestrationUnroutedSetRuleActions], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationUnroutedSetRuleCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationUnroutedSetRuleCondition]]], jsii.get(self, "conditionInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__74ad881e08f4069aa3fc69f339e371e8ef60bf572756c4d40bbf03751b960fa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "label"))

    @label.setter
    def label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f18b570b16fb4450e72c1fa105bfbd8cfb69b4fff278a78afe143e86d468a4d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "label", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationUnroutedSetRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationUnroutedSetRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationUnroutedSetRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d2f7058dc890948b3223bfd2554d0d2d47cd98451671c7037905d7fe231c8af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "EventOrchestrationUnrouted",
    "EventOrchestrationUnroutedCatchAll",
    "EventOrchestrationUnroutedCatchAllActions",
    "EventOrchestrationUnroutedCatchAllActionsExtraction",
    "EventOrchestrationUnroutedCatchAllActionsExtractionList",
    "EventOrchestrationUnroutedCatchAllActionsExtractionOutputReference",
    "EventOrchestrationUnroutedCatchAllActionsOutputReference",
    "EventOrchestrationUnroutedCatchAllActionsVariable",
    "EventOrchestrationUnroutedCatchAllActionsVariableList",
    "EventOrchestrationUnroutedCatchAllActionsVariableOutputReference",
    "EventOrchestrationUnroutedCatchAllOutputReference",
    "EventOrchestrationUnroutedConfig",
    "EventOrchestrationUnroutedSet",
    "EventOrchestrationUnroutedSetList",
    "EventOrchestrationUnroutedSetOutputReference",
    "EventOrchestrationUnroutedSetRule",
    "EventOrchestrationUnroutedSetRuleActions",
    "EventOrchestrationUnroutedSetRuleActionsExtraction",
    "EventOrchestrationUnroutedSetRuleActionsExtractionList",
    "EventOrchestrationUnroutedSetRuleActionsExtractionOutputReference",
    "EventOrchestrationUnroutedSetRuleActionsOutputReference",
    "EventOrchestrationUnroutedSetRuleActionsVariable",
    "EventOrchestrationUnroutedSetRuleActionsVariableList",
    "EventOrchestrationUnroutedSetRuleActionsVariableOutputReference",
    "EventOrchestrationUnroutedSetRuleCondition",
    "EventOrchestrationUnroutedSetRuleConditionList",
    "EventOrchestrationUnroutedSetRuleConditionOutputReference",
    "EventOrchestrationUnroutedSetRuleList",
    "EventOrchestrationUnroutedSetRuleOutputReference",
]

publication.publish()

def _typecheckingstub__8275f256338e5751768f444091a5b8068e8f5bb29eb2d709101305f01c17607c(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    catch_all: typing.Union[EventOrchestrationUnroutedCatchAll, typing.Dict[builtins.str, typing.Any]],
    event_orchestration: builtins.str,
    set: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationUnroutedSet, typing.Dict[builtins.str, typing.Any]]]],
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

def _typecheckingstub__bbdee9f778de5a90e9bb378e4cc1b309983ef7863d142c414e704d8bad4d4342(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__018d268dee74aace0a2368e3a3adbf56b4e2755ed3460d5e2145d21da93dffa0(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationUnroutedSet, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53e4b0ca3d3f8bc5751e5175370f6ef6493a38a288b88c3ffca9b27ac62dcdc7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b00c652ebc1bf8a813059274a274ccbc4a976e7128d9802ac9d151a7ce4f0f41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__06f503a56f272d5c2f99e818b6a494953007278b215cf9e8009bc7756d63894c(
    *,
    actions: typing.Union[EventOrchestrationUnroutedCatchAllActions, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6574dcb4a0e638aece27cc74f601e14a17d0b4395adc2458762bf0dd9ef29cd(
    *,
    event_action: typing.Optional[builtins.str] = None,
    extraction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationUnroutedCatchAllActionsExtraction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    severity: typing.Optional[builtins.str] = None,
    variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationUnroutedCatchAllActionsVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__873057e6f5f2b8466ff463cc0428da1d09eef943c149dc85c306d593a566df69(
    *,
    target: builtins.str,
    regex: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
    template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e0027e63576683e30c8816d4bacdb7fa19e7e06955c20981a00d5b69753b26b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2c8a4e2bd5d821506986e6c1b7ef02e09cfe36f9835a1b2098161c15040f14f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__954af6d347c97be0c28756a0911fbdfdaf96e2c519716ea74a10b5287d55ca14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb9e457abc33e3760870fc13261efc44341d44b54df603440bb35031ccf2c69d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10a4a6475dfa7e67907bf0e67a89e1366380cb148115d49fb68d484d5230f25e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__619013fd37aff2d18a117c3b3607169e2f96985d8dca86444d23e930482b4e6b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationUnroutedCatchAllActionsExtraction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f097efbed909b984662332fa19b2cff5b615e7429e03e3bf09432ba2383c8d2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ee17cb133954e63108ae95a70a7a0b096a2b4f1cdb443a762760170c8a4f2ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35b1ebaeecf768fbd2da1a915451cc1e8c055420aa74dfb95e8ba0cbe93e6b5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fafc1345d70cccbbf3bd424f6fc27f9975ef6e7ac067f55de9bc210c26f26730(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf268df5daefc13ef41f99344ebe5f03f32861b1cd17f656b3b436b19b7cf262(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be05d22a23d358c52138241589e59196792ce534f761d38e956c71ada1772dc5(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationUnroutedCatchAllActionsExtraction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df4afcc52b90728bc39ba8aead7f054c495cf538a5523c0ec110c2a346cc577f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dca0edaf380c2ae04f9a8029200db324145326711199176f420c9ddfd6cb505(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationUnroutedCatchAllActionsExtraction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d437d1e56027293873c7a151a3a266d036670f7548385125e8aedfc1d82afa7b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationUnroutedCatchAllActionsVariable, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19be63d73a870f653dab26f5c94daff0eed587619e15e3e30bb1f71bab0b49a4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfd00bb58d0830780fbeda8396f16d666b3069bad231c7f98b714bb287710bb2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0624943abcc45135d61d7e71399afbd62ce94d725dcf47414d95b6b88c7d236(
    value: typing.Optional[EventOrchestrationUnroutedCatchAllActions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d16718dd84c51311e04997b4675de9db9aec5dd9d5debae2b5d98162b78bced(
    *,
    name: builtins.str,
    path: builtins.str,
    type: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69a49b662949a36b0ffaf8895b79d623f8a36f496ad6177721f4250810615f52(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1380b93653f78fe6914bca9ec71c8bfdccadbaa30099e9500246c38c561e981b(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3a7f4af5291f0265269958f1c6d1ca638ba28bb43a31319634d8e36cdc20a96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6addc45164afaf9240265f0cfe96ec481f3f03027622ac244c6908af1391a6e(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1870fe5e1dbee87c2f3945f4550be60a344c74b44aeb47ebc6bf9adddb1ebaf4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cd2958db1c59646663d2cfb6a7ed94596f5a43dc1b1563332270b30c74ea5c9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationUnroutedCatchAllActionsVariable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__196e18aa7284a5aea561ffa32ea04f9e17096b827a372bee1e24c642dcce6ce2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__514cc3738b0757e7a17486c13d2f38cb98a40de470cea5affcdb2147511ebae7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ab8d960654895992ab0db79d7ee8f58161e4d5484cc1f7821a02c84a70ce02e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f47cef1ec88628b76c3724948de8f1af50a92b08adc0a2220982b81358555d15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba93494ae89f53068f3bf4b8bba7f0b7538cd4ee201548535a7a5e44580d8d87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeca7d344c747657fb4d8c34ad118a33707e209b6bb1f1f897cdd7b1fc4e300e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationUnroutedCatchAllActionsVariable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd8aa5ad6f8ff58a49d792a41b1505092c30f86f07f621704000df770e53ead3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7845e0940d40b2a61bc15180a1f421c130c26f83a4338490932e8c7b5734ae94(
    value: typing.Optional[EventOrchestrationUnroutedCatchAll],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3337998421b1ba5b03def6960dc3e2a48bb7c187bc08eb62a67d24c843f57849(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    catch_all: typing.Union[EventOrchestrationUnroutedCatchAll, typing.Dict[builtins.str, typing.Any]],
    event_orchestration: builtins.str,
    set: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationUnroutedSet, typing.Dict[builtins.str, typing.Any]]]],
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d008f014806e1f881fbd832e0f0859fbb79a6023defe775d45620826b97169c9(
    *,
    id: builtins.str,
    rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationUnroutedSetRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27dac7bee1374e8a6d71d3f8cce1a731b40501dcfd907d6b450b6a02ac1972af(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2060c8b4fca371bffa9b2df36d1e227d5dcf27b3446f716d4b8c8a45aee387ce(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__589426e4a6f278f25cef6b077fe3944ec855cde428e0ad25b062d5993a83795a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fdfe9b29d400ad94627041edb8dc8a65f238a5e3513a2a369f41a71c699e7fc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d957f5fc025a8f93d8c2ea7ae2be6e19fd3784db7d25bf5f71f7e43daf5676a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddec66fccb4a0cf0ae4c523cc4c7797124e47a62794d2fd225f2772b1492c286(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationUnroutedSet]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__034de521d11fde7f36cdcb6a8b289dd3d4abff7a4828961701e694c5b9c0f996(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14096c8150d9cf77ab0422f25e18773a63486679ea7582931560905ae6cd495c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationUnroutedSetRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66b860a7db2b579877641045d626773900a3c8eba1097bb0820a6234667cff10(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9549d3aadf2e2a27d807dd15f5295d14a41d0175cdf12e7999b9ae8907844c65(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationUnroutedSet]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90f64f64a017d7112db8e5120d1e7674247f6faf8869d10751346f3ec813dbba(
    *,
    actions: typing.Union[EventOrchestrationUnroutedSetRuleActions, typing.Dict[builtins.str, typing.Any]],
    condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationUnroutedSetRuleCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    label: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7de69daeae1a5cd1a1063bd644434991e938ef8d905f1e00d5b411fef8b3a529(
    *,
    event_action: typing.Optional[builtins.str] = None,
    extraction: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationUnroutedSetRuleActionsExtraction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    route_to: typing.Optional[builtins.str] = None,
    severity: typing.Optional[builtins.str] = None,
    variable: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationUnroutedSetRuleActionsVariable, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b3013dd35226ec76dc2f09e9719e1c12966fdd5323214ccba59c06037e0e915(
    *,
    target: builtins.str,
    regex: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
    template: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b5ba409596cf7458e3df246b3027fe9ec592a34c20638922a72259b76af8735(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d8d7a2bcbf08049c18b3816e0abbea800b1ba2c505c436d3ec3c7cdfe3ca2a5(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe5367753a7f9176ec09d326b2e3285af7417505ef30b9abb14fbd1c0545316a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5920f18d561fff2aa0285aaebc7fcf2173233ba8ae7a35ebaa159ef2db5d5abe(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a3846ecdd940034b38502a27a804a4cc9cba57740ac075957b6dfc85b64ae8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0ddec5465e9dd8c4635ef2f4fcc42b709c8a4a80c9891ac1147c39ec1b786b7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationUnroutedSetRuleActionsExtraction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a0f4866a14ef5d5072c18ed875a0de10ebac1f9b9937503f4c26f5383f3aca4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__218b77d250f7488272c6687fa4af89330b0d9ee114e66eee0395cc11c6662a91(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4d5aa72bf6b2ca3a515b908c319b06f5806e844dd126c208ab37e488be83d94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2f5193c00bbb1c792c7ce2c8c0fe9b1ce12b7e6608712130c60d6f6e8699730(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c54a36ec938b57bc01e6ddd9ccae6c1ea8e3b8824fc1ef1f2c860f938b793b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fc553cc1c300a70de0ab2da830e9ee63f911336d697a50b6207d1e3ce06fe77(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationUnroutedSetRuleActionsExtraction]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__060d73ba53830954fb97a051575dbd2589ebf9dc5edb52afec2cebb3e361f168(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcac8d5312b10e6ad6ba79da0d02e87bdcdf3d2127986c97eb07afcecc9fdffd(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationUnroutedSetRuleActionsExtraction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17c35ea486dbcb50b9de002b68d378f59a50806975cd173e828f77c0e89a4de1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationUnroutedSetRuleActionsVariable, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1723f97a85f09bf3944806bae183cfc27c526b848ed12c4c8e125d9a2251ead(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39fe95870492f0e1b093afe8831231caab3ccf368dd09414f2196ca3a737d296(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bb14685b0386392b6aa0c1d71acb035260657ef724bf5b4365d11eda37a17d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__427529fd67ee11028870e05d50549fabe448fdf16073724786ecbcfaccc64a82(
    value: typing.Optional[EventOrchestrationUnroutedSetRuleActions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd0c5f57df347bcae15394cd70a29867473ac8aa3688e6f0dc355fc21a2ef2d8(
    *,
    name: builtins.str,
    path: builtins.str,
    type: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4edd0e7e73a8fb39569de97506fd9f55fd448720c532e4207b9ecdb84e31da6e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2ddf8b2a45e89e86e9e46569f7dedb775adc3ac181d7904793c98f43ec75676(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__722825992fcb1853144b603822ca88e63b97607df16fd008037da2b8ecacdb41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ddb24cf319f30935b5696581bd93424cc627c068f7f8341df59a92bb15f13d4(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52aa34464eac9ca489253376eb0d9ed5b380d8082fb95972d66c996312fb26b7(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b2a40f82c6f75b06f1f5280a872b4df3220e18095fdee32938685b5af6c977b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationUnroutedSetRuleActionsVariable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0194ee5442517143811b4a4870649cbbbad62551fec68a1d9bbdcd49cac97d29(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e3f5a741892ad226203f465bf55ecbe9147ae32e4ad1e3e3caf652f63ed2d86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__693ec9ab33827be2c1ed28dd0ef461d2a187126bb4311b1e596c059e4822fecc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__696bac573c81714669a3c7b5a3ba20a6bc3dd38a66ed856cb0794bf66b1efe6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8edc9be515059c450c2c4c1ffa2fc90302988f2362990f7c5a4c95ebcbb316e3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65a142b41cb3d7e2279f4448e7771aa9d8e691ee7f14b1fa794c0d08f8a893c3(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationUnroutedSetRuleActionsVariable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e07b5dc138d66b32d7ebe6a7836500090439b0c193c8ab86ebe5120b056af3f(
    *,
    expression: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4803e1fd51a51e8626ad7d5f61fd462c2dbbcf7f85db4d5558bd57677cbb0bc0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d2660f40645bd0b0dc91bcfed005e1a378ef8130d9117565e126bd3a2e796c3(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8cab0c348e39d936624ccc0f614f2331e90d074238c95787027f044b5fa946f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b595a3fe589a322e0a70256437066e756c68e1a6c3012f92f9c145dc94c9fd11(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1398556532a535c621bf360035898fa93e16ae08052e8b256e945dfe9bfb226(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75a0955b97a4a8b8c7ce55ec6863f0651da1bf09c7bbc27ee7bbf55a0cf531d4(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationUnroutedSetRuleCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8c6b126f665ec40ce74d76aee4719855e7d93a1ecd724de349314253d004000(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bc8ed6780b3ff240166da8fdd6209682ef85daf829e724c27011158f5181401(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b99d5a1b09ad5c0b230f6e39109def4c7ec44b1a3cbba9e36af42525fef1d6e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationUnroutedSetRuleCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb3bf60f3d6a317e2b0dcc02da6c920558c65b8ed5e6fee67fe8f5d889853faa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d1b1c69108c8e0a254db050e1e6700b17f76e2d7d972056ce8fbfcfcff05ce4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98a443f869641f970b84e36283c92ec6e5ce176678792404ea9bf74a1dd30f8d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b11371214d8877555d458cc710371c5d7e4ef12141373b90066e34259c05544(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16fc637d8dba6acb5945a873415b60ab44b3fdcee39a78a1f64af4edb6236225(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63557a88b911c664e57c8c44775c20d9d3b983a15be732ab6e24a542896d5916(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationUnroutedSetRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2396bf7f2a77cc24dfba04a370a6dbdd982a781e3923505d1de47940271f09a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7be9c853ffec7e800ae3283f4f298af07f7da7d284d2883366047eedefaed04(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationUnroutedSetRuleCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74ad881e08f4069aa3fc69f339e371e8ef60bf572756c4d40bbf03751b960fa6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f18b570b16fb4450e72c1fa105bfbd8cfb69b4fff278a78afe143e86d468a4d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d2f7058dc890948b3223bfd2554d0d2d47cd98451671c7037905d7fe231c8af(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationUnroutedSetRule]],
) -> None:
    """Type checking stubs"""
    pass
