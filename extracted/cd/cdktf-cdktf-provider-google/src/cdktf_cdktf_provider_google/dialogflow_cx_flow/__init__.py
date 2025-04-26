r'''
# `google_dialogflow_cx_flow`

Refer to the Terraform Registry for docs: [`google_dialogflow_cx_flow`](https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow).
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


class DialogflowCxFlow(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlow",
):
    '''Represents a {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow google_dialogflow_cx_flow}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        display_name: builtins.str,
        advanced_settings: typing.Optional[typing.Union["DialogflowCxFlowAdvancedSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        event_handlers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxFlowEventHandlers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        is_default_start_flow: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        language_code: typing.Optional[builtins.str] = None,
        nlu_settings: typing.Optional[typing.Union["DialogflowCxFlowNluSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        parent: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DialogflowCxFlowTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        transition_route_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        transition_routes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxFlowTransitionRoutes", typing.Dict[builtins.str, typing.Any]]]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow google_dialogflow_cx_flow} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param display_name: The human-readable name of the flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#display_name DialogflowCxFlow#display_name}
        :param advanced_settings: advanced_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#advanced_settings DialogflowCxFlow#advanced_settings}
        :param description: The description of the flow. The maximum length is 500 characters. If exceeded, the request is rejected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#description DialogflowCxFlow#description}
        :param event_handlers: event_handlers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#event_handlers DialogflowCxFlow#event_handlers}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#id DialogflowCxFlow#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_default_start_flow: Marks this as the `Default Start Flow <https://cloud.google.com/dialogflow/cx/docs/concept/flow#start>`_ for an agent. When you create an agent, the Default Start Flow is created automatically. The Default Start Flow cannot be deleted; deleting the 'google_dialogflow_cx_flow' resource does nothing to the underlying GCP resources. ~> Avoid having multiple 'google_dialogflow_cx_flow' resources linked to the same agent with 'is_default_start_flow = true' because they will compete to control a single Default Start Flow resource in GCP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#is_default_start_flow DialogflowCxFlow#is_default_start_flow}
        :param language_code: The language of the following fields in flow: Flow.event_handlers.trigger_fulfillment.messages Flow.event_handlers.trigger_fulfillment.conditional_cases Flow.transition_routes.trigger_fulfillment.messages Flow.transition_routes.trigger_fulfillment.conditional_cases If not specified, the agent's default language is used. Many languages are supported. Note: languages must be enabled in the agent before they can be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#language_code DialogflowCxFlow#language_code}
        :param nlu_settings: nlu_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#nlu_settings DialogflowCxFlow#nlu_settings}
        :param parent: The agent to create a flow for. Format: projects//locations//agents/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#parent DialogflowCxFlow#parent}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#timeouts DialogflowCxFlow#timeouts}
        :param transition_route_groups: A flow's transition route group serve two purposes: They are responsible for matching the user's first utterances in the flow. They are inherited by every page's [transition route groups][Page.transition_route_groups]. Transition route groups defined in the page have higher priority than those defined in the flow. Format:projects//locations//agents//flows//transitionRouteGroups/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#transition_route_groups DialogflowCxFlow#transition_route_groups}
        :param transition_routes: transition_routes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#transition_routes DialogflowCxFlow#transition_routes}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4e73e5829492f4b7c2b1b1017035124904b70f6aaa69feef28577dda886dac1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = DialogflowCxFlowConfig(
            display_name=display_name,
            advanced_settings=advanced_settings,
            description=description,
            event_handlers=event_handlers,
            id=id,
            is_default_start_flow=is_default_start_flow,
            language_code=language_code,
            nlu_settings=nlu_settings,
            parent=parent,
            timeouts=timeouts,
            transition_route_groups=transition_route_groups,
            transition_routes=transition_routes,
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
        '''Generates CDKTF code for importing a DialogflowCxFlow resource upon running "cdktf plan ".

        :param scope: The scope in which to define this construct.
        :param import_to_id: The construct id used in the generated config for the DialogflowCxFlow to import.
        :param import_from_id: The id of the existing DialogflowCxFlow that should be imported. Refer to the {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#import import section} in the documentation of this resource for the id to use
        :param provider: ? Optional instance of the provider where the DialogflowCxFlow to import is found.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__105eab4b14fc64d76802f265d1eccee4dd95fbb5e5df56075da5c2f7c3a77b43)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument import_to_id", value=import_to_id, expected_type=type_hints["import_to_id"])
            check_type(argname="argument import_from_id", value=import_from_id, expected_type=type_hints["import_from_id"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        return typing.cast(_cdktf_9a9027ec.ImportableResource, jsii.sinvoke(cls, "generateConfigForImport", [scope, import_to_id, import_from_id, provider]))

    @jsii.member(jsii_name="putAdvancedSettings")
    def put_advanced_settings(
        self,
        *,
        audio_export_gcs_destination: typing.Optional[typing.Union["DialogflowCxFlowAdvancedSettingsAudioExportGcsDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        dtmf_settings: typing.Optional[typing.Union["DialogflowCxFlowAdvancedSettingsDtmfSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        logging_settings: typing.Optional[typing.Union["DialogflowCxFlowAdvancedSettingsLoggingSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        speech_settings: typing.Optional[typing.Union["DialogflowCxFlowAdvancedSettingsSpeechSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param audio_export_gcs_destination: audio_export_gcs_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#audio_export_gcs_destination DialogflowCxFlow#audio_export_gcs_destination}
        :param dtmf_settings: dtmf_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#dtmf_settings DialogflowCxFlow#dtmf_settings}
        :param logging_settings: logging_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#logging_settings DialogflowCxFlow#logging_settings}
        :param speech_settings: speech_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#speech_settings DialogflowCxFlow#speech_settings}
        '''
        value = DialogflowCxFlowAdvancedSettings(
            audio_export_gcs_destination=audio_export_gcs_destination,
            dtmf_settings=dtmf_settings,
            logging_settings=logging_settings,
            speech_settings=speech_settings,
        )

        return typing.cast(None, jsii.invoke(self, "putAdvancedSettings", [value]))

    @jsii.member(jsii_name="putEventHandlers")
    def put_event_handlers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxFlowEventHandlers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b2d6f4b8ef64342efd63479e223269d4b954d60379aa3315bdc10447d23bd35)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putEventHandlers", [value]))

    @jsii.member(jsii_name="putNluSettings")
    def put_nlu_settings(
        self,
        *,
        classification_threshold: typing.Optional[jsii.Number] = None,
        model_training_mode: typing.Optional[builtins.str] = None,
        model_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param classification_threshold: To filter out false positive results and still get variety in matched natural language inputs for your agent, you can tune the machine learning classification threshold. If the returned score value is less than the threshold value, then a no-match event will be triggered. The score values range from 0.0 (completely uncertain) to 1.0 (completely certain). If set to 0.0, the default of 0.3 is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#classification_threshold DialogflowCxFlow#classification_threshold}
        :param model_training_mode: Indicates NLU model training mode. - MODEL_TRAINING_MODE_AUTOMATIC: NLU model training is automatically triggered when a flow gets modified. User can also manually trigger model training in this mode. - MODEL_TRAINING_MODE_MANUAL: User needs to manually trigger NLU model training. Best for large flows whose models take long time to train. Possible values: ["MODEL_TRAINING_MODE_AUTOMATIC", "MODEL_TRAINING_MODE_MANUAL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#model_training_mode DialogflowCxFlow#model_training_mode}
        :param model_type: Indicates the type of NLU model. - MODEL_TYPE_STANDARD: Use standard NLU model. - MODEL_TYPE_ADVANCED: Use advanced NLU model. Possible values: ["MODEL_TYPE_STANDARD", "MODEL_TYPE_ADVANCED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#model_type DialogflowCxFlow#model_type}
        '''
        value = DialogflowCxFlowNluSettings(
            classification_threshold=classification_threshold,
            model_training_mode=model_training_mode,
            model_type=model_type,
        )

        return typing.cast(None, jsii.invoke(self, "putNluSettings", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#create DialogflowCxFlow#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#delete DialogflowCxFlow#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#update DialogflowCxFlow#update}.
        '''
        value = DialogflowCxFlowTimeouts(create=create, delete=delete, update=update)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="putTransitionRoutes")
    def put_transition_routes(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxFlowTransitionRoutes", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f440bd7c61584c308c6c0a0c99593338d01255c987529c5d0272b95298a7e6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTransitionRoutes", [value]))

    @jsii.member(jsii_name="resetAdvancedSettings")
    def reset_advanced_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAdvancedSettings", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEventHandlers")
    def reset_event_handlers(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventHandlers", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIsDefaultStartFlow")
    def reset_is_default_start_flow(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIsDefaultStartFlow", []))

    @jsii.member(jsii_name="resetLanguageCode")
    def reset_language_code(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLanguageCode", []))

    @jsii.member(jsii_name="resetNluSettings")
    def reset_nlu_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNluSettings", []))

    @jsii.member(jsii_name="resetParent")
    def reset_parent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParent", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTransitionRouteGroups")
    def reset_transition_route_groups(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransitionRouteGroups", []))

    @jsii.member(jsii_name="resetTransitionRoutes")
    def reset_transition_routes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTransitionRoutes", []))

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
    @jsii.member(jsii_name="advancedSettings")
    def advanced_settings(self) -> "DialogflowCxFlowAdvancedSettingsOutputReference":
        return typing.cast("DialogflowCxFlowAdvancedSettingsOutputReference", jsii.get(self, "advancedSettings"))

    @builtins.property
    @jsii.member(jsii_name="eventHandlers")
    def event_handlers(self) -> "DialogflowCxFlowEventHandlersList":
        return typing.cast("DialogflowCxFlowEventHandlersList", jsii.get(self, "eventHandlers"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="nluSettings")
    def nlu_settings(self) -> "DialogflowCxFlowNluSettingsOutputReference":
        return typing.cast("DialogflowCxFlowNluSettingsOutputReference", jsii.get(self, "nluSettings"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "DialogflowCxFlowTimeoutsOutputReference":
        return typing.cast("DialogflowCxFlowTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="transitionRoutes")
    def transition_routes(self) -> "DialogflowCxFlowTransitionRoutesList":
        return typing.cast("DialogflowCxFlowTransitionRoutesList", jsii.get(self, "transitionRoutes"))

    @builtins.property
    @jsii.member(jsii_name="advancedSettingsInput")
    def advanced_settings_input(
        self,
    ) -> typing.Optional["DialogflowCxFlowAdvancedSettings"]:
        return typing.cast(typing.Optional["DialogflowCxFlowAdvancedSettings"], jsii.get(self, "advancedSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="displayNameInput")
    def display_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "displayNameInput"))

    @builtins.property
    @jsii.member(jsii_name="eventHandlersInput")
    def event_handlers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxFlowEventHandlers"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxFlowEventHandlers"]]], jsii.get(self, "eventHandlersInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="isDefaultStartFlowInput")
    def is_default_start_flow_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "isDefaultStartFlowInput"))

    @builtins.property
    @jsii.member(jsii_name="languageCodeInput")
    def language_code_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "languageCodeInput"))

    @builtins.property
    @jsii.member(jsii_name="nluSettingsInput")
    def nlu_settings_input(self) -> typing.Optional["DialogflowCxFlowNluSettings"]:
        return typing.cast(typing.Optional["DialogflowCxFlowNluSettings"], jsii.get(self, "nluSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="parentInput")
    def parent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parentInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DialogflowCxFlowTimeouts"]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, "DialogflowCxFlowTimeouts"]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="transitionRouteGroupsInput")
    def transition_route_groups_input(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "transitionRouteGroupsInput"))

    @builtins.property
    @jsii.member(jsii_name="transitionRoutesInput")
    def transition_routes_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxFlowTransitionRoutes"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxFlowTransitionRoutes"]]], jsii.get(self, "transitionRoutesInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__525d1f088ad579284f462c890d3748a4be131ff4f772519259c28b3a4d3aabf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f19abc058b54dda393df616ce73c27289c65f807d5d312f0760e42bce485caf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01076f612e6da6ee8f18b9e0bde62fbf9296a44f0a3329ebf4ff53ca393e4ffa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="isDefaultStartFlow")
    def is_default_start_flow(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "isDefaultStartFlow"))

    @is_default_start_flow.setter
    def is_default_start_flow(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01320d262ebc1f160629cf8be936052075f8afd7b1ae7fd48057af3152a3c993)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "isDefaultStartFlow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="languageCode")
    def language_code(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "languageCode"))

    @language_code.setter
    def language_code(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5379073eaf2e87a76c466120e1cbf87fbfd737b2da6b001ef586b29bc520cbf6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "languageCode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="parent")
    def parent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parent"))

    @parent.setter
    def parent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0181a58dd91713b849c24f7f4fda2b0a0e008a48c4013ab789945d642cad2258)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="transitionRouteGroups")
    def transition_route_groups(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "transitionRouteGroups"))

    @transition_route_groups.setter
    def transition_route_groups(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaabe2288b76fe02b5c18080b38e8b4453f0b959296809fde3759f04688ec0e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "transitionRouteGroups", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowAdvancedSettings",
    jsii_struct_bases=[],
    name_mapping={
        "audio_export_gcs_destination": "audioExportGcsDestination",
        "dtmf_settings": "dtmfSettings",
        "logging_settings": "loggingSettings",
        "speech_settings": "speechSettings",
    },
)
class DialogflowCxFlowAdvancedSettings:
    def __init__(
        self,
        *,
        audio_export_gcs_destination: typing.Optional[typing.Union["DialogflowCxFlowAdvancedSettingsAudioExportGcsDestination", typing.Dict[builtins.str, typing.Any]]] = None,
        dtmf_settings: typing.Optional[typing.Union["DialogflowCxFlowAdvancedSettingsDtmfSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        logging_settings: typing.Optional[typing.Union["DialogflowCxFlowAdvancedSettingsLoggingSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        speech_settings: typing.Optional[typing.Union["DialogflowCxFlowAdvancedSettingsSpeechSettings", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param audio_export_gcs_destination: audio_export_gcs_destination block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#audio_export_gcs_destination DialogflowCxFlow#audio_export_gcs_destination}
        :param dtmf_settings: dtmf_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#dtmf_settings DialogflowCxFlow#dtmf_settings}
        :param logging_settings: logging_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#logging_settings DialogflowCxFlow#logging_settings}
        :param speech_settings: speech_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#speech_settings DialogflowCxFlow#speech_settings}
        '''
        if isinstance(audio_export_gcs_destination, dict):
            audio_export_gcs_destination = DialogflowCxFlowAdvancedSettingsAudioExportGcsDestination(**audio_export_gcs_destination)
        if isinstance(dtmf_settings, dict):
            dtmf_settings = DialogflowCxFlowAdvancedSettingsDtmfSettings(**dtmf_settings)
        if isinstance(logging_settings, dict):
            logging_settings = DialogflowCxFlowAdvancedSettingsLoggingSettings(**logging_settings)
        if isinstance(speech_settings, dict):
            speech_settings = DialogflowCxFlowAdvancedSettingsSpeechSettings(**speech_settings)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfefb8ec518d9026c8905a4832dadaec06430a5c8d3aa5016526dc71eaddc47e)
            check_type(argname="argument audio_export_gcs_destination", value=audio_export_gcs_destination, expected_type=type_hints["audio_export_gcs_destination"])
            check_type(argname="argument dtmf_settings", value=dtmf_settings, expected_type=type_hints["dtmf_settings"])
            check_type(argname="argument logging_settings", value=logging_settings, expected_type=type_hints["logging_settings"])
            check_type(argname="argument speech_settings", value=speech_settings, expected_type=type_hints["speech_settings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if audio_export_gcs_destination is not None:
            self._values["audio_export_gcs_destination"] = audio_export_gcs_destination
        if dtmf_settings is not None:
            self._values["dtmf_settings"] = dtmf_settings
        if logging_settings is not None:
            self._values["logging_settings"] = logging_settings
        if speech_settings is not None:
            self._values["speech_settings"] = speech_settings

    @builtins.property
    def audio_export_gcs_destination(
        self,
    ) -> typing.Optional["DialogflowCxFlowAdvancedSettingsAudioExportGcsDestination"]:
        '''audio_export_gcs_destination block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#audio_export_gcs_destination DialogflowCxFlow#audio_export_gcs_destination}
        '''
        result = self._values.get("audio_export_gcs_destination")
        return typing.cast(typing.Optional["DialogflowCxFlowAdvancedSettingsAudioExportGcsDestination"], result)

    @builtins.property
    def dtmf_settings(
        self,
    ) -> typing.Optional["DialogflowCxFlowAdvancedSettingsDtmfSettings"]:
        '''dtmf_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#dtmf_settings DialogflowCxFlow#dtmf_settings}
        '''
        result = self._values.get("dtmf_settings")
        return typing.cast(typing.Optional["DialogflowCxFlowAdvancedSettingsDtmfSettings"], result)

    @builtins.property
    def logging_settings(
        self,
    ) -> typing.Optional["DialogflowCxFlowAdvancedSettingsLoggingSettings"]:
        '''logging_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#logging_settings DialogflowCxFlow#logging_settings}
        '''
        result = self._values.get("logging_settings")
        return typing.cast(typing.Optional["DialogflowCxFlowAdvancedSettingsLoggingSettings"], result)

    @builtins.property
    def speech_settings(
        self,
    ) -> typing.Optional["DialogflowCxFlowAdvancedSettingsSpeechSettings"]:
        '''speech_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#speech_settings DialogflowCxFlow#speech_settings}
        '''
        result = self._values.get("speech_settings")
        return typing.cast(typing.Optional["DialogflowCxFlowAdvancedSettingsSpeechSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxFlowAdvancedSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowAdvancedSettingsAudioExportGcsDestination",
    jsii_struct_bases=[],
    name_mapping={"uri": "uri"},
)
class DialogflowCxFlowAdvancedSettingsAudioExportGcsDestination:
    def __init__(self, *, uri: typing.Optional[builtins.str] = None) -> None:
        '''
        :param uri: The Google Cloud Storage URI for the exported objects. Whether a full object name, or just a prefix, its usage depends on the Dialogflow operation. Format: gs://bucket/object-name-or-prefix Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#uri DialogflowCxFlow#uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e29a4430913b6606df161e07647e8076057de74748be7d7f0ffaf2e71a24845)
            check_type(argname="argument uri", value=uri, expected_type=type_hints["uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if uri is not None:
            self._values["uri"] = uri

    @builtins.property
    def uri(self) -> typing.Optional[builtins.str]:
        '''The Google Cloud Storage URI for the exported objects.

        Whether a full object name, or just a prefix, its usage depends on the Dialogflow operation.
        Format: gs://bucket/object-name-or-prefix

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#uri DialogflowCxFlow#uri}
        '''
        result = self._values.get("uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxFlowAdvancedSettingsAudioExportGcsDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxFlowAdvancedSettingsAudioExportGcsDestinationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowAdvancedSettingsAudioExportGcsDestinationOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57ccb8e40b99abde8aee45a11d6815452ded2ab5f9ad1a6b2b21c3dbd3d14257)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetUri")
    def reset_uri(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUri", []))

    @builtins.property
    @jsii.member(jsii_name="uriInput")
    def uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "uriInput"))

    @builtins.property
    @jsii.member(jsii_name="uri")
    def uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "uri"))

    @uri.setter
    def uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df6d40f2b1fcfa3a1dd196b449788081e0694c9f3779cde481a1c453a52cee85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "uri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxFlowAdvancedSettingsAudioExportGcsDestination]:
        return typing.cast(typing.Optional[DialogflowCxFlowAdvancedSettingsAudioExportGcsDestination], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxFlowAdvancedSettingsAudioExportGcsDestination],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8aaf8ee94304476848778879268b62fb8fd019b09cd22f9099f39ca1c77edc0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowAdvancedSettingsDtmfSettings",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "finish_digit": "finishDigit",
        "max_digits": "maxDigits",
    },
)
class DialogflowCxFlowAdvancedSettingsDtmfSettings:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        finish_digit: typing.Optional[builtins.str] = None,
        max_digits: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: If true, incoming audio is processed for DTMF (dual tone multi frequency) events. For example, if the caller presses a button on their telephone keypad and DTMF processing is enabled, Dialogflow will detect the event (e.g. a "3" was pressed) in the incoming audio and pass the event to the bot to drive business logic (e.g. when 3 is pressed, return the account balance). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#enabled DialogflowCxFlow#enabled}
        :param finish_digit: The digit that terminates a DTMF digit sequence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#finish_digit DialogflowCxFlow#finish_digit}
        :param max_digits: Max length of DTMF digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#max_digits DialogflowCxFlow#max_digits}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a00d02b7c456dd8806f50fc0d5ddaa2074ed8a2ec5cb425b475665c291d697b)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument finish_digit", value=finish_digit, expected_type=type_hints["finish_digit"])
            check_type(argname="argument max_digits", value=max_digits, expected_type=type_hints["max_digits"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if finish_digit is not None:
            self._values["finish_digit"] = finish_digit
        if max_digits is not None:
            self._values["max_digits"] = max_digits

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''If true, incoming audio is processed for DTMF (dual tone multi frequency) events.

        For example, if the caller presses a button on their telephone keypad and DTMF processing is enabled, Dialogflow will detect the event (e.g. a "3" was pressed) in the incoming audio and pass the event to the bot to drive business logic (e.g. when 3 is pressed, return the account balance).

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#enabled DialogflowCxFlow#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def finish_digit(self) -> typing.Optional[builtins.str]:
        '''The digit that terminates a DTMF digit sequence.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#finish_digit DialogflowCxFlow#finish_digit}
        '''
        result = self._values.get("finish_digit")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def max_digits(self) -> typing.Optional[jsii.Number]:
        '''Max length of DTMF digits.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#max_digits DialogflowCxFlow#max_digits}
        '''
        result = self._values.get("max_digits")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxFlowAdvancedSettingsDtmfSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxFlowAdvancedSettingsDtmfSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowAdvancedSettingsDtmfSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__462254d3a984c27bb0ddf3e10b53f20939a5b509c4d1f770a4ff44730b58bf03)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetFinishDigit")
    def reset_finish_digit(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFinishDigit", []))

    @jsii.member(jsii_name="resetMaxDigits")
    def reset_max_digits(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMaxDigits", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="finishDigitInput")
    def finish_digit_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "finishDigitInput"))

    @builtins.property
    @jsii.member(jsii_name="maxDigitsInput")
    def max_digits_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxDigitsInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__680d6897703a4dd204a21b8e5a16a6cb889f1a11e2337cb773cc4687f5994dd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="finishDigit")
    def finish_digit(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "finishDigit"))

    @finish_digit.setter
    def finish_digit(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52b734b42a24330a3bc824a76c3ec08aeafdecfa200937fe3bdde1a4dcb847d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "finishDigit", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="maxDigits")
    def max_digits(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "maxDigits"))

    @max_digits.setter
    def max_digits(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63a0e47fe9116524ba93270f6f8ca878a9a676b76aacc14771ce1d02dc30cc95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxDigits", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxFlowAdvancedSettingsDtmfSettings]:
        return typing.cast(typing.Optional[DialogflowCxFlowAdvancedSettingsDtmfSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxFlowAdvancedSettingsDtmfSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6abf0f48df59f456c6c6dc8d9eb990cd90072e4813fb8eb81fd38882758258a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowAdvancedSettingsLoggingSettings",
    jsii_struct_bases=[],
    name_mapping={
        "enable_consent_based_redaction": "enableConsentBasedRedaction",
        "enable_interaction_logging": "enableInteractionLogging",
        "enable_stackdriver_logging": "enableStackdriverLogging",
    },
)
class DialogflowCxFlowAdvancedSettingsLoggingSettings:
    def __init__(
        self,
        *,
        enable_consent_based_redaction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_interaction_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_consent_based_redaction: Enables consent-based end-user input redaction, if true, a pre-defined session parameter **$session.params.conversation-redaction** will be used to determine if the utterance should be redacted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#enable_consent_based_redaction DialogflowCxFlow#enable_consent_based_redaction}
        :param enable_interaction_logging: Enables DF Interaction logging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#enable_interaction_logging DialogflowCxFlow#enable_interaction_logging}
        :param enable_stackdriver_logging: Enables Google Cloud Logging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#enable_stackdriver_logging DialogflowCxFlow#enable_stackdriver_logging}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11b3b6c253d323bfaf741b86cad4081b2770e88537c935997101bb2f508cf510)
            check_type(argname="argument enable_consent_based_redaction", value=enable_consent_based_redaction, expected_type=type_hints["enable_consent_based_redaction"])
            check_type(argname="argument enable_interaction_logging", value=enable_interaction_logging, expected_type=type_hints["enable_interaction_logging"])
            check_type(argname="argument enable_stackdriver_logging", value=enable_stackdriver_logging, expected_type=type_hints["enable_stackdriver_logging"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enable_consent_based_redaction is not None:
            self._values["enable_consent_based_redaction"] = enable_consent_based_redaction
        if enable_interaction_logging is not None:
            self._values["enable_interaction_logging"] = enable_interaction_logging
        if enable_stackdriver_logging is not None:
            self._values["enable_stackdriver_logging"] = enable_stackdriver_logging

    @builtins.property
    def enable_consent_based_redaction(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables consent-based end-user input redaction, if true, a pre-defined session parameter **$session.params.conversation-redaction** will be used to determine if the utterance should be redacted.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#enable_consent_based_redaction DialogflowCxFlow#enable_consent_based_redaction}
        '''
        result = self._values.get("enable_consent_based_redaction")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_interaction_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables DF Interaction logging.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#enable_interaction_logging DialogflowCxFlow#enable_interaction_logging}
        '''
        result = self._values.get("enable_interaction_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def enable_stackdriver_logging(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Enables Google Cloud Logging.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#enable_stackdriver_logging DialogflowCxFlow#enable_stackdriver_logging}
        '''
        result = self._values.get("enable_stackdriver_logging")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxFlowAdvancedSettingsLoggingSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxFlowAdvancedSettingsLoggingSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowAdvancedSettingsLoggingSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__909c323b36405d0486bbe0b2a9e46aa03db93b0626ea77a97a19691f12937caa)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnableConsentBasedRedaction")
    def reset_enable_consent_based_redaction(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableConsentBasedRedaction", []))

    @jsii.member(jsii_name="resetEnableInteractionLogging")
    def reset_enable_interaction_logging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableInteractionLogging", []))

    @jsii.member(jsii_name="resetEnableStackdriverLogging")
    def reset_enable_stackdriver_logging(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnableStackdriverLogging", []))

    @builtins.property
    @jsii.member(jsii_name="enableConsentBasedRedactionInput")
    def enable_consent_based_redaction_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableConsentBasedRedactionInput"))

    @builtins.property
    @jsii.member(jsii_name="enableInteractionLoggingInput")
    def enable_interaction_logging_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableInteractionLoggingInput"))

    @builtins.property
    @jsii.member(jsii_name="enableStackdriverLoggingInput")
    def enable_stackdriver_logging_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enableStackdriverLoggingInput"))

    @builtins.property
    @jsii.member(jsii_name="enableConsentBasedRedaction")
    def enable_consent_based_redaction(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableConsentBasedRedaction"))

    @enable_consent_based_redaction.setter
    def enable_consent_based_redaction(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c1134d42da8588f5b85d559510a6f88fd80914c9d28ae7291dfb9ca4263fe66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableConsentBasedRedaction", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableInteractionLogging")
    def enable_interaction_logging(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableInteractionLogging"))

    @enable_interaction_logging.setter
    def enable_interaction_logging(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bca5f3a4cbc6e055c641a0cb7a51f80d3f60a65cd21ce7aa78cdb90330d412d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableInteractionLogging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="enableStackdriverLogging")
    def enable_stackdriver_logging(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enableStackdriverLogging"))

    @enable_stackdriver_logging.setter
    def enable_stackdriver_logging(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88dcdaabb70ceb6a4171ac9b5b22389fbd6e40797b229a3efe015c093a447318)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableStackdriverLogging", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxFlowAdvancedSettingsLoggingSettings]:
        return typing.cast(typing.Optional[DialogflowCxFlowAdvancedSettingsLoggingSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxFlowAdvancedSettingsLoggingSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99419c1994a7ef6965385928a79e1c8bacdec4189b89e5ded3e54e6d0620b11d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxFlowAdvancedSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowAdvancedSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e8f6c50247c13b454a3a778c246bc91bc3ab8d8a46a4fd205eba2dfe5c54f54e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAudioExportGcsDestination")
    def put_audio_export_gcs_destination(
        self,
        *,
        uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param uri: The Google Cloud Storage URI for the exported objects. Whether a full object name, or just a prefix, its usage depends on the Dialogflow operation. Format: gs://bucket/object-name-or-prefix Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#uri DialogflowCxFlow#uri}
        '''
        value = DialogflowCxFlowAdvancedSettingsAudioExportGcsDestination(uri=uri)

        return typing.cast(None, jsii.invoke(self, "putAudioExportGcsDestination", [value]))

    @jsii.member(jsii_name="putDtmfSettings")
    def put_dtmf_settings(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        finish_digit: typing.Optional[builtins.str] = None,
        max_digits: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: If true, incoming audio is processed for DTMF (dual tone multi frequency) events. For example, if the caller presses a button on their telephone keypad and DTMF processing is enabled, Dialogflow will detect the event (e.g. a "3" was pressed) in the incoming audio and pass the event to the bot to drive business logic (e.g. when 3 is pressed, return the account balance). Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#enabled DialogflowCxFlow#enabled}
        :param finish_digit: The digit that terminates a DTMF digit sequence. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#finish_digit DialogflowCxFlow#finish_digit}
        :param max_digits: Max length of DTMF digits. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#max_digits DialogflowCxFlow#max_digits}
        '''
        value = DialogflowCxFlowAdvancedSettingsDtmfSettings(
            enabled=enabled, finish_digit=finish_digit, max_digits=max_digits
        )

        return typing.cast(None, jsii.invoke(self, "putDtmfSettings", [value]))

    @jsii.member(jsii_name="putLoggingSettings")
    def put_logging_settings(
        self,
        *,
        enable_consent_based_redaction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_interaction_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enable_consent_based_redaction: Enables consent-based end-user input redaction, if true, a pre-defined session parameter **$session.params.conversation-redaction** will be used to determine if the utterance should be redacted. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#enable_consent_based_redaction DialogflowCxFlow#enable_consent_based_redaction}
        :param enable_interaction_logging: Enables DF Interaction logging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#enable_interaction_logging DialogflowCxFlow#enable_interaction_logging}
        :param enable_stackdriver_logging: Enables Google Cloud Logging. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#enable_stackdriver_logging DialogflowCxFlow#enable_stackdriver_logging}
        '''
        value = DialogflowCxFlowAdvancedSettingsLoggingSettings(
            enable_consent_based_redaction=enable_consent_based_redaction,
            enable_interaction_logging=enable_interaction_logging,
            enable_stackdriver_logging=enable_stackdriver_logging,
        )

        return typing.cast(None, jsii.invoke(self, "putLoggingSettings", [value]))

    @jsii.member(jsii_name="putSpeechSettings")
    def put_speech_settings(
        self,
        *,
        endpointer_sensitivity: typing.Optional[jsii.Number] = None,
        models: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        no_speech_timeout: typing.Optional[builtins.str] = None,
        use_timeout_based_endpointing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param endpointer_sensitivity: Sensitivity of the speech model that detects the end of speech. Scale from 0 to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#endpointer_sensitivity DialogflowCxFlow#endpointer_sensitivity}
        :param models: Mapping from language to Speech-to-Text model. The mapped Speech-to-Text model will be selected for requests from its corresponding language. For more information, see `Speech models <https://cloud.google.com/dialogflow/cx/docs/concept/speech-models>`_. An object containing a list of **"key": value** pairs. Example: **{ "name": "wrench", "mass": "1.3kg", "count": "3" }**. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#models DialogflowCxFlow#models}
        :param no_speech_timeout: Timeout before detecting no speech. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#no_speech_timeout DialogflowCxFlow#no_speech_timeout}
        :param use_timeout_based_endpointing: Use timeout based endpointing, interpreting endpointer sensitivity as seconds of timeout value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#use_timeout_based_endpointing DialogflowCxFlow#use_timeout_based_endpointing}
        '''
        value = DialogflowCxFlowAdvancedSettingsSpeechSettings(
            endpointer_sensitivity=endpointer_sensitivity,
            models=models,
            no_speech_timeout=no_speech_timeout,
            use_timeout_based_endpointing=use_timeout_based_endpointing,
        )

        return typing.cast(None, jsii.invoke(self, "putSpeechSettings", [value]))

    @jsii.member(jsii_name="resetAudioExportGcsDestination")
    def reset_audio_export_gcs_destination(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAudioExportGcsDestination", []))

    @jsii.member(jsii_name="resetDtmfSettings")
    def reset_dtmf_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDtmfSettings", []))

    @jsii.member(jsii_name="resetLoggingSettings")
    def reset_logging_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLoggingSettings", []))

    @jsii.member(jsii_name="resetSpeechSettings")
    def reset_speech_settings(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSpeechSettings", []))

    @builtins.property
    @jsii.member(jsii_name="audioExportGcsDestination")
    def audio_export_gcs_destination(
        self,
    ) -> DialogflowCxFlowAdvancedSettingsAudioExportGcsDestinationOutputReference:
        return typing.cast(DialogflowCxFlowAdvancedSettingsAudioExportGcsDestinationOutputReference, jsii.get(self, "audioExportGcsDestination"))

    @builtins.property
    @jsii.member(jsii_name="dtmfSettings")
    def dtmf_settings(
        self,
    ) -> DialogflowCxFlowAdvancedSettingsDtmfSettingsOutputReference:
        return typing.cast(DialogflowCxFlowAdvancedSettingsDtmfSettingsOutputReference, jsii.get(self, "dtmfSettings"))

    @builtins.property
    @jsii.member(jsii_name="loggingSettings")
    def logging_settings(
        self,
    ) -> DialogflowCxFlowAdvancedSettingsLoggingSettingsOutputReference:
        return typing.cast(DialogflowCxFlowAdvancedSettingsLoggingSettingsOutputReference, jsii.get(self, "loggingSettings"))

    @builtins.property
    @jsii.member(jsii_name="speechSettings")
    def speech_settings(
        self,
    ) -> "DialogflowCxFlowAdvancedSettingsSpeechSettingsOutputReference":
        return typing.cast("DialogflowCxFlowAdvancedSettingsSpeechSettingsOutputReference", jsii.get(self, "speechSettings"))

    @builtins.property
    @jsii.member(jsii_name="audioExportGcsDestinationInput")
    def audio_export_gcs_destination_input(
        self,
    ) -> typing.Optional[DialogflowCxFlowAdvancedSettingsAudioExportGcsDestination]:
        return typing.cast(typing.Optional[DialogflowCxFlowAdvancedSettingsAudioExportGcsDestination], jsii.get(self, "audioExportGcsDestinationInput"))

    @builtins.property
    @jsii.member(jsii_name="dtmfSettingsInput")
    def dtmf_settings_input(
        self,
    ) -> typing.Optional[DialogflowCxFlowAdvancedSettingsDtmfSettings]:
        return typing.cast(typing.Optional[DialogflowCxFlowAdvancedSettingsDtmfSettings], jsii.get(self, "dtmfSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="loggingSettingsInput")
    def logging_settings_input(
        self,
    ) -> typing.Optional[DialogflowCxFlowAdvancedSettingsLoggingSettings]:
        return typing.cast(typing.Optional[DialogflowCxFlowAdvancedSettingsLoggingSettings], jsii.get(self, "loggingSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="speechSettingsInput")
    def speech_settings_input(
        self,
    ) -> typing.Optional["DialogflowCxFlowAdvancedSettingsSpeechSettings"]:
        return typing.cast(typing.Optional["DialogflowCxFlowAdvancedSettingsSpeechSettings"], jsii.get(self, "speechSettingsInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DialogflowCxFlowAdvancedSettings]:
        return typing.cast(typing.Optional[DialogflowCxFlowAdvancedSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxFlowAdvancedSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9bd58252b666f55f41d019b8966c0f66468eb934c556ae719d82c08ec33bf0e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowAdvancedSettingsSpeechSettings",
    jsii_struct_bases=[],
    name_mapping={
        "endpointer_sensitivity": "endpointerSensitivity",
        "models": "models",
        "no_speech_timeout": "noSpeechTimeout",
        "use_timeout_based_endpointing": "useTimeoutBasedEndpointing",
    },
)
class DialogflowCxFlowAdvancedSettingsSpeechSettings:
    def __init__(
        self,
        *,
        endpointer_sensitivity: typing.Optional[jsii.Number] = None,
        models: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        no_speech_timeout: typing.Optional[builtins.str] = None,
        use_timeout_based_endpointing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param endpointer_sensitivity: Sensitivity of the speech model that detects the end of speech. Scale from 0 to 100. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#endpointer_sensitivity DialogflowCxFlow#endpointer_sensitivity}
        :param models: Mapping from language to Speech-to-Text model. The mapped Speech-to-Text model will be selected for requests from its corresponding language. For more information, see `Speech models <https://cloud.google.com/dialogflow/cx/docs/concept/speech-models>`_. An object containing a list of **"key": value** pairs. Example: **{ "name": "wrench", "mass": "1.3kg", "count": "3" }**. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#models DialogflowCxFlow#models}
        :param no_speech_timeout: Timeout before detecting no speech. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s". Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#no_speech_timeout DialogflowCxFlow#no_speech_timeout}
        :param use_timeout_based_endpointing: Use timeout based endpointing, interpreting endpointer sensitivity as seconds of timeout value. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#use_timeout_based_endpointing DialogflowCxFlow#use_timeout_based_endpointing}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c370fa592bc682b70446b182d3fea98301a3699655bbf1fc2a5ffa750052e76c)
            check_type(argname="argument endpointer_sensitivity", value=endpointer_sensitivity, expected_type=type_hints["endpointer_sensitivity"])
            check_type(argname="argument models", value=models, expected_type=type_hints["models"])
            check_type(argname="argument no_speech_timeout", value=no_speech_timeout, expected_type=type_hints["no_speech_timeout"])
            check_type(argname="argument use_timeout_based_endpointing", value=use_timeout_based_endpointing, expected_type=type_hints["use_timeout_based_endpointing"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if endpointer_sensitivity is not None:
            self._values["endpointer_sensitivity"] = endpointer_sensitivity
        if models is not None:
            self._values["models"] = models
        if no_speech_timeout is not None:
            self._values["no_speech_timeout"] = no_speech_timeout
        if use_timeout_based_endpointing is not None:
            self._values["use_timeout_based_endpointing"] = use_timeout_based_endpointing

    @builtins.property
    def endpointer_sensitivity(self) -> typing.Optional[jsii.Number]:
        '''Sensitivity of the speech model that detects the end of speech. Scale from 0 to 100.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#endpointer_sensitivity DialogflowCxFlow#endpointer_sensitivity}
        '''
        result = self._values.get("endpointer_sensitivity")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def models(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Mapping from language to Speech-to-Text model.

        The mapped Speech-to-Text model will be selected for requests from its corresponding language. For more information, see `Speech models <https://cloud.google.com/dialogflow/cx/docs/concept/speech-models>`_.
        An object containing a list of **"key": value** pairs. Example: **{ "name": "wrench", "mass": "1.3kg", "count": "3" }**.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#models DialogflowCxFlow#models}
        '''
        result = self._values.get("models")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def no_speech_timeout(self) -> typing.Optional[builtins.str]:
        '''Timeout before detecting no speech. A duration in seconds with up to nine fractional digits, ending with 's'. Example: "3.5s".

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#no_speech_timeout DialogflowCxFlow#no_speech_timeout}
        '''
        result = self._values.get("no_speech_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_timeout_based_endpointing(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Use timeout based endpointing, interpreting endpointer sensitivity as seconds of timeout value.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#use_timeout_based_endpointing DialogflowCxFlow#use_timeout_based_endpointing}
        '''
        result = self._values.get("use_timeout_based_endpointing")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxFlowAdvancedSettingsSpeechSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxFlowAdvancedSettingsSpeechSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowAdvancedSettingsSpeechSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__243fc480c5151a77c0ba714f54f731557a5e1bf5d6c5e6d6b9c5e09d1f64d752)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEndpointerSensitivity")
    def reset_endpointer_sensitivity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEndpointerSensitivity", []))

    @jsii.member(jsii_name="resetModels")
    def reset_models(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModels", []))

    @jsii.member(jsii_name="resetNoSpeechTimeout")
    def reset_no_speech_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoSpeechTimeout", []))

    @jsii.member(jsii_name="resetUseTimeoutBasedEndpointing")
    def reset_use_timeout_based_endpointing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUseTimeoutBasedEndpointing", []))

    @builtins.property
    @jsii.member(jsii_name="endpointerSensitivityInput")
    def endpointer_sensitivity_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "endpointerSensitivityInput"))

    @builtins.property
    @jsii.member(jsii_name="modelsInput")
    def models_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "modelsInput"))

    @builtins.property
    @jsii.member(jsii_name="noSpeechTimeoutInput")
    def no_speech_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "noSpeechTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="useTimeoutBasedEndpointingInput")
    def use_timeout_based_endpointing_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "useTimeoutBasedEndpointingInput"))

    @builtins.property
    @jsii.member(jsii_name="endpointerSensitivity")
    def endpointer_sensitivity(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "endpointerSensitivity"))

    @endpointer_sensitivity.setter
    def endpointer_sensitivity(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff432305f4fd6da431967093625d49f7ac63584449a22bf609f652bdaac55130)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointerSensitivity", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="models")
    def models(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "models"))

    @models.setter
    def models(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a647b7599ba415029519e1c57ff23908cba39706dcacfc6ad02e27c3a14965f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "models", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="noSpeechTimeout")
    def no_speech_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "noSpeechTimeout"))

    @no_speech_timeout.setter
    def no_speech_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b99781623e16c3999aa375ab1e41aa38c883ac750fa8c1c019e2470cf2e892a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noSpeechTimeout", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="useTimeoutBasedEndpointing")
    def use_timeout_based_endpointing(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "useTimeoutBasedEndpointing"))

    @use_timeout_based_endpointing.setter
    def use_timeout_based_endpointing(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee9666a1838f01e171df77ee5f84135bdba16283a09ea74fc0d350dad848099b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "useTimeoutBasedEndpointing", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxFlowAdvancedSettingsSpeechSettings]:
        return typing.cast(typing.Optional[DialogflowCxFlowAdvancedSettingsSpeechSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxFlowAdvancedSettingsSpeechSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be9e0218babb2169372482a009a54202579bbe50e0b16f823b2c983848e93236)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowConfig",
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
        "advanced_settings": "advancedSettings",
        "description": "description",
        "event_handlers": "eventHandlers",
        "id": "id",
        "is_default_start_flow": "isDefaultStartFlow",
        "language_code": "languageCode",
        "nlu_settings": "nluSettings",
        "parent": "parent",
        "timeouts": "timeouts",
        "transition_route_groups": "transitionRouteGroups",
        "transition_routes": "transitionRoutes",
    },
)
class DialogflowCxFlowConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        advanced_settings: typing.Optional[typing.Union[DialogflowCxFlowAdvancedSettings, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        event_handlers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxFlowEventHandlers", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        is_default_start_flow: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        language_code: typing.Optional[builtins.str] = None,
        nlu_settings: typing.Optional[typing.Union["DialogflowCxFlowNluSettings", typing.Dict[builtins.str, typing.Any]]] = None,
        parent: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["DialogflowCxFlowTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        transition_route_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        transition_routes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxFlowTransitionRoutes", typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param display_name: The human-readable name of the flow. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#display_name DialogflowCxFlow#display_name}
        :param advanced_settings: advanced_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#advanced_settings DialogflowCxFlow#advanced_settings}
        :param description: The description of the flow. The maximum length is 500 characters. If exceeded, the request is rejected. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#description DialogflowCxFlow#description}
        :param event_handlers: event_handlers block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#event_handlers DialogflowCxFlow#event_handlers}
        :param id: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#id DialogflowCxFlow#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param is_default_start_flow: Marks this as the `Default Start Flow <https://cloud.google.com/dialogflow/cx/docs/concept/flow#start>`_ for an agent. When you create an agent, the Default Start Flow is created automatically. The Default Start Flow cannot be deleted; deleting the 'google_dialogflow_cx_flow' resource does nothing to the underlying GCP resources. ~> Avoid having multiple 'google_dialogflow_cx_flow' resources linked to the same agent with 'is_default_start_flow = true' because they will compete to control a single Default Start Flow resource in GCP. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#is_default_start_flow DialogflowCxFlow#is_default_start_flow}
        :param language_code: The language of the following fields in flow: Flow.event_handlers.trigger_fulfillment.messages Flow.event_handlers.trigger_fulfillment.conditional_cases Flow.transition_routes.trigger_fulfillment.messages Flow.transition_routes.trigger_fulfillment.conditional_cases If not specified, the agent's default language is used. Many languages are supported. Note: languages must be enabled in the agent before they can be used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#language_code DialogflowCxFlow#language_code}
        :param nlu_settings: nlu_settings block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#nlu_settings DialogflowCxFlow#nlu_settings}
        :param parent: The agent to create a flow for. Format: projects//locations//agents/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#parent DialogflowCxFlow#parent}
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#timeouts DialogflowCxFlow#timeouts}
        :param transition_route_groups: A flow's transition route group serve two purposes: They are responsible for matching the user's first utterances in the flow. They are inherited by every page's [transition route groups][Page.transition_route_groups]. Transition route groups defined in the page have higher priority than those defined in the flow. Format:projects//locations//agents//flows//transitionRouteGroups/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#transition_route_groups DialogflowCxFlow#transition_route_groups}
        :param transition_routes: transition_routes block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#transition_routes DialogflowCxFlow#transition_routes}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(advanced_settings, dict):
            advanced_settings = DialogflowCxFlowAdvancedSettings(**advanced_settings)
        if isinstance(nlu_settings, dict):
            nlu_settings = DialogflowCxFlowNluSettings(**nlu_settings)
        if isinstance(timeouts, dict):
            timeouts = DialogflowCxFlowTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec698bcfeadd51979d5f29ea8d4a0a592a61a165e38fb999ad729592839dee47)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument advanced_settings", value=advanced_settings, expected_type=type_hints["advanced_settings"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument event_handlers", value=event_handlers, expected_type=type_hints["event_handlers"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument is_default_start_flow", value=is_default_start_flow, expected_type=type_hints["is_default_start_flow"])
            check_type(argname="argument language_code", value=language_code, expected_type=type_hints["language_code"])
            check_type(argname="argument nlu_settings", value=nlu_settings, expected_type=type_hints["nlu_settings"])
            check_type(argname="argument parent", value=parent, expected_type=type_hints["parent"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument transition_route_groups", value=transition_route_groups, expected_type=type_hints["transition_route_groups"])
            check_type(argname="argument transition_routes", value=transition_routes, expected_type=type_hints["transition_routes"])
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
        if advanced_settings is not None:
            self._values["advanced_settings"] = advanced_settings
        if description is not None:
            self._values["description"] = description
        if event_handlers is not None:
            self._values["event_handlers"] = event_handlers
        if id is not None:
            self._values["id"] = id
        if is_default_start_flow is not None:
            self._values["is_default_start_flow"] = is_default_start_flow
        if language_code is not None:
            self._values["language_code"] = language_code
        if nlu_settings is not None:
            self._values["nlu_settings"] = nlu_settings
        if parent is not None:
            self._values["parent"] = parent
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if transition_route_groups is not None:
            self._values["transition_route_groups"] = transition_route_groups
        if transition_routes is not None:
            self._values["transition_routes"] = transition_routes

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
        '''The human-readable name of the flow.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#display_name DialogflowCxFlow#display_name}
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def advanced_settings(self) -> typing.Optional[DialogflowCxFlowAdvancedSettings]:
        '''advanced_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#advanced_settings DialogflowCxFlow#advanced_settings}
        '''
        result = self._values.get("advanced_settings")
        return typing.cast(typing.Optional[DialogflowCxFlowAdvancedSettings], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the flow. The maximum length is 500 characters. If exceeded, the request is rejected.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#description DialogflowCxFlow#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_handlers(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxFlowEventHandlers"]]]:
        '''event_handlers block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#event_handlers DialogflowCxFlow#event_handlers}
        '''
        result = self._values.get("event_handlers")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxFlowEventHandlers"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#id DialogflowCxFlow#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def is_default_start_flow(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Marks this as the `Default Start Flow <https://cloud.google.com/dialogflow/cx/docs/concept/flow#start>`_ for an agent. When you create an agent, the Default Start Flow is created automatically. The Default Start Flow cannot be deleted; deleting the 'google_dialogflow_cx_flow' resource does nothing to the underlying GCP resources.

        ~> Avoid having multiple 'google_dialogflow_cx_flow' resources linked to the same agent with 'is_default_start_flow = true' because they will compete to control a single Default Start Flow resource in GCP.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#is_default_start_flow DialogflowCxFlow#is_default_start_flow}
        '''
        result = self._values.get("is_default_start_flow")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def language_code(self) -> typing.Optional[builtins.str]:
        '''The language of the following fields in flow: Flow.event_handlers.trigger_fulfillment.messages Flow.event_handlers.trigger_fulfillment.conditional_cases Flow.transition_routes.trigger_fulfillment.messages Flow.transition_routes.trigger_fulfillment.conditional_cases If not specified, the agent's default language is used. Many languages are supported. Note: languages must be enabled in the agent before they can be used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#language_code DialogflowCxFlow#language_code}
        '''
        result = self._values.get("language_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def nlu_settings(self) -> typing.Optional["DialogflowCxFlowNluSettings"]:
        '''nlu_settings block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#nlu_settings DialogflowCxFlow#nlu_settings}
        '''
        result = self._values.get("nlu_settings")
        return typing.cast(typing.Optional["DialogflowCxFlowNluSettings"], result)

    @builtins.property
    def parent(self) -> typing.Optional[builtins.str]:
        '''The agent to create a flow for. Format: projects//locations//agents/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#parent DialogflowCxFlow#parent}
        '''
        result = self._values.get("parent")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["DialogflowCxFlowTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#timeouts DialogflowCxFlow#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["DialogflowCxFlowTimeouts"], result)

    @builtins.property
    def transition_route_groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A flow's transition route group serve two purposes: They are responsible for matching the user's first utterances in the flow.

        They are inherited by every page's [transition route groups][Page.transition_route_groups]. Transition route groups defined in the page have higher priority than those defined in the flow.
        Format:projects//locations//agents//flows//transitionRouteGroups/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#transition_route_groups DialogflowCxFlow#transition_route_groups}
        '''
        result = self._values.get("transition_route_groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def transition_routes(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxFlowTransitionRoutes"]]]:
        '''transition_routes block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#transition_routes DialogflowCxFlow#transition_routes}
        '''
        result = self._values.get("transition_routes")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxFlowTransitionRoutes"]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxFlowConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowEventHandlers",
    jsii_struct_bases=[],
    name_mapping={
        "event": "event",
        "target_flow": "targetFlow",
        "target_page": "targetPage",
        "trigger_fulfillment": "triggerFulfillment",
    },
)
class DialogflowCxFlowEventHandlers:
    def __init__(
        self,
        *,
        event: typing.Optional[builtins.str] = None,
        target_flow: typing.Optional[builtins.str] = None,
        target_page: typing.Optional[builtins.str] = None,
        trigger_fulfillment: typing.Optional[typing.Union["DialogflowCxFlowEventHandlersTriggerFulfillment", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param event: The name of the event to handle. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#event DialogflowCxFlow#event}
        :param target_flow: The target flow to transition to. Format: projects//locations//agents//flows/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#target_flow DialogflowCxFlow#target_flow}
        :param target_page: The target page to transition to. Format: projects//locations//agents//flows//pages/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#target_page DialogflowCxFlow#target_page}
        :param trigger_fulfillment: trigger_fulfillment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#trigger_fulfillment DialogflowCxFlow#trigger_fulfillment}
        '''
        if isinstance(trigger_fulfillment, dict):
            trigger_fulfillment = DialogflowCxFlowEventHandlersTriggerFulfillment(**trigger_fulfillment)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a8050a2a4311e47d08ea1a2ae43816ba636f82ed5e2a86798e2bd58858e0cd3)
            check_type(argname="argument event", value=event, expected_type=type_hints["event"])
            check_type(argname="argument target_flow", value=target_flow, expected_type=type_hints["target_flow"])
            check_type(argname="argument target_page", value=target_page, expected_type=type_hints["target_page"])
            check_type(argname="argument trigger_fulfillment", value=trigger_fulfillment, expected_type=type_hints["trigger_fulfillment"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if event is not None:
            self._values["event"] = event
        if target_flow is not None:
            self._values["target_flow"] = target_flow
        if target_page is not None:
            self._values["target_page"] = target_page
        if trigger_fulfillment is not None:
            self._values["trigger_fulfillment"] = trigger_fulfillment

    @builtins.property
    def event(self) -> typing.Optional[builtins.str]:
        '''The name of the event to handle.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#event DialogflowCxFlow#event}
        '''
        result = self._values.get("event")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_flow(self) -> typing.Optional[builtins.str]:
        '''The target flow to transition to. Format: projects//locations//agents//flows/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#target_flow DialogflowCxFlow#target_flow}
        '''
        result = self._values.get("target_flow")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_page(self) -> typing.Optional[builtins.str]:
        '''The target page to transition to. Format: projects//locations//agents//flows//pages/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#target_page DialogflowCxFlow#target_page}
        '''
        result = self._values.get("target_page")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def trigger_fulfillment(
        self,
    ) -> typing.Optional["DialogflowCxFlowEventHandlersTriggerFulfillment"]:
        '''trigger_fulfillment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#trigger_fulfillment DialogflowCxFlow#trigger_fulfillment}
        '''
        result = self._values.get("trigger_fulfillment")
        return typing.cast(typing.Optional["DialogflowCxFlowEventHandlersTriggerFulfillment"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxFlowEventHandlers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxFlowEventHandlersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowEventHandlersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d42939112cfa1221e46883d4e3d76965f5e69c0697aa3b7b334ccbf8426c3d6)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "DialogflowCxFlowEventHandlersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33d35a9d80a7158de74ab6372970bf0ad4e275bb5328969bd8613bcdd35d53d6)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DialogflowCxFlowEventHandlersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9091b6d2a1ca8403a193f3bf25da330278e125aead455dfc44a54a26c0c3ffc7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7f225eff77b3c9853afa47e56d66f22ce1341dcd0b3af4f26f3b64f742be265c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__df4af229d9905c8286ed08d12c2be8f1f51b392b40ae79be05c436883edd8d37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowEventHandlers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowEventHandlers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowEventHandlers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77277aa21281d85989754af45b5d8cb1a5a687b38bb312a2c8bbeceb17ba384b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxFlowEventHandlersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowEventHandlersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__86cb70ea9c34dc73d0d371cd77b5f7efbbe67fc7ff01c6f78ff555b32540cf55)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putTriggerFulfillment")
    def put_trigger_fulfillment(
        self,
        *,
        conditional_cases: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases", typing.Dict[builtins.str, typing.Any]]]]] = None,
        messages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxFlowEventHandlersTriggerFulfillmentMessages", typing.Dict[builtins.str, typing.Any]]]]] = None,
        return_partial_responses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        set_parameter_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tag: typing.Optional[builtins.str] = None,
        webhook: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param conditional_cases: conditional_cases block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#conditional_cases DialogflowCxFlow#conditional_cases}
        :param messages: messages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#messages DialogflowCxFlow#messages}
        :param return_partial_responses: Whether Dialogflow should return currently queued fulfillment response messages in streaming APIs. If a webhook is specified, it happens before Dialogflow invokes webhook. Warning: 1) This flag only affects streaming API. Responses are still queued and returned once in non-streaming API. 2) The flag can be enabled in any fulfillment but only the first 3 partial responses will be returned. You may only want to apply it to fulfillments that have slow webhooks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#return_partial_responses DialogflowCxFlow#return_partial_responses}
        :param set_parameter_actions: set_parameter_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#set_parameter_actions DialogflowCxFlow#set_parameter_actions}
        :param tag: The tag used by the webhook to identify which fulfillment is being called. This field is required if webhook is specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#tag DialogflowCxFlow#tag}
        :param webhook: The webhook to call. Format: projects//locations//agents//webhooks/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#webhook DialogflowCxFlow#webhook}
        '''
        value = DialogflowCxFlowEventHandlersTriggerFulfillment(
            conditional_cases=conditional_cases,
            messages=messages,
            return_partial_responses=return_partial_responses,
            set_parameter_actions=set_parameter_actions,
            tag=tag,
            webhook=webhook,
        )

        return typing.cast(None, jsii.invoke(self, "putTriggerFulfillment", [value]))

    @jsii.member(jsii_name="resetEvent")
    def reset_event(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEvent", []))

    @jsii.member(jsii_name="resetTargetFlow")
    def reset_target_flow(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetFlow", []))

    @jsii.member(jsii_name="resetTargetPage")
    def reset_target_page(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetPage", []))

    @jsii.member(jsii_name="resetTriggerFulfillment")
    def reset_trigger_fulfillment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTriggerFulfillment", []))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="triggerFulfillment")
    def trigger_fulfillment(
        self,
    ) -> "DialogflowCxFlowEventHandlersTriggerFulfillmentOutputReference":
        return typing.cast("DialogflowCxFlowEventHandlersTriggerFulfillmentOutputReference", jsii.get(self, "triggerFulfillment"))

    @builtins.property
    @jsii.member(jsii_name="eventInput")
    def event_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventInput"))

    @builtins.property
    @jsii.member(jsii_name="targetFlowInput")
    def target_flow_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetFlowInput"))

    @builtins.property
    @jsii.member(jsii_name="targetPageInput")
    def target_page_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetPageInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerFulfillmentInput")
    def trigger_fulfillment_input(
        self,
    ) -> typing.Optional["DialogflowCxFlowEventHandlersTriggerFulfillment"]:
        return typing.cast(typing.Optional["DialogflowCxFlowEventHandlersTriggerFulfillment"], jsii.get(self, "triggerFulfillmentInput"))

    @builtins.property
    @jsii.member(jsii_name="event")
    def event(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "event"))

    @event.setter
    def event(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9c20abfac43e96fad5fbc962ef06fbe421b92453ca8b90f23cbb42a71b354c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "event", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetFlow")
    def target_flow(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetFlow"))

    @target_flow.setter
    def target_flow(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33a50c3ba767c788f6efb6617b4b26e680c7a4d29b5bbf39a077787cbff07401)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetFlow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetPage")
    def target_page(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetPage"))

    @target_page.setter
    def target_page(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12d1230ef8f1746d438bfd6ef148f37a451c3051a77d69b611c748d50ac6a189)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetPage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowEventHandlers]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowEventHandlers]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowEventHandlers]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50b90352ac28a01bd24bf21bdd41104d2bbebdabad24d76edb66cfac726ddf1a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowEventHandlersTriggerFulfillment",
    jsii_struct_bases=[],
    name_mapping={
        "conditional_cases": "conditionalCases",
        "messages": "messages",
        "return_partial_responses": "returnPartialResponses",
        "set_parameter_actions": "setParameterActions",
        "tag": "tag",
        "webhook": "webhook",
    },
)
class DialogflowCxFlowEventHandlersTriggerFulfillment:
    def __init__(
        self,
        *,
        conditional_cases: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases", typing.Dict[builtins.str, typing.Any]]]]] = None,
        messages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxFlowEventHandlersTriggerFulfillmentMessages", typing.Dict[builtins.str, typing.Any]]]]] = None,
        return_partial_responses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        set_parameter_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tag: typing.Optional[builtins.str] = None,
        webhook: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param conditional_cases: conditional_cases block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#conditional_cases DialogflowCxFlow#conditional_cases}
        :param messages: messages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#messages DialogflowCxFlow#messages}
        :param return_partial_responses: Whether Dialogflow should return currently queued fulfillment response messages in streaming APIs. If a webhook is specified, it happens before Dialogflow invokes webhook. Warning: 1) This flag only affects streaming API. Responses are still queued and returned once in non-streaming API. 2) The flag can be enabled in any fulfillment but only the first 3 partial responses will be returned. You may only want to apply it to fulfillments that have slow webhooks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#return_partial_responses DialogflowCxFlow#return_partial_responses}
        :param set_parameter_actions: set_parameter_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#set_parameter_actions DialogflowCxFlow#set_parameter_actions}
        :param tag: The tag used by the webhook to identify which fulfillment is being called. This field is required if webhook is specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#tag DialogflowCxFlow#tag}
        :param webhook: The webhook to call. Format: projects//locations//agents//webhooks/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#webhook DialogflowCxFlow#webhook}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e845933aee1763891ad709b181bd0b2a143efbaacda06a9e2b63db9eab9a903)
            check_type(argname="argument conditional_cases", value=conditional_cases, expected_type=type_hints["conditional_cases"])
            check_type(argname="argument messages", value=messages, expected_type=type_hints["messages"])
            check_type(argname="argument return_partial_responses", value=return_partial_responses, expected_type=type_hints["return_partial_responses"])
            check_type(argname="argument set_parameter_actions", value=set_parameter_actions, expected_type=type_hints["set_parameter_actions"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
            check_type(argname="argument webhook", value=webhook, expected_type=type_hints["webhook"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if conditional_cases is not None:
            self._values["conditional_cases"] = conditional_cases
        if messages is not None:
            self._values["messages"] = messages
        if return_partial_responses is not None:
            self._values["return_partial_responses"] = return_partial_responses
        if set_parameter_actions is not None:
            self._values["set_parameter_actions"] = set_parameter_actions
        if tag is not None:
            self._values["tag"] = tag
        if webhook is not None:
            self._values["webhook"] = webhook

    @builtins.property
    def conditional_cases(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases"]]]:
        '''conditional_cases block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#conditional_cases DialogflowCxFlow#conditional_cases}
        '''
        result = self._values.get("conditional_cases")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases"]]], result)

    @builtins.property
    def messages(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxFlowEventHandlersTriggerFulfillmentMessages"]]]:
        '''messages block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#messages DialogflowCxFlow#messages}
        '''
        result = self._values.get("messages")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxFlowEventHandlersTriggerFulfillmentMessages"]]], result)

    @builtins.property
    def return_partial_responses(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether Dialogflow should return currently queued fulfillment response messages in streaming APIs.

        If a webhook is specified, it happens before Dialogflow invokes webhook. Warning: 1) This flag only affects streaming API. Responses are still queued and returned once in non-streaming API. 2) The flag can be enabled in any fulfillment but only the first 3 partial responses will be returned. You may only want to apply it to fulfillments that have slow webhooks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#return_partial_responses DialogflowCxFlow#return_partial_responses}
        '''
        result = self._values.get("return_partial_responses")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def set_parameter_actions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions"]]]:
        '''set_parameter_actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#set_parameter_actions DialogflowCxFlow#set_parameter_actions}
        '''
        result = self._values.get("set_parameter_actions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions"]]], result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''The tag used by the webhook to identify which fulfillment is being called.

        This field is required if webhook is specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#tag DialogflowCxFlow#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def webhook(self) -> typing.Optional[builtins.str]:
        '''The webhook to call. Format: projects//locations//agents//webhooks/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#webhook DialogflowCxFlow#webhook}
        '''
        result = self._values.get("webhook")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxFlowEventHandlersTriggerFulfillment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases",
    jsii_struct_bases=[],
    name_mapping={"cases": "cases"},
)
class DialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases:
    def __init__(self, *, cases: typing.Optional[builtins.str] = None) -> None:
        '''
        :param cases: A JSON encoded list of cascading if-else conditions. Cases are mutually exclusive. The first one with a matching condition is selected, all the rest ignored. See `Case <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/Fulfillment#case>`_ for the schema. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#cases DialogflowCxFlow#cases}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b286635f745e721ea317207f30f8efeb0a8e4cda7ba3f3ebad98f035af3fcfb)
            check_type(argname="argument cases", value=cases, expected_type=type_hints["cases"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cases is not None:
            self._values["cases"] = cases

    @builtins.property
    def cases(self) -> typing.Optional[builtins.str]:
        '''A JSON encoded list of cascading if-else conditions.

        Cases are mutually exclusive. The first one with a matching condition is selected, all the rest ignored.
        See `Case <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/Fulfillment#case>`_ for the schema.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#cases DialogflowCxFlow#cases}
        '''
        result = self._values.get("cases")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCasesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCasesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ad2f3eb4e45a341e4cc22c6b7efbcfc2b452a308a4d075bcdbe92a821641dbe)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCasesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56ca45e914117151278f67fa9f6db512ac74e7c12bae523164211d037ac673dd)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCasesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a933841b84a1c19d0e1a71f5677c047eb87ff461ccdd57d256132d2e9e69f197)
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
            type_hints = typing.get_type_hints(_typecheckingstub__270355a735d469304e3d0af55fce009bc353f5c845b2401d52bf94dfacd7f7a8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6d5579fb18d1f1683c76726132688a0d5530cc4ae99b76f7317ec24ad40c385d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aeab8f21464d92487d7d7746cbf3255c2d11a84114ffbf5878241a34d1b7be6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCasesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCasesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec12073354401977999305c2466f9bfbeed413fa283276ae466a16bca979f635)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCases")
    def reset_cases(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCases", []))

    @builtins.property
    @jsii.member(jsii_name="casesInput")
    def cases_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "casesInput"))

    @builtins.property
    @jsii.member(jsii_name="cases")
    def cases(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cases"))

    @cases.setter
    def cases(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b7187f78cd597ef0b25cd779485532cc09efd7289b3ad2ebf0db3d0dea9a29d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cases", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84068fca10acd7aae87e4f01967ed5b9a179bb7f03374d68aa13b22d4424ab85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowEventHandlersTriggerFulfillmentMessages",
    jsii_struct_bases=[],
    name_mapping={
        "channel": "channel",
        "conversation_success": "conversationSuccess",
        "live_agent_handoff": "liveAgentHandoff",
        "output_audio_text": "outputAudioText",
        "payload": "payload",
        "play_audio": "playAudio",
        "telephony_transfer_call": "telephonyTransferCall",
        "text": "text",
    },
)
class DialogflowCxFlowEventHandlersTriggerFulfillmentMessages:
    def __init__(
        self,
        *,
        channel: typing.Optional[builtins.str] = None,
        conversation_success: typing.Optional[typing.Union["DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccess", typing.Dict[builtins.str, typing.Any]]] = None,
        live_agent_handoff: typing.Optional[typing.Union["DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoff", typing.Dict[builtins.str, typing.Any]]] = None,
        output_audio_text: typing.Optional[typing.Union["DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioText", typing.Dict[builtins.str, typing.Any]]] = None,
        payload: typing.Optional[builtins.str] = None,
        play_audio: typing.Optional[typing.Union["DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudio", typing.Dict[builtins.str, typing.Any]]] = None,
        telephony_transfer_call: typing.Optional[typing.Union["DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCall", typing.Dict[builtins.str, typing.Any]]] = None,
        text: typing.Optional[typing.Union["DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesText", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param channel: The channel which the response is associated with. Clients can specify the channel via QueryParameters.channel, and only associated channel response will be returned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#channel DialogflowCxFlow#channel}
        :param conversation_success: conversation_success block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#conversation_success DialogflowCxFlow#conversation_success}
        :param live_agent_handoff: live_agent_handoff block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#live_agent_handoff DialogflowCxFlow#live_agent_handoff}
        :param output_audio_text: output_audio_text block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#output_audio_text DialogflowCxFlow#output_audio_text}
        :param payload: A custom, platform-specific payload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#payload DialogflowCxFlow#payload}
        :param play_audio: play_audio block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#play_audio DialogflowCxFlow#play_audio}
        :param telephony_transfer_call: telephony_transfer_call block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#telephony_transfer_call DialogflowCxFlow#telephony_transfer_call}
        :param text: text block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#text DialogflowCxFlow#text}
        '''
        if isinstance(conversation_success, dict):
            conversation_success = DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccess(**conversation_success)
        if isinstance(live_agent_handoff, dict):
            live_agent_handoff = DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoff(**live_agent_handoff)
        if isinstance(output_audio_text, dict):
            output_audio_text = DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioText(**output_audio_text)
        if isinstance(play_audio, dict):
            play_audio = DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudio(**play_audio)
        if isinstance(telephony_transfer_call, dict):
            telephony_transfer_call = DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCall(**telephony_transfer_call)
        if isinstance(text, dict):
            text = DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesText(**text)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8807fb19dc54302a5b8791edb5637a83298aee765bf6b45fda2334ee73f245a7)
            check_type(argname="argument channel", value=channel, expected_type=type_hints["channel"])
            check_type(argname="argument conversation_success", value=conversation_success, expected_type=type_hints["conversation_success"])
            check_type(argname="argument live_agent_handoff", value=live_agent_handoff, expected_type=type_hints["live_agent_handoff"])
            check_type(argname="argument output_audio_text", value=output_audio_text, expected_type=type_hints["output_audio_text"])
            check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
            check_type(argname="argument play_audio", value=play_audio, expected_type=type_hints["play_audio"])
            check_type(argname="argument telephony_transfer_call", value=telephony_transfer_call, expected_type=type_hints["telephony_transfer_call"])
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if channel is not None:
            self._values["channel"] = channel
        if conversation_success is not None:
            self._values["conversation_success"] = conversation_success
        if live_agent_handoff is not None:
            self._values["live_agent_handoff"] = live_agent_handoff
        if output_audio_text is not None:
            self._values["output_audio_text"] = output_audio_text
        if payload is not None:
            self._values["payload"] = payload
        if play_audio is not None:
            self._values["play_audio"] = play_audio
        if telephony_transfer_call is not None:
            self._values["telephony_transfer_call"] = telephony_transfer_call
        if text is not None:
            self._values["text"] = text

    @builtins.property
    def channel(self) -> typing.Optional[builtins.str]:
        '''The channel which the response is associated with.

        Clients can specify the channel via QueryParameters.channel, and only associated channel response will be returned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#channel DialogflowCxFlow#channel}
        '''
        result = self._values.get("channel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def conversation_success(
        self,
    ) -> typing.Optional["DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccess"]:
        '''conversation_success block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#conversation_success DialogflowCxFlow#conversation_success}
        '''
        result = self._values.get("conversation_success")
        return typing.cast(typing.Optional["DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccess"], result)

    @builtins.property
    def live_agent_handoff(
        self,
    ) -> typing.Optional["DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoff"]:
        '''live_agent_handoff block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#live_agent_handoff DialogflowCxFlow#live_agent_handoff}
        '''
        result = self._values.get("live_agent_handoff")
        return typing.cast(typing.Optional["DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoff"], result)

    @builtins.property
    def output_audio_text(
        self,
    ) -> typing.Optional["DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioText"]:
        '''output_audio_text block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#output_audio_text DialogflowCxFlow#output_audio_text}
        '''
        result = self._values.get("output_audio_text")
        return typing.cast(typing.Optional["DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioText"], result)

    @builtins.property
    def payload(self) -> typing.Optional[builtins.str]:
        '''A custom, platform-specific payload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#payload DialogflowCxFlow#payload}
        '''
        result = self._values.get("payload")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def play_audio(
        self,
    ) -> typing.Optional["DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudio"]:
        '''play_audio block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#play_audio DialogflowCxFlow#play_audio}
        '''
        result = self._values.get("play_audio")
        return typing.cast(typing.Optional["DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudio"], result)

    @builtins.property
    def telephony_transfer_call(
        self,
    ) -> typing.Optional["DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCall"]:
        '''telephony_transfer_call block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#telephony_transfer_call DialogflowCxFlow#telephony_transfer_call}
        '''
        result = self._values.get("telephony_transfer_call")
        return typing.cast(typing.Optional["DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCall"], result)

    @builtins.property
    def text(
        self,
    ) -> typing.Optional["DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesText"]:
        '''text block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#text DialogflowCxFlow#text}
        '''
        result = self._values.get("text")
        return typing.cast(typing.Optional["DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesText"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxFlowEventHandlersTriggerFulfillmentMessages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccess",
    jsii_struct_bases=[],
    name_mapping={"metadata": "metadata"},
)
class DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccess:
    def __init__(self, *, metadata: typing.Optional[builtins.str] = None) -> None:
        '''
        :param metadata: Custom metadata. Dialogflow doesn't impose any structure on this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#metadata DialogflowCxFlow#metadata}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba3823e96e2872ade15a730fbb317cd7584cb4e2641e3bc774f386111a5eac98)
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metadata is not None:
            self._values["metadata"] = metadata

    @builtins.property
    def metadata(self) -> typing.Optional[builtins.str]:
        '''Custom metadata. Dialogflow doesn't impose any structure on this.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#metadata DialogflowCxFlow#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__82a718517447c53db1a23f87dbd9d124ffe396f30cb2a775057d32b8e5f71ed4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c82dea188a395ac5cb800f51b563df52ca42b2960f6ff1490d0a89178608be26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccess]:
        return typing.cast(typing.Optional[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccess], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccess],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88c003cbbcb4e38bb63b5ba8bffc577b7b969685eff3117efcdf26d183450cf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__21b770448d89ac5ec61108568e4cfe70f38d02c255e25672d651fc27a5084b2f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__262f075c52147f062a1ec860717818d6c406b8e9e77c1c4854e2f59558fda25f)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ade9d6685795e8eb857c8fe31b0c2045737bbd4f324e8fc68d3f43e366ed652)
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
            type_hints = typing.get_type_hints(_typecheckingstub__490cda8ccf07195d8b7d15f8bef539a94d2a9300089141a5e30d6f6c8e668592)
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
            type_hints = typing.get_type_hints(_typecheckingstub__347b69d3503d65eb15250a87ce2e7e30566c0542d94b41817c634990e2fb87e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowEventHandlersTriggerFulfillmentMessages]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowEventHandlersTriggerFulfillmentMessages]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowEventHandlersTriggerFulfillmentMessages]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fb9e1f2abb770c0b7906f4440d3b4f63387c62c2156443aa7d819443649005d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoff",
    jsii_struct_bases=[],
    name_mapping={"metadata": "metadata"},
)
class DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoff:
    def __init__(self, *, metadata: typing.Optional[builtins.str] = None) -> None:
        '''
        :param metadata: Custom metadata. Dialogflow doesn't impose any structure on this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#metadata DialogflowCxFlow#metadata}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0be3bccd08bb404f763dcd6cd11e329dd1969de8ee26456b3e4bf8028e606e4)
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metadata is not None:
            self._values["metadata"] = metadata

    @builtins.property
    def metadata(self) -> typing.Optional[builtins.str]:
        '''Custom metadata. Dialogflow doesn't impose any structure on this.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#metadata DialogflowCxFlow#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoff(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoffOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoffOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__263875aeb3fdeaff84cc115e695d702b3a2fa7ca60afc64f9200339ec9280e0b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65e5dd53f603d1ab997ef49c121333cc9dc41e608780daa0bb5f6b6e4b98e530)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoff]:
        return typing.cast(typing.Optional[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoff], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoff],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9438ac86e894e23534dda49ceee92d28045bfcc35630d92a3debedab759d8d87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioText",
    jsii_struct_bases=[],
    name_mapping={"ssml": "ssml", "text": "text"},
)
class DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioText:
    def __init__(
        self,
        *,
        ssml: typing.Optional[builtins.str] = None,
        text: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ssml: The SSML text to be synthesized. For more information, see SSML. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#ssml DialogflowCxFlow#ssml}
        :param text: The raw text to be synthesized. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#text DialogflowCxFlow#text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5294bbdafa3d1437c1e90b17c51b5ffd6b701e31f13d0bf013702a7f1e1b5423)
            check_type(argname="argument ssml", value=ssml, expected_type=type_hints["ssml"])
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ssml is not None:
            self._values["ssml"] = ssml
        if text is not None:
            self._values["text"] = text

    @builtins.property
    def ssml(self) -> typing.Optional[builtins.str]:
        '''The SSML text to be synthesized. For more information, see SSML.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#ssml DialogflowCxFlow#ssml}
        '''
        result = self._values.get("ssml")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def text(self) -> typing.Optional[builtins.str]:
        '''The raw text to be synthesized.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#text DialogflowCxFlow#text}
        '''
        result = self._values.get("text")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioText(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioTextOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioTextOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2341b965234e63efabeb4aa660271cd27327448f303fd081dd49bce648670b4b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSsml")
    def reset_ssml(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSsml", []))

    @jsii.member(jsii_name="resetText")
    def reset_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetText", []))

    @builtins.property
    @jsii.member(jsii_name="allowPlaybackInterruption")
    def allow_playback_interruption(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "allowPlaybackInterruption"))

    @builtins.property
    @jsii.member(jsii_name="ssmlInput")
    def ssml_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ssmlInput"))

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="ssml")
    def ssml(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ssml"))

    @ssml.setter
    def ssml(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95bf8580d71992a3436c5af954ee4ffc30c4f6bdfc142a83d258f2bbb08a50ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ssml", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "text"))

    @text.setter
    def text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c26ce8483cfba356541e1034f78170e27120f710b05da9b4e17da98f1c69fb9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioText]:
        return typing.cast(typing.Optional[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioText], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioText],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeecfb0a40db87d164491e6ce4591a3c676ab581b86344ea3c36b721f676f988)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1524c5462e785cdf224f651345c075e4ee93b97de98cfbd3042f9b920ce5542)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putConversationSuccess")
    def put_conversation_success(
        self,
        *,
        metadata: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param metadata: Custom metadata. Dialogflow doesn't impose any structure on this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#metadata DialogflowCxFlow#metadata}
        '''
        value = DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccess(
            metadata=metadata
        )

        return typing.cast(None, jsii.invoke(self, "putConversationSuccess", [value]))

    @jsii.member(jsii_name="putLiveAgentHandoff")
    def put_live_agent_handoff(
        self,
        *,
        metadata: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param metadata: Custom metadata. Dialogflow doesn't impose any structure on this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#metadata DialogflowCxFlow#metadata}
        '''
        value = DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoff(
            metadata=metadata
        )

        return typing.cast(None, jsii.invoke(self, "putLiveAgentHandoff", [value]))

    @jsii.member(jsii_name="putOutputAudioText")
    def put_output_audio_text(
        self,
        *,
        ssml: typing.Optional[builtins.str] = None,
        text: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ssml: The SSML text to be synthesized. For more information, see SSML. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#ssml DialogflowCxFlow#ssml}
        :param text: The raw text to be synthesized. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#text DialogflowCxFlow#text}
        '''
        value = DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioText(
            ssml=ssml, text=text
        )

        return typing.cast(None, jsii.invoke(self, "putOutputAudioText", [value]))

    @jsii.member(jsii_name="putPlayAudio")
    def put_play_audio(self, *, audio_uri: builtins.str) -> None:
        '''
        :param audio_uri: URI of the audio clip. Dialogflow does not impose any validation on this value. It is specific to the client that reads it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#audio_uri DialogflowCxFlow#audio_uri}
        '''
        value = DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudio(
            audio_uri=audio_uri
        )

        return typing.cast(None, jsii.invoke(self, "putPlayAudio", [value]))

    @jsii.member(jsii_name="putTelephonyTransferCall")
    def put_telephony_transfer_call(self, *, phone_number: builtins.str) -> None:
        '''
        :param phone_number: Transfer the call to a phone number in E.164 format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#phone_number DialogflowCxFlow#phone_number}
        '''
        value = DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCall(
            phone_number=phone_number
        )

        return typing.cast(None, jsii.invoke(self, "putTelephonyTransferCall", [value]))

    @jsii.member(jsii_name="putText")
    def put_text(
        self,
        *,
        text: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param text: A collection of text responses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#text DialogflowCxFlow#text}
        '''
        value = DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesText(text=text)

        return typing.cast(None, jsii.invoke(self, "putText", [value]))

    @jsii.member(jsii_name="resetChannel")
    def reset_channel(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChannel", []))

    @jsii.member(jsii_name="resetConversationSuccess")
    def reset_conversation_success(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConversationSuccess", []))

    @jsii.member(jsii_name="resetLiveAgentHandoff")
    def reset_live_agent_handoff(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLiveAgentHandoff", []))

    @jsii.member(jsii_name="resetOutputAudioText")
    def reset_output_audio_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputAudioText", []))

    @jsii.member(jsii_name="resetPayload")
    def reset_payload(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPayload", []))

    @jsii.member(jsii_name="resetPlayAudio")
    def reset_play_audio(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlayAudio", []))

    @jsii.member(jsii_name="resetTelephonyTransferCall")
    def reset_telephony_transfer_call(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTelephonyTransferCall", []))

    @jsii.member(jsii_name="resetText")
    def reset_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetText", []))

    @builtins.property
    @jsii.member(jsii_name="conversationSuccess")
    def conversation_success(
        self,
    ) -> DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccessOutputReference:
        return typing.cast(DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccessOutputReference, jsii.get(self, "conversationSuccess"))

    @builtins.property
    @jsii.member(jsii_name="liveAgentHandoff")
    def live_agent_handoff(
        self,
    ) -> DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoffOutputReference:
        return typing.cast(DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoffOutputReference, jsii.get(self, "liveAgentHandoff"))

    @builtins.property
    @jsii.member(jsii_name="outputAudioText")
    def output_audio_text(
        self,
    ) -> DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioTextOutputReference:
        return typing.cast(DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioTextOutputReference, jsii.get(self, "outputAudioText"))

    @builtins.property
    @jsii.member(jsii_name="playAudio")
    def play_audio(
        self,
    ) -> "DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudioOutputReference":
        return typing.cast("DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudioOutputReference", jsii.get(self, "playAudio"))

    @builtins.property
    @jsii.member(jsii_name="telephonyTransferCall")
    def telephony_transfer_call(
        self,
    ) -> "DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCallOutputReference":
        return typing.cast("DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCallOutputReference", jsii.get(self, "telephonyTransferCall"))

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(
        self,
    ) -> "DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTextOutputReference":
        return typing.cast("DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTextOutputReference", jsii.get(self, "text"))

    @builtins.property
    @jsii.member(jsii_name="channelInput")
    def channel_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "channelInput"))

    @builtins.property
    @jsii.member(jsii_name="conversationSuccessInput")
    def conversation_success_input(
        self,
    ) -> typing.Optional[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccess]:
        return typing.cast(typing.Optional[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccess], jsii.get(self, "conversationSuccessInput"))

    @builtins.property
    @jsii.member(jsii_name="liveAgentHandoffInput")
    def live_agent_handoff_input(
        self,
    ) -> typing.Optional[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoff]:
        return typing.cast(typing.Optional[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoff], jsii.get(self, "liveAgentHandoffInput"))

    @builtins.property
    @jsii.member(jsii_name="outputAudioTextInput")
    def output_audio_text_input(
        self,
    ) -> typing.Optional[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioText]:
        return typing.cast(typing.Optional[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioText], jsii.get(self, "outputAudioTextInput"))

    @builtins.property
    @jsii.member(jsii_name="payloadInput")
    def payload_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "payloadInput"))

    @builtins.property
    @jsii.member(jsii_name="playAudioInput")
    def play_audio_input(
        self,
    ) -> typing.Optional["DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudio"]:
        return typing.cast(typing.Optional["DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudio"], jsii.get(self, "playAudioInput"))

    @builtins.property
    @jsii.member(jsii_name="telephonyTransferCallInput")
    def telephony_transfer_call_input(
        self,
    ) -> typing.Optional["DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCall"]:
        return typing.cast(typing.Optional["DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCall"], jsii.get(self, "telephonyTransferCallInput"))

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(
        self,
    ) -> typing.Optional["DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesText"]:
        return typing.cast(typing.Optional["DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesText"], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="channel")
    def channel(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "channel"))

    @channel.setter
    def channel(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53ba97550e4e4d4d5e8f98e87fea663c90ff4b2f79c2bba37be25c824ce5d54a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="payload")
    def payload(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "payload"))

    @payload.setter
    def payload(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0873c8bab7c38190bcad107ed6092d6e84880681471cd8c791e91f3f0e8d1277)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "payload", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowEventHandlersTriggerFulfillmentMessages]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowEventHandlersTriggerFulfillmentMessages]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowEventHandlersTriggerFulfillmentMessages]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff62b63d51d275c5d6f8090162f9e76effd8a6fac20ff5615d088145d1a8a435)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudio",
    jsii_struct_bases=[],
    name_mapping={"audio_uri": "audioUri"},
)
class DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudio:
    def __init__(self, *, audio_uri: builtins.str) -> None:
        '''
        :param audio_uri: URI of the audio clip. Dialogflow does not impose any validation on this value. It is specific to the client that reads it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#audio_uri DialogflowCxFlow#audio_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__402d8129c6fc608a5c28c7d40e6f2ae023b71568c916fdfbd48e1857cc21c4e9)
            check_type(argname="argument audio_uri", value=audio_uri, expected_type=type_hints["audio_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "audio_uri": audio_uri,
        }

    @builtins.property
    def audio_uri(self) -> builtins.str:
        '''URI of the audio clip.

        Dialogflow does not impose any validation on this value. It is specific to the client that reads it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#audio_uri DialogflowCxFlow#audio_uri}
        '''
        result = self._values.get("audio_uri")
        assert result is not None, "Required property 'audio_uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudio(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudioOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudioOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1cf877dbdcab61dc3ffea4bb8b1199eac9d4d14c6be684eccd7aeac2b3470442)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="allowPlaybackInterruption")
    def allow_playback_interruption(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "allowPlaybackInterruption"))

    @builtins.property
    @jsii.member(jsii_name="audioUriInput")
    def audio_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "audioUriInput"))

    @builtins.property
    @jsii.member(jsii_name="audioUri")
    def audio_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "audioUri"))

    @audio_uri.setter
    def audio_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__244cb35bb11cef20b1fab7883d4424387643ee156d7c767893e3bfa870fd9b27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audioUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudio]:
        return typing.cast(typing.Optional[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudio], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudio],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01301615909f5868a189717124c2b92ded840cbb5506e492a2ce452ccedb8b13)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCall",
    jsii_struct_bases=[],
    name_mapping={"phone_number": "phoneNumber"},
)
class DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCall:
    def __init__(self, *, phone_number: builtins.str) -> None:
        '''
        :param phone_number: Transfer the call to a phone number in E.164 format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#phone_number DialogflowCxFlow#phone_number}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1407e0d2af6f452f0508586857daeec50f0519155533376eb1ab8d717beb8091)
            check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "phone_number": phone_number,
        }

    @builtins.property
    def phone_number(self) -> builtins.str:
        '''Transfer the call to a phone number in E.164 format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#phone_number DialogflowCxFlow#phone_number}
        '''
        result = self._values.get("phone_number")
        assert result is not None, "Required property 'phone_number' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCall(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCallOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCallOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__fba771409820a4ffc907da640c7cce8da69bba89140b3fb1dcd0b51261b8a2e2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="phoneNumberInput")
    def phone_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "phoneNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="phoneNumber")
    def phone_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "phoneNumber"))

    @phone_number.setter
    def phone_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__591d8e7d47e829f08f94b2528022016d929e20be855c72105d6848e00acf4e04)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "phoneNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCall]:
        return typing.cast(typing.Optional[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCall], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCall],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__104d3ff6aef14cddfe012b1114d4330f2ebe1db07611af97baf367796c168ccc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesText",
    jsii_struct_bases=[],
    name_mapping={"text": "text"},
)
class DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesText:
    def __init__(
        self,
        *,
        text: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param text: A collection of text responses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#text DialogflowCxFlow#text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdd95e583f0f8e3952133f2d2714eb49bf442d20d97cf76c67da3451d7552bda)
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if text is not None:
            self._values["text"] = text

    @builtins.property
    def text(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A collection of text responses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#text DialogflowCxFlow#text}
        '''
        result = self._values.get("text")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesText(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTextOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTextOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__57cf17e974838a6242a027dedf66d43786df9575c82a70e064bed3dda836967c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetText")
    def reset_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetText", []))

    @builtins.property
    @jsii.member(jsii_name="allowPlaybackInterruption")
    def allow_playback_interruption(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "allowPlaybackInterruption"))

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "text"))

    @text.setter
    def text(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d86bc876f8f99cb85e526b3d3728b33ff0f0688c3ade59490450e925a5e2ae8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesText]:
        return typing.cast(typing.Optional[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesText], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesText],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__054f059845dc63fe3ff4484c8d63dd0e5661049e8aea5d7a6da7201eedddd55d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxFlowEventHandlersTriggerFulfillmentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowEventHandlersTriggerFulfillmentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f256153b78f3197a824e460ce580ddaaed6454618276d329352d9b81f68ee7ba)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConditionalCases")
    def put_conditional_cases(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe85ef43b4cd5ec3bf7ae9530155742865204d7f38299907b44c593e76dc0f0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConditionalCases", [value]))

    @jsii.member(jsii_name="putMessages")
    def put_messages(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxFlowEventHandlersTriggerFulfillmentMessages, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21b031f4424f59e1854a021f9239fbd8386770bb851d54a0411fbf40beeb4f7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMessages", [value]))

    @jsii.member(jsii_name="putSetParameterActions")
    def put_set_parameter_actions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2684484e0e08e5acb5d7486a4df112d4743bd49a548c0bd5355d14731bf562d8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSetParameterActions", [value]))

    @jsii.member(jsii_name="resetConditionalCases")
    def reset_conditional_cases(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConditionalCases", []))

    @jsii.member(jsii_name="resetMessages")
    def reset_messages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessages", []))

    @jsii.member(jsii_name="resetReturnPartialResponses")
    def reset_return_partial_responses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReturnPartialResponses", []))

    @jsii.member(jsii_name="resetSetParameterActions")
    def reset_set_parameter_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSetParameterActions", []))

    @jsii.member(jsii_name="resetTag")
    def reset_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTag", []))

    @jsii.member(jsii_name="resetWebhook")
    def reset_webhook(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebhook", []))

    @builtins.property
    @jsii.member(jsii_name="conditionalCases")
    def conditional_cases(
        self,
    ) -> DialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCasesList:
        return typing.cast(DialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCasesList, jsii.get(self, "conditionalCases"))

    @builtins.property
    @jsii.member(jsii_name="messages")
    def messages(self) -> DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesList:
        return typing.cast(DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesList, jsii.get(self, "messages"))

    @builtins.property
    @jsii.member(jsii_name="setParameterActions")
    def set_parameter_actions(
        self,
    ) -> "DialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActionsList":
        return typing.cast("DialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActionsList", jsii.get(self, "setParameterActions"))

    @builtins.property
    @jsii.member(jsii_name="conditionalCasesInput")
    def conditional_cases_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases]]], jsii.get(self, "conditionalCasesInput"))

    @builtins.property
    @jsii.member(jsii_name="messagesInput")
    def messages_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowEventHandlersTriggerFulfillmentMessages]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowEventHandlersTriggerFulfillmentMessages]]], jsii.get(self, "messagesInput"))

    @builtins.property
    @jsii.member(jsii_name="returnPartialResponsesInput")
    def return_partial_responses_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "returnPartialResponsesInput"))

    @builtins.property
    @jsii.member(jsii_name="setParameterActionsInput")
    def set_parameter_actions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions"]]], jsii.get(self, "setParameterActionsInput"))

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="webhookInput")
    def webhook_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "webhookInput"))

    @builtins.property
    @jsii.member(jsii_name="returnPartialResponses")
    def return_partial_responses(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "returnPartialResponses"))

    @return_partial_responses.setter
    def return_partial_responses(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cba925b43c672643b6fa0e75b060c109ef581b2219659984ff256b7d49a0070)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "returnPartialResponses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fc3c0ee598b94116313bbfb910bba4f5eb11f0c83d50237810c05cfa830d916)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webhook")
    def webhook(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webhook"))

    @webhook.setter
    def webhook(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1b9bb2275f0b408217bff39ff97c6e1b425df4191dbec32fd4c2756e2a7842e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webhook", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxFlowEventHandlersTriggerFulfillment]:
        return typing.cast(typing.Optional[DialogflowCxFlowEventHandlersTriggerFulfillment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxFlowEventHandlersTriggerFulfillment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dec095f27b282c7e7491c82951472e3f5621a882e12b651a948ce6d1e5788a38)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions",
    jsii_struct_bases=[],
    name_mapping={"parameter": "parameter", "value": "value"},
)
class DialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions:
    def __init__(
        self,
        *,
        parameter: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param parameter: Display name of the parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#parameter DialogflowCxFlow#parameter}
        :param value: The new JSON-encoded value of the parameter. A null value clears the parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#value DialogflowCxFlow#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f183a5721eaadf5b77f2882fb66c55fd2d0442a95ea4152d6f9802706591ef99)
            check_type(argname="argument parameter", value=parameter, expected_type=type_hints["parameter"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if parameter is not None:
            self._values["parameter"] = parameter
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def parameter(self) -> typing.Optional[builtins.str]:
        '''Display name of the parameter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#parameter DialogflowCxFlow#parameter}
        '''
        result = self._values.get("parameter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The new JSON-encoded value of the parameter. A null value clears the parameter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#value DialogflowCxFlow#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__291c5a3c72a4b275d87d4090f364f8f83a6b56543fefc5f8951d3cb23b57278e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce43729d47de9e0a2248fac37ae0ee9d28586060898863b972bfce5b830d2b15)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04d0bc992af35b41b59a45d6f88fae06f55958881af324821d78aaa53e9c3bf0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5526c6c535ba9e2458425fb60c4df22987bb2bb22b72e3e6d618d4c3eca647d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6369b9def5bf59a9efde6314945eba95e0a3b3997c31f7709bd55d51d99c25b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74bda41ed7f37e89f14f017baf045a4b96bc74b1df5f252c93b0704bf981eca8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f450a147fbcfa587f875ab74a1e0656a6a9e2d4e6643de75e998bec0028eeefb)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetParameter")
    def reset_parameter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameter", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="parameterInput")
    def parameter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parameterInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="parameter")
    def parameter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameter"))

    @parameter.setter
    def parameter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b10305198beb60fa9d7d6c3b9e91c106b9c68d37d3f482b096e449356e834b5d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33fa6f813009dcf12c2aca2c8275db9a4eead2f4440b760ebea83f48bbce3df2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe092cc3c26fba38eb62a11a4bed3fad593d0061def3b0a181561c59e1659372)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowNluSettings",
    jsii_struct_bases=[],
    name_mapping={
        "classification_threshold": "classificationThreshold",
        "model_training_mode": "modelTrainingMode",
        "model_type": "modelType",
    },
)
class DialogflowCxFlowNluSettings:
    def __init__(
        self,
        *,
        classification_threshold: typing.Optional[jsii.Number] = None,
        model_training_mode: typing.Optional[builtins.str] = None,
        model_type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param classification_threshold: To filter out false positive results and still get variety in matched natural language inputs for your agent, you can tune the machine learning classification threshold. If the returned score value is less than the threshold value, then a no-match event will be triggered. The score values range from 0.0 (completely uncertain) to 1.0 (completely certain). If set to 0.0, the default of 0.3 is used. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#classification_threshold DialogflowCxFlow#classification_threshold}
        :param model_training_mode: Indicates NLU model training mode. - MODEL_TRAINING_MODE_AUTOMATIC: NLU model training is automatically triggered when a flow gets modified. User can also manually trigger model training in this mode. - MODEL_TRAINING_MODE_MANUAL: User needs to manually trigger NLU model training. Best for large flows whose models take long time to train. Possible values: ["MODEL_TRAINING_MODE_AUTOMATIC", "MODEL_TRAINING_MODE_MANUAL"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#model_training_mode DialogflowCxFlow#model_training_mode}
        :param model_type: Indicates the type of NLU model. - MODEL_TYPE_STANDARD: Use standard NLU model. - MODEL_TYPE_ADVANCED: Use advanced NLU model. Possible values: ["MODEL_TYPE_STANDARD", "MODEL_TYPE_ADVANCED"] Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#model_type DialogflowCxFlow#model_type}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02f6b106a84e9a588f565581ce95b6d4506e9efe0633a5a30c824027ded98f8e)
            check_type(argname="argument classification_threshold", value=classification_threshold, expected_type=type_hints["classification_threshold"])
            check_type(argname="argument model_training_mode", value=model_training_mode, expected_type=type_hints["model_training_mode"])
            check_type(argname="argument model_type", value=model_type, expected_type=type_hints["model_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if classification_threshold is not None:
            self._values["classification_threshold"] = classification_threshold
        if model_training_mode is not None:
            self._values["model_training_mode"] = model_training_mode
        if model_type is not None:
            self._values["model_type"] = model_type

    @builtins.property
    def classification_threshold(self) -> typing.Optional[jsii.Number]:
        '''To filter out false positive results and still get variety in matched natural language inputs for your agent, you can tune the machine learning classification threshold.

        If the returned score value is less than the threshold value, then a no-match event will be triggered. The score values range from 0.0 (completely uncertain) to 1.0 (completely certain). If set to 0.0, the default of 0.3 is used.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#classification_threshold DialogflowCxFlow#classification_threshold}
        '''
        result = self._values.get("classification_threshold")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def model_training_mode(self) -> typing.Optional[builtins.str]:
        '''Indicates NLU model training mode.

        - MODEL_TRAINING_MODE_AUTOMATIC: NLU model training is automatically triggered when a flow gets modified. User can also manually trigger model training in this mode.
        - MODEL_TRAINING_MODE_MANUAL: User needs to manually trigger NLU model training. Best for large flows whose models take long time to train. Possible values: ["MODEL_TRAINING_MODE_AUTOMATIC", "MODEL_TRAINING_MODE_MANUAL"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#model_training_mode DialogflowCxFlow#model_training_mode}
        '''
        result = self._values.get("model_training_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def model_type(self) -> typing.Optional[builtins.str]:
        '''Indicates the type of NLU model.

        - MODEL_TYPE_STANDARD: Use standard NLU model.
        - MODEL_TYPE_ADVANCED: Use advanced NLU model. Possible values: ["MODEL_TYPE_STANDARD", "MODEL_TYPE_ADVANCED"]

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#model_type DialogflowCxFlow#model_type}
        '''
        result = self._values.get("model_type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxFlowNluSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxFlowNluSettingsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowNluSettingsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ecadb1a6ad6fc086ec8e4c48ee7bd4f9c8531e0d1489bb7f76700696043ae20)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetClassificationThreshold")
    def reset_classification_threshold(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClassificationThreshold", []))

    @jsii.member(jsii_name="resetModelTrainingMode")
    def reset_model_training_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModelTrainingMode", []))

    @jsii.member(jsii_name="resetModelType")
    def reset_model_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetModelType", []))

    @builtins.property
    @jsii.member(jsii_name="classificationThresholdInput")
    def classification_threshold_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "classificationThresholdInput"))

    @builtins.property
    @jsii.member(jsii_name="modelTrainingModeInput")
    def model_training_mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelTrainingModeInput"))

    @builtins.property
    @jsii.member(jsii_name="modelTypeInput")
    def model_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modelTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="classificationThreshold")
    def classification_threshold(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "classificationThreshold"))

    @classification_threshold.setter
    def classification_threshold(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c18e3a073f391591d61fb72fbb677ab3870989127160c981f5ee629f9c9eb850)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "classificationThreshold", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modelTrainingMode")
    def model_training_mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modelTrainingMode"))

    @model_training_mode.setter
    def model_training_mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daa015a12e14b95c8f7cc50e72d8355131e0d6c86bff90e56cc7ca8b859bb4c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelTrainingMode", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="modelType")
    def model_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "modelType"))

    @model_type.setter
    def model_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ad70c7b65d59e819484e126777959a67520c66af79f6a95747836b6743a3928)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "modelType", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DialogflowCxFlowNluSettings]:
        return typing.cast(typing.Optional[DialogflowCxFlowNluSettings], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxFlowNluSettings],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3ad5e37690e1d5583d17d8ed896e065d40dbb14d7fb295d250b23fb1fb1f81d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete", "update": "update"},
)
class DialogflowCxFlowTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#create DialogflowCxFlow#create}.
        :param delete: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#delete DialogflowCxFlow#delete}.
        :param update: Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#update DialogflowCxFlow#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8595441ba1272955ed9d1289461f1ec0cceca2c1250babf980aebbe83f17fce6)
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
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#create DialogflowCxFlow#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#delete DialogflowCxFlow#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#update DialogflowCxFlow#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxFlowTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxFlowTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0f13b5bbe0d8c6aff2266b7a43514243479d306c23b86c90b0d24dac2e98a97a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f613cc8a6aa58b0cca48cb6853adbb2bab8b9ba79185cc356a03f0fd93feb59f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7dae9783620ec4262dee1dd25877228e67a00c4a5c4a787974b5e74420ffe3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37e9c7689abb731e5baacb5831824aea96a32b5d8e467a97b875794466400837)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowTimeouts]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowTimeouts]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowTimeouts]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0279cd75bdf19b77c9bbdbb7015123e522afc61d5e7c4c3e0e5cc1a2e7f9e2e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowTransitionRoutes",
    jsii_struct_bases=[],
    name_mapping={
        "condition": "condition",
        "intent": "intent",
        "target_flow": "targetFlow",
        "target_page": "targetPage",
        "trigger_fulfillment": "triggerFulfillment",
    },
)
class DialogflowCxFlowTransitionRoutes:
    def __init__(
        self,
        *,
        condition: typing.Optional[builtins.str] = None,
        intent: typing.Optional[builtins.str] = None,
        target_flow: typing.Optional[builtins.str] = None,
        target_page: typing.Optional[builtins.str] = None,
        trigger_fulfillment: typing.Optional[typing.Union["DialogflowCxFlowTransitionRoutesTriggerFulfillment", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param condition: The condition to evaluate against form parameters or session parameters. At least one of intent or condition must be specified. When both intent and condition are specified, the transition can only happen when both are fulfilled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#condition DialogflowCxFlow#condition}
        :param intent: The unique identifier of an Intent. Format: projects//locations//agents//intents/. Indicates that the transition can only happen when the given intent is matched. At least one of intent or condition must be specified. When both intent and condition are specified, the transition can only happen when both are fulfilled. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#intent DialogflowCxFlow#intent}
        :param target_flow: The target flow to transition to. Format: projects//locations//agents//flows/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#target_flow DialogflowCxFlow#target_flow}
        :param target_page: The target page to transition to. Format: projects//locations//agents//flows//pages/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#target_page DialogflowCxFlow#target_page}
        :param trigger_fulfillment: trigger_fulfillment block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#trigger_fulfillment DialogflowCxFlow#trigger_fulfillment}
        '''
        if isinstance(trigger_fulfillment, dict):
            trigger_fulfillment = DialogflowCxFlowTransitionRoutesTriggerFulfillment(**trigger_fulfillment)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afb349726c9c31ddae7f58a58dde47bafc67004b8e33839114f67981eb49406b)
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument intent", value=intent, expected_type=type_hints["intent"])
            check_type(argname="argument target_flow", value=target_flow, expected_type=type_hints["target_flow"])
            check_type(argname="argument target_page", value=target_page, expected_type=type_hints["target_page"])
            check_type(argname="argument trigger_fulfillment", value=trigger_fulfillment, expected_type=type_hints["trigger_fulfillment"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if condition is not None:
            self._values["condition"] = condition
        if intent is not None:
            self._values["intent"] = intent
        if target_flow is not None:
            self._values["target_flow"] = target_flow
        if target_page is not None:
            self._values["target_page"] = target_page
        if trigger_fulfillment is not None:
            self._values["trigger_fulfillment"] = trigger_fulfillment

    @builtins.property
    def condition(self) -> typing.Optional[builtins.str]:
        '''The condition to evaluate against form parameters or session parameters.

        At least one of intent or condition must be specified. When both intent and condition are specified, the transition can only happen when both are fulfilled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#condition DialogflowCxFlow#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def intent(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of an Intent.

        Format: projects//locations//agents//intents/. Indicates that the transition can only happen when the given intent is matched. At least one of intent or condition must be specified. When both intent and condition are specified, the transition can only happen when both are fulfilled.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#intent DialogflowCxFlow#intent}
        '''
        result = self._values.get("intent")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_flow(self) -> typing.Optional[builtins.str]:
        '''The target flow to transition to. Format: projects//locations//agents//flows/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#target_flow DialogflowCxFlow#target_flow}
        '''
        result = self._values.get("target_flow")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target_page(self) -> typing.Optional[builtins.str]:
        '''The target page to transition to. Format: projects//locations//agents//flows//pages/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#target_page DialogflowCxFlow#target_page}
        '''
        result = self._values.get("target_page")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def trigger_fulfillment(
        self,
    ) -> typing.Optional["DialogflowCxFlowTransitionRoutesTriggerFulfillment"]:
        '''trigger_fulfillment block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#trigger_fulfillment DialogflowCxFlow#trigger_fulfillment}
        '''
        result = self._values.get("trigger_fulfillment")
        return typing.cast(typing.Optional["DialogflowCxFlowTransitionRoutesTriggerFulfillment"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxFlowTransitionRoutes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxFlowTransitionRoutesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowTransitionRoutesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ed5aba3d1edf1da1e49b8206ead0ab85228fa64d85a06a915277d0eb62c7371)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DialogflowCxFlowTransitionRoutesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97cf4cab7e3d08968dacb385e05c3ab3c333bf02b477f756ab68c6e2678f07c1)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DialogflowCxFlowTransitionRoutesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c7eb9470a4650390f971e50d8db38f40f3bff8f3e410b6609060e635c3920b1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91e39e72c45cff7c250c07f16bc2580ffa3f0df8ad0cddf37517f6c71b075cba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ac8e5a25899f288f88a8ec3222188a889d782f62f8ae506b72433d61bb02a29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowTransitionRoutes]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowTransitionRoutes]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowTransitionRoutes]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfca25e7faa60fd92f676604b860dc2478f44d6d7ce64f7a37d0951c4bd735af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxFlowTransitionRoutesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowTransitionRoutesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__651912c51f88ac2e5df13f68f2a7e8657d71fe8eb3c400bd9b0499fa124becd2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putTriggerFulfillment")
    def put_trigger_fulfillment(
        self,
        *,
        conditional_cases: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases", typing.Dict[builtins.str, typing.Any]]]]] = None,
        messages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages", typing.Dict[builtins.str, typing.Any]]]]] = None,
        return_partial_responses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        set_parameter_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tag: typing.Optional[builtins.str] = None,
        webhook: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param conditional_cases: conditional_cases block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#conditional_cases DialogflowCxFlow#conditional_cases}
        :param messages: messages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#messages DialogflowCxFlow#messages}
        :param return_partial_responses: Whether Dialogflow should return currently queued fulfillment response messages in streaming APIs. If a webhook is specified, it happens before Dialogflow invokes webhook. Warning: 1) This flag only affects streaming API. Responses are still queued and returned once in non-streaming API. 2) The flag can be enabled in any fulfillment but only the first 3 partial responses will be returned. You may only want to apply it to fulfillments that have slow webhooks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#return_partial_responses DialogflowCxFlow#return_partial_responses}
        :param set_parameter_actions: set_parameter_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#set_parameter_actions DialogflowCxFlow#set_parameter_actions}
        :param tag: The tag used by the webhook to identify which fulfillment is being called. This field is required if webhook is specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#tag DialogflowCxFlow#tag}
        :param webhook: The webhook to call. Format: projects//locations//agents//webhooks/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#webhook DialogflowCxFlow#webhook}
        '''
        value = DialogflowCxFlowTransitionRoutesTriggerFulfillment(
            conditional_cases=conditional_cases,
            messages=messages,
            return_partial_responses=return_partial_responses,
            set_parameter_actions=set_parameter_actions,
            tag=tag,
            webhook=webhook,
        )

        return typing.cast(None, jsii.invoke(self, "putTriggerFulfillment", [value]))

    @jsii.member(jsii_name="resetCondition")
    def reset_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCondition", []))

    @jsii.member(jsii_name="resetIntent")
    def reset_intent(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIntent", []))

    @jsii.member(jsii_name="resetTargetFlow")
    def reset_target_flow(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetFlow", []))

    @jsii.member(jsii_name="resetTargetPage")
    def reset_target_page(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetPage", []))

    @jsii.member(jsii_name="resetTriggerFulfillment")
    def reset_trigger_fulfillment(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTriggerFulfillment", []))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="triggerFulfillment")
    def trigger_fulfillment(
        self,
    ) -> "DialogflowCxFlowTransitionRoutesTriggerFulfillmentOutputReference":
        return typing.cast("DialogflowCxFlowTransitionRoutesTriggerFulfillmentOutputReference", jsii.get(self, "triggerFulfillment"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="intentInput")
    def intent_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "intentInput"))

    @builtins.property
    @jsii.member(jsii_name="targetFlowInput")
    def target_flow_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetFlowInput"))

    @builtins.property
    @jsii.member(jsii_name="targetPageInput")
    def target_page_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "targetPageInput"))

    @builtins.property
    @jsii.member(jsii_name="triggerFulfillmentInput")
    def trigger_fulfillment_input(
        self,
    ) -> typing.Optional["DialogflowCxFlowTransitionRoutesTriggerFulfillment"]:
        return typing.cast(typing.Optional["DialogflowCxFlowTransitionRoutesTriggerFulfillment"], jsii.get(self, "triggerFulfillmentInput"))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "condition"))

    @condition.setter
    def condition(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9300f3859e3dce89b25ab991e8d74ad8000436485e9ce180cc81546b8f94aded)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "condition", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="intent")
    def intent(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "intent"))

    @intent.setter
    def intent(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53965fd3d6e2ad491c51bd4a24fb15bb648bfa16e0e93ba4e7660fdfc2c546b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "intent", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetFlow")
    def target_flow(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetFlow"))

    @target_flow.setter
    def target_flow(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__052a0226286124b80387d0d8b3d805f9b1f88822020a9498b28202e1f32f57cc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetFlow", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="targetPage")
    def target_page(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "targetPage"))

    @target_page.setter
    def target_page(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__684cffac9909be18e70add392b8cc7970460e54c61600719a7b78d1d2cf89ac3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetPage", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowTransitionRoutes]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowTransitionRoutes]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowTransitionRoutes]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f94ff6828f6e3d4f466b85bc58a6ba2f3350c4e843273e9bf5c52a87b9d78668)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowTransitionRoutesTriggerFulfillment",
    jsii_struct_bases=[],
    name_mapping={
        "conditional_cases": "conditionalCases",
        "messages": "messages",
        "return_partial_responses": "returnPartialResponses",
        "set_parameter_actions": "setParameterActions",
        "tag": "tag",
        "webhook": "webhook",
    },
)
class DialogflowCxFlowTransitionRoutesTriggerFulfillment:
    def __init__(
        self,
        *,
        conditional_cases: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases", typing.Dict[builtins.str, typing.Any]]]]] = None,
        messages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages", typing.Dict[builtins.str, typing.Any]]]]] = None,
        return_partial_responses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        set_parameter_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions", typing.Dict[builtins.str, typing.Any]]]]] = None,
        tag: typing.Optional[builtins.str] = None,
        webhook: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param conditional_cases: conditional_cases block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#conditional_cases DialogflowCxFlow#conditional_cases}
        :param messages: messages block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#messages DialogflowCxFlow#messages}
        :param return_partial_responses: Whether Dialogflow should return currently queued fulfillment response messages in streaming APIs. If a webhook is specified, it happens before Dialogflow invokes webhook. Warning: 1) This flag only affects streaming API. Responses are still queued and returned once in non-streaming API. 2) The flag can be enabled in any fulfillment but only the first 3 partial responses will be returned. You may only want to apply it to fulfillments that have slow webhooks. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#return_partial_responses DialogflowCxFlow#return_partial_responses}
        :param set_parameter_actions: set_parameter_actions block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#set_parameter_actions DialogflowCxFlow#set_parameter_actions}
        :param tag: The tag used by the webhook to identify which fulfillment is being called. This field is required if webhook is specified. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#tag DialogflowCxFlow#tag}
        :param webhook: The webhook to call. Format: projects//locations//agents//webhooks/. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#webhook DialogflowCxFlow#webhook}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__432893f9cd29f37454ec7f8cbb609d9f910a492bf9c70661909d433841916dbb)
            check_type(argname="argument conditional_cases", value=conditional_cases, expected_type=type_hints["conditional_cases"])
            check_type(argname="argument messages", value=messages, expected_type=type_hints["messages"])
            check_type(argname="argument return_partial_responses", value=return_partial_responses, expected_type=type_hints["return_partial_responses"])
            check_type(argname="argument set_parameter_actions", value=set_parameter_actions, expected_type=type_hints["set_parameter_actions"])
            check_type(argname="argument tag", value=tag, expected_type=type_hints["tag"])
            check_type(argname="argument webhook", value=webhook, expected_type=type_hints["webhook"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if conditional_cases is not None:
            self._values["conditional_cases"] = conditional_cases
        if messages is not None:
            self._values["messages"] = messages
        if return_partial_responses is not None:
            self._values["return_partial_responses"] = return_partial_responses
        if set_parameter_actions is not None:
            self._values["set_parameter_actions"] = set_parameter_actions
        if tag is not None:
            self._values["tag"] = tag
        if webhook is not None:
            self._values["webhook"] = webhook

    @builtins.property
    def conditional_cases(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases"]]]:
        '''conditional_cases block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#conditional_cases DialogflowCxFlow#conditional_cases}
        '''
        result = self._values.get("conditional_cases")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases"]]], result)

    @builtins.property
    def messages(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages"]]]:
        '''messages block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#messages DialogflowCxFlow#messages}
        '''
        result = self._values.get("messages")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages"]]], result)

    @builtins.property
    def return_partial_responses(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether Dialogflow should return currently queued fulfillment response messages in streaming APIs.

        If a webhook is specified, it happens before Dialogflow invokes webhook. Warning: 1) This flag only affects streaming API. Responses are still queued and returned once in non-streaming API. 2) The flag can be enabled in any fulfillment but only the first 3 partial responses will be returned. You may only want to apply it to fulfillments that have slow webhooks.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#return_partial_responses DialogflowCxFlow#return_partial_responses}
        '''
        result = self._values.get("return_partial_responses")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def set_parameter_actions(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions"]]]:
        '''set_parameter_actions block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#set_parameter_actions DialogflowCxFlow#set_parameter_actions}
        '''
        result = self._values.get("set_parameter_actions")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions"]]], result)

    @builtins.property
    def tag(self) -> typing.Optional[builtins.str]:
        '''The tag used by the webhook to identify which fulfillment is being called.

        This field is required if webhook is specified.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#tag DialogflowCxFlow#tag}
        '''
        result = self._values.get("tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def webhook(self) -> typing.Optional[builtins.str]:
        '''The webhook to call. Format: projects//locations//agents//webhooks/.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#webhook DialogflowCxFlow#webhook}
        '''
        result = self._values.get("webhook")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxFlowTransitionRoutesTriggerFulfillment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases",
    jsii_struct_bases=[],
    name_mapping={"cases": "cases"},
)
class DialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases:
    def __init__(self, *, cases: typing.Optional[builtins.str] = None) -> None:
        '''
        :param cases: A JSON encoded list of cascading if-else conditions. Cases are mutually exclusive. The first one with a matching condition is selected, all the rest ignored. See `Case <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/Fulfillment#case>`_ for the schema. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#cases DialogflowCxFlow#cases}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db75a87a152b7f8cd24c2d3be5187a09faedcdd7a31294efca73627fced7e4f2)
            check_type(argname="argument cases", value=cases, expected_type=type_hints["cases"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cases is not None:
            self._values["cases"] = cases

    @builtins.property
    def cases(self) -> typing.Optional[builtins.str]:
        '''A JSON encoded list of cascading if-else conditions.

        Cases are mutually exclusive. The first one with a matching condition is selected, all the rest ignored.
        See `Case <https://cloud.google.com/dialogflow/cx/docs/reference/rest/v3/Fulfillment#case>`_ for the schema.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#cases DialogflowCxFlow#cases}
        '''
        result = self._values.get("cases")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCasesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCasesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__53eb80aecaebdc977458e713ce1211a5d9197ca95c46427439048463cbf8f52f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCasesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6975b6891a26309aae4b0e4f683822cb64663f270f76644b88854dcb059cabb2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCasesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63ba6d1536101f03b92a46f6803159e214e5909a23a21ed8235423001737c1ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ddaaa7fb89bac7db1d8150f44aef6f06eea2ab5b4a65189a60dd44733bb60d03)
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
            type_hints = typing.get_type_hints(_typecheckingstub__082baee0cf4c238f4dce7f51bbebdb8b8f2f6c67df3f1320a92855df798dd063)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__045ad4aff7ed78ed574a89ba941e704c091b91be039510be0053ba6a9c700b21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCasesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCasesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__68e1aab357642b4a2c1af950961e0062a188502923a989d3cc1dffed7c5ea929)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCases")
    def reset_cases(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCases", []))

    @builtins.property
    @jsii.member(jsii_name="casesInput")
    def cases_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "casesInput"))

    @builtins.property
    @jsii.member(jsii_name="cases")
    def cases(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cases"))

    @cases.setter
    def cases(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59ba510c502f90182dd312e64c7b31f12c037a66f6fe0227d125ffbdfb8dcb8e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cases", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6566bf124b85c9a06c7e0d30ba9c7b9c4ce57eab088d905acbeecb6de9d52618)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages",
    jsii_struct_bases=[],
    name_mapping={
        "channel": "channel",
        "conversation_success": "conversationSuccess",
        "live_agent_handoff": "liveAgentHandoff",
        "output_audio_text": "outputAudioText",
        "payload": "payload",
        "play_audio": "playAudio",
        "telephony_transfer_call": "telephonyTransferCall",
        "text": "text",
    },
)
class DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages:
    def __init__(
        self,
        *,
        channel: typing.Optional[builtins.str] = None,
        conversation_success: typing.Optional[typing.Union["DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccess", typing.Dict[builtins.str, typing.Any]]] = None,
        live_agent_handoff: typing.Optional[typing.Union["DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoff", typing.Dict[builtins.str, typing.Any]]] = None,
        output_audio_text: typing.Optional[typing.Union["DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioText", typing.Dict[builtins.str, typing.Any]]] = None,
        payload: typing.Optional[builtins.str] = None,
        play_audio: typing.Optional[typing.Union["DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudio", typing.Dict[builtins.str, typing.Any]]] = None,
        telephony_transfer_call: typing.Optional[typing.Union["DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCall", typing.Dict[builtins.str, typing.Any]]] = None,
        text: typing.Optional[typing.Union["DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesText", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param channel: The channel which the response is associated with. Clients can specify the channel via QueryParameters.channel, and only associated channel response will be returned. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#channel DialogflowCxFlow#channel}
        :param conversation_success: conversation_success block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#conversation_success DialogflowCxFlow#conversation_success}
        :param live_agent_handoff: live_agent_handoff block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#live_agent_handoff DialogflowCxFlow#live_agent_handoff}
        :param output_audio_text: output_audio_text block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#output_audio_text DialogflowCxFlow#output_audio_text}
        :param payload: A custom, platform-specific payload. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#payload DialogflowCxFlow#payload}
        :param play_audio: play_audio block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#play_audio DialogflowCxFlow#play_audio}
        :param telephony_transfer_call: telephony_transfer_call block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#telephony_transfer_call DialogflowCxFlow#telephony_transfer_call}
        :param text: text block. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#text DialogflowCxFlow#text}
        '''
        if isinstance(conversation_success, dict):
            conversation_success = DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccess(**conversation_success)
        if isinstance(live_agent_handoff, dict):
            live_agent_handoff = DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoff(**live_agent_handoff)
        if isinstance(output_audio_text, dict):
            output_audio_text = DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioText(**output_audio_text)
        if isinstance(play_audio, dict):
            play_audio = DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudio(**play_audio)
        if isinstance(telephony_transfer_call, dict):
            telephony_transfer_call = DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCall(**telephony_transfer_call)
        if isinstance(text, dict):
            text = DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesText(**text)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__413c974e061590651241af2a287f53a9f655c73b0f64269e4a2b5810b868a1d2)
            check_type(argname="argument channel", value=channel, expected_type=type_hints["channel"])
            check_type(argname="argument conversation_success", value=conversation_success, expected_type=type_hints["conversation_success"])
            check_type(argname="argument live_agent_handoff", value=live_agent_handoff, expected_type=type_hints["live_agent_handoff"])
            check_type(argname="argument output_audio_text", value=output_audio_text, expected_type=type_hints["output_audio_text"])
            check_type(argname="argument payload", value=payload, expected_type=type_hints["payload"])
            check_type(argname="argument play_audio", value=play_audio, expected_type=type_hints["play_audio"])
            check_type(argname="argument telephony_transfer_call", value=telephony_transfer_call, expected_type=type_hints["telephony_transfer_call"])
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if channel is not None:
            self._values["channel"] = channel
        if conversation_success is not None:
            self._values["conversation_success"] = conversation_success
        if live_agent_handoff is not None:
            self._values["live_agent_handoff"] = live_agent_handoff
        if output_audio_text is not None:
            self._values["output_audio_text"] = output_audio_text
        if payload is not None:
            self._values["payload"] = payload
        if play_audio is not None:
            self._values["play_audio"] = play_audio
        if telephony_transfer_call is not None:
            self._values["telephony_transfer_call"] = telephony_transfer_call
        if text is not None:
            self._values["text"] = text

    @builtins.property
    def channel(self) -> typing.Optional[builtins.str]:
        '''The channel which the response is associated with.

        Clients can specify the channel via QueryParameters.channel, and only associated channel response will be returned.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#channel DialogflowCxFlow#channel}
        '''
        result = self._values.get("channel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def conversation_success(
        self,
    ) -> typing.Optional["DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccess"]:
        '''conversation_success block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#conversation_success DialogflowCxFlow#conversation_success}
        '''
        result = self._values.get("conversation_success")
        return typing.cast(typing.Optional["DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccess"], result)

    @builtins.property
    def live_agent_handoff(
        self,
    ) -> typing.Optional["DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoff"]:
        '''live_agent_handoff block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#live_agent_handoff DialogflowCxFlow#live_agent_handoff}
        '''
        result = self._values.get("live_agent_handoff")
        return typing.cast(typing.Optional["DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoff"], result)

    @builtins.property
    def output_audio_text(
        self,
    ) -> typing.Optional["DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioText"]:
        '''output_audio_text block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#output_audio_text DialogflowCxFlow#output_audio_text}
        '''
        result = self._values.get("output_audio_text")
        return typing.cast(typing.Optional["DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioText"], result)

    @builtins.property
    def payload(self) -> typing.Optional[builtins.str]:
        '''A custom, platform-specific payload.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#payload DialogflowCxFlow#payload}
        '''
        result = self._values.get("payload")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def play_audio(
        self,
    ) -> typing.Optional["DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudio"]:
        '''play_audio block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#play_audio DialogflowCxFlow#play_audio}
        '''
        result = self._values.get("play_audio")
        return typing.cast(typing.Optional["DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudio"], result)

    @builtins.property
    def telephony_transfer_call(
        self,
    ) -> typing.Optional["DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCall"]:
        '''telephony_transfer_call block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#telephony_transfer_call DialogflowCxFlow#telephony_transfer_call}
        '''
        result = self._values.get("telephony_transfer_call")
        return typing.cast(typing.Optional["DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCall"], result)

    @builtins.property
    def text(
        self,
    ) -> typing.Optional["DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesText"]:
        '''text block.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#text DialogflowCxFlow#text}
        '''
        result = self._values.get("text")
        return typing.cast(typing.Optional["DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesText"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccess",
    jsii_struct_bases=[],
    name_mapping={"metadata": "metadata"},
)
class DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccess:
    def __init__(self, *, metadata: typing.Optional[builtins.str] = None) -> None:
        '''
        :param metadata: Custom metadata. Dialogflow doesn't impose any structure on this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#metadata DialogflowCxFlow#metadata}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0011078f8283a463693b104af4cb53fd6f57ad35fcc60409af13c66c05203a03)
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metadata is not None:
            self._values["metadata"] = metadata

    @builtins.property
    def metadata(self) -> typing.Optional[builtins.str]:
        '''Custom metadata. Dialogflow doesn't impose any structure on this.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#metadata DialogflowCxFlow#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccess(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccessOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccessOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__aebde3d6b786f7fb58c0fc624e474d1ceccff553080c0e0d82b7a65e86dd7fd8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7920e29938be69336c24266a87cfdfcc85815a7ea5ac92624a2b810fbf56580b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccess]:
        return typing.cast(typing.Optional[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccess], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccess],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdcd5691d5c19487ed86585c88347b33448666d92a21a2c7c79b401c682996a8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8192a13205eca13f083f8cbaa79f0dc9b6d1e4fa15ca554e41c6ae909cb720a1)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b374800fdc47f1349d076c5a42b34da49b2a53764cff70f8d87cfc388988e709)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f9d42ed41405d4cef6fd637f62e5e6cf391942939430256eb8e3e220d7fc310)
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
            type_hints = typing.get_type_hints(_typecheckingstub__76d126d757a871096275a3dfc877d3a40f7764e2c09b6ae5519e5ad9b3496f00)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3cac1549a88958d1238388447bed80774e4b46f9c1b346139fa87f217bd4872)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c24ce82fe152e1eee77a18287382275227eb4bced1214e28723a9a22c58370e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoff",
    jsii_struct_bases=[],
    name_mapping={"metadata": "metadata"},
)
class DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoff:
    def __init__(self, *, metadata: typing.Optional[builtins.str] = None) -> None:
        '''
        :param metadata: Custom metadata. Dialogflow doesn't impose any structure on this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#metadata DialogflowCxFlow#metadata}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__263ebc099831bbd840b4132efec9622802980c77d9827f01d5d33003792d9b42)
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if metadata is not None:
            self._values["metadata"] = metadata

    @builtins.property
    def metadata(self) -> typing.Optional[builtins.str]:
        '''Custom metadata. Dialogflow doesn't impose any structure on this.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#metadata DialogflowCxFlow#metadata}
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoff(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoffOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoffOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8ec8c9943604e779f0940933bee206a72bf6603240d6220b60014787275542f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetMetadata")
    def reset_metadata(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMetadata", []))

    @builtins.property
    @jsii.member(jsii_name="metadataInput")
    def metadata_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "metadataInput"))

    @builtins.property
    @jsii.member(jsii_name="metadata")
    def metadata(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "metadata"))

    @metadata.setter
    def metadata(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14cb60f0f3e24b38467262c77f715efb3f292070031d7a718dfa620bea13dd33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "metadata", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoff]:
        return typing.cast(typing.Optional[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoff], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoff],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fe6d2f0baeadbbc5d8c562002baeae65ecc50a36251268e289db5fb68995cb8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioText",
    jsii_struct_bases=[],
    name_mapping={"ssml": "ssml", "text": "text"},
)
class DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioText:
    def __init__(
        self,
        *,
        ssml: typing.Optional[builtins.str] = None,
        text: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ssml: The SSML text to be synthesized. For more information, see SSML. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#ssml DialogflowCxFlow#ssml}
        :param text: The raw text to be synthesized. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#text DialogflowCxFlow#text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de52003c4343cc910bdf4518f1bc3c0030e333624f4a1f6f1c2b73a89e47ed3d)
            check_type(argname="argument ssml", value=ssml, expected_type=type_hints["ssml"])
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ssml is not None:
            self._values["ssml"] = ssml
        if text is not None:
            self._values["text"] = text

    @builtins.property
    def ssml(self) -> typing.Optional[builtins.str]:
        '''The SSML text to be synthesized. For more information, see SSML.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#ssml DialogflowCxFlow#ssml}
        '''
        result = self._values.get("ssml")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def text(self) -> typing.Optional[builtins.str]:
        '''The raw text to be synthesized.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#text DialogflowCxFlow#text}
        '''
        result = self._values.get("text")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioText(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioTextOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioTextOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__02e7b04aa0d39484466a38ea15e484490d84947b0ff55bb85f38198b865fb357)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetSsml")
    def reset_ssml(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSsml", []))

    @jsii.member(jsii_name="resetText")
    def reset_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetText", []))

    @builtins.property
    @jsii.member(jsii_name="allowPlaybackInterruption")
    def allow_playback_interruption(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "allowPlaybackInterruption"))

    @builtins.property
    @jsii.member(jsii_name="ssmlInput")
    def ssml_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ssmlInput"))

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="ssml")
    def ssml(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ssml"))

    @ssml.setter
    def ssml(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22f9f20d6b443763325e39c6b070b38053ced09c5e2cb8812ca5a3a6a20a7ce0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ssml", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "text"))

    @text.setter
    def text(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ae069b1e14d19141dcb345241d9a75f2604b57b78d6ddf127ed5eb1c1a8d7de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioText]:
        return typing.cast(typing.Optional[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioText], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioText],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8542797ccc3fb3abd92a8d8abc23e38a569c39fc642155c7c27bbf6978edf1b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cac5cdbfa0b61ce6540cc4fb8e9af75c75f33c781b00e858f303ff672ab0e25d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putConversationSuccess")
    def put_conversation_success(
        self,
        *,
        metadata: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param metadata: Custom metadata. Dialogflow doesn't impose any structure on this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#metadata DialogflowCxFlow#metadata}
        '''
        value = DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccess(
            metadata=metadata
        )

        return typing.cast(None, jsii.invoke(self, "putConversationSuccess", [value]))

    @jsii.member(jsii_name="putLiveAgentHandoff")
    def put_live_agent_handoff(
        self,
        *,
        metadata: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param metadata: Custom metadata. Dialogflow doesn't impose any structure on this. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#metadata DialogflowCxFlow#metadata}
        '''
        value = DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoff(
            metadata=metadata
        )

        return typing.cast(None, jsii.invoke(self, "putLiveAgentHandoff", [value]))

    @jsii.member(jsii_name="putOutputAudioText")
    def put_output_audio_text(
        self,
        *,
        ssml: typing.Optional[builtins.str] = None,
        text: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param ssml: The SSML text to be synthesized. For more information, see SSML. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#ssml DialogflowCxFlow#ssml}
        :param text: The raw text to be synthesized. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#text DialogflowCxFlow#text}
        '''
        value = DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioText(
            ssml=ssml, text=text
        )

        return typing.cast(None, jsii.invoke(self, "putOutputAudioText", [value]))

    @jsii.member(jsii_name="putPlayAudio")
    def put_play_audio(self, *, audio_uri: builtins.str) -> None:
        '''
        :param audio_uri: URI of the audio clip. Dialogflow does not impose any validation on this value. It is specific to the client that reads it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#audio_uri DialogflowCxFlow#audio_uri}
        '''
        value = DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudio(
            audio_uri=audio_uri
        )

        return typing.cast(None, jsii.invoke(self, "putPlayAudio", [value]))

    @jsii.member(jsii_name="putTelephonyTransferCall")
    def put_telephony_transfer_call(self, *, phone_number: builtins.str) -> None:
        '''
        :param phone_number: Transfer the call to a phone number in E.164 format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#phone_number DialogflowCxFlow#phone_number}
        '''
        value = DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCall(
            phone_number=phone_number
        )

        return typing.cast(None, jsii.invoke(self, "putTelephonyTransferCall", [value]))

    @jsii.member(jsii_name="putText")
    def put_text(
        self,
        *,
        text: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param text: A collection of text responses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#text DialogflowCxFlow#text}
        '''
        value = DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesText(
            text=text
        )

        return typing.cast(None, jsii.invoke(self, "putText", [value]))

    @jsii.member(jsii_name="resetChannel")
    def reset_channel(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetChannel", []))

    @jsii.member(jsii_name="resetConversationSuccess")
    def reset_conversation_success(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConversationSuccess", []))

    @jsii.member(jsii_name="resetLiveAgentHandoff")
    def reset_live_agent_handoff(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLiveAgentHandoff", []))

    @jsii.member(jsii_name="resetOutputAudioText")
    def reset_output_audio_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOutputAudioText", []))

    @jsii.member(jsii_name="resetPayload")
    def reset_payload(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPayload", []))

    @jsii.member(jsii_name="resetPlayAudio")
    def reset_play_audio(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPlayAudio", []))

    @jsii.member(jsii_name="resetTelephonyTransferCall")
    def reset_telephony_transfer_call(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTelephonyTransferCall", []))

    @jsii.member(jsii_name="resetText")
    def reset_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetText", []))

    @builtins.property
    @jsii.member(jsii_name="conversationSuccess")
    def conversation_success(
        self,
    ) -> DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccessOutputReference:
        return typing.cast(DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccessOutputReference, jsii.get(self, "conversationSuccess"))

    @builtins.property
    @jsii.member(jsii_name="liveAgentHandoff")
    def live_agent_handoff(
        self,
    ) -> DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoffOutputReference:
        return typing.cast(DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoffOutputReference, jsii.get(self, "liveAgentHandoff"))

    @builtins.property
    @jsii.member(jsii_name="outputAudioText")
    def output_audio_text(
        self,
    ) -> DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioTextOutputReference:
        return typing.cast(DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioTextOutputReference, jsii.get(self, "outputAudioText"))

    @builtins.property
    @jsii.member(jsii_name="playAudio")
    def play_audio(
        self,
    ) -> "DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudioOutputReference":
        return typing.cast("DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudioOutputReference", jsii.get(self, "playAudio"))

    @builtins.property
    @jsii.member(jsii_name="telephonyTransferCall")
    def telephony_transfer_call(
        self,
    ) -> "DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCallOutputReference":
        return typing.cast("DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCallOutputReference", jsii.get(self, "telephonyTransferCall"))

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(
        self,
    ) -> "DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTextOutputReference":
        return typing.cast("DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTextOutputReference", jsii.get(self, "text"))

    @builtins.property
    @jsii.member(jsii_name="channelInput")
    def channel_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "channelInput"))

    @builtins.property
    @jsii.member(jsii_name="conversationSuccessInput")
    def conversation_success_input(
        self,
    ) -> typing.Optional[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccess]:
        return typing.cast(typing.Optional[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccess], jsii.get(self, "conversationSuccessInput"))

    @builtins.property
    @jsii.member(jsii_name="liveAgentHandoffInput")
    def live_agent_handoff_input(
        self,
    ) -> typing.Optional[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoff]:
        return typing.cast(typing.Optional[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoff], jsii.get(self, "liveAgentHandoffInput"))

    @builtins.property
    @jsii.member(jsii_name="outputAudioTextInput")
    def output_audio_text_input(
        self,
    ) -> typing.Optional[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioText]:
        return typing.cast(typing.Optional[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioText], jsii.get(self, "outputAudioTextInput"))

    @builtins.property
    @jsii.member(jsii_name="payloadInput")
    def payload_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "payloadInput"))

    @builtins.property
    @jsii.member(jsii_name="playAudioInput")
    def play_audio_input(
        self,
    ) -> typing.Optional["DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudio"]:
        return typing.cast(typing.Optional["DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudio"], jsii.get(self, "playAudioInput"))

    @builtins.property
    @jsii.member(jsii_name="telephonyTransferCallInput")
    def telephony_transfer_call_input(
        self,
    ) -> typing.Optional["DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCall"]:
        return typing.cast(typing.Optional["DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCall"], jsii.get(self, "telephonyTransferCallInput"))

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(
        self,
    ) -> typing.Optional["DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesText"]:
        return typing.cast(typing.Optional["DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesText"], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="channel")
    def channel(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "channel"))

    @channel.setter
    def channel(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e1fb905760292a1cedd4024ce20beba99b26e0fbec2f608ce875e95ad4db49e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channel", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="payload")
    def payload(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "payload"))

    @payload.setter
    def payload(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7712d791bdf72cdda80b0f882b00a82c6a63653fe25bee8d0346fbe567623e12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "payload", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2c69dee255f57ff09ac8b552a26bba1aa4b4165419c5d1c164fbc8281f93861)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudio",
    jsii_struct_bases=[],
    name_mapping={"audio_uri": "audioUri"},
)
class DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudio:
    def __init__(self, *, audio_uri: builtins.str) -> None:
        '''
        :param audio_uri: URI of the audio clip. Dialogflow does not impose any validation on this value. It is specific to the client that reads it. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#audio_uri DialogflowCxFlow#audio_uri}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__744a97e2329f1385bef3b89046c9e2e502dec77c1ff68a1433153cbd1828a140)
            check_type(argname="argument audio_uri", value=audio_uri, expected_type=type_hints["audio_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "audio_uri": audio_uri,
        }

    @builtins.property
    def audio_uri(self) -> builtins.str:
        '''URI of the audio clip.

        Dialogflow does not impose any validation on this value. It is specific to the client that reads it.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#audio_uri DialogflowCxFlow#audio_uri}
        '''
        result = self._values.get("audio_uri")
        assert result is not None, "Required property 'audio_uri' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudio(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudioOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudioOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0753cb4645ea63213033758a7b35baac350f608a808b4ef6296de0746049d7be)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="allowPlaybackInterruption")
    def allow_playback_interruption(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "allowPlaybackInterruption"))

    @builtins.property
    @jsii.member(jsii_name="audioUriInput")
    def audio_uri_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "audioUriInput"))

    @builtins.property
    @jsii.member(jsii_name="audioUri")
    def audio_uri(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "audioUri"))

    @audio_uri.setter
    def audio_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22f59ad2b37fc9b6f711d58851e8ffef2390cf5936938a0bdfb0f7389619d30b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "audioUri", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudio]:
        return typing.cast(typing.Optional[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudio], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudio],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86714793efcedd83cbf58515c7954820244b6cc5de54b742a58d8b2b54b7d1f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCall",
    jsii_struct_bases=[],
    name_mapping={"phone_number": "phoneNumber"},
)
class DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCall:
    def __init__(self, *, phone_number: builtins.str) -> None:
        '''
        :param phone_number: Transfer the call to a phone number in E.164 format. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#phone_number DialogflowCxFlow#phone_number}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcc631c62f835ad7ef815276cbed7772c0821925e93e0fc4fdb3592f846d1338)
            check_type(argname="argument phone_number", value=phone_number, expected_type=type_hints["phone_number"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "phone_number": phone_number,
        }

    @builtins.property
    def phone_number(self) -> builtins.str:
        '''Transfer the call to a phone number in E.164 format.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#phone_number DialogflowCxFlow#phone_number}
        '''
        result = self._values.get("phone_number")
        assert result is not None, "Required property 'phone_number' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCall(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCallOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCallOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0738e2e689be00c3099d4344af08b4c77b0ca9d06d7ea36b2216e75c1648a2ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="phoneNumberInput")
    def phone_number_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "phoneNumberInput"))

    @builtins.property
    @jsii.member(jsii_name="phoneNumber")
    def phone_number(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "phoneNumber"))

    @phone_number.setter
    def phone_number(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b949d64290f71f50825ab6970cd92cf85750589d3e7c442ac35c72f006a5d9c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "phoneNumber", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCall]:
        return typing.cast(typing.Optional[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCall], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCall],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b014c3de8de8d10438e1e573db5d9395bc6b6e50953209f6037552c8350f8013)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesText",
    jsii_struct_bases=[],
    name_mapping={"text": "text"},
)
class DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesText:
    def __init__(
        self,
        *,
        text: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param text: A collection of text responses. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#text DialogflowCxFlow#text}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb845cd2e37763a470724a8398ea907a821e78981076ecdb01940c409d1349b2)
            check_type(argname="argument text", value=text, expected_type=type_hints["text"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if text is not None:
            self._values["text"] = text

    @builtins.property
    def text(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A collection of text responses.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#text DialogflowCxFlow#text}
        '''
        result = self._values.get("text")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesText(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTextOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTextOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bb3195addc2e0e2d487a08d2226527582423fc97a2ffb9524e6bce947362e48)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetText")
    def reset_text(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetText", []))

    @builtins.property
    @jsii.member(jsii_name="allowPlaybackInterruption")
    def allow_playback_interruption(self) -> _cdktf_9a9027ec.IResolvable:
        return typing.cast(_cdktf_9a9027ec.IResolvable, jsii.get(self, "allowPlaybackInterruption"))

    @builtins.property
    @jsii.member(jsii_name="textInput")
    def text_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "textInput"))

    @builtins.property
    @jsii.member(jsii_name="text")
    def text(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "text"))

    @text.setter
    def text(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ab99c2979234ff3e742be8fdc1938a88a47aefe67ce81b327a06d1671120302)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "text", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesText]:
        return typing.cast(typing.Optional[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesText], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesText],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5bd9ce82f7c73a35e2a26abf6b7177a060a8f6bab2f680a0232a8af5bcc21cb2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxFlowTransitionRoutesTriggerFulfillmentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowTransitionRoutesTriggerFulfillmentOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__50f80746ca2bb2d342d999743e6969c6f0343890e938ac255799492d66c131a7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putConditionalCases")
    def put_conditional_cases(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6ccfad873224fb7e703149e4980acebb92523eea1edfccf9f1f9ad965822d6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConditionalCases", [value]))

    @jsii.member(jsii_name="putMessages")
    def put_messages(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2c18abe1c3ec735ca9f99216026376e20ee3b108eafa6bbb29c971cc5bd2b7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putMessages", [value]))

    @jsii.member(jsii_name="putSetParameterActions")
    def put_set_parameter_actions(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9790f63e641f9957e62f860d291c3822699db77109e0304effc128e728391c8d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSetParameterActions", [value]))

    @jsii.member(jsii_name="resetConditionalCases")
    def reset_conditional_cases(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConditionalCases", []))

    @jsii.member(jsii_name="resetMessages")
    def reset_messages(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMessages", []))

    @jsii.member(jsii_name="resetReturnPartialResponses")
    def reset_return_partial_responses(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReturnPartialResponses", []))

    @jsii.member(jsii_name="resetSetParameterActions")
    def reset_set_parameter_actions(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSetParameterActions", []))

    @jsii.member(jsii_name="resetTag")
    def reset_tag(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTag", []))

    @jsii.member(jsii_name="resetWebhook")
    def reset_webhook(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebhook", []))

    @builtins.property
    @jsii.member(jsii_name="conditionalCases")
    def conditional_cases(
        self,
    ) -> DialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCasesList:
        return typing.cast(DialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCasesList, jsii.get(self, "conditionalCases"))

    @builtins.property
    @jsii.member(jsii_name="messages")
    def messages(
        self,
    ) -> DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesList:
        return typing.cast(DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesList, jsii.get(self, "messages"))

    @builtins.property
    @jsii.member(jsii_name="setParameterActions")
    def set_parameter_actions(
        self,
    ) -> "DialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActionsList":
        return typing.cast("DialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActionsList", jsii.get(self, "setParameterActions"))

    @builtins.property
    @jsii.member(jsii_name="conditionalCasesInput")
    def conditional_cases_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases]]], jsii.get(self, "conditionalCasesInput"))

    @builtins.property
    @jsii.member(jsii_name="messagesInput")
    def messages_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages]]], jsii.get(self, "messagesInput"))

    @builtins.property
    @jsii.member(jsii_name="returnPartialResponsesInput")
    def return_partial_responses_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "returnPartialResponsesInput"))

    @builtins.property
    @jsii.member(jsii_name="setParameterActionsInput")
    def set_parameter_actions_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions"]]], jsii.get(self, "setParameterActionsInput"))

    @builtins.property
    @jsii.member(jsii_name="tagInput")
    def tag_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tagInput"))

    @builtins.property
    @jsii.member(jsii_name="webhookInput")
    def webhook_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "webhookInput"))

    @builtins.property
    @jsii.member(jsii_name="returnPartialResponses")
    def return_partial_responses(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "returnPartialResponses"))

    @return_partial_responses.setter
    def return_partial_responses(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c04e9ab05a22fd9648c58b89f1efbece6d247a46eb520ee5d36b36f1b6db89b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "returnPartialResponses", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="tag")
    def tag(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tag"))

    @tag.setter
    def tag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__497871d2c57e5396079000d24da65292ac39b0a38ca44b60f20a65cd0f35283d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tag", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="webhook")
    def webhook(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "webhook"))

    @webhook.setter
    def webhook(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fde07765771fec4879fbf618b893f6a10dd429a1eb438b5d605e0e9721a51e47)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webhook", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[DialogflowCxFlowTransitionRoutesTriggerFulfillment]:
        return typing.cast(typing.Optional[DialogflowCxFlowTransitionRoutesTriggerFulfillment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DialogflowCxFlowTransitionRoutesTriggerFulfillment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a201d5f48b8c6c3b824c2d57cb88352f3451f830f8a4a70a15c5803fff4f07c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


@jsii.data_type(
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions",
    jsii_struct_bases=[],
    name_mapping={"parameter": "parameter", "value": "value"},
)
class DialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions:
    def __init__(
        self,
        *,
        parameter: typing.Optional[builtins.str] = None,
        value: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param parameter: Display name of the parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#parameter DialogflowCxFlow#parameter}
        :param value: The new JSON-encoded value of the parameter. A null value clears the parameter. Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#value DialogflowCxFlow#value}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__589eceda523524f13fe19631e4db8792050eab8dc58503d29264b706cb0b6637)
            check_type(argname="argument parameter", value=parameter, expected_type=type_hints["parameter"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if parameter is not None:
            self._values["parameter"] = parameter
        if value is not None:
            self._values["value"] = value

    @builtins.property
    def parameter(self) -> typing.Optional[builtins.str]:
        '''Display name of the parameter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#parameter DialogflowCxFlow#parameter}
        '''
        result = self._values.get("parameter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def value(self) -> typing.Optional[builtins.str]:
        '''The new JSON-encoded value of the parameter. A null value clears the parameter.

        Docs at Terraform Registry: {@link https://registry.terraform.io/providers/hashicorp/google/6.32.0/docs/resources/dialogflow_cx_flow#value DialogflowCxFlow#value}
        '''
        result = self._values.get("value")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActionsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActionsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c353701b6c3c0e8acf0abdb15264ffb9edd25f033c864483984b623ed106cd3f)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActionsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3b36ca47ac7365c6e7c55a0ef592d558a8ef7a8ec5a4f6c2e1e5fa8c5fb5ff0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActionsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__def58bef9966a207c9c703b8ec2321b8a2831f47d2337293d61d653ac0f7e9d6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f33a8785ae8434267d4d07d54c8a74b98d73edf1be9a76c946facdf288051cd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ebfccda72b98bf46c2c69eeaa66d8ba40dac255b607b60a2238d42c40b6ae4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8472bb65c6bc30a762612a16bf446b1d06ed6789d3891d11c6f994b42afb972)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


class DialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActionsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-google.dialogflowCxFlow.DialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActionsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6caa385393286452cae36cc7267b261b2fe18b80e62c69532a0790d85d5e0175)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetParameter")
    def reset_parameter(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetParameter", []))

    @jsii.member(jsii_name="resetValue")
    def reset_value(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetValue", []))

    @builtins.property
    @jsii.member(jsii_name="parameterInput")
    def parameter_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "parameterInput"))

    @builtins.property
    @jsii.member(jsii_name="valueInput")
    def value_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "valueInput"))

    @builtins.property
    @jsii.member(jsii_name="parameter")
    def parameter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "parameter"))

    @parameter.setter
    def parameter(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89abbc011e555bc638fb714f4f783bbd80015ffef425876a2a0563a4a454b2e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "parameter", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="value")
    def value(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "value"))

    @value.setter
    def value(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__997cb4c9dcf6831288c057ec107467e43fe46e542fb1739f579933174051a809)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "value", value) # pyright: ignore[reportArgumentType]

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db15b3ee1da1ce6e9fa2e5584513aa7e497a276e5da0af847d945d73328a683d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value) # pyright: ignore[reportArgumentType]


