r'''
# `azurerm_web_pubsub_hub`

Refer to the Terraform Registry for docs: [`azurerm_web_pubsub_hub`](https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub).
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


class WebPubsubHub(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.webPubsubHub.WebPubsubHub",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub azurerm_web_pubsub_hub}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        web_pubsub_id: builtins.str,
        anonymous_connections_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        event_handler: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WebPubsubHubEventHandler", typing.Dict[builtins.str, typing.Any]]]]] = None,
        event_listener: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WebPubsubHubEventListener", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["WebPubsubHubTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub azurerm_web_pubsub_hub} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#name WebPubsubHub#name}.
        :param web_pubsub_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#web_pubsub_id WebPubsubHub#web_pubsub_id}.
        :param anonymous_connections_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#anonymous_connections_enabled WebPubsubHub#anonymous_connections_enabled}.
        :param event_handler: event_handler block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#event_handler WebPubsubHub#event_handler}
        :param event_listener: event_listener block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#event_listener WebPubsubHub#event_listener}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#id WebPubsubHub#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#timeouts WebPubsubHub#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__494d001c058f88d4cfa6c4d4872ef2775486e2fcc2e47f615196300f3fe02139)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = WebPubsubHubConfig(
            name=name,
            web_pubsub_id=web_pubsub_id,
            anonymous_connections_enabled=anonymous_connections_enabled,
            event_handler=event_handler,
            event_listener=event_listener,
            id=id,
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
        '''Generates CDKTF code for importing a WebPubsubHub resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the WebPubsubHub to import.
        :param import_from_id: The id of the existing WebPubsubHub that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the WebPubsubHub to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7d53ed775d5e9bf43940a26a9f9c9cfe316a0674023a5e95bcf1a77e0a21a43)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putEventHandler")
    def put_event_handler(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WebPubsubHubEventHandler", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ac49fede4b8c8fe2a1ce70926fe7286bdb4199c0548b82e927689eec0e2d586)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEventHandler", [value]))

    @jsii.member(jsii_name="putEventListener")
    def put_event_listener(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WebPubsubHubEventListener", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13ac5cd2c99174fcd69c0cc6359922379abbbe7a6107104709a0fbcc3b0b7005)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEventListener", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#create WebPubsubHub#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#delete WebPubsubHub#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#read WebPubsubHub#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#update WebPubsubHub#update}.
        '''
        value = WebPubsubHubTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAnonymousConnectionsEnabled")
    def reset_anonymous_connections_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAnonymousConnectionsEnabled", []))

    @jsii.member(jsii_name="resetEventHandler")
    def reset_event_handler(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventHandler", []))

    @jsii.member(jsii_name="resetEventListener")
    def reset_event_listener(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventListener", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="eventHandler")
    def event_handler(self) -> "WebPubsubHubEventHandlerList":
        return typing.cast("WebPubsubHubEventHandlerList", jsii.get(self, "eventHandler"))

    @builtins.property
    @jsii.member(jsii_name="eventListener")
    def event_listener(self) -> "WebPubsubHubEventListenerList":
        return typing.cast("WebPubsubHubEventListenerList", jsii.get(self, "eventListener"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "WebPubsubHubTimeoutsOutputReference":
        return typing.cast("WebPubsubHubTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="anonymousConnectionsEnabledInput")
    def anonymous_connections_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "anonymousConnectionsEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="eventHandlerInput")
    def event_handler_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebPubsubHubEventHandler"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebPubsubHubEventHandler"]]], jsii.get(self, "eventHandlerInput"))

    @builtins.property
    @jsii.member(jsii_name="eventListenerInput")
    def event_listener_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebPubsubHubEventListener"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebPubsubHubEventListener"]]], jsii.get(self, "eventListenerInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "WebPubsubHubTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "WebPubsubHubTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="webPubsubIdInput")
    def web_pubsub_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "webPubsubIdInput"))

    @builtins.property
    @jsii.member(jsii_name="anonymousConnectionsEnabled")
    def anonymous_connections_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "anonymousConnectionsEnabled"))

    @anonymous_connections_enabled.setter
    def anonymous_connections_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c80327eab36af5710cbe084a90b61f854b0c81d924f642d6835263a76ea01617)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "anonymousConnectionsEnabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d204c2e43ce5c553f6181c14badf3397a7950b11668bb8fbc8f0081c5428a78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43c77b6864e523046ed1cfc7d6cfd3c4aeafe37297c7b9a0ceb4f89a5530adcf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webPubsubId")
    def web_pubsub_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webPubsubId"))

    @web_pubsub_id.setter
    def web_pubsub_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01af10302c5a09b03733675f17936cbaba2dcb843ecafd207032f03e02db4a4b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webPubsubId", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.webPubsubHub.WebPubsubHubConfig",
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
        "web_pubsub_id": "webPubsubId",
        "anonymous_connections_enabled": "anonymousConnectionsEnabled",
        "event_handler": "eventHandler",
        "event_listener": "eventListener",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class WebPubsubHubConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        web_pubsub_id: builtins.str,
        anonymous_connections_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        event_handler: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WebPubsubHubEventHandler", typing.Dict[builtins.str, typing.Any]]]]] = None,
        event_listener: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["WebPubsubHubEventListener", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["WebPubsubHubTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#name WebPubsubHub#name}.
        :param web_pubsub_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#web_pubsub_id WebPubsubHub#web_pubsub_id}.
        :param anonymous_connections_enabled: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#anonymous_connections_enabled WebPubsubHub#anonymous_connections_enabled}.
        :param event_handler: event_handler block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#event_handler WebPubsubHub#event_handler}
        :param event_listener: event_listener block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#event_listener WebPubsubHub#event_listener}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#id WebPubsubHub#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#timeouts WebPubsubHub#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = WebPubsubHubTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ad1957f5ed5414c992525a58166f0aafac05ccc0bd83ea48835e9f0b04a7742)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument web_pubsub_id", value=web_pubsub_id, expected_type=type_hints["web_pubsub_id"])
            check_type(argname="argument anonymous_connections_enabled", value=anonymous_connections_enabled, expected_type=type_hints["anonymous_connections_enabled"])
            check_type(argname="argument event_handler", value=event_handler, expected_type=type_hints["event_handler"])
            check_type(argname="argument event_listener", value=event_listener, expected_type=type_hints["event_listener"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "web_pubsub_id": web_pubsub_id,
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
        if anonymous_connections_enabled is not None:
            self._values["anonymous_connections_enabled"] = anonymous_connections_enabled
        if event_handler is not None:
            self._values["event_handler"] = event_handler
        if event_listener is not None:
            self._values["event_listener"] = event_listener
        if id is not None:
            self._values["id"] = id
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#name WebPubsubHub#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def web_pubsub_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#web_pubsub_id WebPubsubHub#web_pubsub_id}.'''
        result = self._values.get("web_pubsub_id")
        assert result is not None, "Required property 'web_pubsub_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def anonymous_connections_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#anonymous_connections_enabled WebPubsubHub#anonymous_connections_enabled}.'''
        result = self._values.get("anonymous_connections_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def event_handler(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebPubsubHubEventHandler"]]]:
        '''event_handler block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#event_handler WebPubsubHub#event_handler}
        '''
        result = self._values.get("event_handler")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebPubsubHubEventHandler"]]], result)

    @builtins.property
    def event_listener(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebPubsubHubEventListener"]]]:
        '''event_listener block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#event_listener WebPubsubHub#event_listener}
        '''
        result = self._values.get("event_listener")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["WebPubsubHubEventListener"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#id WebPubsubHub#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["WebPubsubHubTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#timeouts WebPubsubHub#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["WebPubsubHubTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebPubsubHubConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.webPubsubHub.WebPubsubHubEventHandler",
    jsii_struct_bases=[],
    name_mapping={
        "url_template": "urlTemplate",
        "auth": "auth",
        "system_events": "systemEvents",
        "user_event_pattern": "userEventPattern",
    },
)
class WebPubsubHubEventHandler:
    def __init__(
        self,
        *,
        url_template: builtins.str,
        auth: typing.Optional[typing.Union["WebPubsubHubEventHandlerAuth", typing.Dict[builtins.str, typing.Any]]] = None,
        system_events: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_event_pattern: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param url_template: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#url_template WebPubsubHub#url_template}.
        :param auth: auth block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#auth WebPubsubHub#auth}
        :param system_events: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#system_events WebPubsubHub#system_events}.
        :param user_event_pattern: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#user_event_pattern WebPubsubHub#user_event_pattern}.
        '''
        if isinstance(auth, dict):
            auth = WebPubsubHubEventHandlerAuth(**auth)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52f930c4417d181acf9594b0234d2520ceefa3a68bfea4b653e6021312c808b1)
            check_type(argname="argument url_template", value=url_template, expected_type=type_hints["url_template"])
            check_type(argname="argument auth", value=auth, expected_type=type_hints["auth"])
            check_type(argname="argument system_events", value=system_events, expected_type=type_hints["system_events"])
            check_type(argname="argument user_event_pattern", value=user_event_pattern, expected_type=type_hints["user_event_pattern"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url_template": url_template,
        }
        if auth is not None:
            self._values["auth"] = auth
        if system_events is not None:
            self._values["system_events"] = system_events
        if user_event_pattern is not None:
            self._values["user_event_pattern"] = user_event_pattern

    @builtins.property
    def url_template(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#url_template WebPubsubHub#url_template}.'''
        result = self._values.get("url_template")
        assert result is not None, "Required property 'url_template' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def auth(self) -> typing.Optional["WebPubsubHubEventHandlerAuth"]:
        '''auth block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#auth WebPubsubHub#auth}
        '''
        result = self._values.get("auth")
        return typing.cast(typing.Optional["WebPubsubHubEventHandlerAuth"], result)

    @builtins.property
    def system_events(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#system_events WebPubsubHub#system_events}.'''
        result = self._values.get("system_events")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def user_event_pattern(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#user_event_pattern WebPubsubHub#user_event_pattern}.'''
        result = self._values.get("user_event_pattern")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebPubsubHubEventHandler(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.webPubsubHub.WebPubsubHubEventHandlerAuth",
    jsii_struct_bases=[],
    name_mapping={"managed_identity_id": "managedIdentityId"},
)
class WebPubsubHubEventHandlerAuth:
    def __init__(self, *, managed_identity_id: builtins.str) -> None:
        '''
        :param managed_identity_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#managed_identity_id WebPubsubHub#managed_identity_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c52f820b18c76c7b6295f4956fc11370519189789df52e1ed9f49465c2a3cf01)
            check_type(argname="argument managed_identity_id", value=managed_identity_id, expected_type=type_hints["managed_identity_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "managed_identity_id": managed_identity_id,
        }

    @builtins.property
    def managed_identity_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#managed_identity_id WebPubsubHub#managed_identity_id}.'''
        result = self._values.get("managed_identity_id")
        assert result is not None, "Required property 'managed_identity_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebPubsubHubEventHandlerAuth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WebPubsubHubEventHandlerAuthOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.webPubsubHub.WebPubsubHubEventHandlerAuthOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0318b242dfce0b5c6314f2879b977c449108b70d645713950a246dfb33d7d071)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="managedIdentityIdInput")
    def managed_identity_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managedIdentityIdInput"))

    @builtins.property
    @jsii.member(jsii_name="managedIdentityId")
    def managed_identity_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "managedIdentityId"))

    @managed_identity_id.setter
    def managed_identity_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__727fb3bff74d60c32b1ea5f2fc20644af5bd004b0273890ed31af9d843a434b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedIdentityId", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[WebPubsubHubEventHandlerAuth]:
        return typing.cast(typing.Optional[WebPubsubHubEventHandlerAuth], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[WebPubsubHubEventHandlerAuth],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9807a4409cb846d393bab6dbd111350ec2ebd6db8ba6a20c21f5b80e6a3ed32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WebPubsubHubEventHandlerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.webPubsubHub.WebPubsubHubEventHandlerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__13ba3dc4599db75556f14bb00e25630ca9903230faab9ce425e00079841a40fc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "WebPubsubHubEventHandlerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24d7158860d93dda730a81e55ec06b14472f17b43b3e435905e3378ea979d9ac)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WebPubsubHubEventHandlerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__048868787555933c60b905581e650555af9976220edb41f4eef13a4f81ce13f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e759262adda9399d4b60116796936e94ae746c95e6d12a70108fb17d3ed0e725)
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
            type_hints = typing.get_type_hints(_typecheckingstub__62e6fd1a4d9971306c3dc0f7c3e5220952d1d086681b12f69a2516fed00460f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebPubsubHubEventHandler]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebPubsubHubEventHandler]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebPubsubHubEventHandler]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c8e80a3f33063781a6513e72f137ada15e145365106309f59307341c9bb306a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WebPubsubHubEventHandlerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.webPubsubHub.WebPubsubHubEventHandlerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebf04b9f176e5a45b0ea4aec3e09dfd1e914629f63ac33b41347debb35d32bfb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putAuth")
    def put_auth(self, *, managed_identity_id: builtins.str) -> None:
        '''
        :param managed_identity_id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#managed_identity_id WebPubsubHub#managed_identity_id}.
        '''
        value = WebPubsubHubEventHandlerAuth(managed_identity_id=managed_identity_id)

        return typing.cast(None, jsii.invoke(self, "putAuth", [value]))

    @jsii.member(jsii_name="resetAuth")
    def reset_auth(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuth", []))

    @jsii.member(jsii_name="resetSystemEvents")
    def reset_system_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSystemEvents", []))

    @jsii.member(jsii_name="resetUserEventPattern")
    def reset_user_event_pattern(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserEventPattern", []))

    @builtins.property
    @jsii.member(jsii_name="auth")
    def auth(self) -> WebPubsubHubEventHandlerAuthOutputReference:
        return typing.cast(WebPubsubHubEventHandlerAuthOutputReference, jsii.get(self, "auth"))

    @builtins.property
    @jsii.member(jsii_name="authInput")
    def auth_input(self) -> typing.Optional[WebPubsubHubEventHandlerAuth]:
        return typing.cast(typing.Optional[WebPubsubHubEventHandlerAuth], jsii.get(self, "authInput"))

    @builtins.property
    @jsii.member(jsii_name="systemEventsInput")
    def system_events_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "systemEventsInput"))

    @builtins.property
    @jsii.member(jsii_name="urlTemplateInput")
    def url_template_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "urlTemplateInput"))

    @builtins.property
    @jsii.member(jsii_name="userEventPatternInput")
    def user_event_pattern_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userEventPatternInput"))

    @builtins.property
    @jsii.member(jsii_name="systemEvents")
    def system_events(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "systemEvents"))

    @system_events.setter
    def system_events(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d143acaea61d29e89a0dc5683f8b4d463e663a90250874836459b0c42f0ea320)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "systemEvents", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="urlTemplate")
    def url_template(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "urlTemplate"))

    @url_template.setter
    def url_template(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__753206a5f48161aae59248e0fe6cb2528b57882176c13c4df4f683574f1b9bb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "urlTemplate", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userEventPattern")
    def user_event_pattern(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "userEventPattern"))

    @user_event_pattern.setter
    def user_event_pattern(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e705ad2869c717450e32f373339466eb7382c2c4e6b4c5f15c726d6b8a48333)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userEventPattern", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WebPubsubHubEventHandler]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WebPubsubHubEventHandler]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WebPubsubHubEventHandler]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92120dd753fb6d676e379aa78f2c980d67ee8a65d9fa8bd3d421f736201816a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.webPubsubHub.WebPubsubHubEventListener",
    jsii_struct_bases=[],
    name_mapping={
        "eventhub_name": "eventhubName",
        "eventhub_namespace_name": "eventhubNamespaceName",
        "system_event_name_filter": "systemEventNameFilter",
        "user_event_name_filter": "userEventNameFilter",
    },
)
class WebPubsubHubEventListener:
    def __init__(
        self,
        *,
        eventhub_name: builtins.str,
        eventhub_namespace_name: builtins.str,
        system_event_name_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_event_name_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param eventhub_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#eventhub_name WebPubsubHub#eventhub_name}.
        :param eventhub_namespace_name: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#eventhub_namespace_name WebPubsubHub#eventhub_namespace_name}.
        :param system_event_name_filter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#system_event_name_filter WebPubsubHub#system_event_name_filter}.
        :param user_event_name_filter: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#user_event_name_filter WebPubsubHub#user_event_name_filter}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9b2c3777fa79740805b48cf51f99d18f7e22d4c9c845931b85fef4929cb7bec)
            check_type(argname="argument eventhub_name", value=eventhub_name, expected_type=type_hints["eventhub_name"])
            check_type(argname="argument eventhub_namespace_name", value=eventhub_namespace_name, expected_type=type_hints["eventhub_namespace_name"])
            check_type(argname="argument system_event_name_filter", value=system_event_name_filter, expected_type=type_hints["system_event_name_filter"])
            check_type(argname="argument user_event_name_filter", value=user_event_name_filter, expected_type=type_hints["user_event_name_filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "eventhub_name": eventhub_name,
            "eventhub_namespace_name": eventhub_namespace_name,
        }
        if system_event_name_filter is not None:
            self._values["system_event_name_filter"] = system_event_name_filter
        if user_event_name_filter is not None:
            self._values["user_event_name_filter"] = user_event_name_filter

    @builtins.property
    def eventhub_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#eventhub_name WebPubsubHub#eventhub_name}.'''
        result = self._values.get("eventhub_name")
        assert result is not None, "Required property 'eventhub_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def eventhub_namespace_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#eventhub_namespace_name WebPubsubHub#eventhub_namespace_name}.'''
        result = self._values.get("eventhub_namespace_name")
        assert result is not None, "Required property 'eventhub_namespace_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def system_event_name_filter(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#system_event_name_filter WebPubsubHub#system_event_name_filter}.'''
        result = self._values.get("system_event_name_filter")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def user_event_name_filter(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#user_event_name_filter WebPubsubHub#user_event_name_filter}.'''
        result = self._values.get("user_event_name_filter")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebPubsubHubEventListener(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WebPubsubHubEventListenerList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.webPubsubHub.WebPubsubHubEventListenerList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c20497d3cda061977edff70fec6dadc3c3c9a3f43fb5fd6a39da2c7e7603e79c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "WebPubsubHubEventListenerOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83151c48601eb0d81a8be13b58cc4189bc2d35b40caca0a28138766321f37118)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("WebPubsubHubEventListenerOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0ae743c0ca16b1a8398b8e07c3f2955894725395352a2811e8acb112c2aec2a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b68bbea4d6b13465ebf6539b2d343f56ddef7330075a32d50a2c3c58f8bf4276)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdc3d1d47e1c43976cea4dc1ce2ac7cafe1d54e88fbf50240c293d85f838255a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebPubsubHubEventListener]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebPubsubHubEventListener]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebPubsubHubEventListener]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd924ddf4cfb2103e76a2abbb1ea8c52ab43b07b0a5d92bde1c6b92ef15b0a78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class WebPubsubHubEventListenerOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.webPubsubHub.WebPubsubHubEventListenerOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__895f595911bec75fbefb49204b371ea6c6bfd98261679efb933181f916743475)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetSystemEventNameFilter")
    def reset_system_event_name_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSystemEventNameFilter", []))

    @jsii.member(jsii_name="resetUserEventNameFilter")
    def reset_user_event_name_filter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUserEventNameFilter", []))

    @builtins.property
    @jsii.member(jsii_name="eventhubNameInput")
    def eventhub_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventhubNameInput"))

    @builtins.property
    @jsii.member(jsii_name="eventhubNamespaceNameInput")
    def eventhub_namespace_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventhubNamespaceNameInput"))

    @builtins.property
    @jsii.member(jsii_name="systemEventNameFilterInput")
    def system_event_name_filter_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "systemEventNameFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="userEventNameFilterInput")
    def user_event_name_filter_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "userEventNameFilterInput"))

    @builtins.property
    @jsii.member(jsii_name="eventhubName")
    def eventhub_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventhubName"))

    @eventhub_name.setter
    def eventhub_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d00fe9c8e2cfc2cdf29572f9e7311f62d832a55d7724541e052c08266c908e6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventhubName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="eventhubNamespaceName")
    def eventhub_namespace_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventhubNamespaceName"))

    @eventhub_namespace_name.setter
    def eventhub_namespace_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3a13e7a1f6e92e256a8017e32f88889c8b0014e63e1645b1806533644c98d0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventhubNamespaceName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="systemEventNameFilter")
    def system_event_name_filter(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "systemEventNameFilter"))

    @system_event_name_filter.setter
    def system_event_name_filter(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d64d4fb8ce80091329f82e87a6e158241e6bd2176e534746ab3b5e7645b0b6bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "systemEventNameFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="userEventNameFilter")
    def user_event_name_filter(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "userEventNameFilter"))

    @user_event_name_filter.setter
    def user_event_name_filter(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__545af461702b67409ba3c84594ea1aec2af99c027f75f4a609ba43b8a02712c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userEventNameFilter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WebPubsubHubEventListener]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WebPubsubHubEventListener]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WebPubsubHubEventListener]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f15fc5bf9a9d9ecfe197e91901f8d95b45add95cf883e9acc0a654c1f4071f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.webPubsubHub.WebPubsubHubTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class WebPubsubHubTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#create WebPubsubHub#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#delete WebPubsubHub#delete}.
        :param read: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#read WebPubsubHub#read}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#update WebPubsubHub#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf4125e38895f36f1867d536cf288d287efc132c749e2280319c978b65a9b0d6)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#create WebPubsubHub#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#delete WebPubsubHub#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#read WebPubsubHub#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/azurerm/4.35.0/docs/resources/web_pubsub_hub#update WebPubsubHub#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WebPubsubHubTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WebPubsubHubTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.webPubsubHub.WebPubsubHubTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ff60cb9a6011d7d3d32f9257449aa77eab65c7e502e9e066cc843caad1f320b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d05eb02cb81d6db669b4bcc582d9b5c011765dbd231847d5db63cec551fc45c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99e5511019f7d13e9aa19c214685e8e49ef9b5a0933ec2ee081c61b8b650dcb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__635ea0c9b8fd514aee3808f4bb968b2e536792d5f6a8425171fc60ee00af9fa0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db02803e23e82506ae719fe525260a69573e41b89fe74f91ea7f8c49eb7006f5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WebPubsubHubTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WebPubsubHubTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WebPubsubHubTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8883886aac61bab5637d18e5f60ebd6f4bf55284d1d30e84a2da61123068ab0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "WebPubsubHub",
    "WebPubsubHubConfig",
    "WebPubsubHubEventHandler",
    "WebPubsubHubEventHandlerAuth",
    "WebPubsubHubEventHandlerAuthOutputReference",
    "WebPubsubHubEventHandlerList",
    "WebPubsubHubEventHandlerOutputReference",
    "WebPubsubHubEventListener",
    "WebPubsubHubEventListenerList",
    "WebPubsubHubEventListenerOutputReference",
    "WebPubsubHubTimeouts",
    "WebPubsubHubTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__494d001c058f88d4cfa6c4d4872ef2775486e2fcc2e47f615196300f3fe02139(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    web_pubsub_id: builtins.str,
    anonymous_connections_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    event_handler: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebPubsubHubEventHandler, typing.Dict[builtins.str, typing.Any]]]]] = None,
    event_listener: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebPubsubHubEventListener, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[WebPubsubHubTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__b7d53ed775d5e9bf43940a26a9f9c9cfe316a0674023a5e95bcf1a77e0a21a43(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ac49fede4b8c8fe2a1ce70926fe7286bdb4199c0548b82e927689eec0e2d586(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebPubsubHubEventHandler, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13ac5cd2c99174fcd69c0cc6359922379abbbe7a6107104709a0fbcc3b0b7005(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebPubsubHubEventListener, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c80327eab36af5710cbe084a90b61f854b0c81d924f642d6835263a76ea01617(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d204c2e43ce5c553f6181c14badf3397a7950b11668bb8fbc8f0081c5428a78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43c77b6864e523046ed1cfc7d6cfd3c4aeafe37297c7b9a0ceb4f89a5530adcf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01af10302c5a09b03733675f17936cbaba2dcb843ecafd207032f03e02db4a4b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ad1957f5ed5414c992525a58166f0aafac05ccc0bd83ea48835e9f0b04a7742(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    web_pubsub_id: builtins.str,
    anonymous_connections_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    event_handler: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebPubsubHubEventHandler, typing.Dict[builtins.str, typing.Any]]]]] = None,
    event_listener: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[WebPubsubHubEventListener, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[WebPubsubHubTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52f930c4417d181acf9594b0234d2520ceefa3a68bfea4b653e6021312c808b1(
    *,
    url_template: builtins.str,
    auth: typing.Optional[typing.Union[WebPubsubHubEventHandlerAuth, typing.Dict[builtins.str, typing.Any]]] = None,
    system_events: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_event_pattern: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c52f820b18c76c7b6295f4956fc11370519189789df52e1ed9f49465c2a3cf01(
    *,
    managed_identity_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0318b242dfce0b5c6314f2879b977c449108b70d645713950a246dfb33d7d071(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__727fb3bff74d60c32b1ea5f2fc20644af5bd004b0273890ed31af9d843a434b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9807a4409cb846d393bab6dbd111350ec2ebd6db8ba6a20c21f5b80e6a3ed32(
    value: typing.Optional[WebPubsubHubEventHandlerAuth],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13ba3dc4599db75556f14bb00e25630ca9903230faab9ce425e00079841a40fc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24d7158860d93dda730a81e55ec06b14472f17b43b3e435905e3378ea979d9ac(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__048868787555933c60b905581e650555af9976220edb41f4eef13a4f81ce13f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e759262adda9399d4b60116796936e94ae746c95e6d12a70108fb17d3ed0e725(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62e6fd1a4d9971306c3dc0f7c3e5220952d1d086681b12f69a2516fed00460f2(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c8e80a3f33063781a6513e72f137ada15e145365106309f59307341c9bb306a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebPubsubHubEventHandler]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebf04b9f176e5a45b0ea4aec3e09dfd1e914629f63ac33b41347debb35d32bfb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d143acaea61d29e89a0dc5683f8b4d463e663a90250874836459b0c42f0ea320(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__753206a5f48161aae59248e0fe6cb2528b57882176c13c4df4f683574f1b9bb2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e705ad2869c717450e32f373339466eb7382c2c4e6b4c5f15c726d6b8a48333(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92120dd753fb6d676e379aa78f2c980d67ee8a65d9fa8bd3d421f736201816a8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WebPubsubHubEventHandler]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9b2c3777fa79740805b48cf51f99d18f7e22d4c9c845931b85fef4929cb7bec(
    *,
    eventhub_name: builtins.str,
    eventhub_namespace_name: builtins.str,
    system_event_name_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_event_name_filter: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c20497d3cda061977edff70fec6dadc3c3c9a3f43fb5fd6a39da2c7e7603e79c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83151c48601eb0d81a8be13b58cc4189bc2d35b40caca0a28138766321f37118(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0ae743c0ca16b1a8398b8e07c3f2955894725395352a2811e8acb112c2aec2a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b68bbea4d6b13465ebf6539b2d343f56ddef7330075a32d50a2c3c58f8bf4276(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdc3d1d47e1c43976cea4dc1ce2ac7cafe1d54e88fbf50240c293d85f838255a(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd924ddf4cfb2103e76a2abbb1ea8c52ab43b07b0a5d92bde1c6b92ef15b0a78(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[WebPubsubHubEventListener]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__895f595911bec75fbefb49204b371ea6c6bfd98261679efb933181f916743475(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d00fe9c8e2cfc2cdf29572f9e7311f62d832a55d7724541e052c08266c908e6a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3a13e7a1f6e92e256a8017e32f88889c8b0014e63e1645b1806533644c98d0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d64d4fb8ce80091329f82e87a6e158241e6bd2176e534746ab3b5e7645b0b6bf(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__545af461702b67409ba3c84594ea1aec2af99c027f75f4a609ba43b8a02712c6(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f15fc5bf9a9d9ecfe197e91901f8d95b45add95cf883e9acc0a654c1f4071f8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WebPubsubHubEventListener]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf4125e38895f36f1867d536cf288d287efc132c749e2280319c978b65a9b0d6(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ff60cb9a6011d7d3d32f9257449aa77eab65c7e502e9e066cc843caad1f320b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d05eb02cb81d6db669b4bcc582d9b5c011765dbd231847d5db63cec551fc45c9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99e5511019f7d13e9aa19c214685e8e49ef9b5a0933ec2ee081c61b8b650dcb3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__635ea0c9b8fd514aee3808f4bb968b2e536792d5f6a8425171fc60ee00af9fa0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db02803e23e82506ae719fe525260a69573e41b89fe74f91ea7f8c49eb7006f5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8883886aac61bab5637d18e5f60ebd6f4bf55284d1d30e84a2da61123068ab0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, WebPubsubHubTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
