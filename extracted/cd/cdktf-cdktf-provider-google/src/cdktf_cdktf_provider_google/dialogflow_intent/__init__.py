r'''
# `google_dialogflow_intent`

Refer to the Terraform Registry for docs: [`google_dialogflow_intent`](https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent).
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


class DialogflowIntent(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowIntent.DialogflowIntent",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent google_dialogflow_intent}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        action: typing.Optional[builtins.str] = None,
        default_response_platforms: typing.Optional[typing.Sequence[builtins.str]] = None,
        events: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        input_context_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        is_fallback: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ml_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        parent_followup_intent_name: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        reset_contexts: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["DialogflowIntentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        webhook_state: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent google_dialogflow_intent} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: The name of this intent to be displayed on the console. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#display_name DialogflowIntent#display_name}
        :param action: The name of the action associated with the intent. Note: The action name must not contain whitespaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#action DialogflowIntent#action}
        :param default_response_platforms: The list of platforms for which the first responses will be copied from the messages in PLATFORM_UNSPECIFIED (i.e. default platform). Possible values: ["FACEBOOK", "SLACK", "TELEGRAM", "KIK", "SKYPE", "LINE", "VIBER", "ACTIONS_ON_GOOGLE", "GOOGLE_HANGOUTS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#default_response_platforms DialogflowIntent#default_response_platforms}
        :param events: The collection of event names that trigger the intent. If the collection of input contexts is not empty, all of the contexts must be present in the active user session for an event to trigger this intent. See the `events reference <https://cloud.google.com/dialogflow/docs/events-overview>`_ for more details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#events DialogflowIntent#events}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#id DialogflowIntent#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param input_context_names: The list of context names required for this intent to be triggered. Format: projects//agent/sessions/-/contexts/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#input_context_names DialogflowIntent#input_context_names}
        :param is_fallback: Indicates whether this is a fallback intent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#is_fallback DialogflowIntent#is_fallback}
        :param ml_disabled: Indicates whether Machine Learning is disabled for the intent. Note: If mlDisabled setting is set to true, then this intent is not taken into account during inference in ML ONLY match mode. Also, auto-markup in the UI is turned off. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#ml_disabled DialogflowIntent#ml_disabled}
        :param parent_followup_intent_name: The unique identifier of the parent intent in the chain of followup intents. Format: projects//agent/intents/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#parent_followup_intent_name DialogflowIntent#parent_followup_intent_name}
        :param priority: The priority of this intent. Higher numbers represent higher priorities. - If the supplied value is unspecified or 0, the service translates the value to 500,000, which corresponds to the Normal priority in the console. - If the supplied value is negative, the intent is ignored in runtime detect intent requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#priority DialogflowIntent#priority}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#project DialogflowIntent#project}.
        :param reset_contexts: Indicates whether to delete all contexts in the current session when this intent is matched. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#reset_contexts DialogflowIntent#reset_contexts}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#timeouts DialogflowIntent#timeouts}
        :param webhook_state: Indicates whether webhooks are enabled for the intent. - WEBHOOK_STATE_ENABLED: Webhook is enabled in the agent and in the intent. - WEBHOOK_STATE_ENABLED_FOR_SLOT_FILLING: Webhook is enabled in the agent and in the intent. Also, each slot filling prompt is forwarded to the webhook. Possible values: ["WEBHOOK_STATE_ENABLED", "WEBHOOK_STATE_ENABLED_FOR_SLOT_FILLING"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#webhook_state DialogflowIntent#webhook_state}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4a93aa64c3d7b20fb3cbe08453876c8330cbf97d07acacea02f51ca17066710)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DialogflowIntentConfig(
            display_name=display_name,
            action=action,
            default_response_platforms=default_response_platforms,
            events=events,
            id=id,
            input_context_names=input_context_names,
            is_fallback=is_fallback,
            ml_disabled=ml_disabled,
            parent_followup_intent_name=parent_followup_intent_name,
            priority=priority,
            project=project,
            reset_contexts=reset_contexts,
            timeouts=timeouts,
            webhook_state=webhook_state,
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
        '''Generates CDKTF code for importing a DialogflowIntent resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DialogflowIntent to import.
        :param import_from_id: The id of the existing DialogflowIntent that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DialogflowIntent to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec321396834b910ae269ed8b15dee61a0627d7b110866bbcd749788d0abf53e3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#create DialogflowIntent#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#delete DialogflowIntent#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#update DialogflowIntent#update}.
        '''
        value = DialogflowIntentTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAction")
    def reset_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAction", []))

    @jsii.member(jsii_name="resetDefaultResponsePlatforms")
    def reset_default_response_platforms(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultResponsePlatforms", []))

    @jsii.member(jsii_name="resetEvents")
    def reset_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEvents", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetInputContextNames")
    def reset_input_context_names(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInputContextNames", []))

    @jsii.member(jsii_name="resetIsFallback")
    def reset_is_fallback(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsFallback", []))

    @jsii.member(jsii_name="resetMlDisabled")
    def reset_ml_disabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMlDisabled", []))

    @jsii.member(jsii_name="resetParentFollowupIntentName")
    def reset_parent_followup_intent_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParentFollowupIntentName", []))

    @jsii.member(jsii_name="resetPriority")
    def reset_priority(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPriority", []))

    @jsii.member(jsii_name="resetProject")
    def reset_project(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProject", []))

    @jsii.member(jsii_name="resetResetContexts")
    def reset_reset_contexts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResetContexts", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetWebhookState")
    def reset_webhook_state(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebhookState", []))

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
    @jsii.member(jsii_name="followupIntentInfo")
    def followup_intent_info(self) -> "DialogflowIntentFollowupIntentInfoList":
        return typing.cast("DialogflowIntentFollowupIntentInfoList", jsii.get(self, "followupIntentInfo"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="rootFollowupIntentName")
    def root_followup_intent_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "rootFollowupIntentName"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DialogflowIntentTimeoutsOutputReference":
        return typing.cast("DialogflowIntentTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultResponsePlatformsInput")
    def default_response_platforms_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "defaultResponsePlatformsInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="eventsInput")
    def events_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "eventsInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="inputContextNamesInput")
    def input_context_names_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "inputContextNamesInput"))

    @builtins.property
    @jsii.member(jsii_name="isFallbackInput")
    def is_fallback_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isFallbackInput"))

    @builtins.property
    @jsii.member(jsii_name="mlDisabledInput")
    def ml_disabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "mlDisabledInput"))

    @builtins.property
    @jsii.member(jsii_name="parentFollowupIntentNameInput")
    def parent_followup_intent_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentFollowupIntentNameInput"))

    @builtins.property
    @jsii.member(jsii_name="priorityInput")
    def priority_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "priorityInput"))

    @builtins.property
    @jsii.member(jsii_name="projectInput")
    def project_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectInput"))

    @builtins.property
    @jsii.member(jsii_name="resetContextsInput")
    def reset_contexts_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "resetContextsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DialogflowIntentTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DialogflowIntentTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="webhookStateInput")
    def webhook_state_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "webhookStateInput"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @action.setter
    def action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4921b005e4bb14b8e60b709c4beb4056cd117d9d3da53eabfe36ed717bb5b319)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="defaultResponsePlatforms")
    def default_response_platforms(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "defaultResponsePlatforms"))

    @default_response_platforms.setter
    def default_response_platforms(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__873113a17ac318b3ac80ea69d85fdea280b9e49927a87f2b54d7bf6d4f31d759)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultResponsePlatforms", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77a1edb79e179200b61aa3ffb65a55d453fc0ef97445a587e81edcf34c87158f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="events")
    def events(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "events"))

    @events.setter
    def events(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e846d49b6d741a57fc832cb576d525018a6880f5367c7e0b991f648a0a8b5558)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "events", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b059748387f543bf73a53f71eb2e6b64c75d959015fc07bcdf5b424e50a6691)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="inputContextNames")
    def input_context_names(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "inputContextNames"))

    @input_context_names.setter
    def input_context_names(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91e32c9bec6a290a7ec3348274725c82db52daf96989baf0d17fb4769c4a6f61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inputContextNames", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isFallback")
    def is_fallback(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isFallback"))

    @is_fallback.setter
    def is_fallback(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e26ae699b31a1a88eac93feacfb27c10814f2608ca236797f1be9c2a6993c9df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isFallback", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="mlDisabled")
    def ml_disabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "mlDisabled"))

    @ml_disabled.setter
    def ml_disabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e70d408c1166c3f7214f9fa0de58f2bf16abd77a8b6358bd87aef931e6f52f96)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mlDisabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parentFollowupIntentName")
    def parent_followup_intent_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parentFollowupIntentName"))

    @parent_followup_intent_name.setter
    def parent_followup_intent_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a459b91037419e3abb93348a95f98d32d63fa1c4f455a3cd401ee42350fe99a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parentFollowupIntentName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1bf5076b32527089be3280f1c067e20df148fe7a7b85a101937002b984b3b31)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @project.setter
    def project(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b59a22f202afa440caa3eb5699389a8233d4af19e60bb9fe9aadc4473401d51c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "project", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="resetContexts")
    def reset_contexts(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "resetContexts"))

    @reset_contexts.setter
    def reset_contexts(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e34914f2c9ce5ee30e6b8080db3b0aef17d10d76bdfe9afe9343eeb0a0daa41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resetContexts", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webhookState")
    def webhook_state(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webhookState"))

    @webhook_state.setter
    def webhook_state(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f096c2dd2ef9a5633cc58c5c9e144822e6c07707656138cb8e18354d33891107)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webhookState", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowIntent.DialogflowIntentConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "display_name": "displayName",
        "action": "action",
        "default_response_platforms": "defaultResponsePlatforms",
        "events": "events",
        "id": "id",
        "input_context_names": "inputContextNames",
        "is_fallback": "isFallback",
        "ml_disabled": "mlDisabled",
        "parent_followup_intent_name": "parentFollowupIntentName",
        "priority": "priority",
        "project": "project",
        "reset_contexts": "resetContexts",
        "timeouts": "timeouts",
        "webhook_state": "webhookState",
    },
)
class DialogflowIntentConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        display_name: builtins.str,
        action: typing.Optional[builtins.str] = None,
        default_response_platforms: typing.Optional[typing.Sequence[builtins.str]] = None,
        events: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        input_context_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        is_fallback: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ml_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        parent_followup_intent_name: typing.Optional[builtins.str] = None,
        priority: typing.Optional[jsii.Number] = None,
        project: typing.Optional[builtins.str] = None,
        reset_contexts: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["DialogflowIntentTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        webhook_state: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: The name of this intent to be displayed on the console. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#display_name DialogflowIntent#display_name}
        :param action: The name of the action associated with the intent. Note: The action name must not contain whitespaces. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#action DialogflowIntent#action}
        :param default_response_platforms: The list of platforms for which the first responses will be copied from the messages in PLATFORM_UNSPECIFIED (i.e. default platform). Possible values: ["FACEBOOK", "SLACK", "TELEGRAM", "KIK", "SKYPE", "LINE", "VIBER", "ACTIONS_ON_GOOGLE", "GOOGLE_HANGOUTS"]. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#default_response_platforms DialogflowIntent#default_response_platforms}
        :param events: The collection of event names that trigger the intent. If the collection of input contexts is not empty, all of the contexts must be present in the active user session for an event to trigger this intent. See the `events reference <https://cloud.google.com/dialogflow/docs/events-overview>`_ for more details. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#events DialogflowIntent#events}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#id DialogflowIntent#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param input_context_names: The list of context names required for this intent to be triggered. Format: projects//agent/sessions/-/contexts/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#input_context_names DialogflowIntent#input_context_names}
        :param is_fallback: Indicates whether this is a fallback intent. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#is_fallback DialogflowIntent#is_fallback}
        :param ml_disabled: Indicates whether Machine Learning is disabled for the intent. Note: If mlDisabled setting is set to true, then this intent is not taken into account during inference in ML ONLY match mode. Also, auto-markup in the UI is turned off. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#ml_disabled DialogflowIntent#ml_disabled}
        :param parent_followup_intent_name: The unique identifier of the parent intent in the chain of followup intents. Format: projects//agent/intents/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#parent_followup_intent_name DialogflowIntent#parent_followup_intent_name}
        :param priority: The priority of this intent. Higher numbers represent higher priorities. - If the supplied value is unspecified or 0, the service translates the value to 500,000, which corresponds to the Normal priority in the console. - If the supplied value is negative, the intent is ignored in runtime detect intent requests. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#priority DialogflowIntent#priority}
        :param project: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#project DialogflowIntent#project}.
        :param reset_contexts: Indicates whether to delete all contexts in the current session when this intent is matched. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#reset_contexts DialogflowIntent#reset_contexts}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#timeouts DialogflowIntent#timeouts}
        :param webhook_state: Indicates whether webhooks are enabled for the intent. - WEBHOOK_STATE_ENABLED: Webhook is enabled in the agent and in the intent. - WEBHOOK_STATE_ENABLED_FOR_SLOT_FILLING: Webhook is enabled in the agent and in the intent. Also, each slot filling prompt is forwarded to the webhook. Possible values: ["WEBHOOK_STATE_ENABLED", "WEBHOOK_STATE_ENABLED_FOR_SLOT_FILLING"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#webhook_state DialogflowIntent#webhook_state}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = DialogflowIntentTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__063bd323b036fb4733f70655ac03b1bbec2b19c5290c7249c60c1e3e4cb0ac05)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument default_response_platforms", value=default_response_platforms, expected_type=type_hints["default_response_platforms"])
            check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument input_context_names", value=input_context_names, expected_type=type_hints["input_context_names"])
            check_type(argname="argument is_fallback", value=is_fallback, expected_type=type_hints["is_fallback"])
            check_type(argname="argument ml_disabled", value=ml_disabled, expected_type=type_hints["ml_disabled"])
            check_type(argname="argument parent_followup_intent_name", value=parent_followup_intent_name, expected_type=type_hints["parent_followup_intent_name"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument reset_contexts", value=reset_contexts, expected_type=type_hints["reset_contexts"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument webhook_state", value=webhook_state, expected_type=type_hints["webhook_state"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "display_name": display_name,
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
        if action is not None:
            self._values["action"] = action
        if default_response_platforms is not None:
            self._values["default_response_platforms"] = default_response_platforms
        if events is not None:
            self._values["events"] = events
        if id is not None:
            self._values["id"] = id
        if input_context_names is not None:
            self._values["input_context_names"] = input_context_names
        if is_fallback is not None:
            self._values["is_fallback"] = is_fallback
        if ml_disabled is not None:
            self._values["ml_disabled"] = ml_disabled
        if parent_followup_intent_name is not None:
            self._values["parent_followup_intent_name"] = parent_followup_intent_name
        if priority is not None:
            self._values["priority"] = priority
        if project is not None:
            self._values["project"] = project
        if reset_contexts is not None:
            self._values["reset_contexts"] = reset_contexts
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if webhook_state is not None:
            self._values["webhook_state"] = webhook_state

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
    def display_name(self) -> builtins.str:
        '''The name of this intent to be displayed on the console.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#display_name DialogflowIntent#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def action(self) -> typing.Optional[builtins.str]:
        '''The name of the action associated with the intent. Note: The action name must not contain whitespaces.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#action DialogflowIntent#action}
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default_response_platforms(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of platforms for which the first responses will be copied from the messages in PLATFORM_UNSPECIFIED (i.e. default platform). Possible values: ["FACEBOOK", "SLACK", "TELEGRAM", "KIK", "SKYPE", "LINE", "VIBER", "ACTIONS_ON_GOOGLE", "GOOGLE_HANGOUTS"].

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#default_response_platforms DialogflowIntent#default_response_platforms}
        '''
        result = self._values.get("default_response_platforms")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def events(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The collection of event names that trigger the intent.

        If the collection of input contexts is not empty, all of
        the contexts must be present in the active user session for an event to trigger this intent. See the
        `events reference <https://cloud.google.com/dialogflow/docs/events-overview>`_ for more details.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#events DialogflowIntent#events}
        '''
        result = self._values.get("events")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#id DialogflowIntent#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def input_context_names(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of context names required for this intent to be triggered. Format: projects//agent/sessions/-/contexts/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#input_context_names DialogflowIntent#input_context_names}
        '''
        result = self._values.get("input_context_names")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def is_fallback(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether this is a fallback intent.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#is_fallback DialogflowIntent#is_fallback}
        '''
        result = self._values.get("is_fallback")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ml_disabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether Machine Learning is disabled for the intent.

        Note: If mlDisabled setting is set to true, then this intent is not taken into account during inference in ML
        ONLY match mode. Also, auto-markup in the UI is turned off.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#ml_disabled DialogflowIntent#ml_disabled}
        '''
        result = self._values.get("ml_disabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def parent_followup_intent_name(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the parent intent in the chain of followup intents. Format: projects//agent/intents/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#parent_followup_intent_name DialogflowIntent#parent_followup_intent_name}
        '''
        result = self._values.get("parent_followup_intent_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        '''The priority of this intent.

        Higher numbers represent higher priorities.

        - If the supplied value is unspecified or 0, the service translates the value to 500,000, which corresponds
          to the Normal priority in the console.
        - If the supplied value is negative, the intent is ignored in runtime detect intent requests.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#priority DialogflowIntent#priority}
        '''
        result = self._values.get("priority")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#project DialogflowIntent#project}.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reset_contexts(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Indicates whether to delete all contexts in the current session when this intent is matched.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#reset_contexts DialogflowIntent#reset_contexts}
        '''
        result = self._values.get("reset_contexts")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DialogflowIntentTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#timeouts DialogflowIntent#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DialogflowIntentTimeouts"], result)

    @builtins.property
    def webhook_state(self) -> typing.Optional[builtins.str]:
        '''Indicates whether webhooks are enabled for the intent.

        - WEBHOOK_STATE_ENABLED: Webhook is enabled in the agent and in the intent.
        - WEBHOOK_STATE_ENABLED_FOR_SLOT_FILLING: Webhook is enabled in the agent and in the intent. Also, each slot
          filling prompt is forwarded to the webhook. Possible values: ["WEBHOOK_STATE_ENABLED", "WEBHOOK_STATE_ENABLED_FOR_SLOT_FILLING"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#webhook_state DialogflowIntent#webhook_state}
        '''
        result = self._values.get("webhook_state")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowIntentConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowIntent.DialogflowIntentFollowupIntentInfo",
    jsii_struct_bases=[],
    name_mapping={},
)
class DialogflowIntentFollowupIntentInfo:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowIntentFollowupIntentInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowIntentFollowupIntentInfoList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowIntent.DialogflowIntentFollowupIntentInfoList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b480bace0606188cce06b079d61b2a0dbf39d7efb74953fabc070440ed47b52)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DialogflowIntentFollowupIntentInfoOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4b8430ed85977ac410f19bddc7d5de03e1610666b00145d4141343b5cf6481a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DialogflowIntentFollowupIntentInfoOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19d6f817c1fc99e8291a92dd6987cc4492ae6e7bd55ff0319659f07627a16a22)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a271af95fee864991f5971ce08fdd3f574c58f4cdd7842a9269b25fec82a262)
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
            type_hints = typing.get_type_hints(_typecheckingstub__56c6abc8644e74ac31535d5bdd0d1b2e9e1c14faab17e91bbb52b88f30a00e5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]


class DialogflowIntentFollowupIntentInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowIntent.DialogflowIntentFollowupIntentInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ff9a86c43461362d8fc9b567c63f4c04d41d8254f9fe0d91fb61142bf6552f8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="followupIntentName")
    def followup_intent_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "followupIntentName"))

    @builtins.property
    @jsii.member(jsii_name="parentFollowupIntentName")
    def parent_followup_intent_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parentFollowupIntentName"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DialogflowIntentFollowupIntentInfo]:
        return typing.cast(typing.Optional[DialogflowIntentFollowupIntentInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowIntentFollowupIntentInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28af1d695232273b8780c26c587ed80ba2f232f08ce96831e2264aa29747b5f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowIntent.DialogflowIntentTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DialogflowIntentTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#create DialogflowIntent#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#delete DialogflowIntent#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#update DialogflowIntent#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__921663e6d29f9b348c192fe4ef1940eead176375063b4390ff6e62a8c5fef619)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#create DialogflowIntent#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#delete DialogflowIntent#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.45.0/docs/resources/dialogflow_intent#update DialogflowIntent#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowIntentTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowIntentTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowIntent.DialogflowIntentTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__84a60dfa8a98a3e800c7afdc31638849ed8bd6e160869ebe4f30261bd8384df5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ff908ad69f1498f6560b2c94de1fb63657194f8470e5c3731b934564f52a6bb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91cfb538a2af117f4aa0d9e07a767fb69bc64452c65f2622bca03bbfba6c3b97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e28cb69384e251a9d5f4498df20b4faf7780cb1f4d38feeebde639df92e046b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowIntentTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowIntentTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowIntentTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21813259c729eceabd36518551ccb18a1a88e7b3f4ebec84ccdfd06fda8a9a25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DialogflowIntent",
    "DialogflowIntentConfig",
    "DialogflowIntentFollowupIntentInfo",
    "DialogflowIntentFollowupIntentInfoList",
    "DialogflowIntentFollowupIntentInfoOutputReference",
    "DialogflowIntentTimeouts",
    "DialogflowIntentTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__e4a93aa64c3d7b20fb3cbe08453876c8330cbf97d07acacea02f51ca17066710(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    action: typing.Optional[builtins.str] = None,
    default_response_platforms: typing.Optional[typing.Sequence[builtins.str]] = None,
    events: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    input_context_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    is_fallback: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ml_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    parent_followup_intent_name: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    project: typing.Optional[builtins.str] = None,
    reset_contexts: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[DialogflowIntentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    webhook_state: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__ec321396834b910ae269ed8b15dee61a0627d7b110866bbcd749788d0abf53e3(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4921b005e4bb14b8e60b709c4beb4056cd117d9d3da53eabfe36ed717bb5b319(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__873113a17ac318b3ac80ea69d85fdea280b9e49927a87f2b54d7bf6d4f31d759(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77a1edb79e179200b61aa3ffb65a55d453fc0ef97445a587e81edcf34c87158f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e846d49b6d741a57fc832cb576d525018a6880f5367c7e0b991f648a0a8b5558(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b059748387f543bf73a53f71eb2e6b64c75d959015fc07bcdf5b424e50a6691(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91e32c9bec6a290a7ec3348274725c82db52daf96989baf0d17fb4769c4a6f61(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e26ae699b31a1a88eac93feacfb27c10814f2608ca236797f1be9c2a6993c9df(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e70d408c1166c3f7214f9fa0de58f2bf16abd77a8b6358bd87aef931e6f52f96(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a459b91037419e3abb93348a95f98d32d63fa1c4f455a3cd401ee42350fe99a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1bf5076b32527089be3280f1c067e20df148fe7a7b85a101937002b984b3b31(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b59a22f202afa440caa3eb5699389a8233d4af19e60bb9fe9aadc4473401d51c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e34914f2c9ce5ee30e6b8080db3b0aef17d10d76bdfe9afe9343eeb0a0daa41(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f096c2dd2ef9a5633cc58c5c9e144822e6c07707656138cb8e18354d33891107(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__063bd323b036fb4733f70655ac03b1bbec2b19c5290c7249c60c1e3e4cb0ac05(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: builtins.str,
    action: typing.Optional[builtins.str] = None,
    default_response_platforms: typing.Optional[typing.Sequence[builtins.str]] = None,
    events: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    input_context_names: typing.Optional[typing.Sequence[builtins.str]] = None,
    is_fallback: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ml_disabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    parent_followup_intent_name: typing.Optional[builtins.str] = None,
    priority: typing.Optional[jsii.Number] = None,
    project: typing.Optional[builtins.str] = None,
    reset_contexts: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[DialogflowIntentTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    webhook_state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b480bace0606188cce06b079d61b2a0dbf39d7efb74953fabc070440ed47b52(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4b8430ed85977ac410f19bddc7d5de03e1610666b00145d4141343b5cf6481a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19d6f817c1fc99e8291a92dd6987cc4492ae6e7bd55ff0319659f07627a16a22(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a271af95fee864991f5971ce08fdd3f574c58f4cdd7842a9269b25fec82a262(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56c6abc8644e74ac31535d5bdd0d1b2e9e1c14faab17e91bbb52b88f30a00e5e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ff9a86c43461362d8fc9b567c63f4c04d41d8254f9fe0d91fb61142bf6552f8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28af1d695232273b8780c26c587ed80ba2f232f08ce96831e2264aa29747b5f7(
    value: typing.Optional[DialogflowIntentFollowupIntentInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__921663e6d29f9b348c192fe4ef1940eead176375063b4390ff6e62a8c5fef619(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84a60dfa8a98a3e800c7afdc31638849ed8bd6e160869ebe4f30261bd8384df5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff908ad69f1498f6560b2c94de1fb63657194f8470e5c3731b934564f52a6bb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91cfb538a2af117f4aa0d9e07a767fb69bc64452c65f2622bca03bbfba6c3b97(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e28cb69384e251a9d5f4498df20b4faf7780cb1f4d38feeebde639df92e046b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21813259c729eceabd36518551ccb18a1a88e7b3f4ebec84ccdfd06fda8a9a25(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowIntentTimeouts]],
) -> None:
    """Type checking stubs"""
    pass