__all__ = [
    "DialogflowCxFlow",
    "DialogflowCxFlowAdvancedSettings",
    "DialogflowCxFlowAdvancedSettingsAudioExportGcsDestination",
    "DialogflowCxFlowAdvancedSettingsAudioExportGcsDestinationOutputReference",
    "DialogflowCxFlowAdvancedSettingsDtmfSettings",
    "DialogflowCxFlowAdvancedSettingsDtmfSettingsOutputReference",
    "DialogflowCxFlowAdvancedSettingsLoggingSettings",
    "DialogflowCxFlowAdvancedSettingsLoggingSettingsOutputReference",
    "DialogflowCxFlowAdvancedSettingsOutputReference",
    "DialogflowCxFlowAdvancedSettingsSpeechSettings",
    "DialogflowCxFlowAdvancedSettingsSpeechSettingsOutputReference",
    "DialogflowCxFlowConfig",
    "DialogflowCxFlowEventHandlers",
    "DialogflowCxFlowEventHandlersList",
    "DialogflowCxFlowEventHandlersOutputReference",
    "DialogflowCxFlowEventHandlersTriggerFulfillment",
    "DialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases",
    "DialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCasesList",
    "DialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCasesOutputReference",
    "DialogflowCxFlowEventHandlersTriggerFulfillmentMessages",
    "DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccess",
    "DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccessOutputReference",
    "DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesList",
    "DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoff",
    "DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoffOutputReference",
    "DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioText",
    "DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioTextOutputReference",
    "DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputReference",
    "DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudio",
    "DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudioOutputReference",
    "DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCall",
    "DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCallOutputReference",
    "DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesText",
    "DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTextOutputReference",
    "DialogflowCxFlowEventHandlersTriggerFulfillmentOutputReference",
    "DialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions",
    "DialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActionsList",
    "DialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActionsOutputReference",
    "DialogflowCxFlowNluSettings",
    "DialogflowCxFlowNluSettingsOutputReference",
    "DialogflowCxFlowTimeouts",
    "DialogflowCxFlowTimeoutsOutputReference",
    "DialogflowCxFlowTransitionRoutes",
    "DialogflowCxFlowTransitionRoutesList",
    "DialogflowCxFlowTransitionRoutesOutputReference",
    "DialogflowCxFlowTransitionRoutesTriggerFulfillment",
    "DialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases",
    "DialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCasesList",
    "DialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCasesOutputReference",
    "DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages",
    "DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccess",
    "DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccessOutputReference",
    "DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesList",
    "DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoff",
    "DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoffOutputReference",
    "DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioText",
    "DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioTextOutputReference",
    "DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputReference",
    "DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudio",
    "DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudioOutputReference",
    "DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCall",
    "DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCallOutputReference",
    "DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesText",
    "DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTextOutputReference",
    "DialogflowCxFlowTransitionRoutesTriggerFulfillmentOutputReference",
    "DialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions",
    "DialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActionsList",
    "DialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActionsOutputReference",
]

