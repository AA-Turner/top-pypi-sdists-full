r'''
# `pagerduty_event_orchestration_router`

Refer to the Terraform Registry for docs: [`pagerduty_event_orchestration_router`](https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router).
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


class EventOrchestrationRouter(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationRouter.EventOrchestrationRouter",
):
    '''Represents a {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router pagerduty_event_orchestration_router}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        catch_all: typing.Union["EventOrchestrationRouterCatchAll", typing.Dict[builtins.str, typing.Any]],
        event_orchestration: builtins.str,
        set: typing.Union["EventOrchestrationRouterSet", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router pagerduty_event_orchestration_router} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param catch_all: catch_all block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#catch_all EventOrchestrationRouter#catch_all}
        :param event_orchestration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#event_orchestration EventOrchestrationRouter#event_orchestration}.
        :param set: set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#set EventOrchestrationRouter#set}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#id EventOrchestrationRouter#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e870231e90d6f1996b682a7831bdc942e8aadfcf6edf07df400a3ba23f370c5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = EventOrchestrationRouterConfig(
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
        '''Generates CDKTF code for importing a EventOrchestrationRouter resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the EventOrchestrationRouter to import.
        :param import_from_id: The id of the existing EventOrchestrationRouter that should be imported. Refer to the {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the EventOrchestrationRouter to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27573bd1f816c720e586ab7de468822851563b8751e70f77ccda84bcbc5b8b94)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putCatchAll")
    def put_catch_all(
        self,
        *,
        actions: typing.Union["EventOrchestrationRouterCatchAllActions", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#actions EventOrchestrationRouter#actions}
        '''
        value = EventOrchestrationRouterCatchAll(actions=actions)

        return typing.cast(None, jsii.invoke(self, "putCatchAll", [value]))

    @jsii.member(jsii_name="putSet")
    def put_set(
        self,
        *,
        id: builtins.str,
        rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationRouterSetRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#id EventOrchestrationRouter#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#rule EventOrchestrationRouter#rule}
        '''
        value = EventOrchestrationRouterSet(id=id, rule=rule)

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
    def catch_all(self) -> "EventOrchestrationRouterCatchAllOutputReference":
        return typing.cast("EventOrchestrationRouterCatchAllOutputReference", jsii.get(self, "catchAll"))

    @builtins.property
    @jsii.member(jsii_name="set")
    def set(self) -> "EventOrchestrationRouterSetOutputReference":
        return typing.cast("EventOrchestrationRouterSetOutputReference", jsii.get(self, "set"))

    @builtins.property
    @jsii.member(jsii_name="catchAllInput")
    def catch_all_input(self) -> typing.Optional["EventOrchestrationRouterCatchAll"]:
        return typing.cast(typing.Optional["EventOrchestrationRouterCatchAll"], jsii.get(self, "catchAllInput"))

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
    def set_input(self) -> typing.Optional["EventOrchestrationRouterSet"]:
        return typing.cast(typing.Optional["EventOrchestrationRouterSet"], jsii.get(self, "setInput"))

    @builtins.property
    @jsii.member(jsii_name="eventOrchestration")
    def event_orchestration(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventOrchestration"))

    @event_orchestration.setter
    def event_orchestration(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00bdbf3bb946d06de5e001708f2fea28fe3cf0b39bfde74bd0b31d746dde8cb7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventOrchestration", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21248c96006eba658c12d7eb640ba515d930d81a2826e60c400aa21cc5436ef5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationRouter.EventOrchestrationRouterCatchAll",
    jsii_struct_bases=[],
    name_mapping={"actions": "actions"},
)
class EventOrchestrationRouterCatchAll:
    def __init__(
        self,
        *,
        actions: typing.Union["EventOrchestrationRouterCatchAllActions", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#actions EventOrchestrationRouter#actions}
        '''
        if isinstance(actions, dict):
            actions = EventOrchestrationRouterCatchAllActions(**actions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__281ac2524b0356b042ff70bb6e69f9b8319df810054c4d7ba3a3c3d69c0b53b4)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
        }

    @builtins.property
    def actions(self) -> "EventOrchestrationRouterCatchAllActions":
        '''actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#actions EventOrchestrationRouter#actions}
        '''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast("EventOrchestrationRouterCatchAllActions", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationRouterCatchAll(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationRouter.EventOrchestrationRouterCatchAllActions",
    jsii_struct_bases=[],
    name_mapping={"route_to": "routeTo"},
)
class EventOrchestrationRouterCatchAllActions:
    def __init__(self, *, route_to: builtins.str) -> None:
        '''
        :param route_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#route_to EventOrchestrationRouter#route_to}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e0be3fdeb3d7770c2d6fff3b47dc67fa679afcf0176a750bfc71cc5a4cde472)
            check_type(argname="argument route_to", value=route_to, expected_type=type_hints["route_to"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "route_to": route_to,
        }

    @builtins.property
    def route_to(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#route_to EventOrchestrationRouter#route_to}.'''
        result = self._values.get("route_to")
        assert result is not None, "Required property 'route_to' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationRouterCatchAllActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationRouterCatchAllActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationRouter.EventOrchestrationRouterCatchAllActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4feaa5e038992a8da834d4de53685cc4de9cd6110152b152c095102bda6bb5e1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="routeToInput")
    def route_to_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routeToInput"))

    @builtins.property
    @jsii.member(jsii_name="routeTo")
    def route_to(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routeTo"))

    @route_to.setter
    def route_to(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b41ef72b2e95ea67bd7d10fa9db4fe608a5cbf77110da2003f29d39756742757)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeTo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[EventOrchestrationRouterCatchAllActions]:
        return typing.cast(typing.Optional[EventOrchestrationRouterCatchAllActions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventOrchestrationRouterCatchAllActions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79e0575b80fc5c95368efbd3e65ad2e21f6075b6423c62671f4edcbd9a4b5a73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationRouterCatchAllOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationRouter.EventOrchestrationRouterCatchAllOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1cc2abc2423d049114c26aab5145fa37a2f570d39d53e36d8dcd712123ae8be5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putActions")
    def put_actions(self, *, route_to: builtins.str) -> None:
        '''
        :param route_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#route_to EventOrchestrationRouter#route_to}.
        '''
        value = EventOrchestrationRouterCatchAllActions(route_to=route_to)

        return typing.cast(None, jsii.invoke(self, "putActions", [value]))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> EventOrchestrationRouterCatchAllActionsOutputReference:
        return typing.cast(EventOrchestrationRouterCatchAllActionsOutputReference, jsii.get(self, "actions"))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(self) -> typing.Optional[EventOrchestrationRouterCatchAllActions]:
        return typing.cast(typing.Optional[EventOrchestrationRouterCatchAllActions], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EventOrchestrationRouterCatchAll]:
        return typing.cast(typing.Optional[EventOrchestrationRouterCatchAll], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventOrchestrationRouterCatchAll],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac0a95297311c68192b5af8f729ed556f9b590107d388eaf0d5e6d2fbcecfcea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationRouter.EventOrchestrationRouterConfig",
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
class EventOrchestrationRouterConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        catch_all: typing.Union[EventOrchestrationRouterCatchAll, typing.Dict[builtins.str, typing.Any]],
        event_orchestration: builtins.str,
        set: typing.Union["EventOrchestrationRouterSet", typing.Dict[builtins.str, typing.Any]],
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
        :param catch_all: catch_all block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#catch_all EventOrchestrationRouter#catch_all}
        :param event_orchestration: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#event_orchestration EventOrchestrationRouter#event_orchestration}.
        :param set: set block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#set EventOrchestrationRouter#set}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#id EventOrchestrationRouter#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(catch_all, dict):
            catch_all = EventOrchestrationRouterCatchAll(**catch_all)
        if isinstance(set, dict):
            set = EventOrchestrationRouterSet(**set)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4afd553490e1af582cb0e8d112691ece529d18ad439ff5068d4616861c8fa8de)
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
    def catch_all(self) -> EventOrchestrationRouterCatchAll:
        '''catch_all block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#catch_all EventOrchestrationRouter#catch_all}
        '''
        result = self._values.get("catch_all")
        assert result is not None, "Required property 'catch_all' is missing"
        return typing.cast(EventOrchestrationRouterCatchAll, result)

    @builtins.property
    def event_orchestration(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#event_orchestration EventOrchestrationRouter#event_orchestration}.'''
        result = self._values.get("event_orchestration")
        assert result is not None, "Required property 'event_orchestration' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def set(self) -> "EventOrchestrationRouterSet":
        '''set block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#set EventOrchestrationRouter#set}
        '''
        result = self._values.get("set")
        assert result is not None, "Required property 'set' is missing"
        return typing.cast("EventOrchestrationRouterSet", result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#id EventOrchestrationRouter#id}.

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
        return "EventOrchestrationRouterConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationRouter.EventOrchestrationRouterSet",
    jsii_struct_bases=[],
    name_mapping={"id": "id", "rule": "rule"},
)
class EventOrchestrationRouterSet:
    def __init__(
        self,
        *,
        id: builtins.str,
        rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationRouterSetRule", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#id EventOrchestrationRouter#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param rule: rule block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#rule EventOrchestrationRouter#rule}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3ea66f32002399982e2faa96ff423ab54f7bf6b238a5b0f9cd84439b0138bef)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }
        if rule is not None:
            self._values["rule"] = rule

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#id EventOrchestrationRouter#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationRouterSetRule"]]]:
        '''rule block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#rule EventOrchestrationRouter#rule}
        '''
        result = self._values.get("rule")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationRouterSetRule"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationRouterSet(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationRouterSetOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationRouter.EventOrchestrationRouterSetOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2ed60924efa58480239f8fb2f6f521804bb26d6c694b4058b8c0c2a3f93fad6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putRule")
    def put_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationRouterSetRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbfe90667f68be089673ca8d7cc285a034b660f1b728db94ce28695baa0f737a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putRule", [value]))

    @jsii.member(jsii_name="resetRule")
    def reset_rule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRule", []))

    @builtins.property
    @jsii.member(jsii_name="rule")
    def rule(self) -> "EventOrchestrationRouterSetRuleList":
        return typing.cast("EventOrchestrationRouterSetRuleList", jsii.get(self, "rule"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ruleInput")
    def rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationRouterSetRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationRouterSetRule"]]], jsii.get(self, "ruleInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73fd66ba3628d2026aaf51b7018ed7f607788367aa8fee870a26aa63b76e0087)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EventOrchestrationRouterSet]:
        return typing.cast(typing.Optional[EventOrchestrationRouterSet], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventOrchestrationRouterSet],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__defb6a8b233cea46bff40860d33ed3a3def7fffe5692a2e7aea3d7266f150f65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationRouter.EventOrchestrationRouterSetRule",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "condition": "condition",
        "disabled": "disabled",
        "label": "label",
    },
)
class EventOrchestrationRouterSetRule:
    def __init__(
        self,
        *,
        actions: typing.Union["EventOrchestrationRouterSetRuleActions", typing.Dict[builtins.str, typing.Any]],
        condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationRouterSetRuleCondition", typing.Dict[builtins.str, typing.Any]]]]] = None,
        disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        label: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param actions: actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#actions EventOrchestrationRouter#actions}
        :param condition: condition block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#condition EventOrchestrationRouter#condition}
        :param disabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#disabled EventOrchestrationRouter#disabled}.
        :param label: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#label EventOrchestrationRouter#label}.
        '''
        if isinstance(actions, dict):
            actions = EventOrchestrationRouterSetRuleActions(**actions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e916fcdfd35a62fcb7851b0e4128424688a6c77e503279fd05b103ae8babb29c)
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
    def actions(self) -> "EventOrchestrationRouterSetRuleActions":
        '''actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#actions EventOrchestrationRouter#actions}
        '''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast("EventOrchestrationRouterSetRuleActions", result)

    @builtins.property
    def condition(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationRouterSetRuleCondition"]]]:
        '''condition block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#condition EventOrchestrationRouter#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationRouterSetRuleCondition"]]], result)

    @builtins.property
    def disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#disabled EventOrchestrationRouter#disabled}.'''
        result = self._values.get("disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#label EventOrchestrationRouter#label}.'''
        result = self._values.get("label")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationRouterSetRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationRouter.EventOrchestrationRouterSetRuleActions",
    jsii_struct_bases=[],
    name_mapping={"dynamic_route_to": "dynamicRouteTo", "route_to": "routeTo"},
)
class EventOrchestrationRouterSetRuleActions:
    def __init__(
        self,
        *,
        dynamic_route_to: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["EventOrchestrationRouterSetRuleActionsDynamicRouteTo", typing.Dict[builtins.str, typing.Any]]]]] = None,
        route_to: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dynamic_route_to: dynamic_route_to block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#dynamic_route_to EventOrchestrationRouter#dynamic_route_to}
        :param route_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#route_to EventOrchestrationRouter#route_to}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caa9b602d284ce04ab10abbbc5bf9aa3c82cc0caecdea4267e1f11ba0be52073)
            check_type(argname="argument dynamic_route_to", value=dynamic_route_to, expected_type=type_hints["dynamic_route_to"])
            check_type(argname="argument route_to", value=route_to, expected_type=type_hints["route_to"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dynamic_route_to is not None:
            self._values["dynamic_route_to"] = dynamic_route_to
        if route_to is not None:
            self._values["route_to"] = route_to

    @builtins.property
    def dynamic_route_to(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationRouterSetRuleActionsDynamicRouteTo"]]]:
        '''dynamic_route_to block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#dynamic_route_to EventOrchestrationRouter#dynamic_route_to}
        '''
        result = self._values.get("dynamic_route_to")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["EventOrchestrationRouterSetRuleActionsDynamicRouteTo"]]], result)

    @builtins.property
    def route_to(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#route_to EventOrchestrationRouter#route_to}.'''
        result = self._values.get("route_to")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationRouterSetRuleActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationRouter.EventOrchestrationRouterSetRuleActionsDynamicRouteTo",
    jsii_struct_bases=[],
    name_mapping={"lookup_by": "lookupBy", "regex": "regex", "source": "source"},
)
class EventOrchestrationRouterSetRuleActionsDynamicRouteTo:
    def __init__(
        self,
        *,
        lookup_by: builtins.str,
        regex: builtins.str,
        source: builtins.str,
    ) -> None:
        '''
        :param lookup_by: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#lookup_by EventOrchestrationRouter#lookup_by}.
        :param regex: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#regex EventOrchestrationRouter#regex}.
        :param source: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#source EventOrchestrationRouter#source}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__419aa37ec429882cdca80aa3b4fd9e45d4bcf9d9397c7d260ff0d194edb09cb1)
            check_type(argname="argument lookup_by", value=lookup_by, expected_type=type_hints["lookup_by"])
            check_type(argname="argument regex", value=regex, expected_type=type_hints["regex"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "lookup_by": lookup_by,
            "regex": regex,
            "source": source,
        }

    @builtins.property
    def lookup_by(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#lookup_by EventOrchestrationRouter#lookup_by}.'''
        result = self._values.get("lookup_by")
        assert result is not None, "Required property 'lookup_by' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def regex(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#regex EventOrchestrationRouter#regex}.'''
        result = self._values.get("regex")
        assert result is not None, "Required property 'regex' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#source EventOrchestrationRouter#source}.'''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationRouterSetRuleActionsDynamicRouteTo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationRouterSetRuleActionsDynamicRouteToList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationRouter.EventOrchestrationRouterSetRuleActionsDynamicRouteToList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e99c2a663a3f474b3f74ed179c2f3ed13e71ffc75eca20eebe4b637f81f4b1a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventOrchestrationRouterSetRuleActionsDynamicRouteToOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e7ff95d76d33d2b492f0c7ad7b9d98eab453553143f936d9505e38b7b1ce5a4)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationRouterSetRuleActionsDynamicRouteToOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41556be527cdf36352cc2f54b2dc413f60bb3e58da032aedf8113b6c237a427e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d62f6625ba278df003195ee3f1c0e4ddf46f7222d8ddd5348d70f2365d888af)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec4fb2fb7fe2fe66ff20f1baa5829513125558876ca68f7d258c32bdd0f9feb0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationRouterSetRuleActionsDynamicRouteTo]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationRouterSetRuleActionsDynamicRouteTo]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationRouterSetRuleActionsDynamicRouteTo]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca03733e487f6d2144697dc4c0253e5bfb1b3895d4f8b830511d4b8975929096)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationRouterSetRuleActionsDynamicRouteToOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationRouter.EventOrchestrationRouterSetRuleActionsDynamicRouteToOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a19146e5d770e7115dc570e0d2515755c22a1fe5c496bf21000047438b54898f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="lookupByInput")
    def lookup_by_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "lookupByInput"))

    @builtins.property
    @jsii.member(jsii_name="regexInput")
    def regex_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regexInput"))

    @builtins.property
    @jsii.member(jsii_name="sourceInput")
    def source_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sourceInput"))

    @builtins.property
    @jsii.member(jsii_name="lookupBy")
    def lookup_by(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "lookupBy"))

    @lookup_by.setter
    def lookup_by(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18a796063eedbf43e361bb3d0f3162cac1e91a7efb15e29d5c6806c9fdd6476e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lookupBy", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="regex")
    def regex(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "regex"))

    @regex.setter
    def regex(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a864f4849a4c5f7ddeb229e1b1272d3e4ad3f1d779f6c7968be390999d775c9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "regex", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @source.setter
    def source(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baf6065311b95fe8aa54c6ece9679c7c23c75c0f358676c4f8988a4934cf314d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationRouterSetRuleActionsDynamicRouteTo]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationRouterSetRuleActionsDynamicRouteTo]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationRouterSetRuleActionsDynamicRouteTo]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a38ebdaff2c1eac67a04d05b86408751812ba6dcd9236cc5a0d79fc079859574)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationRouterSetRuleActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationRouter.EventOrchestrationRouterSetRuleActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4cee4de14e62ba78fbb18c0a7474c89df6f48e11b3ea50589d23f3fe1f59fad7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putDynamicRouteTo")
    def put_dynamic_route_to(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationRouterSetRuleActionsDynamicRouteTo, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__242f4683ad8f43bc2c7a707af6615a3d42424dc310bd8d7b860154fff3483c59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putDynamicRouteTo", [value]))

    @jsii.member(jsii_name="resetDynamicRouteTo")
    def reset_dynamic_route_to(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDynamicRouteTo", []))

    @jsii.member(jsii_name="resetRouteTo")
    def reset_route_to(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRouteTo", []))

    @builtins.property
    @jsii.member(jsii_name="dynamicRouteTo")
    def dynamic_route_to(
        self,
    ) -> EventOrchestrationRouterSetRuleActionsDynamicRouteToList:
        return typing.cast(EventOrchestrationRouterSetRuleActionsDynamicRouteToList, jsii.get(self, "dynamicRouteTo"))

    @builtins.property
    @jsii.member(jsii_name="dynamicRouteToInput")
    def dynamic_route_to_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationRouterSetRuleActionsDynamicRouteTo]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationRouterSetRuleActionsDynamicRouteTo]]], jsii.get(self, "dynamicRouteToInput"))

    @builtins.property
    @jsii.member(jsii_name="routeToInput")
    def route_to_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "routeToInput"))

    @builtins.property
    @jsii.member(jsii_name="routeTo")
    def route_to(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "routeTo"))

    @route_to.setter
    def route_to(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34ac2c6007e0460ee936925acd96d1e76af76435d837d78c537f21612b82f0ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "routeTo", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[EventOrchestrationRouterSetRuleActions]:
        return typing.cast(typing.Optional[EventOrchestrationRouterSetRuleActions], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[EventOrchestrationRouterSetRuleActions],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c2f28fa9eb22cb2a3f18237d138b71dd8eef89aa636a73b5f53ce70943608e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationRouter.EventOrchestrationRouterSetRuleCondition",
    jsii_struct_bases=[],
    name_mapping={"expression": "expression"},
)
class EventOrchestrationRouterSetRuleCondition:
    def __init__(self, *, expression: builtins.str) -> None:
        '''
        :param expression: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#expression EventOrchestrationRouter#expression}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9b1e400c9376b0dd9f5ce4b4b1010923f4f47c2f6b96d18ec4b0a724173f37e)
            check_type(argname="argument expression", value=expression, expected_type=type_hints["expression"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "expression": expression,
        }

    @builtins.property
    def expression(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#expression EventOrchestrationRouter#expression}.'''
        result = self._values.get("expression")
        assert result is not None, "Required property 'expression' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EventOrchestrationRouterSetRuleCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EventOrchestrationRouterSetRuleConditionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationRouter.EventOrchestrationRouterSetRuleConditionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__150c080ea850552bf239ffa29ee81001445dd29608d0d19ac91326f89f2c9599)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventOrchestrationRouterSetRuleConditionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3eccda3a1e511ff82b681704271e4fa29f67c63f36dc9de34c0775625fb59b8e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationRouterSetRuleConditionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58c82e9758b8a1fd5a7f61f8f943481f23e8f4486a2e9ae5169d83ecd9d171bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fb933080b405fea8c27ca91acc3827324b020e7780ed528a2892ff4ef9da6198)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c88ab6aed745ec89adf437b8b90384af05f5d5d5620590c7033557c5f0a9927d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationRouterSetRuleCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationRouterSetRuleCondition]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationRouterSetRuleCondition]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ccd06f1d712a6a086b0c8d89e934fe35c5cf8a1787bac4fb9c8195d6b87a242)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationRouterSetRuleConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationRouter.EventOrchestrationRouterSetRuleConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__375b96dfd232d9ac36002248db7dc5a837640a089820ae46755bf5bcdc0abc79)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62e544836172ed60911d9f72351f0154cfd8a094e50d9cb7a9b6ec69c184854f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "expression", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationRouterSetRuleCondition]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationRouterSetRuleCondition]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationRouterSetRuleCondition]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdee4e2f0241b13155b895fa910d38e7c226a759c607e873a024d368690a176d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationRouterSetRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationRouter.EventOrchestrationRouterSetRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de695f12a7a3bb9baacbb1519599badc95b77ff0d1ecc1ea2b7b93a00df9e274)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "EventOrchestrationRouterSetRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f512fcfbf9c10d5f82fecebfd06305b1760cfdce91aa4606bc1ac4d0e9490ed)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("EventOrchestrationRouterSetRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfa2ee1ea3f80cb0fe91b6359975daf5c7afbaaf72457e3c577aa5a10474212c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__70f1e22689bd28d2acfca82ed70fa73cc1fb8fc2fab40a8f6ebb3403c0f034bc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7e326b86f640da59df6dab0ab612c2972817097f06d298ba3971db7add6fa16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationRouterSetRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationRouterSetRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationRouterSetRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba01dc4f427ad3f62e8c9c94abb9cab78743606f6325e59ed51eb74a32d23060)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class EventOrchestrationRouterSetRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-pagerduty.eventOrchestrationRouter.EventOrchestrationRouterSetRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a6572e9125d2e1896b24b011184bdc9ca2f66ae0eb234da360f92f271a6c3a3)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putActions")
    def put_actions(
        self,
        *,
        dynamic_route_to: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationRouterSetRuleActionsDynamicRouteTo, typing.Dict[builtins.str, typing.Any]]]]] = None,
        route_to: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param dynamic_route_to: dynamic_route_to block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#dynamic_route_to EventOrchestrationRouter#dynamic_route_to}
        :param route_to: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/pagerduty/pagerduty/3.26.2/docs/resources/event_orchestration_router#route_to EventOrchestrationRouter#route_to}.
        '''
        value = EventOrchestrationRouterSetRuleActions(
            dynamic_route_to=dynamic_route_to, route_to=route_to
        )

        return typing.cast(None, jsii.invoke(self, "putActions", [value]))

    @jsii.member(jsii_name="putCondition")
    def put_condition(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationRouterSetRuleCondition, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40e990aba4dc2f5df45fdad16139a3d5222fdf185bdc52cbdb82e959b7f0326f)
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
    def actions(self) -> EventOrchestrationRouterSetRuleActionsOutputReference:
        return typing.cast(EventOrchestrationRouterSetRuleActionsOutputReference, jsii.get(self, "actions"))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> EventOrchestrationRouterSetRuleConditionList:
        return typing.cast(EventOrchestrationRouterSetRuleConditionList, jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="actionsInput")
    def actions_input(self) -> typing.Optional[EventOrchestrationRouterSetRuleActions]:
        return typing.cast(typing.Optional[EventOrchestrationRouterSetRuleActions], jsii.get(self, "actionsInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationRouterSetRuleCondition]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationRouterSetRuleCondition]]], jsii.get(self, "conditionInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__28cb6a0716b5687a18d741a5006ff69c79f204eed72d02fb22fca4b2c66cd889)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="label")
    def label(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "label"))

    @label.setter
    def label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1126062837ed5c152f0fc08fbca810a00770bf0a9d41fbd5750239c96729b3d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "label", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationRouterSetRule]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationRouterSetRule]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationRouterSetRule]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__607d5402e83e173082bb33616ee6918d92273947bdd857193a0f843f3c495f91)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "EventOrchestrationRouter",
    "EventOrchestrationRouterCatchAll",
    "EventOrchestrationRouterCatchAllActions",
    "EventOrchestrationRouterCatchAllActionsOutputReference",
    "EventOrchestrationRouterCatchAllOutputReference",
    "EventOrchestrationRouterConfig",
    "EventOrchestrationRouterSet",
    "EventOrchestrationRouterSetOutputReference",
    "EventOrchestrationRouterSetRule",
    "EventOrchestrationRouterSetRuleActions",
    "EventOrchestrationRouterSetRuleActionsDynamicRouteTo",
    "EventOrchestrationRouterSetRuleActionsDynamicRouteToList",
    "EventOrchestrationRouterSetRuleActionsDynamicRouteToOutputReference",
    "EventOrchestrationRouterSetRuleActionsOutputReference",
    "EventOrchestrationRouterSetRuleCondition",
    "EventOrchestrationRouterSetRuleConditionList",
    "EventOrchestrationRouterSetRuleConditionOutputReference",
    "EventOrchestrationRouterSetRuleList",
    "EventOrchestrationRouterSetRuleOutputReference",
]

publication.publish()

def _typecheckingstub__8e870231e90d6f1996b682a7831bdc942e8aadfcf6edf07df400a3ba23f370c5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    catch_all: typing.Union[EventOrchestrationRouterCatchAll, typing.Dict[builtins.str, typing.Any]],
    event_orchestration: builtins.str,
    set: typing.Union[EventOrchestrationRouterSet, typing.Dict[builtins.str, typing.Any]],
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

def _typecheckingstub__27573bd1f816c720e586ab7de468822851563b8751e70f77ccda84bcbc5b8b94(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00bdbf3bb946d06de5e001708f2fea28fe3cf0b39bfde74bd0b31d746dde8cb7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21248c96006eba658c12d7eb640ba515d930d81a2826e60c400aa21cc5436ef5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__281ac2524b0356b042ff70bb6e69f9b8319df810054c4d7ba3a3c3d69c0b53b4(
    *,
    actions: typing.Union[EventOrchestrationRouterCatchAllActions, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e0be3fdeb3d7770c2d6fff3b47dc67fa679afcf0176a750bfc71cc5a4cde472(
    *,
    route_to: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4feaa5e038992a8da834d4de53685cc4de9cd6110152b152c095102bda6bb5e1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b41ef72b2e95ea67bd7d10fa9db4fe608a5cbf77110da2003f29d39756742757(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79e0575b80fc5c95368efbd3e65ad2e21f6075b6423c62671f4edcbd9a4b5a73(
    value: typing.Optional[EventOrchestrationRouterCatchAllActions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cc2abc2423d049114c26aab5145fa37a2f570d39d53e36d8dcd712123ae8be5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac0a95297311c68192b5af8f729ed556f9b590107d388eaf0d5e6d2fbcecfcea(
    value: typing.Optional[EventOrchestrationRouterCatchAll],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4afd553490e1af582cb0e8d112691ece529d18ad439ff5068d4616861c8fa8de(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    catch_all: typing.Union[EventOrchestrationRouterCatchAll, typing.Dict[builtins.str, typing.Any]],
    event_orchestration: builtins.str,
    set: typing.Union[EventOrchestrationRouterSet, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3ea66f32002399982e2faa96ff423ab54f7bf6b238a5b0f9cd84439b0138bef(
    *,
    id: builtins.str,
    rule: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationRouterSetRule, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2ed60924efa58480239f8fb2f6f521804bb26d6c694b4058b8c0c2a3f93fad6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbfe90667f68be089673ca8d7cc285a034b660f1b728db94ce28695baa0f737a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationRouterSetRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73fd66ba3628d2026aaf51b7018ed7f607788367aa8fee870a26aa63b76e0087(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__defb6a8b233cea46bff40860d33ed3a3def7fffe5692a2e7aea3d7266f150f65(
    value: typing.Optional[EventOrchestrationRouterSet],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e916fcdfd35a62fcb7851b0e4128424688a6c77e503279fd05b103ae8babb29c(
    *,
    actions: typing.Union[EventOrchestrationRouterSetRuleActions, typing.Dict[builtins.str, typing.Any]],
    condition: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationRouterSetRuleCondition, typing.Dict[builtins.str, typing.Any]]]]] = None,
    disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    label: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caa9b602d284ce04ab10abbbc5bf9aa3c82cc0caecdea4267e1f11ba0be52073(
    *,
    dynamic_route_to: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationRouterSetRuleActionsDynamicRouteTo, typing.Dict[builtins.str, typing.Any]]]]] = None,
    route_to: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__419aa37ec429882cdca80aa3b4fd9e45d4bcf9d9397c7d260ff0d194edb09cb1(
    *,
    lookup_by: builtins.str,
    regex: builtins.str,
    source: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e99c2a663a3f474b3f74ed179c2f3ed13e71ffc75eca20eebe4b637f81f4b1a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e7ff95d76d33d2b492f0c7ad7b9d98eab453553143f936d9505e38b7b1ce5a4(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41556be527cdf36352cc2f54b2dc413f60bb3e58da032aedf8113b6c237a427e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d62f6625ba278df003195ee3f1c0e4ddf46f7222d8ddd5348d70f2365d888af(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec4fb2fb7fe2fe66ff20f1baa5829513125558876ca68f7d258c32bdd0f9feb0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca03733e487f6d2144697dc4c0253e5bfb1b3895d4f8b830511d4b8975929096(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationRouterSetRuleActionsDynamicRouteTo]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a19146e5d770e7115dc570e0d2515755c22a1fe5c496bf21000047438b54898f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18a796063eedbf43e361bb3d0f3162cac1e91a7efb15e29d5c6806c9fdd6476e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a864f4849a4c5f7ddeb229e1b1272d3e4ad3f1d779f6c7968be390999d775c9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baf6065311b95fe8aa54c6ece9679c7c23c75c0f358676c4f8988a4934cf314d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a38ebdaff2c1eac67a04d05b86408751812ba6dcd9236cc5a0d79fc079859574(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationRouterSetRuleActionsDynamicRouteTo]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cee4de14e62ba78fbb18c0a7474c89df6f48e11b3ea50589d23f3fe1f59fad7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__242f4683ad8f43bc2c7a707af6615a3d42424dc310bd8d7b860154fff3483c59(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationRouterSetRuleActionsDynamicRouteTo, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34ac2c6007e0460ee936925acd96d1e76af76435d837d78c537f21612b82f0ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c2f28fa9eb22cb2a3f18237d138b71dd8eef89aa636a73b5f53ce70943608e1(
    value: typing.Optional[EventOrchestrationRouterSetRuleActions],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9b1e400c9376b0dd9f5ce4b4b1010923f4f47c2f6b96d18ec4b0a724173f37e(
    *,
    expression: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__150c080ea850552bf239ffa29ee81001445dd29608d0d19ac91326f89f2c9599(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3eccda3a1e511ff82b681704271e4fa29f67c63f36dc9de34c0775625fb59b8e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58c82e9758b8a1fd5a7f61f8f943481f23e8f4486a2e9ae5169d83ecd9d171bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb933080b405fea8c27ca91acc3827324b020e7780ed528a2892ff4ef9da6198(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c88ab6aed745ec89adf437b8b90384af05f5d5d5620590c7033557c5f0a9927d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ccd06f1d712a6a086b0c8d89e934fe35c5cf8a1787bac4fb9c8195d6b87a242(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationRouterSetRuleCondition]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__375b96dfd232d9ac36002248db7dc5a837640a089820ae46755bf5bcdc0abc79(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62e544836172ed60911d9f72351f0154cfd8a094e50d9cb7a9b6ec69c184854f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdee4e2f0241b13155b895fa910d38e7c226a759c607e873a024d368690a176d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationRouterSetRuleCondition]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de695f12a7a3bb9baacbb1519599badc95b77ff0d1ecc1ea2b7b93a00df9e274(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f512fcfbf9c10d5f82fecebfd06305b1760cfdce91aa4606bc1ac4d0e9490ed(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfa2ee1ea3f80cb0fe91b6359975daf5c7afbaaf72457e3c577aa5a10474212c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70f1e22689bd28d2acfca82ed70fa73cc1fb8fc2fab40a8f6ebb3403c0f034bc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7e326b86f640da59df6dab0ab612c2972817097f06d298ba3971db7add6fa16(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba01dc4f427ad3f62e8c9c94abb9cab78743606f6325e59ed51eb74a32d23060(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[EventOrchestrationRouterSetRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a6572e9125d2e1896b24b011184bdc9ca2f66ae0eb234da360f92f271a6c3a3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40e990aba4dc2f5df45fdad16139a3d5222fdf185bdc52cbdb82e959b7f0326f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[EventOrchestrationRouterSetRuleCondition, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28cb6a0716b5687a18d741a5006ff69c79f204eed72d02fb22fca4b2c66cd889(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1126062837ed5c152f0fc08fbca810a00770bf0a9d41fbd5750239c96729b3d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__607d5402e83e173082bb33616ee6918d92273947bdd857193a0f843f3c495f91(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, EventOrchestrationRouterSetRule]],
) -> None:
    """Type checking stubs"""
    pass