publication.publish()

def _typecheckingstub__b4e73e5829492f4b7c2b1b1017035124904b70f6aaa69feef28577dda886dac1(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    display_name: builtins.str,
    advanced_settings: typing.Optional[typing.Union[DialogflowCxFlowAdvancedSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    event_handlers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxFlowEventHandlers, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    is_default_start_flow: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    language_code: typing.Optional[builtins.str] = None,
    nlu_settings: typing.Optional[typing.Union[DialogflowCxFlowNluSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    parent: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DialogflowCxFlowTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    transition_route_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    transition_routes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxFlowTransitionRoutes, typing.Dict[builtins.str, typing.Any]]]]] = None,
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

def _typecheckingstub__105eab4b14fc64d76802f265d1eccee4dd95fbb5e5df56075da5c2f7c3a77b43(
    scope: _constructs_77d1e7e8.Construct,
    import_to_id: builtins.str,
    import_from_id: builtins.str,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b2d6f4b8ef64342efd63479e223269d4b954d60379aa3315bdc10447d23bd35(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxFlowEventHandlers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f440bd7c61584c308c6c0a0c99593338d01255c987529c5d0272b95298a7e6c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxFlowTransitionRoutes, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__525d1f088ad579284f462c890d3748a4be131ff4f772519259c28b3a4d3aabf9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f19abc058b54dda393df616ce73c27289c65f807d5d312f0760e42bce485caf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01076f612e6da6ee8f18b9e0bde62fbf9296a44f0a3329ebf4ff53ca393e4ffa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01320d262ebc1f160629cf8be936052075f8afd7b1ae7fd48057af3152a3c993(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5379073eaf2e87a76c466120e1cbf87fbfd737b2da6b001ef586b29bc520cbf6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0181a58dd91713b849c24f7f4fda2b0a0e008a48c4013ab789945d642cad2258(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaabe2288b76fe02b5c18080b38e8b4453f0b959296809fde3759f04688ec0e7(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfefb8ec518d9026c8905a4832dadaec06430a5c8d3aa5016526dc71eaddc47e(
    *,
    audio_export_gcs_destination: typing.Optional[typing.Union[DialogflowCxFlowAdvancedSettingsAudioExportGcsDestination, typing.Dict[builtins.str, typing.Any]]] = None,
    dtmf_settings: typing.Optional[typing.Union[DialogflowCxFlowAdvancedSettingsDtmfSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    logging_settings: typing.Optional[typing.Union[DialogflowCxFlowAdvancedSettingsLoggingSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    speech_settings: typing.Optional[typing.Union[DialogflowCxFlowAdvancedSettingsSpeechSettings, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e29a4430913b6606df161e07647e8076057de74748be7d7f0ffaf2e71a24845(
    *,
    uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57ccb8e40b99abde8aee45a11d6815452ded2ab5f9ad1a6b2b21c3dbd3d14257(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df6d40f2b1fcfa3a1dd196b449788081e0694c9f3779cde481a1c453a52cee85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8aaf8ee94304476848778879268b62fb8fd019b09cd22f9099f39ca1c77edc0(
    value: typing.Optional[DialogflowCxFlowAdvancedSettingsAudioExportGcsDestination],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a00d02b7c456dd8806f50fc0d5ddaa2074ed8a2ec5cb425b475665c291d697b(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    finish_digit: typing.Optional[builtins.str] = None,
    max_digits: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__462254d3a984c27bb0ddf3e10b53f20939a5b509c4d1f770a4ff44730b58bf03(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__680d6897703a4dd204a21b8e5a16a6cb889f1a11e2337cb773cc4687f5994dd9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52b734b42a24330a3bc824a76c3ec08aeafdecfa200937fe3bdde1a4dcb847d9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63a0e47fe9116524ba93270f6f8ca878a9a676b76aacc14771ce1d02dc30cc95(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6abf0f48df59f456c6c6dc8d9eb990cd90072e4813fb8eb81fd38882758258a5(
    value: typing.Optional[DialogflowCxFlowAdvancedSettingsDtmfSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11b3b6c253d323bfaf741b86cad4081b2770e88537c935997101bb2f508cf510(
    *,
    enable_consent_based_redaction: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_interaction_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    enable_stackdriver_logging: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__909c323b36405d0486bbe0b2a9e46aa03db93b0626ea77a97a19691f12937caa(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c1134d42da8588f5b85d559510a6f88fd80914c9d28ae7291dfb9ca4263fe66(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bca5f3a4cbc6e055c641a0cb7a51f80d3f60a65cd21ce7aa78cdb90330d412d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88dcdaabb70ceb6a4171ac9b5b22389fbd6e40797b229a3efe015c093a447318(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99419c1994a7ef6965385928a79e1c8bacdec4189b89e5ded3e54e6d0620b11d(
    value: typing.Optional[DialogflowCxFlowAdvancedSettingsLoggingSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8f6c50247c13b454a3a778c246bc91bc3ab8d8a46a4fd205eba2dfe5c54f54e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bd58252b666f55f41d019b8966c0f66468eb934c556ae719d82c08ec33bf0e5(
    value: typing.Optional[DialogflowCxFlowAdvancedSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c370fa592bc682b70446b182d3fea98301a3699655bbf1fc2a5ffa750052e76c(
    *,
    endpointer_sensitivity: typing.Optional[jsii.Number] = None,
    models: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    no_speech_timeout: typing.Optional[builtins.str] = None,
    use_timeout_based_endpointing: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__243fc480c5151a77c0ba714f54f731557a5e1bf5d6c5e6d6b9c5e09d1f64d752(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff432305f4fd6da431967093625d49f7ac63584449a22bf609f652bdaac55130(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a647b7599ba415029519e1c57ff23908cba39706dcacfc6ad02e27c3a14965f(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b99781623e16c3999aa375ab1e41aa38c883ac750fa8c1c019e2470cf2e892a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee9666a1838f01e171df77ee5f84135bdba16283a09ea74fc0d350dad848099b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be9e0218babb2169372482a009a54202579bbe50e0b16f823b2c983848e93236(
    value: typing.Optional[DialogflowCxFlowAdvancedSettingsSpeechSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec698bcfeadd51979d5f29ea8d4a0a592a61a165e38fb999ad729592839dee47(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[typing.Union[jsii.Number, _cdktf_9a9027ec.TerraformCount]] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    display_name: builtins.str,
    advanced_settings: typing.Optional[typing.Union[DialogflowCxFlowAdvancedSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    event_handlers: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxFlowEventHandlers, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    is_default_start_flow: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    language_code: typing.Optional[builtins.str] = None,
    nlu_settings: typing.Optional[typing.Union[DialogflowCxFlowNluSettings, typing.Dict[builtins.str, typing.Any]]] = None,
    parent: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[DialogflowCxFlowTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    transition_route_groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    transition_routes: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxFlowTransitionRoutes, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a8050a2a4311e47d08ea1a2ae43816ba636f82ed5e2a86798e2bd58858e0cd3(
    *,
    event: typing.Optional[builtins.str] = None,
    target_flow: typing.Optional[builtins.str] = None,
    target_page: typing.Optional[builtins.str] = None,
    trigger_fulfillment: typing.Optional[typing.Union[DialogflowCxFlowEventHandlersTriggerFulfillment, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d42939112cfa1221e46883d4e3d76965f5e69c0697aa3b7b334ccbf8426c3d6(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33d35a9d80a7158de74ab6372970bf0ad4e275bb5328969bd8613bcdd35d53d6(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9091b6d2a1ca8403a193f3bf25da330278e125aead455dfc44a54a26c0c3ffc7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f225eff77b3c9853afa47e56d66f22ce1341dcd0b3af4f26f3b64f742be265c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df4af229d9905c8286ed08d12c2be8f1f51b392b40ae79be05c436883edd8d37(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77277aa21281d85989754af45b5d8cb1a5a687b38bb312a2c8bbeceb17ba384b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowEventHandlers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86cb70ea9c34dc73d0d371cd77b5f7efbbe67fc7ff01c6f78ff555b32540cf55(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9c20abfac43e96fad5fbc962ef06fbe421b92453ca8b90f23cbb42a71b354c7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33a50c3ba767c788f6efb6617b4b26e680c7a4d29b5bbf39a077787cbff07401(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12d1230ef8f1746d438bfd6ef148f37a451c3051a77d69b611c748d50ac6a189(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50b90352ac28a01bd24bf21bdd41104d2bbebdabad24d76edb66cfac726ddf1a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowEventHandlers]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e845933aee1763891ad709b181bd0b2a143efbaacda06a9e2b63db9eab9a903(
    *,
    conditional_cases: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases, typing.Dict[builtins.str, typing.Any]]]]] = None,
    messages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxFlowEventHandlersTriggerFulfillmentMessages, typing.Dict[builtins.str, typing.Any]]]]] = None,
    return_partial_responses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    set_parameter_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tag: typing.Optional[builtins.str] = None,
    webhook: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b286635f745e721ea317207f30f8efeb0a8e4cda7ba3f3ebad98f035af3fcfb(
    *,
    cases: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad2f3eb4e45a341e4cc22c6b7efbcfc2b452a308a4d075bcdbe92a821641dbe(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56ca45e914117151278f67fa9f6db512ac74e7c12bae523164211d037ac673dd(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a933841b84a1c19d0e1a71f5677c047eb87ff461ccdd57d256132d2e9e69f197(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__270355a735d469304e3d0af55fce009bc353f5c845b2401d52bf94dfacd7f7a8(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d5579fb18d1f1683c76726132688a0d5530cc4ae99b76f7317ec24ad40c385d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aeab8f21464d92487d7d7746cbf3255c2d11a84114ffbf5878241a34d1b7be6f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec12073354401977999305c2466f9bfbeed413fa283276ae466a16bca979f635(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b7187f78cd597ef0b25cd779485532cc09efd7289b3ad2ebf0db3d0dea9a29d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84068fca10acd7aae87e4f01967ed5b9a179bb7f03374d68aa13b22d4424ab85(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8807fb19dc54302a5b8791edb5637a83298aee765bf6b45fda2334ee73f245a7(
    *,
    channel: typing.Optional[builtins.str] = None,
    conversation_success: typing.Optional[typing.Union[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccess, typing.Dict[builtins.str, typing.Any]]] = None,
    live_agent_handoff: typing.Optional[typing.Union[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoff, typing.Dict[builtins.str, typing.Any]]] = None,
    output_audio_text: typing.Optional[typing.Union[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioText, typing.Dict[builtins.str, typing.Any]]] = None,
    payload: typing.Optional[builtins.str] = None,
    play_audio: typing.Optional[typing.Union[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudio, typing.Dict[builtins.str, typing.Any]]] = None,
    telephony_transfer_call: typing.Optional[typing.Union[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCall, typing.Dict[builtins.str, typing.Any]]] = None,
    text: typing.Optional[typing.Union[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesText, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba3823e96e2872ade15a730fbb317cd7584cb4e2641e3bc774f386111a5eac98(
    *,
    metadata: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82a718517447c53db1a23f87dbd9d124ffe396f30cb2a775057d32b8e5f71ed4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c82dea188a395ac5cb800f51b563df52ca42b2960f6ff1490d0a89178608be26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88c003cbbcb4e38bb63b5ba8bffc577b7b969685eff3117efcdf26d183450cf5(
    value: typing.Optional[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesConversationSuccess],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21b770448d89ac5ec61108568e4cfe70f38d02c255e25672d651fc27a5084b2f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__262f075c52147f062a1ec860717818d6c406b8e9e77c1c4854e2f59558fda25f(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ade9d6685795e8eb857c8fe31b0c2045737bbd4f324e8fc68d3f43e366ed652(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__490cda8ccf07195d8b7d15f8bef539a94d2a9300089141a5e30d6f6c8e668592(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__347b69d3503d65eb15250a87ce2e7e30566c0542d94b41817c634990e2fb87e0(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fb9e1f2abb770c0b7906f4440d3b4f63387c62c2156443aa7d819443649005d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowEventHandlersTriggerFulfillmentMessages]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0be3bccd08bb404f763dcd6cd11e329dd1969de8ee26456b3e4bf8028e606e4(
    *,
    metadata: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__263875aeb3fdeaff84cc115e695d702b3a2fa7ca60afc64f9200339ec9280e0b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65e5dd53f603d1ab997ef49c121333cc9dc41e608780daa0bb5f6b6e4b98e530(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9438ac86e894e23534dda49ceee92d28045bfcc35630d92a3debedab759d8d87(
    value: typing.Optional[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesLiveAgentHandoff],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5294bbdafa3d1437c1e90b17c51b5ffd6b701e31f13d0bf013702a7f1e1b5423(
    *,
    ssml: typing.Optional[builtins.str] = None,
    text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2341b965234e63efabeb4aa660271cd27327448f303fd081dd49bce648670b4b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95bf8580d71992a3436c5af954ee4ffc30c4f6bdfc142a83d258f2bbb08a50ba(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c26ce8483cfba356541e1034f78170e27120f710b05da9b4e17da98f1c69fb9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeecfb0a40db87d164491e6ce4591a3c676ab581b86344ea3c36b721f676f988(
    value: typing.Optional[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesOutputAudioText],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1524c5462e785cdf224f651345c075e4ee93b97de98cfbd3042f9b920ce5542(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53ba97550e4e4d4d5e8f98e87fea663c90ff4b2f79c2bba37be25c824ce5d54a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0873c8bab7c38190bcad107ed6092d6e84880681471cd8c791e91f3f0e8d1277(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff62b63d51d275c5d6f8090162f9e76effd8a6fac20ff5615d088145d1a8a435(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowEventHandlersTriggerFulfillmentMessages]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__402d8129c6fc608a5c28c7d40e6f2ae023b71568c916fdfbd48e1857cc21c4e9(
    *,
    audio_uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cf877dbdcab61dc3ffea4bb8b1199eac9d4d14c6be684eccd7aeac2b3470442(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__244cb35bb11cef20b1fab7883d4424387643ee156d7c767893e3bfa870fd9b27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01301615909f5868a189717124c2b92ded840cbb5506e492a2ce452ccedb8b13(
    value: typing.Optional[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesPlayAudio],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1407e0d2af6f452f0508586857daeec50f0519155533376eb1ab8d717beb8091(
    *,
    phone_number: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fba771409820a4ffc907da640c7cce8da69bba89140b3fb1dcd0b51261b8a2e2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__591d8e7d47e829f08f94b2528022016d929e20be855c72105d6848e00acf4e04(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__104d3ff6aef14cddfe012b1114d4330f2ebe1db07611af97baf367796c168ccc(
    value: typing.Optional[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesTelephonyTransferCall],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdd95e583f0f8e3952133f2d2714eb49bf442d20d97cf76c67da3451d7552bda(
    *,
    text: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57cf17e974838a6242a027dedf66d43786df9575c82a70e064bed3dda836967c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d86bc876f8f99cb85e526b3d3728b33ff0f0688c3ade59490450e925a5e2ae8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__054f059845dc63fe3ff4484c8d63dd0e5661049e8aea5d7a6da7201eedddd55d(
    value: typing.Optional[DialogflowCxFlowEventHandlersTriggerFulfillmentMessagesText],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f256153b78f3197a824e460ce580ddaaed6454618276d329352d9b81f68ee7ba(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe85ef43b4cd5ec3bf7ae9530155742865204d7f38299907b44c593e76dc0f0b(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxFlowEventHandlersTriggerFulfillmentConditionalCases, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21b031f4424f59e1854a021f9239fbd8386770bb851d54a0411fbf40beeb4f7c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxFlowEventHandlersTriggerFulfillmentMessages, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2684484e0e08e5acb5d7486a4df112d4743bd49a548c0bd5355d14731bf562d8(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cba925b43c672643b6fa0e75b060c109ef581b2219659984ff256b7d49a0070(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fc3c0ee598b94116313bbfb910bba4f5eb11f0c83d50237810c05cfa830d916(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1b9bb2275f0b408217bff39ff97c6e1b425df4191dbec32fd4c2756e2a7842e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dec095f27b282c7e7491c82951472e3f5621a882e12b651a948ce6d1e5788a38(
    value: typing.Optional[DialogflowCxFlowEventHandlersTriggerFulfillment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f183a5721eaadf5b77f2882fb66c55fd2d0442a95ea4152d6f9802706591ef99(
    *,
    parameter: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__291c5a3c72a4b275d87d4090f364f8f83a6b56543fefc5f8951d3cb23b57278e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce43729d47de9e0a2248fac37ae0ee9d28586060898863b972bfce5b830d2b15(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04d0bc992af35b41b59a45d6f88fae06f55958881af324821d78aaa53e9c3bf0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5526c6c535ba9e2458425fb60c4df22987bb2bb22b72e3e6d618d4c3eca647d(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6369b9def5bf59a9efde6314945eba95e0a3b3997c31f7709bd55d51d99c25b1(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74bda41ed7f37e89f14f017baf045a4b96bc74b1df5f252c93b0704bf981eca8(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f450a147fbcfa587f875ab74a1e0656a6a9e2d4e6643de75e998bec0028eeefb(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b10305198beb60fa9d7d6c3b9e91c106b9c68d37d3f482b096e449356e834b5d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33fa6f813009dcf12c2aca2c8275db9a4eead2f4440b760ebea83f48bbce3df2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe092cc3c26fba38eb62a11a4bed3fad593d0061def3b0a181561c59e1659372(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowEventHandlersTriggerFulfillmentSetParameterActions]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02f6b106a84e9a588f565581ce95b6d4506e9efe0633a5a30c824027ded98f8e(
    *,
    classification_threshold: typing.Optional[jsii.Number] = None,
    model_training_mode: typing.Optional[builtins.str] = None,
    model_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ecadb1a6ad6fc086ec8e4c48ee7bd4f9c8531e0d1489bb7f76700696043ae20(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c18e3a073f391591d61fb72fbb677ab3870989127160c981f5ee629f9c9eb850(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daa015a12e14b95c8f7cc50e72d8355131e0d6c86bff90e56cc7ca8b859bb4c6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ad70c7b65d59e819484e126777959a67520c66af79f6a95747836b6743a3928(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3ad5e37690e1d5583d17d8ed896e065d40dbb14d7fb295d250b23fb1fb1f81d(
    value: typing.Optional[DialogflowCxFlowNluSettings],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8595441ba1272955ed9d1289461f1ec0cceca2c1250babf980aebbe83f17fce6(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f13b5bbe0d8c6aff2266b7a43514243479d306c23b86c90b0d24dac2e98a97a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f613cc8a6aa58b0cca48cb6853adbb2bab8b9ba79185cc356a03f0fd93feb59f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7dae9783620ec4262dee1dd25877228e67a00c4a5c4a787974b5e74420ffe3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37e9c7689abb731e5baacb5831824aea96a32b5d8e467a97b875794466400837(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0279cd75bdf19b77c9bbdbb7015123e522afc61d5e7c4c3e0e5cc1a2e7f9e2e7(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowTimeouts]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afb349726c9c31ddae7f58a58dde47bafc67004b8e33839114f67981eb49406b(
    *,
    condition: typing.Optional[builtins.str] = None,
    intent: typing.Optional[builtins.str] = None,
    target_flow: typing.Optional[builtins.str] = None,
    target_page: typing.Optional[builtins.str] = None,
    trigger_fulfillment: typing.Optional[typing.Union[DialogflowCxFlowTransitionRoutesTriggerFulfillment, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ed5aba3d1edf1da1e49b8206ead0ab85228fa64d85a06a915277d0eb62c7371(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97cf4cab7e3d08968dacb385e05c3ab3c333bf02b477f756ab68c6e2678f07c1(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c7eb9470a4650390f971e50d8db38f40f3bff8f3e410b6609060e635c3920b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91e39e72c45cff7c250c07f16bc2580ffa3f0df8ad0cddf37517f6c71b075cba(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ac8e5a25899f288f88a8ec3222188a889d782f62f8ae506b72433d61bb02a29(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfca25e7faa60fd92f676604b860dc2478f44d6d7ce64f7a37d0951c4bd735af(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowTransitionRoutes]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__651912c51f88ac2e5df13f68f2a7e8657d71fe8eb3c400bd9b0499fa124becd2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9300f3859e3dce89b25ab991e8d74ad8000436485e9ce180cc81546b8f94aded(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53965fd3d6e2ad491c51bd4a24fb15bb648bfa16e0e93ba4e7660fdfc2c546b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__052a0226286124b80387d0d8b3d805f9b1f88822020a9498b28202e1f32f57cc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__684cffac9909be18e70add392b8cc7970460e54c61600719a7b78d1d2cf89ac3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f94ff6828f6e3d4f466b85bc58a6ba2f3350c4e843273e9bf5c52a87b9d78668(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowTransitionRoutes]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__432893f9cd29f37454ec7f8cbb609d9f910a492bf9c70661909d433841916dbb(
    *,
    conditional_cases: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases, typing.Dict[builtins.str, typing.Any]]]]] = None,
    messages: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages, typing.Dict[builtins.str, typing.Any]]]]] = None,
    return_partial_responses: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    set_parameter_actions: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions, typing.Dict[builtins.str, typing.Any]]]]] = None,
    tag: typing.Optional[builtins.str] = None,
    webhook: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db75a87a152b7f8cd24c2d3be5187a09faedcdd7a31294efca73627fced7e4f2(
    *,
    cases: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53eb80aecaebdc977458e713ce1211a5d9197ca95c46427439048463cbf8f52f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6975b6891a26309aae4b0e4f683822cb64663f270f76644b88854dcb059cabb2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63ba6d1536101f03b92a46f6803159e214e5909a23a21ed8235423001737c1ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddaaa7fb89bac7db1d8150f44aef6f06eea2ab5b4a65189a60dd44733bb60d03(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__082baee0cf4c238f4dce7f51bbebdb8b8f2f6c67df3f1320a92855df798dd063(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__045ad4aff7ed78ed574a89ba941e704c091b91be039510be0053ba6a9c700b21(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68e1aab357642b4a2c1af950961e0062a188502923a989d3cc1dffed7c5ea929(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59ba510c502f90182dd312e64c7b31f12c037a66f6fe0227d125ffbdfb8dcb8e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6566bf124b85c9a06c7e0d30ba9c7b9c4ce57eab088d905acbeecb6de9d52618(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__413c974e061590651241af2a287f53a9f655c73b0f64269e4a2b5810b868a1d2(
    *,
    channel: typing.Optional[builtins.str] = None,
    conversation_success: typing.Optional[typing.Union[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccess, typing.Dict[builtins.str, typing.Any]]] = None,
    live_agent_handoff: typing.Optional[typing.Union[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoff, typing.Dict[builtins.str, typing.Any]]] = None,
    output_audio_text: typing.Optional[typing.Union[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioText, typing.Dict[builtins.str, typing.Any]]] = None,
    payload: typing.Optional[builtins.str] = None,
    play_audio: typing.Optional[typing.Union[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudio, typing.Dict[builtins.str, typing.Any]]] = None,
    telephony_transfer_call: typing.Optional[typing.Union[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCall, typing.Dict[builtins.str, typing.Any]]] = None,
    text: typing.Optional[typing.Union[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesText, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0011078f8283a463693b104af4cb53fd6f57ad35fcc60409af13c66c05203a03(
    *,
    metadata: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aebde3d6b786f7fb58c0fc624e474d1ceccff553080c0e0d82b7a65e86dd7fd8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7920e29938be69336c24266a87cfdfcc85815a7ea5ac92624a2b810fbf56580b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdcd5691d5c19487ed86585c88347b33448666d92a21a2c7c79b401c682996a8(
    value: typing.Optional[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesConversationSuccess],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8192a13205eca13f083f8cbaa79f0dc9b6d1e4fa15ca554e41c6ae909cb720a1(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b374800fdc47f1349d076c5a42b34da49b2a53764cff70f8d87cfc388988e709(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f9d42ed41405d4cef6fd637f62e5e6cf391942939430256eb8e3e220d7fc310(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76d126d757a871096275a3dfc877d3a40f7764e2c09b6ae5519e5ad9b3496f00(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3cac1549a88958d1238388447bed80774e4b46f9c1b346139fa87f217bd4872(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c24ce82fe152e1eee77a18287382275227eb4bced1214e28723a9a22c58370e2(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__263ebc099831bbd840b4132efec9622802980c77d9827f01d5d33003792d9b42(
    *,
    metadata: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8ec8c9943604e779f0940933bee206a72bf6603240d6220b60014787275542f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14cb60f0f3e24b38467262c77f715efb3f292070031d7a718dfa620bea13dd33(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fe6d2f0baeadbbc5d8c562002baeae65ecc50a36251268e289db5fb68995cb8(
    value: typing.Optional[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesLiveAgentHandoff],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de52003c4343cc910bdf4518f1bc3c0030e333624f4a1f6f1c2b73a89e47ed3d(
    *,
    ssml: typing.Optional[builtins.str] = None,
    text: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02e7b04aa0d39484466a38ea15e484490d84947b0ff55bb85f38198b865fb357(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22f9f20d6b443763325e39c6b070b38053ced09c5e2cb8812ca5a3a6a20a7ce0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ae069b1e14d19141dcb345241d9a75f2604b57b78d6ddf127ed5eb1c1a8d7de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8542797ccc3fb3abd92a8d8abc23e38a569c39fc642155c7c27bbf6978edf1b5(
    value: typing.Optional[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesOutputAudioText],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cac5cdbfa0b61ce6540cc4fb8e9af75c75f33c781b00e858f303ff672ab0e25d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e1fb905760292a1cedd4024ce20beba99b26e0fbec2f608ce875e95ad4db49e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7712d791bdf72cdda80b0f882b00a82c6a63653fe25bee8d0346fbe567623e12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2c69dee255f57ff09ac8b552a26bba1aa4b4165419c5d1c164fbc8281f93861(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__744a97e2329f1385bef3b89046c9e2e502dec77c1ff68a1433153cbd1828a140(
    *,
    audio_uri: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0753cb4645ea63213033758a7b35baac350f608a808b4ef6296de0746049d7be(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22f59ad2b37fc9b6f711d58851e8ffef2390cf5936938a0bdfb0f7389619d30b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86714793efcedd83cbf58515c7954820244b6cc5de54b742a58d8b2b54b7d1f8(
    value: typing.Optional[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesPlayAudio],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcc631c62f835ad7ef815276cbed7772c0821925e93e0fc4fdb3592f846d1338(
    *,
    phone_number: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0738e2e689be00c3099d4344af08b4c77b0ca9d06d7ea36b2216e75c1648a2ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b949d64290f71f50825ab6970cd92cf85750589d3e7c442ac35c72f006a5d9c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b014c3de8de8d10438e1e573db5d9395bc6b6e50953209f6037552c8350f8013(
    value: typing.Optional[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesTelephonyTransferCall],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb845cd2e37763a470724a8398ea907a821e78981076ecdb01940c409d1349b2(
    *,
    text: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bb3195addc2e0e2d487a08d2226527582423fc97a2ffb9524e6bce947362e48(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ab99c2979234ff3e742be8fdc1938a88a47aefe67ce81b327a06d1671120302(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5bd9ce82f7c73a35e2a26abf6b7177a060a8f6bab2f680a0232a8af5bcc21cb2(
    value: typing.Optional[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessagesText],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50f80746ca2bb2d342d999743e6969c6f0343890e938ac255799492d66c131a7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6ccfad873224fb7e703149e4980acebb92523eea1edfccf9f1f9ad965822d6c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxFlowTransitionRoutesTriggerFulfillmentConditionalCases, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2c18abe1c3ec735ca9f99216026376e20ee3b108eafa6bbb29c971cc5bd2b7f(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxFlowTransitionRoutesTriggerFulfillmentMessages, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9790f63e641f9957e62f860d291c3822699db77109e0304effc128e728391c8d(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c04e9ab05a22fd9648c58b89f1efbece6d247a46eb520ee5d36b36f1b6db89b(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__497871d2c57e5396079000d24da65292ac39b0a38ca44b60f20a65cd0f35283d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fde07765771fec4879fbf618b893f6a10dd429a1eb438b5d605e0e9721a51e47(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a201d5f48b8c6c3b824c2d57cb88352f3451f830f8a4a70a15c5803fff4f07c3(
    value: typing.Optional[DialogflowCxFlowTransitionRoutesTriggerFulfillment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__589eceda523524f13fe19631e4db8792050eab8dc58503d29264b706cb0b6637(
    *,
    parameter: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c353701b6c3c0e8acf0abdb15264ffb9edd25f033c864483984b623ed106cd3f(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3b36ca47ac7365c6e7c55a0ef592d558a8ef7a8ec5a4f6c2e1e5fa8c5fb5ff0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__def58bef9966a207c9c703b8ec2321b8a2831f47d2337293d61d653ac0f7e9d6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f33a8785ae8434267d4d07d54c8a74b98d73edf1be9a76c946facdf288051cd(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ebfccda72b98bf46c2c69eeaa66d8ba40dac255b607b60a2238d42c40b6ae4d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8472bb65c6bc30a762612a16bf446b1d06ed6789d3891d11c6f994b42afb972(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6caa385393286452cae36cc7267b261b2fe18b80e62c69532a0790d85d5e0175(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89abbc011e555bc638fb714f4f783bbd80015ffef425876a2a0563a4a454b2e6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__997cb4c9dcf6831288c057ec107467e43fe46e542fb1739f579933174051a809(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db15b3ee1da1ce6e9fa2e5584513aa7e497a276e5da0af847d945d73328a683d(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, DialogflowCxFlowTransitionRoutesTriggerFulfillmentSetParameterActions]],
) -> None:
    """Type checking stubs"""
    pass
